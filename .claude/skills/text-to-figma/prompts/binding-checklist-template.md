# Binding Checklist Template

**Purpose:** Template for generating Phase 3 binding checklists after capture.
**Rule:** Sections are conditional — only include what's available based on pre-flight results.

---

## How to Generate

1. Read the pre-flight summary for `tokens_synced` and `components_available` flags
2. Get the captured frame's metadata: `get_metadata(fileKey, nodeId)`
3. Compare metadata values against `tokens.json` and component inventory
4. Fill in the template below, omitting sections marked as conditional

---

## Template

```
BINDING CHECKLIST — [ScreenName/State]
Frame ID: [node ID]
Generated: [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{{IF tokens_synced}}
VARIABLE BINDINGS
Map hardcoded values to Figma variables from the "Tokens" collection.

  Colors:
  □ [layer] fill [hex] → bind to "colors/[token-name]"
  □ [layer] fill [hex] → bind to "colors/[token-name]"
  □ [layer] stroke [hex] → bind to "colors/[token-name]"

  Spacing:
  □ [layer] padding [px] → bind to "spacing/[token-name]"
  □ [layer] gap [px] → bind to "spacing/[token-name]"

  Radii:
  □ [layer] cornerRadius [px] → bind to "radii/[token-name]"

{{ELSE}}
VARIABLE BINDINGS — SKIPPED
Tokens were not synced to Figma. Values remain hardcoded.
To enable: run `python3 scripts/sync-tokens-to-figma.py` and recapture.
{{END}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{{IF components_available}}
COMPONENT SWAPS
Replace raw captured frames with component instances.

  □ [layer ".primary-button"] → swap to "[Button/Primary]"
  □ [layer ".text-input"] → swap to "[Input/Text]"
  □ [layer ".card"] → swap to "[Card/Default]"

How to swap: Select frame → right-click → "Swap component" → search for target
{{ELSE}}
COMPONENT SWAPS — SKIPPED
No components available in this file. Raw frames will remain.
To enable: create components in Figma, then re-run pipeline.
{{END}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MANUAL FIXES
From post-capture verification findings:

  Layer Renames:
  □ Rename "[generic name]" → "[semantic name]"

  Other Fixes:
  □ [describe any other manual adjustments needed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Example: Fully Populated

```
BINDING CHECKLIST — SignIn/Default
Frame ID: 123:456
Generated: 2026-02-18
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VARIABLE BINDINGS

  Colors:
  □ header-bg fill #7c3aed → bind to "colors/primary"
  □ body fill #fafafa → bind to "colors/background"
  □ card fill #ffffff → bind to "colors/card-bg"
  □ card stroke #e4e4e7 → bind to "colors/card-border"
  □ heading-text fill #27272a → bind to "colors/text-dark"
  □ subtitle-text fill #71717a → bind to "colors/text-muted"

  Spacing:
  □ card-content padding 24px → bind to "spacing/lg"
  □ form-fields gap 16px → bind to "spacing/md"
  □ button-group gap 8px → bind to "spacing/sm"

  Radii:
  □ card cornerRadius 16px → bind to "radii/lg"
  □ input cornerRadius 8px → bind to "radii/md"
  □ button cornerRadius 9999px → bind to "radii/pill"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPONENT SWAPS

  □ sign-in-button → swap to "Button/Primary"
  □ email-input → swap to "Input/Text"
  □ password-input → swap to "Input/Password"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MANUAL FIXES

  Layer Renames:
  □ (none — all layers have semantic names)

  Other Fixes:
  □ (none — post-capture verification passed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Execution Notes

- The user executes variable bindings and component swaps in Figma UI
- After binding, run `get_screenshot` to verify the screen looks identical (values should match since we used exact token values in the HTML)
- If visual differences appear after binding, a token value mismatch was present — check and fix
