# Figma MCP Capability Test Script

Run this script to validate official Figma MCP before starting work.

**Purpose:** Prevent design failures by testing MCP capabilities upfront
**Duration:** 2-3 minutes
**Target:** Official Figma MCP (remote or desktop mode)

---

## Test 1: Basic Frame Creation

**Test:** Create a test frame

```bash
create_frame(name: "MCP-Test-Frame", x: 0, y: 0, width: 400, height: 600)
```

**Expected:** Returns frame node ID
**Failure:** Error message or no response

**Result:** ✅ Pass / ❌ Fail
**Node ID:** [record here]

---

## Test 2: Shape Creation & Positioning

**Test:** Create rectangle inside frame

```bash
create_rectangle(
  parentId: [frame node ID from Test 1],
  name: "Test Rectangle",
  x: 20, y: 20, width: 100, height: 100,
  fill: {r: 0.5, g: 0.5, b: 0.5, a: 1.0}
)
```

**Expected:** Rectangle appears at (20, 20) relative to frame
**Failure:** Rectangle offset incorrectly or missing

**Result:** ✅ Pass / ❌ Fail
**Position Check:** Is rectangle at correct position inside frame? ✅/❌

**Note:** If rectangle appears far off-canvas, document this as a positioning issue.

---

## Test 3: Text Creation

**Test:** Create text node

```bash
create_text(
  parentId: [frame node ID],
  name: "Test Text",
  content: "Hello MCP Test",
  x: 20, y: 140,
  fontSize: 16,
  fontWeight: 400
)
```

**Expected:** Text "Hello MCP Test" appears at (20, 140)
**Failure:** Text missing or incorrectly positioned

**Result:** ✅ Pass / ❌ Fail

---

## Test 4: Component Instance Creation

**Pre-requisite:** Create a simple component first or use existing
**Assumption:** Button/Default component exists with key "123:456"

**Test:** Create component instance

```bash
create_component_instance(
  parentId: [frame node ID],
  componentKey: "123:456",
  name: "Test Button Instance",
  x: 20, y: 180
)
```

**Expected:** Button instance appears at (20, 180)
**Failure:** Component not found, instance missing, or error

**Result:** ✅ Pass / ❌ Fail
**Instance Node ID:** [record here]

---

## Test 5: Update Component Instance Text

**Test:** Update text inside component instance
**Assumption:** Button component has a text child

**Method A: Direct text update (if MCP supports)**
```bash
set_text_content(
  nodeId: [instance node ID],
  content: "Test Button Updated"
)
```

**Method B: Find child text node (alternative approach)**
```bash
# 1. Get instance node info
get_node_info(nodeId: [instance node ID])

# 2. Look for children with type "TEXT"
# Output will show child node IDs like "I24:14;5:43"

# 3. Update child text directly
set_text_content(
  nodeId: [child text node ID],  # e.g., "I24:14;5:43"
  content: "Test Button Updated"
)
```

**Expected:** Button text changes to "Test Button Updated"
**Failure:** Text remains unchanged, error, or can't find child node

**Method A Result:** ✅ Pass / ❌ Fail
**Method B Result:** ✅ Pass / ❌ Fail / ⚠️ Not Tried
**Workaround Needed:** Yes / No

---

## Test 6: Auto-Layout Support

**Test:** Apply auto-layout to frame

```bash
set_auto_layout(
  nodeId: [frame node ID],
  mode: "vertical",
  padding: 16,
  itemSpacing: 8
)
```

**Expected:** Children reflow vertically with 8px spacing
**Failure:** Command not found, error, or no effect

**Result:** ✅ Pass / ❌ Fail / ⚠️ Not Supported
**If Pass:** Children reflow vertically? ✅/❌

---

## Test Summary

| Test | Status | Notes |
|------|--------|-------|
| Frame creation | ✅/❌ | |
| Shape positioning | ✅/❌ | Offset bug? Yes/No |
| Text creation | ✅/❌ | |
| Component instance | ✅/❌ | |
| Instance text update | ✅/❌ | Method: A/B/None |
| Auto-layout | ✅/❌/⚠️ | |

**Overall MCP Grade:** A (all pass) / B (minor workarounds) / C (major workarounds) / F (critical failures)

---

## Grading & Recommendations

### Grade A: All Tests Pass ✅
**Capability:** 100% - MCP is fully functional
**Recommendation:** Proceed with confidence
**Actions:** None needed, start building

### Grade B: Minor Workarounds ⚠️
**Capability:** 80-90% - Some features need workarounds
**Recommendation:** Proceed with caution, document workarounds
**Typical Issues:**
- Text update requires Method B (find child nodes)
- No auto-layout (use manual positioning with 8px grid)
**Actions:**
- Document workarounds in Design Brief
- Add 10-20% time estimate for workarounds

### Grade C: Major Workarounds ⚠️
**Capability:** 50-80% - Significant limitations
**Recommendation:** Consider switching MCP or manual Figma work
**Typical Issues:**
- Positioning bugs (children offset by parent position)
- Component instances don't work
- Multiple critical features missing
**Actions:**
- Evaluate if official Figma MCP is available
- If yes: Switch to official MCP
- If no: Plan manual Figma work for critical features

### Grade F: Critical Failures ❌
**Capability:** <50% - Cannot complete task
**Recommendation:** STOP - Use different MCP or manual Figma only
**Typical Issues:**
- Cannot create frames or basic shapes
- Cannot create component instances at all
- Positioning completely broken (all elements off-canvas)
**Actions:**
- **DO NOT start building**
- Switch to official Figma MCP if available
- OR use manual Figma UI exclusively
- Update Design Brief with tool constraint

---

## Discovered Limitations

List any limitations discovered:
1. [Limitation 1]
2. [Limitation 2]

## Workarounds

List workarounds for limitations:
1. [Workaround 1]
2. [Workaround 2]

---

## Common Figma MCP Issues

Potential issues you may encounter (based on historical projects):

1. **Positioning:**
   - Children may use absolute canvas coordinates instead of parent-relative
   - Workaround: Test positioning first, adjust calculations if needed

2. **Text Updates:**
   - Direct instance text update may not work
   - Workaround: Use Method B (find child text node by ID)

3. **Auto-Layout:**
   - May not be fully supported depending on MCP version/mode
   - Workaround: Manual absolute positioning with 8px grid if needed

4. **Flow Connectors:**
   - Programmatic arrow creation may not be available
   - Workaround: Add arrows manually in Figma UI afterward

5. **Component Variants:**
   - Variant switching may not be supported
   - Workaround: Create instance of specific variant directly (e.g., "Button/Outline")

**Note:** The official Figma MCP desktop mode should have better support for these features than third-party implementations.

---

**Source:** Historical project analysis and best practices
**Last Updated:** 2026-02-18
**Target:** Official Figma MCP
