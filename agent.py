"""
============================================================================
Antigravity Workspace Template - Agent Entry Point
============================================================================

PURPOSE:
    Convenience wrapper that allows running the AI agent from the repository
    root directory without navigating to src/. This is a thin entrypoint
    that imports and executes the main GeminiAgent.

WHAT THIS SCRIPT DOES:
    1. Accepts task input from command-line arguments or AGENT_TASK env var
    2. Initializes the GeminiAgent from src/agent.py
    3. Executes the task using Think-Act-Reflect pattern
    4. Ensures proper cleanup and shutdown of agent resources

USAGE:
    # Pass task as command-line arguments
    python agent.py "帮我写一个快速排序算法"
    python agent.py "Write a quick sort algorithm"
    
    # Use environment variable
    export AGENT_TASK="Your task here"
    python agent.py
    
    # Run with default task (weather query)
    python agent.py

REQUIREMENTS:
    - Virtual environment activated (source venv/bin/activate)
    - Dependencies installed (pip install -r requirements.txt)
    - API keys configured in .env file

SEE ALSO:
    - src/agent.py - Main agent implementation
    - docs/en/SCRIPTS.md - Detailed script documentation
    - README.md - Project overview and quick start guide

============================================================================
"""
import os
import sys

from src.agent import GeminiAgent


def main():
    task = " ".join(sys.argv[1:]).strip() or os.environ.get(
        "AGENT_TASK", "帮助我查看今天的天气"
    )

    agent = GeminiAgent()
    try:
        agent.run(task)
    finally:
        agent.shutdown()


if __name__ == "__main__":
    main()
