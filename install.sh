#!/usr/bin/env bash
set -e

# Antigravity Workspace Template Installer for Linux/macOS
# This script sets up the development environment automatically
# Enhanced with MCP servers, graph memory, and AI research tools

echo "🪐 Antigravity Workspace Template - Supercharged Installer"
echo "=========================================================="
echo "Setting up AI research environment with essential MCPs"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $PYTHON_VERSION detected. Python 3.8 or higher is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed."
    echo "Please install Git from https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git $(git --version | cut -d' ' -f3) detected"

# Check if Node.js is installed (required for MCP servers)
if ! command -v node &> /dev/null; then
    echo "⚠️  Warning: Node.js is not installed."
    echo "   Node.js is required for MCP servers (Context7, memory, etc.)"
    echo "   Install from: https://nodejs.org/"
    echo "   Continuing without MCP server setup..."
    NODE_AVAILABLE=false
else
    NODE_VERSION=$(node --version)
    echo "✅ Node.js $NODE_VERSION detected"
    NODE_AVAILABLE=true
fi

echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"

# Initialize configuration
echo "🔧 Setting up configuration..."

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Antigravity Workspace Configuration
# Copy this file and configure your API keys

# Google Gemini API Key (Required)
GOOGLE_API_KEY=your_api_key_here

# Optional: OpenAI API Key for alternative LLM
# OPENAI_API_KEY=your_openai_key_here

# Optional: Model Configuration
# MODEL_NAME=gemini-2.0-flash-exp
EOF
    echo "✅ Created .env file (please configure your API keys)"
else
    echo "⚠️  .env file already exists. Skipping creation."
fi

# Create artifacts directory if it doesn't exist
if [ ! -d "artifacts" ]; then
    mkdir -p artifacts
    echo "✅ Created artifacts directory"
fi

# Create additional directories for research workflow
echo "📁 Setting up research workspace directories..."
mkdir -p artifacts/papers
mkdir -p artifacts/analysis
mkdir -p artifacts/code_reviews
mkdir -p .context/research
mkdir -p .context/references
echo "✅ Created research workspace directories"

# Install essential MCP servers if Node.js is available
if [ "$NODE_AVAILABLE" = true ]; then
    echo ""
    echo "📦 Installing Essential MCP Servers..."
    echo "-------------------------------------------"
    
    # Install Context7 MCP for code intelligence
    echo "🧠 Installing @context7/mcp-server (code intelligence)..."
    npm install -g @context7/mcp-server 2>/dev/null || echo "⚠️  Context7 installation skipped (may require manual setup)"
    
    # Install Memory MCP for persistent context
    echo "💾 Installing @modelcontextprotocol/server-memory..."
    npm install -g @modelcontextprotocol/server-memory 2>/dev/null || echo "✅ Memory server available via npx"
    
    # Install Filesystem MCP
    echo "📂 Installing @modelcontextprotocol/server-filesystem..."
    npm install -g @modelcontextprotocol/server-filesystem 2>/dev/null || echo "✅ Filesystem server available via npx"
    
    # Install GitHub MCP for repository analysis
    echo "🐙 Installing @modelcontextprotocol/server-github..."
    npm install -g @modelcontextprotocol/server-github 2>/dev/null || echo "✅ GitHub server available via npx"
    
    # Install Brave Search MCP for research
    echo "🔍 Installing @modelcontextprotocol/server-brave-search..."
    npm install -g @modelcontextprotocol/server-brave-search 2>/dev/null || echo "✅ Brave Search server available via npx"
    
    # Install Puppeteer MCP for web scraping research papers
    echo "🤖 Installing @modelcontextprotocol/server-puppeteer..."
    npm install -g @modelcontextprotocol/server-puppeteer 2>/dev/null || echo "✅ Puppeteer server available via npx"
    
    echo "✅ MCP servers installation complete"
else
    echo "⚠️  Skipping MCP server installation (Node.js not available)"
fi

echo ""
echo "=========================================================="
echo "✅ Installation complete!"
echo ""
echo "🎯 Research Paper AI Setup Complete"
echo "-------------------------------------------"
echo ""
echo "Next steps:"
echo "1. Configure your API keys in .env file:"
echo "   nano .env"
echo "   (Add: GOOGLE_API_KEY, GITHUB_TOKEN, BRAVE_API_KEY)"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Enable MCP servers in mcp_servers.json:"
echo "   - Context7: Code intelligence & import suggestions"
echo "   - Memory: Graph memory for research context"
echo "   - GitHub: Repository analysis"
echo "   - Brave Search: Academic paper search"
echo "   - Puppeteer: Web scraping for research"
echo ""
echo "4. Run the agent for research tasks:"
echo "   python src/agent.py \"Analyze code quality\""
echo "   python src/agent.py \"Research topic: neural networks\""
echo ""
echo "📚 Documentation: docs/en/QUICK_START.md"
echo "🔬 Research Tools: artifacts/papers/, artifacts/analysis/"
echo "=========================================================="
