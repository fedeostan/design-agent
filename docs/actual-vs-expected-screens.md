# Actual vs Expected: Capo Screens Analysis

**Date:** February 17, 2026
**Analyzed with:** Official Figma MCP (`mcp.figma.com`)
**File:** [Capo Figma File](https://www.figma.com/design/OOJFumY5Xv9SDD4hX0S9fY/Capo)

---

## Executive Summary

Two screens were completed: **Auth/Login** and **Auth/SignUp**. Both have significant issues when compared to the PRD requirements:

- **Auth/Login:** Missing input fields and button (only has labels) ❌
- **Auth/SignUp:** Uses component instances ✅ but text content not updated ⚠️

**Key Finding:** Auth/SignUp is significantly better because it uses component instances from the Design System, whereas Auth/Login was built with raw elements only.

---

## Screen 1: Auth/Login (Node 24:2)

### Visual Preview

![Auth/Login Screenshot](screenshot showing logo, card with "Welcome Back", labels for Email and Password, and footer link)

### Expected (from PRD)

**Source:** [capo-reverse-engineer-prd.md](capo-reverse-engineer-prd.md#auth-login) (lines 39-48)

```
Background: Gray-50 (#fafafa)
Logo: 80x40 violet-200 rounded-12px with "Capo" text (violet-600, 24px/700)

Card (white, border gray-200, 8px radius, shadow):
  ├─ CardHeader
  │   ├─ Title: "Welcome Back" (20px/700)
  │   └─ Description: "Enter your credentials to access your dashboard" (14px/400, gray-500)
  │
  ├─ CardContent
  │   ├─ Input: Email with placeholder "name@example.com"
  │   ├─ Input: Password with placeholder "Password"
  │   └─ Button/Default size=lg: "Sign In" (violet-600 bg, white text, 48px height)
  │
  └─ CardFooter
      └─ Link: "Don't have an account? Sign Up" (violet-600, underlined)
```

### Actual (from Figma)

**Structure (from get_design_context):**

```jsx
<div className="bg-[#fafafa]" data-node-id="24:2">
  {/* Logo */}
  <div className="bg-[#ddd6fe] h-[40px] w-[80px] rounded-[12px]" data-node-id="24:3" />
  <p className="text-[#7c3aed] text-[24px] font-bold" data-node-id="24:4">Capo</p>

  {/* Card */}
  <div className="bg-white border border-[#e4e4e7] rounded-[8px] shadow-[...]" data-node-id="24:5">
    <p className="text-[20px] font-bold" data-node-id="24:6">Welcome Back</p>
    <p className="text-[#71717a] text-[14px]" data-node-id="24:7">
      Enter your credentials to access your dashboard
    </p>

    {/* Only labels - NO INPUT COMPONENTS */}
    <p className="text-[#3f3f46] text-[14px] font-medium" data-node-id="24:8">Email</p>
    <p className="text-[#3f3f46] text-[14px] font-medium" data-node-id="24:11">Password</p>

    {/* NO BUTTON COMPONENT */}

    {/* Footer link */}
    <p className="text-[#7c3aed] text-[14px] underline" data-node-id="24:16">
      Don't have an account? Sign Up
    </p>
  </div>
</div>
```

### Comparison Table

| Element | Expected | Actual | Status |
|---------|----------|--------|--------|
| **Layout** |
| Background color | #fafafa (gray-50) | #fafafa | ✅ Correct |
| Card background | White with border | White with border #e4e4e7 | ✅ Correct |
| Card shadow | 0 1px 2px rgba(0,0,0,0.05) | 0px 1px 2px 0px rgba(0,0,0,0.05) | ✅ Correct |
| Card radius | 8px | 8px | ✅ Correct |
| **Logo** |
| Logo background | 80x40, #ddd6fe, radius 12px | 80x40, #ddd6fe, radius 12px | ✅ Correct |
| Logo text | "Capo", 24px, bold, #7c3aed | "Capo", 24px, bold, #7c3aed | ✅ Correct |
| **Header** |
| Title | "Welcome Back", 20px/700 | "Welcome Back", 20px/700 | ✅ Correct |
| Description | 14px/400, #71717a | 14px/400, #71717a | ✅ Correct |
| **Inputs** |
| Email input field | Input/Default component with placeholder | ❌ **Only text label "Email"** | ❌ **MISSING** |
| Password input field | Input/Default component with placeholder | ❌ **Only text label "Password"** | ❌ **MISSING** |
| **Button** |
| Sign In button | Button/Default size=lg (48px height) | ❌ **Completely missing** | ❌ **MISSING** |
| **Footer** |
| Footer link | "Don't have an account? Sign Up", underlined, #7c3aed | "Don't have an account? Sign Up", underlined, #7c3aed | ✅ Correct |

### Critical Issues

1. **❌ No Input Components**
   - Expected: 2 Input/Default component instances
   - Actual: Only text labels saying "Email" and "Password"
   - Impact: Screen is non-functional — users can't enter credentials

2. **❌ No Button Component**
   - Expected: Button/Default with text "Sign In" (48px height, violet background)
   - Actual: Completely missing
   - Impact: Screen is non-functional — users can't submit form

3. **✅ Layout Structure Correct**
   - Logo, card, header text, footer link all present and correctly styled
   - Positioning and spacing appear correct

### Design System Usage

| Component | Should Use | Actually Uses |
|-----------|------------|---------------|
| Input/Default | ✅ Required (×2) | ❌ Not used (raw text instead) |
| Button/Default | ✅ Required | ❌ Not used (missing entirely) |

**Verdict:** Screen built with **raw elements only**, no component instances used for interactive elements.

---

## Screen 2: Auth/SignUp (Node 24:17)

### Visual Preview

![Auth/SignUp Screenshot](screenshot showing logo, card with "Create an Account", two input fields, button, and footer link)

### Expected (from PRD)

**Source:** [capo-reverse-engineer-prd.md](capo-reverse-engineer-prd.md#auth-signup) (lines 50-55)

```
Same layout as Login with:
  ├─ Title: "Create an Account"
  ├─ Description: "Enter your details to get started"
  ├─ Email input (with placeholder)
  ├─ Password input (with placeholder)
  ├─ Button text: "Sign Up" (violet-600 bg, 40px height for default size)
  └─ Footer: "Already have an account? Sign In"
```

### Actual (from Figma)

**Structure (from get_design_context):**

```jsx
<div className="bg-[#fafafa]" data-node-id="24:17">
  {/* Logo */}
  <div className="bg-[#ddd6fe] h-[40px] w-[80px] rounded-[12px]" data-node-id="24:18" />
  <p className="text-[#7c3aed] text-[24px] font-bold" data-node-id="24:19">Capo</p>

  {/* Card */}
  <div className="bg-white border border-[#e4e4e7] rounded-[8px] shadow-[...]" data-node-id="24:20" />

  <p className="text-[#27272a] text-[20px] font-bold" data-node-id="24:21">
    Create an Account
  </p>
  <p className="text-[#71717a] text-[14px]" data-node-id="24:22">
    Enter your details to get started
  </p>

  {/* Input component instances - GOOD! */}
  <InputDefault className="..." />  {/* Placeholder: "name@example.com" */}
  <InputDefault className="..." />  {/* Placeholder: "name@example.com" */}

  {/* Button component instance - GOOD! */}
  <ButtonDefault className="..." />  {/* Text: "Button" */}

  {/* Footer link */}
  <p className="text-[#7c3aed] text-[14px]" data-node-id="24:29">
    Already have an account? Sign In
  </p>
</div>
```

### Comparison Table

| Element | Expected | Actual | Status |
|---------|----------|--------|--------|
| **Layout** |
| Background color | #fafafa (gray-50) | #fafafa | ✅ Correct |
| Card background | White with border | White with border #e4e4e7 | ✅ Correct |
| **Logo** |
| Logo background | 80x40, #ddd6fe, radius 12px | 80x40, #ddd6fe, radius 12px | ✅ Correct |
| Logo text | "Capo", 24px, bold, #7c3aed | "Capo", 24px, bold, #7c3aed | ✅ Correct |
| **Header** |
| Title | "Create an Account", 20px/700 | "Create an Account", 20px/700, #27272a | ✅ Correct |
| Description | "Enter your details to get started", 14px/400, #71717a | "Enter your details to get started", 14px/400, #71717a | ✅ Correct |
| **Inputs** |
| Email input | Input/Default component | ✅ **Input/Default instance** | ✅ Component used |
| Email label | "Email" label above input | ❌ **No label** | ⚠️ Missing |
| Email placeholder | "name@example.com" | "name@example.com" | ✅ Correct |
| Password input | Input/Default component | ✅ **Input/Default instance** | ✅ Component used |
| Password label | "Password" label above input | ❌ **No label** | ⚠️ Missing |
| Password placeholder | Custom placeholder (not specified in PRD) | "name@example.com" | ⚠️ Not customized |
| **Button** |
| Button component | Button/Default | ✅ **Button/Default instance** | ✅ Component used |
| Button text | "Sign Up" | ❌ **"Button"** | ❌ Not updated |
| Button size | size=lg (48px height per PRD line 47) | 40px height (default size) | ⚠️ Wrong size |
| **Footer** |
| Footer link | "Already have an account? Sign In" | "Already have an account? Sign In" | ✅ Correct |
| Footer underline | Underlined | ❌ **Not underlined** | ⚠️ Missing style |

### Issues Found

1. **❌ Button Text Not Updated**
   - Expected: "Sign Up"
   - Actual: "Button" (default component text)
   - Impact: Unclear call-to-action

2. **⚠️ Missing Input Labels**
   - Expected: "Email" label above first input, "Password" label above second input (implied from Login screen)
   - Actual: No labels, just input fields
   - Impact: Reduced accessibility and clarity

3. **⚠️ Password Placeholder Not Customized**
   - Expected: Password-specific placeholder (or secure entry indication)
   - Actual: Same "name@example.com" placeholder as email field
   - Impact: Confusing UX — both inputs look identical

4. **⚠️ Button Size Wrong**
   - Expected: size=lg (48px height) per PRD Auth/Login spec
   - Actual: 40px height (default size)
   - Impact: Minor visual inconsistency

5. **⚠️ Footer Link Not Underlined**
   - Expected: Underlined link (per Auth/Login spec)
   - Actual: Not underlined
   - Impact: Reduced affordance (harder to identify as clickable)

### Design System Usage

| Component | Should Use | Actually Uses | Configured? |
|-----------|------------|---------------|-------------|
| Input/Default | ✅ Required (×2) | ✅ Used (×2) | ⚠️ Partially (placeholders not customized) |
| Button/Default | ✅ Required | ✅ Used | ❌ No (text not updated, wrong size) |

**Verdict:** Screen uses **component instances** ✅ but **content not customized** ⚠️

---

## Comparison: Login vs SignUp

| Aspect | Auth/Login | Auth/SignUp | Winner |
|--------|-----------|-------------|--------|
| **Component Usage** | ❌ No component instances | ✅ Uses Input/Default (×2) + Button/Default | **SignUp** |
| **Functionality** | ❌ Non-functional (no inputs/button) | ✅ Functional (has inputs + button) | **SignUp** |
| **Text Content** | ✅ All text correct | ⚠️ Button text wrong | **Login** |
| **Labels** | ⚠️ Labels present (but no inputs) | ❌ No labels above inputs | **Login** |
| **Overall Quality** | ❌ Broken (incomplete) | ⚠️ Usable (needs text updates) | **SignUp** |

**Key Takeaway:** Auth/SignUp is **much closer to the PRD requirements** because it uses component instances. Auth/Login appears to have been abandoned mid-build.

---

## Common Issues (Both Screens)

### 1. Absolute Positioning

Both screens use absolute positioning for all elements:

```jsx
<div className="absolute left-[48px] top-[260px]" />
<div className="absolute left-[48px] top-[316px]" />
```

**Issues:**
- ❌ No auto-layout (elements won't reflow when content changes)
- ❌ No constraints (elements won't adapt to different screen sizes)
- ❌ Difficult to maintain (changing spacing requires manual updates)

**Should use:**
- Auto-layout vertical for card content (inputs stacked)
- Auto-layout properties for spacing (8px, 16px gaps)
- Constraints for responsive behavior

### 2. No Component Properties/Variants

The Input and Button component instances don't show any property overrides:

**What's missing:**
- Input placeholder override (to customize "name@example.com" → "Password")
- Button text override (to change "Button" → "Sign Up")
- Button size variant (default → lg)

**Possible reasons:**
- Third-party MCP didn't support property overrides
- Components created without variant properties
- Manual text updates attempted but failed

### 3. Design System Partially Used

**Design System page exists** with components:
- ✅ Button/Default
- ✅ Input/Default
- ✅ Other button variants (Outline, Ghost, Destructive)

**But:**
- ❌ No Button size variants (sm, default, lg, icon)
- ❌ No Input state variants (error, focused)
- ❌ No other components (ProgressBar, Header, Note, IconPlaceholder)

---

## Root Cause Analysis

### Why Auth/Login Failed

**Hypothesis:** Screen was built manually with raw shapes before component system was available.

**Evidence:**
1. No component instances used (only raw divs and text)
2. Labels present ("Email", "Password") suggest intention to add inputs later
3. No button at all (not even raw shape) suggests incomplete work
4. Quality of layout (correct colors, spacing, structure) suggests skill, not ignorance

**Timeline guess:**
1. Built logo, card, header text ✅
2. Added "Email" and "Password" labels ✅
3. **Intended to create input components next** 🔄
4. **Work stopped before inputs/button added** ⏸️

### Why Auth/SignUp Succeeded (Partially)

**Hypothesis:** Screen was built by subagent *after* component system was created.

**Evidence:**
1. Uses Input/Default component instances (×2)
2. Uses Button/Default component instance
3. Missing labels suggest different build approach (bottom-up vs top-down)
4. Placeholder/button text not updated suggests **component instances created but not configured**

**Timeline guess:**
1. Built logo, card, header text ✅
2. Created Input/Default component instances ✅
3. Created Button/Default component instance ✅
4. **Forgot to update component text/properties** ❌
5. Added footer link ✅

---

## What Third-Party MCP Could/Couldn't Do

Based on actual output, the third-party MCP (`claude-talk-to-figma-mcp`) was able to:

### ✅ What Worked

1. **Create frames and basic shapes**
   - Rectangles with fills, borders, radius
   - Text nodes with font properties
   - Nested structures (card inside frame)

2. **Set visual properties**
   - Fill colors (RGB 0-1 format)
   - Border colors and widths
   - Border radius
   - Shadows
   - Font size, weight, color

3. **Position elements**
   - Absolute x/y coordinates
   - Width and height

4. **Create component instances** (SignUp screen proves this)
   - Input/Default instances created
   - Button/Default instance created

### ❌ What Failed or Wasn't Available

1. **Update component instance text**
   - Button still says "Button" instead of "Sign Up"
   - Input placeholders not customized (both say "name@example.com")

2. **Auto-layout**
   - All elements use absolute positioning
   - No flex/auto-layout properties visible

3. **Component properties/variants**
   - No evidence of variant switching (e.g., default → lg size)
   - No property overrides visible

4. **Labels for inputs**
   - Login screen has labels but no inputs
   - SignUp screen has inputs but no labels
   - Suggests confusion about how to structure input fields properly

---

## Recommendations

### Immediate Actions (Current Project)

1. **Delete broken Auth/Login screen**
   - Start fresh with component-based approach
   - Use Auth/SignUp as reference pattern

2. **Fix Auth/SignUp screen:**
   ```
   ✓ Add "Email" label above first input (14px medium, gray-700, 8px margin-bottom)
   ✓ Add "Password" label above second input
   ✓ Update button text: "Button" → "Sign Up"
   ✓ Change button size to lg variant (48px height)
   ✓ Add underline to footer link
   ✓ Change second input placeholder to "Password" or secure entry indicator
   ```

3. **Rebuild Auth/Login screen:**
   - Use same component pattern as SignUp
   - Copy-paste SignUp, then update text:
     - Title: "Create an Account" → "Welcome Back"
     - Description: "Enter your details to get started" → "Enter your credentials to access your dashboard"
     - Button: "Sign Up" → "Sign In"
     - Footer: "Already have an account? Sign In" → "Don't have an account? Sign Up"

4. **Complete component library before building more screens:**
   - Button size variants (sm, default, lg)
   - ProgressBar component
   - Header component
   - Note components (4 variants)
   - IconPlaceholder (2 sizes)

### Process Improvements (Future Projects)

See: [design-failure-analysis.md](design-failure-analysis.md#recommendations-for-next-time)

**Key changes:**
1. ✅ Use official Figma MCP only (`https://mcp.figma.com/mcp`)
2. ✅ Build complete component library BEFORE screens
3. ✅ Test component instance creation + text updates BEFORE building screens
4. ✅ Build 1 screen fully, verify, then continue
5. ✅ Use auto-layout wherever possible (not absolute positioning)

---

## Quality Metrics

### Auth/Login Quality Score: 3/10

| Category | Score | Notes |
|----------|-------|-------|
| Visual design | 7/10 | Layout, colors, spacing correct |
| Component usage | 0/10 | No components used (raw shapes only) |
| Completeness | 2/10 | Missing inputs and button |
| PRD compliance | 3/10 | Structure correct, content incomplete |

**Grade:** ❌ **Fail** — Non-functional screen

### Auth/SignUp Quality Score: 6/10

| Category | Score | Notes |
|----------|-------|-------|
| Visual design | 8/10 | Layout, colors, spacing correct |
| Component usage | 7/10 | Uses component instances but not configured |
| Completeness | 6/10 | All elements present but text wrong |
| PRD compliance | 6/10 | Structure correct, details need updates |

**Grade:** ⚠️ **Needs Revision** — Functional but incomplete

---

## Conclusion

**Auth/SignUp is significantly better than Auth/Login** because it uses component instances from the Design System. This proves the third-party MCP *could* create component instances, but struggled with:

1. Updating component instance text/properties
2. Adding labels above inputs
3. Choosing correct component variants

**Auth/Login appears abandoned mid-build**, suggesting the original approach (raw shapes) was abandoned in favor of a component-based approach (SignUp).

**Next step:** Fix SignUp screen issues, rebuild Login screen using same pattern, verify both screens before building remaining 7 screens.
