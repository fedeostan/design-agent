# Error Recovery Patterns for Figma MCP

When things go wrong during Figma design work, follow these recovery patterns.

**Purpose:** Recover from common Figma MCP issues and limitations
**Source:** Lessons from past projects + official Figma MCP capabilities

---

## Pattern 1: MCP Capability Limitations

**Symptoms:**
- Limited functionality
- Unexpected errors during design operations
- Features work differently than expected
- Operations fail silently

**Diagnosis:**
Verify your Figma MCP configuration:
```bash
# Check which MCP is installed
claude mcp list | grep figma

# Should show official Figma MCP:
# figma - https://mcp.figma.com/mcp (remote)
# OR
# figma - http://127.0.0.1:3845/mcp (desktop)
```

**Recovery:**

**Option 1: Verify MCP Setup**
1. Confirm official Figma MCP is installed
2. Test connection to Figma file
3. Verify authentication is working
4. Check MCP server logs for errors

**Option 2: Test Capabilities**
1. Document all limitations discovered in Gate 1
2. Use quality gates to test each capability
3. Apply workarounds from other patterns
4. Adjust build approach based on available features

**Option 3: Manual Figma Work**
- Build component library programmatically
- Build screens manually in Figma UI
- Use MCP only for reading/inspecting designs

---

## Pattern 2: Component Instance Text Won't Update

**Symptoms:**
- Created component instance successfully
- Button still says "Button" after trying to update text
- `set_text_content(instanceId, "new text")` fails or does nothing
- Input placeholder stays as default

**Root Cause:** Component instances are containers; text is in child nodes.

**Recovery:**

**Method A: Find Child Text Node (Capo Workaround)**
```bash
# 1. Get instance node info
get_node_info(nodeId: [instance ID])

# 2. Look for children with type "TEXT"
# Output will show child node IDs like "I24:14;5:43"
# Example output:
# {
#   "id": "24:14",
#   "type": "INSTANCE",
#   "children": [
#     {"id": "I24:14;5:43", "type": "TEXT", "characters": "Button"}
#   ]
# }

# 3. Update child text directly
set_text_content(
  nodeId: "I24:14;5:43",  # Child text node ID
  content: "Updated Text"
)
```

**Time:** +2-3 minutes per component instance

**Method B: Component Property Override (If Supported)**
```bash
# Some MCPs support property overrides
update_component_properties(
  instanceId: [instance ID],
  properties: {
    "text": "Updated Text"
  }
)
```

**If both methods fail:**
1. **Manual update:** Update text in Figma UI after programmatic build
2. **Component variants:** Create separate component for each text value
3. **Raw elements:** Use raw text elements instead of component instances

**Decision Tree:**
```
Text update needed?
  ├─ Method A works? → Use child node workaround (add time estimate)
  ├─ Method B works? → Use property override
  ├─ Neither works? → Manual Figma or raw elements
  └─ No text update needed? → Proceed normally
```

---

## Pattern 3: Elements Off-Canvas (Positioning Bug)

**Symptoms:**
- Created elements inside frame
- Screenshot shows empty frame
- Elements appear far off-canvas
- Coordinates don't match expectations

**Diagnosis:** See [positioning-validation.md](./positioning-validation.md)

**Quick Check:**
- Frame at (1000, 500)
- Child should be at (1050, 550) for relative (50, 50)
- Actually at (50, 50) or (2050, 1050)? → BUG

**Recovery:**

**Option 1: Use Auto-Layout (Best if Available)**
```bash
set_auto_layout(
  nodeId: [frame ID],
  mode: "vertical",
  padding: 24,
  itemSpacing: 16
)

# Children position automatically, bypassing coordinate bugs
```

**Option 2: Adjust Coordinates Manually**

**For Bug Type 1 (relative as absolute):**
```python
child_x = parent_x + desired_x  # Absolute = Parent + Relative
child_y = parent_y + desired_y

create_element(parentId: frame, x: child_x, y: child_y, ...)
```

**For Bug Type 2 (double-adds):**
```python
child_x = desired_x - parent_x  # Compensate for double-add
child_y = desired_y - parent_y

create_element(parentId: frame, x: child_x, y: child_y, ...)
```

**Option 3: Create at Canvas Root, Then Group**
```bash
# Create at absolute position (no parent)
create_element(x: 1050, y: 550, ...)

# Group into frame manually
# (if MCP supports move_node or group operations)
```

**Time Impact:**
- Auto-layout: No extra time
- Coordinate adjustment: +5-10 minutes per screen
- Canvas root method: +10-15 minutes per screen

---

## Pattern 4: Missing Components

**Symptoms:**
- Design Brief requires Button/Primary
- `get_local_components()` doesn't show it
- `create_component_instance` fails with "component not found"
- Component exists in design system but can't be accessed

**Recovery:**

**Step 1: Check Component Naming**
```bash
get_local_components()
# Look for similar names:
# - "Button/Default" vs "Button - Default" vs "Buttons/Default"
# - Case sensitivity: "button/default" vs "Button/Default"
```

**Step 2: Check Remote Libraries**
```bash
get_remote_components()
# Component might be in linked library, not local file
```

**Step 3: Create Missing Component**

**Option A: Manual Figma UI**
- Build component in Figma UI
- Run Gate 2 verification again
- Get component key, proceed

**Option B: Programmatic Creation**
```bash
# 1. Create element
create_rectangle(name: "Primary Button", x: 0, y: 0, width: 120, height: 48, ...)

# 2. Convert to component
create_component_from_node(nodeId: [element ID], name: "Button/Primary")

# 3. Get component key
get_local_components()  # Find newly created component
```

**Option C: Adjust Design Brief**
- Use existing similar component instead
- Update Design Brief with actual component name
- Document deviation

**Decision Matrix:**
| Situation | Action |
|-----------|--------|
| Component needed, can create | Create in Figma UI, then proceed |
| Component name mismatch | Update Design Brief with correct name |
| Similar component exists | Use alternative, document change |
| Critical component, can't create | STOP, get Design System updated |

---

## Pattern 5: Auto-Layout Not Working

**Symptoms:**
- `set_auto_layout` command exists but does nothing
- Elements still use absolute positioning after setting auto-layout
- Error: "auto-layout not supported"
- Children don't reflow when added

**Diagnosis:** Auto-layout may not be fully supported or configured correctly

**Recovery:**

**Option 1: Manual Absolute Positioning with 8px Grid**
```python
# Calculate positions manually
spacing = 16
y_position = 24  # Start padding

# Element 1
create_element(x: 24, y: y_position, height: 40, ...)
y_position += 40 + spacing  # Move down by height + spacing

# Element 2
create_element(x: 24, y: y_position, height: 32, ...)
y_position += 32 + spacing

# Element 3
create_element(x: 24, y: y_position, height: 48, ...)
```

**Time:** +10% build time for manual calculations

**Option 2: Document Layout Pattern**
```markdown
# In annotation note
Layout: Vertical stack
- Padding: 24px
- Spacing: 16px
- Elements: Input, Input, Button

Implementation: Use flexbox column, gap: 16px
```

**Developers implement proper auto-layout in code**

**Option 3: Post-Processing in Figma UI**
- Build screens programmatically with absolute positions
- Apply auto-layout manually in Figma afterward
- Takes 5-10 minutes for typical screen set

**Option 4: Use Constraints (If Supported)**
```bash
set_constraints(nodeId, {
  horizontal: "left-right",  # Stretch width
  vertical: "top"            # Pin to top
})
```

Provides some responsive behavior without full auto-layout.

---

## Pattern 6: No Flow Arrows/Connectors

**Symptoms:**
- No `create_connector` or `create_arrow` command
- No `create_line` command
- Screens built but not connected visually
- Flow documentation missing

**Diagnosis:** Connector/arrow creation may not be available via MCP

**Recovery:**

**Option 1: Use Figma UI for Arrows (Recommended)**
- Build all screens programmatically first
- Connect with arrows manually in Figma UI
- Takes 5-10 minutes for typical flow (9 screens)

**Option 2: Document Flow in Annotations**
```markdown
# Add to each screen's annotation note:

Next Screen: [Screen Name]
Trigger: [User action]

Example:
- Screen: Auth/Login
- Next: Auth/Login-Loading
- Trigger: Tap "Sign In" button
```

**Developers and UX can understand flow from notes.**

**Option 3: Create Arrow-Like Shapes (Not Recommended)**
```bash
# Complex, ugly, and time-consuming
# Create thin rectangle as line
create_rectangle(width: 200, height: 2, ...)

# Create triangle as arrowhead
create_polygon(points: [[0,0], [10,5], [0,10]], ...)

# Position to connect screens
```

**Time:** 2-3 minutes per arrow, not worth it

**Decision:** Always use Option 1 (manual arrows in UI)

---

## Pattern 7: Variants/Properties Not Working

**Symptoms:**
- Can't switch component variant (Default → Outline)
- Can't set component properties (size: lg)
- Component always renders in default state
- Property override UI not available in MCP

**Diagnosis:** Component variant switching or property overrides may not be supported

**Recovery:**

**Option 1: Create Instance of Specific Variant**
```bash
# Don't use generic component:
# create_component_instance(componentKey: "Button")

# Use specific variant directly:
create_component_instance(componentKey: "Button/Outline")

# For size variants:
create_component_instance(componentKey: "Button/Default/lg")
```

**Requires:** Component keys for each variant documented in Gate 2

**Option 2: Manual Resize for Size Variants**
```bash
# Create Button/Default instance (40px height)
create_component_instance(componentKey: "Button/Default", ...)

# Resize to "lg" size (48px height)
resize_node(nodeId: [instance ID], height: 48, width: 120)
```

**Caution:** May break component constraints

**Option 3: Create Separate Components for Each State**
Instead of:
- Button component with size property (sm/default/lg)

Create:
- Button/sm
- Button/default
- Button/lg

**Time:** More components to manage, but cleaner instance creation

**Decision Matrix:**
| Need | Solution |
|------|----------|
| Different style (Outline, Ghost) | Use specific variant component key |
| Different size (sm, lg) | Resize instance or use size-specific component |
| Different state (Loading, Disabled) | Create separate component or manual styling |

---

## Pattern 8: Can't Read Existing Designs

**Symptoms:**
- Need to match existing screens
- `get_screenshot` or `get_metadata` fails
- "Unauthorized" or "Not found" errors
- Authentication issues

**Diagnosis:** MCP authentication or file access permissions issue

**Solution:** Verify Official Figma MCP Setup

```bash
# Ensure official Figma MCP is configured
claude mcp list | grep figma

# Test file access with a known file URL
# Reading designs:
get_screenshot(nodeId: "123:456", fileKey: "abc...")
get_metadata(nodeId: "123:456", fileKey: "abc...")
get_design_context(nodeId: "123:456", fileKey: "abc...")

# Writing designs (desktop mode):
generate_figma_design(...)  # Code to Canvas — only write tool available
```

**Authentication Check:**
1. Verify Figma MCP authentication (OAuth for remote, desktop app running for local)
2. Confirm file access permissions in Figma
3. Test with a simple file read operation
4. Check MCP server logs for auth errors

---

## Decision Tree: When to Stop vs Continue

```
Issue discovered
  ├─ Critical: Can't create component instances?
  │   └─ **STOP** → Use different MCP or manual Figma
  │
  ├─ Major: Positioning bug or no auto-layout?
  │   ├─ Workaround available? → Continue with workaround
  │   └─ No workaround? → **STOP** → Manual Figma
  │
  ├─ Moderate: Text update requires child node lookup?
  │   └─ Continue (add 2-3 min per component)
  │
  └─ Minor: No connectors, no property overrides?
      └─ Continue (manual Figma for connectors, use variants directly)
```

---

## Escalation Path

If stuck:

1. **Check existing docs:**
   - [docs/design-failure-analysis.md](../../../docs/design-failure-analysis.md)
   - [.claude/skills/figma-quality-gates/prompts/](../)

2. **Test with minimal example:**
   - Create single frame + single element
   - Isolate the issue
   - Document exact command and error

3. **Use error-driven skill generation:**
   - Run `/skill-from-error` command
   - Capture error details
   - Generate skill from error
   - See: [.claude/skills/skill-generation/SKILL.md](../../skill-generation/SKILL.md)

4. **Escalate to user:**
   - Explain issue clearly
   - Propose options (workaround vs switch tool vs manual)
   - Get decision before continuing

---

## Pattern 9: Code-to-Canvas Messy Structure

**Symptoms:**
- 10+ nesting levels in captured Figma frame
- All layers named "Container", "View", or CSS hash names (`.css-1a2b3c`)
- Wrong frame dimensions (not matching intended viewport)
- Hidden/phantom artifacts from browser extensions or framework wrappers
- Layer tree is unmanageable — can't find or edit specific elements

**Root Cause:** Capturing directly from a framework app (React, React Native Web, Next.js, etc.). The framework's DOM wrappers, provider trees, and styling infrastructure all get captured as Figma frames, creating deep nesting with meaningless names.

**Diagnosis:**
```bash
get_metadata(fileKey: "...", nodeId: "[captured frame]")
# Check: How many nesting levels? Are names meaningful?
# Bad: 10+ levels, names like "Container", "View", "css-1a2b3c"
# Good: 3 levels, names like "card", "card-title", "field-input"
```

**Recovery: Clean HTML Re-capture**

1. Screenshot the messy capture for visual reference
2. Get design context (colors, fonts, spacing) from the existing frame
3. Create a minimal flat HTML file (max 3 levels of nesting)
4. Use semantic class names (they become Figma layer names)
5. Include the Figma capture script
6. Serve locally and re-capture

**Full workflow:** See [figma/prompts/code-to-canvas-workflow.md](../../figma/prompts/code-to-canvas-workflow.md)

**Prevention:**
- **Never** capture directly from framework apps — always create flat HTML first
- **Always** set a fixed viewport meta tag
- **Always** use semantic class names on every element
- **Always** use incognito mode to avoid browser extension artifacts

**Time Impact:**
- Clean HTML creation: 15-30 minutes
- Re-capture: 5 minutes
- vs. trying to manually fix messy capture: 1-2 hours (and still bad)

---

**Source:** Historical project analysis + official Figma MCP capabilities
**Last Updated:** 2026-02-18
**Patterns Count:** 9 (common failure modes and recovery strategies)
