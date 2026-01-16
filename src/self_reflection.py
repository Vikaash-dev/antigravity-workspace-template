"""
Self-Reflection and Self-Review System for Autonomous Agents.

This module provides metacognitive capabilities for agents to:
- Reflect on their own work and decision-making
- Critique and improve their outputs
- Learn from mistakes and iterate
- Ensure quality through self-assessment

Inspired by reflexion patterns in autonomous AI systems.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from src.antigravity_gateway import ModelTier, get_gateway
import json


class SelfReflectionEngine:
    """
    Metacognitive engine for agent self-reflection and improvement.
    
    Enables agents to:
    - Analyze their own outputs
    - Identify weaknesses and improvement areas
    - Generate revised versions
    - Track improvement over iterations
    """
    
    def __init__(self, gateway: Optional[Any] = None):
        self.gateway = gateway or get_gateway()
        self.reflection_history = []
    
    async def reflect_on_output(
        self,
        output: Any,
        task_description: str,
        success_criteria: List[str],
        agent_name: str = "agent"
    ) -> Dict[str, Any]:
        """
        Perform self-reflection on agent output.
        
        Args:
            output: The output to reflect on
            task_description: Description of the task
            success_criteria: Criteria for successful completion
            agent_name: Name of the agent for tracking
            
        Returns:
            Reflection results with identified issues and improvements
        """
        reflection_prompt = f"""You are performing self-reflection as {agent_name}.

Task: {task_description}

Your Output:
{self._format_output(output)}

Success Criteria:
{chr(10).join(f"- {criterion}" for criterion in success_criteria)}

Perform critical self-analysis:

1. **Strengths**: What did you do well?
2. **Weaknesses**: What could be improved?
3. **Gaps**: What is missing or incomplete?
4. **Errors**: Are there any mistakes or inconsistencies?
5. **Improvement Plan**: How can this be made better?

Be brutally honest. This is for self-improvement, not external review.

Return structured JSON:
{{
    "strengths": ["list of strengths"],
    "weaknesses": ["list of weaknesses"],
    "gaps": ["list of gaps"],
    "errors": ["list of errors"],
    "improvement_suggestions": ["list of specific improvements"],
    "confidence_score": 0-10,
    "needs_revision": true/false
}}"""
        
        response = self.gateway.generate(
            reflection_prompt,
            model_tier=ModelTier.BALANCED,
            max_tokens=2000,
            temperature=0.3  # Lower temperature for more analytical reflection
        )
        
        try:
            reflection = json.loads(self._extract_json(response.get("text", "{}")))
        except:
            # Fallback if JSON parsing fails
            reflection = {
                "strengths": ["Analysis completed"],
                "weaknesses": ["Unable to parse structured reflection"],
                "gaps": [],
                "errors": [],
                "improvement_suggestions": ["Improve output formatting"],
                "confidence_score": 5,
                "needs_revision": True
            }
        
        # Store in history
        self.reflection_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "task": task_description,
            "reflection": reflection
        })
        
        return reflection
    
    async def iterative_improvement(
        self,
        initial_output: Any,
        task_description: str,
        success_criteria: List[str],
        max_iterations: int = 3,
        agent_name: str = "agent"
    ) -> Dict[str, Any]:
        """
        Iteratively improve output through self-reflection.
        
        Args:
            initial_output: Starting output
            task_description: Task description
            success_criteria: Success criteria
            max_iterations: Maximum improvement iterations
            agent_name: Agent name
            
        Returns:
            Final improved output with iteration history
        """
        current_output = initial_output
        iterations = []
        
        for i in range(max_iterations):
            print(f"  🔄 Iteration {i+1}/{max_iterations}: Self-reflection and improvement")
            
            # Reflect on current output
            reflection = await self.reflect_on_output(
                current_output,
                task_description,
                success_criteria,
                agent_name
            )
            
            iterations.append({
                "iteration": i + 1,
                "reflection": reflection,
                "confidence_score": reflection.get("confidence_score", 0)
            })
            
            # If good enough, stop
            if not reflection.get("needs_revision", True) and reflection.get("confidence_score", 0) >= 8:
                print(f"  ✅ Quality threshold reached (confidence: {reflection.get('confidence_score')}/10)")
                break
            
            # Generate improved version
            improvement_prompt = f"""Based on self-reflection, improve this output.

Original Task: {task_description}

Current Output:
{self._format_output(current_output)}

Self-Identified Issues:
- Weaknesses: {', '.join(reflection.get('weaknesses', []))}
- Gaps: {', '.join(reflection.get('gaps', []))}
- Errors: {', '.join(reflection.get('errors', []))}

Improvement Suggestions:
{chr(10).join(f"- {sugg}" for sugg in reflection.get('improvement_suggestions', []))}

Generate an improved version that addresses ALL identified issues."""
            
            improved_response = self.gateway.generate(
                improvement_prompt,
                model_tier=ModelTier.POWERFUL,
                max_tokens=3000,
                temperature=0.7
            )
            
            current_output = improved_response.get("text", current_output)
        
        return {
            "final_output": current_output,
            "iterations": len(iterations),
            "iteration_history": iterations,
            "final_confidence": iterations[-1].get("confidence_score", 0) if iterations else 0,
            "improved": len(iterations) > 1
        }
    
    def _format_output(self, output: Any) -> str:
        """Format output for display in prompts."""
        if isinstance(output, str):
            return output[:2000]  # Limit length
        elif isinstance(output, dict):
            return json.dumps(output, indent=2)[:2000]
        else:
            return str(output)[:2000]
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text that might contain markdown or other formatting."""
        # Try to find JSON in code blocks
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        else:
            # Try to find JSON object
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return text[start:end]
        return text
    
    def get_reflection_summary(self) -> Dict[str, Any]:
        """Get summary of all reflections."""
        if not self.reflection_history:
            return {"total_reflections": 0}
        
        return {
            "total_reflections": len(self.reflection_history),
            "agents": list(set(r["agent"] for r in self.reflection_history)),
            "average_confidence": sum(
                r["reflection"].get("confidence_score", 0) 
                for r in self.reflection_history
            ) / len(self.reflection_history),
            "total_improvements": sum(
                len(r["reflection"].get("improvement_suggestions", []))
                for r in self.reflection_history
            )
        }


class SelfReviewSystem:
    """
    Comprehensive self-review system for quality assurance.
    
    Performs multi-faceted review of agent outputs including:
    - Technical accuracy
    - Completeness
    - Clarity and coherence
    - Adherence to requirements
    - Best practices compliance
    """
    
    def __init__(self, gateway: Optional[Any] = None):
        self.gateway = gateway or get_gateway()
        self.review_history = []
    
    async def comprehensive_review(
        self,
        content: Any,
        content_type: str,
        requirements: List[str],
        agent_name: str = "agent"
    ) -> Dict[str, Any]:
        """
        Perform comprehensive self-review.
        
        Args:
            content: Content to review
            content_type: Type of content (paper, code, analysis, etc.)
            requirements: List of requirements
            agent_name: Agent name
            
        Returns:
            Comprehensive review with scores and recommendations
        """
        review_prompt = f"""Perform a comprehensive self-review as {agent_name}.

Content Type: {content_type}

Content:
{self._format_content(content)}

Requirements:
{chr(10).join(f"- {req}" for req in requirements)}

Review Dimensions (score 1-10 each):

1. **Technical Accuracy**: Is the content technically correct?
2. **Completeness**: Does it cover all required aspects?
3. **Clarity**: Is it clear and well-structured?
4. **Coherence**: Is it logically consistent?
5. **Novelty**: Does it provide new insights?
6. **Rigor**: Is the methodology sound?

For each dimension, provide:
- Score (1-10)
- Justification
- Specific improvements

Return structured JSON:
{{
    "scores": {{
        "technical_accuracy": {{score, justification, improvements}},
        "completeness": {{score, justification, improvements}},
        "clarity": {{score, justification, improvements}},
        "coherence": {{score, justification, improvements}},
        "novelty": {{score, justification, improvements}},
        "rigor": {{score, justification, improvements}}
    }},
    "overall_score": 0-10,
    "pass_criteria": true/false,
    "major_issues": ["list"],
    "minor_issues": ["list"],
    "recommendations": ["prioritized list of improvements"]
}}"""
        
        response = self.gateway.generate(
            review_prompt,
            model_tier=ModelTier.POWERFUL,
            max_tokens=3000,
            temperature=0.2  # Very analytical
        )
        
        try:
            review = json.loads(self._extract_json(response.get("text", "{}")))
        except:
            review = {
                "scores": {},
                "overall_score": 5,
                "pass_criteria": False,
                "major_issues": ["Review parsing failed"],
                "minor_issues": [],
                "recommendations": ["Improve review process"]
            }
        
        # Store in history
        self.review_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "content_type": content_type,
            "review": review
        })
        
        return review
    
    def _format_content(self, content: Any) -> str:
        """Format content for review."""
        if isinstance(content, str):
            return content[:3000]
        elif isinstance(content, dict):
            return json.dumps(content, indent=2)[:3000]
        else:
            return str(content)[:3000]
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text."""
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        else:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                return text[start:end]
        return text


# Global instances
_reflection_engine = None
_review_system = None


def get_reflection_engine() -> SelfReflectionEngine:
    """Get global self-reflection engine."""
    global _reflection_engine
    if _reflection_engine is None:
        _reflection_engine = SelfReflectionEngine()
    return _reflection_engine


def get_review_system() -> SelfReviewSystem:
    """Get global self-review system."""
    global _review_system
    if _review_system is None:
        _review_system = SelfReviewSystem()
    return _review_system
