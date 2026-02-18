# Positioning Validation Script

Detect absolute vs relative coordinate positioning issues in Figma MCP.

**Purpose:** Catch positioning bugs before building all screens
**Duration:** 2-3 minutes
**Owner:** UI Specialist
**When:** After building first screen (Gate 3)

---

## Common Positioning Issues

**Symptom:** Child elements positioned off-canvas, far from parent frame

**Historical Example:**
- Parent frame at `x: 1100, y: 0`
- Child logo at `x: 2355, y: 100` (should be ~1255)
- Offset: `2355 - 1100 = 1255` (exactly the parent's x position!)

**Root cause:** Some MCP implementations may use absolute canvas coordinates for children instead of parent-relative coordinates

**Impact:** Elements render far off-screen, completely unusable

---

## Validation Test

### 1. Create Test Frame (Not at Origin)

```bash
create_frame(
  name: "Position-Test-Frame",
  x: 1000,  # Intentionally not at 0
  y: 500,   # Intentionally not at 0
  width: 400,
  height: 600
)
```

**Frame Node ID:** [record here]
**Frame Position:** x: 1000, y: 500 ✅

**Why not at origin?** If frame is at (0, 0), bug won't be detectable.

---

### 2. Create Child Element with Relative Coordinates

```bash
create_rectangle(
  parentId: [frame node ID],
  name: "Test Child",
  x: 50,   # Should be 50px from frame left edge
  y: 50,   # Should be 50px from frame top edge
  width: 100,
  height: 100,
  fill: {r: 1.0, g: 0.0, b: 0.0, a: 1.0}  # Red for visibility
)
```

**Child Node ID:** [record here]

---

### 3. Verify Child Position

```bash
get_node_info(nodeId: [child node ID])
# Check the returned x, y coordinates
```

**Expected:** x: 1050 (parent 1000 + relative 50), y: 550 (parent 500 + relative 50)
**Actual:** x: [record], y: [record]

**Calculation:**
- `actual x - parent x = [result]` (should equal 50)
- `actual y - parent y = [result]` (should equal 50)

---

## Bug Diagnosis

| Actual Child Position | Diagnosis | Issue Present? |
|----------------------|-----------|----------------|
| x: 1050, y: 550 | ✅ **Correct** - MCP handles parent-relative positioning | No |
| x: 50, y: 50 | ❌ **Type 1** - MCP uses relative as absolute | Yes |
| x: 2050, y: 1050 | ❌ **Type 2** - MCP double-adds parent position | Yes (variant) |
| Off-canvas far away | ❌ **Type 3** - Coordinate system completely broken | Yes (severe) |

---

## Workarounds

### If Bug Type 1 Detected (uses relative as absolute)

**Problem:** Child at (50, 50) instead of (1050, 550)
**Workaround:** Pass absolute coordinates

```python
# When creating child at desired position (50, 50) inside parent at (1000, 500):

child_x = parent_x + desired_relative_x  # 1000 + 50 = 1050
child_y = parent_y + desired_relative_y  # 500 + 50 = 550

create_rectangle(
  parentId: parent_id,
  x: child_x,  # Pass 1050 (absolute)
  y: child_y,  # Pass 550 (absolute)
  ...
)
```

**Impact:** Must calculate absolute coordinates for every child element.

---

### If Bug Type 2 Detected (double-adds parent position)

**Problem:** Child at (2050, 1050) instead of (1050, 550)
**Workaround:** Subtract parent offset

```python
# When creating child at desired position (50, 50) inside parent at (1000, 500):

child_x = desired_relative_x - parent_x  # 50 - 1000 = -950
child_y = desired_relative_y - parent_y  # 50 - 500 = -450

create_rectangle(
  parentId: parent_id,
  x: child_x,  # Pass -950
  y: child_y,  # Pass -450
  ...
)
```

**Impact:** Must use negative coordinates (unintuitive, error-prone).

---

### If Bug Type 3 Detected (completely broken)

**Problem:** Children appear in random off-canvas locations
**Workaround:** Create at canvas root, then group

```bash
# Alternative approach: Don't use parentId
# Create child at canvas root with absolute coords
create_rectangle(
  x: 1050,  # Absolute canvas position
  y: 550,
  width: 100,
  height: 100,
  ...
)

# Then manually move into parent frame (if MCP supports)
move_node(nodeId: [child id], newParentId: [frame id])
```

**Impact:** Two-step process for every element, may break auto-layout.

---

## Auto-Layout Check (Alternative Solution)

If auto-layout is supported, it may bypass positioning bugs:

```bash
# Apply auto-layout to frame
set_auto_layout(
  nodeId: [frame node ID],
  mode: "vertical",
  padding: 16,
  itemSpacing: 8
)

# Create child without explicit x, y
create_rectangle(
  parentId: [frame node ID],
  name: "Auto-Layout Child",
  width: 100,
  height: 100
  # x, y should be ignored with auto-layout
)

# Verify child positions automatically
```

**Auto-Layout Works:** ✅ Yes / ❌ No

**If Yes:** Use auto-layout for all frames (solves positioning bugs automatically)
**If No:** Use workaround for absolute positioning

---

## Test Summary

**Coordinate System:** ✅ Correct / ❌ Bug Type 1 / ❌ Bug Type 2 / ❌ Bug Type 3
**Auto-Layout Available:** ✅ Yes / ❌ No
**Recommended Approach:**
- ✅ Correct → Use relative coordinates as normal
- ❌ Bug + Auto-layout works → Use auto-layout for all frames
- ❌ Bug + No auto-layout → Use workaround for absolute coords
- ❌ Type 3 → **STOP**, switch to different MCP or manual Figma

---

## Gate 3 Application

**After building first screen:**

1. **Check screenshot:** Are all elements visible in correct positions?
2. **If elements off-canvas:** Run this positioning validation test
3. **Diagnose bug type:** Which pattern matches?
4. **Apply workaround:** Use appropriate coordinate calculation
5. **Rebuild first screen:** Using workaround
6. **Verify with screenshot:** Elements now in correct positions?

**Pass Criterion:** Either coordinate system works correctly OR auto-layout solves it

**Fail Action:** If no workaround available, STOP and switch MCP

---

## Historical Example: Auth/Login Screen

**What happened in a past project:**
- Frame created at `x: 0, y: 0` ✅
- Logo created at `x: 155, y: 80` (relative)
- **Expected position:** `x: 155, y: 80` (since parent at origin)
- **Actual position:** `x: 155, y: 80` ✅ (correct because parent at 0, 0)

**But for second screen:**
- Frame created at `x: 1100, y: 0`
- Logo created at `x: 155, y: 80` (relative)
- **Expected position:** `x: 1255, y: 80` (parent 1100 + relative 155)
- **Actual position:** `x: 2355, y: 100` ❌ (Type 2: double-added parent x)

**Lesson:** Bug not caught because first screen was at origin (0, 0). Should have tested with non-origin frame.

---

**Source:** Historical project analysis
**Last Updated:** 2026-02-18
**Target:** Official Figma MCP positioning validation
