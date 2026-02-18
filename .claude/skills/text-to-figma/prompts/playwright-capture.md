# Playwright Capture Procedure

**Purpose:** Automate the HTML-to-Figma capture using Playwright MCP tools.
**Critical Fix:** Always `browser_resize` BEFORE `browser_navigate` — Playwright's default viewport (1280x720) gets baked into the page layout if you navigate first.

---

## Automated Capture Steps

### Step 1: Close Any Existing Browser
```
browser_close()
```
Ensures a clean session with no extensions or prior state.

### Step 2: Resize Viewport FIRST
```
browser_resize(width: 390, height: 844)
```
**CRITICAL:** This MUST happen before navigation. The viewport size at navigation time determines the page layout. If you navigate first, the page renders at 1280x720 and resizing after won't fix the layout.

Use the dimensions from the pre-flight summary (default: 390x844).

### Step 3: Navigate to Capture URL
```
browser_navigate(url: "http://localhost:8080/screen.html#figmacapture=<ID>&figmaendpoint=<ENDPOINT>&figmadelay=1000&figmaselector=body")
```

**URL parameters:**
- `figmacapture=<ID>` — from `generate_figma_design` response
- `figmaendpoint=<ENDPOINT>` — from `generate_figma_design` response
- `figmadelay=1000` — wait 1s for fonts to load
- `figmaselector=body` — **always include** to prevent oversized wrapper frame

### Step 4: Wait for Capture
```
browser_wait_for(time: 3000)
```
Wait 3 seconds for the capture script to:
1. Parse the URL hash parameters
2. Wait the specified delay (1000ms)
3. Serialize the DOM
4. Submit to the Figma endpoint

### Step 5: Verify Submission
```
browser_take_screenshot()
```
The page should show a capture confirmation or the original content. If it shows an error, check:
- Is the local server running? (`python3 -m http.server 8080`)
- Is the capture ID valid? (Re-call `generate_figma_design` if expired)

---

## Full Sequence (Copy-Paste Ready)

```
1. browser_close()
2. browser_resize(width: 390, height: 844)
3. browser_navigate(url: "http://localhost:8080/<file>.html#figmacapture=<ID>&figmaendpoint=<ENDPOINT>&figmadelay=1000&figmaselector=body")
4. browser_wait_for(time: 3000)
5. browser_take_screenshot()
```

---

## Manual Fallback (When Playwright Unavailable)

If Playwright MCP tools are not available, instruct the user:

1. Start local server: `python3 -m http.server 8080`
2. Call `generate_figma_design` to get capture ID and endpoint
3. Open **incognito/private window** (critical — extensions inject phantom frames)
4. Resize browser window to approximately 390px wide
5. Navigate to: `http://localhost:8080/<file>.html#figmacapture=<ID>&figmaendpoint=<ENDPOINT>&figmadelay=1000&figmaselector=body`
6. Wait for capture confirmation
7. Check Figma file for the new frame

---

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Frame is 1280px wide | Navigated before resizing | Close browser, resize first, then navigate |
| Frame is ~1425px wide | Browser viewport captured instead of body | Add `figmaselector=body` to URL |
| Phantom 0x0 frames | Extensions injected DOM nodes | Use `browser_close()` first for clean session |
| Capture timeout | Server not running or ID expired | Check server, regenerate capture ID |
| Fonts look wrong | Fonts not loaded before capture | Increase `figmadelay` to 2000 |

---

## Anti-Pattern: Navigate Then Resize

```
# WRONG — page renders at default 1280x720 viewport
browser_navigate(url: "http://localhost:8080/screen.html...")
browser_resize(width: 390, height: 844)  # Too late!

# RIGHT — viewport set before page renders
browser_resize(width: 390, height: 844)
browser_navigate(url: "http://localhost:8080/screen.html...")
```
