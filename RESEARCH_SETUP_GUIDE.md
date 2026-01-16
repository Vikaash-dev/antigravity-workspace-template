# 🔬 Research Paper AI - Setup Guide

## Overview

This enhanced setup transforms the Antigravity Workspace into a powerful AI research assistant optimized for academic paper writing, code analysis, and literature review.

## 🎯 Use Case

**Target Workflow:** Writing research papers using AI for:
- Code improvement and bug fixing
- Creating research papers on specific topics
- Cross-analysis of different approaches
- Negative analysis and critical evaluation
- Literature review and citation management

## 🚀 Essential MCPs Installed

### 1. **Context7** - Code Intelligence
- **Purpose:** Retrieves code context, suggests imports, assists with file reviews
- **Use Cases:**
  - Automatic import suggestions when writing code
  - Code review and quality assessment
  - File structure analysis
  - Dependency resolution
- **Configuration:** `mcp_servers.json` - enabled by default
- **Requires:** Node.js (installed automatically)

### 2. **Memory** - Graph Memory
- **Purpose:** Persistent context storage with graph-based relationships
- **Use Cases:**
  - Store research paper references
  - Maintain analysis history
  - Link related concepts and findings
  - Remember previous discussions and decisions
- **Configuration:** `mcp_servers.json` - enabled by default
- **Storage:** Automatic graph-based memory management

### 3. **Filesystem** - File Operations
- **Purpose:** Advanced file system access for papers and code
- **Use Cases:**
  - Store research papers in organized structure
  - Manage code artifacts
  - Read/write analysis results
- **Configuration:** Points to project root directory
- **Directories:**
  - `artifacts/papers/` - Research papers
  - `artifacts/analysis/` - Analysis results
  - `artifacts/code_reviews/` - Code review outputs
  - `.context/research/` - Research notes
  - `.context/references/` - Paper references

### 4. **GitHub** - Repository Analysis
- **Purpose:** Access GitHub repositories for code mining and analysis
- **Use Cases:**
  - Analyze implementation patterns
  - Mine code repositories for research
  - Track issues and discussions
  - Cross-reference implementations
- **Configuration:** Requires `GITHUB_TOKEN` in `.env`
- **Scopes Required:** `repo`, `read:org`

### 5. **Brave Search** - Academic Search
- **Purpose:** Search for academic papers and research literature
- **Use Cases:**
  - Find relevant papers on research topics
  - Discover recent publications
  - Literature review automation
  - Citation discovery
- **Configuration:** Requires `BRAVE_API_KEY` in `.env`
- **Free Tier:** Available at https://brave.com/search/api/

### 6. **Puppeteer** - Web Scraping
- **Purpose:** Scrape research papers from ArXiv, Google Scholar, etc.
- **Use Cases:**
  - Extract paper metadata
  - Download paper PDFs
  - Collect citation information
  - Scrape author profiles
- **Configuration:** `mcp_servers.json` - enabled by default
- **Note:** Respect robots.txt and rate limits

## 🛠️ Research-Specific Tools

### Research Tools (`src/tools/research_tools.py`)

1. **`analyze_paper_structure(paper_text)`**
   - Analyzes research paper structure
   - Checks for required sections
   - Estimates completeness

2. **`cross_analyze_approaches(approach_a, approach_b, criteria)`**
   - Compares two research approaches
   - Evaluates against custom criteria
   - Generates comparative analysis

3. **`negative_analysis(hypothesis, counterpoints)`**
   - Performs critical evaluation
   - Assesses counterarguments
   - Identifies weaknesses and risks

4. **`code_quality_assessment(code, language)`**
   - Evaluates code quality for research implementations
   - Measures documentation, complexity
   - Best practices compliance

5. **`save_research_artifact(artifact_type, content, filename)`**
   - Saves research outputs to organized directories
   - Types: paper, analysis, review, data, reference

6. **`extract_citations(text)`**
   - Extracts citations from research text
   - Identifies inline and reference citations
   - Provides line numbers for review

7. **`generate_paper_outline(title, research_question, methodology)`**
   - Creates structured paper outline
   - Standard academic sections
   - Content guides for each section

8. **`compare_code_implementations(impl_a, impl_b, criteria)`**
   - Compares two code implementations
   - Side-by-side quality metrics
   - Recommendations for improvement

### Planner Tool (`src/tools/planner_tool.py`)

1. **`create_research_plan(topic, deadline, paper_type)`**
   - Creates comprehensive research timeline
   - 5 phases: Literature Review → Methodology → Implementation → Writing → Review
   - Milestone tracking and task management

2. **`update_task_status(plan, phase, task_index, status)`**
   - Updates task progress
   - Statuses: pending, in_progress, completed, blocked

3. **`get_plan_progress(plan)`**
   - Calculates overall progress
   - Per-phase completion statistics
   - Timeline adherence check

4. **`generate_daily_tasks(plan)`**
   - Recommends daily tasks
   - Prioritizes based on timeline
   - Helps maintain momentum

5. **`save_plan_artifact(plan)` / `load_latest_plan()`**
   - Persist and retrieve research plans
   - Stored in `artifacts/plans/`

## 📁 Directory Structure

```
antigravity-workspace-template/
├── artifacts/
│   ├── papers/          # Final research papers
│   ├── analysis/        # Analysis results and data
│   ├── code_reviews/    # Code review outputs
│   └── plans/           # Research plans and timelines
├── .context/
│   ├── research/        # Research notes and context
│   └── references/      # Paper references and citations
├── src/
│   └── tools/
│       ├── research_tools.py   # Research analysis tools
│       └── planner_tool.py     # Research planning tools
└── mcp_servers.json     # MCP server configuration
```

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# AI Model
GOOGLE_API_KEY=your_gemini_api_key

# MCP Servers
GITHUB_TOKEN=ghp_your_token              # GitHub access
BRAVE_API_KEY=your_brave_api_key         # Academic search

# Optional
DATABASE_URL=postgresql://...            # For data storage
SLACK_BOT_TOKEN=xoxb-...                # Team collaboration

# Agent Settings
MCP_ENABLED=true
AGENT_NAME=ResearchAssistant
```

### MCP Server Configuration (`mcp_servers.json`)

All essential servers are **enabled by default**:
- ✅ Context7 (code intelligence)
- ✅ Memory (graph memory)
- ✅ Filesystem (file operations)
- ✅ GitHub (repository analysis)
- ✅ Brave Search (academic search)
- ✅ Puppeteer (web scraping)

## 📝 Usage Examples

### 1. Create Research Plan

```bash
python src/agent.py "Create a research plan for: Neural Architecture Search optimization, deadline: 2024-06-30, type: conference"
```

### 2. Literature Review

```bash
python src/agent.py "Search for papers on transformer architectures and summarize key findings"
```

### 3. Code Analysis

```bash
python src/agent.py "Analyze the code quality of implementation_a.py and compare with implementation_b.py"
```

### 4. Cross-Analysis

```bash
python src/agent.py "Compare BERT vs GPT approaches for text classification using criteria: accuracy, efficiency, interpretability"
```

### 5. Negative Analysis

```bash
python src/agent.py "Perform negative analysis on hypothesis: 'Deep learning always outperforms traditional ML' with counterpoints from recent papers"
```

### 6. Paper Writing

```bash
python src/agent.py "Generate outline for paper: Efficient Neural Network Pruning with research question: How can we reduce model size without accuracy loss?"
```

### 7. Daily Tasks

```bash
python src/agent.py "Show my daily research tasks based on current plan"
```

## 🎓 Research Workflow

### Phase 1: Literature Review (Weeks 1-2)
```bash
# Search papers
python src/agent.py "Search recent papers on [topic]"

# Analyze structure
python src/agent.py "Analyze structure of paper.pdf"

# Extract citations
python src/agent.py "Extract citations from literature_review.txt"
```

### Phase 2: Methodology Design (Weeks 3-5)
```bash
# Create plan
python src/agent.py "Create research plan for [topic]"

# Design approach
python src/agent.py "Design methodology for [research question]"
```

### Phase 3: Implementation (Weeks 6-9)
```bash
# Code quality check
python src/agent.py "Review code quality of implementation.py"

# Compare implementations
python src/agent.py "Compare my_approach.py vs baseline.py"
```

### Phase 4: Analysis & Writing (Weeks 10-11)
```bash
# Cross-analysis
python src/agent.py "Cross-analyze approach A vs approach B on metrics: speed, accuracy, memory"

# Negative analysis
python src/agent.py "Negative analysis of my hypothesis with counterpoints"

# Generate outline
python src/agent.py "Generate paper outline for [title]"
```

### Phase 5: Review & Refinement (Week 12)
```bash
# Structure check
python src/agent.py "Analyze paper structure of draft_paper.txt"

# Progress check
python src/agent.py "Show research plan progress"
```

## 🔬 Advanced Features

### Graph Memory Integration

Memory MCP automatically stores:
- Research paper references
- Analysis history
- Code review results
- Relationships between concepts

Query memory:
```bash
python src/agent.py "What papers have I reviewed on topic X?"
python src/agent.py "Show my analysis history for approach Y"
```

### Context7 Code Intelligence

Automatic features:
- Import suggestions when writing code
- File structure understanding
- Dependency resolution
- Code review assistance

### Brave Search Integration

Enhanced search:
- Academic paper discovery
- Recent publication tracking
- Citation network exploration
- Author research

## 🚨 Troubleshooting

### MCP Servers Not Starting

1. Check Node.js installation: `node --version`
2. Verify `mcp_servers.json` syntax
3. Check API keys in `.env`
4. View logs: `artifacts/logs/mcp_*.log`

### Context7 Issues

```bash
# Reinstall globally
npm install -g @context7/mcp-server

# Or use npx (no global install)
# Already configured in mcp_servers.json
```

### Memory Graph Issues

Memory is stored locally. To reset:
```bash
rm -rf ~/.mcp/memory
```

### API Rate Limits

- **GitHub:** 5,000 requests/hour (authenticated)
- **Brave Search:** Varies by plan (free tier available)
- Use caching and respect rate limits

## 📚 Additional Resources

- [MCP Integration Guide](docs/en/MCP_INTEGRATION.md)
- [Swarm Protocol](docs/en/SWARM_PROTOCOL.md)
- [Philosophy & Architecture](docs/en/PHILOSOPHY.md)
- [Context7 Documentation](https://context7.dev)
- [Brave Search API](https://brave.com/search/api/)

## 🎯 Best Practices

1. **Start with a plan**: Use `create_research_plan()` before diving in
2. **Document as you go**: Use `save_research_artifact()` frequently
3. **Track progress**: Run `get_plan_progress()` weekly
4. **Use graph memory**: Let Memory MCP track relationships
5. **Regular reviews**: Perform negative analysis early and often
6. **Organize files**: Use the artifacts directory structure
7. **Version control**: Commit research artifacts and code together

## 🌟 Tips for Research Paper Writing

1. **Literature Review**: Use Brave Search + Memory to build comprehensive literature map
2. **Code Analysis**: Use Context7 + code quality tools for implementation sections
3. **Cross-Analysis**: Compare your approach with baselines systematically
4. **Negative Analysis**: Identify weaknesses before reviewers do
5. **Citations**: Extract and organize citations early
6. **Incremental Writing**: Write sections as you complete corresponding research phases

## 📞 Support

Issues or questions? Open an issue at:
https://github.com/study8677/antigravity-workspace-template/issues

Include:
- OS and versions (Python, Node.js)
- Error messages
- Configuration files (sanitized)
- Steps to reproduce

---

**Happy Researching! 🚀📚**
