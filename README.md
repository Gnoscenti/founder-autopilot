# Founder Autopilot

AI-powered business builder orchestrator with agent-based architecture for launching automated online businesses.

## Overview

Founder Autopilot is a task orchestrator system that uses AI agents to guide you through the complete process of building and launching an online business. It combines:

- **30 Business-Building Prompts**: Comprehensive prompt library covering everything from concept generation to scaling
- **Agent-Based Architecture**: Specialized agents for business strategy, web development, marketing, and more
- **Tool Plugins**: Modular tools for filesystem, shell, Git, Stripe, browser automation, and external services
- **State Management**: Tracks execution progress with resumable task graphs
- **Security First**: Encrypted credential vault and permission-based tool access

## Architecture

### Backend (FastAPI + Python)

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── settings.py          # Configuration with OpenAI/vLLM support
│   ├── prompts/
│   │   └── business_prompts.json  # 30 business-building prompts
│   ├── core/
│   │   ├── business_spec.py       # Business specification models
│   │   ├── task_graph.py          # Task orchestration and state
│   │   ├── permissions.py         # Tool access control
│   │   └── vault.py               # Encrypted credential storage
│   ├── agents/
│   │   ├── orchestrator.py        # Main coordinator agent
│   │   ├── business_builder.py   # Business strategy agent
│   │   ├── webdev.py              # Web development agent
│   │   ├── stripe_agent.py        # Payment integration agent
│   │   ├── marketing.py           # Marketing strategy agent
│   │   └── reviewer.py            # Quality assurance agent
│   └── tools/
│       ├── filesystem_tool.py     # File operations
│       ├── shell_tool.py          # Shell command execution
│       ├── git_tool.py            # Version control
│       ├── stripe_tool.py         # Stripe API integration
│       ├── gcloud_tool.py         # Google Cloud operations
│       ├── playwright_tool.py     # Browser automation
│       ├── email_tool.py          # Email marketing
│       └── social_tool.py         # Social media posting
└── data/
    ├── runs.db              # SQLite database for runs
    ├── workspace/           # Working directory for runs
    └── artifacts/           # Generated assets
```

### Frontend (React + TypeScript + Vite)

```
frontend/
├── src/
│   ├── App.tsx              # Main app with routing
│   ├── lib/
│   │   └── api.ts           # API client
│   └── pages/
│       ├── PromptLibrary.tsx    # Browse and use prompts
│       ├── BusinessSpec.tsx     # Define business constraints
│       ├── LaunchRun.tsx        # Start and monitor runs
│       ├── Permissions.tsx      # View agent permissions
│       ├── Connectors.tsx       # Manage integrations
│       └── Logs.tsx             # View execution logs
└── package.json
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key OR vLLM server running locally

### Backend Setup

1. **Install dependencies:**

```bash
cd backend
pip install -e .
```

2. **Configure environment:**

Create a `.env` file in the `backend` directory:

```env
# For vLLM (local model)
OPENAI_API_KEY=EMPTY
OPENAI_API_BASE=http://localhost:8000/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct

# OR for OpenAI API
# OPENAI_API_KEY=sk-...
# OPENAI_API_BASE=https://api.openai.com/v1
# OPENAI_MODEL=gpt-4-turbo-preview

# Optional: External services
STRIPE_API_KEY=sk_test_...
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

3. **Run the backend:**

```bash
cd backend
python -m app.main
```

The API will be available at `http://localhost:8001`

### Frontend Setup

1. **Install dependencies:**

```bash
cd frontend
npm install
```

2. **Run the development server:**

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Using vLLM (Recommended)

To run a local model with vLLM for maximum control and cost savings:

1. **Install vLLM:**

```bash
pip install vllm
```

2. **Start vLLM server:**

```bash
vllm serve Qwen/Qwen2.5-7B-Instruct --dtype auto --port 8000
```

3. **Configure backend to use vLLM** (already set in default `.env`):

```env
OPENAI_API_KEY=EMPTY
OPENAI_API_BASE=http://localhost:8000/v1
OPENAI_MODEL=Qwen/Qwen2.5-7B-Instruct
```

The system uses OpenAI-compatible API, so you can easily switch between vLLM and OpenAI.

## Usage

### 1. Define Your Business Spec

Navigate to **Business Spec** and fill in your constraints:
- Skills and expertise
- Time available
- Budget
- Risk tolerance
- Target income
- Topics of interest

### 2. Browse Prompts

Explore the **Prompt Library** to see all 30 business-building prompts. Each prompt is designed for a specific stage of the business-building process.

### 3. Launch a Run

Go to **Launch Run** and:
1. Enter your business goal (e.g., "Launch a $10k/month SaaS business")
2. Click "Launch Run"
3. The orchestrator will create a task graph with dependencies
4. Click "Execute Next Task" to progress through the plan

### 4. Monitor Progress

- View task status in real-time
- See which agent is working on each task
- Track overall progress percentage
- Review outputs and artifacts

### 5. Configure Connectors

Set up integrations in **Connectors**:
- Stripe (for payments)
- Email provider (for marketing)
- GitHub (for code)
- Vercel/Netlify (for deployment)

## Agent Permissions

Each agent has specific tool permissions to maintain security:

| Agent | Filesystem | Shell | Git | Stripe | Browser | Email | Social |
|-------|-----------|-------|-----|--------|---------|-------|--------|
| orchestrator | ✓ | ✓ | ✓ | | | | |
| business_builder | ✓ | | | | | | |
| webdev | ✓ | ✓ | ✓ | | ✓ | | |
| stripe_agent | ✓ | | | ✓ | ✓ | | |
| marketing | ✓ | | | | ✓ | ✓ | ✓ |
| reviewer | ✓ | | | | | | |

Dangerous operations (git push, Stripe operations, email campaigns) require human approval.

## Security

### Credential Storage

Credentials are stored in an encrypted vault using Fernet encryption:
- Vault file: `backend/data/vault.enc`
- Encryption key: `backend/data/.vault_key` (never commit this!)
- Permissions: 0600 (owner read/write only)

### Tool Permissions

The permission system ensures agents can only access tools they need:
- Read-only operations for most agents
- Write operations require explicit permissions
- Dangerous operations require human approval

## Development

### Adding a New Agent

1. Create agent file in `backend/app/agents/`
2. Define agent permissions in `backend/app/core/permissions.py`
3. Register agent in orchestrator

### Adding a New Tool

1. Create tool file in `backend/app/tools/`
2. Implement tool interface with proper error handling
3. Add tool to permission system
4. Update agent permissions as needed

### Adding a New Prompt

1. Edit `backend/app/prompts/business_prompts.json`
2. Add prompt with unique ID, title, category, and content
3. Restart backend to reload prompts

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Deployment

### Backend

Deploy to any Python hosting service:
- Railway
- Render
- Fly.io
- Google Cloud Run
- AWS Lambda (with Mangum adapter)

### Frontend

Deploy to static hosting:
- Vercel
- Netlify
- Cloudflare Pages
- GitHub Pages

## Roadmap

- [ ] Database persistence (replace in-memory storage)
- [ ] WebSocket support for real-time updates
- [ ] Human-in-the-loop approval UI
- [ ] Browser session persistence for authenticated services
- [ ] Multi-model support (switch between models per task)
- [ ] Artifact gallery and export
- [ ] Run templates and presets
- [ ] Collaboration features (team access)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions or issues:
- Open an issue on GitHub
- Check the documentation
- Review example runs in the logs

---

**Built with ❤️ for founders who want to automate the boring parts of building a business.**
