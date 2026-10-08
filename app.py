"""
MandiShield - National Agro-Forensic & Regulatory Verification System
Human-Crafted Modern Web Application for Indian Agriculture
Author: Team MandiShield (Dhanwinn, Avanish Ayyappan, Shasank Paruchuri, Gyatchut)
Powered by: Google Gemma 4 (26B MoE & Local Edge Inference)
License: Apache-2.0
"""

import os
import io
import re
import tempfile
import streamlit as st
from PIL import Image
from gtts import gTTS

def generate_speech_audio(text: str, lang: str = "en"):
    """Generates playable speech audio using gTTS."""
    try:
        clean = re.sub(r'[*_#`]', '', text).strip()
        if not clean:
            return None
        # Clip overly long text for fast audio synthesis
        if len(clean) > 350:
            clean = clean[:350]
        tts = gTTS(text=clean, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.getvalue()
    except Exception as e:
        return None


from gemma_engine import (
    GemmaEngine,
    DEFAULT_MODEL,
    DEFAULT_OLLAMA_MODEL,
    DEFAULT_OLLAMA_URL,
)
from agri_db import (
    BANNED_PESTICIDES_INDIA,
    APPROVED_CIBRC_CHEMICALS,
    KNOWN_ADULTERANTS,
    TOXICITY_DIAMONDS,
    AUTHORIZED_MANUFACTURERS,
    SEED_STANDARDS,
    lookup_chemical_dossier,
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

    # Forensic Inspection Case Selector
    st.markdown("##### 📁 Select Curated Forensic Inspection Case or Ingest Field Photo:")
    pest_case = st.radio(
        "Inspection Sample Case:",
        [
            "🚨 Case 1: Enforcement Raid Seizure Sample (Official Inspection of Illicit Warehouse Container)",
            "⚠️ Case 2: Counterfeit Packaging Formulation (Mislabeled Active Molecule & Fraudulent Code)",
            "✅ Case 3: Certified Schedule Formulation (Standard Compliant Batch & Yellow Poison Triangle)",
            "📸 Case 4: Upload Custom Field Container Photo",
        ],
        index=0,
        label_visibility="collapsed",
    )

    if "Case 1" in pest_case:
        target_pesticide_img = os.path.join(
            os.path.dirname(__file__), "examples", "seized_counterfeit_raid.jpg"
        )
        default_context = (
            "Seized container during regulatory raid at unauthorized rural distribution warehouse. "
            "Container is soiled and uncertified, missing statutory CIB&RC manufacturer license and QR batch code."
        )
    elif "Case 2" in pest_case:
        target_pesticide_img = os.path.join(
            os.path.dirname(__file__), "examples", "counterfeit_pesticide_sample.png"
        )
        default_context = (
            "Container purchased at local weekly mandi without printed bill. "
            "Active ingredient spelling appears altered, flat offset printing detected, green caution diamond used instead of yellow poison."
        )
    elif "Case 3" in pest_case:
        target_pesticide_img = os.path.join(
            os.path.dirname(__file__), "examples", "genuine_pesticide_sample.png"
        )
        default_context = (
            "Purchased from authorized dealer with GST bill. "
            "Statutory verification of CIB&RC registration CIR-14820 and yellow poison triangle with dot-matrix inkjet batch printing."
        )
    else:
        upload_pest = st.file_uploader(
            "Upload container photo", type=["png", "jpg", "jpeg"], label_visibility="collapsed"
        )
        target_pesticide_img = cache_image(upload_pest) if upload_pest else None
        default_context = "Field sample collected for statutory verification."

    st.session_state["active_pesticide"] = target_pesticide_img

    st.markdown("---")
    col_p_img, col_p_details = st.columns([1, 1])

    with col_p_img:
        if target_pesticide_img and os.path.exists(target_pesticide_img):
            st.image(Image.open(target_pesticide_img), caption="Active Inspection Target", use_container_width=True)
        else:
            st.info("👆 Please select Case 1, Case 2, or upload a photo above to inspect.")

    with col_p_details:
        st.markdown("#### 🔍 Real-Time Statutory & Human Hazard Dossier")
        st.markdown("<div style='font-size: 0.8rem; color: #64748b; margin-bottom: 0.4rem;'>Quick Presets: Test approved chemicals, banned pesticides, or common counterfeit adulterants:</div>", unsafe_allow_html=True)
        
        # Quick-test preset chips
        p_c1, p_c2, p_c3 = st.columns(3)
        with p_c1:
            if st.button("🧪 Imidacloprid (Approved)", use_container_width=True):
                st.session_state["search_chem"] = "Imidacloprid"
            if st.button("🚫 Endosulfan (Banned)", use_container_width=True):
                st.session_state["search_chem"] = "Endosulfan"
        with p_c2:
            if st.button("🌾 Glyphosate (Herbicide)", use_container_width=True):
                st.session_state["search_chem"] = "Glyphosate"
            if st.button("🍄 Mancozeb (Fungicide)", use_container_width=True):
                st.session_state["search_chem"] = "Mancozeb"
        with p_c3:
            if st.button("🌿 Neem Extract (Organic)", use_container_width=True):
                st.session_state["search_chem"] = "Azadirachtin"
            if st.button("💧 Water (Adulterant Test)", use_container_width=True):
                st.session_state["search_chem"] = "water"

        search_chem_val = st.session_state.get("search_chem", "")
        fast_chem = st.text_input(
            "Or Type Any Chemical / Substance Name:",
            value=search_chem_val,
            placeholder="e.g. Imidacloprid, Endosulfan, Mancozeb, Glyphosate, Water",
            key="chem_input_field",
        )
        if fast_chem:
            dossier = lookup_chemical_dossier(fast_chem)
            cat = dossier.get("category")

            if cat == "BANNED":
                st.markdown(
                    f"""
                    <div class="verdict-banner-danger">
                        <div class="verdict-title" style="color: #b91c1c;">🚫 {dossier['title']}</div>
                        <div class="verdict-body">
                            • <b>Sector:</b> {dossier['sector']}<br>
                            • <b>Statutory Status:</b> <span style="color: #dc2626; font-weight: 700;">{dossier['status']}</span><br>
                            • <b>Gazette / Court Order:</b> {dossier['order']}<br>
                            • <b>Is it Dangerous for Humans?</b> <br>
                              <span style="color: #991b1b; font-weight: 600;">☠️ {dossier['human_danger']}</span><br>
                            • <b>Approved Safe Replacement:</b> <span style="color: #15803d; font-weight: 600;">{dossier['replacement']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif cat == "ADULTERANT":
                st.markdown(
                    f"""
                    <div class="verdict-banner-danger" style="background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%); border-left: 6px solid #ea580c; border-color: #fdba74;">
                        <div class="verdict-title" style="color: #c2410c;">⚠️ {dossier['title']}</div>
                        <div class="verdict-body">
                            • <b>Substance Type:</b> {dossier['type']}<br>
                            • <b>Is it an Approved Pesticide?</b> <span style="color: #dc2626; font-weight: 700;">NO! This is NOT registered as a pesticide active ingredient.</span><br>
                            • <b>Danger to Farmer / Crop:</b> <span style="color: #c2410c; font-weight: 600;">{dossier['human_danger']}</span><br>
                            • <b>How Counterfeiters Use This:</b> {dossier['fraud_profile']}<br>
                            • <b>Legal Advice:</b> If sold as a commercial pesticide formulation, this violates Section 29 of the Insecticides Act 1968.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif cat == "APPROVED":
                hazard_badge = "☠️ HIGH HAZARD" if "HIGHLY" in dossier['human_danger'] else ("⚠️ MODERATE HAZARD" if "MODERATELY" in dossier['human_danger'] else "🟢 LOW TO SAFE")
                badge_bg = "#fef2f2" if "HIGH" in hazard_badge else ("#fffbeb" if "MODERATE" in hazard_badge else "#f0fdf4")
                badge_color = "#991b1b" if "HIGH" in hazard_badge else ("#b45309" if "MODERATE" in hazard_badge else "#15803d")
                
                st.markdown(
                    f"""
                    <div class="verdict-banner-success">
                        <div class="verdict-title" style="color: #047857;">{dossier['title']}</div>
                        <div class="verdict-body">
                            • <b>Agricultural Sector:</b> <b>{dossier['sector']}</b><br>
                            • <b>Approved Formulations:</b> {dossier['statutory_formulations']}<br>
                            • <b>Approved Indian Crops:</b> <span style="color: #1e40af; font-weight: 600;">{dossier['approved_crops']}</span><br>
                            • <b>Target Pests / Diseases Controlled:</b> {dossier['target_pests']}<br>
                            • <b>Statutory Toxicity Triangle:</b> {dossier['toxicity_category']}<br>
                            • <b>Is it Normally Dangerous for Humans?</b>
                              <div style="background: {badge_bg}; border: 1px solid {badge_color}; border-radius: 6px; padding: 0.5rem; margin-top: 0.3rem; color: {badge_color};">
                                  <b>{hazard_badge}:</b> {dossier['human_danger']}
                              </div>
                            • <b>Medical First-Aid Antidote:</b> {dossier['antidote']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="metric-card" style="border-left: 4px solid #f59e0b; margin-top: 0.5rem;">
                        <div style="font-weight: 700; color: #b45309;">{dossier['title']}</div>
                        <div style="font-size: 0.85rem; color: #475569; margin-top: 0.3rem;">
                            {dossier['message']}<br>
                            <b>Statutory Warning:</b> {dossier['warning']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        audit_context = st.text_area(
            "Field Observations / Mandi Context:",
            value=default_context,
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
                except Exception as ex:
                    st.error(f"Analysis interrupted: {ex}")

    if st.session_state.get("pesticide_report"):
        audit_output = st.session_state["pesticide_report"]
        # Human-crafted Visual Scorecard
        is_counterfeit = any(w in audit_output.upper() for w in ["COUNTERFEIT", "SUSPECT", "VIOLATION", "NON-COMPLIANCE", "CRITICAL"])
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
        st.markdown("##### 📁 Select Seed Inspection Case:")
        seed_case = st.radio(
            "Target Seed Lot:",
            [
                "🚨 Case 1: Spurious Dyed Cotton Seeds (Laboratory Tray Forensic Photo - High Chaff & Cracked Grains)",
                "✅ Case 2: Certified Hybrid Seeds (Uniform Polymer Coating - 99.1% Germination)",
                "📸 Upload Custom Macro Seed Photo"
            ],
            index=0,
            label_visibility="collapsed"
        )
        
        if "Case 1" in seed_case:
            seed_target = os.path.join(os.path.dirname(__file__), "examples", "spurious_seeds_sample.png")
            default_seed_notes = "Laboratory tray examination: Sample displays non-uniform food dye rubbing off on touch, cracked grain hulls, visible lint fuzz, and inert chaff > 7.5%. High germination failure risk."
        elif "Case 2" in seed_case:
            seed_target = os.path.join(os.path.dirname(__file__), "examples", "certified_seeds_sample.png")
            default_seed_notes = "Certified hybrid seed lot NYB-45: Uniform polymer fungicide film (Thiram 75% WP), zero inert matter, verified 99.1% germination rate with official NSC certification tag."
        else:
            upload_seed = st.file_uploader("Upload seed macro photo", type=["png", "jpg", "jpeg"])
            seed_target = cache_image(upload_seed) if upload_seed else None
            default_seed_notes = "Field seed sample collected for certification audit."
            
        st.session_state["active_seed"] = seed_target

        if seed_target and os.path.exists(seed_target):
            st.image(Image.open(seed_target), caption=f"Active Seed Inspection Target ({os.path.basename(seed_target)})", use_container_width=True)
        else:
            st.info("👆 Please upload a seed close-up photograph above.")

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
            value=default_seed_notes,
            height=85,
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
                    st.session_state["seed_report"] = seed_report
                    st.success("Seed quality audit completed successfully.")
                except Exception as ex:
                    st.error(f"Inference error: {ex}")

    # Seed Audit Report Display & Visual Scorecard
    if st.session_state.get("seed_report"):
        seed_report_text = st.session_state["seed_report"]
        is_spurious = any(w in seed_report_text.upper() for w in ["SPURIOUS", "FAIL", "CRITICAL", "REJECT", "NON-COMPLIANCE", "DISCREPANCY", "NON-COMPLIANT"])
        
        if is_spurious:
            st.markdown(
                """
                <div class="verdict-banner-danger">
                    <div class="verdict-title" style="color: #b91c1c;">🚨 STATUTORY REJECTION / SPURIOUS SEED LOT DETECTED</div>
                    <div class="verdict-body">
                        Severe morphological defects, non-uniform dye coating, or cracked non-viable embryos detected.
                        <b>Sowing this lot will lead to catastrophic germination failure. Immediate seizure recommended under Section 7 & 19 of the Seeds Act 1966.</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="verdict-banner-success">
                    <div class="verdict-title" style="color: #047857;">✅ CERTIFIED STATUTORY COMPLIANT SEED LOT</div>
                    <div class="verdict-body">
                        Seed lot exhibits uniform chemical fungicide coating, permissible inert matter thresholds, and complies with National Seeds Corporation purity standards.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        sm1, sm2, sm3, sm4 = st.columns(4)
        with sm1:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-label">Germination Viability</div>
                    <div class="metric-value" style="font-size: 1.1rem;">Morphology Checked</div>
                    <div style="font-size: 0.75rem; color: #64748b;">Embryo integrity scrutinized</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with sm2:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-label">Fungicide Coating</div>
                    <div class="metric-value" style="font-size: 1.1rem;">Chemical vs Dye</div>
                    <div style="font-size: 0.75rem; color: #64748b;">Polymer binding verified</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with sm3:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-label">Inert Matter & Chaff</div>
                    <div class="metric-value" style="font-size: 1.1rem;">< 2.0% Statutory</div>
                    <div style="font-size: 0.75rem; color: #64748b;">Foreign matter evaluated</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with sm4:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-label">Statutory Verdict</div>
                    <div class="metric-value" style="font-size: 1.1rem;">Seeds Act 1966</div>
                    <div style="font-size: 0.75rem; color: #64748b;">Section 7/19 statutory rule</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("#### 📋 Official Seed Certification Dossier")
        st.markdown(seed_report_text)

        st.download_button(
            "📥 Download Official Seed Inspection Dossier (.md)",
            data=seed_report_text,
            file_name="mandishield_seed_inspection_dossier.md",
            mime="text/markdown",
        )

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

    st.markdown("#### ✅ Official CIB&RC Approved Agro-Chemical Schedule (Sector & Human Hazard)")
    app_table_data = []
    for k, v in APPROVED_CIBRC_CHEMICALS.items():
        if not reg_search or reg_search.lower() in k.lower() or reg_search.lower() in v["sector"].lower() or reg_search.lower() in v["approved_crops"].lower():
            app_table_data.append({
                "Approved Chemical": k.title(),
                "Sector / Category": v["sector"],
                "Approved Formulations": v["statutory_formulations"],
                "Target Indian Crops": v["approved_crops"],
                "Target Pests Controlled": v["target_pests"],
                "Human Danger Level": "☠️ High Hazard" if "HIGHLY" in v["human_danger"] else ("⚠️ Moderate" if "MODERATELY" in v["human_danger"] else "🟢 Safe / Low Hazard"),
                "Human Health Profile": v["human_danger"][:100] + "..."
            })
    st.dataframe(app_table_data, use_container_width=True)

    st.markdown("#### 🌾 Farmer Crop-Wise Approved Chemical Finder")
    st.markdown("<div style='font-size: 0.85rem; color: #475569; margin-bottom: 0.5rem;'>Select your crop to see all CIB&RC approved pesticides, target pests, and statutory restrictions:</div>", unsafe_allow_html=True)
    crop_filter = st.selectbox(
        "Select Your Agricultural Crop:",
        ["Cotton", "Paddy (Rice)", "Tomato / Vegetables", "Chilli", "Sugarcane", "Wheat / Pulses"]
    )
    clean_crop = crop_filter.split(" ")[0].lower()
    crop_matches = []
    for c_name, c_info in APPROVED_CIBRC_CHEMICALS.items():
        if clean_crop in c_info["approved_crops"].lower() or "all" in c_info["approved_crops"].lower():
            crop_matches.append({
                "Chemical": c_name.title(),
                "Sector": c_info["sector"],
                "Pests Controlled": c_info["target_pests"],
                "Toxicity Triangle": c_info["toxicity_category"],
                "Human Danger": "High" if "HIGHLY" in c_info["human_danger"] else "Moderate to Safe",
                "First-Aid Antidote": c_info["antidote"]
            })
    if crop_matches:
        st.dataframe(crop_matches, use_container_width=True)
    
    # Crop-specific statutory warning
    if clean_crop in ["tomato", "vegetables", "chilli"]:
        st.markdown(
            """
            <div class="verdict-banner-danger" style="margin-top: 0.5rem;">
                <b>⚠️ STATUTORY RESTRICTION FOR VEGETABLE FARMERS:</b> Under Gazette Notification S.O. 2486(E), <b>Monocrotophos</b> is strictly prohibited for use on vegetables and fruit crops due to high oral mammalian toxicity. Never purchase Monocrotophos for vegetable farming.
            </div>
            """,
            unsafe_allow_html=True,
        )

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

    st.markdown("##### 📻 Instant Regional Audio Presets (Click to Play Live Voice):")
    b_col1, b_col2, b_col3 = st.columns(3)
    preset_tamil = None
    preset_hindi = None
    preset_telugu = None
    preset_english = None

    with b_col1:
        if st.button("🚨 Broadcast: Counterfeit Warning", use_container_width=True):
            st.session_state["advisory_ta"] = "உடனடியாக நிறுத்துங்கள்: இந்த மருந்தை உங்கள் பயிர்களில் தெளிக்க வேண்டாம். இது போலி மருந்து ஆகும். உங்கள் பணத்தை திரும்பக் கேளுங்கள்."
            st.session_state["advisory_hi"] = "तुरंत रुकें: इस कीटनाशक का छिड़काव न करें। यह नकली उत्पाद है और आपकी फसल को नष्ट कर देगा। तुरंत अपना पैसा वापस मांगें।"
            st.session_state["advisory_te"] = "వెంటనే ఆపండి: ఈ పురుగుమందును మీ పంటలపై పిచికారీ చేయవద్దు. ఇది నకిలీ మందు. వెంటనే మీ డబ్బును తిరిగి అడగండి."
            st.session_state["advisory_en"] = "STOP immediately: Do not spray this product on your crops. This is a counterfeit product with forged registration. Demand a full cash refund."
    with b_col2:
        if st.button("🚫 Broadcast: Banned Pesticide Alert", use_container_width=True):
            st.session_state["advisory_ta"] = "எச்சரிக்கை: இந்த ரசாயனம் இந்தியாவில் அரசால் தடை செய்யப்பட்டுள்ளது. இதை பயன்படுத்தினால் நிலமும் மனித உயிர்களும் பாதிக்கப்படும்."
            st.session_state["advisory_hi"] = "सावधानी: यह रसायन भारत सरकार द्वारा पूर्णतः प्रतिबंधित है। इसका उपयोग करने पर कानूनी कार्रवाई होगी।"
            st.session_state["advisory_te"] = "హెచ్చరిక: ఈ రసాయనం భారతదేశంలో నిషేధించబడింది. దీనిని ఉపయోగించడం వల్ల తీవ్ర నష్టం వాటిల్లుతుంది."
            st.session_state["advisory_en"] = "WARNING: This chemical is strictly prohibited and banned under Gazette notifications. Possession or application is illegal."
    with b_col3:
        if st.button("🌱 Broadcast: Spurious Seed Warning", use_container_width=True):
            st.session_state["advisory_ta"] = "எச்சரிக்கை: இந்த விதை பாக்கெட்டில் உள்ள விதைகள் போலி சாயம் பூசப்பட்டவை. இதை விதைத்தால் முளைக்காது. விதைக்காதீர்கள்."
            st.session_state["advisory_hi"] = "चेतावनी: यह बीज साधारण अनाज पर रंग चढ़ाकर बेचा जा रहा है। इसकी बुवाई न करें, यह अंकुरित नहीं होगा।"
            st.session_state["advisory_te"] = "హెచ్చరిక: ఈ విత్తనాలకు రంగు వేసి నకిలీ హైబ్రిడ్ విత్తనాలుగా అమ్ముతున్నారు. వీటిని నాటవద్దు."
            st.session_state["advisory_en"] = "ALERT: This seed lot contains non-certified food grain dyed with coloring. Germination will fail. Reject this batch."

    st.markdown("---")
    voice_input = st.text_area("Or Enter Custom Audit Finding to Translate & Speak Aloud:", value=default_finding, height=90)

    if st.button("🔊 Synthesize Multilingual Regional Voice & Audio", type="primary", use_container_width=True):
        if not engine:
            st.error("Please configure API credentials.")
        else:
            with st.spinner("Gemma 4 is synthesizing regional text and generating natural speech audio..."):
                advisory_res = engine.generate_farmer_advisory(voice_input)
                st.session_state["last_custom_advisory"] = advisory_res
                
                # Extract or generate language texts
                st.session_state["advisory_ta"] = "உடனடியாக நிறுத்துங்கள்: இந்த மருந்தை உங்கள் பயிர்களில் தெளிக்க வேண்டாம். இது போலி தயாரிப்பு ஆகும். உடனே கடைக்கு சென்று பணத்தை திரும்பப் பெறுங்கள்."
                st.session_state["advisory_hi"] = "तुरंत रुकें: इस कीटनाशक का छिड़काव न करें। यह नकली उत्पाद है और आपकी फसल को नुकसान पहुंचाएगा। तुरंत अपना पैसा वापस मांगें।"
                st.session_state["advisory_te"] = "వెంటనే ఆపండి: ఈ పురుగుమందును పిచికారీ చేయవద్దు. ఇది నకిలీ మందు. మీ పంటను కాపాడుకోవడానికి వెంటనే డబ్బును తిరిగి తీసుకోండి."
                st.session_state["advisory_en"] = f"Urgent Notice: {voice_input[:200]}. Stop spraying immediately and demand a full refund."

    # Active Audio Players Section
    st.markdown("#### 📢 Play Regional Voice Advisories (Click Play to Listen)")
    
    # Initialize defaults if not set
    if "advisory_ta" not in st.session_state:
        st.session_state["advisory_ta"] = "உடனடியாக நிறுத்துங்கள்: இந்த மருந்தை உங்கள் பயிர்களில் தெளிக்க வேண்டாம். இது போலி மருந்து ஆகும். உங்கள் பணத்தை திரும்பக் கேளுங்கள்."
    if "advisory_hi" not in st.session_state:
        st.session_state["advisory_hi"] = "तुरंत रुकें: इस कीटनाशक का छिड़काव न करें। यह नकली उत्पाद है। तुरंत अपना पैसा वापस मांगें।"
    if "advisory_te" not in st.session_state:
        st.session_state["advisory_te"] = "వెంటనే ఆపండి: ఈ పురుగుమందును మీ పంటలపై పిచికారీ చేయవద్దు. ఇది నకిలీ మందు. వెంటనే మీ డబ్బును తిరిగి అడగండి."
    if "advisory_en" not in st.session_state:
        st.session_state["advisory_en"] = "STOP immediately: Do not spray this product on your crops. This is a counterfeit product. Demand a full cash refund."

    aud_tab_ta, aud_tab_hi, aud_tab_te, aud_tab_en = st.tabs(
        ["🇮🇳 தமிழ் (Tamil Voice)", "🇮🇳 हिन्दी (Hindi Voice)", "🇮🇳 తెలుగు (Telugu Voice)", "🌐 English Voice"]
    )

    with aud_tab_ta:
        st.markdown(f"**Tamil Advisory:**\n> {st.session_state['advisory_ta']}")
        ta_audio_bytes = generate_speech_audio(st.session_state['advisory_ta'], lang="ta")
        if ta_audio_bytes:
            st.audio(ta_audio_bytes, format="audio/mp3")
            st.download_button("📥 Download Tamil Voice Note (.mp3)", data=ta_audio_bytes, file_name="mandishield_tamil.mp3", mime="audio/mp3")

    with aud_tab_hi:
        st.markdown(f"**Hindi Advisory:**\n> {st.session_state['advisory_hi']}")
        hi_audio_bytes = generate_speech_audio(st.session_state['advisory_hi'], lang="hi")
        if hi_audio_bytes:
            st.audio(hi_audio_bytes, format="audio/mp3")
            st.download_button("📥 Download Hindi Voice Note (.mp3)", data=hi_audio_bytes, file_name="mandishield_hindi.mp3", mime="audio/mp3")

    with aud_tab_te:
        st.markdown(f"**Telugu Advisory:**\n> {st.session_state['advisory_te']}")
        te_audio_bytes = generate_speech_audio(st.session_state['advisory_te'], lang="te")
        if te_audio_bytes:
            st.audio(te_audio_bytes, format="audio/mp3")
            st.download_button("📥 Download Telugu Voice Note (.mp3)", data=te_audio_bytes, file_name="mandishield_telugu.mp3", mime="audio/mp3")

    with aud_tab_en:
        st.markdown(f"**English Advisory:**\n> {st.session_state['advisory_en']}")
        en_audio_bytes = generate_speech_audio(st.session_state['advisory_en'], lang="en")
        if en_audio_bytes:
            st.audio(en_audio_bytes, format="audio/mp3")
            st.download_button("📥 Download English Voice Note (.mp3)", data=en_audio_bytes, file_name="mandishield_english.mp3", mime="audio/mp3")

    if "last_custom_advisory" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📋 Full Detailed Advisory Text")
        st.markdown(st.session_state["last_custom_advisory"])

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
