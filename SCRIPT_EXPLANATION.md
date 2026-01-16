# Script Purpose Explanation

## Overview

This repository contains the **Antigravity Workspace Template** - a production-grade starter kit for building autonomous AI agents using Google Gemini (or OpenAI-compatible backends). The project provides a complete cognitive architecture for AI agents with infinite memory, auto-discovery of tools, and multi-agent coordination.

**✨ NEW: Enhanced with Research Paper AI capabilities** - This workspace is now supercharged with essential MCP servers (Context7, Graph Memory, GitHub, Brave Search) and specialized research tools for academic paper writing, code analysis, and literature review. See [RESEARCH_SETUP_GUIDE.md](RESEARCH_SETUP_GUIDE.md) for details.

---

## Main Scripts

### 1. `install.sh` - Installation Script (Linux/macOS)

**Location:** `/install.sh`

**Purpose:** Automates the setup of the development environment for the Antigravity workspace. **Now enhanced with essential MCP servers and research tools.**

**What it does:**
- ✅ **Checks prerequisites**: Verifies Python 3.8+, Git, and Node.js are installed
- ✅ **Creates virtual environment**: Sets up an isolated Python environment (`venv/`)
- ✅ **Installs dependencies**: Installs all required Python packages from `requirements.txt`
- ✅ **Configures environment**: Creates a `.env` file with API key placeholders
- ✅ **Creates directories**: Sets up the `artifacts/` directory for agent outputs
- ✨ **NEW: Installs MCP servers**: Automatically installs Context7, Memory, GitHub, Brave Search, Puppeteer, and Filesystem MCPs
- ✨ **NEW: Creates research directories**: Sets up `artifacts/papers/`, `artifacts/analysis/`, `.context/research/`, etc.

**Usage:**
```bash
chmod +x install.sh
./install.sh
```

**Output:** After completion, you'll have a fully configured development environment with essential MCP servers ready for AI-assisted research.

---

### 2. `agent.py` - Main Entry Point

**Location:** `/agent.py` (root directory)

**Purpose:** Convenience wrapper that allows you to run the agent from the project root directory.

**What it does:**
- Provides a simple command-line interface to the agent
- Accepts tasks via command-line arguments or the `AGENT_TASK` environment variable
- Delegates execution to the core agent implementation in `src/agent.py`
- Handles graceful shutdown of the agent

**Usage:**
```bash
# Run with a task as argument
python agent.py "Write a quicksort algorithm"

# Run with environment variable
export AGENT_TASK="Check today's weather"
python agent.py

# Default task if none provided
python agent.py  # Runs: "帮助我查看今天的天气" (Check today's weather)
```

---

### 3. `src/agent.py` - Core Agent Implementation

**Location:** `/src/agent.py`

**Purpose:** Contains the `GeminiAgent` class - the brain of the autonomous AI agent system.

**What it does:**

#### Core Capabilities:
1. **Think-Act-Reflect Loop**: Implements a cognitive architecture where the agent thinks, takes action, and reflects on results
2. **Infinite Memory**: Uses recursive summarization to compress context automatically (via `MemoryManager`)
3. **Tool Auto-Discovery**: Automatically discovers and loads Python functions from `src/tools/` directory
4. **MCP Integration**: Connects to Model Context Protocol (MCP) servers for external tools (GitHub, databases, filesystems)
5. **Multi-Backend Support**: 
   - Primary: Google Gemini API
   - Fallback: OpenAI-compatible endpoints (e.g., local Ollama)
6. **Artifact Generation**: Produces plans, logs, and evidence for every task

#### Key Features:
- **Dynamic Tool Loading**: Scans `src/tools/` and registers all Python functions as callable tools
- **Context Injection**: Auto-loads knowledge base from `.context/` directory
- **Swarm Coordination**: Supports multi-agent orchestration for complex tasks
- **Sandbox Execution**: Safely executes generated code (configurable: local, docker, or e2b)

#### Architecture:
```
GeminiAgent
├── Memory Management (agent_memory.json)
├── Tool Registry (local + MCP tools)
├── Context Loading (.context/ files)
├── LLM Client (Gemini or OpenAI-compatible)
└── Execution Loop (Think → Act → Reflect)
```

---

## Other Important Scripts

### 4. `scripts/demo_tools.py`

**Purpose:** Contains demonstration tools that showcase how to add custom capabilities to the agent.

### 5. Test Files (`tests/*.py`)

**Purpose:** Unit tests for various components:
- `test_agent.py` - Tests the core agent functionality
- `test_execution_tool.py` - Tests code execution capabilities
- `test_mcp.py` - Tests MCP integration
- `test_swarm.py` - Tests multi-agent coordination
- `test_memory.py` - Tests memory management

### 6. Research Tools (`src/tools/research_tools.py`) ✨ NEW

**Purpose:** Specialized tools for academic research and paper writing:
- `analyze_paper_structure()` - Analyzes research paper completeness
- `cross_analyze_approaches()` - Compares different research approaches
- `negative_analysis()` - Critical evaluation and counterargument analysis
- `code_quality_assessment()` - Evaluates research implementation quality
- `generate_paper_outline()` - Creates structured academic paper outlines
- `compare_code_implementations()` - Side-by-side code comparison

### 7. Planner Tool (`src/tools/planner_tool.py`) ✨ NEW

**Purpose:** Research workflow and project management:
- `create_research_plan()` - Creates timeline with 5 phases (Literature Review → Writing)
- `update_task_status()` - Tracks progress on research tasks
- `get_plan_progress()` - Calculates completion percentages
- `generate_daily_tasks()` - Recommends daily priorities

---

## How It All Works Together

### Workflow:
1. **Setup**: Run `install.sh` to configure the environment
2. **Configuration**: Edit `.env` to add API keys
3. **Execution**: Run `python agent.py "your task"` to start the agent
4. **Processing**:
   - Agent loads tools from `src/tools/`
   - Connects to MCP servers (if configured)
   - Loads context from `.context/`
   - Executes the think-act-reflect loop
   - Saves outputs to `artifacts/`

### Example Task Flow:
```
User → agent.py → src/agent.py → GeminiAgent
                                      ↓
                              ┌───────┴────────┐
                              │                │
                         Load Tools      Load Context
                              │                │
                         src/tools/      .context/
                              │                │
                              └───────┬────────┘
                                      ↓
                              Execute Task
                                      ↓
                              Save Artifacts
                                      ↓
                              artifacts/
```

---

## Key Design Principles

1. **Zero-Config Philosophy**: Minimize setup - "Clone → Rename → Prompt"
2. **Convention Over Configuration**: Smart defaults reduce boilerplate
3. **IDE as Teammate**: Context-aware rules (`.cursorrules`, `.antigravity/rules.md`) turn the IDE into an architect
4. **Explicit Intent**: Capture architecture in files, not tribal knowledge
5. **Minimal Repetition**: Encode defaults so setup is nearly zero

---

## Quick Reference

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `install.sh` | Environment setup | First time setup or after cloning |
| `agent.py` | Run the agent | Every time you want to execute a task |
| `src/agent.py` | Core logic | Extend functionality or understand internals |

---

## Getting Help

- **Documentation**: See `/docs/en/` for comprehensive guides
- **Quick Start**: `docs/en/QUICK_START.md`
- **Philosophy**: `docs/en/PHILOSOPHY.md`
- **Issues**: https://github.com/study8677/antigravity-workspace-template/issues

---

## Summary

The scripts in this repository form a **complete AI agent framework** enhanced for research:
- `install.sh` sets up your environment **with essential MCP servers**
- `agent.py` provides the entry point
- `src/agent.py` implements the intelligent agent with memory, tools, and multi-agent capabilities
- **NEW:** `research_tools.py` provides academic research and paper writing tools
- **NEW:** `planner_tool.py` manages research timelines and task planning

The goal is to make building production-grade AI agents as simple as **Clone → Configure → Prompt**, with specialized support for **academic research and paper writing workflows**.

---

## 🔬 Research Paper AI Features

This workspace is now optimized for **AI-assisted research paper writing**:

### Essential MCP Servers (Auto-installed)
- **Context7**: Code intelligence for imports and file reviews
- **Memory**: Graph-based memory for research context
- **GitHub**: Repository analysis and code mining
- **Brave Search**: Academic paper discovery
- **Puppeteer**: Web scraping for research papers
- **Filesystem**: Organized artifact storage

### Research Workflow Support
1. **Literature Review**: Search, scrape, and organize academic papers
2. **Code Analysis**: Quality assessment and implementation comparison
3. **Cross-Analysis**: Compare research approaches systematically
4. **Negative Analysis**: Critical evaluation and weakness identification
5. **Paper Writing**: Structured outlines and progress tracking
6. **Planning**: 5-phase research timeline with milestone tracking

### Quick Start for Research
```bash
# 1. Run enhanced installer
./install.sh

# 2. Configure API keys in .env
nano .env  # Add GOOGLE_API_KEY, GITHUB_TOKEN, BRAVE_API_KEY

# 3. Create research plan
python src/agent.py "Create research plan for: [your topic], deadline: 2024-12-31"

# 4. Start researching
python src/agent.py "Search papers on neural architecture search"
```

📚 **See [RESEARCH_SETUP_GUIDE.md](RESEARCH_SETUP_GUIDE.md) for complete documentation.**
