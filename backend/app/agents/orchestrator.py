"""Orchestrator agent - coordinates all tasks and agents."""
from typing import Dict, Any, Optional, List
from openai import OpenAI
import json
from datetime import datetime

from app.settings import settings
from app.core.task_graph import BusinessRun, Task, TaskStatus
from app.core.permissions import permission_manager


class OrchestratorAgent:
    """Main orchestrator that plans and coordinates task execution."""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        self.model = settings.openai_model
        self.max_iterations = settings.max_agent_iterations
    
    def plan_execution(self, goal: str, constraints: Dict[str, Any]) -> BusinessRun:
        """Create an execution plan for the given goal."""
        from app.core.task_graph import create_default_task_graph
        
        workspace_path = f"{settings.workspace_path}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        artifacts_path = f"{settings.artifacts_path}/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Create default task graph
        run = create_default_task_graph(goal, workspace_path, artifacts_path)
        
        # Optionally: Use LLM to customize the plan based on constraints
        # For now, we use the standard plan
        
        return run
    
    def execute_task(
        self,
        task: Task,
        context: Dict[str, Any],
        prompts: Dict[str, str]
    ) -> Dict[str, Any]:
        """Execute a single task using the appropriate agent and tools."""
        
        # Get the prompt for this task
        prompt_text = prompts.get(task.prompt_id, "")
        
        # Build the system message
        system_message = self._build_system_message(task, context)
        
        # Build the user message with context
        user_message = self._build_user_message(task, context, prompt_text)
        
        # Execute with LLM
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = self._call_llm(messages)
        
        # Parse response and extract structured outputs
        outputs = self._parse_response(response, task)
        
        return outputs
    
    def _build_system_message(self, task: Task, context: Dict[str, Any]) -> str:
        """Build system message for the agent."""
        permissions = permission_manager.get_agent_permissions(task.agent_name or "orchestrator")
        
        system_msg = f"""You are the {task.agent_name or 'orchestrator'} agent in the Founder Autopilot system.

Your role: {task.description}

Available tools: {', '.join(permissions)}

Guidelines:
- Be practical and implementation-focused
- Optimize for automation and low-touch operations
- Consider real-world constraints and risks
- Provide specific, actionable outputs
- Use clear structure and formatting
- Avoid fluff and generic advice

Current task: {task.title}
"""
        return system_msg
    
    def _build_user_message(
        self,
        task: Task,
        context: Dict[str, Any],
        prompt_text: str
    ) -> str:
        """Build user message with context and prompt."""
        
        # Include relevant context from previous tasks
        context_str = ""
        if context:
            context_str = "\n\nContext from previous tasks:\n"
            for key, value in context.items():
                if isinstance(value, (dict, list)):
                    context_str += f"\n{key}:\n{json.dumps(value, indent=2)}\n"
                else:
                    context_str += f"\n{key}: {value}\n"
        
        # Include task inputs
        inputs_str = ""
        if task.inputs:
            inputs_str = "\n\nTask inputs:\n" + json.dumps(task.inputs, indent=2)
        
        user_msg = f"""{prompt_text}

{context_str}

{inputs_str}

Please provide your response in a structured format that can be easily parsed and used by subsequent tasks.
"""
        return user_msg
    
    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """Call the LLM with the given messages."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}")
    
    def _parse_response(self, response: str, task: Task) -> Dict[str, Any]:
        """Parse LLM response into structured outputs."""
        # Try to extract JSON if present
        outputs = {"raw_response": response}
        
        # Look for JSON blocks
        if "```json" in response:
            try:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
                parsed = json.loads(json_str)
                outputs.update(parsed)
            except Exception:
                pass
        
        # Extract markdown sections
        outputs["sections"] = self._extract_sections(response)
        
        return outputs
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """Extract markdown sections from text."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in text.split("\n"):
            if line.startswith("# ") or line.startswith("## "):
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                
                # Start new section
                current_section = line.lstrip("#").strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()
        
        return sections
    
    def should_continue(self, run: BusinessRun) -> bool:
        """Determine if execution should continue."""
        if run.status in ["completed", "failed", "cancelled"]:
            return False
        
        next_task = run.get_next_task()
        return next_task is not None
    
    def get_next_action(self, run: BusinessRun) -> Optional[Task]:
        """Get the next task to execute."""
        return run.get_next_task()
