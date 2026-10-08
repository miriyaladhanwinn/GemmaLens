"""
MandiShield - Indian Agricultural Regulatory & Chemical Database
Central Insecticides Board & Registration Committee (CIB&RC) and Seeds Act 1966 Reference Engine.
"""

from typing import Dict, List, Optional, Tuple
import re

# List of 27 Pesticides Banned or Severely Restricted in India (Gazette of India Notifications)
BANNED_PESTICIDES_INDIA: Dict[str, Dict[str, str]] = {
    "endosulfan": {
        "status": "COMPLETELY BANNED",
        "order": "Supreme Court of India (W.P. Civil 213/2011) & Gazette S.O. 116(E)",
        "hazard": "Severe neurotoxicity, congenital deformities, bioaccumulation.",
        "replacement": "Chlorantraniliprole 18.5% SC or Flubendiamide 39.35% SC"
    },
    "monocrotophos": {
        "status": "BANNED ON VEGETABLES / RESTRICTED",
        "order": "Gazette Notification S.O. 2486(E) & S.O. 3951(E)",
        "hazard": "Extremely high mammalian oral toxicity; WHO Class Ib. High incidence of fatal poisoning.",
        "replacement": "Spinosad 45% SC or Emamectin Benzoate 5% SG"
    },
    "carbofuran": {
        "status": "BANNED / PHASED OUT",
        "order": "Draft Banned List Gazette Notification 2020 (S.O. 1512(E))",
        "hazard": "Endocrine disruptor, high avian toxicity, ground water contamination.",
        "replacement": "Fipronil 0.3% GR or Cartap Hydrochloride 4% GR"
    },
    "paraquat dichloride": {
        "status": "HIGHLY RESTRICTED / BANNED IN MULTIPLE STATES",
        "order": "Restricted under Section 27 of Insecticides Act 1968; banned in Kerala, Odisha, Telangana",
        "hazard": "Fatal pulmonary fibrosis with no known antidote. Ingestion of 1 teaspoon is fatal.",
        "replacement": "Glufosinate Ammonium 13.5% SL"
    },
    "chlorpyrifos": {
        "status": "PROPOSED FOR BAN / BANNED ON RESIDENTIAL & VEGETABLE USES",
        "order": "Gazette S.O. 1512(E) 2020 Draft Order; 2023 Expert Committee Review",
        "hazard": "Developmental neurotoxicity in children, acetylcholinesterase inhibition.",
        "replacement": "Thiamethoxam 25% WG or Novaluron 10% EC"
    },
    "malathion": {
        "status": "RESTRICTED / BANNED IN PUBLIC HEALTH INDOOR SPRAY",
        "order": "Gazette S.O. 1512(E)",
        "hazard": "IARC Group 2A probable human carcinogen.",
        "replacement": "Neem-based Azadirachtin 10,000 PPM or Deltamethrin 2.5% WP"
    },
    "dichlorvos (ddvp)": {
        "status": "BANNED / RESTRICTED",
        "order": "Gazette S.O. 1512(E) / Expert Committee 2023",
        "hazard": "Organophosphate acute toxicity, nervous system paralysis.",
        "replacement": "Pymetrozine 50% WG"
    },
    "triazophos": {
        "status": "BANNED IN SELECTED CROPS / PROPOSED BAN",
        "order": "Gazette S.O. 1512(E)",
        "hazard": "Extremely toxic to honeybees and aquatic organisms.",
        "replacement": "Chlorantraniliprole 18.5% SC"
    },
    "benomyl": {
        "status": "BANNED IN ALL CROPS",
        "order": "Gazette Notification S.O. 2486(E)",
        "hazard": "Mutagenic and teratogenic effects.",
        "replacement": "Carbendazim + Mancozeb (or Trichoderma viride biological)"
    },
    "methomyl": {
        "status": "BANNED",
        "order": "Gazette S.O. 1512(E)",
        "hazard": "Extremely toxic carbamate; WHO Class Ib.",
        "replacement": "Indoxacarb 14.5% SC"
    }
}

# Statutory Toxicity Triangle Categories under Indian Insecticides Rules 1971 (Rule 19)
TOXICITY_DIAMONDS: Dict[str, Dict[str, str]] = {
    "bright red": {
        "classification": "Extremely Toxic (Category I)",
        "signal_word": "POISON (विष / நஞ்சு)",
        "symbol": "Skull and Crossbones",
        "oral_ld50": "1 to 50 mg/kg body weight",
        "color_code": "#D32F2F",
        "required_warning": "KEEP OUT OF REACH OF CHILDREN. ANECDOTE MUST BE STATED."
    },
    "bright yellow": {
        "classification": "Highly Toxic (Category II)",
        "signal_word": "POISON (विष / நஞ்சு)",
        "symbol": "Skull and Crossbones (or Warning Triangle)",
        "oral_ld50": "51 to 500 mg/kg body weight",
        "color_code": "#FBC02D",
        "required_warning": "DANGEROUS TO BE HANDLED WITHOUT PROTECTIVE GEAR."
    },
    "bright blue": {
        "classification": "Moderately Toxic (Category III)",
        "signal_word": "DANGER (खतरा / ஆபத்து)",
        "symbol": "Caution Triangle",
        "oral_ld50": "501 to 5000 mg/kg body weight",
        "color_code": "#1976D2",
        "required_warning": "HARMFUL IF SWALLOWED OR INHALED."
    },
    "bright green": {
        "classification": "Slightly Toxic (Category IV)",
        "signal_word": "CAUTION (सावधानी / எச்சரிக்கை)",
        "symbol": "Caution Notice",
        "oral_ld50": "> 5000 mg/kg body weight",
        "color_code": "#388E3C",
        "required_warning": "WEAR GLOVES AND WASH THOROUGHLY AFTER APPLICATION."
    }
}

# Verified Indian Authorized Agro-Chemical Manufacturers (CIB&RC Registered)
AUTHORIZED_MANUFACTURERS: List[Dict[str, str]] = [
    {"name": "Bayer CropScience Limited", "code": "BAY", "state": "Maharashtra / Gujarat", "prefix": "CIR-BAY"},
    {"name": "UPL Limited (United Phosphorus)", "code": "UPL", "state": "Gujarat", "prefix": "CIR-UPL"},
    {"name": "Rallis India Limited (A Tata Enterprise)", "code": "RAL", "state": "Maharashtra", "prefix": "CIR-RAL"},
    {"name": "PI Industries Ltd", "code": "PII", "state": "Rajasthan / Gujarat", "prefix": "CIR-PI"},
    {"name": "Coromandel International Limited", "code": "CIL", "state": "Andhra Pradesh / Telangana / Tamil Nadu", "prefix": "CIR-COR"},
    {"name": "Dhanuka Agritech Limited", "code": "DAN", "state": "Haryana / Gujarat", "prefix": "CIR-DHN"},
    {"name": "Syngenta India Limited", "code": "SYN", "state": "Maharashtra / Goa", "prefix": "CIR-SYN"},
    {"name": "Godrej Agrovet Limited", "code": "GAV", "state": "Maharashtra", "prefix": "CIR-GAV"},
    {"name": "FMC India Private Limited", "code": "FMC", "state": "Gujarat / Telangana", "prefix": "CIR-FMC"},
    {"name": "Indofil Industries Limited", "code": "IND", "state": "Maharashtra / Gujarat", "prefix": "CIR-IND"}
]

# Statutory Label Requirements under Insecticides Rules 1971
STATUTORY_LABEL_REQUIREMENTS: List[str] = [
    "CIB&RC Registration Number (CIR-XXXXX/YYYY/...)",
    "Manufacturing License Number (Mfg. Lic. No.)",
    "Toxicity Diamond (Red/Yellow/Blue/Green lower triangle)",
    "Antidote statement in bold",
    "Batch Number, Date of Manufacture, Expiry Date (Inkjet Dot-Matrix)",
    "Maximum Retail Price (inclusive of all taxes)",
    "Net Contents (ml / gm / kg)",
    "Composition (Active ingredient % w/w, Adjuvants, Solvents)",
    "Leaflet inside packet with instructions in English, Hindi, and Regional Language"
]

# Common Hybrid Seed Verification Standards (Seeds Act 1966)
SEED_STANDARDS: Dict[str, Dict[str, str]] = {
    "hybrid_cotton_bt": {
        "crop": "Cotton (Gossypium hirsutum) BG-II",
        "germination_min_pct": "75%",
        "genetic_purity_min_pct": "90%",
        "inert_matter_max_pct": "2.0%",
        "mandatory_coating": "Fungicide (Thiram 75% WP @ 2.5g/kg or Captan) - Distinct Pink/Magenta coat",
        "counterfeit_flags": "Non-uniform food color dye, visible lint fuzz on seeds, uncracked non-viable seeds > 15%"
    },
    "hybrid_paddy_rice": {
        "crop": "Hybrid Rice (Oryza sativa)",
        "germination_min_pct": "80%",
        "genetic_purity_min_pct": "95%",
        "inert_matter_max_pct": "2.0%",
        "mandatory_coating": "Carbendazim 50% WP or Trichoderma (distinct blue or green treatment)",
        "counterfeit_flags": "Mixed grain sizes, unfilled husk chaff > 10%, absence of chemical seed treatment smell"
    },
    "hybrid_maize_corn": {
        "crop": "Hybrid Maize (Zea mays)",
        "germination_min_pct": "90%",
        "genetic_purity_min_pct": "95%",
        "inert_matter_max_pct": "1.0%",
        "mandatory_coating": "Metalaxyl 35% WS + Thiram (Intense Orange/Red coat)",
        "counterfeit_flags": "Damaged embryo tips (weevil holes), flaking color coat that stains fingers like chalk"
    }
}


def check_banned_chemical(chemical_name: str) -> Optional[Dict[str, str]]:
    """
    Check if a chemical or active ingredient is banned in India.
    """
    clean_name = chemical_name.strip().lower()
    for banned, details in BANNED_PESTICIDES_INDIA.items():
        if banned in clean_name or clean_name in banned:
            return {"chemical": banned, **details}
    return None


def validate_cibrc_format(registration_code: str) -> Tuple[bool, str]:
    """
    Validate the CIB&RC registration code structure under Central Insecticides Board norms.
    Standard Format: CIR-[0-9]{4,6}/[1-2][0-9]{3}/[A-Za-z0-9_-]+
    """
    if not registration_code:
        return False, "CIB&RC registration code is missing from label."

    clean_code = registration_code.strip().upper()
    # Match standard patterns like CIR-12345/2018/Chemical-999 or CIR-10294/2015(312)
    pattern = r"CIR-?\s*([0-9]{4,6})\s*/\s*([1-2][0-9]{3})"
    match = re.search(pattern, clean_code)
    if match:
        reg_num = match.group(1)
        year = int(match.group(2))
        if 1970 <= year <= 2026:
            return True, f"Valid CIB&RC structure: Reg No. {reg_num}, Year {year}."
        else:
            return False, f"Invalid registration year {year} in CIB&RC code."

    # Secondary check for legacy formats
    if clean_code.startswith("CIR-") or clean_code.startswith("RC-"):
        return True, "Potential legacy CIB&RC registration format; verify against central gazette."

    return False, "Malformed or missing CIB&RC code. Genuine Indian pesticides MUST carry CIR-XXXXX/YYYY."


def evaluate_toxicity_diamond(color_detected: str) -> Optional[Dict[str, str]]:
    """
    Match detected diamond color to statutory warning category.
    """
    clean_color = color_detected.strip().lower()
    for color_key, data in TOXICITY_DIAMONDS.items():
        if color_key in clean_color or clean_color in color_key:
            return data
    return None
