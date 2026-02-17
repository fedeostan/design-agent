# Figma MCP Setup

## `figma` MCP Setup (Read-Only)
```bash
# Install official Figma MCP (remote server)
claude mcp add --transport http figma https://mcp.figma.com/mcp

# Verify installation
claude mcp list | grep figma

# Authenticate (OAuth)
# Will prompt on first use - follow browser flow
```

## `figma-edit` MCP Setup (Write)
Requires Figma Desktop app running with the MCP plugin:
1. Open Figma Desktop
2. Run the MCP plugin (Plugins → MCP)
3. The local MCP server connects automatically
4. Verify: `claude mcp list | grep figma-edit`

## Session Start
When starting a Figma design session:
1. **Verify both MCPs are available:**
   ```bash
   claude mcp list | grep figma
   ```
   Should show both `figma` (remote) and `figma-edit` (local)

2. **Get Figma file link** from user (e.g., `https://figma.com/file/abc123/...`)

3. **Connect and verify:**
   - Use `figma` MCP tools with file link for reading
   - Use `figma-edit` tools for creating/modifying designs
   - For `figma-edit`: join the channel first, then get document info
