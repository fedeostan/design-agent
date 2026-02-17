# Capo App — Reverse Engineering PRD

*Created: 2026-02-13*
*Source: `/Users/federicoostan/Capo/` (React Native + Expo)*

---

## 1. Objective

Reverse engineer the Capo construction project management app's first 3 screen groups into a Figma design file. The goal is to create a complete, component-based Figma source of truth for Auth, Onboarding, and Dashboard screens.

---

## 2. Scope

### In Scope
| Group | Screens | Count |
|-------|---------|-------|
| Auth | Login, SignUp, Login-Loading, Login-Error | 4 |
| Onboarding | Profile (Step 1/3), ProjectSetup (Step 2/3), Timeline (Step 3/3) | 3 |
| Dashboard | Default (with projects), Empty (no projects) | 2 |
| **Total** | | **9 frames** |

### Out of Scope
- ProjectDetail screen
- ProjectSettings screen
- UploadQuote screen
- ProjectCreateModal
- OnboardingProcessing screen
- All Firebase/backend logic
- Navigation implementation details

---

## 3. Screen Inventory

### 3.1 Auth Group

#### Auth/Login
- **Background:** Gray-50 (`#fafafa`)
- **Header area:** Logo placeholder (80x40 violet-200 rounded rect with "Capo" text in violet-600)
- **Card** (white, border gray-200, radius 8px, shadow):
  - **CardHeader:** Title "Welcome Back" (h4, 20px/700), Description "Enter your credentials to access your dashboard" (14px/400, gray-500)
  - **CardContent:**
    - Email Input: placeholder "name@example.com"
    - Password Input: placeholder "Password", secure entry
    - Button/Default size=lg: "Sign In" (violet-600, white text, pill shape)
  - **CardFooter:** Link button "Don't have an account? Sign Up" (violet-600 text, underlined)

#### Auth/SignUp
- Same layout as Login with:
  - Title: "Create an Account"
  - Description: "Enter your details to get started"
  - Button text: "Sign Up"
  - Footer link: "Already have an account? Sign In"

#### Auth/Login-Loading
- Same as Login with:
  - Button shows ActivityIndicator spinner + disabled state (opacity 0.5)
  - All inputs disabled appearance

#### Auth/Login-Error
- Same as Login with:
  - Red error banner below card header: "Authentication Error: Invalid credentials"
  - Input borders change to red (`#ef4444`)

### 3.2 Onboarding Group

**Shared pattern:** Gray-50 background, Header component with title + Exit button, step indicator + progress bar, Card with form content.

#### Onboarding/Profile (Step 1/3)
- **Header:** "Setup Your Profile" (h2) + Ghost button "Exit" (top right)
- **Step indicator:** "STEP 1 OF 3" (14px, violet-600, bold) + Progress bar 33% (6px height, gray-200 track, violet-600 fill, pill radius)
- **Card:**
  - Title: "Tell us about yourself"
  - Description: "We need a few details to customize your experience."
  - Input: "First Name" (label + placeholder "e.g. John")
  - Input: "Last Name" (label + placeholder "e.g. Doe")
  - Label: "What is your role?"
  - 5 role selector buttons (flex-wrap row, 8px gap):
    - "General Contractor" (selected=default variant, violet bg)
    - "Project Manager", "Architect / Engineer", "Subcontractor", "Client / Owner" (outline variant)
  - Button/Default size=lg: "Continue"
  - Button/Ghost size=sm: "Skip for now"

#### Onboarding/ProjectSetup (Step 2/3)
- **Step indicator:** "STEP 2 OF 3" + Progress bar 66%
- **Card:**
  - Title: "First Project Setup"
  - Description: "Let's get your project ready."
  - Input: "Project Name" (label + placeholder "e.g. Downtown renovation")
  - Label: "Upload Quote"
  - Muted text: "Take a photo of your estimation/quote. Our AI will analyze it to create tasks."
  - Two outline buttons side-by-side: "Gallery" (image icon) + "Camera" (camera icon)
  - Button/Default size=lg: "Next Step"

#### Onboarding/Timeline (Step 3/3)
- **Step indicator:** "STEP 3 OF 3" + Progress bar 100%
- **Card:**
  - Title: "Project Timeline"
  - Description: "When do you plan to complete [Project Name]?"
  - Label: "Start Date" + Date picker (compact, left-aligned)
  - Muted text: "*Currently set to start today."
  - Label: "Estimated Duration (Weeks)"
  - 3 duration buttons in row: "2 Weeks" | "1 Month" (selected=violet bg+border) | "3 Months"
  - Result preview box (gray-100 bg, centered): "CALCULATED DEADLINE" label + "2026-03-13" value (18px bold)
  - Button/Default size=lg: "Create Project & Analyze Quote"

### 3.3 Dashboard Group

#### Dashboard/Default
- **SafeArea:** White background (status bar area)
- **Header:** "My Projects" (h2) + Ghost button "Log Out" (red text, top right)
- **Content area:** Gray-50 background, 24px padding
- **3 Project cards** (stacked, 16px gap):
  - Each card:
    - Left: Icon placeholder (40x40 circle, gray-100 bg, violet icon)
    - Title: Project name (h4)
    - Right: Status badge ("Active" in emerald-600)
    - Body: "Tap to view details" (muted text)
- **FAB button:** "+ New Project" (violet-600 bg, white text, pill shape, bottom-right, shadow)

#### Dashboard/Empty
- Same header as Default
- **Empty state** (centered in content area):
  - Large icon placeholder (80x80 circle)
  - Title: "No projects yet"
  - Description: "Create your first project to get started"
  - Button/Default: "Create Project"

---

## 4. Design Tokens

### 4.1 Colors

| Token | Hex | Usage |
|-------|-----|-------|
| **Brand** | | |
| primary.DEFAULT | `#7c3aed` | Violet-600 — buttons, links, accents |
| primary.hover | `#6d28d9` | Violet-700 — pressed states |
| primary.light | `#ddd6fe` | Violet-200 — logo bg, selected bg |
| primary.foreground | `#FFFFFF` | Text on primary |
| **Neutral** | | |
| white | `#FFFFFF` | Card bg, header bg |
| gray.50 | `#fafafa` | Screen backgrounds |
| gray.100 | `#f4f4f5` | Icon circle bg, result preview bg |
| gray.200 | `#e4e4e7` | Borders, input borders, progress track |
| gray.300 | `#d4d4d8` | Outline button border |
| gray.400 | `#a1a1aa` | Icons |
| gray.500 | `#71717a` | Muted text, descriptions |
| gray.700 | `#3f3f46` | Labels |
| gray.800 | `#27272a` | Foreground text (also `black`) |
| **Status** | | |
| emerald.600 | `#059669` | Success, active status |
| destructive.DEFAULT | `#ef4444` | Red-500 — errors, logout |
| amber.400 | `#fbbf24` | Warnings |
| blue.400 | `#60a5fa` | Info |
| sky.400 | `#38bdf8` | New indicators |

### 4.2 Typography

| Style | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| h1 | 36px | 40px | 800 (extrabold) | Page titles |
| h2 | 30px | 36px | 700 (bold) | Section headers, screen titles |
| h3 | 24px | 32px | 700 (bold) | Logo text, card titles (large) |
| h4 | 20px | 28px | 700 (bold) | Card titles |
| p | 16px | 24px | 400 (regular) | Body text |
| lead | 18px | 28px | 400 (regular) | Intro text (muted color) |
| large | 18px | 28px | 500 (medium) | Emphasized body |
| small | 14px | 20px | 500 (medium) | Labels, step indicators |
| muted | 14px | 20px | 400 (regular) | Descriptions, help text (gray-500) |

Font: System (Inter planned)

### 4.3 Spacing (8px grid)

| Token | Value | Common Usage |
|-------|-------|-------------|
| 1 | 4px | Tight gaps (error text margin) |
| 2 | 8px | Input margins, button gaps, progress bar margin |
| 3 | 12px | Input padding horizontal, card header bottom |
| 4 | 16px | Card gaps, section margins, input bottom margin |
| 5 | 20px | — |
| 6 | 24px | Screen padding, card internal padding |
| 8 | 32px | Section spacing, logo margin bottom, FAB position |
| 10 | 40px | — |
| 12 | 48px | Large section spacing, FAB bottom (Android) |

### 4.4 Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| sm | 2px | — |
| DEFAULT | 4px | — |
| md | 6px | Input fields, duration buttons, date input |
| lg | 8px | Cards |
| xl | 12px | Logo placeholder |
| xxl | 16px | — |
| full | 9999px | Buttons (pill shape), FAB, icon circles |

---

## 5. Component Library

### 5.1 Button
- **Variants:** Default (violet bg), Outline (transparent + border), Ghost (transparent), Destructive (red bg), Link (underline), Secondary (gray bg)
- **Sizes:** sm (32px height, 12px hPad), default (40px height, 16px hPad), lg (48px height, 32px hPad), icon (40x40)
- **Shape:** Pill (radius full/9999px)
- **States:** Default, Loading (spinner), Disabled (50% opacity)

### 5.2 Input
- **Height:** 40px
- **Border:** 1px gray-200, radius md (6px)
- **Padding:** 12px horizontal
- **Font:** 14px regular
- **States:** Default, Focused (border violet-600), Error (border red-500 + error text below)
- **Optional label:** 14px medium, 8px margin bottom

### 5.3 Card
- **Background:** White
- **Border:** 1px gray-200
- **Radius:** lg (8px)
- **Shadow:** 0 1px 2px rgba(0,0,0,0.05)
- **Sub-components:**
  - CardHeader: 24px padding, 12px padding-bottom
  - CardTitle: h4 style (20px/700)
  - CardDescription: muted style (14px/400, gray-500)
  - CardContent: 24px padding, 0 padding-top
  - CardFooter: 24px padding, 0 padding-top, row layout

### 5.4 ProgressBar
- **Track:** 6px height, gray-200, pill radius (3px)
- **Fill:** violet-600, pill radius, width = percentage
- **Usage:** Onboarding steps (33%, 66%, 100%)

### 5.5 Header
- **Background:** White
- **Padding:** 24px horizontal, 24px top (iOS), 16px bottom
- **Border bottom:** 1px gray-200
- **Layout:** Row — left (back button + title) | right (action button)
- **Title:** h2 style (30px/700)
- **Optional subtitle:** muted style

### 5.6 Note Components
| Variant | Icon | Title Color | Usage |
|---------|------|-------------|-------|
| Note/Business | --- | Default | Business logic, requirements |
| Note/Design | --- | Default | Design decisions, rationale |
| Note/Dev | --- | Default | Technical specs, API details |
| Note/Question | --- | Default | Open questions, pending decisions |

Structure: Auto-layout vertical, title (bold) + body text, white bg, 1px border, 16px padding

### 5.7 IconPlaceholder
- **Size:** 40x40 (default), 80x80 (large)
- **Shape:** Circle (radius full)
- **Background:** gray-100 (project cards) or violet-200 (logo)
- **Icon:** Feather icon in violet-600 or centered text

---

## 6. User Flows

### Auth Flow
```
Auth/Login ──[Tap Sign In]──> Auth/Login-Loading
                                    │
                              ┌─────┴─────┐
                              ▼           ▼
                     Dashboard/Default  Auth/Login-Error
                     (existing user)    (back to login)

Auth/Login ──[Tap Sign Up link]──> Auth/SignUp
Auth/Login ──[New user, first login]──> Onboarding/Profile
```

### Onboarding Flow
```
Onboarding/Profile ──[Continue]──> Onboarding/ProjectSetup
                                          │
                                    [Next Step]
                                          ▼
                                   Onboarding/Timeline
                                          │
                                   [Create Project]
                                          ▼
                                   Dashboard/Default
```

### Dashboard Flow
```
Dashboard/Default ──[Tap + New Project]──> (out of scope)
Dashboard/Default ──[Tap project card]──> (out of scope)
Dashboard/Default ──[Tap Log Out]──> Auth/Login
```

---

## 7. Figma File Structure

### Page: "Design System"
- Color swatches (visual reference)
- Typography scale (visual reference)
- Spacing reference (8px grid visual)
- Component library (all components as Figma components)

### Page: "Screens"
- **Row 1 (y=0):** Auth group — Login, SignUp, Login-Loading, Login-Error (160px horizontal gaps)
- **Row 2 (y=1200):** Onboarding group — Profile, ProjectSetup, Timeline
- **Row 3 (y=2400):** Dashboard group — Default, Empty

Frame size: 390x844 (iPhone 14)

---

## 8. Acceptance Criteria

1. All 9 screens built as 390x844 frames with correct naming
2. All components created and used as instances (not raw shapes)
3. Colors, typography, and spacing match tokens exactly
4. Flow arrows connect all screens per flow map
5. Every screen has at least one annotation note
6. Design System page has complete token reference + all components
7. No "Frame 123" or unnamed layers
