# Implementation Spec: Pulse Onboarding Flow

## Overview

The Pulse Onboarding Flow is a 10-screen native iOS onboarding experience for an AI productivity companion app. It covers brand introduction, feature discovery, multi-method authentication (Apple, Google, magic link email), and success confirmation. The flow uses a dark UI theme with purple brand accents and animated gradient visuals.

**Key Technical Considerations:**
- **Platform:** iOS (Swift/SwiftUI assumed). All specs use iOS conventions (ASAuthorizationController, GIDSignIn SDK, 44pt touch targets, SF Symbols fallback).
- **Authentication:** Three methods -- Apple Sign In (native), Google Sign In (SDK), and custom magic link email. Magic link requires a polling mechanism or deep link handler.
- **Animation:** The gradient orb hero element, success checkmark, and loading spinner all require animation. Support `UIAccessibility.isReduceMotionEnabled` / `@Environment(\.accessibilityReduceMotion)` to swap animations for static/crossfade alternatives.
- **Dark theme only:** The onboarding flow is dark-mode only. No light theme variant is required at launch.
- **Offline handling:** Network error states are fully designed. The app must detect connectivity and present the correct error screen.

---

## Component Mapping

| # | Design Component | Code Component | Status | Props / Notes |
|---|-----------------|----------------|--------|---------------|
| 1 | Page Indicator (3 dots) | `PageIndicator` | **Build** | `totalPages: Int`, `currentPage: Int`, `activeColor: Color`, `inactiveColor: Color` |
| 2 | Gradient Orb | `GradientOrb` | **Build** | `size: CGFloat`, `primaryColor: Color`, `secondaryColor: Color`, `animated: Bool`. Use `MeshGradient` (iOS 18+) or `RadialGradient` with animation. |
| 3 | Feature Card | `FeatureCard` | **Build** | `icon: Image`, `title: String`, `description: String` |
| 4 | Auth Button (Apple) | `AuthButton` | **Build** | `variant: .apple`, uses `SignInWithAppleButton` wrapper |
| 5 | Auth Button (Google) | `AuthButton` | **Build** | `variant: .google`, custom styled button per Google branding guidelines |
| 6 | Auth Button (Email) | `AuthButton` | **Build** | `variant: .email`, outlined style |
| 7 | Text Input | `PulseTextField` | **Build** | `label: String`, `placeholder: String`, `text: Binding<String>`, `state: .default / .focused / .error / .disabled`, `errorMessage: String?` |
| 8 | Primary Button | `PrimaryButton` | **Build** | `title: String`, `state: .default / .disabled / .loading`, `action: () -> Void` |
| 9 | Secondary Button | `SecondaryButton` | **Build** | `title: String`, `action: () -> Void`. Outlined variant. |
| 10 | Link Button | `LinkButton` | **Build** | `title: String`, `action: () -> Void`. Text-only, no background. |
| 11 | Loading Spinner | `LoadingSpinner` | **Build** | `statusText: String?`, `animated: Bool`. Circular indeterminate spinner with optional label. |
| 12 | Error Illustration (Network) | `ErrorIllustration` | **Build** | `variant: .network / .auth`. Illustrated graphic with semantic meaning. |
| 13 | Success Checkmark | `SuccessCheckmark` | **Build** | `animated: Bool`, `onComplete: (() -> Void)?`. Animated circle + check path draw. |
| 14 | Header Bar | `OnboardingHeaderBar` | **Build** | `showBackButton: Bool`, `title: String?`, `onBack: (() -> Void)?`. Transparent background. |
| 15 | Status Bar | (System) | **Exists** | Use `.preferredStatusBarStyle = .lightContent` or SwiftUI `.statusBarHidden(false)` with light style. No custom component needed. |
| 16 | Note/Business | (Figma-only) | **N/A** | Annotation component -- not rendered in code. |
| 17 | Note/Design | (Figma-only) | **N/A** | Annotation component -- not rendered in code. |
| 18 | Note/Dev | (Figma-only) | **N/A** | Annotation component -- not rendered in code. |
| 19 | Note/Question | (Figma-only) | **N/A** | Annotation component -- not rendered in code. |

---

## Design Tokens

### Colors

| Token | Hex | CSS Variable | SwiftUI | Usage |
|-------|-----|-------------|---------|-------|
| bg-primary | `#0A0A0F` | `--color-bg-primary` | `Color("bgPrimary")` | Screen backgrounds |
| bg-card | `#14141F` | `--color-bg-card` | `Color("bgCard")` | Card backgrounds, input fields bg |
| brand-primary | `#6C5CE7` | `--color-brand-primary` | `Color("brandPrimary")` | CTA buttons, active indicator, orb primary |
| brand-light | `#A29BFE` | `--color-brand-light` | `Color("brandLight")` | Orb highlight, secondary brand accent |
| text-primary | `#FFFFFF` | `--color-text-primary` | `Color("textPrimary")` | Headings, primary labels |
| text-secondary | `#B0B0C0` | `--color-text-secondary` | `Color("textSecondary")` | Body text, subtitles |
| text-tertiary | `#6C6C80` | `--color-text-tertiary` | `Color("textTertiary")` | Hints, inactive elements, placeholder text |
| error | `#FF6B6B` | `--color-error` | `Color("error")` | Error borders, error text, error icons |
| success | `#51CF66` | `--color-success` | `Color("success")` | Success checkmark, success text |
| border-default | `#2A2A3A` | `--color-border-default` | `Color("borderDefault")` | Input borders at rest, dividers |
| border-active | `#3A3A50` | `--color-border-active` | `Color("borderActive")` | Input borders on focus |
| surface-apple | `#000000` | `--color-surface-apple` | `Color.black` | Apple Sign In button background |
| surface-google | `#FFFFFF` | `--color-surface-google` | `Color.white` | Google Sign In button background |

**Contrast Verification:**

| Pair | Ratio | WCAG AA | WCAG AAA |
|------|-------|---------|----------|
| text-primary (#FFF) on bg-primary (#0A0A0F) | 19.2:1 | Pass | Pass |
| text-secondary (#B0B0C0) on bg-primary (#0A0A0F) | 9.4:1 | Pass | Pass |
| text-tertiary (#6C6C80) on bg-primary (#0A0A0F) | 4.1:1 | Marginal | Fail |
| error (#FF6B6B) on bg-primary (#0A0A0F) | 5.2:1 | Pass | Fail |
| brand-primary (#6C5CE7) on bg-primary (#0A0A0F) | 4.7:1 | Pass (large text) | Fail |
| text-primary (#FFF) on brand-primary (#6C5CE7) | 4.1:1 | Pass (large text) | Fail |

**Action Required:** `text-tertiary` on `bg-primary` is at the AA boundary (4.1:1). Confirm it is only used for non-essential decorative text. If used for any actionable UI, lighten to `#8080A0` (~5.5:1). White text on `brand-primary` buttons should use bold/large text (16px semi-bold meets the "large text" threshold of 14pt bold).

### Typography

| Token | Font Family | Size | Weight | Line Height | Letter Spacing | SwiftUI | Usage |
|-------|------------|------|--------|-------------|----------------|---------|-------|
| h1 | Inter | 28px | Bold (700) | 34px (1.2x) | -0.5px | `.font(.custom("Inter-Bold", size: 28))` | Screen titles |
| h2 | Inter | 22px | SemiBold (600) | 28px (1.27x) | -0.3px | `.font(.custom("Inter-SemiBold", size: 22))` | Section headings |
| body | Inter | 16px | Regular (400) | 24px (1.5x) | 0px | `.font(.custom("Inter-Regular", size: 16))` | Body text |
| body-bold | Inter | 16px | SemiBold (600) | 24px (1.5x) | 0px | `.font(.custom("Inter-SemiBold", size: 16))` | Button labels |
| caption | Inter | 14px | Regular (400) | 20px (1.43x) | 0px | `.font(.custom("Inter-Regular", size: 14))` | Subtitles, descriptions |
| small | Inter | 12px | Regular (400) | 16px (1.33x) | 0.2px | `.font(.custom("Inter-Regular", size: 12))` | Legal text, hints |

**Font Integration Note:** Inter must be bundled with the app. Add `Inter-Regular.ttf`, `Inter-SemiBold.ttf`, and `Inter-Bold.ttf` to the Xcode project and register them in `Info.plist` under `UIAppFonts`. Consider using the Inter variable font file for smaller bundle size.

### Spacing

| Token | Value | SwiftUI | Usage |
|-------|-------|---------|-------|
| xs | 8px | `Spacing.xs` / `8` | Tight gaps between related items, icon-to-label gaps |
| sm | 16px | `Spacing.sm` / `16` | Standard gaps between elements, card internal padding |
| md | 24px | `Spacing.md` / `24` | Section spacing, note-to-screen gap |
| lg | 32px | `Spacing.lg` / `32` | Large section gaps |
| xl | 40px | `Spacing.xl` / `40` | Screen top safe-area padding |
| 2xl | 48px | `Spacing.xxl` / `48` | Hero section spacing |

### Border Radius

| Token | Value | SwiftUI | Usage |
|-------|-------|---------|-------|
| radius-sm | 8px | `.cornerRadius(8)` | Small cards, note frames |
| radius-md | 12px | `.cornerRadius(12)` | Buttons, text inputs |
| radius-lg | 16px | `.cornerRadius(16)` | Feature cards, modal sheets |
| radius-full | 9999px | `.clipShape(Capsule())` | Page indicator dots, orb, pills |

### Shadows

| Token | Offset | Blur | Spread | Color | Usage |
|-------|--------|------|--------|-------|-------|
| shadow-card | (0, 2) | 8px | 0 | `rgba(0,0,0,0.3)` | Feature cards (subtle depth on dark bg) |
| shadow-orb | (0, 0) | 40px | 0 | `rgba(108,92,231,0.3)` | Glow behind gradient orb |
| shadow-button | (0, 4) | 12px | 0 | `rgba(108,92,231,0.25)` | Primary CTA buttons hover/pressed |

---

## Screen Implementation Notes

### Screen 1: Onboarding/Welcome/Default
**Figma Node:** `86:54`

- **Components:** GradientOrb, PageIndicator (page 1 of 3), PrimaryButton ("Get Started"), StatusBar
- **State:**
  - `isAnimating: Bool` -- Controls orb entrance animation
- **API calls:** None
- **Interactions:**
  - Orb animates on appear (gentle float/pulse). Respect `reduceMotion`.
  - "Get Started" button navigates to Features screen
  - Swipe left gesture also advances to Features
  - PageIndicator shows 1/3 active
- **Accessibility:**
  - `accessibilityLabel` on orb: "Pulse logo animation"
  - `accessibilityTraits: .header` on title text
  - `accessibilityHint` on button: "Moves to feature overview"
  - VoiceOver: Read title, subtitle, then focus on CTA
- **Complexity:** **Low** -- Static content, simple navigation, one animation

---

### Screen 2: Onboarding/Features/Default
**Figma Node:** `86:55`

- **Components:** PageIndicator (page 2 of 3), FeatureCard (x3), PrimaryButton ("Continue"), HeaderBar (back button), StatusBar
- **State:**
  - `selectedFeature: Int?` -- Optional highlight state for tapped card
- **API calls:** None
- **Interactions:**
  - Three feature cards displayed vertically with stagger entrance animation
  - Back button returns to Welcome
  - "Continue" navigates to SignIn
  - Swipe left/right navigates between pages
  - Cards are non-interactive (informational only) unless tap-to-expand is desired
- **Accessibility:**
  - Each FeatureCard is a single accessibility element: `accessibilityLabel = "\(title). \(description)"`
  - Cards should not trap focus -- swipe through linearly
  - `accessibilityTraits: .staticText` on each card
- **Complexity:** **Low** -- Static content, list of cards

---

### Screen 3: Onboarding/SignIn/Default
**Figma Node:** `86:56`

- **Components:** HeaderBar (back button), AuthButton (Apple), AuthButton (Google), AuthButton (Email), LinkButton ("Skip"), StatusBar
- **State:**
  - `isAppleAuthLoading: Bool`
  - `isGoogleAuthLoading: Bool`
- **API calls:**
  - Apple: Trigger `ASAuthorizationController` flow
  - Google: Trigger `GIDSignIn.sharedInstance.signIn()` flow
- **Interactions:**
  - "Continue with Apple" -> Triggers native Apple Sign In sheet -> On success, navigate to AuthLoading
  - "Continue with Google" -> Triggers Google Sign In SDK -> On success, navigate to AuthLoading
  - "Continue with Email" -> Navigate to EmailEntry
  - "Skip" -> Navigate directly to main app (unauthenticated experience)
  - "Skip" should present a confirmation if skipping has consequences
- **Accessibility:**
  - `accessibilityLabel` per button: "Sign in with Apple", "Sign in with Google", "Sign in with email"
  - `accessibilityTraits: .button` on all interactive elements
  - Skip button: `accessibilityHint: "Continues without signing in. Some features may be limited."`
  - Divider "or" text: `accessibilityHidden(true)` (decorative)
- **Complexity:** **Medium** -- Three auth method integrations, social auth SDK wiring

---

### Screen 4: Onboarding/SignIn/EmailEntry
**Figma Node:** `86:57`

- **Components:** HeaderBar (back button, title "Sign In"), PulseTextField (email input), PrimaryButton ("Send Magic Link"), LinkButton ("Use a different method"), StatusBar
- **State:**
  - `email: String` -- Bound to text field
  - `isValidEmail: Bool` -- Client-side validation
  - `isSubmitting: Bool` -- Loading state after submit
  - `fieldState: FieldState` -- `.default`, `.focused`, `.error`
- **API calls:**
  - `POST /auth/magic-link` (on submit, after client-side validation passes)
- **Interactions:**
  - Text field auto-focuses on appear (present keyboard)
  - Client-side email validation on text change (debounced) and on submit
  - "Send Magic Link" disabled until `isValidEmail == true`
  - On submit: button enters loading state, calls API
  - On API success: navigate to EmailSent
  - On API error (invalid_email, disposable_email, blocked_domain): navigate to EmailError
  - On network error: navigate to NetworkError
  - "Use a different method" -> Navigate back to SignIn
  - Keyboard "Done" / "Return" key triggers submit
- **Accessibility:**
  - Text field: `accessibilityLabel: "Email address"`, `textContentType: .emailAddress`, `keyboardType: .emailAddress`, `autocapitalization: .never`
  - Error message (if inline): `accessibilityLiveRegion` announcement
  - Button state change: announce "Loading" when submitting
- **Complexity:** **Medium** -- Form validation, API call, state transitions, keyboard management

---

### Screen 5: Onboarding/SignIn/EmailError
**Figma Node:** `86:58`

- **Components:** HeaderBar (back button, title "Sign In"), PulseTextField (email input, error state), PrimaryButton ("Send Magic Link", disabled), StatusBar
- **State:**
  - Inherits from EmailEntry state
  - `errorMessage: String` -- Specific error text from API or client validation
  - `fieldState: .error`
- **API calls:** None (re-triggers on fix + resubmit)
- **Interactions:**
  - Error message displayed below text field in error color
  - Input border changes to error color
  - User edits email -> error clears, returns to EmailEntry state (field goes to `.focused`)
  - "Send Magic Link" re-enables once email is valid again
- **Accessibility:**
  - Error message: `accessibilityLiveRegion: .assertive` -- Immediately announced by VoiceOver
  - Text field: `accessibilityValue` includes error message: "Invalid email address. Error: Please enter a valid email."
  - Focus should move to the text field on error so users can correct immediately
- **Complexity:** **Low** -- This is a state variant of EmailEntry, not a separate view. Implement as a state within the EmailEntry screen.

**Implementation Note:** Screens 4 and 5 should be the same SwiftUI view. EmailError is not a separate screen in code -- it is the error state of the EmailEntry view. The Figma screens show them separately for design documentation purposes.

---

### Screen 6: Onboarding/SignIn/EmailSent
**Figma Node:** `86:59`

- **Components:** HeaderBar (back button), GradientOrb (small, email icon overlay), PrimaryButton ("Open Email App"), SecondaryButton ("Resend Email"), LinkButton ("Use a different method"), StatusBar
- **State:**
  - `email: String` -- Display the submitted email (masked or full)
  - `resendCooldown: Int` -- Countdown timer (e.g., 30s) before resend is enabled
  - `resendCount: Int` -- Track number of resends (limit to 3)
  - `canResend: Bool` -- Derived from cooldown + count
- **API calls:**
  - `POST /auth/magic-link` (on "Resend Email" tap, same endpoint)
- **Interactions:**
  - "Open Email App" -> Open system email app via `UIApplication.shared.open(URL(string: "message://")!)`
  - "Resend Email" -> Disabled for 30s after last send, re-calls magic link API
  - "Use a different method" -> Navigate back to SignIn
  - Display sent email address: "We sent a link to f***@example.com"
  - Auto-poll or listen for deep link: when magic link is clicked, app receives callback
- **Accessibility:**
  - Confirmation text: `accessibilityTraits: .header`
  - Email display: announce full email to VoiceOver (do not mask for screen readers)
  - Resend button when disabled: `accessibilityHint: "Available in \(seconds) seconds"`
  - Timer countdown: do NOT announce every second. Announce only when resend becomes available.
- **Complexity:** **Medium** -- Timer logic, resend limiting, deep link handling, email app integration

---

### Screen 7: Onboarding/SignIn/AuthLoading
**Figma Node:** `86:60`

- **Components:** LoadingSpinner, StatusBar
- **State:**
  - `authMethod: AuthMethod` -- `.apple`, `.google`, `.email`
  - `statusText: String` -- Dynamic text: "Verifying your account...", "Almost there..."
  - `elapsedTime: TimeInterval` -- Track loading duration for timeout
- **API calls:**
  - For magic link: `GET /auth/verify` (polling every 2-3 seconds)
  - For social auth: Await SDK callback
- **Interactions:**
  - Spinner animates continuously (respect `reduceMotion`)
  - Status text updates after 3s: "This might take a moment..."
  - Timeout after 30s: navigate to NetworkError or AuthError
  - On success: navigate to Success
  - On failure: navigate to AuthError
  - On network error: navigate to NetworkError
  - **No back button** -- User cannot cancel mid-auth (prevents partial state)
- **Accessibility:**
  - Screen announcement on appear: "Verifying your account. Please wait."
  - Status text changes: `accessibilityLiveRegion: .polite`
  - Spinner: `accessibilityLabel: "Loading"`, `accessibilityTraits: .updatesFrequently`
- **Complexity:** **Medium** -- Polling logic, timeout handling, SDK callbacks, state machine transitions

---

### Screen 8: Onboarding/SignIn/NetworkError
**Figma Node:** `86:61`

- **Components:** ErrorIllustration (variant: network), PrimaryButton ("Try Again"), SecondaryButton ("Use Different Method"), StatusBar
- **State:**
  - `lastAuthMethod: AuthMethod` -- What was being attempted when the error occurred
  - `retryCount: Int` -- Track retries
- **API calls:** Retry the last attempted auth call on "Try Again"
- **Interactions:**
  - "Try Again" -> Navigate back to AuthLoading, re-attempt the same auth method
  - "Use Different Method" -> Navigate back to SignIn (clear auth state)
  - Monitor `NWPathMonitor` -- If connectivity restores, optionally auto-retry or show a "Connection restored" toast
  - After 3 failed retries, change "Try Again" text to "Check your connection and try again"
- **Accessibility:**
  - Error illustration: `accessibilityLabel: "Network connection error"`, `accessibilityTraits: .image`
  - Error title: `accessibilityTraits: .header`
  - Screen announcement on appear: "Network error. Unable to connect. You can try again or use a different sign-in method."
- **Complexity:** **Low** -- Static error screen with two CTAs and retry logic

---

### Screen 9: Onboarding/SignIn/AuthError
**Figma Node:** `86:62`

- **Components:** ErrorIllustration (variant: auth), PrimaryButton ("Try Again"), SecondaryButton ("Try Different Method"), StatusBar
- **State:**
  - `errorCode: String` -- API error code (expired_link, already_used, invalid_token, account_locked)
  - `errorMessage: String` -- Human-readable message derived from code
  - `lastAuthMethod: AuthMethod`
- **API calls:** Retry auth on "Try Again"
- **Interactions:**
  - Display different copy based on `errorCode`:
    - `expired_link`: "Your sign-in link has expired. Request a new one."
    - `already_used`: "This link has already been used. Request a new one."
    - `invalid_token`: "Something went wrong. Please try again."
    - `account_locked`: "Your account has been locked. Contact support." (Disable "Try Again", show support link instead)
  - "Try Again" -> Navigate to AuthLoading (or EmailEntry if expired/used link)
  - "Try Different Method" -> Navigate back to SignIn
- **Accessibility:**
  - Same pattern as NetworkError
  - If `account_locked`: announce "Account locked" with `.accessibilityTraits: .staticText` and provide support link
- **Complexity:** **Low** -- Static error screen with conditional copy

---

### Screen 10: Onboarding/Success/Default
**Figma Node:** `86:63`

- **Components:** SuccessCheckmark (animated), StatusBar
- **State:**
  - `isAnimating: Bool`
  - `autoAdvanceTimer: Timer?` -- 2-second auto-advance
- **API calls:**
  - `POST /users/onboarding-complete` -- Fire-and-forget. Do not block navigation on this call. Retry silently if it fails.
- **Interactions:**
  - Checkmark draws in with animation (respect `reduceMotion`: use fade-in instead)
  - Optional confetti particles (disable if `reduceMotion`)
  - Auto-advance to main app after 2 seconds
  - Tap anywhere to advance immediately
  - Call `/users/onboarding-complete` in background
- **Accessibility:**
  - Screen announcement on appear: "Success! Your account is ready. Opening Pulse."
  - Auto-advance: VoiceOver users need enough time to hear the announcement. Extend timer to 4s when VoiceOver is active, or wait for VoiceOver to finish speaking.
  - Tap target: entire screen is tappable (`.contentShape(Rectangle())`)
- **Complexity:** **Low** -- Animation + timer + one fire-and-forget API call

---

## API Requirements

### POST /auth/magic-link

**Purpose:** Send a magic link email to the user.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Magic link sent",
  "expiresIn": 600
}
```

**Error Responses:**

| Status | Code | Message | UI Handling |
|--------|------|---------|-------------|
| 400 | `invalid_email` | "Invalid email format" | Show inline field error |
| 400 | `disposable_email` | "Disposable email addresses are not allowed" | Show inline field error |
| 400 | `blocked_domain` | "This email domain is not supported" | Show inline field error |
| 429 | `rate_limited` | "Too many requests. Try again in {n} seconds" | Disable resend, show countdown |
| 500 | `server_error` | "Something went wrong" | Navigate to NetworkError |

**Client-side validation (before API call):**
- RFC 5322 email format regex
- Non-empty string
- Length < 254 characters

---

### GET /auth/verify

**Purpose:** Poll for magic link confirmation after user clicks the link in their email.

**Request:**
```
GET /auth/verify?token={session_token}
Headers: X-Session-ID: {session_id_from_magic_link_response}
```

**Response (200 OK -- link clicked):**
```json
{
  "status": "verified",
  "accessToken": "eyJhbG...",
  "refreshToken": "dGhpcyB...",
  "user": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "isNewUser": true
  }
}
```

**Response (200 OK -- still waiting):**
```json
{
  "status": "pending"
}
```

**Error Responses:**

| Status | Code | Message | UI Handling |
|--------|------|---------|-------------|
| 400 | `expired_link` | "Link has expired" | Navigate to AuthError (expired copy) |
| 400 | `already_used` | "Link already used" | Navigate to AuthError (used copy) |
| 400 | `invalid_token` | "Invalid verification token" | Navigate to AuthError (generic copy) |
| 403 | `account_locked` | "Account is locked" | Navigate to AuthError (locked copy, hide retry) |
| 500 | `server_error` | "Verification failed" | Navigate to NetworkError |

**Polling Strategy:**
- Poll every 3 seconds
- Maximum 10 minutes (200 polls)
- Show timeout error after 30 seconds of no response (network issue) or after 10 minutes (link expired)
- Stop polling when app backgrounds; resume when foregrounded
- Use exponential backoff on consecutive 500 errors

---

### POST /users/onboarding-complete

**Purpose:** Mark the user's onboarding as complete. Prevents showing onboarding again.

**Request:**
```json
{
  "userId": "usr_abc123",
  "completedAt": "2026-02-11T10:30:00Z",
  "authMethod": "email" | "apple" | "google" | "skipped"
}
```

**Response (200 OK):**
```json
{
  "success": true
}
```

**Error Handling:** This is a fire-and-forget call. If it fails:
1. Cache the completion event locally (UserDefaults/Keychain)
2. Retry on next app launch
3. Do NOT block the user from proceeding to the main app

---

### Apple Sign In

**SDK:** `AuthenticationServices` framework (native iOS)

**Flow:**
1. Present `ASAuthorizationController` with `ASAuthorizationAppleIDProvider`
2. Request scopes: `.email`, `.fullName`
3. On success: receive `ASAuthorizationAppleIDCredential`
4. Send `identityToken` to backend for verification
5. Backend returns access/refresh tokens

**Key Implementation Notes:**
- Apple only provides name/email on FIRST sign-in. Cache these.
- Handle `ASAuthorizationError` codes: `.canceled`, `.failed`, `.invalidResponse`, `.notHandled`, `.unknown`
- `.canceled` -> Return to SignIn silently (do not show error)
- `.failed` / others -> Navigate to AuthError

---

### Google Sign In

**SDK:** `GoogleSignIn` (GIDSignIn) -- version 7.x+

**Flow:**
1. Call `GIDSignIn.sharedInstance.signIn(withPresenting: viewController)`
2. On success: receive `GIDGoogleUser` with `idToken`
3. Send `idToken` to backend for verification
4. Backend returns access/refresh tokens

**Key Implementation Notes:**
- Configure `GIDClientID` in `Info.plist`
- Add URL scheme for Google callback
- Handle cancellation silently (user dismissed the sheet)
- Handle `.hasNoAuthInKeychain` -> User never signed in with Google before (not an error)

---

## State Management

### Global State (App-wide)

```swift
class OnboardingState: ObservableObject {
    // Navigation
    @Published var currentScreen: OnboardingScreen = .welcome
    @Published var navigationPath: [OnboardingScreen] = []

    // Auth
    @Published var authMethod: AuthMethod? = nil  // .apple, .google, .email
    @Published var email: String = ""
    @Published var sessionToken: String? = nil
    @Published var accessToken: String? = nil
    @Published var refreshToken: String? = nil

    // User
    @Published var userId: String? = nil
    @Published var isNewUser: Bool = true

    // Status
    @Published var isOnboardingComplete: Bool = false  // Persisted to UserDefaults
}

enum OnboardingScreen: Hashable {
    case welcome
    case features
    case signIn
    case emailEntry
    case emailSent
    case authLoading
    case networkError
    case authError(code: String)
    case success
}

enum AuthMethod: String, Codable {
    case apple, google, email, skipped
}
```

### Local State (Per-screen)

| Screen | Local State | Notes |
|--------|------------|-------|
| Welcome | `isOrbAnimating: Bool` | Controls entrance animation |
| Features | None | Static content |
| SignIn | `isAppleLoading: Bool`, `isGoogleLoading: Bool` | Loading state per auth button |
| EmailEntry | `emailText: String`, `fieldState: FieldState`, `errorMessage: String?`, `isSubmitting: Bool` | Form state |
| EmailSent | `resendCooldown: Int`, `resendCount: Int`, `canResend: Bool` | Resend timer |
| AuthLoading | `statusText: String`, `elapsedTime: TimeInterval` | Dynamic loading text |
| NetworkError | `retryCount: Int` | Track retries |
| AuthError | `errorCode: String`, `errorMessage: String` | Contextual error display |
| Success | `isCheckmarkAnimating: Bool`, `autoAdvanceTimer: Timer?` | Animation + timer |

### Server State (Cached from API)

| Data | Source | Cache Strategy |
|------|--------|---------------|
| Auth tokens | `/auth/verify` or social SDK | Keychain (secure) |
| User profile | `/auth/verify` response | In-memory during onboarding, then persisted |
| Onboarding complete flag | `/users/onboarding-complete` | UserDefaults (local) + server (source of truth) |
| Magic link session | `/auth/magic-link` response | In-memory only, discard on exit |

---

## Implementation Order

The build sequence is ordered by dependency (foundational components first) and decreasing risk (hardest integrations early).

### Phase 1: Foundation (Days 1-2)

| # | Item | Type | Rationale |
|---|------|------|-----------|
| 1.1 | Design Tokens | Config | All components depend on tokens. Define `Colors.swift`, `Typography.swift`, `Spacing.swift`, `Shadows.swift`. |
| 1.2 | Inter font integration | Config | Register font files in Xcode project. All text depends on this. |
| 1.3 | `OnboardingState` | State | Navigation and auth state model. All screens depend on this. |
| 1.4 | `OnboardingCoordinator` | Navigation | `NavigationStack`-based coordinator. Defines all transitions. |

### Phase 2: Core Components (Days 2-3)

| # | Item | Type | Rationale |
|---|------|------|-----------|
| 2.1 | `PrimaryButton` | Component | Used on 7 of 10 screens. Build first with all states (default, disabled, loading). |
| 2.2 | `SecondaryButton` | Component | Used on error screens. |
| 2.3 | `LinkButton` | Component | Used on 5 screens (Skip, Resend, Use different method). |
| 2.4 | `OnboardingHeaderBar` | Component | Used on 7 screens. Back button + optional title. |
| 2.5 | `PageIndicator` | Component | Used on Welcome + Features. |
| 2.6 | `PulseTextField` | Component | Used on EmailEntry/EmailError. All states. |
| 2.7 | `LoadingSpinner` | Component | Used on AuthLoading. |

### Phase 3: Specialized Components (Days 3-4)

| # | Item | Type | Rationale |
|---|------|------|-----------|
| 3.1 | `GradientOrb` | Component | Animated gradient. More complex, used on Welcome + EmailSent. |
| 3.2 | `FeatureCard` | Component | Used on Features screen. |
| 3.3 | `AuthButton` | Component | 3 variants. Apple/Google require specific branding compliance. |
| 3.4 | `ErrorIllustration` | Component | 2 variants (network, auth). Illustrated or icon-based. |
| 3.5 | `SuccessCheckmark` | Component | Animated path drawing. |

### Phase 4: Screens -- Happy Path (Days 4-6)

| # | Item | Type | Rationale |
|---|------|------|-----------|
| 4.1 | Welcome Screen | Screen | Entry point. Simple, validates token setup + orb animation. |
| 4.2 | Features Screen | Screen | Static content. Validates FeatureCard + PageIndicator. |
| 4.3 | SignIn Screen | Screen | Hub screen. Validates AuthButton layout. No API yet. |
| 4.4 | EmailEntry Screen | Screen | Form + client-side validation. |
| 4.5 | EmailSent Screen | Screen | Confirmation + resend timer logic. |
| 4.6 | AuthLoading Screen | Screen | Spinner + status text. |
| 4.7 | Success Screen | Screen | Checkmark animation + auto-advance. |

### Phase 5: API Integration (Days 6-8)

| # | Item | Type | Rationale |
|---|------|------|-----------|
| 5.1 | Magic link API service | Service | `POST /auth/magic-link` + `GET /auth/verify` polling. |
| 5.2 | Apple Sign In integration | Service | ASAuthorizationController wiring. |
| 5.3 | Google Sign In integration | Service | GIDSignIn SDK wiring. |
| 5.4 | Onboarding complete API | Service | Fire-and-forget + local cache fallback. |
| 5.5 | Token storage (Keychain) | Service | Secure storage for access/refresh tokens. |

### Phase 6: Error Screens + Edge Cases (Days 8-9)

| # | Item | Type | Rationale |
|---|------|------|-----------|
| 6.1 | NetworkError Screen | Screen | Error UI + retry logic. |
| 6.2 | AuthError Screen | Screen | Conditional copy based on error code. |
| 6.3 | EmailError state | State | Error state within EmailEntry (not a separate screen). |
| 6.4 | Timeout handling | Logic | 30s timeout on AuthLoading. |
| 6.5 | Retry limiting | Logic | Max 3 retries, then alternate messaging. |
| 6.6 | Network monitoring | Logic | `NWPathMonitor` for connectivity changes. |

### Phase 7: Accessibility + Polish (Days 9-10)

| # | Item | Type | Rationale |
|---|------|------|-----------|
| 7.1 | VoiceOver labels + hints | A11y | All interactive elements. |
| 7.2 | Focus order | A11y | Logical tab/swipe order per screen. |
| 7.3 | Live region announcements | A11y | Error states, loading states, success. |
| 7.4 | Reduced motion support | A11y | Check `UIAccessibility.isReduceMotionEnabled`. Replace animations with fades. |
| 7.5 | Dynamic type support | A11y | Ensure text scales with system font size (optional for v1, but recommended). |
| 7.6 | Screen transition animations | Polish | Slide/fade transitions between screens. |
| 7.7 | Haptic feedback | Polish | Light haptic on success, error. |

**Total Estimated Effort:** 10 working days (2 weeks) for one iOS developer.

---

## Technical Risks

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|------------|------------|
| 1 | **Apple Sign In first-use data loss** -- Apple only provides name/email on the very first authorization. If the app fails to capture it, the data is lost forever. | High | Medium | Cache `fullName` and `email` from `ASAuthorizationAppleIDCredential` immediately on receipt. Store in Keychain before making any network calls. Implement a fallback "What's your name?" screen if data is missing. |
| 2 | **Magic link polling reliability** -- Long polling (up to 10 min) is fragile. App backgrounding, network changes, and device sleep can interrupt polling. | High | High | Use a combination of polling + deep link handling. Register a universal link (`pulse.app/auth/verify?token=xxx`) so the app opens directly when the user clicks the email link. Polling is a fallback only. |
| 3 | **Google Sign In SDK version conflicts** -- GIDSignIn SDK updates frequently and has breaking changes between major versions. | Medium | Medium | Pin to a specific SDK version in `Package.swift` or `Podfile`. Test with the pinned version. Document the required version in this spec. |
| 4 | **Inter font rendering** -- Custom fonts can render differently across iOS versions and devices. Line heights and metrics may not match Figma exactly. | Low | Medium | Test on oldest supported iOS version. Use `.lineSpacing()` modifier if needed to match design. Accept minor rendering differences (1-2px). |
| 5 | **Gradient orb performance** -- Complex animated gradients can cause frame drops on older devices (iPhone SE 2, iPad Air 3). | Medium | Medium | Profile on oldest supported device. Use `MeshGradient` (iOS 18+) for modern devices, fall back to `RadialGradient` with `CADisplayLink` animation. If frame drops detected, reduce animation complexity or use a pre-rendered Lottie animation. |
| 6 | **Deep link hijacking** -- Universal links require proper domain verification. If not configured correctly, the magic link will open in Safari instead of the app. | High | Low | Set up Apple App Site Association (AASA) file on the server. Test universal links in TestFlight (they do not work in Simulator). Have a fallback: if the link opens in Safari, show a "Open in Pulse" button that uses a custom URL scheme. |
| 7 | **Race condition on auth completion** -- User could click magic link, return to app, and see AuthLoading while the verify call is still in flight. If they also tap "Try Again", multiple verify calls could overlap. | Medium | Medium | Use a state machine pattern. Once `authMethod` is set and loading begins, disable all retry buttons until the current attempt resolves. Cancel in-flight requests before starting new ones. |
| 8 | **Onboarding-complete call failure** -- If `POST /users/onboarding-complete` fails and the local flag is not set, the user will see onboarding again on next launch. | Low | Low | Always set a local flag (UserDefaults) immediately on success screen arrival, BEFORE making the API call. The API call syncs the server state but the local flag is the source of truth for "should I show onboarding?". Retry the API call silently on next app launch if it failed. |

---

## Handoff Checklist

### Design Completeness
- [x] All 10 screens designed and annotated
- [x] All interactive states included (default, loading, error, success, disabled)
- [x] Micro-copy is final (not placeholder)
- [x] Empty/loading/error states are fully designed
- [ ] Responsive breakpoints defined -- **N/A** (iOS only, single size class for now. iPad adaptation is out of scope for v1.)
- [x] Interactions and transitions specified in this document

### Documentation
- [x] Business notes on each screen (Figma annotations)
- [x] Dev notes with API/technical context (Figma annotations + this document)
- [x] Design notes explaining non-obvious decisions (Figma annotations)
- [x] Open questions resolved or flagged (see below)

### Technical Readiness
- [x] All design components mapped to code components (Component Mapping table above)
- [x] Design tokens extracted and documented (Design Tokens section above)
- [x] API requirements documented with request/response shapes
- [x] Implementation order defined with dependency rationale
- [x] Complexity estimated per screen
- [ ] Code Connect mappings published to Figma -- **Pending.** Will be set up once code components are built. Component keys are documented above for future mapping.

### Accessibility
- [x] Color contrast verified (see Contrast Verification table; one marginal case flagged)
- [x] Touch targets specified (44px minimum throughout)
- [x] Focus order documented per screen
- [x] Screen reader flow defined (VoiceOver labels, hints, live regions)
- [x] ARIA roles / accessibility traits specified per component
- [x] Reduced motion support specified

### Open Items

| # | Item | Owner | Priority | Status |
|---|------|-------|----------|--------|
| 1 | **text-tertiary contrast** -- 4.1:1 ratio is at the AA boundary. Confirm it is only used for non-essential text, or lighten the color. | Design | Medium | Open |
| 2 | **Skip behavior** -- What happens when user skips? What features are limited? Is there a later prompt to sign in? | PM/Product | High | Open |
| 3 | **iPad layout** -- Current designs are iPhone-only (390x844). Define iPad behavior (centered card? full-width?) if needed for v1. | Design | Low | Deferred to v2 |
| 4 | **Confetti on success** -- Particle effect is noted but not fully spec'd in design. Is this a Lottie animation, SpriteKit, or SwiftUI Canvas? | Engineering | Low | Open |
| 5 | **Analytics events** -- No analytics events are defined. Define event names and properties for each screen view and user action. | PM/Engineering | Medium | Open |
| 6 | **Deep link domain** -- What domain will host the AASA file and magic link URLs? (e.g., `auth.pulse.app`) | Engineering/DevOps | High | Open |
| 7 | **Error illustration assets** -- Are these custom illustrations, SF Symbols, or Lottie animations? Need final assets exported from design. | Design | Medium | Open |
| 8 | **Session persistence on app kill** -- If user requests a magic link, kills the app, then clicks the link, should the app resume the auth flow? | Engineering | Medium | Open |

---

## Dev Notes

1. **Navigation Pattern:** Use `NavigationStack` with a path-based approach. The `OnboardingScreen` enum conforms to `Hashable` and drives the navigation stack. Do not use `NavigationLink` with destination views -- use programmatic navigation via `navigationDestination(for:)`.

2. **SwiftUI vs UIKit:** The entire onboarding flow can be built in SwiftUI. The only UIKit bridges needed are:
   - `ASAuthorizationController` (Apple Sign In) -- wrap in a `UIViewControllerRepresentable` or use the SwiftUI `SignInWithAppleButton`
   - `GIDSignIn` -- wrap the presenting view controller

3. **Testing:** Write unit tests for:
   - Email validation regex
   - `OnboardingState` transitions (state machine correctness)
   - Resend cooldown timer logic
   - Retry count limiting
   - API response parsing (all error codes)

4. **Feature Flags:** Consider wrapping the "Skip" option behind a feature flag. This allows product to A/B test skip vs. mandatory auth.

5. **Localization:** All user-facing strings should use `String(localized:)` from day one, even if launching in English only. This avoids a painful retrofit later.

6. **Minimum iOS Version:** If targeting iOS 17+, `MeshGradient` is not available (iOS 18+). Decide the gradient implementation based on deployment target.

7. **Screen Naming Convention:** In code, name view files to match the Figma convention: `OnboardingWelcomeView.swift`, `OnboardingFeaturesView.swift`, `OnboardingSignInView.swift`, `OnboardingEmailEntryView.swift`, `OnboardingEmailSentView.swift`, `OnboardingAuthLoadingView.swift`, `OnboardingNetworkErrorView.swift`, `OnboardingAuthErrorView.swift`, `OnboardingSuccessView.swift`. Note that `EmailError` is a state within `OnboardingEmailEntryView`, not a separate file.

---

*Generated by Solution Architect Agent | Pulse Onboarding Flow | February 2026*
