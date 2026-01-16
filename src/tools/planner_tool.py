"""
Planner Tool for Research Paper Workflow Management.

Helps organize and plan research tasks, milestones, and paper writing workflow.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import json


def create_research_plan(
    topic: str,
    deadline: Optional[str] = None,
    paper_type: str = "conference"
) -> Dict[str, Any]:
    """
    Creates a comprehensive research plan with milestones and tasks.
    
    Args:
        topic: Research topic or paper title
        deadline: Target deadline (ISO format date, e.g., "2024-12-31")
        paper_type: Type of paper ("conference", "journal", "workshop")
        
    Returns:
        Structured research plan with phases and tasks
    """
    today = datetime.now()
    
    # Calculate timeline based on paper type
    if paper_type == "conference":
        duration_weeks = 12
    elif paper_type == "journal":
        duration_weeks = 20
    else:  # workshop
        duration_weeks = 8
    
    if deadline:
        try:
            target_date = datetime.fromisoformat(deadline)
        except ValueError:
            return {
                "error": f"Invalid deadline format: {deadline}. Use ISO format (YYYY-MM-DD)"
            }
    else:
        target_date = today + timedelta(weeks=duration_weeks)
    
    plan = {
        "research_topic": topic,
        "paper_type": paper_type,
        "start_date": today.strftime("%Y-%m-%d"),
        "target_deadline": target_date.strftime("%Y-%m-%d"),
        "duration_weeks": duration_weeks,
        "phases": []
    }
    
    # Phase 1: Literature Review (20% of time)
    phase1_end = today + timedelta(weeks=duration_weeks * 0.2)
    plan["phases"].append({
        "phase": 1,
        "name": "Literature Review & Background Research",
        "start": today.strftime("%Y-%m-%d"),
        "end": phase1_end.strftime("%Y-%m-%d"),
        "tasks": [
            {
                "task": "Search and collect relevant papers",
                "tools": ["brave-search", "puppeteer", "github"],
                "status": "pending"
            },
            {
                "task": "Read and annotate key papers (minimum 15-20 papers)",
                "tools": ["memory", "filesystem"],
                "status": "pending"
            },
            {
                "task": "Identify research gap",
                "tools": ["memory", "analysis"],
                "status": "pending"
            },
            {
                "task": "Define research question and objectives",
                "tools": ["planner"],
                "status": "pending"
            }
        ]
    })
    
    # Phase 2: Methodology & Design (25% of time)
    phase2_start = phase1_end
    phase2_end = phase2_start + timedelta(weeks=duration_weeks * 0.25)
    plan["phases"].append({
        "phase": 2,
        "name": "Methodology Design & Implementation Planning",
        "start": phase2_start.strftime("%Y-%m-%d"),
        "end": phase2_end.strftime("%Y-%m-%d"),
        "tasks": [
            {
                "task": "Design research methodology",
                "tools": ["planner", "memory"],
                "status": "pending"
            },
            {
                "task": "Plan experiments and data collection",
                "tools": ["planner"],
                "status": "pending"
            },
            {
                "task": "Setup code repository and development environment",
                "tools": ["github", "filesystem"],
                "status": "pending"
            },
            {
                "task": "Implement baseline approaches",
                "tools": ["context7", "github"],
                "status": "pending"
            }
        ]
    })
    
    # Phase 3: Implementation & Experimentation (30% of time)
    phase3_start = phase2_end
    phase3_end = phase3_start + timedelta(weeks=duration_weeks * 0.30)
    plan["phases"].append({
        "phase": 3,
        "name": "Implementation & Experimentation",
        "start": phase3_start.strftime("%Y-%m-%d"),
        "end": phase3_end.strftime("%Y-%m-%d"),
        "tasks": [
            {
                "task": "Implement proposed approach",
                "tools": ["context7", "github", "filesystem"],
                "status": "pending"
            },
            {
                "task": "Run experiments and collect data",
                "tools": ["execution", "filesystem"],
                "status": "pending"
            },
            {
                "task": "Perform cross-analysis with baselines",
                "tools": ["research_tools"],
                "status": "pending"
            },
            {
                "task": "Document results and create visualizations",
                "tools": ["filesystem", "memory"],
                "status": "pending"
            }
        ]
    })
    
    # Phase 4: Paper Writing (20% of time)
    phase4_start = phase3_end
    phase4_end = phase4_start + timedelta(weeks=duration_weeks * 0.20)
    plan["phases"].append({
        "phase": 4,
        "name": "Paper Writing & Drafting",
        "start": phase4_start.strftime("%Y-%m-%d"),
        "end": phase4_end.strftime("%Y-%m-%d"),
        "tasks": [
            {
                "task": "Write first draft (Introduction, Related Work, Methodology)",
                "tools": ["memory", "filesystem"],
                "status": "pending"
            },
            {
                "task": "Write Results and Discussion sections",
                "tools": ["research_tools", "filesystem"],
                "status": "pending"
            },
            {
                "task": "Write Abstract and Conclusion",
                "tools": ["memory", "filesystem"],
                "status": "pending"
            },
            {
                "task": "Create figures, tables, and citations",
                "tools": ["filesystem"],
                "status": "pending"
            }
        ]
    })
    
    # Phase 5: Review & Refinement (5% of time)
    phase5_start = phase4_end
    phase5_end = target_date
    plan["phases"].append({
        "phase": 5,
        "name": "Review, Revision & Submission",
        "start": phase5_start.strftime("%Y-%m-%d"),
        "end": phase5_end.strftime("%Y-%m-%d"),
        "tasks": [
            {
                "task": "Perform self-review and negative analysis",
                "tools": ["research_tools"],
                "status": "pending"
            },
            {
                "task": "Address limitations and strengthen arguments",
                "tools": ["memory", "research_tools"],
                "status": "pending"
            },
            {
                "task": "Proofread and format according to venue guidelines",
                "tools": ["filesystem"],
                "status": "pending"
            },
            {
                "task": "Final submission",
                "tools": ["filesystem"],
                "status": "pending"
            }
        ]
    })
    
    plan["created_at"] = datetime.now().isoformat()
    
    # Save plan as artifact
    save_plan_artifact(plan)
    
    return plan


def update_task_status(plan: Dict[str, Any], phase: int, task_index: int, status: str) -> Dict[str, Any]:
    """
    Updates the status of a specific task in the research plan.
    
    Args:
        plan: The research plan dictionary
        phase: Phase number (1-5)
        task_index: Index of the task within the phase (0-based)
        status: New status ("pending", "in_progress", "completed", "blocked")
        
    Returns:
        Updated research plan
    """
    valid_statuses = ["pending", "in_progress", "completed", "blocked"]
    
    if status not in valid_statuses:
        return {"error": f"Invalid status. Must be one of: {valid_statuses}"}
    
    if phase < 1 or phase > len(plan["phases"]):
        return {"error": f"Invalid phase number. Must be between 1 and {len(plan['phases'])}"}
    
    phase_data = plan["phases"][phase - 1]
    
    if task_index < 0 or task_index >= len(phase_data["tasks"]):
        return {"error": f"Invalid task index. Must be between 0 and {len(phase_data['tasks']) - 1}"}
    
    phase_data["tasks"][task_index]["status"] = status
    phase_data["tasks"][task_index]["updated_at"] = datetime.now().isoformat()
    
    # Save updated plan
    save_plan_artifact(plan)
    
    return plan


def get_plan_progress(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates overall progress of the research plan.
    
    Args:
        plan: The research plan dictionary
        
    Returns:
        Progress statistics
    """
    total_tasks = 0
    completed_tasks = 0
    in_progress_tasks = 0
    blocked_tasks = 0
    
    phase_progress = []
    
    for phase in plan["phases"]:
        phase_total = len(phase["tasks"])
        phase_completed = sum(1 for task in phase["tasks"] if task["status"] == "completed")
        phase_in_progress = sum(1 for task in phase["tasks"] if task["status"] == "in_progress")
        phase_blocked = sum(1 for task in phase["tasks"] if task["status"] == "blocked")
        
        total_tasks += phase_total
        completed_tasks += phase_completed
        in_progress_tasks += phase_in_progress
        blocked_tasks += phase_blocked
        
        phase_progress.append({
            "phase": phase["phase"],
            "name": phase["name"],
            "total_tasks": phase_total,
            "completed": phase_completed,
            "in_progress": phase_in_progress,
            "blocked": phase_blocked,
            "completion_percentage": (phase_completed / phase_total * 100) if phase_total > 0 else 0
        })
    
    overall_completion = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "blocked_tasks": blocked_tasks,
        "pending_tasks": total_tasks - completed_tasks - in_progress_tasks - blocked_tasks,
        "overall_completion_percentage": overall_completion,
        "phase_progress": phase_progress,
        "on_track": overall_completion >= calculate_expected_progress(plan),
        "checked_at": datetime.now().isoformat()
    }


def calculate_expected_progress(plan: Dict[str, Any]) -> float:
    """
    Calculates expected progress based on timeline.
    
    Args:
        plan: The research plan dictionary
        
    Returns:
        Expected completion percentage
    """
    try:
        start_date = datetime.fromisoformat(plan["start_date"])
        end_date = datetime.fromisoformat(plan["target_deadline"])
    except (ValueError, KeyError) as e:
        # Invalid or missing dates in plan
        return 0.0
    
    today = datetime.now()
    
    if today < start_date:
        return 0.0
    if today >= end_date:
        return 100.0
    
    total_duration = (end_date - start_date).days
    elapsed_duration = (today - start_date).days
    
    expected_progress = (elapsed_duration / total_duration * 100) if total_duration > 0 else 0.0
    
    return expected_progress


def add_task_to_plan(
    plan: Dict[str, Any],
    phase: int,
    task_description: str,
    tools: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Adds a new task to a specific phase in the research plan.
    
    Args:
        plan: The research plan dictionary
        phase: Phase number (1-5)
        task_description: Description of the task
        tools: List of tools needed for the task
        
    Returns:
        Updated research plan
    """
    if phase < 1 or phase > len(plan["phases"]):
        return {"error": f"Invalid phase number. Must be between 1 and {len(plan['phases'])}"}
    
    if tools is None:
        tools = []
    
    new_task = {
        "task": task_description,
        "tools": tools,
        "status": "pending",
        "added_at": datetime.now().isoformat()
    }
    
    plan["phases"][phase - 1]["tasks"].append(new_task)
    
    # Save updated plan
    save_plan_artifact(plan)
    
    return plan


def save_plan_artifact(plan: Dict[str, Any]) -> str:
    """
    Saves research plan to artifacts directory.
    
    Args:
        plan: The research plan dictionary
        
    Returns:
        Path to saved plan file
    """
    artifacts_dir = Path("artifacts/plans")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # Use topic as filename
    topic_slug = plan["research_topic"].replace(" ", "_").lower()[:50]
    filename = f"research_plan_{topic_slug}.json"
    
    filepath = artifacts_dir / filename
    filepath.write_text(json.dumps(plan, indent=2))
    
    return str(filepath)


def load_latest_plan() -> Optional[Dict[str, Any]]:
    """
    Loads the most recently modified research plan.
    
    Returns:
        Research plan dictionary or None if no plans exist
    """
    artifacts_dir = Path("artifacts/plans")
    
    if not artifacts_dir.exists():
        return None
    
    plan_files = list(artifacts_dir.glob("research_plan_*.json"))
    
    if not plan_files:
        return None
    
    # Get most recent file
    latest_file = max(plan_files, key=lambda p: p.stat().st_mtime)
    
    return json.loads(latest_file.read_text())


def generate_daily_tasks(plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates recommended daily tasks based on current plan progress.
    
    Args:
        plan: The research plan dictionary
        
    Returns:
        List of recommended tasks for today
    """
    progress = get_plan_progress(plan)
    today = datetime.now()
    
    # Find current phase based on dates
    current_phase = None
    for phase in plan["phases"]:
        try:
            phase_start = datetime.fromisoformat(phase["start"])
            phase_end = datetime.fromisoformat(phase["end"])
            if phase_start <= today <= phase_end:
                current_phase = phase
                break
        except (ValueError, KeyError):
            # Skip phases with invalid dates
            continue
    
    if not current_phase:
        return [{"message": "No active phase found. Check your plan timeline."}]
    
    # Get pending and in-progress tasks from current phase
    daily_tasks = []
    
    # Priority 1: Blocked tasks that need attention
    for task in current_phase["tasks"]:
        if task["status"] == "blocked":
            daily_tasks.append({
                "priority": "HIGH",
                "task": f"Unblock: {task['task']}",
                "tools": task["tools"],
                "phase": current_phase["name"]
            })
    
    # Priority 2: In-progress tasks
    for task in current_phase["tasks"]:
        if task["status"] == "in_progress":
            daily_tasks.append({
                "priority": "MEDIUM",
                "task": f"Continue: {task['task']}",
                "tools": task["tools"],
                "phase": current_phase["name"]
            })
    
    # Priority 3: Pending tasks (up to 3)
    pending_count = 0
    for task in current_phase["tasks"]:
        if task["status"] == "pending" and pending_count < 3:
            daily_tasks.append({
                "priority": "MEDIUM",
                "task": f"Start: {task['task']}",
                "tools": task["tools"],
                "phase": current_phase["name"]
            })
            pending_count += 1
    
    if not daily_tasks:
        daily_tasks.append({
            "priority": "LOW",
            "task": "All tasks in current phase are completed. Review progress or move to next phase.",
            "tools": ["planner"],
            "phase": current_phase["name"]
        })
    
    return daily_tasks
