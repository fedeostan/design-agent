# Design System Constraints

You are working with Fede's design system. Follow these rules strictly.

## General Principles

1. **Always use existing components** - Never create raw shapes when a component exists
2. **Follow auto-layout patterns** - All frames should use auto-layout
3. **Maintain consistency** - Match existing screens in the file
4. **Ask before creating** - If unsure about a pattern, ask first

## Component Usage

### Before Creating Anything
1. Run `get_local_components` to see available components
2. Check if a component already exists for what you need
3. Use `create_component_instance` instead of raw shapes

### Finding Components
```
// Get all local components
get_local_components

// Look for naming patterns like:
// - Button/Primary, Button/Secondary
// - Input/Text, Input/Password
// - Card/Default, Card/Elevated
// - Note/Business, Note/Design, Note/Dev
```

## Auto-Layout Rules

1. **All containers use auto-layout** - No absolute positioning inside frames
2. **Consistent spacing** - Use 8px grid (8, 16, 24, 32, 40, 48)
3. **Padding patterns**:
   - Cards: 16px or 24px all sides
   - Sections: 24px or 32px
   - Buttons: 12px horizontal, 8px vertical

## Naming Conventions

- Frames: `ScreenName/State` (e.g., "Login/Default", "Login/Error")
- Components: `Category/Variant` (e.g., "Button/Primary")
- Layers: Descriptive, no "Frame 123" names

## Colors

Use design tokens, not raw hex values. Reference:
- `get_styles` to see available color styles
- Apply via component properties when possible

## Typography

Use text styles from the design system:
- Headings: H1, H2, H3, H4
- Body: Body/Regular, Body/Bold
- Caption: Caption/Regular

---

**Remember:** When in doubt, read the existing design first with `read_my_design` and match its patterns.
