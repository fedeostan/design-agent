# Post-Capture Verification (Quality Gate)

**Purpose:** 5-check quality gate after each Figma capture. Run immediately after every `generate_figma_design` capture completes.
**Rule:** If any check fails, route to recapture or manual fix before proceeding.

---

## Verification Procedure

After capture, call:
```
get_metadata(fileKey: "...", nodeId: "[new frame ID]")
get_screenshot(fileKey: "...", nodeId: "[new frame ID]", format: "png")
```

Then run all 5 checks against the metadata:

---

### Check 1: Frame Dimensions

**Expected:** Matches pre-flight viewport (default 390x844)
**How to verify:** Check the root frame's `absoluteBoundingBox` width and height.

| Result | Action |
|--------|--------|
| Width = 390, Height = 844 | **Pass** |
| Width ≈ 1280 or 1425 | **Fail — Recapture.** Viewport wasn't set before navigation. See `playwright-capture.md` step 2. |
| Width = 390, Height differs | **Pass** (content height may vary) |

### Check 2: Phantom Frames

**Expected:** No 0x0 elements in the frame tree.
**How to verify:** Traverse `children` recursively. Flag any node with `width: 0` or `height: 0`.

| Result | Action |
|--------|--------|
| No 0x0 nodes | **Pass** |
| 0x0 nodes found | **Fail — Recapture.** Browser extensions injected DOM. Use `browser_close()` for clean session or instruct user to open incognito. |

### Check 3: Auto-Layout Present

**Expected:** All container frames have `layoutMode` set (HORIZONTAL or VERTICAL).
**How to verify:** Check every FRAME node that has children for `layoutMode` property.

| Result | Action |
|--------|--------|
| All containers have layoutMode | **Pass** |
| Some containers lack layoutMode | **Fail — Recapture.** HTML containers missing `display: flex`. Fix the HTML source, add flexbox to all containers, then recapture. |

### Check 4: Layer Names

**Expected:** Semantic names (e.g., "card-title", "header-section"), NOT generic names.
**How to verify:** Check `name` property of all nodes. Flag any named "Container", "Frame", "Group", or similar generics.

| Result | Action |
|--------|--------|
| All names are semantic | **Pass** |
| 1-3 generic names | **Minor — Manual fix.** Rename in Figma UI. Add to binding checklist. |
| 4+ generic names | **Fail — Recapture.** HTML elements missing class names. Fix the HTML, add semantic classes to all elements, then recapture. |

### Check 5: Nesting Depth

**Expected:** Max 4 levels deep (body → section → element → child).
**How to verify:** Walk the tree and count max depth.

| Result | Action |
|--------|--------|
| Depth ≤ 4 | **Pass** |
| Depth 5-6 | **Minor — Acceptable** but note for future improvement. |
| Depth 7+ | **Fail — Recapture.** HTML has too many wrapper divs. Flatten the structure. |

---

## Verification Summary Template

After running all checks, produce this summary:

```
POST-CAPTURE VERIFICATION — [ScreenName/State]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Frame ID:       [node ID]
Dimensions:     [width]x[height]  ✅ / ❌
Phantom frames: [count] found     ✅ / ❌
Auto-layout:    [x]/[total] have layout  ✅ / ❌
Layer names:    [generic count] generic  ✅ / ⚠️ / ❌
Nesting depth:  [max depth] levels       ✅ / ⚠️ / ❌
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Result:         PASS / NEEDS RECAPTURE / NEEDS MANUAL FIX
```

---

## Routing Decision

```
All 5 checks pass?
  → YES: Proceed to binding checklist (Phase 3)
  → NO, any ❌ (Fail):
      → Fix the root cause in HTML
      → Recapture using playwright-capture.md
      → Re-run this verification
  → NO, only ⚠️ (Minor):
      → Add manual fixes to binding checklist
      → Proceed to binding checklist
```
