"""
GemmaLens: Multimodal AI System & Code Auditor
Author: Gyatchut (gyatchut@gmail.com)
Powered by: Google Gemma 4 (26B MoE - 4B Active) / Local Gemma (Ollama)
License: Apache-2.0
"""

import os
import tempfile
import streamlit as st
from PIL import Image

from gemma_engine import GemmaEngine, DEFAULT_MODEL, DEFAULT_OLLAMA_MODEL, DEFAULT_OLLAMA_URL
from prompts import ARCHITECTURE_AUDIT_PROMPT, CODE_SECURITY_PROMPT, AGENT_SKILL_META_PROMPT
from agent_skills import AgentSkillPackage

# Page Configuration
st.set_page_config(
    page_title="GemmaLens - Multimodal AI Auditor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1a73e8;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #5f6368;
        margin-bottom: 1.5rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: #e8f0fe;
        color: #1a73e8;
        margin-right: 0.4rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-header">🔍 GemmaLens: Multimodal System & Code Auditor</div>', unsafe_allow_html=True)
st.markdown("""
<div>
    <span class="badge-pill">🧠 Model: Gemma 4 (26B MoE & Ollama)</span>
    <span class="badge-pill">📄 License: Apache-2.0 Open Weights</span>
    <span class="badge-pill">🧩 Standard: Agent Skills Open Standard</span>
    <span class="badge-pill">⚡ Hacktoberfest Hack Day Coimbatore</span>
</div>
<div class="sub-header">
    An open-source multimodal developer copilot that ingests architecture diagrams, audits infrastructure for single points of failure, deep-reasons over low-level code, and packages reusable Agent Skills.
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("⚙️ Engine & Inference Mode")

backend_choice = st.sidebar.radio(
    "Inference Backend",
    options=["Hosted Gemini API (Gemma 4 MoE)", "Local Offline (Ollama)"],
    index=0,
    help="Hosted API provides full 26B MoE & Multimodal vision. Local Ollama runs 100% offline."
)

is_local = "Ollama" in backend_choice

api_key = ""
model_choice = "gemma-4-26b-a4b-it"
ollama_model = DEFAULT_OLLAMA_MODEL
ollama_url = DEFAULT_OLLAMA_URL

if not is_local:
    api_key = st.sidebar.text_input(
        "Google AI Studio API Key",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Get a free key at https://aistudio.google.com/apikey"
    )
    model_choice = st.sidebar.selectbox(
        "Active Gemma Model",
        options=["gemma-4-26b-a4b-it", "gemma-4-31b-it"],
        index=0,
        help="gemma-4-26b-a4b-it is the 26B Mixture-of-Experts model with 4B active parameters."
    )
    thinking_mode = st.sidebar.toggle("Enable Deep Thinking Mode", value=True)
    thinking_level = "high" if thinking_mode else "minimal"
else:
    ollama_url = st.sidebar.text_input("Ollama Server URL", value=DEFAULT_OLLAMA_URL)
    ollama_model = st.sidebar.text_input("Ollama Model Name", value=DEFAULT_OLLAMA_MODEL)
    thinking_level = "minimal"
    ollama_live = GemmaEngine.is_ollama_available(ollama_url)
    if ollama_live:
        st.sidebar.success("🟢 Local Ollama Server Detected!")
    else:
        st.sidebar.warning("🟡 Ollama server not detected. Run `ollama serve` if running locally.")

st.sidebar.divider()
st.sidebar.markdown("""
### 👥 Team GemmaLens
- **Team Lead:** Dhanwinn (`dhanwinn15@gmail.com`)
- **Engine Architect:** Avanish (`avanishayyappan2007@gmail.com`)
- **Agent Specialist:** Shasank (`paruchurishasank04@gmail.com`)
- **Frontend Lead:** Gyatchut (`gyatchut@gmail.com`)

### 🏆 Prize Categories
- **DeepMind:** Best Use of Gemma 4
- **DigitalOcean:** Best Open-Source AI Project
""")

# Initialize Engine
engine = None
try:
    if not is_local:
        if api_key:
            engine = GemmaEngine(api_key=api_key, model=model_choice, backend="gemini_api")
        else:
            st.info("👋 Welcome! Please enter your Google AI Studio API key in the sidebar to begin, or switch to Local Ollama.")
    else:
        engine = GemmaEngine(backend="ollama", ollama_url=ollama_url, ollama_model=ollama_model)
except Exception as e:
    st.sidebar.error(f"Initialization error: {e}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🏛️ Architecture & Diagram Auditor",
    "🛡️ Deep Code Reasoning & Bug Hunter",
    "🧩 Agent Skills Studio",
    "📋 Compliance & Verification"
])

# ----------------- TAB 1: ARCHITECTURE AUDITOR -----------------
with tab1:
    st.subheader("Visual Infrastructure & Whiteboard Ingestion")
    st.write("Upload an architecture diagram, cloud topology screenshot, or whiteboard sketch to get a full resilience audit and generated Docker Compose.")

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_image = st.file_uploader(
            "Upload System Diagram (PNG, JPG, JPEG)",
            type=["png", "jpg", "jpeg"],
            key="arch_image"
        )

        custom_prompt = st.text_area(
            "Custom Instructions (Optional)",
            value="Audit this topology for single points of failure, missing caches, security flaws, and output a runnable Docker Compose setup for testing.",
            height=100
        )

        run_arch_button = st.button("Audit Architecture with Gemma 4 🚀", type="primary", disabled=engine is None)

        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Architecture Diagram", use_container_width=True)

    with col2:
        if run_arch_button and engine:
            temp_path = None
            try:
                with st.spinner("Gemma 4 is inspecting diagram and deep-thinking..."):
                    if uploaded_image:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                            tmp.write(uploaded_image.getvalue())
                            temp_path = tmp.name

                    full_prompt = f"{ARCHITECTURE_AUDIT_PROMPT}\n\nAdditional Instructions:\n{custom_prompt}"
                    report = engine.analyze(
                        prompt=full_prompt,
                        image_path=temp_path,
                        thinking_level=thinking_level
                    )

                    st.markdown("### 📋 Gemma 4 Architecture Audit Report")
                    st.markdown(report)

                    # Download button for report
                    st.download_button(
                        label="📥 Download Audit Report (Markdown)",
                        data=report,
                        file_name="architecture_audit_report.md",
                        mime="text/markdown"
                    )
            except Exception as e:
                st.error(f"Error executing analysis: {e}")
            finally:
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

# ----------------- TAB 2: CODE REASONING & BUG HUNTER -----------------
with tab2:
    st.subheader("Deep-Reasoning Code Security & Pointer Arithmetic Auditor")
    st.write("Leverage Gemma 4's multi-step thinking process to catch boundary errors, memory leaks, and concurrency hazards.")

    col_code1, col_code2 = st.columns([1, 1])

    with col_code1:
        sample_c_code = """#include <stdio.h>
#include <stdlib.h>

void process_buffer(int *arr, int len) {
    int *ptr = arr;
    for (int i = 0; i <= len; i++) {
        *(ptr++) = i * 2;
    }
}

int main() {
    int size = 5;
    int *data = (int *)malloc(size * sizeof(int));
    process_buffer(data, size);
    printf("Processed %d\\n", data[0]);
    return 0; // Notice: missing free(data)
}"""

        code_input = st.text_area(
            "Paste Code Snippet (C / C++ / Rust / Python / Go):",
            value=sample_c_code,
            height=280
        )

        run_code_button = st.button("Run Deep Thinking Analysis 🧠", type="primary", disabled=engine is None)

    with col_code2:
        if run_code_button and engine:
            try:
                with st.spinner("Gemma 4 is applying multi-step reasoning to code..."):
                    full_code_prompt = f"{CODE_SECURITY_PROMPT}\n\nTarget Code:\n```c\n{code_input}\n```"
                    code_report = engine.analyze(
                        prompt=full_code_prompt,
                        thinking_level=thinking_level
                    )

                    st.markdown("### 🛡️ Static Verification & Hardened Fix")
                    st.markdown(code_report)

                    st.download_button(
                        label="📥 Download Code Audit Report",
                        data=code_report,
                        file_name="code_security_audit.md",
                        mime="text/markdown"
                    )
            except Exception as e:
                st.error(f"Error during code analysis: {e}")

# ----------------- TAB 3: AGENT SKILLS STUDIO -----------------
with tab3:
    st.subheader("Agent Skills Open Standard Exporter")
    st.write("Packages custom developer workflows into reusable Agent Skills conforming to the [Agent Skills open standard](https://agentskills.io/specification).")

    skill_name = st.text_input("Skill Name:", value="System Topology & Memory Safety Auditor")
    skill_desc = st.text_area(
        "Skill Purpose:",
        value="Autonomous agent capability to parse architecture sketches, audit memory safety in low-level code, and generate verified deployment scripts."
    )
    skill_instructions = st.text_area(
        "Skill Instructions:",
        value="1. Receive architecture diagram or source code.\n2. Dispatch to Gemma 4 (26B MoE) with thinking_level='high'.\n3. Parse findings into vulnerabilities, Docker Compose, and unit tests.\n4. Output report in GitHub-flavored markdown.",
        height=120
    )

    if st.button("Generate & Validate SKILL.md 🧩"):
        skill_md = AgentSkillPackage.create_skill_markdown(
            skill_name=skill_name,
            description=skill_desc,
            instructions=skill_instructions,
            author="Team GemmaLens (Hacktoberfest Hack Day Coimbatore 2026)"
        )

        st.success("✅ Valid Agent Skill generated conforming to https://agentskills.io/specification!")
        st.code(skill_md, language="markdown")

        st.download_button(
            label="📥 Download Validated SKILL.md",
            data=skill_md,
            file_name="SKILL.md",
            mime="text/markdown"
        )

# ----------------- TAB 4: COMPLIANCE & VERIFICATION -----------------
with tab4:
    st.subheader("Official Hackathon Rule Compliance & Model Verification")
    
    st.markdown("""
    | Rule # | MLH / Coimbatore Rule | How GemmaLens Satisfies It |
    | :--- | :--- | :--- |
    | **01** | **Build During Hack Day** | Built fresh during the event with incremental git commits. |
    | **02** | **Show Your Progress** | Clean commit history featuring all 4 team members with verified emails. |
    | **03** | **Team of 4** | Exactly 4 teammates (Dhanwinn, Avanish, Shasank, Gyatchut). |
    | **04** | **Original Work** | Powered by open-weight Gemma 4 using official Google GenAI SDK & Ollama. |
    | **05** | **Working Build Required** | Fully interactive live Streamlit web application. |
    | **06** | **Submit On Time** | Prepared for OrganizerHQ submission ahead of 5:00 PM IST. |
    | **07** | **Keep It Clear** | Complete README with Setup, Dependencies, and Usage. |
    | **08** | **Open-Source AI Track** | Repository licensed under Apache-2.0, utilizing open-weight Gemma 4. |
    | **09** | **Partner Challenge** | Primary engine uses Google Gemma 4 (26B MoE) with multimodal & thinking mode. |
    """)

    st.divider()
    st.markdown("""
    ### 🤖 Model Attribution & Terms
    - **Hosted Model:** `gemma-4-26b-a4b-it` (Google DeepMind) via Gemini API
    - **Local Offline Model:** `gemma4:e2b` / `gemma2:2b` via Ollama
    - **Parameters:** 26 Billion Total (4 Billion Active via Mixture-of-Experts)
    - **License:** Apache 2.0 Open Weights
    - **Provider Terms:** [Google Gemma Terms](https://ai.google.dev/gemma/terms)
    """)
