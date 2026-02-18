# Pre-Flight Checklist (Stage 0)

**Purpose:** Verify all prerequisites before starting the Text-to-Figma pipeline.
**Rule:** Pipeline is BLOCKED until all 6 checks pass.

---

## Checks

### 1. Figma MCP Access
**Test:** Call `get_metadata` on the target Figma file.
- **Pass:** Returns file name and document structure
- **Fail:** MCP not connected or file key invalid → fix before continuing

### 2. Token Sync Status
**Test:** Run `get_variable_defs(fileKey)` and compare against `tokens.json`.
- **Pass:** Variable collection "Tokens" exists with matching values
- **Synced but stale:** Values differ → re-run `python3 scripts/sync-tokens-to-figma.py`
- **Not synced:** No "Tokens" collection → run sync script first
- **Note:** If sync is skipped (no PAT available), mark `tokens_synced: false` — binding checklist will adapt

### 3. Component Inventory
**Test:** Call `get_design_context(fileKey)` or check local components.
- **Pass:** List of available components documented
- **Empty:** No components available → mark `components_available: false` — binding checklist will skip component swaps
- **Record:** Save component list for binding checklist generation

### 4. Viewport Dimensions
**Test:** Confirm target device dimensions.
- **Default:** 390x844 (iPhone 14/15 Pro)
- **Custom:** User specifies alternative → record in pre-flight summary
- **Used by:** HTML template `<meta viewport>`, Playwright `browser_resize`, post-capture verification

### 5. Playwright Availability
**Test:** Check if Playwright MCP tools are available (`browser_navigate`, `browser_resize`, `browser_take_screenshot`).
- **Available:** Will use automated capture flow
- **Unavailable:** Will fall back to manual capture (user opens incognito browser)
- **Record:** `playwright_available: true/false`

### 6. Required Inputs
**Test:** Verify the pipeline has what it needs to start.
- **Figma file key:** Extracted from URL or provided directly
- **Design brief or description:** Text input describing what to design
- **Target screens:** List of screens to produce (can be determined by PM/UX stages)

---

## Pre-Flight Summary Block

After running all checks, produce this summary and pass it to all subsequent stages:

```
PRE-FLIGHT SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Figma file:        [file key]
Figma access:      ✅ / ❌
Tokens synced:     ✅ / ❌ (skipped)
Components:        ✅ [count] available / ❌ none
Viewport:          [width]x[height]
Playwright:        ✅ / ❌ (manual fallback)
Input:             [brief description of input]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Blocking Rules

| Check | Can Skip? | Impact if Skipped |
|-------|-----------|-------------------|
| Figma MCP Access | No | Cannot produce any output |
| Token Sync | Yes | Binding checklist omits variable bindings |
| Component Inventory | Yes | Binding checklist omits component swaps |
| Viewport Dimensions | No | Wrong frame sizes, failed post-capture QA |
| Playwright | Yes | Falls back to manual capture |
| Required Inputs | No | Pipeline has nothing to design |
