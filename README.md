# 🔍 GemmaLens: Multimodal AI System & Code Auditor

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Model](https://img.shields.io/badge/Model-Gemma_4_(26B_MoE)-orange.svg)](https://ai.google.dev/gemma)
[![Standard](https://img.shields.io/badge/Standard-Agent_Skills_Open_Standard-green.svg)](https://agentskills.io/specification)
[![Hackathon](https://img.shields.io/badge/MLH-Hacktoberfest_Hack_Day_Coimbatore_2026-red.svg)](https://www.mlh.com/events/hacktoberfest-hack-day-coimbatore-x-init-club/challenges)

> **Built for Hacktoberfest Hack Day Coimbatore 2026**  
> Hosted by **INIT Club & iDEA Club** at **Amrita Vishwa Vidyapeetham, Coimbatore**  
> In collaboration with **Major League Hacking (MLH)**, **Google DeepMind**, **DigitalOcean**, and **SkySync**.

---

## 🌟 1. Project Overview & Inspiration

Engineering teams frequently whiteboard architectures, draft cloud topology sketches, or debug low-level systems code where human review is slow and prone to oversight.

**GemmaLens** is an open-source, multimodal developer copilot powered by Google's **Gemma 4** (`gemma-4-26b-a4b-it` Mixture-of-Experts). It bridges visual architecture design and production deployment by:
1. **Visual Diagram Ingestion:** Ingesting whiteboard sketches, handwritten topologies, and network screenshots to detect Single Points of Failure (SPOFs) and security vulnerabilities.
2. **Deep Code Reasoning:** Employing Gemma 4's multi-step **thinking process** to perform static analysis on C/C++/Rust code, hunting boundary errors, dangling pointers, and concurrency hazards.
3. **Automated Infrastructure as Code (IaC):** Converting raw architectural sketches into runnable Docker Compose and Terraform topologies.
4. **Agent Skills Open Standard Compliance:** Packaging workflows into reusable `SKILL.md` bundles conforming to the [Agent Skills specification](https://agentskills.io/specification).

---

## 🤖 2. Open-Source AI Model & Terms

- **Model Used:** Google Gemma 4 (`gemma-4-26b-a4b-it`)
- **Architecture:** Mixture-of-Experts (MoE) with 26 Billion total parameters and 4 Billion active parameters.
- **Key Capabilities Utilized:**
  - **Multimodal Visual Understanding:** Direct image ingestion for architecture topologies and diagrams.
  - **Internal Thinking Mode:** High-level logical reasoning (`thinking_level="high"`).
- **Model License:** [Apache 2.0 Open Weights](https://ai.google.dev/gemma)
- **Model Terms & Usage:** [Gemma Terms of Use](https://ai.google.dev/gemma/terms)
- **Inference Runtime:** Google GenAI SDK (`google-genai`) hosted on the Gemini API.

---

## 🏆 3. Target Hackathon Prize Categories

GemmaLens specifically targets and satisfies **both** prize challenges:

1. **Best Use of Gemma 4 (Google DeepMind Track):**
   - Directly incorporates Gemma 4's multimodal capabilities (visual diagrams) and reasoning mode (`thinking_config`).
2. **Best Open-Source AI Project (DigitalOcean / Main Event Track):**
   - Built under the **Apache-2.0 open-source license**.
   - Conforms strictly to the **Agent Skills open standard** (`skills/gemma-auditor/SKILL.md`).
   - Clean, reproducible repository structure.

---

## 👥 4. Team GemmaLens (Team of 4)

In accordance with Hackathon Rule 02 and Rule 03, every team member actively contributed with distinct commits:

| Member | Role | GitHub Email | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Dhanwinn** | Team Lead & DevOps | `dhanwinn15@gmail.com` | Repo setup, Apache 2.0 license, requirements, deployment |
| **Avanish Ayyappan** | AI Engine Architect | `avanishayyappan2007@gmail.com` | `gemma_engine.py`, API client, thinking configuration, multimodal upload |
| **Shasank Paruchuri** | Agent & Prompt Specialist | `paruchurishasank04@gmail.com` | `prompts.py`, `agent_skills.py`, `SKILL.md` open standard compliance |
| **Gyatchut** | Frontend & UI Lead | `gyatchut@gmail.com` | `app.py`, Streamlit dashboard, interactive report exporter |

---

## 🚀 5. Setup & Installation

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- A free Google AI Studio API Key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 1. Clone the Repository
```bash
git clone https://github.com/MRLDHANWINN/GemmaLens.git
cd GemmaLens
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Your API Key (Optional environment variable)
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"

# Linux / macOS
export GEMINI_API_KEY="your_api_key_here"
```

---

## 💻 6. Usage & Running the Demo

### Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

### Key Features to Explore:
1. **🏛️ Architecture Auditor:** Upload an image of an architecture diagram or whiteboard sketch. Watch Gemma 4 analyze single points of failure and generate a working Docker Compose manifest.
2. **🛡️ Code Reasoning:** Paste C or low-level systems code. Enable "Deep Thinking Mode" to see Gemma 4 break down memory allocation, pointer indexing, and safety bugs.
3. **🧩 Agent Skills Studio:** Inspect and export an open-standard `SKILL.md` file ready to be loaded by autonomous agent runtimes.

---

## 📦 7. Dependencies

- `google-genai>=0.1.1` — Official Google GenAI SDK for Gemma 4 & Gemini models.
- `streamlit>=1.35.0` — Interactive web application interface.
- `pillow>=10.0.0` — Image processing for visual diagram uploads.
- `pydantic>=2.0.0` — Data validation and schema enforcement.

---

## 📄 8. License

This project is open-source software licensed under the **[Apache License 2.0](LICENSE)**.
