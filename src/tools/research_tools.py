"""
Research Tools for AI-Assisted Paper Writing and Code Analysis.

These tools support academic research workflows including:
- Literature review and paper analysis
- Cross-analysis of research approaches
- Negative analysis and critique
- Code quality assessment for research implementations
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime


def analyze_paper_structure(paper_text: str) -> Dict[str, Any]:
    """
    Analyzes the structure of a research paper.
    
    Args:
        paper_text: The full text of the research paper
        
    Returns:
        Dictionary with structural analysis including sections, methodology, results
    """
    sections = {
        "abstract": "abstract" in paper_text.lower(),
        "introduction": "introduction" in paper_text.lower(),
        "methodology": any(word in paper_text.lower() for word in ["methodology", "methods", "approach"]),
        "results": "results" in paper_text.lower(),
        "discussion": "discussion" in paper_text.lower(),
        "conclusion": "conclusion" in paper_text.lower(),
        "references": any(word in paper_text.lower() for word in ["references", "bibliography"])
    }
    
    word_count = len(paper_text.split())
    
    analysis = {
        "word_count": word_count,
        "sections_present": sections,
        "completeness_score": sum(sections.values()) / len(sections),
        "estimated_pages": word_count // 250,  # Approximate pages
        "timestamp": datetime.now().isoformat()
    }
    
    return analysis


def cross_analyze_approaches(approach_a: str, approach_b: str, criteria: List[str]) -> Dict[str, Any]:
    """
    Performs cross-analysis of two research approaches against specified criteria.
    
    Args:
        approach_a: Description of first approach
        approach_b: Description of second approach
        criteria: List of evaluation criteria (e.g., ["accuracy", "efficiency", "scalability"])
        
    Returns:
        Comparative analysis highlighting strengths and weaknesses
    """
    analysis = {
        "approach_a": {
            "description": approach_a[:200] + "..." if len(approach_a) > 200 else approach_a,
            "length": len(approach_a.split()),
            "criteria_mentions": {}
        },
        "approach_b": {
            "description": approach_b[:200] + "..." if len(approach_b) > 200 else approach_b,
            "length": len(approach_b.split()),
            "criteria_mentions": {}
        },
        "comparison": {},
        "timestamp": datetime.now().isoformat()
    }
    
    # Count mentions of each criterion in both approaches
    for criterion in criteria:
        a_mentions = approach_a.lower().count(criterion.lower())
        b_mentions = approach_b.lower().count(criterion.lower())
        
        analysis["approach_a"]["criteria_mentions"][criterion] = a_mentions
        analysis["approach_b"]["criteria_mentions"][criterion] = b_mentions
        
        analysis["comparison"][criterion] = {
            "approach_a_focus": a_mentions,
            "approach_b_focus": b_mentions,
            "difference": abs(a_mentions - b_mentions)
        }
    
    return analysis


def negative_analysis(hypothesis: str, counterpoints: List[str]) -> Dict[str, Any]:
    """
    Performs negative analysis by evaluating counterpoints to a hypothesis.
    
    Args:
        hypothesis: The hypothesis or claim to analyze
        counterpoints: List of counterarguments or limitations
        
    Returns:
        Structured negative analysis with risk assessment
    """
    analysis = {
        "hypothesis": hypothesis,
        "num_counterpoints": len(counterpoints),
        "counterpoints_analysis": [],
        "risk_level": "low" if len(counterpoints) < 3 else "medium" if len(counterpoints) < 5 else "high",
        "recommendations": [],
        "timestamp": datetime.now().isoformat()
    }
    
    for i, point in enumerate(counterpoints, 1):
        analysis["counterpoints_analysis"].append({
            "id": i,
            "counterpoint": point,
            "severity": "high" if any(word in point.lower() for word in ["invalid", "false", "incorrect", "wrong"]) else "medium"
        })
    
    # Generate recommendations
    if len(counterpoints) >= 5:
        analysis["recommendations"].append("Consider revising hypothesis due to multiple significant counterpoints")
    if len(counterpoints) >= 3:
        analysis["recommendations"].append("Address at least top 3 counterpoints in paper discussion")
    
    analysis["recommendations"].append("Strengthen argument with additional evidence")
    
    return analysis


def code_quality_assessment(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Assesses code quality for research implementations.
    
    Args:
        code: The code to assess
        language: Programming language (default: python)
        
    Returns:
        Quality metrics including complexity, documentation, and best practices
    """
    lines = code.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    comment_lines = [line for line in lines if line.strip().startswith('#') or line.strip().startswith('//')]
    
    # Basic metrics
    metrics = {
        "language": language,
        "total_lines": len(lines),
        "code_lines": len(non_empty_lines),
        "comment_lines": len(comment_lines),
        "documentation_ratio": len(comment_lines) / max(len(non_empty_lines), 1),
        "average_line_length": sum(len(line) for line in non_empty_lines) / max(len(non_empty_lines), 1),
        "has_docstrings": '"""' in code or "'''" in code,
        "timestamp": datetime.now().isoformat()
    }
    
    # Quality indicators
    quality_indicators = {
        "well_documented": metrics["documentation_ratio"] > 0.2,
        "reasonable_line_length": metrics["average_line_length"] < 100,
        "has_functions": "def " in code if language == "python" else "function" in code,
        "has_classes": "class " in code if language == "python" else "class" in code
    }
    
    metrics["quality_indicators"] = quality_indicators
    metrics["quality_score"] = sum(quality_indicators.values()) / len(quality_indicators)
    
    return metrics


def save_research_artifact(artifact_type: str, content: str, filename: Optional[str] = None) -> str:
    """
    Saves research artifacts (papers, analyses, reviews) to organized directories.
    
    Args:
        artifact_type: Type of artifact ("paper", "analysis", "review", "data")
        content: The content to save
        filename: Optional filename (auto-generated if not provided)
        
    Returns:
        Path to saved artifact
    """
    base_dir = Path("artifacts")
    
    # Map artifact types to directories
    type_dirs = {
        "paper": base_dir / "papers",
        "analysis": base_dir / "analysis",
        "review": base_dir / "code_reviews",
        "data": base_dir / "analysis",
        "reference": Path(".context") / "references"
    }
    
    target_dir = type_dirs.get(artifact_type, base_dir / "analysis")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{artifact_type}_{timestamp}.txt"
    
    filepath = target_dir / filename
    filepath.write_text(content)
    
    return str(filepath)


def extract_citations(text: str) -> List[Dict[str, str]]:
    """
    Extracts citations from research text (basic extraction).
    
    Args:
        text: Text containing citations
        
    Returns:
        List of extracted citations with metadata
    """
    citations = []
    
    # Simple extraction patterns (can be enhanced with regex)
    lines = text.split('\n')
    citation_keywords = ['et al.', 'et al,', '(19', '(20', 'doi:', 'arxiv:']
    
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in citation_keywords):
            citations.append({
                "line_number": i + 1,
                "text": line.strip(),
                "type": "inline" if line.startswith(' ') else "reference"
            })
    
    return citations


def generate_paper_outline(title: str, research_question: str, methodology: str) -> Dict[str, Any]:
    """
    Generates a structured outline for a research paper.
    
    Args:
        title: Paper title
        research_question: Main research question
        methodology: Research methodology description
        
    Returns:
        Structured paper outline with sections
    """
    outline = {
        "title": title,
        "research_question": research_question,
        "sections": {
            "1_abstract": {
                "title": "Abstract",
                "content_guide": "Summary of research question, methodology, key findings (150-250 words)"
            },
            "2_introduction": {
                "title": "Introduction",
                "subsections": [
                    "Background and motivation",
                    "Research gap identification",
                    "Research question and objectives",
                    "Paper structure overview"
                ]
            },
            "3_related_work": {
                "title": "Related Work",
                "content_guide": "Literature review, comparison with existing approaches"
            },
            "4_methodology": {
                "title": "Methodology",
                "content": methodology,
                "subsections": [
                    "Approach description",
                    "Implementation details",
                    "Experimental setup"
                ]
            },
            "5_results": {
                "title": "Results",
                "subsections": [
                    "Experimental results",
                    "Performance analysis",
                    "Comparison with baselines"
                ]
            },
            "6_discussion": {
                "title": "Discussion",
                "subsections": [
                    "Interpretation of results",
                    "Limitations and threats to validity",
                    "Implications for practice and research"
                ]
            },
            "7_conclusion": {
                "title": "Conclusion",
                "subsections": [
                    "Summary of contributions",
                    "Future work"
                ]
            },
            "8_references": {
                "title": "References",
                "content_guide": "Alphabetically sorted list of all cited works"
            }
        },
        "estimated_length": "6-8 pages (conference) or 12-15 pages (journal)",
        "created_at": datetime.now().isoformat()
    }
    
    # Save outline as artifact
    outline_json = json.dumps(outline, indent=2)
    save_research_artifact("paper", outline_json, f"outline_{title.replace(' ', '_')[:30]}.json")
    
    return outline


def compare_code_implementations(impl_a: str, impl_b: str, criteria: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Compares two code implementations for research paper analysis.
    
    Args:
        impl_a: First implementation code
        impl_b: Second implementation code
        criteria: Optional evaluation criteria
        
    Returns:
        Detailed comparison of implementations
    """
    if criteria is None:
        criteria = ["complexity", "efficiency", "readability", "maintainability"]
    
    metrics_a = code_quality_assessment(impl_a)
    metrics_b = code_quality_assessment(impl_b)
    
    comparison = {
        "implementation_a": {
            "lines_of_code": metrics_a["code_lines"],
            "documentation_ratio": metrics_a["documentation_ratio"],
            "quality_score": metrics_a["quality_score"]
        },
        "implementation_b": {
            "lines_of_code": metrics_b["code_lines"],
            "documentation_ratio": metrics_b["documentation_ratio"],
            "quality_score": metrics_b["quality_score"]
        },
        "comparison_summary": {
            "more_concise": "a" if metrics_a["code_lines"] < metrics_b["code_lines"] else "b",
            "better_documented": "a" if metrics_a["documentation_ratio"] > metrics_b["documentation_ratio"] else "b",
            "higher_quality": "a" if metrics_a["quality_score"] > metrics_b["quality_score"] else "b"
        },
        "criteria": criteria,
        "timestamp": datetime.now().isoformat()
    }
    
    return comparison
