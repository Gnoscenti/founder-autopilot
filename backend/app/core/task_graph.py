"""Task graph and orchestration state management."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import json


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class TaskType(str, Enum):
    """Types of tasks in the orchestration."""
    INTERVIEW = "interview"
    CONCEPT_GENERATION = "concept_generation"
    VALIDATION = "validation"
    POSITIONING = "positioning"
    OFFER_DESIGN = "offer_design"
    BRAND_CREATION = "brand_creation"
    WEBSITE_COPY = "website_copy"
    PRODUCT_BUILD = "product_build"
    AUTOMATION_SETUP = "automation_setup"
    MARKETING_PLAN = "marketing_plan"
    DEPLOYMENT = "deployment"


class Task(BaseModel):
    """A single task in the execution graph."""
    id: str
    type: TaskType
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = Field(default_factory=list, description="Task IDs that must complete first")
    
    # Execution
    agent_name: Optional[str] = None
    tool_permissions: List[str] = Field(default_factory=list)
    prompt_id: Optional[str] = None
    
    # State
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    # I/O
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    artifacts: List[str] = Field(default_factory=list, description="File paths to generated artifacts")
    
    # Metadata
    iteration_count: int = 0
    tokens_used: int = 0
    cost_usd: float = 0.0


class RunStatus(str, Enum):
    """Overall run status."""
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BusinessRun(BaseModel):
    """A complete business building run."""
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Status
    status: RunStatus = RunStatus.CREATED
    current_task_id: Optional[str] = None
    
    # Business context
    business_spec_id: Optional[str] = None
    goal: str = Field(description="High-level goal, e.g., 'Launch a $10k/mo SaaS'")
    
    # Execution graph
    tasks: List[Task] = Field(default_factory=list)
    
    # Artifacts
    workspace_path: str
    artifacts_path: str
    
    # Metrics
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    
    # Human-in-the-loop
    requires_human_input: bool = False
    human_input_prompt: Optional[str] = None
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_next_task(self) -> Optional[Task]:
        """Get the next task to execute based on dependencies."""
        completed_ids = {t.id for t in self.tasks if t.status == TaskStatus.COMPLETED}
        
        for task in self.tasks:
            if task.status != TaskStatus.PENDING:
                continue
            
            # Check if all dependencies are met
            if all(dep_id in completed_ids for dep_id in task.dependencies):
                return task
        
        return None
    
    def mark_task_completed(self, task_id: str, outputs: Dict[str, Any], artifacts: List[str] = None):
        """Mark a task as completed with outputs."""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.outputs = outputs
            if artifacts:
                task.artifacts = artifacts
            self.updated_at = datetime.utcnow()
    
    def mark_task_failed(self, task_id: str, error: str):
        """Mark a task as failed."""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.error = error
            self.status = RunStatus.FAILED
            self.updated_at = datetime.utcnow()
    
    def to_json(self) -> str:
        """Serialize to JSON."""
        return self.model_dump_json(indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "BusinessRun":
        """Deserialize from JSON."""
        return cls.model_validate_json(json_str)


def create_default_task_graph(goal: str, workspace_path: str, artifacts_path: str) -> BusinessRun:
    """Create a default task graph for business building."""
    run = BusinessRun(
        id=f"run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        goal=goal,
        workspace_path=workspace_path,
        artifacts_path=artifacts_path,
    )
    
    # Define the standard task sequence
    tasks = [
        Task(
            id="task_001",
            type=TaskType.INTERVIEW,
            title="Interview and Build Spec",
            description="Conduct 12-question interview to capture constraints and create Build Spec",
            agent_name="orchestrator",
            prompt_id="prompt_0_setup",
        ),
        Task(
            id="task_002",
            type=TaskType.CONCEPT_GENERATION,
            title="Generate 3 Business Concepts",
            description="Propose 3 optimized business concepts based on Build Spec",
            agent_name="business_builder",
            prompt_id="prompt_1_concepts",
            dependencies=["task_001"],
        ),
        Task(
            id="task_003",
            type=TaskType.VALIDATION,
            title="Validation Plan",
            description="Create 7-day validation plan with testable hypotheses",
            agent_name="business_builder",
            prompt_id="prompt_2_validation",
            dependencies=["task_002"],
        ),
        Task(
            id="task_004",
            type=TaskType.POSITIONING,
            title="Competitive Positioning",
            description="Build competitor map and positioning wedge",
            agent_name="business_builder",
            prompt_id="prompt_3_positioning",
            dependencies=["task_002"],
        ),
        Task(
            id="task_005",
            type=TaskType.OFFER_DESIGN,
            title="Design Core Offer",
            description="Design irresistible offer with boundaries",
            agent_name="business_builder",
            prompt_id="prompt_4_offer",
            dependencies=["task_003", "task_004"],
        ),
        Task(
            id="task_006",
            type=TaskType.BRAND_CREATION,
            title="Brand Identity",
            description="Create brand name, tagline, and identity kit",
            agent_name="business_builder",
            prompt_id="prompt_5_brand",
            dependencies=["task_004"],
        ),
        Task(
            id="task_007",
            type=TaskType.WEBSITE_COPY,
            title="Website Copy",
            description="Write high-converting landing page and pricing page copy",
            agent_name="business_builder",
            prompt_id="prompt_7_home_copy",
            dependencies=["task_005", "task_006"],
        ),
        Task(
            id="task_008",
            type=TaskType.PRODUCT_BUILD,
            title="Product Blueprint",
            description="Create MVP to V2 product roadmap",
            agent_name="business_builder",
            prompt_id="prompt_10_product_blueprint",
            dependencies=["task_005"],
        ),
        Task(
            id="task_009",
            type=TaskType.AUTOMATION_SETUP,
            title="Automation Architecture",
            description="Design automation plan for fulfillment and support",
            agent_name="orchestrator",
            prompt_id="prompt_14_automation_nocode",
            dependencies=["task_008"],
            tool_permissions=["stripe", "email", "filesystem"],
        ),
        Task(
            id="task_010",
            type=TaskType.MARKETING_PLAN,
            title="Go-to-Market Plan",
            description="Choose primary channel and create 60-day execution plan",
            agent_name="marketing",
            prompt_id="prompt_18_channel_focus",
            dependencies=["task_007"],
        ),
        Task(
            id="task_011",
            type=TaskType.DEPLOYMENT,
            title="Deploy Website",
            description="Build and deploy website with Stripe integration",
            agent_name="webdev",
            dependencies=["task_007", "task_009"],
            tool_permissions=["filesystem", "shell", "git", "stripe", "playwright"],
        ),
    ]
    
    run.tasks = tasks
    return run
