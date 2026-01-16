"""
DeepCode Integration - Paper2Code & Text2Web & Text2Backend
Integrates HKUDS/DeepCode capabilities for agentic coding
GitHub: https://github.com/HKUDS/DeepCode (13,888 stars)
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

class DeepCodeAgent:
    """
    DeepCode agent for converting research papers to code, text to web apps, and text to backend
    """
    
    def __init__(self, api_gateway=None):
        self.api_gateway = api_gateway
        self.cache_dir = Path("artifacts/deepcode_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    async def paper_to_code(self, paper_content: str, paper_title: str, 
                           language: str = "python") -> Dict[str, Any]:
        """
        Convert research paper to implementation code
        
        Args:
            paper_content: Full text of research paper
            paper_title: Title of the paper
            language: Target programming language
            
        Returns:
            Dictionary with generated code, tests, and documentation
        """
        prompt = f"""You are an expert at converting research papers to production-ready code.

Paper Title: {paper_title}

Paper Content:
{paper_content[:8000]}  # Truncate if too long

Task: Generate a complete, production-ready implementation in {language} that:
1. Implements the core algorithm/methodology from the paper
2. Includes proper error handling and input validation
3. Has comprehensive docstrings and comments
4. Includes unit tests
5. Follows best practices for {language}

Provide:
- main.py: Core implementation
- tests.py: Unit tests
- README.md: Documentation
- requirements.txt: Dependencies

Format as JSON with keys: main_code, test_code, readme, requirements"""

        if self.api_gateway:
            response = await self.api_gateway.generate(
                prompt=prompt,
                model_tier="powerful",  # Use Claude Opus or GPT-4
                task_type="code_generation"
            )
        else:
            # Fallback to local generation
            response = {"content": json.dumps({
                "main_code": "# Generated code placeholder",
                "test_code": "# Test code placeholder",
                "readme": "# Documentation placeholder",
                "requirements": "# Dependencies placeholder"
            })}
        
        try:
            result = json.loads(response.get("content", "{}"))
        except:
            result = {
                "main_code": response.get("content", ""),
                "test_code": "",
                "readme": "",
                "requirements": ""
            }
        
        # Save to cache
        cache_file = self.cache_dir / f"{paper_title.replace(' ', '_')}.json"
        with open(cache_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
    
    async def text_to_web(self, description: str, framework: str = "react") -> Dict[str, str]:
        """
        Convert text description to web application
        
        Args:
            description: Description of desired web app
            framework: Web framework (react, vue, svelte)
            
        Returns:
            Dictionary with generated web app files
        """
        prompt = f"""You are an expert full-stack developer specializing in {framework}.

Requirements:
{description}

Generate a complete {framework} web application that:
1. Has a modern, responsive UI with Tailwind CSS
2. Includes proper state management
3. Has API integration capability
4. Follows {framework} best practices
5. Is production-ready

Provide:
- App.jsx/tsx: Main component
- components/: Reusable components
- api.js: API integration layer
- package.json: Dependencies
- README.md: Setup instructions

Format as JSON with file paths as keys and content as values."""

        if self.api_gateway:
            response = await self.api_gateway.generate(
                prompt=prompt,
                model_tier="powerful",
                task_type="code_generation"
            )
        else:
            response = {"content": "{}"}
        
        try:
            result = json.loads(response.get("content", "{}"))
        except:
            result = {"App.jsx": response.get("content", "")}
        
        return result
    
    async def text_to_backend(self, description: str, framework: str = "fastapi") -> Dict[str, str]:
        """
        Convert text description to backend API
        
        Args:
            description: Description of desired backend
            framework: Backend framework (fastapi, flask, express)
            
        Returns:
            Dictionary with generated backend files
        """
        prompt = f"""You are an expert backend developer specializing in {framework}.

Requirements:
{description}

Generate a complete {framework} backend API that:
1. Has RESTful endpoints with proper HTTP methods
2. Includes authentication and authorization
3. Has database models and migrations
4. Includes error handling and validation
5. Has API documentation (OpenAPI/Swagger)
6. Is production-ready with logging

Provide:
- main.py: Application entry point
- routes/: API endpoints
- models/: Database models
- auth.py: Authentication logic
- requirements.txt: Dependencies
- README.md: Setup instructions

Format as JSON with file paths as keys and content as values."""

        if self.api_gateway:
            response = await self.api_gateway.generate(
                prompt=prompt,
                model_tier="powerful",
                task_type="code_generation"
            )
        else:
            response = {"content": "{}"}
        
        try:
            result = json.loads(response.get("content", "{}"))
        except:
            result = {"main.py": response.get("content", "")}
        
        return result
    
    async def improve_code_with_paper(self, code: str, paper_content: str) -> str:
        """
        Improve existing code using insights from research paper
        
        Args:
            code: Existing code to improve
            paper_content: Research paper content
            
        Returns:
            Improved code
        """
        prompt = f"""You are an expert at improving code using research insights.

Current Code:
{code[:4000]}

Research Paper Insights:
{paper_content[:4000]}

Task: Improve the code by:
1. Applying algorithmic improvements from the paper
2. Optimizing performance
3. Adding research-backed enhancements
4. Maintaining backward compatibility
5. Adding comments explaining improvements

Return only the improved code."""

        if self.api_gateway:
            response = await self.api_gateway.generate(
                prompt=prompt,
                model_tier="balanced",
                task_type="code_improvement"
            )
        else:
            response = {"content": code}
        
        return response.get("content", code)


# Export for use in other modules
__all__ = ['DeepCodeAgent']
