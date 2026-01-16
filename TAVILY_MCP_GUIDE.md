# Tavily MCP Configuration Guide

## Overview

Tavily is an AI-powered search engine optimized for research and academic paper discovery. The `tavily-mcp` package provides MCP server integration for the Antigravity workspace.

## Installation

The installer automatically installs Tavily MCP:

```bash
# Linux/macOS
./install.sh

# Windows
install.bat
```

Manual installation:
```bash
npm install -g tavily-mcp
```

## Configuration

### API Key Setup

1. Get your free API key at: https://tavily.com
2. Add to `.env`:
```bash
TAVILY_API_KEY=tvly-your_api_key_here
```

### MCP Server Configuration

The Tavily MCP server is configured in `mcp_servers.json`:

```json
{
  "name": "tavily-search",
  "description": "Tavily AI-powered search for academic papers and research",
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "tavily-mcp"],
  "enabled": true,
  "env": {
    "TAVILY_API_KEY": "${TAVILY_API_KEY}"
  },
  "priority": "high",
  "use_cases": ["paper_search", "literature_review", "research_discovery", "ai_search"]
}
```

## Features

- **AI-Powered Search**: Advanced web search optimized for research
- **Academic Paper Discovery**: Find relevant research papers quickly
- **Real-Time Results**: Get up-to-date search results
- **Web Extraction**: Extract key information from web pages
- **Data Extraction**: Pull structured data from search results

## Usage

### Through Agent

```bash
# Search for academic papers
python src/agent.py "Search for papers on neural architecture search using Tavily"

# Literature review
python src/agent.py "Find recent publications on transformer models"

# Research discovery
python src/agent.py "Discover research on quantum computing applications"
```

### Direct Tool Usage

```python
from src.mcp_client import MCPManager

# Initialize MCP manager
mcp = MCPManager()

# Use Tavily search
results = mcp.call_tool("tavily-search", {
    "query": "neural architecture search",
    "max_results": 10
})
```

## Search Tips

1. **Be Specific**: Use detailed queries for better results
   - ❌ "machine learning"
   - ✅ "machine learning optimization techniques for deep neural networks"

2. **Use Filters**: Leverage search parameters
   - Time range: Recent publications
   - Source type: Academic papers, articles
   - Domain: arxiv.org, scholar.google.com

3. **Combine Searches**: Use multiple queries for comprehensive research
   ```python
   queries = [
       "neural architecture search survey",
       "NAS optimization methods 2024",
       "efficient architecture search"
   ]
   ```

4. **Extract Information**: Use Tavily's extraction capabilities
   - Paper metadata
   - Citations
   - Key findings

## Integration with Research Workflow

### Phase 1: Literature Review

```python
from src.tools.research_tools import save_research_artifact

# Search and save results
search_results = tavily_search("quantum machine learning")
save_research_artifact("reference", search_results, "quantum_ml_papers.json")
```

### Phase 2: Citation Management

```python
from src.tools.research_tools import extract_citations

# Extract citations from Tavily results
papers = tavily_search("transformer architectures")
citations = extract_citations(papers)
```

### Phase 3: Cross-Analysis

```python
from src.tools.research_tools import cross_analyze_approaches

# Compare different research approaches
results_a = tavily_search("approach A")
results_b = tavily_search("approach B")
analysis = cross_analyze_approaches(results_a, results_b, ["accuracy", "efficiency"])
```

## Troubleshooting

### API Key Issues

```bash
# Check if API key is set
echo $TAVILY_API_KEY  # Linux/macOS
echo %TAVILY_API_KEY%  # Windows

# Test API key
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{"api_key":"YOUR_KEY","query":"test"}'
```

### MCP Server Not Starting

1. **Verify installation**:
   ```bash
   npm list -g tavily-mcp
   ```

2. **Check Node.js version** (requires Node.js 14+):
   ```bash
   node --version
   ```

3. **Reinstall if needed**:
   ```bash
   npm uninstall -g tavily-mcp
   npm install -g tavily-mcp
   ```

### Rate Limits

Tavily API has rate limits based on your plan:
- **Free Tier**: 1,000 searches/month
- **Pro Tier**: Unlimited searches

If you hit rate limits:
- Wait for reset (monthly)
- Upgrade plan
- Use caching to reduce API calls

## Advanced Configuration

### Custom Search Parameters

Edit `mcp_servers.json` to add custom parameters:

```json
{
  "name": "tavily-search",
  "args": ["-y", "tavily-mcp", "--max-results", "20"],
  "env": {
    "TAVILY_API_KEY": "${TAVILY_API_KEY}",
    "TAVILY_SEARCH_DEPTH": "advanced",
    "TAVILY_INCLUDE_DOMAINS": "arxiv.org,scholar.google.com"
  }
}
```

### Multiple API Keys (Load Balancing)

For high-volume research, use `tavily-mcp-multikey`:

```bash
npm install -g tavily-mcp-multikey
```

Configure multiple keys in `.env`:
```bash
TAVILY_API_KEY_1=tvly-key1
TAVILY_API_KEY_2=tvly-key2
TAVILY_API_KEY_3=tvly-key3
```

## Best Practices

1. **Cache Results**: Save search results to avoid repeated API calls
   ```python
   save_research_artifact("reference", results, f"search_{timestamp}.json")
   ```

2. **Use Memory MCP**: Store frequently accessed search results
   ```python
   # Memory MCP automatically caches search results
   ```

3. **Combine with Google Search**: Use both Tavily and Google for comprehensive coverage
   ```python
   tavily_results = search_tavily(query)
   google_results = search_google(query)
   combined = merge_results(tavily_results, google_results)
   ```

4. **Monitor Usage**: Track API calls to stay within limits
   ```python
   # Check usage stats
   print(f"Searches used: {api_usage.get('searches_count')}")
   ```

## Resources

- **Tavily Website**: https://tavily.com
- **Tavily Documentation**: https://docs.tavily.com
- **MCP Package**: https://www.npmjs.com/package/tavily-mcp
- **API Reference**: https://docs.tavily.com/api-reference

## Support

- **Issues**: Open an issue in the repository
- **Tavily Support**: support@tavily.com
- **Community**: Join the Tavily Discord

---

**Quick Start**: Just run `./install.sh` or `install.bat` - Tavily MCP is configured automatically!
