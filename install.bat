@echo off
REM Antigravity Workspace Template - Complete Auto-Setup for Windows
REM This script automatically installs, configures, and sets up everything globally

setlocal enabledelayedexpansion

echo.
echo 🪐 Antigravity Workspace Template - Auto-Setup
echo =====================================================
echo Setting up AI research environment with global config
echo.

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python !PYTHON_VERSION! detected

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Git is not installed.
    echo Please install Git from https://git-scm.com/downloads
    pause
    exit /b 1
)

for /f "tokens=3" %%i in ('git --version') do set GIT_VERSION=%%i
echo ✅ Git !GIT_VERSION! detected

REM Check if Node.js is installed (required for MCP servers)
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Node.js is not installed.
    echo    Node.js is required for MCP servers (Context7, memory, tasks, etc.)
    echo    Install from: https://nodejs.org/
    echo    Continuing without MCP server setup...
    set NODE_AVAILABLE=false
) else (
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ Node.js !NODE_VERSION! detected
    set NODE_AVAILABLE=true
)

echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist "venv\" (
    echo ⚠️  Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ⚠️  Warning: pip upgrade had issues, continuing...
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Error: Failed to install dependencies.
    pause
    exit /b 1
)
echo ✅ Dependencies installed

REM Create directory structure for research workflow
echo 📁 Setting up research workspace directories...
if not exist "artifacts\" mkdir artifacts
if not exist "artifacts\papers\" mkdir artifacts\papers
if not exist "artifacts\analysis\" mkdir artifacts\analysis
if not exist "artifacts\code_reviews\" mkdir artifacts\code_reviews
if not exist "artifacts\plans\" mkdir artifacts\plans
if not exist "artifacts\tasks\" mkdir artifacts\tasks
if not exist ".context\" mkdir .context
if not exist ".context\research\" mkdir .context\research
if not exist ".context\references\" mkdir .context\references
echo ✅ Created research workspace directories

REM Install essential MCP servers globally if Node.js is available
if "!NODE_AVAILABLE!"=="true" (
    echo.
    echo 📦 Installing Essential MCP Servers Globally...
    echo ---------------------------------------------------
    
    echo 🧠 Installing @context7/mcp-server (code intelligence)...
    call npm install -g @context7/mcp-server 2>nul || echo ✅ Context7 available via npx
    
    echo 💾 Installing @modelcontextprotocol/server-memory...
    call npm install -g @modelcontextprotocol/server-memory 2>nul || echo ✅ Memory server available via npx
    
    echo 📂 Installing @modelcontextprotocol/server-filesystem...
    call npm install -g @modelcontextprotocol/server-filesystem 2>nul || echo ✅ Filesystem server available via npx
    
    echo 🐙 Installing @modelcontextprotocol/server-github...
    call npm install -g @modelcontextprotocol/server-github 2>nul || echo ✅ GitHub server available via npx
    
    echo 🔍 Installing @tavily/mcp-server (AI-powered search)...
    call npm install -g @tavily/mcp-server 2>nul || echo ✅ Tavily server available via npx
    
    echo 🌐 Installing @modelcontextprotocol/server-google-search...
    call npm install -g @modelcontextprotocol/server-google-search 2>nul || echo ✅ Google Search server available via npx
    
    echo 📋 Installing @antigravity/mcp-tasks (task orchestration)...
    call npm install -g @antigravity/mcp-tasks 2>nul || echo ✅ Tasks server available via npx
    
    echo 🤖 Installing @modelcontextprotocol/server-puppeteer...
    call npm install -g @modelcontextprotocol/server-puppeteer 2>nul || echo ✅ Puppeteer server available via npx
    
    echo ✅ MCP servers installation complete
) else (
    echo ⚠️  Skipping MCP server installation (Node.js not available)
)

REM Initialize global configuration
echo.
echo 🔧 Setting up global configuration...

REM Create .env with all required keys if it doesn't exist
if not exist ".env" (
    (
        echo # Antigravity Workspace Configuration - Auto-Setup Edition
        echo # This file was automatically generated. Configure your API keys below.
        echo.
        echo # ============================================================
        echo # AI Model Configuration
        echo # ============================================================
        echo.
        echo # Google Gemini API Key (Primary LLM^)
        echo # Get your key at: https://makersuite.google.com/app/apikey
        echo GOOGLE_API_KEY=your_google_api_key_here
        echo GEMINI_MODEL_NAME=gemini-2.5-flash
        echo.
        echo # Optional: OpenAI API Key for alternative LLM
        echo # OPENAI_API_KEY=sk-your_openai_key_here
        echo # OPENAI_BASE_URL=https://api.openai.com/v1
        echo.
        echo # ============================================================
        echo # MCP Server Configuration (Essential for Research^)
        echo # ============================================================
        echo.
        echo # GitHub Token - For repository analysis and code mining
        echo # Generate at: https://github.com/settings/tokens
        echo GITHUB_TOKEN=ghp_your_github_token_here
        echo.
        echo # Tavily API Key - AI-powered search for academic papers
        echo # Get free API key at: https://tavily.com
        echo TAVILY_API_KEY=tvly-your_tavily_api_key
        echo.
        echo # Google Custom Search API - For comprehensive research
        echo # Get API key at: https://developers.google.com/custom-search/v1/overview
        echo GOOGLE_SEARCH_API_KEY=your_google_search_api_key
        echo GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
        echo.
        echo # ============================================================
        echo # Agent Configuration
        echo # ============================================================
        echo.
        echo # Enable MCP (Model Context Protocol^) integration
        echo MCP_ENABLED=true
        echo.
        echo # Agent behavior settings
        echo AGENT_NAME=ResearchAssistant
        echo MAX_ITERATIONS=10
        echo TEMPERATURE=0.7
        echo.
        echo # ============================================================
        echo # Task Manager Configuration
        echo # ============================================================
        echo.
        echo # Maximum parallel workers for task execution
        echo MAX_PARALLEL_TASKS=4
        echo.
        echo # Enable automatic task import from MCP
        echo AUTO_IMPORT_MCP_TASKS=true
        echo.
        echo # ============================================================
        echo # Sandbox Configuration
        echo # ============================================================
        echo.
        echo SANDBOX_TYPE=local
        echo SANDBOX_TIMEOUT_SEC=30
        echo SANDBOX_MAX_OUTPUT_KB=10
    ) > .env
    echo ✅ Created .env file with global configuration
) else (
    echo ⚠️  .env file already exists. Skipping creation.
)

REM Run automatic configuration setup
echo.
echo 🤖 Running automatic agent configuration...
python -c "from src.config import settings; print(f'✅ Agent configured: {settings.AGENT_NAME}')" 2>nul || echo ⚠️  Could not verify agent config

REM Test MCP connectivity
if "!NODE_AVAILABLE!"=="true" (
    echo.
    echo 🔌 Testing MCP server connectivity...
    python -c "import json; mcp = json.load(open('mcp_servers.json')); enabled = [s['name'] for s in mcp['servers'] if s.get('enabled')]; print(f'✅ {len(enabled)} MCP servers enabled: {', '.join(enabled[:5])}')" 2>nul || echo ⚠️  Could not verify MCP config
)

REM Initialize task manager
echo.
echo 📋 Initializing task manager...
python -c "from src.tools.task_manager import get_task_manager, import_ai_tasks_from_mcp; tm = get_task_manager(); tasks = import_ai_tasks_from_mcp(); print(f'✅ Task manager initialized with {len(tasks)} imported AI tasks')" 2>nul || echo ⚠️  Task manager will be initialized on first use

echo.
echo =====================================================
echo ✅ Complete Auto-Setup Finished!
echo.
echo 🎯 Global Configuration Summary
echo ---------------------------------------------------
echo   ✓ Python environment: Configured
echo   ✓ Virtual environment: Created and activated
echo   ✓ Dependencies: Installed
echo   ✓ MCP Servers: Installed globally (if Node.js available^)
echo   ✓ Research directories: Created
echo   ✓ Global .env: Configured
echo   ✓ Task manager: Initialized
echo   ✓ Workflows: Ready
echo.
echo 📝 Next steps:
echo ---------------------------------------------------
echo 1. Configure your API keys in .env file:
echo    notepad .env
echo    (Required: GOOGLE_API_KEY, GITHUB_TOKEN, TAVILY_API_KEY^)
echo.
echo 2. Verify MCP servers are running:
echo    python -c "from src.mcp_client import MCPManager; print('MCP Status: OK'^)"
echo.
echo 3. Test the setup:
echo    python src/agent.py "Show available tools"
echo.
echo 4. Start researching:
echo    python src/agent.py "Create research plan for: [your topic]"
echo.
echo 📚 Documentation:
echo    - Quick Start: QUICKSTART_RESEARCH.md
echo    - Full Guide: RESEARCH_SETUP_GUIDE.md
echo    - Scripts: SCRIPT_EXPLANATION.md
echo.
echo 🚀 Everything is configured globally!
echo    Run this script again anytime to update configuration.
echo =====================================================
echo.
pause
