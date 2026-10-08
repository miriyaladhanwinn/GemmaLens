"""
MandiShield Comprehensive Unit & Integration Test Suite
Verifies:
1. Indian CIB&RC registration code validation & edge case handling
2. Banned chemical detection against the Gazette of India
3. Counterfeit Adulterant detection (Water, Chalk, Kerosene, Textile Dye)
4. Chemical Dossier lookups (Sector, Human Danger, Target Crops, Antidote)
5. Statutory Toxicity Triangle (Rule 19) classification & color extraction
6. Seed purity & physical germination thresholds (Seeds Act 1966)
7. Agent Skills Open Standard packaging
"""

import unittest
import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agri_db import (
    lookup_chemical_dossier,
    check_banned_chemical,
    validate_cibrc_format,
    evaluate_toxicity_diamond,
    BANNED_PESTICIDES_INDIA,
    APPROVED_CIBRC_CHEMICALS,
    KNOWN_ADULTERANTS,
    TOXICITY_DIAMONDS,
    SEED_STANDARDS,
    AUTHORIZED_MANUFACTURERS
)
from agent_skills import AgentSkillPackage
from prompts import PESTICIDE_LABEL_AUDIT_PROMPT, SEED_MORPHOLOGY_AUDIT_PROMPT, REGIONAL_FARMER_ADVISORY_PROMPT


class TestMandiShieldBannedChemicals(unittest.TestCase):
    def test_all_banned_chemicals_detected(self):
        """Every chemical in the statutory banned list must be detected correctly."""
        for chem_name in BANNED_PESTICIDES_INDIA.keys():
            result = check_banned_chemical(chem_name)
            self.assertIsNotNone(result, f"Failed to detect banned chemical: {chem_name}")
            self.assertIn("status", result)
            self.assertIn("order", result)
            self.assertIn("replacement", result)

    def test_case_insensitivity_and_partial_matches(self):
        """Must detect chemical despite mixed case or trade formulation suffix."""
        res1 = check_banned_chemical("eNdOsUlFaN 35% EC")
        self.assertIsNotNone(res1)
        self.assertEqual(res1["status"], "COMPLETELY BANNED")

        res2 = check_banned_chemical("Commercial Monocrotophos 36% SL Formulation")
        self.assertIsNotNone(res2)
        self.assertIn("BANNED", res2["status"])

        res3 = check_banned_chemical("Paraquat Dichloride 24% SL (Gramoxone)")
        self.assertIsNotNone(res3)
        self.assertIn("RESTRICTED", res3["status"])

    def test_benign_chemicals_not_flagged(self):
        """Non-banned registered chemicals must not be falsely flagged as banned."""
        safe_list = [
            "Imidacloprid 17.8% SL",
            "Chlorantraniliprole 18.5% SC",
            "Azadirachtin 10000 PPM (Neem)",
            "Emamectin Benzoate 5% SG"
        ]
        for chem in safe_list:
            self.assertIsNone(check_banned_chemical(chem), f"False positive for safe chemical: {chem}")


class TestMandiShieldChemicalDossierAndAdulterants(unittest.TestCase):
    def test_water_flagged_as_counterfeit_adulterant(self):
        """'Water' must be caught as a counterfeit adulterant and NEVER as an approved pesticide."""
        dossier = lookup_chemical_dossier("water")
        self.assertEqual(dossier["category"], "ADULTERANT")
        self.assertEqual(dossier["verdict"], "FRAUD_SUSPECT")
        self.assertIn("Adulterant", dossier["type"])
        self.assertIn("crop destruction", dossier["human_danger"].lower())

        # Also test variations like 'tap water'
        dossier_tap = lookup_chemical_dossier("tap water")
        self.assertEqual(dossier_tap["category"], "ADULTERANT")

    def test_other_adulterants_detected(self):
        """Kerosene, chalk, and textile dyes must be detected as diluents/counterfeits."""
        for adult in ["kerosene", "chalk", "diesel", "textile dye"]:
            dossier = lookup_chemical_dossier(adult)
            self.assertEqual(dossier["category"], "ADULTERANT", f"Failed for {adult}")

    def test_approved_chemical_dossier_integrity(self):
        """Approved chemicals must return sector, approved crops, target pests, and human danger."""
        test_chems = ["imidacloprid", "chlorantraniliprole", "glyphosate", "mancozeb", "azadirachtin"]
        for c in test_chems:
            dossier = lookup_chemical_dossier(c)
            self.assertEqual(dossier["category"], "APPROVED", f"Failed for {c}")
            self.assertIn("sector", dossier)
            self.assertIn("approved_crops", dossier)
            self.assertIn("target_pests", dossier)
            self.assertIn("human_danger", dossier)
            self.assertIn("antidote", dossier)

    def test_human_danger_level_reported(self):
        """Pesticides must accurately report human hazard."""
        d_coragen = lookup_chemical_dossier("chlorantraniliprole")
        self.assertIn("SAFE FOR OPERATORS", d_coragen["human_danger"])

        d_endo = lookup_chemical_dossier("endosulfan")
        self.assertIn("CRITICAL / LETHAL", d_endo["human_danger"])

    def test_unregistered_unknown_input(self):
        """Completely random or unregistered strings must return UNKNOWN warning."""
        d_unknown = lookup_chemical_dossier("xyz123fakechemical")
        self.assertEqual(d_unknown["category"], "UNKNOWN")
        self.assertIn("NOT listed", d_unknown["message"])


class TestMandiShieldCIBRCValidation(unittest.TestCase):
    def test_valid_cibrc_formats(self):
        """Valid CIB&RC codes spanning multiple years and formats must pass."""
        valid_cases = [
            "CIR-14820/2014/Imidacloprid(SL)-512",
            "CIR-9821/2021/Chlorantraniliprole-101",
            "CIR-1200/1975/CopperOxychloride-22",
            "CIR-55201/2026/BioPesticide-88"
        ]
        for code in valid_cases:
            valid, msg = validate_cibrc_format(code)
            self.assertTrue(valid, f"Expected valid for {code}, got: {msg}")

    def test_invalid_cibrc_years(self):
        """Years prior to 1970 or future years past 2026 must be rejected."""
        valid, msg = validate_cibrc_format("CIR-0014/1965/INVALID")
        self.assertFalse(valid)
        self.assertIn("Invalid registration year", msg)

        valid2, msg2 = validate_cibrc_format("CIR-99999/2045/FAKE")
        self.assertFalse(valid2)
        self.assertIn("Invalid registration year", msg2)

    def test_malformed_cibrc_codes(self):
        """Malformed or blank codes must be rejected."""
        invalid_cases = ["", "   ", "NOT_A_CODE", "12345678", "LIC-99812-ONLY"]
        for code in invalid_cases:
            valid, msg = validate_cibrc_format(code)
            self.assertFalse(valid, f"Expected failure for '{code}'")


class TestMandiShieldToxicityDiamonds(unittest.TestCase):
    def test_statutory_color_lookup(self):
        """Test Rule 19 toxicity category mappings."""
        colors = {
            "bright red": ("Category I", "POISON"),
            "bright yellow": ("Category II", "POISON"),
            "bright blue": ("Category III", "DANGER"),
            "bright green": ("Category IV", "CAUTION")
        }
        for color, (cat, word) in colors.items():
            result = evaluate_toxicity_diamond(color)
            self.assertIsNotNone(result, f"Color not found: {color}")
            self.assertIn(cat, result["classification"])
            self.assertIn(word, result["signal_word"])

    def test_color_variation_matching(self):
        """Match subtle color descriptions."""
        self.assertIsNotNone(evaluate_toxicity_diamond("bright red diamond with skull"))
        self.assertIsNotNone(evaluate_toxicity_diamond("bright yellow toxicity triangle"))
        self.assertIsNotNone(evaluate_toxicity_diamond("bright green caution"))


class TestMandiShieldSeedStandards(unittest.TestCase):
    def test_seed_standards_validity(self):
        """Validate all crop seed standards comply with Seeds Act 1966."""
        crops = ["hybrid_cotton_bt", "hybrid_paddy_rice", "hybrid_maize_corn"]
        for crop in crops:
            self.assertIn(crop, SEED_STANDARDS)
            std = SEED_STANDARDS[crop]
            self.assertIn("germination_min_pct", std)
            self.assertIn("mandatory_coating", std)
            self.assertIn("counterfeit_flags", std)


class TestMandiShieldAgentPackaging(unittest.TestCase):
    def test_agent_skills_yaml_header(self):
        """Agent Skills output must contain valid YAML frontmatter conforming to specification."""
        md = AgentSkillPackage.create_skill_markdown(
            skill_name="mandishield-auditor",
            description="Forensic agro-chemical & seed inspector",
            instructions="Execution steps for autonomous verification."
        )
        self.assertTrue(md.startswith("---"))
        self.assertIn("https://agentskills.io/specification", md)
        self.assertIn("Apache-2.0", md)


if __name__ == "__main__":
    unittest.main()
