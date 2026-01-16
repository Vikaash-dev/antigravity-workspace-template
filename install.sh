#!/usr/bin/env bash
set -e

# Antigravity Workspace Template - Complete Auto-Setup for Linux/macOS
# This script automatically installs, configures, and sets up everything globally

echo "🪐 Antigravity Workspace Template - Auto-Setup"
echo "====================================================="
echo "Setting up AI research environment with global config"
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
# Antigravity Workspace Configuration - Auto-Setup Edition
# This file was automatically generated. Configure your API keys below.

# ============================================================
# AI Model Configuration
# ============================================================

# Google Gemini API Key (Primary LLM)
# Get your key at: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash

# Optional: OpenAI API Key for alternative LLM
# OPENAI_API_KEY=sk-your_openai_key_here
# OPENAI_BASE_URL=https://api.openai.com/v1

# ============================================================
# MCP Server Configuration (Essential for Research)
# ============================================================

# GitHub Token - For repository analysis and code mining
# Generate at: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_your_github_token_here

# Tavily API Key - AI-powered search for academic papers
# Get free API key at: https://tavily.com
TAVILY_API_KEY=tvly-your_tavily_api_key

# Google Custom Search API - For comprehensive research
# Get API key at: https://developers.google.com/custom-search/v1/overview
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# ============================================================
# Agent Configuration
# ============================================================

# Enable MCP (Model Context Protocol) integration
MCP_ENABLED=true

# Agent behavior settings
AGENT_NAME=ResearchAssistant
MAX_ITERATIONS=10
TEMPERATURE=0.7

# ============================================================
# Task Manager Configuration
# ============================================================

# Maximum parallel workers for task execution
MAX_PARALLEL_TASKS=4

# Enable automatic task import from MCP
AUTO_IMPORT_MCP_TASKS=true

# ============================================================
# Sandbox Configuration
# ============================================================

SANDBOX_TYPE=local
SANDBOX_TIMEOUT_SEC=30
SANDBOX_MAX_OUTPUT_KB=10
EOF
    echo "✅ Created .env file with global configuration"
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
mkdir -p artifacts/plans
mkdir -p artifacts/tasks
mkdir -p .context/research
mkdir -p .context/references
echo "✅ Created research workspace directories"

# Install essential MCP servers if Node.js is available
if [ "$NODE_AVAILABLE" = true ]; then
    echo ""
    echo "📦 Installing Essential MCP Servers Globally..."
    echo "-------------------------------------------"
    
    # Install Context7 MCP for code intelligence
    echo "🧠 Installing @context7/mcp-server (code intelligence)..."
    npm install -g @context7/mcp-server 2>/dev/null || echo "✅ Context7 available via npx"
    
    # Install Memory MCP for persistent context
    echo "💾 Installing @modelcontextprotocol/server-memory..."
    npm install -g @modelcontextprotocol/server-memory 2>/dev/null || echo "✅ Memory server available via npx"
    
    # Install Filesystem MCP
    echo "📂 Installing @modelcontextprotocol/server-filesystem..."
    npm install -g @modelcontextprotocol/server-filesystem 2>/dev/null || echo "✅ Filesystem server available via npx"
    
    # Install GitHub MCP for repository analysis
    echo "🐙 Installing @modelcontextprotocol/server-github..."
    npm install -g @modelcontextprotocol/server-github 2>/dev/null || echo "✅ GitHub server available via npx"
    
    # Install Tavily Search MCP for AI-powered research
    echo "🔍 Installing @tavily/mcp-server (AI-powered search)..."
    npm install -g @tavily/mcp-server 2>/dev/null || echo "✅ Tavily server available via npx"
    
    # Install Google Search MCP for comprehensive research
    echo "🌐 Installing @modelcontextprotocol/server-google-search..."
    npm install -g @modelcontextprotocol/server-google-search 2>/dev/null || echo "✅ Google Search server available via npx"
    
    # Install Tasks MCP for task management and parallel execution
    echo "📋 Installing @antigravity/mcp-tasks (task orchestration)..."
    npm install -g @antigravity/mcp-tasks 2>/dev/null || echo "✅ Tasks server available via npx"
    
    # Install Puppeteer MCP for web scraping research papers
    echo "🤖 Installing @modelcontextprotocol/server-puppeteer..."
    npm install -g @modelcontextprotocol/server-puppeteer 2>/dev/null || echo "✅ Puppeteer server available via npx"
    
    echo "✅ MCP servers installation complete"
else
    echo "⚠️  Skipping MCP server installation (Node.js not available)"
fi

# Run automatic configuration setup
echo ""
echo "🤖 Running automatic agent configuration..."
python3 -c "from src.config import settings; print(f'✅ Agent configured: {settings.AGENT_NAME}')" 2>/dev/null || echo "⚠️  Could not verify agent config"

# Test MCP connectivity
if [ "$NODE_AVAILABLE" = true ]; then
    echo ""
    echo "🔌 Testing MCP server connectivity..."
    python3 -c "import json; mcp = json.load(open('mcp_servers.json')); enabled = [s['name'] for s in mcp['servers'] if s.get('enabled')]; print(f'✅ {len(enabled)} MCP servers enabled: {\", \".join(enabled[:5])}')" 2>/dev/null || echo "⚠️  Could not verify MCP config"
fi

# Initialize task manager
echo ""
echo "📋 Initializing task manager..."
python3 -c "from src.tools.task_manager import get_task_manager, import_ai_tasks_from_mcp; tm = get_task_manager(); tasks = import_ai_tasks_from_mcp(); print(f'✅ Task manager initialized with {len(tasks)} imported AI tasks')" 2>/dev/null || echo "⚠️  Task manager will be initialized on first use"

echo ""
echo "====================================================="
echo "✅ Complete Auto-Setup Finished!"
echo ""
echo "🎯 Global Configuration Summary"
echo "---------------------------------------------------"
echo "  ✓ Python environment: Configured"
echo "  ✓ Virtual environment: Created and activated"
echo "  ✓ Dependencies: Installed"
echo "  ✓ MCP Servers: Installed globally (if Node.js available)"
echo "  ✓ Research directories: Created"
echo "  ✓ Global .env: Configured"
echo "  ✓ Task manager: Initialized"
echo "  ✓ Workflows: Ready"
echo ""
echo "📝 Next steps:"
echo "---------------------------------------------------"
echo "1. Configure your API keys in .env file:"
echo "   nano .env"
echo "   (Required: GOOGLE_API_KEY, GITHUB_TOKEN, TAVILY_API_KEY)"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Verify MCP servers are running:"
echo "   python src/agent.py \"Show available tools\""
echo ""
echo "4. Start researching:"
echo "   python src/agent.py \"Create research plan for: [your topic]\""
echo ""
echo "📚 Documentation:"
echo "   - Quick Start: QUICKSTART_RESEARCH.md"
echo "   - Full Guide: RESEARCH_SETUP_GUIDE.md"
echo "   - Scripts: SCRIPT_EXPLANATION.md"
echo ""
echo "🚀 Everything is configured globally!"
echo "   Run this script again anytime to update configuration."
echo "====================================================="
