# DEPRECATED

**This repository is superseded by [LaunchOpsPro](https://github.com/Gnoscenti/LaunchOpsPro).**

## Why

Founder Autopilot was the predecessor design for what is now the Dynexis launch operating system. Several files in this repo (`PIPELINE_STATUS.md`, `LAUNCH_SEQUENCE.md`, `ROADMAP.md`) share identical SHAs with the LaunchOpsPro versions — they have been migrated and are no longer maintained here.

The canonical implementation in **[LaunchOpsPro](https://github.com/Gnoscenti/LaunchOpsPro)** carries:

- 17 specialized agents (vs the earlier 6-agent design here)
- 10-stage governed Atlas pipeline (formation → infrastructure → legal → payments → funding → coaching → growth → done)
- ProofGuard attestation on every agent action (CQS scoring, IMDA pillars, HITL approval)
- Generative UI dashboard (React + SSE) with inline charts, KPI cards, alerts
- MCP gateway for external agent ecosystem
- 49 unit tests
- Production-ready Docker Compose business infrastructure stack

## What To Do

- **For new development:** build against [LaunchOpsPro](https://github.com/Gnoscenti/LaunchOpsPro).
- **For historical reference:** this repo is preserved as-is.
- **Issues / PRs filed here:** please re-file them against LaunchOpsPro.

This repo will be archived after a 30-day notice window.
