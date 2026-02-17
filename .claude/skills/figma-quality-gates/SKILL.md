---
name: figma-quality-gates
description: 5-gate quality framework for Figma builds. Prevents positioning bugs, component issues, and design failures.
user-invocable: false
---

# Figma Quality Gates Skill

Mandatory quality checkpoints to prevent design failures when using figma-edit MCP.

## Overview

This skill enforces a 5-gate quality process discovered from the Capo project failure analysis. Each gate MUST pass before proceeding to the next stage.

**Source:** Lessons learned from [docs/design-failure-analysis.md](/Users/federicoostan/design-agent/docs/design-failure-analysis.md)

**Target MCP:** `figma-edit` (Figma Desktop local MCP)

## The 5 Quality Gates

### Gate 1: Tool Ready
**When:** Before starting any Figma work
**Duration:** 2-3 minutes
**Owner:** UI Specialist (or Orchestrator)

#### Checklist
- [ ] Verify which Figma MCP is available (figma-edit vs official)
- [ ] Test basic operations (create frame, create rectangle, create text)
- [ ] Test component instance creation
- [ ] Test text update inside component instance
- [ ] Test auto-layout support (if available)
- [ ] Document limitations discovered

#### Testing Script
See: [prompts/mcp-capability-test.md](./prompts/mcp-capability-test.md)

#### Pass Criteria
- All basic operations work without errors
- Component instance text can be updated OR workaround documented
- Positioning behavior understood (absolute vs relative)

#### If Failed
- STOP work immediately
- Document which operations failed
- Switch to different MCP if available
- OR adjust plan to avoid broken features

---

### Gate 2: Components Ready
**When:** Before building first screen
**Duration:** 5-10 minutes
**Owner:** UI Specialist

#### Checklist
- [ ] All components from Design Brief exist in Figma
- [ ] Each component tested with instance creation
- [ ] Text overrides work for each component
- [ ] Variant switching works (if needed)
- [ ] Component keys documented for easy reference

#### Testing Script
See: [prompts/component-verification.md](./prompts/component-verification.md)

#### Pass Criteria
- Can create instance of every component needed
- Can update text/properties in instances
- No "component not found" errors

#### If Failed
- Create missing components first
- Test each component individually
- Document which components have issues
- Plan workarounds (e.g., duplicate and modify)

---

### Gate 3: First Screen Done
**When:** After building first screen completely
**Duration:** 5 minutes validation
**Owner:** UI Specialist + UX Specialist (review)

#### Checklist
- [ ] Screen built with component instances (not raw shapes)
- [ ] All interactive elements present (inputs, buttons)
- [ ] Text content updated from defaults
- [ ] Positioning works correctly (no off-canvas elements)
- [ ] Visual review matches PRD/spec
- [ ] Screenshot taken for verification

#### Validation Script
See: [prompts/positioning-validation.md](./prompts/positioning-validation.md)

#### Pass Criteria
- Screenshot shows all elements in correct positions
- All components render correctly
- No "Button" placeholder text remains
- Layout structure matches spec

#### If Failed
- Fix positioning issues
- Update component text/properties
- Take another screenshot
- **DO NOT proceed to other screens until pass**

---

### Gate 4: Mid-Point Review
**When:** After 30-50% of screens complete
**Duration:** 10 minutes review
**Owner:** UX Specialist reviews UI Specialist's work

#### Checklist
- [ ] Consistency check across completed screens
- [ ] Naming convention followed (`ScreenName/State`)
- [ ] Component usage consistent
- [ ] Flow arrows added between screens
- [ ] Annotations present on each screen

#### Review Questions
1. Do all screens use the same components for the same elements?
2. Is spacing consistent (8px grid)?
3. Are states clearly labeled in frame names?
4. Can you trace the user flow visually?

#### Pass Criteria
- All screens follow same patterns
- No major inconsistencies found
- User approved to continue

#### If Failed
- Fix inconsistencies before building more screens
- Update component usage patterns
- Realign with Design Brief

---

### Gate 5: Final Review
**When:** After all screens complete
**Duration:** 15-20 minutes
**Owner:** Full team (UX + UI + Orchestrator)

#### Checklist
- [ ] All screens from spec are built
- [ ] All states per screen exist
- [ ] Flow arrows complete
- [ ] Annotations complete (Business, Design, Dev, Question)
- [ ] Acceptance criteria met
- [ ] Export/handoff ready

#### Acceptance Criteria Template
From Design Brief:
- [ ] [Criterion 1 from brief]
- [ ] [Criterion 2 from brief]
- [ ] ...

#### Pass Criteria
- All acceptance criteria checked
- No critical issues remain
- User approves design

#### If Failed
- List all remaining issues
- Prioritize (critical vs nice-to-have)
- Fix critical issues
- Document known limitations

---

## Integration with Agent Workflows

### For UI Specialist (Subagent Mode)

**Before building:**
1. Read: `.claude/skills/figma-quality-gates/SKILL.md`
2. Execute: Gate 1 (Tool Ready) - run MCP capability tests
3. Execute: Gate 2 (Components Ready) - verify all components
4. Build first screen
5. Execute: Gate 3 (First Screen Done) - validate before continuing
6. Build remaining screens
7. Self-check: Gate 4 (Mid-Point Review) at 50%

**After building:**
8. Signal ready for Gate 5 (Final Review)
9. Invite UX Specialist to review

### For Agent Team (UX + UI Debate)

**Phase integration:**
1. UX Proposes → Define acceptance criteria
2. UI Responds → Run Gate 1 & 2 before committing
3. Debate & Converge
4. UI Builds → Gate 3 after first screen
5. UX Reviews → Gate 4 at mid-point, Gate 5 at end

---

## Error Recovery Patterns

When a gate fails, follow these patterns:

### Tool Limitations Discovered (Gate 1 failure)
**Pattern:** Adapt plan to limitations
**Actions:**
1. Document exact limitation (what fails, error message)
2. Check if official Figma MCP has this feature
3. If yes: Switch MCPs
4. If no: Plan workaround (manual Figma work, different approach)
5. Update Design Brief with constraint

### Component Issues (Gate 2 failure)
**Pattern:** Fix components before screens
**Actions:**
1. List all broken components
2. Test each individually
3. Fix or recreate broken components
4. Document which components work (green list)
5. Only use green-listed components in screens

### Positioning Bugs (Gate 3 failure)
**Pattern:** Diagnose coordinate system
**Actions:**
1. Take screenshot of frame
2. Check child element absolute positions
3. Calculate if children are offset by parent position
4. If yes: MCP has positioning bug (see [prompts/positioning-validation.md](./prompts/positioning-validation.md))
5. Switch MCP or use workaround (create children at canvas root, then move)

### Inconsistency Issues (Gate 4 failure)
**Pattern:** Establish consistency rules
**Actions:**
1. Choose the best pattern from built screens
2. Document the pattern
3. Update non-conforming screens
4. Add pattern to Design System constraints

---

## References

- **Source:** [docs/design-failure-analysis.md](../../docs/design-failure-analysis.md) (lines 638-671)
- **Component constraints:** [.claude/skills/figma/prompts/design-system-constraints.md](../figma/prompts/design-system-constraints.md)
- **Flow conventions:** [.claude/skills/figma/prompts/flow-style.md](../figma/prompts/flow-style.md)
- **Annotation style:** [.claude/skills/figma/prompts/annotation-style.md](../figma/prompts/annotation-style.md)
- **Error recovery:** [prompts/error-recovery-patterns.md](./prompts/error-recovery-patterns.md)

---

## Quick Reference Card

| Gate | When | Key Question | Pass = | Fail = |
|------|------|--------------|--------|--------|
| 1. Tool Ready | Before starting | Can this MCP do what we need? | All tests pass | Switch MCP or adapt plan |
| 2. Components Ready | Before first screen | Do all components exist and work? | All components usable | Create/fix components first |
| 3. First Screen Done | After first screen | Does this screen work correctly? | Screenshot shows correct layout | Fix before continuing |
| 4. Mid-Point Review | At 50% complete | Are screens consistent? | Same patterns across screens | Fix inconsistencies now |
| 5. Final Review | All screens done | Does it meet acceptance criteria? | All criteria checked | Fix critical issues |

---

**Last Updated:** 2026-02-17
**Created By:** Design Agent Workflow Improvement
**Triggered By:** Capo project failure analysis
