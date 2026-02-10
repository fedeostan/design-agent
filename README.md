# Design Agent 🎨

A Claude Code agent workspace for AI-powered design in Figma.

## What This Is

This repo is a workspace for Claude CLI. When you open Claude in this folder, it becomes a **design agent** with access to:

- **Figma** - Create and modify designs via MCP
- **Atlassian** - Pull context from Jira/Confluence (optional)
- **Asana** - Read tasks for requirements (optional)

## Quick Start

```bash
# 1. Run setup (first time only)
./scripts/setup.sh

# 2. Start Figma WebSocket server (keep open)
./scripts/start-figma.sh

# 3. In Figma: Run Claude MCP Plugin, copy Channel ID

# 4. Open Claude in this folder
cd ~/design-agent
claude

# 5. Connect and design!
# "Connect to Figma channel ABC123. Create a login flow."
```

## Structure

```
design-agent/
├── CLAUDE.md           # Agent instructions (Claude reads this)
├── .mcp/
│   └── config.json     # MCP server configurations
├── skills/
│   └── figma/          # Figma-specific skills
│       ├── prompts/    # Design constraints & rules
│       └── components/ # Component specs
├── scripts/
│   ├── setup.sh        # Initial setup
│   └── start-figma.sh  # Start WebSocket server
└── README.md
```

## How It Works

1. **Claude reads CLAUDE.md** when you start it in this folder
2. **MCPs provide tools** for Figma, Atlassian, etc.
3. **Skills folder** contains design rules and constraints
4. **You talk naturally**, Claude creates designs

## Example Commands

```
"Create a 3-screen onboarding flow with welcome, features, and get started"

"Read the current selection and add a Business Note below it"

"Connect this screen to the next with an arrow labeled 'Continue'"

"Update all buttons to use the Primary variant"
```

## Customization

### Add Your Design System
Edit `skills/figma/prompts/design-system-constraints.md`

### Add Note Types
Edit `skills/figma/prompts/annotation-style.md`

### Change Flow Style
Edit `skills/figma/prompts/flow-style.md`

---

Built for Fede by Jarvis 🤖
