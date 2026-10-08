# AGENTS.md

## Hacktoberfest Hack Day — Coimbatore 2026

This file is the single source of truth for coding agents working in this repository, including Claude Code, OpenAI Codex, Gemini CLI, Cursor, Windsurf, GitHub Copilot, Aider, RooCode, and other agentic development tools.

Read this file before making changes to the repository.

## 1. Project Context

This repository contains **MandiShield: The Autonomous Counterfeit Pesticide & Spurious Seed Audit Engine**, built for **Hacktoberfest Hack Day — Coimbatore 2026**, organized by INIT CLUB × iDEA CLUB in collaboration with Major League Hacking (MLH) and Google DeepMind.

The project is developed as a functional hackathon submission adhering to:
- **Main Track:** Best Open-Source AI Project (DigitalOcean)
- **Partner Challenge:** Best Use of Gemma 4 (Google DeepMind)
- **Agent Standard:** Agent Skills Open Standard (`https://agentskills.io/specification`)

## 2. Development Principles

Agents working in this repository must:
- Understand the existing project before modifying it.
- Never hardcode API keys, tokens, passwords, or private credentials.
- Keep implementations focused on the real-world agricultural fraud crisis in rural India.
- Keep commits focused, meaningful, and distributed across all 4 team members.
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
├── app.py                         # Streamlit multi-tab agricultural interface
├── agri_db.py                     # Statutory CIB&RC & Seeds Act 1966 database
├── gemma_engine.py                # Dual Gemma 4 inference engine (API & local Ollama)
├── prompts.py                     # Specialized forensic audit prompts & templates
├── agent_skills.py                # Agent Skills open standard exporter
├── skills/
│   └── mandishield/
│       └── SKILL.md               # Standard-compliant Agent Skill manifest
├── examples/                      # Synthetic high-resolution test samples
│   ├── counterfeit_pesticide_sample.png
│   ├── genuine_pesticide_sample.png
│   └── spurious_seeds_sample.png
└── tests/
    └── test_mandishield.py        # Passing unit test suite (5/5)
```

## 4. Key Model Details
- **Primary Model:** Google Gemma 4 (`gemma-4-26b-a4b-it`) via Google GenAI SDK with thinking mode enabled.
- **Local Fallback:** Ollama running `gemma4:e2b` (100% offline edge inference for rural mandis).
- **License:** Apache 2.0 Open Weights.
