# Flow & Arrow Style Guide

## Arrow Style (FigJam-like)

### Visual Specification
- **Start:** Rounded end (no arrow)
- **End:** Arrow head
- **Line:** Curved/organic, not rigid
- **Stroke:** 2px, color from design system (typically gray or blue)
- **Text:** Can include label inside/alongside arrow

### Creating Flow Arrows

```
// Use the connector tools
set_default_connector  // Set up default arrow style
create_connections     // Connect nodes with arrows
```

### Arrow Naming
- Name arrows by their action: "Tap Login", "Submit Form", "Navigate Back"
- Or by condition: "If Valid", "On Error", "Success"

## Flow Layout

### Screen Arrangement
1. **Horizontal flows:** Left to right progression
2. **Vertical alternatives:** Stack variants vertically
3. **Spacing:** 100-200px between screens
4. **Alignment:** Center-align screens in a flow

### Example Layout
```
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Login  │───▶│  Home   │───▶│ Profile │
│ Screen  │    │ Screen  │    │ Screen  │
└─────────┘    └─────────┘    └─────────┘
     │
     ▼ (on error)
┌─────────┐
│  Error  │
│  State  │
└─────────┘
```

### Snapping
- Enable smart guides
- Snap to 8px grid
- Align with existing frames

## State Variations

When creating a flow, include all states:
1. **Default** - Initial/empty state
2. **Loading** - Processing state
3. **Success** - Completed state
4. **Error** - Error state
5. **Empty** - No data state

Name pattern: `ScreenName/StateName`

## Connecting Screens

```javascript
// After creating screens, connect them:
create_connections({
  connections: [
    { from: "screen1_id", to: "screen2_id", label: "Tap Continue" },
    { from: "screen2_id", to: "screen3_id", label: "Submit" }
  ]
})
```

---

**Always ask:** "What states should this screen have?" before creating a single screen.
