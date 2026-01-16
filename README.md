# 🪐 Google Antigravity Workspace Template

**The Ultimate Autonomous AI Research & Coding Platform** - From research papers to production code in minutes, with 100+ integrated AI tools and MCP servers.

Language: [English](/docs/en/) | [中文（仓库主页）](README_CN.md) | [中文文档](/docs/zh/) | [Español](/docs/es/)

![License](https://img.shields.io/badge/License-MIT-green)
![Gemini](https://img.shields.io/badge/AI-Gemini_2.0_Flash-blue)
![Architecture](https://img.shields.io/badge/Architecture-Event_Driven-purple)
![Memory](https://img.shields.io/badge/Context-Infinite-orange)
![MCPs](https://img.shields.io/badge/MCP_Servers-100+-red)
![AI_Tools](https://img.shields.io/badge/AI_Tools-Integrated-yellow)

## 🚀 What's New

- **🧠 Self-Reflection & Self-Review**: Agents that think about their thinking and iteratively improve
- **🔬 Multi-Approach Research**: 7 research methodologies working in parallel, aggregated into superior papers
- **💻 DeepCode Integration**: Paper2Code, Text2Web, Text2Backend (13,888⭐)
- **⚡ Vibe Coding Engine**: Context-aware AI coding with Context7 (42,101⭐)
- **📦 100+ MCP Servers**: Auto-tool selection from awesome-mcp-servers (78,962⭐)
- **🤖 AI Agent Orchestrator**: Automatically selects best tools for any task
- **🌐 Unified Antigravity API**: ONE KEY for Gemini, Claude Opus 4.5, OpenAI, and all MCPs
- **🔄 Agent Context Protocol (ACP)**: Multi-agent coordination and autonomous workflows

## 🌟 Project Intent

In a world full of AI IDEs, I want enterprise-grade architecture to be as simple as **Clone → Configure → Prompt**.

This project is now the **most comprehensive autonomous research and coding platform**, combining:
- Google Antigravity's cognitive architecture
- 100+ integrated MCP servers
- Paper2Code, Text2Web, Text2Backend capabilities  
- Multi-methodology research with self-reflection
- Vibe coding with semantic code search
- Unified API management

When you open this project, your IDE becomes an **industry-savvy architect** with access to **every AI tool imaginable**.

**First principles:**

- Minimize repetition: the repo should encode defaults so setup is nearly zero.
- Make intent explicit: capture architecture, context, and workflows in files, not tribal knowledge.
- Treat the IDE as a teammate: contextual rules turn the editor into a proactive architect, not a passive tool.
- **Maximize capability**: Integrate best tools so you have superhuman abilities out of the box.
- **Automate everything**: From research to production code, fully autonomous.

### Why do we need a thinking scaffold?

While building with Google Antigravity or Cursor, I found a pain point:

**The IDE and models are powerful, but the empty project is too weak.**

Every new project repeats the same boring setup:

- "Should my code live in `src` or `app`?"
- "How do I define utilities so Gemini recognizes them?"
- "How do I help the AI remember prior context?"
- **"How do I convert research papers to code?"**
- **"How do I coordinate multiple AI agents?"**
- **"Which MCP servers should I use?"**

This repetition wastes creative energy. My ideal workflow is: **after a git clone, the IDE already knows what to do AND has every tool available.**

So I built this project: **Antigravity Workspace Template** - now with **100+ integrated AI tools and MCP servers**.

## ⚡ Quick Start

### Automated Installation (Recommended)

**Linux / macOS:**
```bash
# 1. Clone the template
git clone https://github.com/study8677/antigravity-workspace-template.git my-project
cd my-project

# 2. Run the installer
chmod +x install.sh
./install.sh

# 3. Configure your API keys
nano .env

# 4. Run the agent
source venv/bin/activate
python src/agent.py
```

**Windows:**
```cmd
# 1. Clone the template
git clone https://github.com/study8677/antigravity-workspace-template.git my-project
cd my-project

# 2. Run the installer
install.bat

# 3. Configure your API keys (notepad .env)

# 4. Run the agent
python src/agent.py
```

### Manual Installation

```bash
# 1. Clone the template
git clone https://github.com/study8677/antigravity-workspace-template.git my-project
cd my-project

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API keys
cp .env.example .env  # (if available) or create .env manually
nano .env

# 5. Run the agent
python src/agent.py
```

**That's it!** The IDE auto-loads configuration via `.cursorrules` + `.antigravity/rules.md`. You're ready to prompt.

## 🎯 What Is This?

This is **not** another LangChain wrapper. It's a minimal, transparent workspace for building AI agents that:

- 🧠 Have infinite memory (recursive summarization)
- 🛠️ Auto-discover tools from `src/tools/`
- 📚 Auto-inject context from `.context/`
- 🔌 Connect to MCP servers seamlessly
- 🤖 Coordinate multiple specialist agents
- 📦 Save outputs as artifacts (plans, logs, evidence)

**Clone → Rename → Prompt. That's the workflow.**

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Infinite Memory** | Recursive summarization compresses context automatically |
| 🛠️ **Universal Tools** | Drop Python functions in `src/tools/` → auto-discovered |
| 📚 **Auto Context** | Add files to `.context/` → auto-injected into prompts |
| 🔌 **MCP Support** | Connect GitHub, databases, filesystems, custom servers |
| 🤖 **Swarm Agents** | Multi-agent orchestration with Router-Worker pattern |
| ⚡ **Gemini Native** | Optimized for Gemini 2.0 Flash |
| 🌐 **LLM Agnostic** | Use OpenAI, Azure, Ollama, or any OpenAI-compatible API |
| 📂 **Artifact-First** | Every task produces plans, logs, and evidence |
| 🔒 **Sandbox Execution** | Configurable code execution environments (local by default) |

## 📚 Documentation

**Full documentation available in `/docs/en/`:**

- **[Quick Start](docs/en/QUICK_START.md)** — Installation & deployment
- **[Philosophy](docs/en/PHILOSOPHY.md)** — Core concepts & architecture
- **[Zero-Config](docs/en/ZERO_CONFIG.md)** — Auto tool & context loading
- **[MCP Integration](docs/en/MCP_INTEGRATION.md)** — External tool connectivity
- **[Swarm Protocol](docs/en/SWARM_PROTOCOL.md)** — Multi-agent coordination
- **[Roadmap](docs/en/ROADMAP.md)** — Future phases & vision

### Sandbox Configuration (Zero-Config by default)

The sandbox lets the agent execute generated Python code safely and consistently. It defaults to a local subprocess with isolation and limits.

- `SANDBOX_TYPE`: `local` (default) | `docker` (opt-in) | `e2b` (future)
- `SANDBOX_TIMEOUT_SEC`: maximum execution time in seconds (default `30`)
- `SANDBOX_MAX_OUTPUT_KB`: truncate stdout/stderr to limit size (default `10`)

Docker (opt-in) extra variables:
- `DOCKER_IMAGE` (default `python:3.11-slim`)
- `DOCKER_NETWORK_ENABLED` (`false` by default)
- `DOCKER_CPU_LIMIT` (default `0.5` cores)
- `DOCKER_MEMORY_LIMIT` (default `256m`)

Example:

```bash
export SANDBOX_TYPE=local
export SANDBOX_TIMEOUT_SEC=30
export SANDBOX_MAX_OUTPUT_KB=10
# Docker mode
# export SANDBOX_TYPE=docker
# export DOCKER_IMAGE=python:3.11-slim
# export DOCKER_NETWORK_ENABLED=false
# export DOCKER_CPU_LIMIT=0.5
# export DOCKER_MEMORY_LIMIT=256m
```

## 🏗️ Project Structure

```
src/
├── agent.py           # Main agent loop
├── memory.py          # JSON memory manager
├── mcp_client.py      # MCP integration
├── swarm.py           # Multi-agent orchestration
├── agents/            # Specialist agents
└── tools/             # Your custom tools

.context/             # Knowledge base (auto-injected)
.antigravity/         # Antigravity rules
artifacts/            # Outputs & evidence
```

## 💡 Example: Build a Tool in 30 Seconds

```python
# src/tools/my_tool.py
def analyze_sentiment(text: str) -> str:
    """Analyzes the sentiment of given text."""
    return "positive" if len(text) > 10 else "neutral"
```

**Restart agent.** Done! The tool is now available.

## 🔌 MCP Integration

Connect to external tools:

```json
{
  "servers": [
    {
      "name": "github",
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "enabled": true
    }
  ]
}
```

Agent automatically discovers and uses all MCP tools.

## 🤖 Multi-Agent Swarm

Decompose complex tasks:

```python
from src.swarm import SwarmOrchestrator

swarm = SwarmOrchestrator()
result = swarm.execute("Build and review a calculator")
```

The swarm automatically:
- 📤 Routes to Coder, Reviewer, Researcher agents
- 🧩 Synthesizes results
- 📂 Saves artifacts

## ✅ What's Complete

- ✅ Phase 1-7: Foundation, DevOps, Memory, Tools, Swarm, Discovery
- ✅ Phase 8: MCP Integration (fully implemented)
- 🚀 Phase 9: Enterprise Core (in progress)

## 🆕 Recent Updates

- Added local OpenAI-compatible backend support (e.g., Ollama) when no Google API key is provided.
- Fixed `.env` loading so runs from the `src/` folder still read the project-root config.
- Default `.env` now points to local backend placeholders instead of a hardcoded Google key.
- CLI entrypoints (`agent.py` and `src/agent.py`) now accept tasks via arguments or `AGENT_TASK`, instead of a fixed demo task.

See [Roadmap](docs/en/ROADMAP.md) for details.

## 🤝 Contributing

Ideas are contributions too! Open an [issue](https://github.com/study8677/antigravity-workspace-template/issues) to:
- Report bugs
- Suggest features
- Propose architecture (Phase 9)

Or submit a PR to improve docs or code.

## 👥 Contributors

- [@devalexanderdaza](https://github.com/devalexanderdaza) — First contributor. Implemented demo tools, enhanced agent functionality, proposed the "Agent OS" roadmap, and completed MCP integration.
- [@Subham-KRLX](https://github.com/Subham-KRLX) — Added dynamic tools and context loading (Fixes #4) and the multi-agent cluster protocol (Fixes #6).

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=study8677/antigravity-workspace-template&type=Date)](https://star-history.com/#study8677/antigravity-workspace-template&Date)

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

**[Explore Full Documentation →](docs/en/)**
