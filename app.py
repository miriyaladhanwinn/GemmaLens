"""
MandiShield - The Autonomous Counterfeit Pesticide & Spurious Seed Audit Engine
Author: Gyatchut (gyatchut@gmail.com)
Powered by: Google Gemma 4 (26B MoE - 4B Active parameters / Local Gemma 4 E2B via Ollama)
License: Apache-2.0
Team: MandiShield (Hacktoberfest Hack Day Coimbatore 2026)
"""

import os
import tempfile
import streamlit as st
from PIL import Image

from gemma_engine import (
    GemmaEngine,
    DEFAULT_MODEL,
    DEFAULT_OLLAMA_MODEL,
    DEFAULT_OLLAMA_URL,
)
from agri_db import (
    BANNED_PESTICIDES_INDIA,
    TOXICITY_DIAMONDS,
    AUTHORIZED_MANUFACTURERS,
    STATUTORY_LABEL_REQUIREMENTS,
    SEED_STANDARDS,
    check_banned_chemical,
    validate_cibrc_format,
    evaluate_toxicity_diamond,
)
from agent_skills import AgentSkillPackage

# Page Configuration
st.set_page_config(
    page_title="MandiShield - Agri-Forensic Auditor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Agri-Tech Styling
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1b5e20;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4a5568;
        margin-bottom: 1.2rem;
    }
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: #e8f5e9;
        color: #2e7d32;
        margin-right: 0.4rem;
        margin-bottom: 0.5rem;
        border: 1px solid #c8e6c9;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 0.8rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .danger-box {
        background-color: #ffebee;
        border-left: 5px solid #d32f2f;
        padding: 0.8rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #2e7d32;
        padding: 0.8rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# App Header
st.markdown(
    '<div class="main-header">🌾 MandiShield: Counterfeit Pesticide & Seed Audit Engine</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div>
    <span class="badge-pill">🧠 Model: Google Gemma 4 (26B MoE & Local Ollama)</span>
    <span class="badge-pill">🛡️ Regulatory: CIB&RC & Insecticides Act 1968</span>
    <span class="badge-pill">🌱 Standard: Seeds Act 1966 & Indian Pharmacopeia</span>
    <span class="badge-pill">📦 Protocol: Agent Skills Open Standard</span>
    <span class="badge-pill">🏆 Hacktoberfest Hack Day Coimbatore 2026</span>
</div>
<div class="sub-header">
    Protecting Indian smallholder farmers against the ₹25,000 Crore counterfeit agro-chemical epidemic using multimodal reasoning, micro-typography forensics, and local edge inference.
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar Configuration
st.sidebar.title("⚙️ Engine & Inference Mode")

backend_choice = st.sidebar.radio(
    "Select Gemma 4 Backend:",
    ["Hosted Gemini API (gemma-4-26b-a4b-it)", "Offline Local Ollama (gemma4:e2b)"],
    index=0,
)

backend_type = "gemini_api" if "Hosted" in backend_choice else "ollama"

api_key = None
if backend_type == "gemini_api":
    api_key_env = os.environ.get("GEMINI_API_KEY", "")
    api_key = st.sidebar.text_input(
        "Google AI Studio API Key:",
        value=api_key_env,
        type="password",
        help="Reads automatically from GEMINI_API_KEY environment variable.",
    )
    if not api_key:
        st.sidebar.warning("⚠️ Enter your Gemini API key to enable Gemma 4 cloud inference.")
else:
    ollama_url = st.sidebar.text_input("Ollama Host URL:", value=DEFAULT_OLLAMA_URL)
    ollama_model = st.sidebar.text_input("Ollama Model Name:", value=DEFAULT_OLLAMA_MODEL)
    is_up = GemmaEngine.is_ollama_available(ollama_url)
    if is_up:
        st.sidebar.success(f"🟢 Ollama is running at {ollama_url}")
    else:
        st.sidebar.error(f"🔴 Cannot connect to Ollama at {ollama_url}")

thinking_level = st.sidebar.select_slider(
    "Gemma 4 Thinking / Reasoning Depth:",
    options=["minimal", "high"],
    value="high",
    help="High enables multi-step chain-of-thought analysis for statutory discrepancy detection.",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👥 MandiShield Team Matrix")
st.sidebar.markdown(
    """
- **Dhanwinn (Lead):** Core Architecture & Regulatory Integration
- **Avanish Ayyappan:** Gemma 4 Dual Engine & Edge Resilience
- **Shasank Paruchuri:** Statutory Prompts & Agent Skills Spec
- **Gyatchut:** Streamlit Multimodal UI & Regional Localizer
"""
)

# Initialize Engine
engine = None
try:
    if backend_type == "gemini_api":
        if api_key:
            engine = GemmaEngine(api_key=api_key, backend="gemini_api")
    else:
        engine = GemmaEngine(
            backend="ollama",
            ollama_url=ollama_url if "ollama_url" in locals() else DEFAULT_OLLAMA_URL,
            ollama_model=ollama_model if "ollama_model" in locals() else DEFAULT_OLLAMA_MODEL,
        )
except Exception as e:
    st.sidebar.error(f"Initialization error: {e}")

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🧪 1. Pesticide Bottle Auditor",
        "🌱 2. Seed Coating & Purity Inspector",
        "🚫 3. Banned Chemicals & CIB&RC Registry",
        "⚖️ 4. DAO Legal Complaint Generator",
        "🗣️ 5. Multilingual Farmer Advisory",
        "📦 6. Agent Skills & Open Source",
    ]
)

# Helper function to save uploaded image
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name


# TAB 1: Pesticide Bottle Auditor
with tab1:
    st.subheader("🧪 Forensic Pesticide Packaging & CIB&RC Auditor")
    st.markdown(
        "Upload a photograph of the pesticide container label, or select one of our curated forensic test samples below:"
    )

    col_btn1, col_btn2 = st.columns(2)
    sample_to_load = None

    with col_btn1:
        if st.button("🚩 Load Sample 1: Counterfeit Chlor-Strike 20 EC (Flagged Flaws)"):
            sample_to_load = os.path.join(
                os.path.dirname(__file__), "examples", "counterfeit_pesticide_sample.png"
            )
    with col_btn2:
        if st.button("✅ Load Sample 2: Genuine Bayer Confidor 17.8 SL (Statutory Compliant)"):
            sample_to_load = os.path.join(
                os.path.dirname(__file__), "examples", "genuine_pesticide_sample.png"
            )

    uploaded_pesticide = st.file_uploader(
        "Upload Pesticide Bottle / Label Photo (PNG, JPG, JPEG):",
        type=["png", "jpg", "jpeg"],
        key="pest_uploader",
    )

    pesticide_img_path = None
    if uploaded_pesticide:
        pesticide_img_path = save_uploaded_file(uploaded_pesticide)
    elif sample_to_load and os.path.exists(sample_to_load):
        pesticide_img_path = sample_to_load

    col_img, col_notes = st.columns([1, 1])

    with col_img:
        if pesticide_img_path:
            img = Image.open(pesticide_img_path)
            st.image(img, caption="Target Agro-Chemical Label for Forensic Audit", use_container_width=True)
        else:
            st.info("👆 Upload an image or click a test sample above to preview.")

    with col_notes:
        st.markdown("#### Statutory Rapid Pre-Check")
        pre_chem = st.text_input(
            "Claimed Active Chemical (Optional Fast-Check):",
            placeholder="e.g. Endosulfan 35% EC, Chlorpyrifos 20% EC",
        )
        if pre_chem:
            banned_info = check_banned_chemical(pre_chem)
            if banned_info:
                st.markdown(
                    f"""
                <div class="danger-box">
                    🚨 <b>LEGAL ALERT:</b> <code>{banned_info['chemical'].upper()}</code> is <b>{banned_info['status']}</b> in India!<br>
                    <b>Order:</b> {banned_info['order']}<br>
                    <b>Toxic Hazard:</b> {banned_info['hazard']}<br>
                    <b>Approved Alternative:</b> {banned_info['replacement']}
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="success-box">✅ Chemical <code>{pre_chem}</code> is not in the Indian Gazette banned list.</div>',
                    unsafe_allow_html=True,
                )

        pesticide_notes = st.text_area(
            "Mandi / Purchase Observations (Optional):",
            value="Sold at rural weekly market without printed tax invoice. Batch number looks flat-printed.",
            height=100,
        )

        audit_btn = st.button("🚀 Run Gemma 4 Forensic Audit", type="primary", use_container_width=True)

    if audit_btn:
        if not engine:
            st.error("Please configure your Gemini API Key in the sidebar or start Ollama locally.")
        elif not pesticide_img_path:
            st.warning("Please upload a label image or pick a test sample.")
        else:
            with st.spinner("🧠 Gemma 4 Multimodal Reasoner is auditing CIB&RC code, typography, and toxicity diamond..."):
                try:
                    result = engine.audit_pesticide_label(
                        image_path=pesticide_img_path,
                        additional_notes=pesticide_notes,
                        thinking_level=thinking_level,
                    )
                    st.session_state["last_audit_report"] = result
                    st.success("✅ Audit Complete!")
                    st.markdown("### 📋 MandiShield Forensic Audit Report")
                    st.markdown(result)
                    
                    st.download_button(
                        "📥 Download Forensic Report (.md)",
                        data=result,
                        file_name="mandishield_forensic_report.md",
                        mime="text/markdown",
                    )
                except Exception as ex:
                    st.error(f"Inference failed: {ex}")


# TAB 2: Seed Coating & Purity Inspector
with tab2:
    st.subheader("🌱 Seed Physical Morphology & Coating Integrity Inspector")
    st.markdown(
        "Detect spurious seeds dyed with food coloring vs genuine certified hybrid lots under the **Seeds Act 1966**."
    )

    if st.button("🚩 Load Sample 3: Spurious Dyed Cotton Seed Lot (High Inert Matter)"):
        st.session_state["seed_sample_path"] = os.path.join(
            os.path.dirname(__file__), "examples", "spurious_seeds_sample.png"
        )

    uploaded_seed = st.file_uploader(
        "Upload Seed Macro Photo (Close-up of grains/coating):",
        type=["png", "jpg", "jpeg"],
        key="seed_uploader",
    )

    seed_img_path = None
    if uploaded_seed:
        seed_img_path = save_uploaded_file(uploaded_seed)
    elif "seed_sample_path" in st.session_state and os.path.exists(st.session_state["seed_sample_path"]):
        seed_img_path = st.session_state["seed_sample_path"]

    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        if seed_img_path:
            st.image(Image.open(seed_img_path), caption="Seed Macro Sample", use_container_width=True)
        else:
            st.info("👆 Upload a seed photo or click Sample 3 to preview.")

    with col_s2:
        crop_selection = st.selectbox(
            "Select Crop Standard (Seeds Act 1966):",
            ["hybrid_cotton_bt", "hybrid_paddy_rice", "hybrid_maize_corn"],
            format_func=lambda x: SEED_STANDARDS[x]["crop"],
        )
        std = SEED_STANDARDS[crop_selection]
        st.markdown(
            f"""
        **Statutory Standards for {std['crop']}:**
        - **Min. Germination:** {std['germination_min_pct']}
        - **Max. Inert Matter:** {std['inert_matter_max_pct']}
        - **Mandatory Coating:** {std['mandatory_coating']}
        - **Common Counterfeit Flags:** {std['counterfeit_flags']}
        """
        )

        seed_notes = st.text_area(
            "Physical Observations on Grain:",
            value="Color flaking off on fingers when touched; noticeable broken hulls in bag.",
        )

        seed_audit_btn = st.button("🔬 Audit Seed Morphology with Gemma 4", type="primary", use_container_width=True)

    if seed_audit_btn:
        if not engine:
            st.error("Please configure API key in sidebar.")
        elif not seed_img_path:
            st.warning("Please upload a seed macro image or load sample.")
        else:
            with st.spinner("Analyzing seed grain coating, embryo integrity, and purity standards..."):
                try:
                    seed_report = engine.audit_seed_sample(
                        image_path=seed_img_path,
                        sample_details=f"Crop: {std['crop']}\nNotes: {seed_notes}",
                        thinking_level=thinking_level,
                    )
                    st.markdown("### 🌾 Seed Certification Audit Findings")
                    st.markdown(seed_report)
                except Exception as ex:
                    st.error(f"Inference error: {ex}")


# TAB 3: Banned Pesticides & CIB&RC Registry
with tab3:
    st.subheader("🚫 Central Insecticides Board (CIB&RC) Regulatory Registry")
    st.markdown("Searchable statutory database of banned chemicals and authorized Indian agro-chemical manufacturers.")

    search_query = st.text_input("🔍 Search Active Chemical or Manufacturer:", placeholder="e.g. Endosulfan, Bayer, UPL, Monocrotophos")

    st.markdown("#### 🚫 27 Banned / Severely Restricted Pesticides in India")
    banned_rows = []
    for k, v in BANNED_PESTICIDES_INDIA.items():
        if not search_query or search_query.lower() in k.lower():
            banned_rows.append({"Chemical": k.upper(), "Status": v["status"], "Legal Gazette Order": v["order"], "Health Hazard": v["hazard"], "Safe Alternative": v["replacement"]})
    st.dataframe(banned_rows, use_container_width=True)

    st.markdown("#### 🏢 Top Authorized CIB&RC Registered Manufacturers")
    mfg_rows = []
    for m in AUTHORIZED_MANUFACTURERS:
        if not search_query or search_query.lower() in m["name"].lower():
            mfg_rows.append({"Manufacturer": m["name"], "Code": m["code"], "Registered Facilities": m["state"], "CIB&RC Prefix": m["prefix"]})
    st.dataframe(mfg_rows, use_container_width=True)


# TAB 4: DAO Legal Complaint Generator
with tab4:
    st.subheader("⚖️ District Agricultural Officer (DAO) Legal Complaint Generator")
    st.markdown("Generates a formal, legally enforceable complaint petition under **Section 29 of the Insecticides Act 1968**.")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        farmer_name = st.text_input("Complainant Farmer Name:", value="Murugan R.")
        farmer_village = st.text_input("Village / Panchayat:", value="Sulur")
        farmer_district = st.text_input("District / State:", value="Coimbatore, Tamil Nadu")
    with col_f2:
        shop_name = st.text_input("Agro-Chemical Retailer / Shop Name:", value="Sri Lakshmi Fertilizer & Seed Depot")
        product_name = st.text_input("Suspect Product & Formulation:", value="Chlor-Strike 20 EC")
        batch_no = st.text_input("Batch No. & Expiry on Container:", value="BATCH-8889-OFFSET (Exp: 12/2030)")

    violations_text = st.text_area(
        "Identified Forensic Violations:",
        value="Forged CIB&RC registration code CIR-0014/1965; misspelled active ingredient 'Chlorpyriphos'; missing antidote statement; flat offset printing on label.",
        height=100,
    )

    if st.button("📜 Generate Section 29 Complaint Petition", type="primary"):
        if not engine:
            st.error("Please configure API key in sidebar.")
        else:
            with st.spinner("Drafting formal legal complaint petition with statutory references..."):
                complaint_doc = engine.generate_dao_complaint(
                    farmer_name=farmer_name,
                    farmer_village=farmer_village,
                    farmer_district=farmer_district,
                    shop_name=shop_name,
                    product_name=product_name,
                    batch_no=batch_no,
                    violations=violations_text,
                )
                st.markdown("### 📄 Formal Complaint Petition")
                st.markdown(complaint_doc)

                st.download_button(
                    "📥 Download Legal Complaint Petition (.txt)",
                    data=complaint_doc,
                    file_name="dao_insecticides_act_complaint.txt",
                    mime="text/plain",
                )


# TAB 5: Multilingual Farmer Advisory
with tab5:
    st.subheader("🗣️ Multilingual Regional Voice & Text Advisory")
    st.markdown("Translates forensic findings into plain, urgent language for farmers in **Tamil, Telugu, Hindi, and English**.")

    sample_report_input = st.text_area(
        "Audit Findings to Translate:",
        value=st.session_state.get(
            "last_audit_report",
            "CRITICAL HAZARD: Product is counterfeit Chlor-Strike 20 EC. Forged CIB&RC code. Do not spray on crops.",
        ),
        height=120,
    )

    if st.button("🌐 Generate Multilingual Farmer Advisory"):
        if not engine:
            st.error("Please configure API key in sidebar.")
        else:
            with st.spinner("Gemma 4 is synthesizing regional multilingual advisories..."):
                advisory = engine.generate_farmer_advisory(sample_report_input)
                st.markdown(advisory)


# TAB 6: Agent Skills & Open Source Spec
with tab6:
    st.subheader("📦 Agent Skills Open Standard & Open Source Distribution")
    st.markdown(
        "MandiShield exports its automated agricultural forensic workflow as an open-standard Agent Skill conforming to [Agent Skills](https://agentskills.io/specification)."
    )

    skill_path = os.path.join(os.path.dirname(__file__), "skills", "mandishield", "SKILL.md")
    if os.path.exists(skill_path):
        with open(skill_path, "r", encoding="utf-8") as f:
            skill_content = f.read()
        st.code(skill_content, language="markdown")
        st.download_button(
            "📥 Download SKILL.md",
            data=skill_content,
            file_name="mandishield_SKILL.md",
            mime="text/markdown",
        )

    st.markdown("---")
    st.markdown("### 🐳 Docker & DigitalOcean Deployment")
    st.code(
        """
# Run MandiShield on DigitalOcean Droplet or App Platform
docker build -t mandishield-gemma4:latest .
docker run -p 8501:8501 -e GEMINI_API_KEY="YOUR_KEY" mandishield-gemma4:latest
    """,
        language="bash",
    )
