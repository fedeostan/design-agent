---
name: figma
description: Figma design system constraints, annotation style, flow conventions, and component rules.
user-invocable: false
---

# Figma Orchestrator Skill

Orchestrate Figma design creation via Claude CLI with the official Figma MCP server.

## Architecture

```
Claude CLI
  ├── Figma MCP (official)     → Remote or Desktop mode
  │     Remote: mcp.figma.com (read-only, OAuth)
  │     Desktop: localhost:3845 (read + Code to Canvas write, requires Figma Desktop)
  │
  │     Read capabilities:
  │     - Screenshots, metadata, design context
  │     - Variables, Code Connect, node structure
  │
  │     Write capabilities:
  │     - generate_figma_design (Code to Canvas — HTML → Figma frames)
  │     - Code Connect mappings
  │     - NO granular write tools (no create_frame, rename_node, etc.)
  │
  ├── Atlassian MCP            → Jira & Confluence
  └── Asana MCP                → Task management
```

## Important: Quality Gates

**For reliable Figma design work:**
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

1. **Official Figma MCP** configured (remote or desktop mode)
2. **Claude CLI** configured with Figma MCP

## Setup

### 1. Install Official Figma MCP

**For read-only operations (remote mode):**
```bash
# Install via npm package
claude mcp add figma -- npx -y @modelcontextprotocol/server-figma

# OR configure manually in .mcp/config.json:
{
  "figma": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-figma"],
    "env": {
      "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_PERSONAL_ACCESS_TOKEN}"
    }
  }
}

# Authenticates via OAuth on first use
```

**For read/write operations (desktop mode):**
```bash
# Requires Figma Desktop app running
# Desktop server runs automatically at http://127.0.0.1:3845/mcp
# Requires Dev or Full seat on paid Figma plan

# Configure in .mcp/config.json:
{
  "figma": {
    "url": "http://127.0.0.1:3845/mcp"
  }
}
```

**Verification:**
```bash
claude mcp list | grep figma
# Should show: figma - configured
```

### 2. Other MCPs (optional)
```bash
# Atlassian MCP
claude mcp add atlassian -- npx @anthropic-ai/mcp-atlassian

# Asana MCP
claude mcp add asana -- npx @anthropic-ai/mcp-asana
```

## Tool Reference

### Official Figma MCP Tools

**Read Operations** (available in both remote and desktop modes):
| Tool | Purpose |
|------|---------|
| `get_file` | Get Figma file metadata and structure |
| `get_screenshot` | Capture screenshots of frames/nodes |
| `get_metadata` | Read node structure, properties, styles |
| `get_design_context` | Generate code context from designs |
| `get_node` / `get_nodes` | Get specific node(s) information |
| `get_document_info` | Get document structure |
| `get_selection` | Get currently selected nodes (desktop only) |
| `get_local_components` | List available local components |
| `get_remote_components` | List available library components |
| `get_styles` | List available styles |
| `get_variable_defs` | Extract design tokens and variables |
| `get_code_connect_map` | View Code Connect mappings |
| `get_code_connect_suggestions` | Get automated mapping suggestions |
| `generate_diagram` | Create FigJam diagrams from Mermaid |
| `get_figjam` | Read FigJam boards |

**Write Operations — Code to Canvas** (desktop mode only):

> **Important:** The Figma MCP has NO granular write tools. Tools like `create_frame`, `rename_node`, `set_auto_layout`, etc. **do not exist** in the MCP. The only way to push designs into Figma is via `generate_figma_design`.

| Tool | Purpose |
|------|---------|
| `generate_figma_design` | Convert HTML/CSS to Figma frames (Code to Canvas) |
| `add_code_connect_map` | Add Code Connect mapping |
| `send_code_connect_mappings` | Publish Code Connect mappings |

**How Code to Canvas works:**
1. Create a flat HTML file with inline styles representing the design
2. Include the Figma capture script: `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>`
3. Serve the HTML locally and open with the capture URL
4. Figma converts the rendered HTML into native Figma frames

**Best practices for clean output:**
- Keep DOM flat — max 3 levels of nesting
- Use semantic class names (they become Figma layer names)
- Use inline styles or `<style>` blocks, not external CSS
- Set a fixed viewport (`width=390` for mobile)
- Never capture directly from framework apps (React, Next.js) — the DOM wrappers create 10+ nesting levels

See: `prompts/code-to-canvas-workflow.md` for the full workflow.

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
