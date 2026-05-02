> ⚠️ **DEPRECATED — superseded by [LaunchOpsPro](https://github.com/Gnoscenti/LaunchOpsPro).** See [DEPRECATED.md](DEPRECATED.md) for the migration note. The content below is preserved for historical reference.

---

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
│   │   ├── business_builder.py    # Business strategy agent
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

## Migration Path

For every concept in this repo, the canonical home is now LaunchOpsPro:

| Founder Autopilot | LaunchOpsPro |
|---|---|
| `backend/app/agents/` | `agents/` (17 agents) |
| `backend/app/core/task_graph.py` | `core/task_graph.py` + `core/orchestrator.py` |
| `backend/app/core/vault.py` | `core/credentials.py` (Fernet-encrypted) |
| `backend/app/core/permissions.py` | `core/permissions.py` |
| `backend/app/tools/` | `tools/` + agent-level integrations |
| `frontend/` (React + Vite) | `dashboard/` (React + Generative UI) |
| `business_prompts.json` (30) | Embedded across agent prompts |
| (none) | ProofGuard governance, MCP gateway, HITL approval |

## License

MIT License — see LICENSE.

---

_This repository is no longer accepting feature work. File new issues at [LaunchOpsPro](https://github.com/Gnoscenti/LaunchOpsPro/issues)._
