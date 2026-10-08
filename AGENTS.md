# AGENTS.md

## Hacktoberfest Hack Day — Coimbatore 2026

This file is the single source of truth for coding agents working in this repository, including Claude Code, OpenAI Codex, Gemini CLI, Cursor, Windsurf, GitHub Copilot, Aider, RooCode, and other agentic development tools.

Read this file before making changes to the repository.

## 1. Project Context

This repository contains **GemmaLens**, built for **Hacktoberfest Hack Day — Coimbatore 2026**, organized by INIT CLUB × iDEA CLUB in collaboration with Major League Hacking (MLH).

The project is developed as a functional hackathon submission adhering to:
- Open-Source AI Track: meaningful use of open-source or open-weight AI (Google Gemma 4).
- Partner Challenge: Best Use of Gemma 4.
- Agent Skills Open Standard (`https://agentskills.io/specification`).

## 2. Development Principles

Agents working in this repository must:
- Understand the existing project before modifying it.
- Never hardcode API keys, tokens, passwords, or private credentials.
- Keep implementations focused on the hackathon problem.
- Keep commits focused, meaningful, and distributed across the team.
- Do not fabricate functionality, results, benchmarks, integrations, or claims.

## 3. Repository Structure

```text
.
├── LICENSE                        # Apache 2.0 Open Source License
├── README.md                      # Primary hackathon submission documentation
├── AGENTS.md                      # Single source of truth for AI agents
├── CLAUDE.md                      # Claude code entrypoint
├── .gitignore                     # Git ignore rules
├── .env.example                   # Example environment configuration
├── requirements.txt               # Python package dependencies
├── app.py                         # Streamlit multi-tab user interface
├── gemma_engine.py                # Gemma 4 inference engine (API & local Ollama)
├── prompts.py                     # Specialized audit prompts & templates
├── agent_skills.py                # Agent Skills open standard exporter
└── skills/
    └── gemma-auditor/
        └── SKILL.md               # Standard-compliant Agent Skill manifest
```

## 4. Key Model Details
- **Primary Model:** Google Gemma 4 (`gemma-4-26b-a4b-it`) via Google GenAI SDK.
- **Local Fallback:** Ollama running `gemma4:e2b` or `gemma2:2b`.
- **License:** Apache 2.0 Open Weights.
