---
name: handoff
description: Implementation spec, Code Connect workflow, and design token guide.
user-invocable: false
---

# Handoff Skill

Templates and workflows for design-to-development handoff.

## Implementation Spec Template

```markdown
# Implementation Spec: [Feature Name]

## Overview
[What's being built. Key technical considerations.]

## Component Mapping
| Design Component | Code Component | Status | Notes |
|-----------------|----------------|--------|-------|
| [Figma name] | [Code path] | Exists / Build / Update | [Details] |

## Code Connect
| Figma Node | Component | Source | Framework |
|------------|-----------|--------|-----------|
| [nodeId] | [Name] | [path] | [React/etc] |

## Design Tokens

### Colors
| Token | Value | CSS Variable |
|-------|-------|-------------|
| [name] | [hex] | [--var] |

### Spacing
| Token | Value | Usage |
|-------|-------|-------|
| [name] | [px] | [context] |

### Typography
| Token | Spec | Usage |
|-------|------|-------|
| [name] | [font/size/weight] | [context] |

## Screen Notes
### [Screen Name]
- **Components:** [list]
- **State:** [what state this manages]
- **API:** [endpoints needed]
- **Accessibility:** [ARIA, keyboard, screen reader]
- **Complexity:** Low / Medium / High

## API Requirements
| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| [path] | [verb] | [shape] | [shape] |

## Implementation Order
1. [First] — [Rationale]
2. [Second]
3. [Third]
```

---

## Code Connect Workflow

### What is Code Connect?
Code Connect maps Figma design components to their code counterparts. When developers inspect a design in Figma, they see the actual code component to use, not just visual properties.

### Setup Process

1. **Get current mappings:**
   ```
   get_code_connect_map(nodeId, fileKey)
   ```
   Returns: `{ [nodeId]: { codeConnectSrc, codeConnectName } }`

2. **Get suggestions:**
   ```
   get_code_connect_suggestions(nodeId, fileKey)
   ```
   Returns automated mapping suggestions based on component names.

3. **Add a mapping:**
   ```
   add_code_connect_map(
     nodeId: "123:456",
     fileKey: "abc123",
     source: "src/components/Button.tsx",
     componentName: "Button",
     label: "React"
   )
   ```

4. **Bulk send mappings:**
   ```
   send_code_connect_mappings(
     nodeId: "root",
     fileKey: "abc123",
     mappings: [
       { nodeId: "123:456", componentName: "Button", source: "src/components/Button.tsx", label: "React" },
       { nodeId: "789:012", componentName: "Input", source: "src/components/Input.tsx", label: "React" }
     ]
   )
   ```

### Supported Labels
React, Web Components, Vue, Svelte, Storybook, Javascript, Swift UIKit, Objective-C UIKit, SwiftUI, Compose, Java, Kotlin, Android XML Layout, Flutter, Markdown

### Best Practices
- Map at the component level, not the instance level
- Use the most specific component path (e.g., `Button/Primary` not just `Button`)
- Include the framework label that matches the project's tech stack
- Review suggestions before applying — automated mappings need human verification
- Update mappings when components are renamed or moved

---

## Design Token Guide

### Extracting Tokens from Figma

```
get_variable_defs(nodeId, fileKey)
```

Returns variable definitions like: `{ 'icon/default/secondary': '#949494' }`

### Token Categories

#### Color Tokens
```css
/* Semantic naming */
--color-primary: #0066FF;
--color-primary-hover: #0052CC;
--color-error: #FF3B30;
--color-success: #34C759;
--color-text-primary: #1A1A1A;
--color-text-secondary: #666666;
--color-bg-primary: #FFFFFF;
--color-bg-secondary: #F5F5F5;
```

#### Spacing Tokens
```css
/* 8px grid system */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-2xl: 40px;
--spacing-3xl: 48px;
```

#### Typography Tokens
```css
--font-family: 'Inter', sans-serif;
--font-size-h1: 32px;
--font-size-h2: 24px;
--font-size-h3: 20px;
--font-size-body: 16px;
--font-size-caption: 12px;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-bold: 700;
```

#### Shadow Tokens
```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px rgba(0,0,0,0.07);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.10);
```

#### Border Tokens
```css
--radius-sm: 4px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-full: 9999px;
--border-width: 1px;
--border-color: #E5E5E5;
```

### Token Audit Checklist
- [ ] All colors in the design are tokenized (no raw hex values)
- [ ] All spacing follows the 8px grid
- [ ] Typography uses defined scale
- [ ] Shadows use defined tokens
- [ ] Border radii are consistent
- [ ] Tokens have semantic names (not `blue-500`, but `color-primary`)
- [ ] Dark mode variants defined (if applicable)

---

## Handoff Checklist

Before marking a design as ready for development:

### Design Completeness
- [ ] All screens and states are designed
- [ ] Responsive breakpoints defined (if applicable)
- [ ] Interactions and transitions specified
- [ ] Empty, loading, error states included
- [ ] Micro-copy is final (not placeholder)

### Documentation
- [ ] Business notes on each screen
- [ ] Dev notes with API/technical context
- [ ] Design notes explaining non-obvious decisions
- [ ] Open questions resolved or flagged

### Technical Readiness
- [ ] Components mapped via Code Connect
- [ ] Design tokens extracted
- [ ] API requirements documented
- [ ] Implementation order defined
- [ ] Complexity estimated per screen

### Accessibility
- [ ] Color contrast verified
- [ ] Touch targets verified (44x44px)
- [ ] Focus order documented
- [ ] Screen reader flow defined
- [ ] ARIA roles specified for custom components
