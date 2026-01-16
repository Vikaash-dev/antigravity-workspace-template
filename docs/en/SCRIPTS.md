# Script Documentation

This document describes the purpose and usage of all scripts in the Antigravity Workspace Template.

## Table of Contents

- [Installation Scripts](#installation-scripts)
  - [install.sh](#installsh)
  - [install.bat](#installbat)
- [Agent Scripts](#agent-scripts)
  - [agent.py (root)](#agentpy-root)
  - [src/agent.py](#srcagentpy)
- [Demo Scripts](#demo-scripts)
  - [scripts/demo_tools.py](#scriptsdemo_toolspy)

---

## Installation Scripts

### install.sh

**Location:** `/install.sh`

**Purpose:** Automated installation script for Linux and macOS systems.

**What it does:**
1. **Environment Validation:**
   - Checks if Python 3.8+ is installed
   - Verifies Git is installed
   - Validates Python version compatibility

2. **Virtual Environment Setup:**
   - Creates a Python virtual environment (`venv/`)
   - Activates the virtual environment
   - Upgrades pip to the latest version

3. **Dependency Installation:**
   - Installs all required Python packages from `requirements.txt`

4. **Configuration Setup:**
   - Creates a `.env` file from template if it doesn't exist
   - Sets up the `artifacts/` directory for agent outputs
   - Provides user with next steps and instructions

**Usage:**
```bash
chmod +x install.sh
./install.sh
```

**Output:**
- Creates `venv/` directory
- Creates `.env` file (if not exists)
- Creates `artifacts/` directory (if not exists)
- Displays setup completion message with next steps

---

### install.bat

**Location:** `/install.bat`

**Purpose:** Automated installation script for Windows systems.

**What it does:**
Similar to `install.sh` but designed for Windows Command Prompt:
1. Validates Python installation
2. Creates virtual environment
3. Installs dependencies
4. Sets up configuration files

**Usage:**
```cmd
install.bat
```

---

## Agent Scripts

### agent.py (root)

**Location:** `/agent.py`

**Purpose:** Convenience entrypoint wrapper that allows running the agent from the repository root.

**What it does:**
1. **Task Input Handling:**
   - Accepts task via command-line arguments
   - Falls back to `AGENT_TASK` environment variable
   - Uses a default task if neither is provided

2. **Agent Initialization:**
   - Imports and initializes the main `GeminiAgent` from `src/agent.py`
   - Ensures proper cleanup on exit

**Usage:**
```bash
# Run with command-line task
python agent.py "帮我写一个快速排序算法"

# Run with environment variable
export AGENT_TASK="Write a quick sort algorithm"
python agent.py

# Run with default task
python agent.py
```

**Why it exists:**
Provides convenience for users who want to run the agent from the project root without navigating to the `src/` directory.

---

### src/agent.py

**Location:** `/src/agent.py`

**Purpose:** Main AI agent implementation using Google Gemini with the Think-Act-Reflect pattern.

**What it does:**

#### 1. **GeminiAgent Class**
The core autonomous agent that integrates multiple capabilities:

**Initialization:**
- Loads configuration from environment variables
- Initializes memory management system
- Auto-discovers and loads tools from `src/tools/` directory
- Connects to MCP (Model Context Protocol) servers if enabled
- Sets up Google Gemini API client or OpenAI-compatible backend

**Key Features:**

##### Tool Discovery (`_load_tools`)
- Automatically scans `src/tools/` directory
- Imports all Python modules dynamically
- Registers public functions as available tools
- Enables "zero-config" tool integration - just drop a `.py` file in `src/tools/`

##### Context Loading (`_load_context`)
- Automatically loads markdown files from `.context/` directory
- Injects domain knowledge into agent's system prompt
- Supports project-specific coding standards and rules

##### MCP Integration (`_initialize_mcp`)
- Connects to external tool servers via Model Context Protocol
- Discovers and registers remote tools
- Makes MCP tools available alongside local tools
- Supports GitHub, databases, filesystems, and custom servers

##### Memory Management
- Maintains conversation history in JSON format
- Implements recursive summarization for infinite context
- Compresses older messages to stay within token limits
- Preserves decisions, intents, and outcomes

##### Think-Act-Reflect Loop

**Think Phase (`think`):**
- Analyzes the task
- Loads context knowledge
- Identifies necessary tools
- Formulates execution plan

**Act Phase (`act`):**
- Executes tasks using available tools
- Calls Gemini API or OpenAI-compatible backend
- Parses tool invocation requests
- Executes tools and processes results
- Generates final response with tool observations

**Reflect Phase (`reflect`):**
- Reviews past interactions
- Improves future performance

#### 2. **Backend Support**
- **Primary:** Google Gemini 2.0 Flash (via `genai` SDK)
- **Fallback:** OpenAI-compatible API (e.g., Ollama for local models)
- **Testing:** Dummy client for deterministic tests without API calls

#### 3. **Tool Execution**
Supports two invocation patterns:
- JSON format: `{"action": "tool_name", "args": {"param": "value"}}`
- Plain text: `Action: tool_name`

#### 4. **Artifact Generation**
All outputs and logs are saved to the `artifacts/` directory for:
- Audit trails
- Evidence preservation
- Debugging
- Future reference

**Usage:**
```bash
# Direct execution
python src/agent.py "Your task here"

# With environment variable
export AGENT_TASK="Your task"
python src/agent.py
```

**Configuration:**
Environment variables (via `.env` file):
- `GOOGLE_API_KEY` - Google Gemini API key
- `OPENAI_BASE_URL` - OpenAI-compatible endpoint (optional)
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `GEMINI_MODEL_NAME` - Model to use (default: gemini-2.0-flash-exp)
- `MCP_ENABLED` - Enable MCP integration (true/false)

**Architecture:**
```
User Task
    ↓
[Think] Analyze & Plan
    ↓
[Act] Execute with Tools
    ↓
Tool Invocation → Tool Execution → Observation
    ↓
[Reflect] Learn & Improve
    ↓
Result + Artifacts
```

---

## Demo Scripts

### scripts/demo_tools.py

**Location:** `/scripts/demo_tools.py`

**Purpose:** Example tool implementations to demonstrate the agent's tool system.

**What it does:**
Provides sample tools that showcase:
- How to write agent-compatible tools
- Tool documentation format
- Parameter handling
- Return value conventions

---

## How to Add New Scripts

### For Tools (Auto-discovered)
1. Create a new `.py` file in `src/tools/`
2. Define public functions with docstrings
3. Restart the agent - tools are auto-loaded

Example:
```python
# src/tools/my_tool.py
def analyze_sentiment(text: str) -> str:
    """Analyzes the sentiment of given text."""
    return "positive" if len(text) > 10 else "neutral"
```

### For Utilities
1. Create in `src/` directory
2. Import and use in agent code
3. Document in this file if it's user-facing

### For Automation
1. Add shell scripts to project root
2. Make executable: `chmod +x script.sh`
3. Document purpose and usage here

---

## Script Relationships

```
install.sh / install.bat
    ↓
Sets up environment
    ↓
agent.py (root) → src/agent.py
    ↓               ↓
User Interface   Core Logic
    ↓               ↓
    └───────────────┘
           ↓
    Loads Tools & Context
           ↓
    src/tools/*.py
    .context/*.md
           ↓
    Executes Task
           ↓
    artifacts/
```

---

## Testing Scripts

All test files are in the `tests/` directory:
- `test_agent.py` - Agent core functionality tests
- `test_execution_tool.py` - Tool execution tests
- `test_mcp.py` - MCP integration tests
- `test_memory.py` - Memory management tests
- `test_swarm.py` - Multi-agent swarm tests
- `conftest.py` - Pytest configuration and fixtures

**Run tests:**
```bash
pytest tests/
```

---

## Additional Resources

- **[Quick Start Guide](QUICK_START.md)** - Installation and setup
- **[Architecture Documentation](PHILOSOPHY.md)** - System design
- **[MCP Integration Guide](MCP_INTEGRATION.md)** - External tool setup
- **[README](../../README.md)** - Project overview
