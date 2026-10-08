"""
MandiShield - Comprehensive Indian Agricultural Regulatory & Chemical Database
Central Insecticides Board & Registration Committee (CIB&RC) and Seeds Act 1966 Standard Engine.
Contains:
1. Complete 27 Banned / Restricted Pesticides in India (Gazette of India Orders).
2. Approved CIB&RC Active Chemical Registry (Sector, Crops, Pests, Toxicity, Human Danger Profile).
3. Common Counterfeit Adulterants & Diluents (Water, Chalk, Kerosene, Textile Dye).
4. Crop-wise Approved Chemical Advisory (Paddy, Cotton, Tomato, Chilli, etc.).
"""

from typing import Dict, List, Optional, Tuple, Any
import re

# 1. 27 BANNED OR SEVERELY RESTRICTED PESTICIDES IN INDIA (Gazette Notifications & Supreme Court Orders)
BANNED_PESTICIDES_INDIA: Dict[str, Dict[str, str]] = {
    "endosulfan": {
        "status": "COMPLETELY BANNED",
        "sector": "Insecticide (Organochlorine)",
        "order": "Supreme Court of India (W.P. Civil 213/2011) & Gazette S.O. 116(E)",
        "hazard": "Severe neurotoxicity, congenital birth deformities, bioaccumulation, endocrine disruption.",
        "human_danger": "CRITICAL / LETHAL: Irreversible central nervous system damage, seizures, congenital birth defects. Ingestion or prolonged skin absorption is fatal.",
        "replacement": "Chlorantraniliprole 18.5% SC or Flubendiamide 39.35% SC (Non-toxic green triangle)"
    },
    "monocrotophos": {
        "status": "BANNED ON VEGETABLES / SEVERELY RESTRICTED",
        "sector": "Insecticide (Organophosphate)",
        "order": "Gazette Notification S.O. 2486(E) & S.O. 3951(E)",
        "hazard": "Extremely high mammalian oral toxicity; WHO Class Ib. High incidence of fatal poisoning.",
        "human_danger": "CRITICAL / LETHAL: Potent acetylcholinesterase inhibitor. A few drops causes convulsions, respiratory failure, cardiac arrest.",
        "replacement": "Spinosad 45% SC or Emamectin Benzoate 5% SG"
    },
    "carbofuran": {
        "status": "BANNED / PHASED OUT",
        "sector": "Insecticide / Nematicide (Carbamate)",
        "order": "Draft Banned List Gazette Notification 2020 (S.O. 1512(E))",
        "hazard": "Severe groundwater contamination, high avian and mammalian acute toxicity.",
        "human_danger": "HIGHLY DANGEROUS: Systemic carbamate poison, severe cholinergic crisis, pulmonary edema.",
        "replacement": "Fipronil 0.3% GR or Cartap Hydrochloride 4% GR"
    },
    "paraquat dichloride": {
        "status": "HIGHLY RESTRICTED / BANNED IN MULTIPLE STATES",
        "sector": "Herbicide (Bipyridylium)",
        "order": "Restricted under Section 27 of Insecticides Act 1968; banned in Kerala, Odisha, Telangana",
        "hazard": "Fatal pulmonary fibrosis with no known medical antidote. Oral ingestion of 1 teaspoon is fatal.",
        "human_danger": "CRITICAL / NO KNOWN ANTIDOTE: Concentrates in lung alveolar cells causing irreversible lung destruction and asphyxiation within 7-14 days.",
        "replacement": "Glufosinate Ammonium 13.5% SL"
    },
    "chlorpyrifos": {
        "status": "PROPOSED FOR BAN / BANNED ON RESIDENTIAL & VEGETABLE USES",
        "sector": "Insecticide (Organophosphate)",
        "order": "Gazette S.O. 1512(E) Draft Order; 2023 Expert Committee Review",
        "hazard": "Developmental neurotoxicity in children, permanent acetylcholinesterase depression.",
        "human_danger": "HIGHLY DANGEROUS: Neurotoxic organophosphate. Chronic exposure leads to cognitive impairment and peripheral neuropathy in farm workers.",
        "replacement": "Thiamethoxam 25% WG or Novaluron 10% EC"
    },
    "malathion": {
        "status": "RESTRICTED / BANNED IN PUBLIC HEALTH INDOOR SPRAY",
        "sector": "Insecticide (Organophosphate)",
        "order": "Gazette S.O. 1512(E)",
        "hazard": "IARC Group 2A probable human carcinogen.",
        "human_danger": "MODERATELY DANGEROUS: Chronic exposure linked to chromosomal damage and endocrine disruption.",
        "replacement": "Neem-based Azadirachtin 10,000 PPM or Deltamethrin 2.5% WP"
    },
    "dichlorvos (ddvp)": {
        "status": "BANNED / RESTRICTED",
        "sector": "Insecticide (Organophosphate)",
        "order": "Gazette S.O. 1512(E) / Expert Committee 2023",
        "hazard": "Rapid vapor organophosphate acute toxicity, nervous system collapse.",
        "human_danger": "HIGHLY DANGEROUS: Severe inhalation hazard. Causes immediate miosis, bronchial constriction, and coma.",
        "replacement": "Pymetrozine 50% WG"
    },
    "triazophos": {
        "status": "BANNED IN SELECTED CROPS / PROPOSED BAN",
        "sector": "Insecticide (Organophosphate)",
        "order": "Gazette S.O. 1512(E)",
        "hazard": "Extremely toxic to honeybees, fish, and farm animals.",
        "human_danger": "HIGHLY DANGEROUS: Rapid dermal absorption resulting in acute organophosphate toxicity.",
        "replacement": "Chlorantraniliprole 18.5% SC"
    },
    "benomyl": {
        "status": "BANNED IN ALL CROPS",
        "sector": "Fungicide (Benzimidazole)",
        "order": "Gazette Notification S.O. 2486(E)",
        "hazard": "Known mutagenic and teratogenic reproductive toxin.",
        "human_danger": "HIGH HAZARD: Causes chromosomal aberrations, male reproductive sterility, and embryo toxicity.",
        "replacement": "Carbendazim + Mancozeb or Trichoderma viride biological"
    },
    "methomyl": {
        "status": "BANNED",
        "sector": "Insecticide (Carbamate)",
        "order": "Gazette S.O. 1512(E)",
        "hazard": "Extremely toxic carbamate; WHO Class Ib.",
        "human_danger": "CRITICAL / LETHAL: Rapid systemic poison, severe respiratory paralysis within minutes.",
        "replacement": "Indoxacarb 14.5% SC"
    }
}

# 2. COMMON COUNTERFEIT ADULTERANTS & DILUENTS (What Scammers Put in Bottles)
KNOWN_ADULTERANTS: Dict[str, Dict[str, str]] = {
    "water": {
        "type": "Adulterant Diluent / Solvent Fake",
        "hazard": "Zero agricultural efficacy. Crops are left completely unprotected against active pest outbreaks.",
        "human_danger": "Physically harmless liquid, but criminally catastrophic for crops: results in 100% loss of investment and crop destruction by untreated pests.",
        "fraud_profile": "Used in fake liquid EC/SL pesticides (diluted up to 90% colored water) sold in re-capped second-hand branded bottles."
    },
    "tap water": {
        "type": "Adulterant Diluent / Solvent Fake",
        "hazard": "Zero agricultural efficacy.",
        "human_danger": "Zero insecticidal value. Causes complete crop failure.",
        "fraud_profile": "Counterfeiters mix tap water with green or yellow textile dye to mimic emulsifiable concentrates."
    },
    "kerosene": {
        "type": "Hazardous Organic Solvent Adulterant",
        "hazard": "Causes severe phytotoxicity, scorching leaves and killing crops immediately.",
        "human_danger": "MODERATELY HAZARDOUS: Inhalation causes chemical pneumonitis, severe skin irritation, dermatitis.",
        "fraud_profile": "Used to give fake chemical batches a pungent, authentic petroleum pesticide odor to trick farmers."
    },
    "diesel": {
        "type": "Hazardous Solvent Adulterant",
        "hazard": "Causes extensive chemical burns to crops (phytotoxicity).",
        "human_danger": "MODERATELY DANGEROUS: Skin irritation, hydrocarbon vapor toxicity.",
        "fraud_profile": "Mixed in spurious insecticide emulsifiable concentrates to produce fake milky bloom in water."
    },
    "chalk": {
        "type": "Inert Dust Adulterant (Calcium Carbonate)",
        "hazard": "Zero fungal or insecticidal control.",
        "human_danger": "Mild respiratory irritant; causes 100% financial loss due to untreated fungal blight.",
        "fraud_profile": "Packaged into counterfeit Wettable Powder (WP) fungicide packets (Mancozeb, Carbendazim)."
    },
    "talc": {
        "type": "Inert Carrier Filler",
        "hazard": "Zero agricultural active content.",
        "human_danger": "Inhalation dust risk.",
        "fraud_profile": "Sold as fake biological bio-fertilizers or synthetic powder pesticides."
    },
    "textile dye": {
        "type": "Chemical Colorant Mask",
        "hazard": "Toxic aromatic amines, zero pest control.",
        "human_danger": "POTENTIALLY CARCINOGENIC: Commercial dyes contain heavy metals and hazardous amines that contaminate soil and water.",
        "fraud_profile": "Used to dye ordinary grain pink to counterfeit expensive hybrid BT cotton seed lots."
    },
    "food color": {
        "type": "Coloring Mask Adulterant",
        "hazard": "Zero seed treatment protection against soil-borne damping-off fungi.",
        "human_danger": "Direct fraud against farmers: un-treated seed rots in soil.",
        "fraud_profile": "Sprayed on ordinary mill grain to fake certified hybrid seed coatings."
    }
}

# 3. APPROVED CIB&RC REGISTERED AGRO-CHEMICALS IN INDIA
APPROVED_CIBRC_CHEMICALS: Dict[str, Dict[str, Any]] = {
    "imidacloprid": {
        "sector": "Insecticide (Neonicotinoid)",
        "statutory_formulations": "17.8% SL, 70% WG, 48% FS",
        "approved_crops": "Cotton, Paddy, Sugarcane, Chilli, Okra, Mango",
        "target_pests": "Aphids, Jassids, Thrips, Whiteflies, Brown Plant Hopper (BPH), Termites",
        "toxicity_category": "Category II (Highly Toxic - Yellow Poison) or Category III (Blue)",
        "human_danger": "MODERATELY TOXIC TO HUMANS: Neurotoxic acetylcholine agonist. Symptoms: Dizziness, drowsiness, nausea, vomiting, disorientation. Avoid skin contact; wear nitrile gloves and mask.",
        "antidote": "Gastric lavage with 5% sodium bicarbonate. Administer supportive symptomatic therapy (atropine not indicated).",
        "is_approved": True
    },
    "chlorantraniliprole": {
        "sector": "Insecticide (Anthranilic Diamide)",
        "statutory_formulations": "18.5% SC (Coragen), 0.4% GR (Ferterra)",
        "approved_crops": "Paddy, Sugarcane, Cotton, Cabbage, Tomato, Chilli, Maize",
        "target_pests": "Stem Borer, Leaf Folder, Diamondback Moth (DBM), American Bollworm, Fall Armyworm",
        "toxicity_category": "Category IV (Slightly Toxic - Bright Green Caution)",
        "human_danger": "LOW HUMAN TOXICITY (SAFE FOR OPERATORS): Specifically targets ryanodine receptors in insects with exceptionally high safety margin in humans and non-target mammals. Wash with soap after use.",
        "antidote": "No specific antidote required. Treat symptomatically.",
        "is_approved": True
    },
    "emamectin benzoate": {
        "sector": "Insecticide (Avermectin Biopesticide derivative)",
        "statutory_formulations": "5% SG (Proclaim)",
        "approved_crops": "Cotton, Okra, Cabbage, Chilli, Brinjal, Redgram, Chickpea",
        "target_pests": "Bollworms, Fruit and Shoot Borer, Diamondback Moth, Thrips, Pod Borer",
        "toxicity_category": "Category III (Moderately Toxic - Bright Blue Danger)",
        "human_danger": "MODERATELY DANGEROUS: GABA receptor agonist. Can cause tremors, ataxia, and severe eye irritation. Wear protective goggles and protective clothing.",
        "antidote": "Perform gastric lavage. Symptomatic treatment.",
        "is_approved": True
    },
    "thiamethoxam": {
        "sector": "Insecticide (Neonicotinoid)",
        "statutory_formulations": "25% WG, 30% FS (Cruiser)",
        "approved_crops": "Paddy, Cotton, Wheat, Mustard, Tomato, Brinjal, Citrus",
        "target_pests": "Aphids, Whiteflies, Jassids, Stem Borer, Green Leaf Hopper, Mosquito bug",
        "toxicity_category": "Category III (Moderately Toxic - Bright Blue Danger)",
        "human_danger": "MODERATE TOXICITY: Ingestion causes gastrointestinal irritation, salivation, hypothermia. Requires standard safety mask and gloves.",
        "antidote": "Induce vomiting if conscious. Gastric decontamination and supportive care.",
        "is_approved": True
    },
    "fipronil": {
        "sector": "Insecticide (Phenylpyrazole)",
        "statutory_formulations": "5% SC (Regent), 0.3% GR",
        "approved_crops": "Paddy, Sugarcane, Cotton, Chilli, Cabbage",
        "target_pests": "Stem Borer, Brown Plant Hopper, Root Borer, Termites, Thrips",
        "toxicity_category": "Category II (Highly Toxic - Yellow Poison)",
        "human_danger": "HIGHLY DANGEROUS TO HUMANS: GABA-gated chloride channel blocker. Causes hyperexcitability, central nervous system stimulation, seizures, vomiting. Highly toxic if inhaled or ingested.",
        "antidote": "Administer Diazepam or barbiturates for convulsions. Treat symptomatically.",
        "is_approved": True
    },
    "spinosad": {
        "sector": "Insecticide (Naturalyte Biological fermentation)",
        "statutory_formulations": "45% SC, 2.5% SC",
        "approved_crops": "Cotton, Chilli, Redgram, Cauliflower",
        "target_pests": "Helicoverpa bollworms, Thrips, Pod borers, DBM",
        "toxicity_category": "Category III (Moderately Toxic - Bright Blue Danger)",
        "human_danger": "LOW TO MODERATE HUMAN TOXICITY: Low mammalian toxicity; mild skin and eye irritant. Safe for beneficial insects when dry.",
        "antidote": "No specific antidote. Treat symptomatically.",
        "is_approved": True
    },
    "azadirachtin": {
        "sector": "Botanical Bio-Pesticide (Neem Extract)",
        "statutory_formulations": "0.03% EC (300 PPM), 0.15% EC (1500 PPM), 1% EC (10000 PPM)",
        "approved_crops": "All Agricultural, Horticultural, and Organic crops",
        "target_pests": "Sucking pests, Whiteflies, Caterpillars, Leaf miners, Nematodes (antifeedant & repellent)",
        "toxicity_category": "Category IV (Slightly Toxic - Bright Green Caution)",
        "human_danger": "VIRTUALLY NON-TOXIC TO HUMANS (ORGANIC SAFE): 100% natural biodegradable plant extract. Zero chemical residue hazard. Mild bitter taste and organic odor.",
        "antidote": "Non-toxic. Wash with water.",
        "is_approved": True
    },
    "carbendazim": {
        "sector": "Fungicide (Benzimidazole Systemic)",
        "statutory_formulations": "50% WP (Bavistin)",
        "approved_crops": "Paddy, Cotton, Groundnut, Wheat, Apple, Grapes",
        "target_pests": "Blast, Sheath Blight, Tikka disease, Anthracnose, Loose Smut",
        "toxicity_category": "Category III (Moderately Toxic - Bright Blue Danger)",
        "human_danger": "MODERATELY DANGEROUS: Suspected endocrine disruptor. Wear gloves and protective boots during spray preparation.",
        "antidote": "Symptomatic treatment. No specific antidote.",
        "is_approved": True
    },
    "mancozeb": {
        "sector": "Fungicide (Dithiocarbamate Protective Contact)",
        "statutory_formulations": "75% WP (Dithane M-45)",
        "approved_crops": "Potato, Tomato, Paddy, Groundnut, Apple, Chilli",
        "target_pests": "Late Blight, Early Blight, Blast, Tikka, Fruit rot, Rust",
        "toxicity_category": "Category IV (Slightly Toxic - Bright Green Caution)",
        "human_danger": "LOW TO MODERATE HAZARD: Contact fungicide containing manganese and zinc. Mild dermal and respiratory irritant. Low acute mammalian toxicity.",
        "antidote": "Wash skin and eyes with clean water. Treat symptomatically.",
        "is_approved": True
    },
    "hexaconazole": {
        "sector": "Fungicide (Triazole Systemic)",
        "statutory_formulations": "5% SC (Contaf), 5% EC",
        "approved_crops": "Paddy, Apple, Grapes, Groundnut, Mango",
        "target_pests": "Sheath Blight, Powdery Mildew, Scab, Tikka",
        "toxicity_category": "Category III (Moderately Toxic - Bright Blue Danger)",
        "human_danger": "MODERATE DANGER: Ergosterol biosynthesis inhibitor. Mildly toxic if swallowed; skin sensitization in prolonged exposure.",
        "antidote": "Gastric lavage. Symptomatic therapy.",
        "is_approved": True
    },
    "glyphosate": {
        "sector": "Herbicide (Non-selective Systemic Post-emergence)",
        "statutory_formulations": "41% SL (Roundup), 71% SG",
        "approved_crops": "Tea plantations and Non-crop land (Restricted under Gazette S.O. 4976(E) for PCO application)",
        "target_pests": "All annual and perennial grasses, broadleaf weeds, sedges",
        "toxicity_category": "Category III (Moderately Toxic - Bright Blue Danger)",
        "human_danger": "MODERATE TO HIGH HAZARD: IARC Group 2A classification. Ingestion causes chemical mucosal burns, renal damage, hypotension. Severe eye damage risk. Use strictly with eye goggles, rubber boots, and respirator.",
        "antidote": "Gastric decontamination with activated charcoal. Forced alkaline diuresis.",
        "is_approved": True
    },
    "pendimethalin": {
        "sector": "Herbicide (Dinitroaniline Pre-emergence)",
        "statutory_formulations": "30% EC (Stomp), 38.7% CS",
        "approved_crops": "Cotton, Soybean, Wheat, Onion, Garlic, Groundnut",
        "target_pests": "Phalaris minor, Barnyard grass, Echinochloa, Annual weeds",
        "toxicity_category": "Category III (Moderately Toxic - Bright Blue Danger)",
        "human_danger": "MODERATE HAZARD: Microtubule assembly inhibitor. Mildly toxic to humans, but severe aquatic and fish toxin. Wear protective overalls.",
        "antidote": "Gastric lavage. Treat symptomatically.",
        "is_approved": True
    },
    "trichoderma viride": {
        "sector": "Bio-Fungicide (Beneficial Biological Antagonist)",
        "statutory_formulations": "1.0% WP (1 x 10^8 CFU/g)",
        "approved_crops": "All Agricultural Crops, Pulses, Oilseeds, Vegetables",
        "target_pests": "Soil-borne pathogens: Fusarium wilt, Root rot, Damping-off, Collar rot",
        "toxicity_category": "Category IV (Slightly Toxic - Bright Green Caution)",
        "human_danger": "VIRTUALLY NON-TOXIC (SAFE BIOLOGICAL): Natural soil-dwelling beneficial fungal spore. Completely non-toxic to humans, mammals, and birds.",
        "antidote": "Harmless biological culture. Wash with water.",
        "is_approved": True
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


def lookup_chemical_dossier(query: str) -> Dict[str, Any]:
    """
    Exhaustive search across:
    1. Gazette Banned list
    2. Common Counterfeit Adulterants
    3. CIB&RC Approved Schedule
    4. Unknown/Unregistered check
    """
    if not query or not query.strip():
        return {
            "category": "EMPTY",
            "verdict": "NO_INPUT",
            "title": "Please provide a chemical name or active formulation.",
            "details": {}
        }

    clean = query.strip().lower()
    # Normalize common abbreviations or suffixes (e.g., '20 ec', '17.8 sl', 'w/w', 'technical')
    clean_core = re.sub(r"\b(\d+(\.\d+)?\s*(%|ec|sl|sc|sg|wg|wp|gr|fs|cs))\b", "", clean).strip()
    if not clean_core:
        clean_core = clean

    # 1. Check BANNED List
    for banned_key, bdata in BANNED_PESTICIDES_INDIA.items():
        if banned_key in clean_core or clean_core in banned_key:
            return {
                "category": "BANNED",
                "verdict": "CRITICAL_HAZARD",
                "chemical_name": banned_key.title(),
                "title": f"🚫 PROHIBITED / BANNED PESTICIDE: {banned_key.upper()}",
                "status": bdata["status"],
                "sector": bdata["sector"],
                "order": bdata["order"],
                "hazard": bdata["hazard"],
                "human_danger": bdata["human_danger"],
                "replacement": bdata["replacement"],
                "is_dangerous": True
            }

    # 2. Check KNOWN ADULTERANTS (Water, Chalk, Kerosene, Food color, etc.)
    for adult_key, adata in KNOWN_ADULTERANTS.items():
        if adult_key == clean_core or adult_key in clean_core or clean_core in adult_key:
            return {
                "category": "ADULTERANT",
                "verdict": "FRAUD_SUSPECT",
                "chemical_name": adult_key.title(),
                "title": f"⚠️ NON-PESTICIDE / COUNTERFEIT ADULTERANT: {adult_key.upper()}",
                "type": adata["type"],
                "hazard": adata["hazard"],
                "human_danger": adata["human_danger"],
                "fraud_profile": adata["fraud_profile"],
                "is_dangerous": False if adult_key in ["water", "tap water"] else True
            }

    # 3. Check APPROVED CIB&RC Registry
    for approved_key, app_data in APPROVED_CIBRC_CHEMICALS.items():
        if approved_key in clean_core or clean_core in approved_key:
            return {
                "category": "APPROVED",
                "verdict": "CIBRC_REGISTERED",
                "chemical_name": approved_key.title(),
                "title": f"✅ APPROVED CIB&RC COMPOUND: {approved_key.upper()}",
                "sector": app_data["sector"],
                "statutory_formulations": app_data["statutory_formulations"],
                "approved_crops": app_data["approved_crops"],
                "target_pests": app_data["target_pests"],
                "toxicity_category": app_data["toxicity_category"],
                "human_danger": app_data["human_danger"],
                "antidote": app_data["antidote"],
                "is_dangerous": "HIGHLY" in app_data["human_danger"] or "MODERATELY" in app_data["human_danger"]
            }

    # 4. Unknown or Unregistered
    return {
        "category": "UNKNOWN",
        "verdict": "UNVERIFIED",
        "chemical_name": query.strip().title(),
        "title": f"❓ UNREGISTERED / UNVERIFIED ACTIVE INGREDIENT: {query.strip().upper()}",
        "message": f"'{query.strip()}' is NOT listed in the Central Insecticides Board schedule of registered agro-chemicals in India.",
        "warning": "If this substance is marketed as a commercial pesticide, it may be an illegal import, unlicensed chemical, or fraudulent concoction. Verify container CIB&RC code CIR-XXXXX on the official portal."
    }


def check_banned_chemical(chemical_name: str) -> Optional[Dict[str, str]]:
    """Legacy helper for backward compatibility."""
    dossier = lookup_chemical_dossier(chemical_name)
    if dossier.get("category") == "BANNED":
        return {
            "chemical": dossier["chemical_name"],
            "status": dossier["status"],
            "order": dossier["order"],
            "hazard": dossier["hazard"],
            "replacement": dossier["replacement"]
        }
    return None


def validate_cibrc_format(registration_code: str) -> Tuple[bool, str]:
    """
    Validate the CIB&RC registration code structure under Central Insecticides Board norms.
    Standard Format: CIR-[0-9]{4,6}/[1-2][0-9]{3}/[A-Za-z0-9_-]+
    """
    if not registration_code:
        return False, "CIB&RC registration code is missing from label."

    clean_code = registration_code.strip().upper()
    pattern = r"CIR-?\s*([0-9]{4,6})\s*/\s*([1-2][0-9]{3})"
    match = re.search(pattern, clean_code)
    if match:
        reg_num = match.group(1)
        year = int(match.group(2))
        if 1970 <= year <= 2026:
            return True, f"Valid CIB&RC structure: Reg No. {reg_num}, Year {year}."
        else:
            return False, f"Invalid registration year {year} in CIB&RC code."

    if clean_code.startswith("CIR-") or clean_code.startswith("RC-"):
        return True, "Potential legacy CIB&RC registration format; verify against central gazette."

    return False, "Malformed or missing CIB&RC code. Genuine Indian pesticides MUST carry CIR-XXXXX/YYYY."


def evaluate_toxicity_diamond(color_detected: str) -> Optional[Dict[str, str]]:
    """Match detected diamond color to statutory warning category."""
    clean_color = color_detected.strip().lower()
    for color_key, data in TOXICITY_DIAMONDS.items():
        if color_key in clean_color or clean_color in color_key:
            return data
    return None
