# Figma Orchestrator Skill

Orchestrate Figma design creation via Claude CLI with MCP integration.

## Architecture

```
Clawdbot (Jarvis) → Claude CLI + MCPs → Figma Plugin → Figma
                         ↓
              [Figma MCP, Atlassian MCP, Asana MCP]
```

## Prerequisites

1. **Figma Desktop** running with MCP Plugin connected
2. **WebSocket Server** running (`bun socket` from claude-talk-to-figma-mcp)
3. **Claude CLI** configured with MCPs

## Setup

### 1. Start WebSocket Server
```bash
cd ~/clawd/research/figma-mcp/claude-figma
bun socket
```

### 2. Configure Claude CLI MCPs
```bash
# Figma MCP
claude mcp add figma -- bunx claude-talk-to-figma-mcp@latest

# Atlassian MCP (when ready)
claude mcp add atlassian -- npx @anthropic-ai/mcp-atlassian

# Asana MCP (when ready)
claude mcp add asana -- npx @anthropic-ai/mcp-asana
```

### 3. Connect Figma Plugin
- Open Figma Desktop
- Plugins → Development → Import from manifest
- Select: `~/clawd/research/figma-mcp/claude-figma/src/claude_mcp_plugin/manifest.json`
- Run plugin, copy channel ID

## Usage

### From Clawdbot
Jarvis spawns Claude CLI with Figma context:
```bash
claude --mcp figma "Connect to channel ABC123. Create a login flow with 3 screens..."
```

### Direct CLI
```bash
claude "Talk to Figma on channel ABC123. Read my current selection."
```

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
