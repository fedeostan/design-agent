# Code-to-Canvas Workflow

Push designs into Figma using `generate_figma_design` — the only write path available via the Figma MCP.

**Purpose:** Get screen designs into Figma as clean, responsive, design-system-aware frames
**Source:** Learned from Capo auth screen builds (Feb 2026)

---

## Overview: Three Phases

```
Phase 1 — Design System Sync     (once per project)
Phase 2 — Screen Capture          (per screen)
Phase 3 — Design System Binding   (post-capture)
```

---

## Phase 1: Design System Sync (Once Per Project)

Run this once when starting a new project or when tokens change.

### 1.1 Sync Code Tokens → Figma Variables

Use the token sync script to create Figma variables from your codebase:

```bash
python3 scripts/sync-tokens-to-figma.py \
    --tokens tokens.json \
    --file-key YOUR_FIGMA_FILE_KEY \
    --token YOUR_FIGMA_PAT
```

This creates a "Tokens" variable collection in Figma with COLOR and FLOAT variables matching your code tokens. Future captures will have matching variables ready for binding.

**Token file format** (JSON):
```json
{
  "colors": {
    "primary": "#7c3aed",
    "primary-light": "#ddd6fe",
    "background": "#fafafa"
  },
  "spacing": {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32
  }
}
```

### 1.2 Catalog Available Components

Read existing components so you know what's available for post-capture swaps:

```
get_local_components(fileKey: "...")
```

Document the component inventory — you'll reference this in Phase 3 when swapping raw frames for component instances.

### 1.3 Verify Variables Exist

Confirm the sync worked:

```
get_variable_defs(fileKey: "...")
```

Should return the tokens you just synced. Record the exact values — you'll use these in Phase 2 HTML generation.

---

## Phase 2: Screen Capture (Per Screen)

Repeat this for each screen you need in Figma.

### 2.1 Get Visual Reference

Either screenshot an existing Figma frame or the live app:
```
get_screenshot(fileKey: "...", nodeId: "...", format: "png")
```

### 2.2 Read Design Context + Tokens

Get existing styles and the token values from Phase 1:
```
get_design_context(fileKey: "...", nodeId: "...")
get_variable_defs(fileKey: "...")
```

Use the returned token values as exact CSS values in your HTML. This ensures visual accuracy and makes Phase 3 binding straightforward.

### 2.3 Create Minimal Flat HTML

Build an HTML file that represents the screen. **This is the critical step.**

Rules for clean Figma output:
- **Max 3 levels of nesting** — every extra `<div>` becomes a Figma frame
- **Semantic class names on EVERY element** — they become Figma layer names (`.card-title` not `.css-1a2b3c`). Never leave a `<div>` without a class.
- **Flexbox on EVERY container** — CSS `display: flex` converts to Figma auto-layout. Every element that has children MUST use flexbox with explicit `flex-direction`, `align-items`, `justify-content`, and `gap`. This is how we get fully responsive frames.
- **Use exact token values** — e.g., `color: #7c3aed` matching `primary` variable, not approximations
- **Inline styles or `<style>` block** — no external CSS files
- **Fixed viewport** — set `<meta name="viewport" content="width=390">` for mobile
- **No JavaScript frameworks** — pure HTML/CSS only

### 2.4 Add the Capture Script

Include in `<head>`:
```html
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
```

### 2.5 Serve and Capture

```bash
# Serve locally
python3 -m http.server 8080
```

Then use `generate_figma_design` to get a capture ID.

**CRITICAL — Use `figmaselector=body` to capture only the body element:**
```bash
# macOS — note the &figmaselector=body parameter
open "http://localhost:8080/screen.html#figmacapture=<ID>&figmaendpoint=<ENDPOINT>&figmadelay=1000&figmaselector=body"
```

The `figmaselector=body` parameter ensures only the `<body>` element is captured — without it, the capture grabs the full browser viewport (e.g. 1425px wide on a laptop) and wraps your mobile frame inside an oversized parent frame.

**CRITICAL — Open in incognito / private window:**
Browser extensions (Grammarly, password managers, ad blockers) inject DOM nodes that become phantom 0-width/0-height frames in Figma. Always capture in an incognito window with extensions disabled. If you cannot open incognito programmatically, warn the user to do so manually.

### 2.5a Automated Capture with Playwright

If Playwright MCP tools are available, automate the capture instead of opening a browser manually.

**Critical:** Resize the viewport BEFORE navigating — Playwright's default viewport (1280x720) gets baked into the page layout at navigation time.

```
1. browser_close()                           # Clean session, no extensions
2. browser_resize(width: 390, height: 844)   # MUST be before navigate
3. browser_navigate(url: "http://localhost:8080/<file>.html#figmacapture=<ID>&figmaendpoint=<ENDPOINT>&figmadelay=1000&figmaselector=body")
4. browser_wait_for(time: 3000)              # Wait for capture submission
5. browser_take_screenshot()                 # Verify it worked
```

**Fallback:** If Playwright is unavailable, use the manual flow in 2.5 above.

See also: `.claude/skills/text-to-figma/prompts/playwright-capture.md` for full procedure and troubleshooting.

### 2.6 Verify Capture

```
get_screenshot(fileKey: "...", nodeId: "[new frame ID]")
get_metadata(fileKey: "...", nodeId: "[new frame ID]")
```

Check:
- **Frame dimensions** — should match viewport exactly (e.g. 390x844), NOT browser viewport size
- **No phantom frames** — no 0-width/0-height "Container" or extension-injected frames
- **Auto-layout** — every container should have auto-layout (from flexbox in HTML)
- **Nesting depth** — should be ~3 levels, not 10+
- **Layer names** — should be semantic class names, not generic "Container"

---

## Phase 3: Design System Binding (Post-Capture)

After capture, frames have hardcoded values. This phase connects them to the design system.

### 3.1 Generate Binding Checklist

Compare the captured frame's metadata against your token map to produce a binding checklist:

```
Binding Checklist — [ScreenName/State]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Variable Bindings:
  □ .header-bg fill #7c3aed → bind to "colors/primary"
  □ .card fill #ffffff → bind to "colors/card"
  □ .body-text fill #27272a → bind to "colors/foreground"
  □ .muted-text fill #71717a → bind to "colors/muted"
  □ .border stroke #e4e4e7 → bind to "colors/border"
  □ .section padding 24px → bind to "spacing/lg"

Component Swaps:
  □ .primary-button frame → swap to "Button/Primary" component
  □ .text-input frame → swap to "Input/Text" component
  □ .card frame → swap to "Card/Default" component
```

### 3.2 Execute Binding

The user executes the checklists in Figma UI:

**Variable binding:** Select node → right panel → apply variable to fill/stroke/spacing
**Component swap:** Select raw frame → right-click → swap to component instance

### 3.3 Verify Final Result

After binding:
```
get_screenshot(fileKey: "...", nodeId: "[frame ID]")
```

Confirm the screen looks identical before and after binding — values should match since we used exact token values in Phase 2.

---

## HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=390">
<title>[ScreenName/State]</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  /* RULE: Every element with children MUST use display:flex.
     This converts to Figma auto-layout for responsive frames. */

  body {
    width: 390px;
    height: 844px;
    background: #fafafa;
    font-family: Inter, -apple-system, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 24px 0 24px;
    gap: 32px;
  }

  /* --- Add screen-specific styles here --- */
  /* Use semantic class names: .card, .card-title, .field-input */
  /* Keep selectors flat — avoid deep nesting */
  /* EVERY container: display:flex + flex-direction + align-items + gap */
  /* Use exact token values from get_variable_defs */
</style>
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
</head>
<body>

<!-- Keep DOM structure flat: max 3 levels -->
<!-- body > section > element -->
<!-- Every container MUST have a class name and use flexbox -->

</body>
</html>
```

---

## Flexbox → Auto-Layout Cheat Sheet

The capture script converts CSS flexbox properties to Figma auto-layout:

| CSS Property | Figma Auto-Layout |
|---|---|
| `display: flex` | Enables auto-layout on the frame |
| `flex-direction: column` | Vertical auto-layout |
| `flex-direction: row` | Horizontal auto-layout |
| `gap: 16px` | Item spacing = 16 |
| `padding: 24px` | Frame padding = 24 |
| `align-items: center` | Cross-axis alignment = center |
| `justify-content: center` | Primary axis alignment = center |
| `align-items: stretch` + `width: 100%` on children | Fill container |

**Rule:** If an element has children, it MUST have `display: flex`. No exceptions. This ensures every frame in Figma has auto-layout, making the design fully responsive — like real products.

---

## Capture URL Parameters

| Parameter | Purpose | Required? |
|---|---|---|
| `figmacapture=<ID>` | Capture ID from generate_figma_design | Yes |
| `figmaendpoint=<URL>` | Submission endpoint | Yes |
| `figmadelay=1000` | Wait 1s before capture (for fonts to load) | Recommended |
| `figmaselector=body` | **Capture only the body element** — prevents oversized browser-viewport wrapper frame | **Always use for mobile screens** |
| `figmaselector=.my-class` | Capture a specific element by CSS selector | Optional |

---

## Known Limitations

Even with clean HTML, expect these issues:

| Issue | Workaround |
|-------|-----------|
| Generic "Container" names for unnamed divs | Put a semantic class name on EVERY element — no exceptions |
| No component instances | Captured frames are raw — swap to component instances in Phase 3 |
| No variable bindings | Captured values are hardcoded — bind to variables in Phase 3 |
| Font rendering differences | Ensure fonts are loaded (use system fonts or Google Fonts link) |
| CSS custom properties resolved | Browser computes them — variable names lost. Use exact values instead. |

---

## Anti-Patterns

**Never do these:**

1. **Capture directly from React/Next.js/React Native Web apps** — framework DOM wrappers create 10+ nesting levels, all named "Container" or with CSS hash class names
2. **Use external CSS files** — the capture script may not resolve them
3. **Include interactive JavaScript** — animations/transitions create extra frames
4. **Skip the viewport meta tag** — results in wrong dimensions
5. **Nest `<div>`s deeply** — every unnecessary wrapper becomes a Figma frame
6. **Skip `figmaselector=body`** — results in a browser-viewport-sized outer frame wrapping your mobile frame
7. **Capture with browser extensions active** — Grammarly, password managers, etc. inject phantom 0x0 frames
8. **Omit `display: flex` on containers** — results in frames without auto-layout (not responsive)
9. **Use approximate color values** — always use exact token values so Phase 3 binding is straightforward
10. **Navigate before resizing in Playwright** — the viewport at navigation time determines the layout. Always `browser_resize()` BEFORE `browser_navigate()`

---

## Decision: When to Re-capture vs Manual Fix

```
Messy Figma capture?
  ├─ 5+ nesting levels? → Re-capture with clean HTML
  ├─ Wrong dimensions / oversized wrapper? → Re-capture with figmaselector=body
  ├─ Phantom 0x0 frames? → Re-capture in incognito mode
  ├─ Missing auto-layout? → Re-capture with flexbox on all containers
  ├─ Good structure, minor issues? → Fix manually in Figma UI
  └─ Only needs text/color updates? → Fix manually in Figma UI
```

---

**Source:** Capo auth screen builds — Sign In + Sign Up captures (Feb 2026)
**Last Updated:** 2026-02-18
