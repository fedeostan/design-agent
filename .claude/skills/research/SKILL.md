---
name: research
description: Heuristic evaluation, competitive analysis, WCAG audit, and cognitive walkthrough templates.
user-invocable: false
---

# Research Skill

Templates and frameworks for design research activities.

## Heuristic Evaluation Template

### Setup
1. Define the scope (which flow/screens to evaluate)
2. Take screenshots of every screen and state
3. Evaluate each screen against all 10 heuristics
4. Rate severity (0-4)
5. Compile findings

### Nielsen's 10 Heuristics Checklist

#### H1: Visibility of System Status
- [ ] Users know where they are in the flow
- [ ] Loading states provide feedback
- [ ] Progress indicators show completion
- [ ] Actions have visible results
- [ ] System responds within acceptable time

#### H2: Match Between System and Real World
- [ ] Language matches user vocabulary (not dev jargon)
- [ ] Icons are universally understood
- [ ] Information follows natural/logical order
- [ ] Conventions match real-world expectations

#### H3: User Control and Freedom
- [ ] Clear "undo" or "back" for mistakes
- [ ] Easy to exit unwanted states
- [ ] Cancel option available for processes
- [ ] Users aren't trapped in flows

#### H4: Consistency and Standards
- [ ] Same action = same result everywhere
- [ ] UI patterns match platform conventions
- [ ] Terminology is consistent across screens
- [ ] Layout patterns are consistent

#### H5: Error Prevention
- [ ] Destructive actions require confirmation
- [ ] Input validation happens before submission
- [ ] Defaults prevent common errors
- [ ] Constraints guide correct input

#### H6: Recognition Rather Than Recall
- [ ] Options are visible, not hidden
- [ ] Instructions available when needed
- [ ] Context carried between screens
- [ ] Recently used items are accessible

#### H7: Flexibility and Efficiency of Use
- [ ] Shortcuts for expert users
- [ ] Frequent actions are quick to perform
- [ ] Personalization or customization available
- [ ] Multiple ways to complete common tasks

#### H8: Aesthetic and Minimalist Design
- [ ] Only relevant information shown
- [ ] Visual hierarchy guides attention
- [ ] No decorative elements that distract
- [ ] White space used effectively

#### H9: Help Users Recognize, Diagnose, and Recover from Errors
- [ ] Error messages in plain language
- [ ] Error messages describe the problem specifically
- [ ] Error messages suggest a solution
- [ ] Users can easily recover from errors

#### H10: Help and Documentation
- [ ] Key features are self-explanatory
- [ ] Help is available when needed
- [ ] Documentation is searchable
- [ ] Steps are concrete and actionable

### Severity Rating

| Severity | Label | Definition |
|----------|-------|------------|
| 0 | Not a problem | Evaluator disagrees |
| 1 | Cosmetic | Fix if time allows |
| 2 | Minor | Low priority fix |
| 3 | Major | Must fix before release |
| 4 | Catastrophic | Fix immediately |

---

## Competitive Analysis Framework

### Step 1: Identify Competitors
- 3-5 direct competitors (same market, same solution)
- 2-3 indirect competitors (different market, similar UX problem)
- 1-2 best-in-class examples (any industry, gold standard UX)

### Step 2: Define Analysis Dimensions
For each competitor, evaluate:
- **Task completion flow** — How many steps? How clear?
- **Information architecture** — How is content organized?
- **Error handling** — How are errors shown and recovered?
- **Onboarding** — How do new users get started?
- **Accessibility** — Basic accessibility check
- **Differentiators** — What's unique about their approach?

### Step 3: Comparison Matrix

| Dimension | Us | Competitor A | Competitor B | Competitor C |
|-----------|-----|-------------|-------------|-------------|
| Steps to complete task | | | | |
| Error handling quality | | | | |
| Mobile experience | | | | |
| Accessibility | | | | |
| Unique features | | | | |

### Step 4: Opportunity Map
- **Table stakes** (everyone does it, we must too)
- **Competitive advantages** (few do it, high value)
- **Differentiators** (no one does it, potential high value)
- **Over-served** (everyone over-invests here, diminishing returns)

---

## WCAG 2.1 AA Quick Audit Checklist

### Perceivable
- [ ] **1.1.1** Non-text content has alt text
- [ ] **1.3.1** Info and relationships conveyed through structure
- [ ] **1.3.3** Sensory characteristics not sole way to convey info
- [ ] **1.4.1** Color not sole means of conveying info
- [ ] **1.4.3** Contrast ratio 4.5:1 (normal text), 3:1 (large text)
- [ ] **1.4.4** Text can resize up to 200% without loss
- [ ] **1.4.11** Non-text contrast 3:1 for UI components

### Operable
- [ ] **2.1.1** All functionality keyboard accessible
- [ ] **2.1.2** No keyboard trap
- [ ] **2.4.3** Focus order is logical
- [ ] **2.4.6** Headings and labels describe purpose
- [ ] **2.4.7** Focus visible
- [ ] **2.5.5** Touch targets 44x44px minimum

### Understandable
- [ ] **3.1.1** Language of page identified
- [ ] **3.2.1** No unexpected context change on focus
- [ ] **3.2.2** No unexpected context change on input
- [ ] **3.3.1** Errors identified and described in text
- [ ] **3.3.2** Labels and instructions provided for input
- [ ] **3.3.3** Error suggestions provided when possible

### Robust
- [ ] **4.1.2** Name, role, value available for all UI components

---

## Cognitive Walkthrough Template

### Setup
- **Persona:** [Name, experience level, context]
- **Task:** [What the user is trying to accomplish]
- **Starting point:** [Where the user begins]

### Per-Step Analysis

| Step | Action | Q1: Will they try? | Q2: Will they see it? | Q3: Will they understand? | Q4: Will they know they progressed? | Issue? |
|------|--------|--------------------|-----------------------|--------------------------|-------------------------------------|--------|
| 1 | [Action] | [Yes/No + why] | [Yes/No + why] | [Yes/No + why] | [Yes/No + why] | [Issue] |
| 2 | [Action] | | | | | |

### Questions
- **Q1:** Will users try to achieve this step's effect?
- **Q2:** Will users see the control for this step?
- **Q3:** Will users understand the control produces this effect?
- **Q4:** Will users understand the feedback after this step?
