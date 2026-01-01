# Architecture Documentation

## System Overview

Founder Autopilot is a **task orchestrator** with **agent-based architecture** designed to automate the process of building and launching online businesses.

## Core Concepts

### 1. Task Graph

The system uses a **directed acyclic graph (DAG)** to represent business-building tasks:

- **Nodes**: Individual tasks (e.g., "Generate business concepts", "Write landing page copy")
- **Edges**: Dependencies between tasks (Task B depends on Task A)
- **State**: Each task tracks status (pending, running, completed, failed)

```python
class Task:
    id: str
    type: TaskType
    status: TaskStatus
    dependencies: List[str]
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    artifacts: List[str]
```

### 2. Orchestrator Pattern

The **Orchestrator Agent** coordinates all other agents:

1. **Plan**: Creates execution plan based on goal and constraints
2. **Schedule**: Determines next task based on dependencies
3. **Delegate**: Assigns tasks to specialized agents
4. **Monitor**: Tracks progress and handles failures
5. **Resume**: Can resume interrupted runs

### 3. Agent Specialization

Each agent is specialized for a domain:

- **Business Builder**: Strategy, positioning, offers
- **Web Dev**: Website architecture, code generation
- **Stripe Agent**: Payment setup, subscription management
- **Marketing**: Go-to-market, SEO, email campaigns
- **Reviewer**: Quality assurance, critique, improvements

### 4. Tool Plugins

Tools provide capabilities to agents:

- **Filesystem**: Read/write files, manage directories
- **Shell**: Execute commands (npm, git, deployment)
- **Git**: Version control operations
- **Stripe**: Payment API integration
- **Playwright**: Browser automation for services without APIs
- **Email**: Marketing and transactional emails
- **Social**: Social media posting and scheduling

### 5. Permission System

Security through least-privilege access:

- Each agent has explicit tool permissions
- Dangerous operations require human approval
- Filesystem access is sandboxed to workspace

## Data Flow

```
User Input (Goal + Constraints)
    ↓
Orchestrator (Creates Task Graph)
    ↓
Task Queue (Dependency-based scheduling)
    ↓
Agent Selection (Based on task type)
    ↓
Tool Execution (With permissions check)
    ↓
Output Storage (Artifacts + State)
    ↓
Next Task or Completion
```

## State Management

### Run State

```python
class BusinessRun:
    id: str
    status: RunStatus
    current_task_id: Optional[str]
    tasks: List[Task]
    workspace_path: str
    artifacts_path: str
```

### Persistence

- **In-memory**: Current implementation (fast, ephemeral)
- **Filesystem**: JSON snapshots for resume capability
- **Database**: Future implementation for production

## Security Model

### Credential Storage

1. **Vault**: Encrypted storage using Fernet (symmetric encryption)
2. **Key Management**: Separate key file with 0600 permissions
3. **Fallback**: Environment variables for CI/CD

### Tool Permissions

```python
AGENT_PERMISSIONS = {
    "orchestrator": {"filesystem", "shell", "git"},
    "business_builder": {"filesystem"},
    "webdev": {"filesystem", "shell", "git", "playwright"},
    # ...
}
```

### Human-in-the-Loop

Operations requiring approval:
- Git push to remote
- Stripe product/price creation
- Email campaign sending
- Social media posting
- Shell sudo commands

## Prompt Engineering

### Prompt Structure

Each prompt in the library follows a pattern:

1. **Role Definition**: "You are X, your job is Y"
2. **Context**: Relevant information from previous tasks
3. **Task Instructions**: Specific deliverables
4. **Format Requirements**: JSON, Markdown, or structured output
5. **Constraints**: Boundaries and guidelines

### Context Passing

Tasks pass context to dependent tasks:

```python
context = {
    "task_001": {"build_spec": {...}},
    "task_002": {"concepts": [...]},
}
```

## LLM Integration

### OpenAI-Compatible API

The system uses OpenAI's API format, supporting:

- **OpenAI**: Direct API access
- **vLLM**: Local model serving
- **Other providers**: Any OpenAI-compatible endpoint

### Model Configuration

```python
client = OpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_base,
)

response = client.chat.completions.create(
    model=settings.openai_model,
    messages=[...],
    temperature=settings.openai_temperature,
)
```

### Best Practices

1. **Use # in model names**: `Qwen/Qwen2.5-7B-Instruct` (not `Qwen-Qwen2.5-7B-Instruct`)
2. **Set appropriate temperature**: 0.3 for code, 0.7 for creative tasks
3. **Handle rate limits**: Implement retry with exponential backoff
4. **Parse structured output**: Extract JSON from markdown code blocks

## Frontend Architecture

### React + TypeScript + Vite

- **React Router**: Client-side routing
- **TanStack Query**: Server state management
- **Zustand**: Client state (if needed)
- **Tailwind CSS**: Styling
- **Lucide Icons**: Icon library

### API Client

```typescript
export const api = axios.create({
  baseURL: '/api',
  headers: {'Content-Type': 'application/json'},
})
```

### Real-time Updates

- **Polling**: Query refetch every 5 seconds
- **Future**: WebSocket for push updates

## Deployment Architecture

### Development

```
[Frontend:3000] → [Backend:8001] → [vLLM:8000]
```

### Production

```
[Vercel/Netlify] → [Railway/Render] → [OpenAI API]
                                    ↓
                              [External Services]
                              - Stripe
                              - Email Provider
                              - Cloud Storage
```

## Extensibility

### Adding a New Agent

1. Create agent class in `backend/app/agents/`
2. Implement agent methods
3. Add to permission system
4. Register in orchestrator

### Adding a New Tool

1. Create tool class in `backend/app/tools/`
2. Implement tool interface
3. Add permission definitions
4. Update agent permissions

### Adding a New Task Type

1. Add to `TaskType` enum
2. Create task in task graph
3. Assign to appropriate agent
4. Define dependencies

## Performance Considerations

### Latency

- **LLM calls**: 2-30 seconds depending on model and token count
- **Tool operations**: <1 second for most operations
- **Task execution**: Varies by complexity

### Optimization

1. **Parallel execution**: Independent tasks can run concurrently (future)
2. **Caching**: Cache prompt responses for identical inputs
3. **Streaming**: Stream LLM responses for better UX (future)
4. **Model selection**: Use smaller models for simple tasks

## Error Handling

### Retry Strategy

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        result = execute_task()
        break
    except Exception as e:
        if attempt == max_retries - 1:
            mark_failed(task_id, str(e))
        else:
            wait_exponential(attempt)
```

### Failure Recovery

1. **Task-level**: Retry failed tasks
2. **Run-level**: Resume from last successful task
3. **Human intervention**: Request help for persistent failures

## Future Enhancements

1. **Multi-agent collaboration**: Agents work together on complex tasks
2. **Learning from feedback**: Improve prompts based on outcomes
3. **Template library**: Pre-built task graphs for common scenarios
4. **Integration marketplace**: Community-contributed tools and agents
5. **Observability**: Detailed metrics and tracing
