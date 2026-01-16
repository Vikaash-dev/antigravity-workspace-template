"""
Integrations Package - External AI Tools and MCP Servers

This package provides integrations with:
- DeepCode: Paper2Code, Text2Web, Text2Backend (13,888⭐)
- Vibe Coding: Context-aware AI coding with Context7 (42,101⭐)
- Awesome MCP Servers: 100+ MCP integrations (78,962⭐)
- AI Coding Tools: TabbyML, Cherry Studio, Onlook, OpenSpec
"""

from .deepcode_integration import DeepCodeAgent
from .vibe_coding_integration import VibeCodingEngine, Context7Integration
from .awesome_integrations import MCPRegistry, AIAgentOrchestrator, RECOMMENDED_MCP_SERVERS, AI_CODING_TOOLS

__all__ = [
    'DeepCodeAgent',
    'VibeCodingEngine',
    'Context7Integration',
    'MCPRegistry',
    'AIAgentOrchestrator',
    'RECOMMENDED_MCP_SERVERS',
    'AI_CODING_TOOLS'
]
