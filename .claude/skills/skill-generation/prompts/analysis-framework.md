# Error Analysis Framework

Analyze captured errors to generate actionable skills.

**Purpose:** Root cause analysis and skill recommendation
**Used By:** `/skill-from-error` command (Step 2: Analyze)

---

## Input

**Error Report:** [Link to completed error-capture-template.md or actual error doc]

---

## 1. Root Cause Analysis (5 Whys)

**Question:** Why did this error occur? (Not "what failed" but "why")

**5 Whys Technique:**

1. **Why did [the error] happen?**
   → [Answer 1]

2. **Why did [Answer 1] happen?**
   → [Answer 2]

3. **Why did [Answer 2] happen?**
   → [Answer 3]

4. **Why did [Answer 3] happen?**
   → [Answer 4]

5. **Why did [Answer 4] happen?**
   → [Root cause]

**Example (Capo positioning bug):**
1. Why did screens have positioning bugs?
   → Elements positioned off-canvas

2. Why were elements off-canvas?
   → Used absolute canvas coordinates instead of parent-relative

3. Why did that happen?
   → figma-edit MCP interprets coordinates incorrectly

4. Why wasn't this caught earlier?
   → No validation test before building all screens

5. Why no validation?
   → **Root Cause:** No quality gate for MCP capability testing

---

## 2. Classification

### Error Type
- [ ] **Tool Limitation** - MCP/API doesn't support needed feature (can't change tool code)
- [ ] **Tool Bug** - MCP/API has incorrect behavior (coordinate system wrong)
- [ ] **Process Gap** - Missing verification/quality gate (no pre-flight check)
- [ ] **Knowledge Gap** - Agent/user didn't know how to use tool correctly
- [ ] **Architecture Issue** - Wrong tool chosen for task (third-party vs official MCP)
- [ ] **Data Issue** - Incorrect input/configuration (wrong component key)
- [ ] **Timing Issue** - Action taken at wrong stage (delegated too early)

### Scope
- [ ] **Tool-specific** - Only affects [specific MCP/tool name]
- [ ] **Domain-specific** - Affects all [Figma/Atlassian/etc] work
- [ ] **Agent-specific** - Only affects [specific agent role]
- [ ] **Universal** - Could happen in any context

### Frequency Risk
- [ ] **High** - Will recur frequently without intervention (every time we use this MCP)
- [ ] **Medium** - May recur occasionally (certain types of screens/components)
- [ ] **Low** - Rare edge case (specific configuration only)

---

## 3. Prevention Opportunity

**Could this be caught earlier?**
- [ ] Yes, at tool selection stage (compare MCPs before choosing)
- [ ] Yes, with pre-flight validation (test MCP before building)
- [ ] Yes, with incremental verification (check first screen before continuing)
- [ ] Yes, with better documentation (add to skill/checklist)
- [ ] No, unpredictable until encountered

**Where in workflow?**
- [ ] Before starting (setup/planning phase) - **Gate 0**
- [ ] At beginning (tool ready check) - **Gate 1**
- [ ] During work (incremental validation) - **Gate 3**
- [ ] At end (final review) - **Gate 5**
- [ ] N/A

**Prevention method:**
- [ ] Add quality gate (pre-flight test, validation checkpoint)
- [ ] Add diagnostic script (automated test)
- [ ] Add checklist to existing skill (manual verification)
- [ ] Update agent workflow (add step to process)
- [ ] Update tool selection criteria (decision framework)

---

## 4. Recovery Pattern

**When error occurs, what's the fix?**

### Recovery Type
- [ ] **Workaround** - Can continue with different approach (time impact: [X] min)
- [ ] **Tool Switch** - Need different MCP/tool (requires: [setup time])
- [ ] **Manual Intervention** - Human must fix (time impact: [X] min)
- [ ] **Restart** - Undo and start over (time lost: [X] hours)
- [ ] **No Recovery** - Task impossible (blocker: [describe])

### Recovery Complexity
- [ ] **Simple** - One command or quick fix (< 5 min)
- [ ] **Moderate** - Multi-step workaround (5-15 min)
- [ ] **Complex** - Significant rework (> 15 min)

### Recovery Steps
[List the steps to recover from this error]

**Example (Component text update):**
1. Get instance node info
2. Find child text node ID (pattern: "I[parent]:[child]")
3. Update child text node directly
4. Repeat for each instance

**Time Impact:** +2-3 minutes per component instance

---

## 5. Skill Recommendation

**Should this become a skill?**
- [ ] **Yes - High Priority** - Critical error, frequent, preventable, high impact
- [ ] **Yes - Medium Priority** - Important but moderate frequency or lower impact
- [ ] **Yes - Low Priority** - Document for completeness, rare but valuable
- [ ] **No** - Too rare or too specific to justify skill creation

**Skill Type:**
- [ ] **Quality Gate** - Add to `figma-quality-gates/SKILL.md`
- [ ] **Error Recovery** - Add to `error-recovery-patterns.md`
- [ ] **Diagnostic** - Add validation script to `prompts/[name]-test.md`
- [ ] **Process Update** - Update agent workflow in `.claude/agents/[agent].md`
- [ ] **New Skill** - Create standalone skill for new domain `.claude/skills/[name]/SKILL.md`

**Integration Points:**
[Which files should be updated?]
- [ ] `.claude/skills/figma-quality-gates/SKILL.md` (add new gate or update existing)
- [ ] `.claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md` (add pattern)
- [ ] `.claude/agents/ui-specialist.md` (add workflow step)
- [ ] `.claude/agents/[other].md`
- [ ] `.claude/team.md` (add to collaboration protocol)
- [ ] `CLAUDE.md` (update orchestrator instructions)
- [ ] New skill: `.claude/skills/[name]/SKILL.md`
- [ ] `.claude/skills/README.md` (add to index)

---

## 6. Generalization

**Can this pattern apply beyond the specific case?**

**Specific Case:**
[Example: "figma-edit MCP has positioning bug with absolute coordinates"]

**Generalizable Principle:**
[Extract the general lesson]
[Example: "Always validate coordinate systems before building screens"]

**Other domains where this applies:**
- [Domain 1: Any MCP that creates nested elements]
- [Domain 2: Any visual design tool with parent-child relationships]
- [Domain 3: Any coordinate-based layout system]

**Meta-Pattern:**
[Highest level abstraction]
[Example: "Test tool capabilities with minimal example before full implementation"]

---

## Analysis Output

### Summary
[2-3 sentences: root cause, impact, recommendation]

**Example:**
"Root cause: figma-edit MCP uses absolute canvas coordinates instead of parent-relative. Impact: All child elements positioned off-canvas, screens unusable. Recommendation: Create quality gate (Gate 1) with MCP capability test including positioning validation."

### Skill Title
[Proposed name for the skill to be generated]

**Example:** "Figma MCP Capability Test" or "Positioning Validation Script"

### Skill Location
[Which file to update or create]

**Example:**
- Update: `.claude/skills/figma-quality-gates/prompts/mcp-capability-test.md`
- Update: `.claude/skills/figma-quality-gates/prompts/positioning-validation.md`
- Update: `.claude/skills/figma-quality-gates/SKILL.md` (add Gate 1 and Gate 3)

### Priority
- [ ] Urgent (implement now - blocking issue)
- [ ] High (implement this sprint - high frequency)
- [ ] Medium (implement when time allows - moderate impact)
- [ ] Low (document for reference - rare occurrence)

---

## Decision Matrix

| Error Type | Frequency | Prevention Opportunity | Skill Type |
|-----------|-----------|----------------------|-----------|
| Tool Bug | High | Yes (pre-flight test) | Quality Gate + Diagnostic |
| Tool Limitation | High | Yes (workaround doc) | Error Recovery |
| Process Gap | Any | Yes (add step) | Quality Gate or Workflow Update |
| Knowledge Gap | Medium | Yes (documentation) | Skill Update (add example) |
| Architecture | Low | Yes (tool selection) | Tool Selection Guide |
| Timing | Medium | Yes (checklist) | Workflow Update |

---

## Next Step

**Proceed to:** [skill-template-generator.md](./skill-template-generator.md)

**With:**
- Root cause identified
- Error classified
- Skill type determined
- Integration points listed
- Priority assigned

---

**Framework Version:** 1.0
**Last Updated:** 2026-02-17
**Used By:** `/skill-from-error` command (Step 2)
