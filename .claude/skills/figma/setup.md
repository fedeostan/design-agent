# Official Figma MCP Setup

## Overview

The official Figma MCP server provides comprehensive design access through two deployment modes:
- **Remote Server** (`https://mcp.figma.com/mcp`) - Read-only operations, works with browser Figma
- **Desktop Server** (`http://127.0.0.1:3845/mcp`) - Full read/write operations, requires Figma Desktop app

## Remote Server Setup (Read-Only)

**Best for:** Reviewing designs, extracting design tokens, Code Connect mappings

```bash
# Option 1: Install via npm package
claude mcp add figma -- npx -y @modelcontextprotocol/server-figma

# Option 2: Manual configuration in .mcp/config.json
{
  "figma": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-figma"],
    "env": {
      "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_PERSONAL_ACCESS_TOKEN}"
    }
  }
}

# Verify installation
claude mcp list | grep figma

# Authenticate (OAuth)
# Will prompt on first use - follow browser flow
```

**Get Personal Access Token:**
1. Go to [Figma Settings → Personal Access Tokens](https://www.figma.com/settings#access-tokens)
2. Generate new token
3. Save to environment variable: `FIGMA_PERSONAL_ACCESS_TOKEN`

---

## Desktop Server Setup (Read/Write)

**Best for:** Building screens, creating components, modifying designs

**Requirements:**
- Figma Desktop app (latest version)
- Dev or Full seat on a paid Figma plan
- Figma Desktop running while working

```bash
# Configure in .mcp/config.json
{
  "figma": {
    "url": "http://127.0.0.1:3845/mcp"
  }
}

# Verify installation
claude mcp list | grep figma

# Start Figma Desktop
# Desktop server automatically runs at localhost:3845
```

**Verification:**
1. Open Figma Desktop
2. Open any file
3. Test connection with a simple read operation
4. Confirm write operations work (if needed)

---

## Session Start Workflow

When starting a Figma design session:

### 1. Verify MCP is Available
```bash
claude mcp list | grep figma
```
Should show: `figma - configured` or similar

### 2. Get Figma File Link
Ask user for file URL: `https://figma.com/file/abc123/...`

### 3. Test Connection
**For remote server:**
- Use file link directly with tools
- Example: `get_file(file_url: "https://figma.com/...")`

**For desktop server:**
- Open file in Figma Desktop
- Use selection-based workflow or file link
- Example: `get_document_info()` or `get_selection()`

### 4. Verify Access
- Read file metadata to confirm access
- Check components and styles are visible
- Verify write permissions (if needed for desktop mode)

---

## Troubleshooting

### Remote Server Issues

**Problem:** Authentication fails
```bash
# Solution: Re-generate personal access token
# 1. Revoke old token in Figma settings
# 2. Generate new token
# 3. Update FIGMA_PERSONAL_ACCESS_TOKEN environment variable
# 4. Restart Claude CLI
```

**Problem:** "File not found" or "Unauthorized"
- Verify file URL is correct
- Confirm token has access to the file/team
- Check if file is in private team (token may need team access)

### Desktop Server Issues

**Problem:** Can't connect to desktop server
```bash
# Solution: Verify Figma Desktop is running
# 1. Quit and restart Figma Desktop
# 2. Confirm server is running: curl http://127.0.0.1:3845/health
# 3. Check Figma Desktop preferences for MCP settings
```

**Problem:** Write operations fail
- Confirm you have Dev or Full seat (Viewer seats can't write)
- Verify file is not locked or read-only
- Check if you have edit permissions on the file

### General Issues

**Problem:** MCP tools not available
```bash
# Solution: Restart MCP servers
claude mcp restart figma
# OR restart entire Claude CLI
```

**Problem:** Slow performance
- Desktop server is faster than remote server
- Use desktop mode for write-heavy workflows
- Use remote mode for read-only analysis

---

## Best Practices

1. **Use Remote Mode for:**
   - Code Connect mapping
   - Design token extraction
   - Screenshot generation
   - Design review and analysis

2. **Use Desktop Mode for:**
   - Building new screens
   - Creating components
   - Modifying existing designs
   - Bulk edit operations

3. **Always run quality gates before building:**
   - See: `.claude/skills/figma-quality-gates/SKILL.md`
   - Test MCP capabilities with Gate 1
   - Verify components with Gate 2
   - Validate first screen with Gate 3

4. **Keep Figma Desktop updated:**
   - Desktop server capabilities improve with each release
   - Check for updates regularly

---

## Additional Resources

- [Official Figma MCP Documentation](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- [Figma Personal Access Tokens](https://www.figma.com/developers/api#access-tokens)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
