# Design Agent Skills Index

Central index of all skills for the Design Agent system.

**Purpose:** Track all skills, when to use them, and maintenance schedule
**Last Updated:** 2026-02-17

---

## Skill Categories

### 1. Figma Skills
**Domain:** Figma design work (read & write)
**When to Use:** Any Figma-related task

| Skill | Purpose | Key Files | Owner |
|-------|---------|-----------|-------|
| **Figma** | Core Figma tool reference and setup | `figma/SKILL.md` | UI Specialist |
| **Figma Quality Gates** | Prevent design failures with 5 quality checkpoints | `figma-quality-gates/SKILL.md` + 4 prompts | UI Specialist |

**Related Prompts:**
- `figma/prompts/design-system-constraints.md` - Component usage rules, 8px grid, naming
- `figma/prompts/annotation-style.md` - Note component patterns (Business/Design/Dev/Question)
- `figma/prompts/flow-style.md` - Arrow and flow layout conventions
- `figma-quality-gates/prompts/mcp-capability-test.md` - Gate 1 diagnostic (6 tests)
- `figma-quality-gates/prompts/component-verification.md` - Gate 2 checklist
- `figma-quality-gates/prompts/positioning-validation.md` - Gate 3 diagnostic (coordinate bugs)
- `figma-quality-gates/prompts/error-recovery-patterns.md` - 8 recovery patterns

---

### 2. Research Skills
**Domain:** Design analysis and evaluation
**When to Use:** Competitive analysis, heuristic evaluation, accessibility audit, cognitive walkthrough

| Skill | Purpose | Key Files | Owner |
|-------|---------|-----------|-------|
| **Research** | Evaluation frameworks and templates | `research/SKILL.md` | Research Specialist |

**Templates Included:**
- Heuristic Evaluation (Nielsen's 10 heuristics, severity rating 0-4)
- Competitive Analysis Framework
- WCAG 2.1 AA Quick Audit Checklist
- Cognitive Walkthrough Template

---

### 3. Requirements Skills
**Domain:** Requirements gathering and documentation
**When to Use:** New feature kickoff, design brief creation, user story writing

| Skill | Purpose | Key Files | Owner |
|-------|---------|-----------|-------|
| **Requirements** | Design brief and user story templates | `requirements/SKILL.md` | PM Agent |

**Templates Included:**
- Design Brief Template
- User Story Writing Guide (INVEST criteria)
- Acceptance Criteria Patterns (Given-When-Then format)
- Stakeholder Priority Matrix (MoSCoW method)

---

### 4. Handoff Skills
**Domain:** Developer handoff and implementation specs
**When to Use:** Design complete, preparing for implementation

| Skill | Purpose | Key Files | Owner |
|-------|---------|-----------|-------|
| **Handoff** | Implementation specs and Code Connect | `handoff/SKILL.md` | Solution Architect |

**Templates Included:**
- Implementation Spec Template
- Code Connect Workflow
- Design Token Guide (4 categories: colors, typography, spacing, elevation)
- Handoff Checklist

---

### 5. Pipeline Skills
**Domain:** End-to-end design pipelines
**When to Use:** Full text-to-Figma workflows, automated capture, post-capture QA

| Skill | Purpose | Key Files | Owner |
|-------|---------|-----------|-------|
| **Text-to-Figma** | 9-stage pipeline from text to Figma screens | `text-to-figma/SKILL.md` + 4 prompts | Orchestrator |

**Command:** `/text-to-figma` (invokes full pipeline)

**Sub-Prompts:**
- `text-to-figma/prompts/pre-flight.md` - Stage 0 prerequisites (6 checks, blocks pipeline)
- `text-to-figma/prompts/playwright-capture.md` - Automated Playwright capture (viewport fix)
- `text-to-figma/prompts/post-capture-verification.md` - 5-check quality gate
- `text-to-figma/prompts/binding-checklist-template.md` - Phase 3 variable/component binding

---

### 6. Meta-Skills
**Domain:** Workflow improvement and error learning
**When to Use:** Capturing errors, generating new skills

| Skill | Purpose | Key Files | Owner |
|-------|---------|-----------|-------|
| **Skill Generation** | Convert errors into prevention skills | `skill-generation/SKILL.md` + 3 prompts | Orchestrator |

**Command:** `/skill-from-error` (intelligent error capture and skill generation)

**Process:**
1. Capture error context (auto-detect task + result)
2. Analyze with 5 Whys and classification
3. Match existing skills or create new
4. Generate skill from templates
5. Integrate into workflows
6. Validate prevention

**Templates:**
- Error Capture Template
- Analysis Framework (5 Whys, classification, prevention opportunity)
- Skill Template Generator (5 template types: quality gate, error recovery, diagnostic, workflow update, new skill)

---

## Skill Index (All Skills)

| Date Created | Topic | File | Triggered By | Status |
|--------------|-------|------|--------------|--------|
| 2026-02-17 | Figma Quality Gates | `figma-quality-gates/SKILL.md` | Capo project failure | ✅ Active |
| 2026-02-17 | MCP Capability Test | `figma-quality-gates/prompts/mcp-capability-test.md` | Capo positioning bugs | ✅ Active |
| 2026-02-17 | Component Verification | `figma-quality-gates/prompts/component-verification.md` | Capo missing components | ✅ Active |
| 2026-02-17 | Positioning Validation | `figma-quality-gates/prompts/positioning-validation.md` | Capo coordinate bugs | ✅ Active |
| 2026-02-17 | Error Recovery Patterns | `figma-quality-gates/prompts/error-recovery-patterns.md` | Capo 8 failure patterns | ✅ Active |
| 2026-02-17 | Skill Generation | `skill-generation/SKILL.md` | Need for systematic learning | ✅ Active |
| [Earlier] | Figma Core | `figma/SKILL.md` | Initial setup | ✅ Active |
| [Earlier] | Research | `research/SKILL.md` | Initial setup | ✅ Active |
| [Earlier] | Requirements | `requirements/SKILL.md` | Initial setup | ✅ Active |
| [Earlier] | Handoff | `handoff/SKILL.md` | Initial setup | ✅ Active |
| 2026-02-18 | Text-to-Figma Pipeline | `text-to-figma/SKILL.md` | Capo pipeline test | ✅ Active |
| 2026-02-18 | Pre-Flight Checklist | `text-to-figma/prompts/pre-flight.md` | Capo pipeline test | ✅ Active |
| 2026-02-18 | Playwright Capture | `text-to-figma/prompts/playwright-capture.md` | Capo 500px bug | ✅ Active |
| 2026-02-18 | Post-Capture Verification | `text-to-figma/prompts/post-capture-verification.md` | Capo QA gaps | ✅ Active |
| 2026-02-18 | Binding Checklist | `text-to-figma/prompts/binding-checklist-template.md` | Capo binding gaps | ✅ Active |

**Status Legend:**
- ✅ Active - Currently in use
- ⏳ Pending - Created but not validated
- ⚠️ Deprecated - Outdated, needs update
- ❌ Archived - No longer relevant

---

## How to Use This Index

### For Agents
1. **Before starting a task:** Check relevant skill category
2. **During task:** Reference prompts for constraints and patterns
3. **After task:** If error occurred, use `/skill-from-error` to capture

### For Users
1. **View all skills:** Browse skill categories above
2. **Find specific skill:** Use table to locate file
3. **Track new skills:** Check "Skill Index" table for recent additions

### For Maintenance
1. **Weekly:** Review `skill-generation/generated/` for new auto-generated skills
2. **Monthly:** Consolidate similar skills, remove duplicates
3. **Quarterly:** Re-validate skills against tool updates, deprecate outdated

---

## Skill Naming Conventions

**Pattern:** `[domain]/SKILL.md` for main skills
**Pattern:** `[domain]/prompts/[specific-name].md` for supporting prompts

**Examples:**
- `figma/SKILL.md` - Main Figma skill
- `figma/prompts/design-system-constraints.md` - Specific constraint document
- `figma-quality-gates/prompts/mcp-capability-test.md` - Specific diagnostic test

---

## Adding New Skills

### Manual Addition
1. Create skill file: `.claude/skills/[name]/SKILL.md`
2. Follow skill template structure (see `skill-generation/SKILL.md`)
3. Add to this index (skill categories + skill index table)
4. Cross-reference in relevant agent workflows

### Automatic Addition (via `/skill-from-error`)
1. Run command when error occurs
2. Agent auto-generates skill
3. Agent auto-updates this index
4. Agent auto-integrates with workflows

---

## Maintenance Schedule

### Weekly Review
- [ ] Check `.claude/skills/skill-generation/generated/` for new skills
- [ ] Review if new skills should be promoted to main skill files
- [ ] Update skill index table if new skills added

### Monthly Review
- [ ] Search for duplicate skills (same symptoms, same tool)
- [ ] Consolidate similar patterns
- [ ] Update related skills with new cross-references
- [ ] Check for outdated information (tool versions changed)

### Quarterly Review
- [ ] Re-validate all diagnostic scripts
- [ ] Test all recovery patterns still work
- [ ] Update tool version references
- [ ] Deprecate skills for discontinued tools
- [ ] Promote frequently-used generated skills

---

## Skill Effectiveness Metrics

Track these for each skill:

| Skill | Times Used | Errors Prevented | Validation Status | Last Validated |
|-------|-----------|------------------|-------------------|----------------|
| Figma Quality Gates | TBD | TBD | ⏳ Pending first use | - |
| MCP Capability Test | TBD | TBD | ⏳ Pending first use | - |
| Component Verification | TBD | TBD | ⏳ Pending first use | - |
| Positioning Validation | TBD | TBD | ⏳ Pending first use | - |

**Goal:** High "Errors Prevented" count means skill is effective

---

## Quick Reference

**Command:** `/skill-from-error` - Generate skill from error
**Location:** All skills in `.claude/skills/`
**Index:** This file (`.claude/skills/README.md`)
**Maintenance:** Weekly check, monthly review, quarterly validation

---

## Related Documentation

- **Agent Workflows:** `.claude/agents/` - Individual agent instructions
- **Agent Team:** `.claude/team.md` - UX+UI collaboration protocol
- **Orchestrator:** `CLAUDE.md` - Main orchestrator instructions
- **Error Analysis:** `docs/design-failure-analysis.md` - Capo project lessons

---

**Maintained By:** Design Agent Orchestrator
**Contributors:** All agents (PM, Research, UX, UI, Solution Architect)
**Version:** 1.0
**Last Updated:** 2026-02-17
