---
name: mandishield-auditor
description: Autonomous multimodal audit tool for detecting counterfeit pesticides, banned agro-chemicals, and spurious seeds under Indian agricultural statutes.
author: Team MandiShield (Hacktoberfest Hack Day Coimbatore 2026)
version: 1.0.0
license: Apache-2.0
standard: https://agentskills.io/specification
---

# MandiShield Autonomous Agricultural Auditor

MandiShield provides automated forensic verification of agro-chemical inputs (pesticides, fungicides, herbicides) and certified seed lots across rural Indian mandis.

## Model Recommendations
- Foundation Model: Google Gemma 4 (`gemma-4-26b-a4b-it` via Google GenAI or `gemma4:e2b` via local Ollama).
- Core Capabilities: Multimodal high-resolution label OCR, Micro-typography analysis, Indian statutory knowledge, and Multi-step reasoning (`thinking_level="high"`).

## Input Requirements
1. **Container Image**: Clear photograph of the pesticide bottle or seed packet label (showing brand, batch, active ingredients, CIB&RC code, and toxicity diamond).
2. **Seed Macro Image** (Optional): Close-up photo of seed grain treatment coating and embryo morphology.
3. **Receipt / Vendor Metadata** (Optional): Shop name, village, and invoice date for legal complaint generation.

## Execution Workflow
1. **Extraction**:
   - Extract product trade name, active chemical molecule, and formulation percentage.
   - Extract CIB&RC Registration Code (`CIR-XXXXX/YYYY/...`) and Manufacturing License number.
   - Extract batch details (Batch No, Mfg Date, Exp Date).
2. **Statutory & Chemical Validation**:
   - Match active chemical against the **List of 27 Banned Pesticides in India** (Gazette notifications).
   - Validate CIB&RC registration code structure and year.
   - Verify that the **Toxicity Diamond color** (Red, Yellow, Blue, Green) matches the statutory oral $LD_{50}$ classification under Rule 19 of the Insecticides Rules 1971.
3. **Forensic Typography Check**:
   - Audit batch number print method (genuine inkjet dot-matrix vs flat offset counterfeit).
   - Check for chemical name spelling variations (e.g. 'Chlorpyriphos' vs 'Chlorpyrifos').
4. **Remediation & Reporting**:
   - Produce an Authenticity Score (0-100%).
   - Synthesize multilingual farmer advisories in English, Tamil, Hindi, and Telugu.
   - Generate a pre-filled legal complaint petition to the District Agricultural Officer (DAO) under Section 29 of the Insecticides Act 1968 if counterfeit markers are detected.
