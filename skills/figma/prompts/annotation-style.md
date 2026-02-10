# Annotation & Notes Style Guide

## Note Types

Fede uses different note types for different purposes. Each is a component with auto-layout.

### 1. Business Note
**Use when:** Explaining business logic, requirements, stakeholder decisions
**Component:** `Note/Business`
**Structure:**
```
┌────────────────────────────┐
│ 📊 Business Note           │  ← Title (bold)
├────────────────────────────┤
│ This screen shows the      │
│ onboarding flow required   │  ← Body text
│ by compliance team...      │
└────────────────────────────┘
```

### 2. Design Note
**Use when:** Explaining design decisions, alternatives considered, rationale
**Component:** `Note/Design`
**Structure:**
```
┌────────────────────────────┐
│ 🎨 Design Note             │
├────────────────────────────┤
│ Using cards instead of     │
│ list for better scannability│
└────────────────────────────┘
```

### 3. Dev Note
**Use when:** Technical specs, API endpoints, implementation details
**Component:** `Note/Dev`
**Structure:**
```
┌────────────────────────────┐
│ 💻 Dev Note                │
├────────────────────────────┤
│ Endpoint: POST /auth/login │
│ Validate email format      │
│ client-side                │
└────────────────────────────┘
```

### 4. Question Note
**Use when:** Open questions, things to discuss, pending decisions
**Component:** `Note/Question`
**Structure:**
```
┌────────────────────────────┐
│ ❓ Question                │
├────────────────────────────┤
│ Should we show password    │
│ strength indicator?        │
└────────────────────────────┘
```

## Placement Rules

1. **Below the screen** - Notes go directly below their related screen
2. **Left-aligned** - Align with the left edge of the screen
3. **Spacing** - 24px gap between screen and note
4. **Width** - Match screen width or use fixed 300px for side notes
5. **Multiple notes** - Stack vertically with 16px gap

## Layout Example
```
┌─────────────────────┐
│                     │
│    Login Screen     │
│                     │
└─────────────────────┘
         ↓ 24px gap
┌─────────────────────┐
│ 📊 Business Note    │
│ User must accept    │
│ terms before login  │
└─────────────────────┘
         ↓ 16px gap
┌─────────────────────┐
│ 💻 Dev Note         │
│ Check ToS version   │
│ from /api/legal     │
└─────────────────────┘
```

## Creating Notes

```javascript
// Use component instances, not raw frames
create_component_instance({
  componentKey: "Note/Business",  // Get key from get_local_components
  x: screenX,
  y: screenY + screenHeight + 24,  // Position below screen
})

// Then set the text content
set_text_content({
  nodeId: "note_body_text_id",
  text: "Your note content here..."
})
```

## When to Add Notes

- **Every screen** should have at least one note explaining its purpose
- **Complex interactions** need design notes
- **API-dependent screens** need dev notes
- **Unresolved items** need question notes

---

**Rule:** If a developer or PM would ask "why?" about something, add a note.
