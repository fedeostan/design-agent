#!/bin/bash
# Start the Figma WebSocket server

FIGMA_MCP_DIR="$HOME/clawd/research/figma-mcp/claude-figma"

if [ ! -d "$FIGMA_MCP_DIR" ]; then
    echo "❌ Figma MCP not found at $FIGMA_MCP_DIR"
    echo "   Run: ./scripts/setup.sh first"
    exit 1
fi

cd "$FIGMA_MCP_DIR"

# Check if bun is installed
if ! command -v bun &> /dev/null; then
    echo "❌ Bun not installed. Install with:"
    echo "   curl -fsSL https://bun.sh/install | bash"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    bun install
fi

echo "🚀 Starting Figma WebSocket server on localhost:3055..."
echo "   Keep this terminal open!"
echo ""
echo "   Next steps:"
echo "   1. Open Figma Desktop"
echo "   2. Run the Claude MCP Plugin"
echo "   3. Copy the Channel ID"
echo "   4. In another terminal: claude 'Connect to Figma channel {ID}'"
echo ""
bun socket
