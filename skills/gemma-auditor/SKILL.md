---
name: gemma-architecture-auditor
description: Audits cloud topologies, whiteboard diagrams, and code snippets for single points of failure, security risks, and generates Docker Compose infrastructure.
author: Team GemmaLens (Hacktoberfest Hack Day Coimbatore 2026)
version: 1.0.0
license: Apache-2.0
standard: https://agentskills.io/specification
---

# Gemma Architecture & Code Auditor Skill

An open-standard Agent Skill powered by Google Gemma 4 (26B MoE open-weight model).

## When to Use This Skill
Activate this skill whenever a user:
1. Provides a handwritten or drawn system architecture diagram and needs an infrastructure review.
2. Needs automated Docker Compose or Terraform scaffolding derived directly from a topology sketch.
3. Submits low-level C / Rust pointer operations or network services requiring memory safety verification.

## Execution Workflow
1. Ingest visual artifact (PNG, JPG, SVG) or text specification.
2. Dispatch query to `gemma-4-26b-a4b-it` with `thinking_level="high"`.
3. Synthesize findings into:
   - Component discovery table
   - Single Points of Failure (SPOF) list
   - Recommended Docker Compose / Kubernetes manifest
   - Reliability scorecard
4. Return validated Markdown report to caller.
