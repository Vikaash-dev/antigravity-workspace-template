# 🚀 Quick Start - Research Paper AI

## Installation (One Command)

```bash
./install.sh
```

This installs:
- ✅ Python dependencies
- ✅ Context7 (code intelligence)
- ✅ Memory (graph memory)
- ✅ GitHub, Brave Search, Puppeteer MCPs
- ✅ Research workspace directories

## Configuration (2 Minutes)

Edit `.env`:
```bash
GOOGLE_API_KEY=your_gemini_key
GITHUB_TOKEN=ghp_your_token
BRAVE_API_KEY=your_brave_key
MCP_ENABLED=true
```

## Usage Examples

### Create Research Plan
```bash
python src/agent.py "Create research plan for: Efficient Neural Networks, deadline: 2024-12-31, type: conference"
```

### Literature Review
```bash
python src/agent.py "Search papers on transformer optimization and summarize top 5"
```

### Code Analysis
```bash
python src/agent.py "Analyze code quality of src/model.py"
```

### Cross-Analysis
```bash
python src/agent.py "Compare BERT vs GPT-2 on criteria: speed, accuracy, memory"
```

### Negative Analysis
```bash
python src/agent.py "Negative analysis: 'Larger models always perform better' with counterpoints"
```

### Generate Paper Outline
```bash
python src/agent.py "Generate outline for: Novel Pruning Techniques for CNNs"
```

### Check Progress
```bash
python src/agent.py "Show my research plan progress"
```

### Daily Tasks
```bash
python src/agent.py "What should I work on today?"
```

## Essential Tools

### Research Tools (`research_tools.py`)
- `analyze_paper_structure()` - Check paper completeness
- `cross_analyze_approaches()` - Compare approaches
- `negative_analysis()` - Critical evaluation
- `code_quality_assessment()` - Evaluate implementations
- `generate_paper_outline()` - Create structure
- `compare_code_implementations()` - Side-by-side comparison

### Planner (`planner_tool.py`)
- `create_research_plan()` - Full timeline (5 phases)
- `update_task_status()` - Track progress
- `get_plan_progress()` - Statistics
- `generate_daily_tasks()` - Daily recommendations

## MCPs Enabled by Default

| MCP | Purpose | Use For |
|-----|---------|---------|
| Context7 | Code intelligence | Imports, reviews, file analysis |
| Memory | Graph memory | Context, references, history |
| GitHub | Repo analysis | Code mining, issue tracking |
| Brave Search | Academic search | Paper discovery, literature review |
| Puppeteer | Web scraping | ArXiv, Scholar, metadata |
| Filesystem | File ops | Paper storage, artifacts |

## Directory Structure

```
artifacts/
  papers/          # Research papers
  analysis/        # Analysis results
  code_reviews/    # Code reviews
  plans/           # Research plans
.context/
  research/        # Research notes
  references/      # Citations
```

## Research Workflow (12 Weeks)

1. **Literature Review** (Weeks 1-2)
   - Search papers, extract citations, build knowledge base

2. **Methodology Design** (Weeks 3-5)
   - Design approach, plan experiments, setup repo

3. **Implementation** (Weeks 6-9)
   - Code, experiment, analyze, document

4. **Paper Writing** (Weeks 10-11)
   - Draft sections, create figures, add citations

5. **Review & Refinement** (Week 12)
   - Self-review, negative analysis, final polish

## Tips

✅ Start with `create_research_plan()` first
✅ Use Memory MCP to track everything
✅ Run `get_plan_progress()` weekly
✅ Perform `negative_analysis()` early
✅ Save artifacts frequently
✅ Let Context7 handle imports/reviews

## Help

📚 Full Guide: [RESEARCH_SETUP_GUIDE.md](RESEARCH_SETUP_GUIDE.md)
📖 Scripts: [SCRIPT_EXPLANATION.md](SCRIPT_EXPLANATION.md)
🌐 Docs: `docs/en/`

---

**Ready to write your research paper with AI! 🔬📝**
