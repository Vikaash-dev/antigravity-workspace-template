"""
Vibe Coding Integration - Context-aware AI coding
Integrates Context7 and vibe-coding concepts for intelligent development
GitHub: https://github.com/upstash/context7 (42,101 stars)
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

class VibeCodingEngine:
    """
    Vibe coding engine with semantic code search and context understanding
    """
    
    def __init__(self, api_gateway=None):
        self.api_gateway = api_gateway
        self.context_cache = {}
        self.code_embeddings = {}
        
    async def get_code_context(self, query: str, codebase_path: str) -> Dict[str, Any]:
        """
        Get relevant code context for a query using semantic search
        
        Args:
            query: What the developer wants to do
            codebase_path: Path to codebase
            
        Returns:
            Relevant code snippets and context
        """
        # Search for relevant files
        relevant_files = await self._semantic_code_search(query, codebase_path)
        
        context = {
            "query": query,
            "relevant_files": relevant_files,
            "imports_needed": await self._suggest_imports(query, relevant_files),
            "patterns_found": await self._find_patterns(relevant_files),
            "documentation": await self._get_relevant_docs(query)
        }
        
        return context
    
    async def _semantic_code_search(self, query: str, codebase_path: str) -> List[Dict]:
        """
        Perform semantic search over codebase
        """
        codebase = Path(codebase_path)
        if not codebase.exists():
            return []
        
        results = []
        for file_path in codebase.rglob("*.py"):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Simple relevance scoring (in production, use embeddings)
                score = 0
                query_terms = query.lower().split()
                for term in query_terms:
                    if term in content.lower():
                        score += content.lower().count(term)
                
                if score > 0:
                    results.append({
                        "path": str(file_path),
                        "relevance_score": score,
                        "content": content[:500]  # Preview
                    })
            except (IOError, UnicodeDecodeError):
                continue
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:10]  # Top 10 results
    
    async def _suggest_imports(self, query: str, relevant_files: List[Dict]) -> List[str]:
        """
        Suggest imports based on query and relevant files
        """
        prompt = f"""Based on this coding task and relevant code, suggest necessary imports:

Task: {query}

Relevant Code:
{json.dumps(relevant_files[:3], indent=2)}

List Python imports needed (one per line, no explanation):"""

        if self.api_gateway:
            response = await self.api_gateway.generate(
                prompt=prompt,
                model_tier="fast",
                task_type="code_analysis"
            )
        else:
            response = {"content": "import os\nimport json"}
        
        imports = response.get("content", "").strip().split("\n")
        return [imp.strip() for imp in imports if imp.strip().startswith("import") or imp.strip().startswith("from")]
    
    async def _find_patterns(self, relevant_files: List[Dict]) -> List[str]:
        """
        Find common patterns in relevant files
        """
        patterns = []
        
        for file_info in relevant_files[:5]:
            content = file_info.get("content", "")
            
            # Detect patterns
            if "async def" in content:
                patterns.append("async_functions")
            if "class " in content and "(BaseModel)" in content:
                patterns.append("pydantic_models")
            if "@app.route" in content or "@router." in content:
                patterns.append("api_endpoints")
            if "def test_" in content:
                patterns.append("unit_tests")
        
        return list(set(patterns))
    
    async def _get_relevant_docs(self, query: str) -> str:
        """
        Get relevant documentation for the query
        """
        # This would integrate with documentation search
        # For now, return placeholder
        return f"Documentation relevant to: {query}"
    
    async def vibe_code(self, intention: str, context_files: List[str] = None) -> str:
        """
        Generate code based on intention with full context awareness
        
        Args:
            intention: What you want the code to do
            context_files: Files to use as context
            
        Returns:
            Generated code
        """
        # Get context
        context = await self.get_code_context(intention, ".")
        
        prompt = f"""You are an expert developer with vibe coding superpowers.

Developer Intention: {intention}

Code Context:
{json.dumps(context, indent=2)}

Context Files:
{context_files}

Generate production-ready code that:
1. Matches the developer's intention perfectly
2. Uses patterns found in the codebase
3. Includes necessary imports
4. Follows project conventions
5. Is clean and maintainable

Return only the code, no explanations."""

        if self.api_gateway:
            response = await self.api_gateway.generate(
                prompt=prompt,
                model_tier="powerful",
                task_type="vibe_coding"
            )
        else:
            response = {"content": "# Generated code placeholder"}
        
        return response.get("content", "")
    
    async def review_with_context(self, code: str, file_path: str) -> Dict[str, Any]:
        """
        Review code with full project context
        
        Args:
            code: Code to review
            file_path: Path of the file
            
        Returns:
            Review results with suggestions
        """
        context = await self.get_code_context(f"reviewing {file_path}", ".")
        
        prompt = f"""Review this code with full project context:

Code:
{code}

File: {file_path}

Project Context:
{json.dumps(context, indent=2)}

Provide:
1. Issues found (bugs, security, performance)
2. Style consistency with project
3. Missing imports or dependencies
4. Suggested improvements
5. Overall quality score (0-10)

Format as JSON."""

        if self.api_gateway:
            response = await self.api_gateway.generate(
                prompt=prompt,
                model_tier="balanced",
                task_type="code_review"
            )
        else:
            response = {"content": "{}"}
        
        try:
            return json.loads(response.get("content", "{}"))
        except (json.JSONDecodeError, ValueError):
            return {"issues": [], "quality_score": 7}


class Context7Integration:
    """
    Integration with Context7 MCP server for real-time code intelligence
    """
    
    def __init__(self):
        self.enabled = os.getenv("CONTEXT7_ENABLED", "true").lower() == "true"
        self.api_key = os.getenv("CONTEXT7_API_KEY", "")
        
    async def get_documentation(self, library: str, method: str = None) -> str:
        """
        Get up-to-date documentation from Context7
        """
        if not self.enabled:
            return ""
        
        # This would call Context7 MCP server
        # For now, return placeholder
        query = f"{library}.{method}" if method else library
        return f"Documentation for {query}: [Context7 would provide real-time docs here]"
    
    async def suggest_code_completion(self, context: str, cursor_position: int) -> List[str]:
        """
        Suggest code completions based on context
        """
        if not self.enabled:
            return []
        
        # This would call Context7 MCP server
        return ["suggestion1", "suggestion2", "suggestion3"]


# Export for use in other modules
__all__ = ['VibeCodingEngine', 'Context7Integration']
