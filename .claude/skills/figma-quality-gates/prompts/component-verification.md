# Component Verification Checklist

Verify all components from Design Brief exist and work before building screens.

**Purpose:** Prevent missing/broken components causing build failures
**Duration:** 5-10 minutes
**Owner:** UI Specialist
**When:** Before building first screen (Gate 2)

---

## Setup

**Design Brief Components List:**
[Copy component list from Design Brief section 5 or Component Library]

Example components typically needed:
- Button/Default (default, lg sizes)
- Button/Outline
- Button/Ghost
- Button/Destructive
- Input/Default
- Card/Default
- ProgressBar
- Header
- Note (Business, Design, Dev, Question variants)
- IconPlaceholder (40×40, 80×80)

---

## Verification Process

For EACH component needed:

### 1. Check Component Exists

```bash
# Get all local components
get_local_components()

# Search output for component name
# Example: Look for "Button/Default", "Input/Default", etc.
```

**Component:** [Component Name]
**Status:** ✅ Exists / ❌ Missing
**Component Key:** [e.g., "123:456"]

---

### 2. Test Instance Creation

```bash
# Create test instance in MCP-Test-Frame
create_component_instance(
  parentId: [test frame ID from mcp-capability-test],
  componentKey: [component key from step 1],
  name: "Test [Component Name] Instance",
  x: 0, y: 0
)
```

**Result:** ✅ Success / ❌ Failed
**Instance Node ID:** [record if success]
**Error:** [record if failed]

---

### 3. Test Text Update (for components with text)

**For components with text (Button, Input, etc.):**

```bash
# Try direct update first
set_text_content(
  nodeId: [instance node ID],
  content: "UPDATED TEXT"
)

# If that fails, find child text node:
get_node_info(nodeId: [instance node ID])
# Find child text node ID (e.g., "I24:14;5:43")

set_text_content(
  nodeId: [child text node ID],
  content: "UPDATED TEXT"
)
```

**Result:** ✅ Success / ⚠️ Workaround Needed / ❌ Failed
**Method:** Direct / Child Node / None

---

### 4. Test Resizing (for size variants)

**For components that should support different sizes:**

```bash
# Test resizing instance
resize_node(
  nodeId: [instance node ID],
  width: [new width],
  height: [new height]
)
```

**Result:** ✅ Success / ❌ Failed

---

## Component Verification Table

| Component | Exists | Instance Works | Text Update | Resize | Overall |
|-----------|--------|----------------|-------------|--------|---------|
| Button/Default | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Button/Outline | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Button/Ghost | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Input/Default | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Card/Default | ✅/❌ | ✅/❌ | N/A | ✅/❌ | ✅/⚠️/❌ |
| ProgressBar | ✅/❌ | ✅/❌ | N/A | ✅/❌ | ✅/⚠️/❌ |
| Header | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Note/Business | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Note/Design | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Note/Dev | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| Note/Question | ✅/❌ | ✅/❌ | ✅/⚠️/❌ | ✅/❌ | ✅/⚠️/❌ |
| IconPlaceholder/40 | ✅/❌ | ✅/❌ | N/A | ✅/❌ | ✅/⚠️/❌ |
| IconPlaceholder/80 | ✅/❌ | ✅/❌ | N/A | ✅/❌ | ✅/⚠️/❌ |

**Legend:**
- ✅ Works correctly
- ⚠️ Workaround available (e.g., child node text update)
- ❌ Broken (cannot use)

---

## Missing Components

Components that need to be created:
1. [Component name] - [Reason: not in design system]
2. ...

**Action Before Continuing:**
- Create these components in Figma UI first
- OR adjust Design Brief to use existing components
- OR plan manual creation during screen build

---

## Broken Components

Components that exist but don't work:
1. [Component name] - [Issue: text update fails]
2. ...

**Action Before Continuing:**
- Fix component (recreate, update properties)
- OR document workaround
- OR use alternative component

---

## Green List (Verified Working)

**Only use these components when building screens:**
- [Component 1] - Key: [key], Notes: [any workarounds]
- [Component 2] - Key: [key], Notes: [any workarounds]
- ...

**Pass Criterion:** At least 80% of needed components on green list

---

## Component Keys Reference

Document keys for easy reference during build:

```
Button/Default/default: [key]
Button/Default/lg: [key]
Button/Outline/default: [key]
Input/Default: [key]
Card/Default: [key]
...
```

**Use these keys when creating instances:**
```bash
create_component_instance(componentKey: "[key from above]", ...)
```

---

## Workarounds Discovered

List specific workarounds needed:

**Example:**
1. **Button text update:**
   - Issue: Direct `set_text_content(instanceId, text)` doesn't work
   - Workaround: Use `get_node_info`, find child text node, update child node

2. **Input placeholder:**
   - Issue: Cannot set placeholder property
   - Workaround: Accept default placeholder, or duplicate component with different placeholder

---

## Gate 2 Pass/Fail Decision

**PASS if:**
- ✅ All critical components exist and work (buttons, inputs, basic layout)
- ✅ Text update workaround identified for components that need it
- ✅ At least 80% of components on green list
- ✅ Missing components can be created or substituted

**FAIL if:**
- ❌ Critical components missing and can't be created
- ❌ Component instances fail to create
- ❌ No workaround for text updates and text customization is required
- ❌ <50% of components work

**If FAIL:**
- Stop building screens
- Create/fix components first
- Re-run this verification
- Only proceed when Gate 2 passes

---

**Source:** Historical project analysis (component availability and text update validation)
**Last Updated:** 2026-02-17
**Integrates With:** [mcp-capability-test.md](./mcp-capability-test.md) (Test 4 & 5)
