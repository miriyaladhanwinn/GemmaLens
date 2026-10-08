"""
Agent Skills Open Standard Exporter
Author: Shasank Paruchuri (paruchurishasank04@gmail.com)
Standard: https://agentskills.io/specification
License: Apache-2.0
"""

import os
from typing import Dict, Any

class AgentSkillPackage:
    """
    Manages packaging and validation of Agent Skills conforming
    to the Agent Skills open standard.
    """
    @staticmethod
    def create_skill_markdown(
        skill_name: str,
        description: str,
        instructions: str,
        author: str = "Team GemmaLens",
        version: str = "1.0.0"
    ) -> str:
        clean_name = skill_name.strip().lower().replace(" ", "-")
        skill_content = f"""---
name: {clean_name}
description: {description.strip()}
author: {author}
version: {version}
license: Apache-2.0
standard: https://agentskills.io/specification
---

# {skill_name}

{description}

## Usage & Execution Instructions
{instructions}

## Model Recommendations
- Primary Model: Google Gemma 4 (gemma-4-26b-a4b-it)
- Features: Multimodal visual diagram ingestion, thinking mode enabled.
"""
        return skill_content

    @staticmethod
    def export_skill_to_disk(target_dir: str, skill_content: str) -> str:
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, "SKILL.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(skill_content)
        return file_path
