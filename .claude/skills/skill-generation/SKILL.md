---
name: skill-generation
description: Convert errors into prevention skills automatically. Use /skill-from-error command.
user-invocable: true
argument-hint: [error description]
---

# Skill Generation from Errors

Capture errors, analyze patterns, and automatically generate skill documentation.

**Purpose:** Convert ANY failure into reusable prevention skills so future work avoids the same mistakes
**Command:** `/skill-from-error`
**Meta-Skill:** This skill creates other skills

---

## Overview

When work fails or errors occur, this workflow converts failures into reusable skills. Every error makes the system smarter. No error happens twice.

**Philosophy:** Systematic learning from failures → Prevention → Continuous improvement

---

## When to Use

Trigger this workflow when:
- ✅ A task fails despite following existing skills
- ✅ An MCP tool behaves unexpectedly
- ✅ A multi-step process requires workarounds
- ✅ User reports "terrible" or "broken" output
- ✅ New error patterns discovered
- ✅ Quality gate fails repeatedly

---

## The Intelligent Workflow

### Command: `/skill-from-error`

**User triggers command and describes what happened:**

```
User: /skill-from-error
Agent: Let me help capture this error and improve the workflow.

Tell me what happened - what task were you trying to accomplish?
User: "I tried to build 9 Capo app screens but only 2 were created and they had positioning bugs"
```

**Agent automatically:**
1. Searches conversation history for task description
2. Searches docs/ for result analysis files
3. Generates error report
4. Analyzes root cause and classification
5. Checks if relevant skill exists
6. Generates new skill OR updates existing skill
7. Integrates skill into workflows
8. Offers validation

---

## The 5-Step Process

### Step 1: Capture Error Context

**Automatic Detection:**
```python
# Agent searches for:
task_description = search_conversation(
  patterns=["build", "create", "design", "implement"],
  context_window=last_100_messages
)

result_docs = glob_files(
  patterns=["docs/*failure*.md", "docs/*analysis*.md", "docs/*error*.md"]
)
```

**Structured Capture:**
Using template: [prompts/error-capture-template.md](./prompts/error-capture-template.md)

**Captures:**
- Task context (what, who, which tools/MCPs)
- Expected vs actual behavior
- Error messages
- Commands run
- Impact assessment (Critical/Major/Moderate/Minor)
- Environment details
- Artifacts (screenshots, logs)

**Output:** Error Report (markdown file in `generated/`)

---

### Step 2: Analyze Error Pattern

**Automatic Analysis:**
Using framework: [prompts/analysis-framework.md](./prompts/analysis-framework.md)

**5 Whys Root Cause:**
```
1. Why did screens have positioning bugs?
   → Elements positioned with absolute canvas coords

2. Why did that happen?
   → figma-edit MCP uses wrong coordinate system

3. Why wasn't this caught?
   → No pre-flight validation of MCP

4. Why no validation?
   → No quality gate for tool capabilities

5. Root cause: Process gap (missing quality gate)
```

**Classification:**
- Error Type: Tool limitation / Tool bug / Process gap / Knowledge gap / Architecture issue
- Scope: Tool-specific / Domain-specific / Agent-specific / Universal
- Frequency Risk: High / Medium / Low
- Prevention Opportunity: Yes (where?) / No

**Skill Recommendation:**
- Priority: Urgent / High / Medium / Low
- Type: Quality gate / Error recovery / Diagnostic / Workflow update / New skill
- Integration: Which files need updates

**Output:** Analysis Summary

---

### Step 3: Skill Matching

**Agent checks if skill already exists:**
```python
existing_skills = search_skills(
  symptom_keywords=["positioning", "absolute", "coordinate", "off-canvas"],
  tool_keywords=["figma", "figma-edit", "MCP"],
  error_type=["positioning bug"]
)

if existing_skill_found:
  action = "UPDATE existing skill"
  file = existing_skill.file_path
else:
  action = "CREATE new skill"
  file = generate_skill_path(error_classification)
```

**Decision:**
- ✅ **Update existing** if similar symptom + same tool + related error type
- ✅ **Create new** if different domain, new tool, or fundamentally different pattern

---

### Step 4: Generate Skill

**Automatic Template Selection:**
Using generator: [prompts/skill-template-generator.md](./prompts/skill-template-generator.md)

**5 Template Types:**

| Error Classification | Template | Output File |
|---------------------|----------|-------------|
| Process gap (validation missing) | Quality Gate Addition | Update `figma-quality-gates/SKILL.md` |
| Tool limitation (known workaround) | Error Recovery Pattern | Update `figma-quality-gates/prompts/error-recovery-patterns.md` |
| Specific capability needs test | Diagnostic Script | Create `figma-quality-gates/prompts/[name]-test.md` |
| Agent missed step | Agent Workflow Update | Update `.claude/agents/[agent].md` |
| New domain/major pattern | New Standalone Skill | Create `.claude/skills/[name]/SKILL.md` |

**Generated Skill Includes:**
- Problem pattern (symptoms, root cause)
- Prevention (before starting work, during work)
- Detection (how to recognize, diagnostic script)
- Recovery (step-by-step options)
- Example (before/after)
- Related skills (cross-references)
- Source metadata (error report, date, created by)

---

### Step 5: Integrate & Validate

**Automatic Integration:**
```python
if skill_type == "quality_gate":
  update_file(".claude/agents/ui-specialist.md", add_gate_reference)
  update_file(".claude/team.md", add_gate_to_phases)
  update_file("CLAUDE.md", add_gate_to_direct_work)

if skill_type == "error_recovery":
  update_file("figma-quality-gates/prompts/error-recovery-patterns.md", append_pattern)

update_file(".claude/skills/README.md", add_to_index)
```

**Validation Offer:**
```
Agent: ✅ Created .claude/skills/figma-quality-gates/SKILL.md
Agent: ✅ Updated .claude/agents/ui-specialist.md
Agent: ✅ Updated .claude/skills/README.md (skill index)

Would you like me to validate this skill by:
1. Running the diagnostic tests (if test script created)
2. Rebuilding the original scenario with the new skill
3. Just save for future use

Choose: [1/2/3]
```

---

## Skill Template Structure

When generating a new skill:

```markdown
# [Skill Name]

[One-sentence purpose]

## Context

**Created:** [Date]
**Triggered By:** [Error report link]
**Source:** [Original task/project]

## Problem Pattern

**Symptoms:**
- [Symptom 1: Observable behavior]
- [Symptom 2: Error messages]

**Root Cause:**
[Technical explanation]

**Affected Tools/MCPs:**
- [Tool 1]
- [Tool 2]

**Frequency:** High / Medium / Low

---

## Prevention

**Before starting work:**
1. [Check 1]
2. [Check 2]

**During work:**
1. [Verification 1]
2. [Verification 2]

---

## Detection

**How to recognize this issue:**
1. [Sign 1]
2. [Sign 2]

**Diagnostic Script:**
```bash
[Test commands with expected vs actual]
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

**Option 2: [Recovery Method 2]**
```bash
[Alternative approach]
```
**Time:** [X minutes]

**If all fail:**
[Escalation path]

---

## Example

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

---

## Related Skills

- [Skill 1]: [Relationship - prerequisite/alternative/follow-up]
- [Skill 2]: [Relationship]

---

## Metadata

**Source:** [Error report file]
**Date Created:** [YYYY-MM-DD]
**Created By:** [Agent/User]
**Last Updated:** [YYYY-MM-DD]
**Validated:** ✅ Yes / ⏳ Pending / ❌ No
```

---

## Examples of Generated Skills

### Example 1: Positioning Bug Skill

**Error:** Elements positioned off-canvas in figma-edit MCP
**Analysis:** Tool bug, high frequency, preventable with validation
**Template:** Diagnostic Script
**Output:** `.claude/skills/figma-quality-gates/prompts/positioning-validation.md`
**Integration:** Added to Gate 3 (First Screen Done)
**Validation:** ✅ Tested with Capo scenario, bug now caught early

### Example 2: Component Text Update Skill

**Error:** Button instance text won't update
**Analysis:** Tool limitation, workaround available
**Template:** Error Recovery Pattern
**Output:** Added Pattern 2 to `error-recovery-patterns.md`
**Integration:** Referenced in Gate 2 (Components Ready)
**Validation:** ✅ Workaround tested and documented

### Example 3: Delegation Timing Skill

**Error:** Delegated 8 screens before validating first screen
**Analysis:** Process gap, quality gate missing
**Template:** Quality Gate Addition
**Output:** Added Gate 3 requirement to `figma-quality-gates/SKILL.md`
**Integration:** Updated `.claude/agents/ui-specialist.md` workflow
**Validation:** ⏳ Pending next design task

---

## Skill Index Maintenance

**Location:** `.claude/skills/README.md`

**Entry Format:**
```markdown
| Date | Topic | File | Triggered By |
|------|-------|------|--------------|
| 2026-02-17 | Figma positioning bug | figma-quality-gates/prompts/positioning-validation.md | Capo project |
| 2026-02-17 | Component text update | figma-quality-gates/prompts/error-recovery-patterns.md | Capo project |
```

**Maintenance Schedule:**
- **Weekly:** Review new skills in `generated/` directory
- **Monthly:** Consolidate similar skills, remove duplicates
- **Quarterly:** Re-validate skills against tool updates, deprecate outdated

---

## Meta-Learning Loop

```
Error occurs
  ↓
/skill-from-error command
  ↓
Capture (auto-detect task + result)
  ↓
Analyze (5 Whys, classification)
  ↓
Match (check existing skills)
  ↓
Generate (template selection, content creation)
  ↓
Integrate (update workflows, agents)
  ↓
Validate (test with scenario)
  ↓
Future work avoids error ✅
  ↓
(If new error → repeat)
```

**Goal:** Every failure makes the system smarter. Build institutional knowledge.

---

## Quality Criteria for Generated Skills

A good skill should be:
1. **Specific:** Addresses exact error pattern with concrete symptoms
2. **Actionable:** Provides clear steps (prevention + detection + recovery)
3. **Testable:** Includes diagnostic script with pass/fail criteria
4. **Integrated:** Referenced in relevant workflows and quality gates
5. **Maintained:** Updated when new info discovered, dated, sourced

---

## Command Usage Examples

### Example 1: From Recent Conversation

```
User: /skill-from-error

Agent: Tell me what happened - what task were you trying to accomplish?

User: I was building dashboard screens but the cards weren't stacking vertically

Agent: [Analyzing conversation...]
Found task: "Build Dashboard screens with project cards"
Found issue: Cards not stacking (auto-layout problem)

Agent: [Generating error report...]
- Expected: Cards stack vertically with 16px spacing
- Actual: Cards overlap or positioned incorrectly
- Root Cause: auto-layout not working in figma-edit MCP

Agent: [Checking existing skills...]
Found existing skill: error-recovery-patterns.md - Pattern 5

Agent: [Updating skill...]
✅ Updated Pattern 5 with card stacking example
✅ Added manual positioning formula for card lists

Done! Pattern 5 now includes card stacking recovery.
```

### Example 2: From Documentation

```
User: /skill-from-error docs/design-failure-analysis.md

Agent: [Reading docs/design-failure-analysis.md...]
Found comprehensive error analysis.

Extracting key failures:
1. Wrong MCP selection (third-party vs official)
2. Positioning bugs (children offset by parent)
3. Component text update failures
4. No auto-layout support
5. Missing quality gates

Agent: [Analyzing patterns...]
Creating skills:
1. Quality Gates framework (NEW)
2. MCP capability test (NEW)
3. Positioning validation (NEW)
4. Component verification (NEW)
5. Error recovery patterns (NEW)

Agent: [Generating 5 skills...]
✅ Created .claude/skills/figma-quality-gates/SKILL.md
✅ Created .claude/skills/figma-quality-gates/prompts/mcp-capability-test.md
✅ Created .claude/skills/figma-quality-gates/prompts/positioning-validation.md
✅ Created .claude/skills/figma-quality-gates/prompts/component-verification.md
✅ Created .claude/skills/figma-quality-gates/prompts/error-recovery-patterns.md

Agent: [Integrating...]
✅ Updated .claude/agents/ui-specialist.md
✅ Updated .claude/team.md
✅ Updated CLAUDE.md
✅ Updated .claude/skills/README.md

All skills created and integrated!
```

---

## References

- **Error Capture Template:** [prompts/error-capture-template.md](./prompts/error-capture-template.md)
- **Analysis Framework:** [prompts/analysis-framework.md](./prompts/analysis-framework.md)
- **Skill Template Generator:** [prompts/skill-template-generator.md](./prompts/skill-template-generator.md)
- **Generated Skills Directory:** [generated/](./generated/)
- **Skill Index:** [.claude/skills/README.md](../README.md)

---

**Last Updated:** 2026-02-17
**Created By:** Design Agent Workflow Improvement
**Triggered By:** Need for systematic error learning
**Validated:** ⏳ Pending first use
