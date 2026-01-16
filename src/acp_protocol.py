"""
Agent Context Protocol (ACP) - Coordination Layer for Autonomous Agents.

ACP provides a standardized protocol for agents to:
- Share context and knowledge
- Coordinate tasks and workflows
- Communicate findings and results
- Maintain consistency across the research pipeline

This is the autonomous layer that makes all agents work together seamlessly.
"""

import json
import asyncio
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from pathlib import Path
from enum import Enum
import hashlib


class AgentRole(Enum):
    """Standard agent roles in the research workflow."""
    RESEARCHER = "researcher"  # Literature review, paper discovery
    ANALYZER = "analyzer"  # Data analysis, cross-analysis
    CODER = "coder"  # Code implementation and review
    WRITER = "writer"  # Paper writing and documentation
    REVIEWER = "reviewer"  # Quality control and critique
    COORDINATOR = "coordinator"  # Workflow orchestration


class MessageType(Enum):
    """ACP message types."""
    TASK = "task"  # Task assignment
    RESULT = "result"  # Task result
    QUERY = "query"  # Information request
    RESPONSE = "response"  # Query response
    CONTEXT = "context"  # Context sharing
    STATUS = "status"  # Status update


class ACPMessage:
    """Standard ACP message format."""
    
    def __init__(
        self,
        message_type: MessageType,
        sender: str,
        receiver: str,
        content: Any,
        context: Optional[Dict[str, Any]] = None,
        priority: int = 5
    ):
        self.id = self._generate_id()
        self.type = message_type
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.context = context or {}
        self.priority = priority
        self.timestamp = datetime.now().isoformat()
    
    def _generate_id(self) -> str:
        """Generate unique message ID."""
        data = f"{datetime.now().isoformat()}:{id(self)}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "context": self.context,
            "priority": self.priority,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ACPMessage':
        """Create message from dictionary."""
        msg = cls(
            message_type=MessageType(data["type"]),
            sender=data["sender"],
            receiver=data["receiver"],
            content=data["content"],
            context=data.get("context"),
            priority=data.get("priority", 5)
        )
        msg.id = data["id"]
        msg.timestamp = data["timestamp"]
        return msg


class ACPAgent:
    """
    Base class for ACP-compatible agents.
    
    All agents in the system inherit from this class to ensure
    they can communicate via ACP and use the unified Antigravity API.
    """
    
    def __init__(
        self,
        role: AgentRole,
        name: str,
        capabilities: List[str],
        gateway: Optional[Any] = None
    ):
        self.role = role
        self.name = name
        self.capabilities = capabilities
        self.gateway = gateway
        self.inbox: List[ACPMessage] = []
        self.outbox: List[ACPMessage] = []
        self.context = {}
        self.active = True
        
        print(f"🤖 ACP Agent initialized: {name} ({role.value})")
        print(f"   Capabilities: {', '.join(capabilities)}")
    
    async def send_message(self, message: ACPMessage):
        """Send message to another agent."""
        self.outbox.append(message)
        print(f"📤 {self.name} → {message.receiver}: {message.type.value}")
    
    async def receive_message(self, message: ACPMessage):
        """Receive message from another agent."""
        self.inbox.append(message)
        print(f"📥 {self.name} ← {message.sender}: {message.type.value}")
        await self.process_message(message)
    
    async def process_message(self, message: ACPMessage):
        """Process received message (override in subclasses)."""
        pass
    
    def update_context(self, key: str, value: Any):
        """Update agent's context."""
        self.context[key] = value
    
    def get_context(self, key: str) -> Optional[Any]:
        """Get context value."""
        return self.context.get(key)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using Antigravity API (override in subclasses)."""
        raise NotImplementedError


class ACPCoordinator:
    """
    Central coordinator for ACP agents.
    
    Manages agent registration, message routing, and workflow orchestration.
    Uses the Antigravity API Gateway for all AI operations.
    """
    
    def __init__(self, gateway: Optional[Any] = None):
        from src.antigravity_gateway import get_gateway
        
        self.gateway = gateway or get_gateway()
        self.agents: Dict[str, ACPAgent] = {}
        self.message_queue: List[ACPMessage] = []
        self.workflow_history: List[Dict[str, Any]] = []
        
        print("🌐 ACP Coordinator initialized")
        print(f"   Using Antigravity API Gateway: {self.gateway}")
    
    def register_agent(self, agent: ACPAgent):
        """Register an agent with the coordinator."""
        self.agents[agent.name] = agent
        agent.gateway = self.gateway
        print(f"✓ Registered agent: {agent.name} ({agent.role.value})")
    
    async def route_message(self, message: ACPMessage):
        """Route message to target agent."""
        if message.receiver in self.agents:
            await self.agents[message.receiver].receive_message(message)
        elif message.receiver == "broadcast":
            # Broadcast to all agents
            for agent in self.agents.values():
                if agent.name != message.sender:
                    await agent.receive_message(message)
        else:
            print(f"⚠️ Agent not found: {message.receiver}")
    
    async def process_queue(self):
        """Process all pending messages."""
        # Sort by priority (higher first)
        self.message_queue.sort(key=lambda m: m.priority, reverse=True)
        
        while self.message_queue:
            message = self.message_queue.pop(0)
            await self.route_message(message)
    
    async def coordinate_research_workflow(
        self,
        research_topic: str,
        phases: List[str] = None
    ) -> Dict[str, Any]:
        """
        Coordinate a complete research workflow across multiple agents.
        
        Args:
            research_topic: Topic to research
            phases: Research phases to execute
            
        Returns:
            Workflow results
        """
        if phases is None:
            phases = [
                "literature_review",
                "methodology_design",
                "implementation",
                "analysis",
                "writing"
            ]
        
        workflow_start = datetime.now()
        results = {
            "topic": research_topic,
            "phases": {},
            "start_time": workflow_start.isoformat()
        }
        
        print(f"\n🚀 Starting autonomous research workflow: {research_topic}")
        print(f"   Phases: {', '.join(phases)}")
        
        # Phase 1: Literature Review
        if "literature_review" in phases:
            print("\n📚 Phase 1: Literature Review")
            if "researcher" in [a.role.value for a in self.agents.values()]:
                researcher = next(a for a in self.agents.values() if a.role == AgentRole.RESEARCHER)
                task = ACPMessage(
                    MessageType.TASK,
                    "coordinator",
                    researcher.name,
                    {
                        "action": "literature_review",
                        "topic": research_topic,
                        "count": 20
                    }
                )
                await researcher.receive_message(task)
                lit_review = await researcher.execute_task(task.content)
                results["phases"]["literature_review"] = lit_review
        
        # Phase 2: Analysis
        if "analysis" in phases:
            print("\n🔬 Phase 2: Analysis")
            if "analyzer" in [a.role.value for a in self.agents.values()]:
                analyzer = next(a for a in self.agents.values() if a.role == AgentRole.ANALYZER)
                task = ACPMessage(
                    MessageType.TASK,
                    "coordinator",
                    analyzer.name,
                    {
                        "action": "cross_analysis",
                        "topic": research_topic,
                        "data": results["phases"].get("literature_review", {})
                    }
                )
                await analyzer.receive_message(task)
                analysis = await analyzer.execute_task(task.content)
                results["phases"]["analysis"] = analysis
        
        # Phase 3: Implementation
        if "implementation" in phases:
            print("\n💻 Phase 3: Implementation")
            if "coder" in [a.role.value for a in self.agents.values()]:
                coder = next(a for a in self.agents.values() if a.role == AgentRole.CODER)
                task = ACPMessage(
                    MessageType.TASK,
                    "coordinator",
                    coder.name,
                    {
                        "action": "implement",
                        "topic": research_topic,
                        "requirements": results["phases"].get("analysis", {})
                    }
                )
                await coder.receive_message(task)
                implementation = await coder.execute_task(task.content)
                results["phases"]["implementation"] = implementation
        
        # Phase 4: Writing
        if "writing" in phases:
            print("\n✍️ Phase 4: Paper Writing")
            if "writer" in [a.role.value for a in self.agents.values()]:
                writer = next(a for a in self.agents.values() if a.role == AgentRole.WRITER)
                task = ACPMessage(
                    MessageType.TASK,
                    "coordinator",
                    writer.name,
                    {
                        "action": "write_paper",
                        "topic": research_topic,
                        "content": results["phases"]
                    }
                )
                await writer.receive_message(task)
                paper = await writer.execute_task(task.content)
                results["phases"]["writing"] = paper
        
        # Phase 5: Review
        if "reviewer" in [a.role.value for a in self.agents.values()]:
            print("\n🔍 Final Review")
            reviewer = next(a for a in self.agents.values() if a.role == AgentRole.REVIEWER)
            task = ACPMessage(
                MessageType.TASK,
                "coordinator",
                reviewer.name,
                {
                    "action": "review",
                    "content": results
                }
            )
            await reviewer.receive_message(task)
            review = await reviewer.execute_task(task.content)
            results["review"] = review
        
        workflow_end = datetime.now()
        results["end_time"] = workflow_end.isoformat()
        results["duration_seconds"] = (workflow_end - workflow_start).total_seconds()
        
        # Save workflow history
        self.workflow_history.append(results)
        self._save_workflow_history()
        
        print(f"\n✅ Research workflow completed in {results['duration_seconds']:.1f}s")
        return results
    
    def _save_workflow_history(self):
        """Save workflow history to disk."""
        history_file = Path("artifacts/workflows/acp_history.json")
        history_file.parent.mkdir(parents=True, exist_ok=True)
        history_file.write_text(json.dumps(self.workflow_history, indent=2))
    
    def get_agent_by_role(self, role: AgentRole) -> Optional[ACPAgent]:
        """Get first agent with specified role."""
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        return None
    
    def get_all_agents_by_role(self, role: AgentRole) -> List[ACPAgent]:
        """Get all agents with specified role."""
        return [agent for agent in self.agents.values() if agent.role == role]


# Convenience functions
async def create_research_workflow(
    topic: str,
    gateway: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Create and execute a complete autonomous research workflow.
    
    Args:
        topic: Research topic
        gateway: Antigravity API Gateway instance
        
    Returns:
        Workflow results
    """
    coordinator = ACPCoordinator(gateway)
    
    # Register default agents
    from src.tools.autonomous_agents import (
        ResearchAgent, AnalyzerAgent, CoderAgent, 
        WriterAgent, ReviewerAgent
    )
    
    coordinator.register_agent(ResearchAgent("researcher_1", gateway))
    coordinator.register_agent(AnalyzerAgent("analyzer_1", gateway))
    coordinator.register_agent(CoderAgent("coder_1", gateway))
    coordinator.register_agent(WriterAgent("writer_1", gateway))
    coordinator.register_agent(ReviewerAgent("reviewer_1", gateway))
    
    # Execute workflow
    return await coordinator.coordinate_research_workflow(topic)
