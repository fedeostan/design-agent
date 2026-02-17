# Error Capture Template

Fill this out when an error occurs to enable skill generation.

**Purpose:** Structured error documentation for automatic skill generation
**Used By:** `/skill-from-error` command (Step 1: Capture)

---

## Basic Info

**Date:** [YYYY-MM-DD]
**Agent/User:** [Who encountered the error]
**Project:** [Project name, if applicable]

---

## Task Context

**What were you trying to do?**
[1-2 sentences describing the goal]

Example: "Build 9 Capo app screens (Auth, Onboarding, Dashboard) from PRD into Figma"

**Which agent/role?**
- [ ] Orchestrator
- [ ] PM Agent
- [ ] Research Specialist
- [ ] UX Specialist
- [ ] UI Specialist
- [ ] Solution Architect
- [ ] User (manual work)

**Which tools/MCPs involved?**
- [ ] figma-edit MCP (local desktop)
- [ ] figma MCP (official, https://mcp.figma.com/mcp)
- [ ] Atlassian MCP
- [ ] Notion MCP
- [ ] Other: [specify]

---

## Expected vs Actual

**Expected Behavior:**
[What should have happened?]

Example: "9 complete screens with component instances, proper positioning, flow arrows"

**Actual Behavior:**
[What actually happened?]

Example: "Only 2 screens created, positioning bugs (elements off-canvas), component text not updated"

**Error Messages (if any):**
```
[Paste exact error text]
```

---

## Commands Run

**Tools called:**
```bash
create_frame(name: "Auth/Login", x: 0, y: 0, width: 390, height: 844)
# Result: Frame created successfully, node ID: 24:2

create_rectangle(parentId: "24:2", x: 155, y: 80, width: 80, height: 40, ...)
# Result: Rectangle created but positioned incorrectly (off-canvas)

create_component_instance(componentKey: "Button/Default", ...)
# Result: Instance created but text still says "Button"
```

**Files involved:**
- [File 1]: [Description]
- [File 2]: [Description]

---

## Impact Assessment

**What broke as a result?**
- [ ] Task completely failed
- [ ] Task partially completed (with workarounds)
- [ ] Output was poor quality
- [ ] Wasted time/effort (how much: [X] minutes/hours)

**Who was affected?**
- [ ] End user saw broken output
- [ ] Developer received bad handoff
- [ ] Blocked other work
- [ ] Just wasted agent time

**Impact Level:**
- [ ] **Critical** - Unusable output, complete failure, task cannot be completed
- [ ] **Major** - Significant quality issues, manual rework needed, workaround time-consuming
- [ ] **Moderate** - Workaround available but adds time, partial functionality
- [ ] **Minor** - Small inconvenience, easy fix, doesn't block progress

---

## Recovery

**How was it fixed (if at all)?**
[Describe the solution or workaround]

Example: "Found child text node IDs, updated text manually. Used absolute coordinates for positioning."

**Time to recover:**
[X minutes/hours]

Example: "Added 3+ hours for workarounds and debugging"

**Could this have been prevented?**
- [ ] Yes - [How? Example: "Pre-flight MCP capability test"]
- [ ] No - Unpredictable failure
- [ ] Uncertain

---

## Pattern Recognition

**Have you seen this before?**
- [ ] First time
- [ ] Happened once before
- [ ] Recurring pattern (happened [X] times)

**Related errors:**
- [Link to similar error report, if any]

**Suspected root cause:**
[Your hypothesis about why this happened]

Example: "figma-edit MCP uses absolute canvas coordinates instead of parent-relative coordinates"

---

## Environment Details

**MCP Version/Source:**
- [ ] figma-edit: local desktop, Figma plugin
- [ ] figma: https://mcp.figma.com/mcp
- [ ] Other: [details]

**File/Project Details:**
- Figma file: [URL or name]
- Node ID(s): [if relevant, e.g., "24:2, 24:17"]
- Components involved: [list, e.g., "Button/Default, Input/Default"]

**System:**
- Platform: [darwin/linux/windows]
- Figma Desktop version: [if applicable]
- MCP configuration: [relevant .mcp/config.json details]

---

## Artifacts

**Screenshots:**
[Attach or link to screenshots showing the issue]

Example: "Screenshot of Auth/Login screen showing elements off-canvas"

**Logs:**
[Attach relevant logs]

**Output files:**
[Link to generated files, docs, or analysis]

Example:
- `docs/design-failure-analysis.md` - Comprehensive error analysis
- `docs/actual-vs-expected-screens.md` - Comparison of what was built

---

## Next Steps

**Immediate action taken:**
- [x] [Action 1: Documented error in design-failure-analysis.md]
- [x] [Action 2: Analyzed root cause]
- [ ] [Action 3: Create skills to prevent recurrence - pending]

**Skill generation needed:**
- [ ] Yes - This should become a **prevention skill** (quality gate)
- [ ] Yes - This should become a **recovery pattern** (error workaround)
- [ ] Maybe - Unclear if pattern will recur
- [ ] No - One-off edge case

**Priority:**
- [ ] Urgent - Critical failure, blocks all work
- [ ] High - Significant impact, affects multiple projects
- [ ] Medium - Important but infrequent
- [ ] Low - Minor issue, rare occurrence

---

## Notes

[Any additional context or observations]

Example: "This error would have been caught with pre-flight MCP testing. Should create quality gate for tool validation before starting design work."

---

**Template Version:** 1.0
**Last Updated:** 2026-02-17
**Used By:** `/skill-from-error` command
