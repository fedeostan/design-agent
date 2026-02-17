---
name: requirements
description: Design brief, user story, and acceptance criteria templates.
user-invocable: false
---

# Requirements Skill

Templates for gathering and structuring product requirements.

## Design Brief Template

```markdown
# Design Brief: [Feature Name]

## Summary
[1-2 sentences: what we're building and why]

## Problem Statement
[What user problem are we solving? Current pain point?]

## User Stories

### Primary
- As a [user type], I want to [action] so that [benefit]
  - **AC:** [Acceptance criterion 1]
  - **AC:** [Acceptance criterion 2]

### Secondary
- As a [user type], I want to [action] so that [benefit]
  - **AC:** [Acceptance criterion]

## Business Rules
1. [Rule]: [Description + rationale]

## Constraints
- **Platform:** [web/mobile/both]
- **Accessibility:** WCAG 2.1 AA
- **Technical:** [API/data constraints]
- **Compliance:** [Regulatory requirements]

## Scope
**In:** [What's included]
**Out:** [What's explicitly excluded]

## Open Questions
1. [Question] — Owner: [who]

## Priority
Impact: [H/M/L] | Urgency: [H/M/L] | Effort: [S/M/L/XL]

## Source
[Link to ticket/doc]
```

---

## User Story Writing Guide

### INVEST Criteria
Good user stories are:
- **I**ndependent — Can be developed on its own
- **N**egotiable — Details can be discussed
- **V**aluable — Delivers value to the user
- **E**stimable — Team can estimate effort
- **S**mall — Fits in one sprint
- **T**estable — Has clear acceptance criteria

### Format
```
As a [user persona],
I want to [action/capability],
so that [benefit/value].
```

### Acceptance Criteria Patterns

**Given-When-Then (for behavior):**
```
Given [precondition],
When [action],
Then [expected result].
```

**Checklist (for simpler stories):**
```
- [ ] [Observable outcome 1]
- [ ] [Observable outcome 2]
```

### Common Acceptance Criteria to Include
- Happy path completion
- Error handling (invalid input, network failure)
- Edge cases (empty state, max length, special characters)
- Loading/progress feedback
- Accessibility requirements
- Analytics events

---

## Acceptance Criteria Patterns by Feature Type

### Form Features
- [ ] All fields validate on blur and on submit
- [ ] Error messages are specific and actionable
- [ ] Form preserves input on validation failure
- [ ] Submit button shows loading state
- [ ] Success state confirms completion
- [ ] Keyboard navigation works (Tab, Enter, Escape)

### List/Feed Features
- [ ] Empty state shown when no items
- [ ] Loading state with skeleton/spinner
- [ ] Pull-to-refresh (mobile) / Refresh button (web)
- [ ] Pagination or infinite scroll
- [ ] Item count displayed
- [ ] Error state with retry

### Navigation Features
- [ ] Current location indicated
- [ ] Back navigation works correctly
- [ ] Deep linking supported
- [ ] Breadcrumbs (if applicable)
- [ ] Transition animations appropriate

### Authentication Features
- [ ] Login/signup fields validate
- [ ] Password requirements displayed
- [ ] Show/hide password toggle
- [ ] Forgot password flow
- [ ] Session timeout handling
- [ ] Biometric/SSO options (if applicable)

---

## Stakeholder Priority Matrix

### MoSCoW Method
- **Must have:** Critical for launch. Without these, the feature doesn't work.
- **Should have:** Important but not critical. Workarounds exist.
- **Could have:** Nice to have. Include if time allows.
- **Won't have (this time):** Explicitly deferred to a future iteration.

### Priority Scoring
| Factor | Weight | Score (1-5) | Weighted |
|--------|--------|-------------|----------|
| User impact | 3x | | |
| Business value | 2x | | |
| Technical risk | 1x | | |
| Effort | 1x | | |
| **Total** | | | |

---

## Requirements Gathering Questions

### For Any Feature
1. Who is the primary user? Secondary users?
2. What's the user's goal? What triggers them to use this?
3. What does success look like for the user?
4. What does success look like for the business?
5. What are the constraints? (technical, legal, brand)
6. What's out of scope?
7. What existing patterns should we follow?
8. When does this need to ship?

### For Redesigns
1. What works well in the current version?
2. What are the top user complaints?
3. What metrics are we trying to improve?
4. What can we NOT change? (technical debt, API constraints)
5. What's the migration plan for existing users?
