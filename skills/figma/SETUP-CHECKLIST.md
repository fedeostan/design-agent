# Figma Orchestrator Setup Checklist

## When You Get Home

### Phase 1: Basic Setup (15 min)

- [ ] **Install Bun** (if not already)
  ```bash
  curl -fsSL https://bun.sh/install | bash
  ```

- [ ] **Install dependencies for Figma MCP**
  ```bash
  cd ~/clawd/research/figma-mcp/claude-figma
  bun install
  ```

- [ ] **Configure Claude CLI with Figma MCP**
  ```bash
  claude mcp add figma -- bunx claude-talk-to-figma-mcp@latest
  ```

- [ ] **Start WebSocket Server**
  ```bash
  cd ~/clawd/research/figma-mcp/claude-figma
  bun socket
  # Keep this terminal open - server runs on localhost:3055
  ```

### Phase 2: Figma Plugin (10 min)

- [ ] **Open Figma Desktop**

- [ ] **Import the MCP Plugin**
  - Menu → Plugins → Development → Import plugin from manifest
  - Select: `~/clawd/research/figma-mcp/claude-figma/src/claude_mcp_plugin/manifest.json`

- [ ] **Run the Plugin**
  - Plugins → Development → Claude MCP Plugin
  - Copy the **Channel ID** that appears

- [ ] **Test Connection**
  ```bash
  claude "Talk to Figma on channel {YOUR_CHANNEL_ID}. What's the current document name?"
  ```

### Phase 3: Design System Components (20 min)

- [ ] **Create Note Components** (in your design system file)
  - Note/Business (see components/README.md for specs)
  - Note/Design
  - Note/Dev
  - Note/Question

- [ ] **Publish the Library**
  - Right-click library → Publish

- [ ] **Link to Working File**
  - In your working file: Assets → Team Library → Enable your design system

### Phase 4: Test It! (5 min)

- [ ] **Verify components are visible**
  ```bash
  claude "Connect to Figma channel {ID}. List all local components."
  ```

- [ ] **Create a test note**
  ```bash
  claude "Connect to Figma channel {ID}. Create an instance of Note/Business at position 0,0."
  ```

- [ ] **Tell Jarvis you're ready**
  ```
  "Figma MCP is connected. Channel ID is: {YOUR_ID}. Components are ready."
  ```

---

## Phase 5: Additional MCPs (When Ready)

### Atlassian MCP
```bash
# Install
claude mcp add atlassian -- npx @anthropic-ai/mcp-atlassian

# Configure (needs API token)
# Get token: https://id.atlassian.com/manage-profile/security/api-tokens
```

### Asana MCP
```bash
# Find the right package (check npm/GitHub)
claude mcp add asana -- npx @anthropic-ai/mcp-asana
```

---

## Troubleshooting

### WebSocket won't connect
```bash
# Check if server is running
curl http://localhost:3055/status
```

### Plugin not showing in Figma
- Restart Figma Desktop
- Re-import manifest

### Claude can't see components
- Make sure library is published AND linked
- Run `get_local_components` to debug

### Channel ID issues
- Each time you restart Figma plugin, you get a new channel ID
- Always re-copy the channel ID after restart

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `bun socket` | Start WebSocket server |
| `claude mcp list` | See configured MCPs |
| `curl localhost:3055/status` | Check server status |

---

**Done?** Tell Jarvis: "Figma setup complete, channel {ID}"
