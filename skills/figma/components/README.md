# Components to Create in Your Design System

Create these components in your Figma design system library. Once created, the AI can instantiate them when building flows.

---

## Note Components

### Note/Business
- **Background:** Light blue or your brand subtle color
- **Padding:** 16px all sides
- **Auto-layout:** Vertical, 8px gap
- **Border radius:** 8px
- **Contents:**
  - Title: "📊 Business Note" (bold, 14px)
  - Body: Text area (regular, 14px)

### Note/Design
- **Background:** Light purple or accent color
- **Same structure as Business Note**
- **Title:** "🎨 Design Note"

### Note/Dev
- **Background:** Light gray or code-like color
- **Same structure as Business Note**
- **Title:** "💻 Dev Note"
- **Optional:** Monospace font for body

### Note/Question
- **Background:** Light yellow/orange (attention color)
- **Same structure as Business Note**
- **Title:** "❓ Question"

---

## Flow Components

### Flow/Arrow
- **Type:** Line with arrow end
- **Start:** Rounded cap
- **End:** Arrow head
- **Stroke:** 2px
- **Color:** Gray (default) or Blue (primary action)
- **Text property:** Label text (optional)

### Flow/Screen Frame
- **Standard frame for flow screens**
- **Device frame optional**
- **Consistent sizing:** e.g., 375x812 (iPhone) or custom

---

## Spec Components (Optional but Recommended)

### Spec/Spacing
- Visual indicator for spacing values
- Shows 8, 16, 24, 32px etc.

### Spec/Annotation
- Callout style for pointing to specific elements
- Line + text bubble

---

## Component Properties to Expose

For each Note component, expose these as properties:
1. **Title text** - So AI can set custom titles
2. **Body text** - Main content
3. **Type/Color variant** - If you want color variations

## Naming Convention

Use this exact naming so the AI can find them:
```
Note/Business
Note/Design
Note/Dev
Note/Question
Flow/Arrow
Flow/ScreenFrame
```

---

## After Creating

1. Publish your design system library
2. Link it to your working files
3. Tell Jarvis: "My design system components are ready"
4. Jarvis will run `get_local_components` to verify

---

**Tip:** Start with just Note/Business and test. Add others iteratively.
