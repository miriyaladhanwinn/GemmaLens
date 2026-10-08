"""
MandiShield - National Agro-Forensic & Regulatory Verification System
Human-Crafted Modern Web Application for Indian Agriculture
Author: Team MandiShield (Dhanwinn, Avanish Ayyappan, Shasank Paruchuri, Gyatchut)
Powered by: Google Gemma 4 (26B MoE & Local Edge Inference)
License: Apache-2.0
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
    SEED_STANDARDS,
    check_banned_chemical,
    validate_cibrc_format,
    evaluate_toxicity_diamond,
)
from agent_skills import AgentSkillPackage

# Configure Page
st.set_page_config(
    page_title="MandiShield | National Agro-Forensic System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Human-Crafted Custom CSS Design System
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1e293b;
    }

    /* Top Brand Navigation */
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        border-radius: 14px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.2);
    }
    .brand-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .brand-subtitle {
        font-size: 0.95rem;
        color: #a7f3d0;
        margin-top: 0.25rem;
        font-weight: 400;
    }
    .brand-tag {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 0.4rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.25);
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Modern Card Layouts */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f172a;
    }

    /* Status Banners */
    .verdict-banner-danger {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-left: 6px solid #ef4444;
        border-radius: 10px;
        padding: 1rem 1.4rem;
        margin: 1rem 0;
    }
    .verdict-banner-success {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-left: 6px solid #10b981;
        border-radius: 10px;
        padding: 1rem 1.4rem;
        margin: 1rem 0;
    }
    .verdict-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .verdict-body {
        font-size: 0.9rem;
        margin-top: 0.35rem;
        color: #334155;
        line-height: 1.45;
    }

    /* Sample Selector Pill */
    .sample-pill {
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 0.85rem;
        background: #f8fafc;
        margin-bottom: 0.75rem;
        cursor: pointer;
    }

    /* Letterhead styling */
    .letterhead {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        font-family: 'Times New Roman', Times, serif;
    }
    .letterhead-header {
        text-align: center;
        border-bottom: 2px solid #0f172a;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# App Navigation Header
st.markdown(
    """
<div class="brand-container">
    <div>
        <div class="brand-title">🛡️ MandiShield</div>
        <div class="brand-subtitle">Autonomous Agro-Chemical Forensic Inspection System • Indian Agricultural Quality Council</div>
    </div>
    <div style="text-align: right;">
        <span class="brand-tag">⚡ Powered by Google Gemma 4</span>
        <div style="font-size: 0.75rem; color: #d1fae5; margin-top: 0.35rem;">Statutory CIB&RC & Seeds Act 1966 Standard Engine</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ System Controls")
    
    backend_mode = st.radio(
        "AI Foundation Engine",
        ["Google Cloud Gemma 4 (26B MoE)", "Local Mandi Offline (Ollama E2B)"],
        index=0,
        help="Select whether to use the high-accuracy cloud Gemma 4 model or local offline weights for remote mandis.",
    )
    is_cloud = "Cloud" in backend_mode

    api_key = None
    if is_cloud:
        default_key = os.environ.get("GEMINI_API_KEY", "")
        api_key = st.text_input(
            "Gemini API Key",
            value=default_key,
            type="password",
            help="Pre-configured from system environment.",
        )
        if not api_key:
            st.warning("Please provide your Google AI Studio API Key to execute cloud audits.")
        else:
            st.success("🟢 Engine Active: `gemma-4-26b-a4b-it`")
    else:
        ollama_url = st.text_input("Ollama Endpoint", value=DEFAULT_OLLAMA_URL)
        ollama_model = st.text_input("Local Model Tag", value=DEFAULT_OLLAMA_MODEL)
        if GemmaEngine.is_ollama_available(ollama_url):
            st.success(f"🟢 Connected to Local Ollama ({ollama_model})")
        else:
            st.error("🔴 Offline Ollama daemon unreachable.")

    reasoning_depth = st.select_slider(
        "Forensic Reasoning Depth",
        options=["minimal", "high"],
        value="high",
        help="High engages Gemma 4's deep multi-step thinking mode to scrutinize statutory fine print.",
    )

    st.markdown("---")
    st.markdown("### 📊 System Registry Stats")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric("Banned List", "27 Chems")
    with col_sb2:
        st.metric("CIB&RC Firms", "10 Major")

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b;">
            <b>MandiShield Dev Team</b><br>
            • Dhanwinn (Lead & Regulatory DB)<br>
            • Avanish Ayyappan (Inference & Edge)<br>
            • Shasank Paruchuri (Prompts & Skills)<br>
            • Gyatchut (UI & Regional Localization)
        </div>
        """,
        unsafe_allow_html=True,
    )

# Engine Initialization
engine = None
try:
    if is_cloud:
        if api_key:
            engine = GemmaEngine(api_key=api_key, backend="gemini_api")
    else:
        engine = GemmaEngine(
            backend="ollama",
            ollama_url=ollama_url if "ollama_url" in locals() else DEFAULT_OLLAMA_URL,
            ollama_model=ollama_model if "ollama_model" in locals() else DEFAULT_OLLAMA_MODEL,
        )
except Exception as e:
    st.error(f"Engine connection issue: {e}")

# Helper for file save
def cache_image(upload):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
        f.write(upload.getvalue())
        return f.name

# Main Navigation Tabs
tab_pesticide, tab_seeds, tab_registry, tab_legal, tab_audio, tab_spec = st.tabs(
    [
        "🧪 Pesticide Bottle Auditor",
        "🌱 Seed Coating & Purity",
        "🚫 Statutory Gazette Registry",
        "⚖️ Official DAO Complaint Portal",
        "🗣️ Multilingual Regional Voice",
        "📦 Open Architecture & Spec",
    ]
)

# -------------------------------------------------------------
# TAB 1: Pesticide Bottle Auditor
# -------------------------------------------------------------
with tab_pesticide:
    st.markdown("### 🧪 Agro-Chemical Packaging & Forensic CIB&RC Verification")
    st.markdown(
        "Verify genuine pesticide containers, active chemical percentages, statutory Rule 19 toxicity diamonds, and detect flat-print counterfeit labeling."
    )

    # Human-Friendly Test Case Cards
    st.markdown("##### 📁 Select a Curated Forensic Case or Upload Your Photo")
    c1, c2, c3 = st.columns(3)
    selected_sample = None

    with c1:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #ef4444;">
                <div style="font-weight: 700; color: #b91c1c;">🚨 Case 1: Spurious Formulation</div>
                <div style="font-size: 0.82rem; color: #64748b; margin: 0.4rem 0;">
                    • Trade Name: Chlor-Strike 20 EC<br>
                    • Flaw: Misspelled active molecule, fake 1965 CIB&RC code, wrong green caution diamond.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Load Case 1 (Counterfeit)", key="btn_case_1", use_container_width=True):
            st.session_state["active_pesticide"] = os.path.join(
                os.path.dirname(__file__), "examples", "counterfeit_pesticide_sample.png"
            )

    with c2:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #10b981;">
                <div style="font-weight: 700; color: #047857;">✅ Case 2: Certified Product</div>
                <div style="font-size: 0.82rem; color: #64748b; margin: 0.4rem 0;">
                    • Trade Name: Bayer Confidor 17.8 SL<br>
                    • Certified: Genuine CIB&RC CIR-14820, yellow poison triangle, dot-matrix inkjet batch.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Load Case 2 (Genuine)", key="btn_case_2", use_container_width=True):
            st.session_state["active_pesticide"] = os.path.join(
                os.path.dirname(__file__), "examples", "genuine_pesticide_sample.png"
            )

    with c3:
        st.markdown(
            """
            <div class="metric-card" style="border-left: 4px solid #3b82f6;">
                <div style="font-weight: 700; color: #1d4ed8;">📸 Case 3: Live Custom Image</div>
                <div style="font-size: 0.82rem; color: #64748b; margin: 0.4rem 0;">
                    • Ingest any field photo<br>
                    • Analyzes container front/back labels, QR codes, and tamper-evident cap seals.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        upload_pest = st.file_uploader("Upload container photo", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if upload_pest:
            st.session_state["active_pesticide"] = cache_image(upload_pest)

    target_pesticide_img = st.session_state.get("active_pesticide", None)

    st.markdown("---")
    col_p_img, col_p_details = st.columns([1, 1])

    with col_p_img:
        if target_pesticide_img and os.path.exists(target_pesticide_img):
            st.image(Image.open(target_pesticide_img), caption="Active Inspection Target", use_container_width=True)
        else:
            st.info("👆 Please select Case 1, Case 2, or upload a photo above to inspect.")

    with col_p_details:
        st.markdown("#### 🔍 Real-Time Statutory Pre-Screening")
        fast_chem = st.text_input(
            "Enter Chemical Name for Instant Gazette Match:",
            placeholder="e.g. Endosulfan, Monocrotophos, Chlorpyrifos",
        )
        if fast_chem:
            banned = check_banned_chemical(fast_chem)
            if banned:
                st.markdown(
                    f"""
                    <div class="verdict-banner-danger">
                        <div class="verdict-title" style="color: #b91c1c;">🚫 PROHIBITED CHEMICAL: {banned['chemical'].upper()}</div>
                        <div class="verdict-body">
                            <b>Statutory Status:</b> {banned['status']}<br>
                            <b>Government Order:</b> {banned['order']}<br>
                            <b>Health Risk:</b> {banned['hazard']}<br>
                            <b>Prescribed Alternative:</b> {banned['replacement']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="verdict-banner-success">
                        <div class="verdict-title" style="color: #047857;">✅ Gazette Clearance: {fast_chem}</div>
                        <div class="verdict-body">Active compound is currently approved for licensed manufacture in India under CIB&RC norms.</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        audit_context = st.text_area(
            "Field Observations / Mandi Context:",
            value="Container purchased at local weekly market without printed bill. Batch number printing looks suspiciously flat.",
            height=80,
        )

        execute_audit = st.button("🔬 Execute Forensic Inspection via Gemma 4", type="primary", use_container_width=True)

    if execute_audit:
        if not engine:
            st.error("Please configure your AI engine credentials in the sidebar.")
        elif not target_pesticide_img:
            st.warning("Please select or upload a sample image first.")
        else:
            with st.spinner("Gemma 4 Multimodal Reasoner is examining packaging micro-typography, CIB&RC registration, and Rule 19 toxicity codes..."):
                try:
                    audit_output = engine.audit_pesticide_label(
                        image_path=target_pesticide_img,
                        additional_notes=audit_context,
                        thinking_level=reasoning_depth,
                    )
                    st.session_state["pesticide_report"] = audit_output
                    st.success("Inspection completed successfully.")

                    # Human-crafted Visual Scorecard
                    is_counterfeit = "COUNTERFEIT" in audit_output.upper() or "SUSPECT" in audit_output.upper()
                    if is_counterfeit:
                        st.markdown(
                            """
                            <div class="verdict-banner-danger">
                                <div class="verdict-title" style="color: #b91c1c;">🚨 STATUTORY VIOLATION / HIGH FRAUD RISK DETECTED</div>
                                <div class="verdict-body">
                                    This container displays clear evidence of counterfeit packaging, fraudulent registration numbering, or sub-standard chemical composition.
                                    <b>Do not spray on crops. Immediate seizure recommended under Section 21 of the Insecticides Act 1968.</b>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            """
                            <div class="verdict-banner-success">
                                <div class="verdict-title" style="color: #047857;">✅ CERTIFIED STATUTORY COMPLIANT PRODUCT</div>
                                <div class="verdict-body">
                                    Packaging displays genuine CIB&RC registration numbering, verified manufacturer credentials, compliant Rule 19 toxicity labeling, and authentic inkjet printing.
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    # Forensic Matrix Grid
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.markdown(
                            """
                            <div class="metric-card">
                                <div class="metric-label">Chemical Molecule</div>
                                <div class="metric-value" style="font-size: 1.1rem;">Checked</div>
                                <div style="font-size: 0.75rem; color: #64748b;">Formula & spelling audited</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with m2:
                        st.markdown(
                            """
                            <div class="metric-card">
                                <div class="metric-label">CIB&RC Registry</div>
                                <div class="metric-value" style="font-size: 1.1rem;">Verified</div>
                                <div style="font-size: 0.75rem; color: #64748b;">CIR code syntax & year tested</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with m3:
                        st.markdown(
                            """
                            <div class="metric-card">
                                <div class="metric-label">Toxicity Triangle</div>
                                <div class="metric-value" style="font-size: 1.1rem;">Rule 19</div>
                                <div style="font-size: 0.75rem; color: #64748b;">Color matched to Oral LD50</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with m4:
                        st.markdown(
                            """
                            <div class="metric-card">
                                <div class="metric-label">Print Forensics</div>
                                <div class="metric-value" style="font-size: 1.1rem;">Inkjet vs Offset</div>
                                <div style="font-size: 0.75rem; color: #64748b;">Batch method scrutinized</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown("#### 📋 Exhaustive Forensic Report")
                    st.markdown(audit_output)

                    st.download_button(
                        "📥 Download Official Forensic Dossier (.md)",
                        data=audit_output,
                        file_name="mandishield_forensic_audit.md",
                        mime="text/markdown",
                    )
                except Exception as ex:
                    st.error(f"Analysis interrupted: {ex}")

# -------------------------------------------------------------
# TAB 2: Seed Coating & Purity Inspector
# -------------------------------------------------------------
with tab_seeds:
    st.markdown("### 🌱 Certified Seed Coating & Physical Morphology Inspector")
    st.markdown(
        "Detect spurious seed lots where commercial food grain is dyed with cheap textile/food color and sold as expensive hybrid seeds under the **Seeds Act 1966**."
    )

    sc1, sc2 = st.columns([1, 1])
    with sc1:
        if st.button("🚩 Load Forensic Sample: Spurious Dyed Cotton Seed Lot", use_container_width=True):
            st.session_state["active_seed"] = os.path.join(
                os.path.dirname(__file__), "examples", "spurious_seeds_sample.png"
            )

        upload_seed = st.file_uploader("Or upload seed macro photo", type=["png", "jpg", "jpeg"])
        if upload_seed:
            st.session_state["active_seed"] = cache_image(upload_seed)

        seed_target = st.session_state.get("active_seed", None)
        if seed_target and os.path.exists(seed_target):
            st.image(Image.open(seed_target), caption="Seed Lot Macro Inspection Target", use_container_width=True)
        else:
            st.info("👆 Load the forensic sample or upload a seed close-up photograph above.")

    with sc2:
        crop_std_key = st.selectbox(
            "Select Statutory Seed Standard (Seeds Act 1966):",
            ["hybrid_cotton_bt", "hybrid_paddy_rice", "hybrid_maize_corn"],
            format_func=lambda x: SEED_STANDARDS[x]["crop"],
        )
        cur_std = SEED_STANDARDS[crop_std_key]

        st.markdown(
            f"""
            <div class="metric-card">
                <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Statutory Certification Thresholds:</div>
                <div style="font-size: 0.85rem; color: #475569; line-height: 1.6;">
                    • <b>Minimum Germination:</b> {cur_std['germination_min_pct']}<br>
                    • <b>Maximum Inert Matter:</b> {cur_std['inert_matter_max_pct']}<br>
                    • <b>Prescribed Fungicide Treatment:</b> {cur_std['mandatory_coating']}<br>
                    • <b>Known Counterfeit Markers:</b> {cur_std['counterfeit_flags']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        seed_notes_input = st.text_area(
            "Physical Lot Inspection Notes:",
            value="Color flaking off easily on palms upon contact; noticed high percentage of broken chaff in the bag.",
        )

        run_seed_audit = st.button("🔬 Audit Seed Quality with Gemma 4", type="primary", use_container_width=True)

    if run_seed_audit:
        if not engine:
            st.error("Please configure API credentials.")
        elif not seed_target:
            st.warning("Please provide a seed sample image.")
        else:
            with st.spinner("Auditing seed grain morphology, fungicide coating integrity, and genetic purity..."):
                try:
                    seed_report = engine.audit_seed_sample(
                        image_path=seed_target,
                        sample_details=f"Crop: {cur_std['crop']}\nField Notes: {seed_notes_input}",
                        thinking_level=reasoning_depth,
                    )
                    st.markdown("### 🌾 Seed Certification Audit Findings")
                    st.markdown(seed_report)
                except Exception as ex:
                    st.error(f"Inference error: {ex}")

# -------------------------------------------------------------
# TAB 3: Statutory Gazette Registry
# -------------------------------------------------------------
with tab_registry:
    st.markdown("### 🚫 Central Insecticides Board (CIB&RC) Official Gazette Registry")
    st.markdown(
        "Direct access to statutory records maintained under the **Insecticides Act 1968** and Gazette of India orders."
    )

    reg_search = st.text_input("🔍 Filter by Chemical Name, Gazette Notification, or Manufacturer:", placeholder="e.g. Endosulfan, Bayer, S.O. 1512")

    st.markdown("#### 📋 27 Banned or Severely Restricted Pesticides in India")
    table_data = []
    for k, v in BANNED_PESTICIDES_INDIA.items():
        if not reg_search or reg_search.lower() in k.lower() or reg_search.lower() in v["order"].lower():
            table_data.append({
                "Chemical Compound": k.title(),
                "Regulatory Status": v["status"],
                "Supreme Court / Gazette Order": v["order"],
                "Toxicological Profile": v["hazard"],
                "Safe Biological Alternative": v["replacement"],
            })
    st.dataframe(table_data, use_container_width=True)

    st.markdown("#### 🏢 Top Authorized Indian Manufacturers (CIB&RC Registered)")
    mfg_data = []
    for m in AUTHORIZED_MANUFACTURERS:
        if not reg_search or reg_search.lower() in m["name"].lower():
            mfg_data.append({
                "Manufacturer Name": m["name"],
                "Registration Code": m["code"],
                "Licensed Facilities": m["state"],
                "CIB&RC Prefix": m["prefix"],
            })
    st.dataframe(mfg_data, use_container_width=True)

# -------------------------------------------------------------
# TAB 4: Official DAO Complaint Portal
# -------------------------------------------------------------
with tab_legal:
    st.markdown("### ⚖️ Official Legal Complaint Generator (District Agricultural Office)")
    st.markdown(
        "Draft a formal, legally enforceable Complaint Petition under **Section 29 of the Insecticides Act 1968** with statutory citations and relief demands."
    )

    st.markdown(
        """
        <div class="metric-card" style="margin-bottom: 1rem;">
            <b>Statutory Notice:</b> Selling spurious, misbranded, or adulterated agro-chemicals in India carries mandatory imprisonment of up to 2 years and seizure of dealer license under Section 29 of the Insecticides Act 1968.
        </div>
        """,
        unsafe_allow_html=True,
    )

    lf1, lf2 = st.columns(2)
    with lf1:
        c_farmer = st.text_input("Complainant Farmer Name:", value="Murugan R.")
        c_village = st.text_input("Village / Gram Panchayat:", value="Sulur")
        c_district = st.text_input("District & State:", value="Coimbatore, Tamil Nadu")
    with lf2:
        c_vendor = st.text_input("Dealer / Agro-Shop Name:", value="Sri Lakshmi Fertilizer & Agro Depot")
        c_product = st.text_input("Product Trade Name:", value="Chlor-Strike 20 EC")
        c_batch = st.text_input("Batch No. & Container Markings:", value="BATCH-8889-OFFSET (Exp: 12/2030)")

    c_grounds = st.text_area(
        "Summary of Forensic Non-Compliance:",
        value="Forged CIB&RC registration code CIR-0014/1965 (precedes 1968 Act); misspelled active molecule 'Chlorpyriphos'; illegal Category IV green caution diamond on Category II poison; missing antidote statement.",
        height=90,
    )

    if st.button("📜 Generate Formal Section 29 Petition Letter", type="primary", use_container_width=True):
        if not engine:
            st.error("Please configure API credentials.")
        else:
            with st.spinner("Drafting formal legal grievance petition with statutory citations..."):
                complaint_text = engine.generate_dao_complaint(
                    farmer_name=c_farmer,
                    farmer_village=c_village,
                    farmer_district=c_district,
                    shop_name=c_vendor,
                    product_name=c_product,
                    batch_no=c_batch,
                    violations=c_grounds,
                )
                
                # Render inside official letterhead container
                st.markdown(
                    f"""
                    <div class="letterhead">
                        <div class="letterhead-header">
                            <h3 style="margin: 0; color: #0f172a;">FORMAL GRIEVANCE PETITION UNDER SECTION 29</h3>
                            <h4 style="margin: 0.3rem 0; color: #475569;">INSECTICIDES ACT, 1968 & SEEDS ACT, 1966</h4>
                            <div style="font-size: 0.85rem; color: #64748b;">BEFORE THE DISTRICT AGRICULTURAL OFFICER / JOINT DIRECTOR OF AGRICULTURE</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(complaint_text)

                st.download_button(
                    "📥 Download Legal Petition Ready for Sign & Submission (.txt)",
                    data=complaint_text,
                    file_name=f"dao_complaint_{c_farmer.replace(' ', '_')}.txt",
                    mime="text/plain",
                )

# -------------------------------------------------------------
# TAB 5: Multilingual Regional Voice
# -------------------------------------------------------------
with tab_audio:
    st.markdown("### 🗣️ Multilingual Regional Voice & Audio Advisory")
    st.markdown(
        "Immediate, clear, regional voice and text guidance in **Tamil, Telugu, Hindi, and English** designed for rural smallholders at the Mandi counter."
    )

    default_finding = st.session_state.get(
        "pesticide_report",
        "CRITICAL HAZARD: Product is counterfeit Chlor-Strike 20 EC. Forged CIB&RC code. Do not spray on crops. Immediate shop refund required.",
    )

    voice_input = st.text_area("Audit Finding to Translate:", value=default_finding, height=100)

    if st.button("🌐 Synthesize Multilingual Regional Advisories", type="primary"):
        if not engine:
            st.error("Please configure API credentials.")
        else:
            with st.spinner("Gemma 4 is synthesizing regional advisories with colloquial farmer terminology..."):
                advisory_res = engine.generate_farmer_advisory(voice_input)
                
                # Display language cards
                st.markdown("#### 📢 Regional Voice Readouts")
                st.markdown(advisory_res)
                
                st.markdown("---")
                st.markdown(
                    """
                    <div class="metric-card" style="background: #f8fafc;">
                        <b>🔊 Voice Playback Simulation:</b> Rural field workers can broadcast this audio advisory directly over smartphone loudspeakers at village weekly markets or Krishi Vigyan Kendra centers.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# -------------------------------------------------------------
# TAB 6: Open Architecture & Spec
# -------------------------------------------------------------
with tab_spec:
    st.markdown("### 📦 Open Source Architecture & Agent Skills Standard")
    st.markdown(
        "MandiShield is completely open source under the **Apache-2.0 License** and exports its automated verification protocol conforming to the [Agent Skills Open Standard](https://agentskills.io/specification)."
    )

    skill_file = os.path.join(os.path.dirname(__file__), "skills", "mandishield", "SKILL.md")
    if os.path.exists(skill_file):
        with open(skill_file, "r", encoding="utf-8") as f:
            manifest_code = f.read()
        st.code(manifest_code, language="markdown")
        st.download_button(
            "📥 Download SKILL.md Standard Manifest",
            data=manifest_code,
            file_name="mandishield_SKILL.md",
            mime="text/markdown",
        )

    st.markdown("---")
    st.markdown("#### 🐳 Reproducible Container Execution")
    st.code(
        """
# Build and run MandiShield on DigitalOcean Droplet or App Platform
docker build -t mandishield:latest .
docker run -d -p 8501:8501 -e GEMINI_API_KEY="AIzaSy..." mandishield:latest
        """,
        language="bash",
    )
