#!/bin/bash
# Setup script for Design Agent

echo "🎨 Design Agent Setup"
echo "====================="
echo ""

# Check for bun
if ! command -v bun &> /dev/null; then
    echo "📦 Installing Bun..."
    curl -fsSL https://bun.sh/install | bash
    source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null
fi

# Check for Claude CLI
if ! command -v claude &> /dev/null; then
    echo "❌ Claude CLI not found!"
    echo "   Install from: https://docs.anthropic.com/claude-code"
    exit 1
fi
echo "✅ Claude CLI found"

# Clone Figma MCP if not exists
FIGMA_MCP_DIR="$HOME/clawd/research/figma-mcp/claude-figma"
if [ ! -d "$FIGMA_MCP_DIR" ]; then
    echo "📦 Cloning Figma MCP..."
    mkdir -p "$HOME/clawd/research/figma-mcp"
    git clone --depth 1 https://github.com/arinspunk/claude-talk-to-figma-mcp.git "$FIGMA_MCP_DIR"
fi
echo "✅ Figma MCP ready"

# Install Figma MCP dependencies
cd "$FIGMA_MCP_DIR"
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Figma MCP dependencies..."
    bun install
fi

# Configure Claude CLI MCPs
echo ""
echo "🔧 Configuring MCPs..."

# Add Figma MCP
claude mcp add figma -- bunx claude-talk-to-figma-mcp@latest 2>/dev/null || true
echo "✅ Figma MCP configured"

# Add Atlassian MCP (optional - will fail without credentials)
# claude mcp add atlassian -- npx @anthropic-ai/mcp-atlassian 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start Figma server: ./scripts/start-figma.sh"
echo "2. Open Figma Desktop and run the Claude MCP Plugin"
echo "3. Copy the Channel ID from the plugin"
echo "4. Open claude in this folder: claude"
echo "5. Say: 'Connect to Figma channel {YOUR_CHANNEL_ID}'"
echo ""
echo "For Atlassian integration, set these env vars:"
echo "  export ATLASSIAN_URL=https://yoursite.atlassian.net"
echo "  export ATLASSIAN_EMAIL=your@email.com"
echo "  export ATLASSIAN_API_TOKEN=your_token"
