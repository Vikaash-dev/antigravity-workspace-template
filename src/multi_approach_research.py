"""
Multi-Approach Parallel Research System with Aggregation.

This module enables multiple AI agents to research the same topic using
different methodologies and approaches, then aggregate their findings
into a single superior research paper.

Key features:
- Parallel agents with different research philosophies
- Methodology diversity (quantitative, qualitative, theoretical, empirical)
- Consensus building and conflict resolution
- Quality-weighted aggregation
- Cross-validation of findings
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json
from src.acp_protocol import ACPAgent, AgentRole, ACPCoordinator
from src.antigravity_gateway import ModelTier, get_gateway
from src.self_reflection import get_reflection_engine, get_review_system


class ResearchApproach:
    """Defines a research methodology approach."""
    
    QUANTITATIVE = "quantitative"  # Data-driven, statistical
    QUALITATIVE = "qualitative"  # Interpretive, contextual
    THEORETICAL = "theoretical"  # Conceptual, abstract
    EMPIRICAL = "empirical"  # Experimental, evidence-based
    COMPUTATIONAL = "computational"  # Algorithmic, simulation
    SURVEY_BASED = "survey"  # Literature synthesis
    CRITICAL = "critical"  # Analytical, evaluative


class MultiApproachAgent(ACPAgent):
    """
    Research agent that uses a specific methodological approach.
    
    Multiple instances with different approaches work in parallel
    on the same research question.
    """
    
    def __init__(
        self,
        name: str,
        approach: str,
        gateway: Optional[Any] = None
    ):
        super().__init__(
            role=AgentRole.RESEARCHER,
            name=name,
            capabilities=[f"{approach}_research", "analysis", "synthesis"],
            gateway=gateway
        )
        self.approach = approach
        self.research_output = None
        self.quality_score = 0.0
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research task using this agent's specific approach."""
        topic = task.get("topic")
        requirements = task.get("requirements", [])
        
        print(f"  🔬 {self.name} ({self.approach} approach) researching: {topic}")
        
        # Research with specific methodology
        research_result = await self._research_with_approach(topic, requirements)
        
        # Self-reflect and improve
        reflection_engine = get_reflection_engine()
        improved_result = await reflection_engine.iterative_improvement(
            research_result,
            f"Research {topic} using {self.approach} approach",
            requirements,
            max_iterations=2,
            agent_name=self.name
        )
        
        # Self-review
        review_system = get_review_system()
        review = await review_system.comprehensive_review(
            improved_result["final_output"],
            "research_paper",
            requirements,
            self.name
        )
        
        self.research_output = improved_result["final_output"]
        self.quality_score = review.get("overall_score", 0)
        
        return {
            "approach": self.approach,
            "agent": self.name,
            "output": improved_result["final_output"],
            "quality_score": self.quality_score,
            "iterations": improved_result["iterations"],
            "review": review,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _research_with_approach(
        self,
        topic: str,
        requirements: List[str]
    ) -> str:
        """Conduct research using this agent's specific approach."""
        approach_prompts = {
            ResearchApproach.QUANTITATIVE: f"""Research {topic} using a QUANTITATIVE approach:
- Focus on numerical data, statistics, and measurable variables
- Emphasize statistical analysis and data-driven insights
- Use mathematical models and quantitative methods
- Provide empirical evidence with numbers
- Structure findings around data and metrics""",
            
            ResearchApproach.QUALITATIVE: f"""Research {topic} using a QUALITATIVE approach:
- Focus on understanding context, meaning, and interpretation
- Emphasize case studies, interviews, and observations
- Explore underlying motivations and reasoning
- Provide rich descriptive narratives
- Structure findings around themes and patterns""",
            
            ResearchApproach.THEORETICAL: f"""Research {topic} using a THEORETICAL approach:
- Focus on conceptual frameworks and abstract models
- Emphasize theoretical foundations and principles
- Develop new theories or extend existing ones
- Provide logical reasoning and deductive analysis
- Structure findings around theoretical contributions""",
            
            ResearchApproach.EMPIRICAL: f"""Research {topic} using an EMPIRICAL approach:
- Focus on direct observation and experimentation
- Emphasize controlled studies and replicable results
- Test hypotheses through systematic investigation
- Provide experimental evidence
- Structure findings around empirical validation""",
            
            ResearchApproach.COMPUTATIONAL: f"""Research {topic} using a COMPUTATIONAL approach:
- Focus on algorithms, simulations, and computational methods
- Emphasize implementation and performance analysis
- Develop computational models and tools
- Provide algorithmic insights and complexity analysis
- Structure findings around computational contributions""",
            
            ResearchApproach.SURVEY_BASED: f"""Research {topic} using a SURVEY-BASED approach:
- Focus on comprehensive literature review
- Emphasize synthesis of existing research
- Identify trends, gaps, and future directions
- Provide systematic overview of the field
- Structure findings around literature analysis""",
            
            ResearchApproach.CRITICAL: f"""Research {topic} using a CRITICAL approach:
- Focus on analytical evaluation and critique
- Emphasize strengths, weaknesses, and limitations
- Challenge assumptions and conventional wisdom
- Provide balanced critical analysis
- Structure findings around critical assessment"""
        }
        
        prompt = approach_prompts.get(
            self.approach,
            f"Research {topic} thoroughly"
        )
        
        prompt += f"""

Requirements:
{chr(10).join(f"- {req}" for req in requirements)}

Produce a comprehensive research section (1500-2000 words) that:
1. Introduces the {self.approach} perspective
2. Presents findings using {self.approach} methodology
3. Discusses implications from {self.approach} viewpoint
4. Concludes with {self.approach}-specific insights

Be thorough, rigorous, and true to the {self.approach} methodology."""
        
        response = self.gateway.generate(
            prompt,
            model_tier=ModelTier.POWERFUL,
            max_tokens=3000,
            temperature=0.7
        )
        
        return response.get("text", "")


class ResearchAggregator:
    """
    Aggregates research from multiple agents with different approaches
    into a single coherent, superior research paper.
    """
    
    def __init__(self, gateway: Optional[Any] = None):
        self.gateway = gateway or get_gateway()
    
    async def aggregate_research(
        self,
        research_outputs: List[Dict[str, Any]],
        topic: str,
        synthesis_strategy: str = "quality_weighted"
    ) -> Dict[str, Any]:
        """
        Aggregate multiple research outputs into a single paper.
        
        Args:
            research_outputs: List of research outputs from different agents
            topic: Research topic
            synthesis_strategy: How to combine (quality_weighted, consensus, comprehensive)
            
        Returns:
            Aggregated research paper with metadata
        """
        print(f"\n📊 Aggregating {len(research_outputs)} research approaches")
        
        # Sort by quality score
        sorted_outputs = sorted(
            research_outputs,
            key=lambda x: x.get("quality_score", 0),
            reverse=True
        )
        
        # Extract findings from each approach
        approach_summaries = []
        for output in sorted_outputs:
            approach_summaries.append({
                "approach": output.get("approach"),
                "quality_score": output.get("quality_score"),
                "content": output.get("output", ""),
                "agent": output.get("agent")
            })
        
        # Identify consensus and conflicts
        consensus_analysis = await self._analyze_consensus(approach_summaries, topic)
        
        # Synthesize into unified paper
        unified_paper = await self._synthesize_paper(
            topic,
            approach_summaries,
            consensus_analysis,
            synthesis_strategy
        )
        
        # Final quality review
        review_system = get_review_system()
        final_review = await review_system.comprehensive_review(
            unified_paper,
            "aggregated_research_paper",
            [
                "Integrates multiple methodological perspectives",
                "Presents consensus findings",
                "Addresses conflicting viewpoints",
                "Provides comprehensive coverage",
                "Maintains academic rigor"
            ],
            "aggregator"
        )
        
        return {
            "topic": topic,
            "paper": unified_paper,
            "approaches_used": [o.get("approach") for o in sorted_outputs],
            "quality_scores": [o.get("quality_score") for o in sorted_outputs],
            "consensus_analysis": consensus_analysis,
            "final_review": final_review,
            "overall_quality": final_review.get("overall_score", 0),
            "timestamp": datetime.now().isoformat()
        }
    
    async def _analyze_consensus(
        self,
        approach_summaries: List[Dict[str, Any]],
        topic: str
    ) -> Dict[str, Any]:
        """Analyze consensus and conflicts across approaches."""
        analysis_prompt = f"""Analyze consensus and conflicts across different research approaches for: {topic}

Research Approaches and Findings:

{self._format_approaches(approach_summaries)}

Identify:
1. **Consensus Points**: What do all/most approaches agree on?
2. **Conflicting Views**: Where do approaches disagree?
3. **Complementary Insights**: How do approaches complement each other?
4. **Unique Contributions**: What unique value does each approach provide?
5. **Integration Strategy**: How can these be best combined?

Return structured analysis as JSON:
{{
    "consensus_points": ["list of agreed findings"],
    "conflicts": [{{
        "issue": "conflicting point",
        "approaches": {{"approach1": "view1", "approach2": "view2"}},
        "resolution": "how to resolve"
    }}],
    "complementary_insights": ["how approaches complement"],
    "unique_contributions": {{"approach": "unique value"}},
    "integration_strategy": "recommended synthesis approach"
}}"""
        
        response = self.gateway.generate(
            analysis_prompt,
            model_tier=ModelTier.POWERFUL,
            max_tokens=2500,
            temperature=0.3
        )
        
        try:
            return json.loads(self._extract_json(response.get("text", "{}")))
        except:
            return {
                "consensus_points": ["Multiple perspectives analyzed"],
                "conflicts": [],
                "complementary_insights": ["Diverse methodologies applied"],
                "unique_contributions": {},
                "integration_strategy": "Sequential integration"
            }
    
    async def _synthesize_paper(
        self,
        topic: str,
        approach_summaries: List[Dict[str, Any]],
        consensus_analysis: Dict[str, Any],
        strategy: str
    ) -> str:
        """Synthesize a unified research paper."""
        synthesis_prompt = f"""Create a comprehensive, unified research paper on: {topic}

You have access to research from multiple methodological approaches:

{self._format_approaches(approach_summaries)}

Consensus Analysis:
{json.dumps(consensus_analysis, indent=2)}

Synthesis Strategy: {strategy}

Create a superior research paper that:

1. **INTEGRATES** all approaches into a coherent narrative
2. **HIGHLIGHTS** consensus findings prominently
3. **ADDRESSES** conflicts thoughtfully with balanced perspective
4. **LEVERAGES** complementary insights for deeper understanding
5. **ACKNOWLEDGES** methodological diversity as a strength

Structure:

**Abstract** (200 words)
- Multi-method research summary

**Introduction** (500 words)
- Problem statement
- Multi-approach rationale
- Research questions

**Methodology** (400 words)
- Overview of approaches used
- Justification for multi-method design

**Findings** (1500 words)
- Consensus findings (what all approaches agree on)
- Approach-specific insights (unique contributions)
- Conflicting viewpoints (with analysis)
- Integrated analysis (synthesized understanding)

**Discussion** (800 words)
- Implications of integrated findings
- Methodological triangulation benefits
- Limitations and future work

**Conclusion** (300 words)
- Key contributions
- Practical implications
- Future directions

Write in academic style, cite approaches appropriately, maintain rigor.
Target length: 3500-4000 words."""
        
        response = self.gateway.generate(
            synthesis_prompt,
            model_tier=ModelTier.POWERFUL,
            max_tokens=5000,
            temperature=0.7
        )
        
        return response.get("text", "")
    
    def _format_approaches(self, summaries: List[Dict[str, Any]]) -> str:
        """Format approach summaries for prompts."""
        formatted = []
        for i, summary in enumerate(summaries, 1):
            formatted.append(f"""
Approach {i}: {summary['approach'].upper()} (Quality: {summary['quality_score']}/10)
Agent: {summary['agent']}
Findings:
{summary['content'][:1500]}...
""")
        return "\n".join(formatted)
    
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


async def parallel_multi_approach_research(
    topic: str,
    approaches: List[str] = None,
    requirements: List[str] = None,
    gateway: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Conduct parallel research using multiple approaches and aggregate results.
    
    Args:
        topic: Research topic
        approaches: List of research approaches to use
        requirements: Research requirements
        gateway: API gateway
        
    Returns:
        Aggregated research paper with all approach outputs
    """
    if approaches is None:
        approaches = [
            ResearchApproach.QUANTITATIVE,
            ResearchApproach.QUALITATIVE,
            ResearchApproach.THEORETICAL,
            ResearchApproach.EMPIRICAL,
            ResearchApproach.COMPUTATIONAL
        ]
    
    if requirements is None:
        requirements = [
            "Comprehensive coverage of topic",
            "Rigorous methodology",
            "Novel insights",
            "Practical implications",
            "Future research directions"
        ]
    
    gateway = gateway or get_gateway()
    
    print(f"\n🚀 Starting parallel multi-approach research on: {topic}")
    print(f"   Approaches: {', '.join(approaches)}")
    print(f"   Agents: {len(approaches)} parallel researchers\n")
    
    # Create agents for each approach
    agents = []
    for i, approach in enumerate(approaches):
        agent = MultiApproachAgent(
            name=f"researcher_{approach}_{i+1}",
            approach=approach,
            gateway=gateway
        )
        agents.append(agent)
    
    # Execute research in parallel
    tasks = [
        agent.execute_task({
            "topic": topic,
            "requirements": requirements
        })
        for agent in agents
    ]
    
    research_outputs = await asyncio.gather(*tasks)
    
    # Aggregate results
    aggregator = ResearchAggregator(gateway)
    aggregated_result = await aggregator.aggregate_research(
        research_outputs,
        topic,
        synthesis_strategy="quality_weighted"
    )
    
    # Save results
    output_dir = Path("artifacts/papers/multi_approach")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save aggregated paper
    paper_file = output_dir / f"{topic.replace(' ', '_')}_aggregated.md"
    paper_file.write_text(aggregated_result["paper"])
    
    # Save metadata
    metadata_file = output_dir / f"{topic.replace(' ', '_')}_metadata.json"
    metadata_file.write_text(json.dumps({
        "topic": topic,
        "approaches": aggregated_result["approaches_used"],
        "quality_scores": aggregated_result["quality_scores"],
        "overall_quality": aggregated_result["overall_quality"],
        "timestamp": aggregated_result["timestamp"]
    }, indent=2))
    
    # Save individual approach outputs
    for output in research_outputs:
        approach_file = output_dir / f"{topic.replace(' ', '_')}_{output['approach']}.md"
        approach_file.write_text(output["output"])
    
    print(f"\n✅ Research complete!")
    print(f"   Aggregated paper: {paper_file}")
    print(f"   Overall quality: {aggregated_result['overall_quality']}/10")
    print(f"   Approaches used: {len(approaches)}")
    
    return aggregated_result
