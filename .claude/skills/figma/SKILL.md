---
name: figma
description: Figma design system constraints, annotation style, flow conventions, and component rules.
user-invocable: false
---

# Figma Orchestrator Skill

Orchestrate Figma design creation via Claude CLI with two MCP servers.

## Architecture

```
Claude CLI
  ├── figma MCP (read-only)    → mcp.figma.com (remote, OAuth)
  │     Screenshots, metadata, design context, variables, Code Connect
  │
  ├── figma-edit MCP (write)   → Local Figma Desktop MCP
  │     Create/edit frames, components, text, styling, auto-layout, export
  │
  ├── Atlassian MCP            → Jira & Confluence
  └── Asana MCP                → Task management
```

## Important: Quality Gates

**For reliability when using figma-edit MCP:**
- ⚠️ The figma-edit MCP has known limitations (positioning bugs, text update workarounds)
- ✅ **Always use quality gates** before building: See [figma-quality-gates/SKILL.md](../figma-quality-gates/SKILL.md)
- ✅ **Run pre-flight tests:** See [figma-quality-gates/prompts/mcp-capability-test.md](../figma-quality-gates/prompts/mcp-capability-test.md)
- ✅ **Error recovery:** See [figma-quality-gates/prompts/error-recovery-patterns.md](../figma-quality-gates/prompts/error-recovery-patterns.md)

**Quick Quality Gate Checklist:**
1. **Before starting:** Gate 1 (Tool Ready) + Gate 2 (Components Ready)
2. **After first screen:** Gate 3 (First Screen Done) - validate positioning
3. **At mid-point:** Gate 4 (Mid-Point Review) - check consistency
4. **At completion:** Gate 5 (Final Review) - verify acceptance criteria

---

## Prerequisites

1. **`figma` MCP** configured (remote, always available)
2. **Figma Desktop** running with MCP plugin for `figma-edit`
3. **Claude CLI** configured with both MCPs

## Setup

### 1. Install `figma` MCP (Read-Only)
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
# Authenticates via OAuth on first use
```

### 2. Install `figma-edit` MCP (Write)
Requires Figma Desktop app with the MCP plugin running:
1. Open Figma Desktop
2. Run the MCP plugin (Plugins → MCP)
3. The local MCP server connects automatically
4. Verify: `claude mcp list | grep figma-edit`

### 3. Other MCPs (when ready)
```bash
# Atlassian MCP
claude mcp add atlassian -- npx @anthropic-ai/mcp-atlassian

# Asana MCP
claude mcp add asana -- npx @anthropic-ai/mcp-asana
```

## Tool Reference

### `figma` MCP (Read-Only)
| Tool | Purpose |
|------|---------|
| `get_screenshot` | Capture screenshots of frames/nodes |
| `get_metadata` | Read node structure, properties, styles |
| `get_design_context` | Generate code context from designs |
| `get_variable_defs` | Extract design tokens and variables |
| `get_code_connect_map` | View Code Connect mappings |
| `get_code_connect_suggestions` | Get automated mapping suggestions |
| `add_code_connect_map` | Add Code Connect mapping |
| `send_code_connect_mappings` | Publish Code Connect mappings |
| `generate_diagram` | Create FigJam diagrams from Mermaid |
| `get_figjam` | Read FigJam boards |

### `figma-edit` MCP (Write)
| Tool | Purpose |
|------|---------|
| `join_channel` | Connect to Figma Desktop session |
| `get_document_info` | Get document structure |
| `get_local_components` | List available local components |
| `get_remote_components` | List available library components |
| `get_styles` | List available styles |
| `create_frame` | Create new frames |
| `create_component_instance` | Instantiate components |
| `create_text` | Create text nodes |
| `create_rectangle/ellipse/polygon/star` | Create shapes |
| `set_auto_layout` | Configure auto-layout |
| `set_fill_color/stroke_color` | Set colors |
| `set_text_content/font_size/font_name` | Edit text |
| `move_node/resize_node/clone_node/delete_node` | Manipulate nodes |
| `export_node_as_image` | Export assets |

## Custom Constraints

All design work follows constraints in:
- `prompts/design-system-constraints.md` - Colors, typography, spacing
- `prompts/flow-style.md` - Arrow and flow conventions
- `prompts/annotation-style.md` - Note component usage

## Components to Create in Figma

Before using, create these components in your design system:
1. **Note/Business** - Business context notes
2. **Note/Design** - Design decision notes
3. **Note/Dev** - Developer handoff notes
4. **Note/Question** - Open questions
5. **Flow/Arrow** - FigJam-style connector

See `components/README.md` for specs.
