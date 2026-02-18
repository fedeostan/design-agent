# Code-to-Canvas Workflow

Push designs into Figma using `generate_figma_design` — the only write path available via the Figma MCP.

**Purpose:** Get screen designs into Figma as clean, flat frames
**Source:** Learned from Capo login screen cleanup (Feb 2026)

---

## When to Use

- Capturing a live app screen into Figma
- Rebuilding a messy/nested Figma capture
- Creating new screens from scratch
- Any time you need to write design content into Figma

## The Clean HTML Re-capture Technique

### Step 1: Get a Visual Reference

Either screenshot an existing Figma frame or the live app:
```bash
get_screenshot(fileKey: "...", nodeId: "...", format: "png")
```

### Step 2: Get Design Context

If matching an existing design, extract styles and tokens:
```bash
get_design_context(fileKey: "...", nodeId: "...")
get_variable_defs(fileKey: "...")
```

### Step 3: Create Minimal Flat HTML

Build an HTML file that represents the screen. **This is the critical step.**

Rules for clean Figma output:
- **Max 3 levels of nesting** — every extra `<div>` becomes a Figma frame
- **Semantic class names** — they become Figma layer names (`.card-title` not `.css-1a2b3c`)
- **Inline styles or `<style>` block** — no external CSS files
- **Fixed viewport** — set `<meta name="viewport" content="width=390">` for mobile
- **No JavaScript frameworks** — pure HTML/CSS only
- **No browser extensions active** — they inject DOM nodes that become phantom Figma layers

### Step 4: Add the Capture Script

Include in `<head>`:
```html
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
```

### Step 5: Serve and Capture

```bash
# Serve locally
python3 -m http.server 8080

# Open in browser with capture URL
# The capture script communicates with Figma Desktop
```

Then use `generate_figma_design` with the HTML content or URL.

### Step 6: Verify

```bash
get_screenshot(fileKey: "...", nodeId: "[new frame ID]")
get_metadata(fileKey: "...", nodeId: "[new frame ID]")
```

Check:
- Nesting depth (should be ~3 levels, not 10+)
- Layer names match class names
- Dimensions match viewport
- No phantom/hidden artifacts

---

## HTML Template

Based on the successful Capo login clean capture:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=390">
<title>[Screen Name]</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 390px;
    height: 844px;
    background: #fafafa;
    font-family: Inter, -apple-system, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 24px 0 24px;
  }

  /* --- Add screen-specific styles here --- */
  /* Use semantic class names: .card, .card-title, .field-input */
  /* Keep selectors flat — avoid deep nesting */
</style>
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
</head>
<body>

<!-- Keep DOM structure flat: max 3 levels -->
<!-- body > section > element -->

</body>
</html>
```

---

## Known Limitations

Even with clean HTML, expect these issues:

| Issue | Workaround |
|-------|-----------|
| No auto-layout on captured frames | Apply manually in Figma UI, or document layout intent in annotations |
| Generic "Container" names for unnamed divs | Use semantic class names on every element |
| Wrong dimensions if viewport not set | Always set `<meta name="viewport" content="width=390">` |
| Phantom artifacts from browser extensions | Use incognito mode or disable extensions |
| No component instances | Captured frames are raw — swap to component instances manually if needed |
| Font rendering differences | Ensure fonts are loaded (use system fonts or Google Fonts link) |

---

## Anti-Patterns

**Never do these:**

1. **Capture directly from React/Next.js/React Native Web apps** — framework DOM wrappers create 10+ nesting levels, all named "Container" or with CSS hash class names
2. **Use external CSS files** — the capture script may not resolve them
3. **Include interactive JavaScript** — animations/transitions create extra frames
4. **Skip the viewport meta tag** — results in wrong dimensions
5. **Nest `<div>`s deeply** — every unnecessary wrapper becomes a Figma frame

---

## Decision: When to Re-capture vs Manual Fix

```
Messy Figma capture?
  ├─ 5+ nesting levels? → Re-capture with clean HTML
  ├─ Wrong dimensions? → Re-capture with correct viewport
  ├─ Good structure, minor issues? → Fix manually in Figma UI
  └─ Only needs text/color updates? → Fix manually in Figma UI
```

---

**Source:** Capo login screen cleanup — React Native Web capture (10 levels) vs clean HTML capture (3 levels)
**Last Updated:** 2026-02-18
