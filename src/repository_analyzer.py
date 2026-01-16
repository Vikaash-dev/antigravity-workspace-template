"""
Repository Analyzer - File-by-file Analysis and Code Integration
Analyzes current codebase and similar GitHub repositories to extract proven patterns.
Inspired by DATAGEN, Aetherius AI, STORM Research, and other proven systems.
"""

import os
import ast
import json
import logging
from typing import Dict, List, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class FileAnalysis:
    """Analysis result for a single file"""
    filepath: str
    lines_of_code: int
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    docstring: str = ""
    complexity_score: int = 0
    dependencies: List[str] = field(default_factory=list)
    functional_block: str = ""  # e.g., "research", "agent_coordination", "memory"

@dataclass
class FunctionalBlock:
    """Represents a functional block in the system"""
    name: str
    description: str
    files: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    key_patterns: List[str] = field(default_factory=list)
    similarity_repos: List[str] = field(default_factory=list)  # Similar repos for reference

class RepositoryAnalyzer:
    """
    Comprehensive repository analyzer that performs file-by-file, line-by-line analysis.
    Identifies functional blocks and maps them to proven patterns from similar repositories.
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.analyses: Dict[str, FileAnalysis] = {}
        self.functional_blocks: Dict[str, FunctionalBlock] = {}
        self.logger = logging.getLogger(__name__)
        
        # Define functional blocks based on proven systems
        self._init_functional_blocks()
    
    def _init_functional_blocks(self):
        """Initialize functional blocks based on proven multi-agent research systems"""
        self.functional_blocks = {
            "literature_search": FunctionalBlock(
                name="Literature Search & Collection",
                description="Search academic papers, scrape ArXiv, Google Scholar",
                similarity_repos=["DATAGEN/src/tools/arxiv_tool.py", "STORM/literature_search.py"]
            ),
            "hypothesis_generation": FunctionalBlock(
                name="Hypothesis Generation",
                description="Generate research hypotheses from literature",
                similarity_repos=["DATAGEN/src/agents/hypothesis_agent.py"]
            ),
            "data_analysis": FunctionalBlock(
                name="Data Analysis & Statistics",
                description="Statistical analysis, data processing, visualization",
                similarity_repos=["DATAGEN/src/agents/analysis_agent.py"]
            ),
            "code_generation": FunctionalBlock(
                name="Code Generation & Execution",
                description="Generate code implementations, run experiments",
                similarity_repos=["DATAGEN/src/agents/code_agent.py", "Paper2Code"]
            ),
            "multi_agent_coordination": FunctionalBlock(
                name="Multi-Agent Coordination",
                description="Agent orchestration, message passing, workflow management",
                similarity_repos=["DATAGEN/src/core/coordinator.py", "Aetherius/multi_agent.py"]
            ),
            "long_term_memory": FunctionalBlock(
                name="Long-Term Memory & Context",
                description="Persistent memory, context retention, knowledge graphs",
                similarity_repos=["Aetherius/memory_system.py", "DATAGEN/src/core/memory.py"]
            ),
            "report_writing": FunctionalBlock(
                name="Report & Paper Writing",
                description="Academic paper generation, formatting, citations",
                similarity_repos=["DATAGEN/src/agents/writer_agent.py", "STORM/paper_generator.py"]
            ),
            "self_reflection": FunctionalBlock(
                name="Self-Reflection & Improvement",
                description="Agent self-assessment, iterative improvement",
                similarity_repos=["current/src/self_reflection.py"]
            ),
            "research_orchestration": FunctionalBlock(
                name="Research Workflow Orchestration",
                description="End-to-end research pipeline management",
                similarity_repos=["DATAGEN/src/system.py", "STORM/orchestrator.py"]
            ),
            "tool_integration": FunctionalBlock(
                name="Tool Integration Layer",
                description="External tool integration (APIs, MCPs, services)",
                similarity_repos=["current/src/integrations/", "DATAGEN/src/tools/"]
            )
        }
    
    def analyze_file(self, filepath: Path) -> FileAnalysis:
        """
        Perform line-by-line analysis of a Python file.
        Extracts functions, classes, imports, complexity metrics.
        """
        analysis = FileAnalysis(filepath=str(filepath), lines_of_code=0)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                analysis.lines_of_code = len(content.splitlines())
                
                # Parse AST
                try:
                    tree = ast.parse(content)
                    analysis.docstring = ast.get_docstring(tree) or ""
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            analysis.functions.append(node.name)
                        elif isinstance(node, ast.ClassDef):
                            analysis.classes.append(node.name)
                        elif isinstance(node, ast.Import):
                            for alias in node.names:
                                analysis.imports.append(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                analysis.imports.append(node.module)
                    
                    # Calculate complexity (simple metric: number of nodes)
                    analysis.complexity_score = len(list(ast.walk(tree)))
                    
                except SyntaxError as e:
                    self.logger.warning(f"Syntax error in {filepath}: {e}")
                
        except Exception as e:
            self.logger.error(f"Error analyzing {filepath}: {e}")
        
        # Determine functional block
        analysis.functional_block = self._classify_functional_block(filepath, analysis)
        
        return analysis
    
    def _classify_functional_block(self, filepath: Path, analysis: FileAnalysis) -> str:
        """Classify file into a functional block based on path and content"""
        path_str = str(filepath).lower()
        
        # Path-based classification
        if "research" in path_str or "paper" in path_str:
            return "report_writing"
        elif "agent" in path_str and "autonomous" in path_str:
            return "multi_agent_coordination"
        elif "memory" in path_str:
            return "long_term_memory"
        elif "self_reflection" in path_str or "review" in path_str:
            return "self_reflection"
        elif "tool" in path_str or "integration" in path_str:
            return "tool_integration"
        elif "task" in path_str or "planner" in path_str:
            return "research_orchestration"
        
        # Content-based classification
        functions_str = " ".join(analysis.functions).lower()
        if "search" in functions_str or "arxiv" in functions_str:
            return "literature_search"
        elif "hypothesis" in functions_str or "generate_idea" in functions_str:
            return "hypothesis_generation"
        elif "analyze" in functions_str or "statistics" in functions_str:
            return "data_analysis"
        elif "code_gen" in functions_str or "execute" in functions_str:
            return "code_generation"
        
        return "unknown"
    
    def analyze_repository(self) -> Dict[str, Any]:
        """
        Perform complete repository analysis.
        Returns comprehensive report with functional block mapping.
        """
        self.logger.info(f"Analyzing repository: {self.repo_path}")
        
        # Find all Python files
        python_files = list(self.repo_path.rglob("*.py"))
        self.logger.info(f"Found {len(python_files)} Python files")
        
        # Analyze each file
        for filepath in python_files:
            if "venv" in str(filepath) or "__pycache__" in str(filepath):
                continue
            
            analysis = self.analyze_file(filepath)
            self.analyses[str(filepath)] = analysis
            
            # Add to functional block
            block_name = analysis.functional_block
            if block_name in self.functional_blocks:
                self.functional_blocks[block_name].files.append(str(filepath))
        
        # Generate report
        report = self._generate_report()
        return report
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        total_loc = sum(a.lines_of_code for a in self.analyses.values())
        total_functions = sum(len(a.functions) for a in self.analyses.values())
        total_classes = sum(len(a.classes) for a in self.analyses.values())
        
        report = {
            "summary": {
                "total_files": len(self.analyses),
                "total_lines_of_code": total_loc,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "average_complexity": sum(a.complexity_score for a in self.analyses.values()) / len(self.analyses) if self.analyses else 0
            },
            "functional_blocks": {},
            "files": {}
        }
        
        # Functional blocks summary
        for block_name, block in self.functional_blocks.items():
            if block.files:
                report["functional_blocks"][block_name] = {
                    "description": block.description,
                    "file_count": len(block.files),
                    "files": block.files,
                    "similar_repos": block.similarity_repos,
                    "total_loc": sum(
                        self.analyses[f].lines_of_code 
                        for f in block.files 
                        if f in self.analyses
                    )
                }
        
        # File-level details
        for filepath, analysis in self.analyses.items():
            report["files"][filepath] = {
                "lines": analysis.lines_of_code,
                "functions": analysis.functions,
                "classes": analysis.classes,
                "imports": analysis.imports[:10],  # Top 10 imports
                "complexity": analysis.complexity_score,
                "functional_block": analysis.functional_block
            }
        
        return report
    
    def identify_integration_opportunities(self, target_repos: List[str]) -> Dict[str, List[str]]:
        """
        Identify integration opportunities by comparing functional blocks
        with patterns from target repositories (e.g., DATAGEN, STORM).
        """
        opportunities = {}
        
        for block_name, block in self.functional_blocks.items():
            if not block.files:
                # Missing functional block - high priority integration
                opportunities[block_name] = {
                    "status": "missing",
                    "priority": "high",
                    "recommended_sources": block.similarity_repos,
                    "action": f"Implement {block.description} based on patterns from {', '.join(block.similarity_repos)}"
                }
            elif len(block.files) < 2:
                # Under-developed block
                opportunities[block_name] = {
                    "status": "under_developed",
                    "priority": "medium",
                    "current_files": block.files,
                    "recommended_sources": block.similarity_repos,
                    "action": f"Enhance {block.description} with additional patterns"
                }
        
        return opportunities
    
    def export_report(self, output_path: str):
        """Export analysis report to JSON file"""
        report = self.analyze_repository()
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Report exported to {output_path}")
        
        # Also create a human-readable summary
        summary_path = output_path.replace('.json', '_summary.txt')
        with open(summary_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("REPOSITORY ANALYSIS REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write("SUMMARY\n")
            f.write("-"*80 + "\n")
            for key, value in report["summary"].items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n\nFUNCTIONAL BLOCKS\n")
            f.write("-"*80 + "\n")
            for block_name, block_data in report["functional_blocks"].items():
                f.write(f"\n{block_name.upper()}\n")
                f.write(f"  Description: {block_data['description']}\n")
                f.write(f"  Files: {block_data['file_count']}\n")
                f.write(f"  Total LOC: {block_data['total_loc']}\n")
                f.write(f"  Similar Repos: {', '.join(block_data['similar_repos'])}\n")
            
            f.write("\n\nINTEGRATION OPPORTUNITIES\n")
            f.write("-"*80 + "\n")
            opportunities = self.identify_integration_opportunities([])
            for block_name, opp in opportunities.items():
                f.write(f"\n{block_name.upper()}\n")
                f.write(f"  Status: {opp['status']}\n")
                f.write(f"  Priority: {opp['priority']}\n")
                f.write(f"  Action: {opp['action']}\n")
        
        self.logger.info(f"Summary exported to {summary_path}")
        return summary_path


def analyze_current_repository():
    """Run analysis on current repository"""
    logging.basicConfig(level=logging.INFO)
    
    repo_path = "/home/runner/work/antigravity-workspace-template/antigravity-workspace-template"
    analyzer = RepositoryAnalyzer(repo_path)
    
    # Run analysis
    output_path = "/home/runner/work/antigravity-workspace-template/antigravity-workspace-template/artifacts/repository_analysis.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    summary_path = analyzer.export_report(output_path)
    
    print(f"\n✅ Analysis complete!")
    print(f"📊 Full report: {output_path}")
    print(f"📝 Summary: {summary_path}")
    
    return analyzer


if __name__ == "__main__":
    analyze_current_repository()
