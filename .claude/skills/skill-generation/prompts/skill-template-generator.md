# Skill Template Generator

Generate skill documentation from error analysis.

**Purpose:** Convert error analysis into actionable skill documentation
**Used By:** `/skill-from-error` command (Step 3: Generate)

---

## Input

**Error Report:** [Link to error-capture-template.md or error doc]
**Analysis:** [Link to completed analysis-framework.md output]

---

## Template Selection Decision Tree

```
Error Classification
  │
  ├─ Process Gap + Prevention Opportunity
  │   └─ **Template A: Quality Gate Addition**
  │       File: Update .claude/skills/figma-quality-gates/SKILL.md
  │
  ├─ Tool Limitation + Workaround Available
  │   └─ **Template B: Error Recovery Pattern**
  │       File: Update .claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md
  │
  ├─ Tool Bug + Needs Validation Test
  │   └─ **Template C: Diagnostic Script**
  │       File: Create .claude/skills/figma-quality-gates/prompts/[name]-test.md
  │
  ├─ Agent Behavior + Workflow Gap
  │   └─ **Template D: Agent Workflow Update**
  │       File: Update .claude/agents/[agent-name].md
  │
  └─ New Domain or Major Pattern
      └─ **Template E: New Standalone Skill**
          File: Create .claude/skills/[skill-name]/SKILL.md
```

---

## Template A: Quality Gate Addition

**Use when:** Prevention opportunity identified, should be caught early

**Output:** Update `.claude/skills/figma-quality-gates/SKILL.md`

**Format:**
```markdown
### Gate [N]: [Gate Name]
**When:** [Stage in workflow - Before starting / Before first screen / After first screen / At 50% / After all screens]
**Duration:** [X minutes]
**Owner:** [Agent role - UI Specialist / UX Specialist / Orchestrator]

#### Checklist
- [ ] [Check 1: Specific actionable item]
- [ ] [Check 2: Specific actionable item]
- [ ] [Check 3: Specific actionable item]

#### Testing Script
See: [prompts/[new-test-script].md](./prompts/[new-test-script].md)

#### Pass Criteria
- [Criterion 1: Measurable success condition]
- [Criterion 2: Measurable success condition]

#### If Failed
- [Action 1: What to do if check fails]
- [Action 2: Escalation path]
```

**Also Create:** Corresponding test script using Template C

---

## Template B: Error Recovery Pattern

**Use when:** Recovery workaround discovered, tool limitation identified

**Output:** Update `.claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md`

**Format:**
```markdown
## Pattern [N]: [Pattern Name]

**Symptoms:**
- [Symptom 1: Observable behavior]
- [Symptom 2: Error messages or visual signs]

**Root Cause:**
[Technical explanation from analysis]

**Diagnosis:**
[How to identify this issue - specific tests or checks]

**Recovery:**

**Option 1: [Method Name]**
```bash
[Step-by-step commands or actions]
```
**Time Impact:** +[X] minutes

**Option 2: [Alternate Method]**
```bash
[Alternative approach]
```
**Time Impact:** +[X] minutes

**If both fail:**
- [Escalation path: Switch tool, manual work, or stop]

**Decision Tree:**
```
[When to use Option 1 vs Option 2 vs escalate]
```
```

**Example from Analysis:**
- Symptoms: Component text won't update
- Root Cause: Text is in child node, not instance
- Recovery: Find child node ID, update directly
- Time: +2-3 min per instance

---

## Template C: Diagnostic Script

**Use when:** Need validation test for specific tool capability

**Output:** Create `.claude/skills/figma-quality-gates/prompts/[name]-test.md`

**Format:**
```markdown
# [Capability Name] Test Script

Test [tool/MCP] for [specific capability] before starting work.

**Purpose:** [Why this test is needed]
**Duration:** [X minutes]
**Target:** [Which MCP/tool]

---

## Test [N]: [Test Name]

**Test:** [What to test]

```bash
[Command to run with parameters]

# Expected: [Expected result]
# Failure: [Failure symptoms]
```

**Result:** ✅ Pass / ❌ Fail
**[Measurement]:** [Value to record - e.g., Position, Node ID]

---

## Test Summary

| Test | Status | Notes |
|------|--------|-------|
| [Test 1] | ✅/❌ | |
| [Test 2] | ✅/❌ | |

**Overall Grade:** A (all pass) / B (minor issues) / C (major issues) / F (critical failure)

**Recommendation:**
- **Grade A:** [Advice - e.g., "Proceed with confidence"]
- **Grade B:** [Advice - e.g., "Proceed with documented workarounds"]
- **Grade C:** [Advice - e.g., "Consider switching MCP"]
- **Grade F:** [Advice - e.g., "STOP - Use different MCP"]

---

## Discovered Limitations

List any limitations:
1. [Limitation 1]

## Workarounds

List workarounds:
1. [Workaround 1]

---

**Source:** [Error report link]
**Last Updated:** [YYYY-MM-DD]
**Validated With:** [Which MCP/tool version]
```

---

## Template D: Agent Workflow Update

**Use when:** Process gap in agent behavior, missing step in workflow

**Output:** Update `.claude/agents/[agent-name].md`

**Format:**
```markdown
### [Phase N]. [Workflow Step Name]

[Description of what to do at this stage]

**Validation:**
- [ ] [Check 1: What to verify]
- [ ] [Check 2: What to verify]

**Before continuing:**
- Verify [criterion from quality gate]
- If failed: [action - stop, fix, escalate]
```

**Integration Points:**
- Add to specific agent file (ui-specialist, ux-specialist, etc.)
- Add cross-reference to quality gates skill
- Update phase numbers if inserting new phase

**Example:**
```markdown
### Phase 0: Pre-Flight Quality Gates

**REQUIRED before building:**
- Read: .claude/skills/figma-quality-gates/SKILL.md
- Execute: Gate 1 (Tool Ready)
- Execute: Gate 2 (Components Ready)
- Document: Any limitations discovered

**Pass criterion:** MCP capabilities sufficient for proposed design
```

---

## Template E: New Standalone Skill

**Use when:** New domain, major pattern, or fundamentally different error type

**Output:** Create `.claude/skills/[skill-name]/SKILL.md`

**Full Template:**
```markdown
# [Skill Name]

[One-sentence purpose]

## Overview

[2-3 paragraphs: What this skill is, when to use it, who uses it]

## Context

**Created:** [YYYY-MM-DD]
**Triggered By:** [Error report link or project]
**Source:** [Original task that revealed the need]

---

## Problem Pattern

**Symptoms:**
- [Symptom 1: Observable behavior]
- [Symptom 2: Error messages]
- [Symptom 3: Impact]

**Root Cause:**
[Technical explanation]

**Affected Tools/MCPs:**
- [Tool 1]
- [Tool 2]

**Frequency:** High / Medium / Low

---

## Prevention

**Before starting work:**
1. [Check 1: Pre-work validation]
2. [Check 2: Pre-work setup]

**During work:**
1. [Verification 1: Incremental check]
2. [Verification 2: Quality gate]

---

## Detection

**How to recognize this issue:**
1. [Sign 1: Early warning]
2. [Sign 2: Observable problem]

**Diagnostic Script:**
```bash
[Test commands with expected vs actual results]
```

**Result:** ✅ Pass / ❌ Fail

---

## Recovery

**If this issue occurs:**

**Option 1: [Recovery Method 1]**
```bash
[Step-by-step commands or actions]
```
**Time:** [X minutes]
**Pros:** [Advantages]
**Cons:** [Limitations]

**Option 2: [Recovery Method 2]**
```bash
[Alternative approach]
```
**Time:** [X minutes]
**Pros:** [Advantages]
**Cons:** [Limitations]

**If all fail:**
[Escalation path]

---

## Example

**Scenario:** [Concrete use case]

**Before (broken approach):**
```
[Code or description of failed approach]

Result: [What went wrong]
```

**After (working approach):**
```
[Code or description of successful approach]

Result: [Success outcome]
```

**Lessons:**
- [Lesson 1]
- [Lesson 2]

---

## Integration with Workflows

**For [Agent Role]:**
[When and how this agent uses this skill]

**For [Another Agent Role]:**
[When and how they use it]

---

## Related Skills

- [Skill 1]: [Relationship - prerequisite/alternative/follow-up]
- [Skill 2]: [Relationship]

---

## References

- **Tool documentation:** [Link]
- **Related error reports:** [Links]
- **Source analysis:** [Link to error doc]

---

## Metadata

**Source:** [Error report file]
**Date Created:** [YYYY-MM-DD]
**Created By:** [Agent/User who triggered /skill-from-error]
**Last Updated:** [YYYY-MM-DD]
**Validated:** ✅ Yes / ⏳ Pending / ❌ No
**Validation Notes:** [How was this tested]
```

---

## Content Generation Process

### 1. Fill Template

Copy selected template and populate with details from error analysis:
- **Symptoms** ← from error report "Actual Behavior"
- **Root cause** ← from analysis "5 Whys" final answer
- **Recovery steps** ← from error report "How was it fixed"
- **Prevention** ← from analysis "Prevention Opportunity"

### 2. Add Examples

**Include:**
- "Before" example (broken approach) from error report
- "After" example (working approach) from recovery
- Real error messages from error report
- Screenshots if available

### 3. Add Cross-References

**Link to:**
- Related skills (if similar pattern exists)
- Source error report (for context)
- Quality gates (if prevention is gate-based)
- Agent workflows (if process-based)

### 4. Add Metadata

```markdown
---
**Source:** [Link to error-capture-template.md or error doc]
**Date Created:** [YYYY-MM-DD from error report]
**Created By:** [From error report: agent/user]
**Last Updated:** [YYYY-MM-DD when skill generated]
**Validated:** ⏳ Pending (will be ✅ after validation)
---
```

---

## Integration Automation

After generating skill, auto-update these files:

### If Quality Gate Created:
```python
update_file(
  ".claude/agents/ui-specialist.md",
  insert_before_line=43,  # Phase 0
  content="Read: .claude/skills/figma-quality-gates/SKILL.md\nExecute: Gate [N]"
)

update_file(
  ".claude/team.md",
  section="Phase 0: Tool Readiness",
  add="Execute: Gate [N]"
)

update_file(
  "CLAUDE.md",
  section="Before Any Design Work",
  add_step="Run Gate [N]"
)
```

### If Error Recovery Added:
```python
update_file(
  ".claude/skills/figma-quality-gates/SKILL.md",
  section="Error Recovery Patterns",
  add_reference="See: prompts/error-recovery-patterns.md - Pattern [N]"
)
```

### Always:
```python
update_file(
  ".claude/skills/README.md",
  section="Skill Index",
  add_row={
    "date": today,
    "topic": skill_title,
    "file": skill_file_path,
    "triggered_by": error_project
  }
)
```

---

## Validation Checklist

After generating skill:

### Completeness
- [ ] Problem clearly described with specific symptoms
- [ ] Symptoms listed as observable behaviors
- [ ] Diagnostic method provided (test script or checks)
- [ ] Recovery steps actionable (copy-paste ready)
- [ ] Examples included (before/after)
- [ ] Cross-references added (related skills, sources)
- [ ] Metadata complete (source, dates, validation status)

### Clarity
- [ ] Can agent understand without full error context?
- [ ] Commands copy-paste ready (no placeholders undefined)?
- [ ] Decision points clear (if X then Y logic)?
- [ ] Pass/fail criteria measurable?

### Integration
- [ ] Referenced in relevant agent workflow?
- [ ] Added to quality gate (if prevention skill)?
- [ ] Added to error recovery (if workaround)?
- [ ] Skill index updated?
- [ ] Cross-references bidirectional (skill ↔ workflow)?

---

## Output Summary

**Generated:**
- [ ] Skill file created/updated: [path]
- [ ] Integration updates applied: [list files]
- [ ] Skill index entry added: ✅

**Validation Status:**
- [ ] Tested with original error scenario: ✅/⏳/❌
- [ ] Prevented recurrence: ✅/⏳/❌
- [ ] Generalized correctly: ✅/⚠️ Too specific/❌ Too vague

---

**Generator Version:** 1.0
**Last Updated:** 2026-02-17
**Used By:** `/skill-from-error` command (Step 3)
