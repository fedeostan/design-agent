---
name: text-to-figma
description: End-to-end pipeline from plain text description to Figma screens
user-invocable: true
---

# Text-to-Figma Pipeline

Transform a plain text description into production-ready Figma screens through a 9-stage orchestrated pipeline.

**Input:** Text description of what to design (e.g., "Design a sign-in flow for a fitness app")
**Output:** Figma screens with auto-layout, design tokens bound, and binding checklist

---

## Quick Reference

| Stage | Owner | Input | Output | Blocker? |
|-------|-------|-------|--------|----------|
| 0. Pre-Flight | Orchestrator | Figma file key | Pre-flight summary | YES — blocks all |
| 1. PM | PM subagent | Text description | Design Brief | No |
| 2. Research | Research subagent | Design Brief | Competitive Analysis | No |
| 3. UX+UI Debate | Agent Team | Brief + Research | Screen specs + Figma screens | No |
| 4. Token Sync | Orchestrator | tokens.json + file key | Figma variables | Only if PAT available |
| 5. HTML Generation | Orchestrator/UI | Screen specs | HTML files | No |
| 6. Playwright Capture | Orchestrator | HTML files + capture IDs | Figma frames | No |
| 7. Post-Capture QA | Orchestrator | Captured frame IDs | Verification report | YES — blocks binding |
| 8. Binding Checklist | Orchestrator | Metadata + tokens + components | Binding checklist | No |

---

## Stage 0: Pre-Flight

**Read:** `prompts/pre-flight.md`

Run 6 prerequisite checks before anything else. Produces a pre-flight summary block that flows into all subsequent stages.

**BLOCKS the pipeline until all required checks pass.**

---

## Stage 1: PM — Requirements

**Delegate to:** PM subagent (`pm.md`)

Pass the user's text description. PM produces a Design Brief with:
- Problem statement
- User stories
- Success metrics
- Scope (in/out)
- Target screens list

---

## Stage 2: Research — Competitive Analysis

**Delegate to:** Research subagent (`research-specialist.md`)

Pass the Design Brief. Research produces:
- 3-5 competitor screenshots/analysis
- Pattern recommendations
- UX best practices for this domain

---

## Stage 3: UX + UI Debate — Screen Design

**Delegate to:** Agent Team (`.claude/team.md`)

Pass Brief + Research output. The team:
1. UX proposes screen structure and flow
2. UI challenges/refines from visual perspective
3. They debate (max 3 rounds), converge
4. UI produces final screen specifications
5. UX reviews

**Output:** Detailed screen specs ready for HTML generation.

---

## Stage 4: Token Sync

**Run:** Token sync script (if Figma PAT is available)

```bash
python3 scripts/sync-tokens-to-figma.py \
    --tokens tokens.json \
    --file-key <FILE_KEY> \
    --token <FIGMA_PAT>
```

Verify with `get_variable_defs(fileKey)`.

**Skip if:** No Figma PAT available. Mark `tokens_synced: false` in pre-flight summary.

---

## Stage 5: HTML Generation

**Read:** `.claude/skills/figma/prompts/code-to-canvas-workflow.md` (HTML Template section)

For each screen from Stage 3, generate a minimal flat HTML file following these rules:
- Max 3 nesting levels
- Semantic class on EVERY element
- `display: flex` on EVERY container
- Exact token values from `tokens.json`
- Include capture script in `<head>`
- Viewport meta tag matching pre-flight dimensions

Save as `<screen-name>.html` in project root.

---

## Stage 6: Playwright Capture

**Read:** `prompts/playwright-capture.md`

For each HTML file:
1. Start local server (`python3 -m http.server 8080`)
2. Call `generate_figma_design` to get capture ID
3. Execute the 5-step Playwright sequence (close → resize → navigate → wait → screenshot)
4. Record the new frame's node ID

**Critical:** `browser_resize` BEFORE `browser_navigate`.

**Fallback:** If Playwright unavailable, guide user through manual incognito capture.

---

## Stage 7: Post-Capture QA

**Read:** `prompts/post-capture-verification.md`

For each captured frame, run the 5-check quality gate:
1. Frame dimensions
2. Phantom frames
3. Auto-layout
4. Layer names
5. Nesting depth

**BLOCKS binding** until all checks pass (or only minor warnings remain).

If any check fails → fix HTML → recapture → re-verify.

---

## Stage 8: Binding Checklist

**Read:** `prompts/binding-checklist-template.md`

Generate a binding checklist for each screen:
- **Variable bindings** (conditional — only if `tokens_synced: true`)
- **Component swaps** (conditional — only if `components_available: true`)
- **Manual fixes** (from post-capture QA findings)

Present checklist to user for execution in Figma UI.

---

## Pipeline Entry Points

The pipeline can be entered at any stage:

| Scenario | Start At |
|----------|----------|
| "Design X from scratch" | Stage 0 (full pipeline) |
| "I have a brief, design it" | Stage 3 (skip PM + Research) |
| "Build this HTML screen in Figma" | Stage 5 (skip design stages) |
| "Capture this HTML file" | Stage 6 (capture only) |
| "Check my Figma capture quality" | Stage 7 (verification only) |

---

## Known Limitations

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| No granular Figma write tools | Can't programmatically bind variables or swap components | User executes binding checklist manually in Figma UI |
| Capture script resolves CSS variables | Token names lost in capture | Use exact hex/px values, bind after capture |
| Layer names from CSS classes only | Unnamed elements get generic names | Put semantic class on every HTML element |
| Playwright viewport must be set before navigate | Wrong viewport = wrong frame size | Always resize before navigate (enforced in Stage 6) |
| Browser extensions inject phantom frames | Extra 0x0 frames in Figma | `browser_close()` for clean session, or manual incognito |

---

## Related Skills

- **Code-to-Canvas:** `.claude/skills/figma/prompts/code-to-canvas-workflow.md` — detailed HTML-to-Figma reference
- **Quality Gates:** `.claude/skills/figma-quality-gates/SKILL.md` — 5-gate framework for direct Figma work
- **Design System:** `.claude/skills/figma/prompts/design-system-constraints.md` — component and naming rules
