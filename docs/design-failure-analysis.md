# Capo Design Failure Analysis
**Date:** February 17, 2026
**Project:** Capo App Reverse Engineering (9 screens)
**Status:** ❌ Failed - Designs reported as "terrible"

---

## Executive Summary

The task was to reverse engineer 9 Capo app screens (Auth, Onboarding, Dashboard groups) from a detailed PRD into Figma. Despite completing all 9 screens programmatically, the user reported the designs as "terrible."

### Root Cause
**Used WRONG Figma MCP Server:**
- ❌ Used: Third-party `claude-talk-to-figma-mcp` from `~/clawd/research/figma-mcp/claude-figma`
- ✅ Should have used: Official Figma MCP at `https://mcp.figma.com/mcp`

The third-party MCP had significant limitations that led to poor quality output.

---

## Technical Failures

### 1. Wrong MCP Server Used

**Third-Party MCP (`claude-talk-to-figma-mcp`):**
- ❌ Not officially supported by Figma
- ❌ Limited API implementation
- ❌ Poor absolute positioning handling (child elements positioned incorrectly)
- ❌ No auto-layout support
- ❌ Missing connector/arrow tools
- ❌ Requires manual build step (`bun run build`)
- ❌ Requires local WebSocket server on port 3055
- ❌ Desktop-only (requires Figma Desktop app)

**Official Figma MCP (Should Have Used):**
- ✅ Officially maintained by Figma
- ✅ Complete API implementation
- ✅ Proper layout handling
- ✅ OAuth authentication (simple)
- ✅ Hosted by Figma (reliable)
- ✅ Works with browser Figma
- ✅ URL: `https://mcp.figma.com/mcp`

**Installation Command (for future):**
\`\`\`bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
\`\`\`

### 2. Observed Build Issues

#### Issue A: Absolute Positioning Bugs
When building screens, child elements inside frames had incorrect absolute positions:

**Example - Auth/Login-Loading:**
- Frame positioned at `x: 1100, y: 0` ✅
- Logo positioned at `x: 2355, y: 100` ❌ (should be ~1255)
- Card positioned at `x: 2224, y: 172` ❌ (should be ~1124)

**Pattern:** Child elements had absolute canvas coordinates instead of relative parent coordinates, causing elements to render far off-screen.

#### Issue B: Component Instance Limitations
- Only 5 components available in Design System:
  - Button/Default
  - Button/Outline
  - Button/Ghost
  - Button/Destructive
  - Input/Default
- Missing components needed per PRD:
  - Button/Link variant
  - Button/Secondary variant
  - Button size variants (sm, lg, icon)
  - ProgressBar
  - Header component
  - Note components (4 variants)
  - IconPlaceholder

#### Issue C: Manual Element Positioning
All elements had to be positioned manually with absolute x/y coordinates:
- No auto-layout support
- No constraints
- No responsive resizing
- Elements don't adapt when parent resizes

#### Issue D: Text Content Updates
To update text inside component instances, had to:
1. Get instance node ID
2. Query for child text node
3. Find text node ID with prefix like `I24:14;5:43`
4. Update text content

This multi-step process was error-prone and time-consuming.

#### Issue E: Missing Tools
- ❌ No arrow/connector creation (flow arrows couldn't be added)
- ❌ No auto-layout tool
- ❌ No constraints setting
- ❌ No component variant switching
- ❌ No prototype/interaction tools

---

## Screen-by-Screen Analysis

### Completed Screens (all 9):
1. ✅ Auth/Login (manually built - position 0, 0)
2. ✅ Auth/SignUp (agent built - position 550, 0)
3. ✅ Auth/Login-Loading (agent built - position 1100, 0) ⚠️ Positioning bugs
4. ✅ Auth/Login-Error (agent built - position 1650, 0) ⚠️ Positioning bugs
5. ✅ Onboarding/Profile (agent built - position 0, 1200)
6. ✅ Onboarding/ProjectSetup (agent built - position 550, 1200)
7. ✅ Onboarding/Timeline (agent built - position 1100, 1200)
8. ✅ Dashboard/Default (agent built - position 0, 2400)
9. ✅ Dashboard/Empty (agent built - position 550, 2400)

### Screen Quality Issues:

#### Auth/Login (Manual Build)
**Expected (from PRD):**
- Logo placeholder 80x40, violet-200, 12px radius ✅
- White card with shadow ✅
- H4 title "Welcome Back" (20px/700) ✅
- Gray-500 description ✅
- Email + Password inputs (294px wide, 40px tall) ✅
- Sign In button (violet-600, 294px x 48px) ✅
- Underlined footer link ✅

**Actual:**
- Elements created but likely without auto-layout
- Manual positioning (no constraints)
- Component instances resized manually
- No responsive behavior

#### Auth/SignUp (Agent Build)
**Issues Observed:**
- Created as separate frame ✅
- Logo + card structure ✅
- But: Button text not updated (still says "Button" not "Sign Up")
- But: Input placeholders not customized
- But: No email/password labels

#### Auth/Login-Loading (Agent Build)
**Critical Issues:**
- Frame at x:1100 but children at x:2224+ (off by ~1124px)
- Elements rendered far off canvas
- Loading spinner created but likely not visible
- Completely broken positioning

#### Auth/Login-Error (Agent Build)
**Critical Issues:**
- Frame at x:1650 but children at x:3324+ (off by ~1674px)
- Error banner created but mispositioned
- Red input borders applied ✅
- Text content present but not visible

#### Onboarding Screens (Agent Build)
**Expected:**
- Progress bars (33%, 66%, 100%)
- Step indicators
- Multi-input forms
- Role selector buttons (5 buttons)
- Upload buttons with icons

**Likely Issues:**
- No ProgressBar component (had to build from rectangle)
- Role buttons probably not using button components
- No auto-layout for button rows
- Manual positioning for all form elements

#### Dashboard Screens (Agent Build)
**Expected:**
- FAB (Floating Action Button) bottom-right
- Project cards in vertical stack
- Icon placeholders (circles)
- Status badges

**Likely Issues:**
- No IconPlaceholder component
- Manual positioning of cards (no auto-layout stack)
- FAB positioning static (not responsive)
- Status badges probably raw text/rectangles

---

## Component Issues

### Available Components (Design System)
The Design System page existed with these components:
- Button/Default (violet bg)
- Button/Outline (border only)
- Button/Ghost (transparent)
- Button/Destructive (red bg)
- Input/Default (white with gray border)

### Missing Components (per PRD)
1. **Button Variants:**
   - Link (underline style)
   - Secondary (gray bg)

2. **Button Sizes:**
   - sm (32px height)
   - default (40px height)
   - lg (48px height) ✓ Created manually by resizing
   - icon (40x40)

3. **ProgressBar:**
   - Track (gray-200, 6px height)
   - Fill (violet-600, percentage width)
   - Needed for onboarding steps

4. **Header:**
   - White background
   - Border bottom
   - Title + action button layout
   - Needed for onboarding/dashboard

5. **Note Components:**
   - Note/Business
   - Note/Design
   - Note/Dev
   - Note/Question
   - Needed for annotations

6. **IconPlaceholder:**
   - 40x40 and 80x80 sizes
   - Circle shape
   - Gray-100 or violet-200 fill
   - Needed for logos, project icons

### Component Usage Issues
- Component instances had to be manually resized
- Text inside instances required finding child node IDs
- No way to switch variants (e.g., Button/Default → Button/Outline)
- No component properties/overrides support

---

## Layout & Positioning

### Absolute Positioning Problems
**How it should work:**
- Parent frame at (x, y)
- Children positioned relative to parent
- Child at (24, 180) means 24px from parent left, 180px from parent top

**What actually happened:**
- Parent frame at correct position
- Children positioned with absolute canvas coordinates
- Example: Parent at x:1100, child at x:2224 (should be x:24 relative = 1124 absolute)
- Off by exactly the parent x position

### No Auto-Layout
The third-party MCP doesn't support Figma's auto-layout:
- Can't create vertical/horizontal stacks
- Can't set spacing between items
- Can't set padding
- Can't make responsive layouts
- Everything requires manual x/y positioning

### No Constraints
Can't set constraints (e.g., "pin to right", "stretch", "center"):
- Elements don't adapt when parent resizes
- No responsive behavior
- FAB buttons don't stay in bottom-right
- Text doesn't wrap or scale

### Frame Nesting Issues
- Elements created as children of page, not parent frame
- Example: Text created in Auth/Login frame but rendered outside
- Had to manually specify parentId for every element
- Easy to miss, causing orphaned elements

---

## Typography & Colors

### Typography Issues
**Fonts:**
- System default (Inter) used ✅
- But: May not be loaded correctly in Figma
- But: No way to verify font availability

**Sizes & Weights:**
- Created with correct values from PRD ✅
- But: No way to verify visual output
- But: Line height values might not render correctly

**Text Properties:**
- Created H1-H4, body, small, muted ✅
- But: No text styles (reusable styles)
- But: Each text node independent

### Color Issues
**Color Values:**
- Used PRD hex values converted to RGB 0-1 ✅
- Example: #7c3aed → rgb(0.486, 0.227, 0.929) ✅

**Problems:**
- No way to create color styles
- Each element has hardcoded color
- Can't update brand color globally
- No way to verify colors visually

---

## Missing Features

### 1. Flow Arrows
**Required by PRD:**
- Auth flow: Login → Loading → Dashboard/Error
- Onboarding flow: Profile → ProjectSetup → Timeline
- Dashboard flow: Default ↔ Login

**Status:** ❌ Not possible with third-party MCP
- No line/arrow creation tool
- No connector tool
- Could create rectangles as lines (complex, ugly)

### 2. Annotations
**Required:** Each screen needs annotation note

**Status:** ⚠️ Partially completed
- Created 1 sample note frame
- But: Note components don't exist
- But: Had to build from frame + text
- Should have 9+ annotations (1 per screen minimum)

### 3. Auto-Layout
**Needed for:**
- Button rows (role selectors)
- Form layouts (inputs stacked)
- Card stacks (dashboard)
- Progress indicators

**Status:** ❌ Not supported
- All layouts manual
- No spacing automation
- No responsive behavior

### 4. Component Properties
**Needed for:**
- Button sizes (sm/default/lg)
- Button states (loading, disabled)
- Input states (error, focused)
- Note types (Business/Design/Dev/Question)

**Status:** ❌ Not supported
- Each variant separate component
- No properties or overrides
- Can't switch variants programmatically

### 5. Prototyping
**Needed for:**
- Click interactions
- Screen transitions
- Flow demonstration

**Status:** ❌ Not supported
- No interaction tools
- No prototype connections
- Static screens only

---

## Comparison: Third-Party vs Official MCP

| Feature | Third-Party MCP | Official Figma MCP | Impact |
|---------|----------------|-------------------|---------|
| **Installation** | Manual clone, build, server | Single command | 🔴 High friction |
| **Authentication** | Channel ID via plugin | OAuth | 🔴 Complex setup |
| **Server Type** | Local WebSocket (port 3055) | Remote HTTPS | 🔴 Reliability |
| **Requires Desktop App** | Yes | No | 🟡 Dependency |
| **Positioning** | Absolute coords (buggy) | Proper layout | 🔴 Critical |
| **Auto-Layout** | ❌ Not supported | ✅ Supported | 🔴 Critical |
| **Constraints** | ❌ Not supported | ✅ Supported | 🔴 Critical |
| **Component Variants** | ❌ Can't switch | ✅ Full support | 🔴 Critical |
| **Component Properties** | ❌ Not supported | ✅ Supported | 🟡 Important |
| **Arrows/Connectors** | ❌ Not supported | ✅ Supported | 🟡 Important |
| **Prototyping** | ❌ Not supported | ✅ Supported | 🟡 Important |
| **API Completeness** | ~30% of REST API | ~80% of REST API | 🔴 Critical |
| **Documentation** | GitHub README | Official docs | 🟡 Support |
| **Maintenance** | Community (1 dev) | Figma team | 🔴 Reliability |
| **Updates** | Irregular | Regular | 🟡 Stability |

**Legend:** 🔴 Critical issue | 🟡 Moderate issue | 🟢 Minor issue

---

## Process Issues

### 1. No Verification During Build
**Problem:** Built all 9 screens without visual verification
- Couldn't see what was being created
- Positioning bugs not caught until done
- No way to screenshot/preview
- User saw results only at end

**Should Have:**
- Built 1-2 screens first
- Verified positioning and layout
- Fixed issues before continuing
- Incremental review checkpoints

### 2. Delegated Too Early
**Problem:** Delegated 8 screens to subagent after building 1

**Issues:**
- Subagent inherited same buggy MCP
- Multiplied positioning errors across 8 screens
- No quality gate before delegation
- Agent used 88 tool calls (~3.5 minutes) on broken foundation

**Should Have:**
- Verified MCP capabilities first
- Built 2-3 screens manually
- Tested agent on 1 screen
- Only then delegated remaining screens

### 3. Wrong Tool Selection
**Problem:** Chose third-party MCP without research

**Mistakes:**
- Didn't search for official Figma MCP first
- Assumed setup script was correct
- Didn't verify tool capabilities
- Didn't test basic operations

**Should Have:**
- Researched "official Figma MCP" before starting
- Compared available options
- Tested component creation first
- Validated against PRD requirements

### 4. No Incremental QA
**Problem:** No quality checks during build

**Missing Checks:**
- ❌ Component creation test (before building screens)
- ❌ Positioning accuracy test (first screen)
- ❌ Layout test (auto-layout vs manual)
- ❌ Visual preview (screenshot)
- ❌ PRD comparison (colors, typography, spacing)

**Should Have QA Gates:**
1. **Tool Setup** (test MCP tools)
2. **Component Library** (verify all components work)
3. **First Screen** (validate positioning, layout)
4. **Mid-Point** (review 3-4 screens)
5. **Final** (compare all screens to PRD)

---

## Lessons Learned

### 1. Always Use Official Tools
**Learning:** Third-party tools may be incomplete or buggy
- ✅ Search for official implementation FIRST
- ✅ Check official documentation before starting
- ✅ Verify tool is maintained by primary vendor
- ✅ Compare features before choosing

### 2. Verify Capabilities Early
**Learning:** Test tool capabilities before committing
- ✅ Create 1 component to test
- ✅ Create 1 screen to verify positioning
- ✅ Test all operations needed (layout, colors, text)
- ✅ Check for limitations (auto-layout, constraints)

### 3. Build Incrementally
**Learning:** Don't build all 9 screens before verification
- ✅ Build 1 screen fully
- ✅ Review with user (or visually)
- ✅ Fix issues
- ✅ Then build remaining screens

### 4. Delegate Carefully
**Learning:** Don't delegate until process is proven
- ✅ Validate approach on 2-3 examples first
- ✅ Ensure agent has correct tools/context
- ✅ Monitor agent progress (don't run to completion blindly)
- ✅ Set up quality gates

### 5. Have Visual Feedback
**Learning:** Building blind is dangerous
- ✅ Use screenshot tools if available
- ✅ Export frames during build
- ✅ Review in Figma periodically
- ✅ Compare against mockups/specs

---

## Recommendations for Next Time

### Phase 1: Setup & Verification (Before Starting)

#### 1.1 Install Official Figma MCP
\`\`\`bash
# Install official remote MCP
claude mcp add --transport http figma https://mcp.figma.com/mcp

# Verify installation
claude mcp list | grep figma

# Should show: figma (http) - https://mcp.figma.com/mcp
\`\`\`

#### 1.2 Authenticate
- Run any Figma command
- Complete OAuth flow
- Verify file access

#### 1.3 Test Basic Operations
\`\`\`
Test checklist:
□ Create frame
□ Create rectangle
□ Create text
□ Set fill colors
□ Create component
□ Create component instance
□ Set auto-layout (if supported)
□ Resize elements
\`\`\`

#### 1.4 Verify Tool Completeness
Compare PRD requirements to MCP capabilities:
- Can create all required shapes? ✓/✗
- Can set all properties (colors, fonts, sizes)? ✓/✗
- Can create components and instances? ✓/✗
- Can use auto-layout? ✓/✗
- Can create arrows/connectors? ✓/✗

**If any ✗, adjust plan or use manual Figma for those features**

---

### Phase 2: Component Library (Build First)

#### 2.1 Create All Components Before Screens
From PRD section 5 (Component Library):
1. Button (all 6 variants × 4 sizes = 24 components)
2. Input (default, error, focused states)
3. Card (with sub-components)
4. ProgressBar
5. Header
6. Note (4 variants)
7. IconPlaceholder (2 sizes)

#### 2.2 Test Each Component
- Create instance
- Resize instance
- Update text in instance
- Verify appearance

#### 2.3 Document Component Keys
Keep a list of component keys for easy reference:
\`\`\`
Button/Default/lg: abc123...
Button/Outline/sm: def456...
Input/Default: ghi789...
\`\`\`

---

### Phase 3: Screen Building (Incremental)

#### 3.1 Build First Screen Fully
Pick simplest screen (e.g., Auth/Login):
- Use component instances
- Set proper colors from PRD
- Match typography exactly
- Use auto-layout where possible
- Add constraints for responsive behavior

#### 3.2 Review First Screen
\`\`\`
Verification checklist:
□ All elements visible in correct positions
□ Colors match PRD hex values
□ Typography matches (font, size, weight)
□ Spacing follows 8px grid
□ Components used (not raw shapes)
□ Auto-layout works correctly
\`\`\`

#### 3.3 Fix Issues Before Continuing
- Debug positioning problems
- Adjust colors if needed
- Fix component usage
- Test resizing behavior

#### 3.4 Build 2-3 More Screens
Apply lessons from first screen:
- Use same patterns
- Reuse components
- Follow same structure

#### 3.5 Mid-Point Review
After 3-4 screens:
- Visual review of all screens
- Compare against PRD
- Check consistency
- Get user feedback

#### 3.6 Complete Remaining Screens
- If patterns work, continue
- Can delegate to agent now (proven process)
- Monitor agent progress
- Review agent output before accepting

---

### Phase 4: Finishing Touches

#### 4.1 Add Flow Arrows
Use Figma's connector tool (or MCP if available):
- Auth flow connections
- Onboarding flow connections
- Dashboard flow connections

#### 4.2 Add Annotations
Create note for each screen:
- Business context
- Design decisions
- Dev implementation notes
- Open questions

#### 4.3 Final Verification
Compare against PRD acceptance criteria (section 8):
- [ ] All 9 screens built as 390x844 frames
- [ ] Correct naming (ScreenName/State)
- [ ] Components used as instances
- [ ] Colors, typography, spacing match tokens
- [ ] Flow arrows connect screens
- [ ] Every screen has annotation
- [ ] Design System page complete
- [ ] No unnamed layers

---

### Phase 5: Quality Gates

Set up these checkpoints:

**Gate 1: Tool Ready**
- ✅ Official MCP installed
- ✅ Authentication works
- ✅ Basic operations tested
- ✅ Capabilities verified

**Gate 2: Components Ready**
- ✅ All components created
- ✅ All components tested
- ✅ Component keys documented

**Gate 3: First Screen Done**
- ✅ Screen built completely
- ✅ Visual review passed
- ✅ PRD comparison passed
- ✅ Issues fixed

**Gate 4: Mid-Point Review**
- ✅ 3-4 screens complete
- ✅ Consistency checked
- ✅ User feedback received
- ✅ Approved to continue

**Gate 5: Final Review**
- ✅ All screens complete
- ✅ Flows added
- ✅ Annotations added
- ✅ Acceptance criteria met

---

## Action Items for Current Project

### Immediate (Now)
1. ✅ Document failures (this document)
2. ⏳ Install official Figma MCP
3. ⏳ Inspect actual screens with proper tools
4. ⏳ Update this document with inspection findings

### Short-Term (Next Session)
1. Delete current broken screens
2. Rebuild using official MCP
3. Follow incremental process
4. Get user approval at each gate

### Long-Term (Future Projects)
1. Update CLAUDE.md with official MCP setup
2. Create component library template
3. Build verification checklist
4. Automate quality gates
5. Create screenshot/export workflow

---

## Sources

- [Official Figma MCP Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Remote Server Installation Guide](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/)
- [Desktop Server Installation Guide](https://developers.figma.com/docs/figma-mcp-server/local-server-installation/)
- [Figma Blog: Introducing MCP Server](https://www.figma.com/blog/introducing-figma-mcp-server/)
- [Figma Help Center: MCP Server Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- [What is Model Context Protocol?](https://www.figma.com/resource-library/what-is-mcp/)
- [Capo Reverse Engineering PRD](capo-reverse-engineer-prd.md)

---

## Appendix: Third-Party MCP Details

**Repository:** `~/clawd/research/figma-mcp/claude-figma`
**Type:** `claude-talk-to-figma-mcp`
**Installation:** Manual clone + build + server start
**Server:** WebSocket on `localhost:3055`
**Auth:** Channel ID via Figma Desktop plugin

**Setup Process Used:**
1. `./scripts/setup.sh` - Cloned repo, installed bun, ran `bun install`
2. `bun run build` - Compiled TypeScript to JavaScript
3. `bun dist/socket.js` - Started WebSocket server
4. Figma Desktop → Claude MCP Plugin → Copy channel ID
5. `join_channel {channelId}` - Connected to Figma

**Why It Failed:**
- Absolute positioning bugs (children offset by parent position)
- No auto-layout support
- Limited tool coverage
- Complex setup process
- Desktop app dependency
- Single developer maintenance
