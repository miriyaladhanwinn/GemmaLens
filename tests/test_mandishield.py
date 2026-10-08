"""
MandiShield Unit Test Suite
Verifies:
1. Indian CIB&RC registration code validation
2. Banned chemical detection (Gazette list)
3. Toxicity triangle statutory color matching
4. Prompt structure and Agent Skills packaging
"""

import unittest
import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agri_db import (
    check_banned_chemical,
    validate_cibrc_format,
    evaluate_toxicity_diamond,
    BANNED_PESTICIDES_INDIA,
    TOXICITY_DIAMONDS
)
from agent_skills import AgentSkillPackage
from prompts import PESTICIDE_LABEL_AUDIT_PROMPT, SEED_MORPHOLOGY_AUDIT_PROMPT

class TestMandiShieldDatabase(unittest.TestCase):
    def test_banned_chemical_detection(self):
        # Endosulfan is banned by Supreme Court of India
        result = check_banned_chemical("Endosulfan 35% EC")
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "COMPLETELY BANNED")

        # Monocrotophos is restricted/banned on vegetables
        result_mono = check_banned_chemical("Monocrotophos 36% SL")
        self.assertIsNotNone(result_mono)
        self.assertIn("BANNED", result_mono["status"])

        # Clean chemical (e.g. Imidacloprid) is not in banned list
        clean_res = check_banned_chemical("Imidacloprid 17.8% SL")
        self.assertIsNone(clean_res)

    def test_cibrc_format_validation(self):
        # Valid format
        valid, msg = validate_cibrc_format("CIR-14820/2014/Imidacloprid(SL)-512")
        self.assertTrue(valid)
        self.assertIn("Valid CIB&RC", msg)

        # Pre-Act year (1965 precedes Insecticides Act 1968)
        invalid_year, msg2 = validate_cibrc_format("CIR-0014/1965/INVALID")
        self.assertFalse(invalid_year)

        # Missing code
        invalid_empty, msg3 = validate_cibrc_format("")
        self.assertFalse(invalid_empty)

    def test_toxicity_diamond_classification(self):
        # Yellow = Highly toxic
        yellow = evaluate_toxicity_diamond("bright yellow")
        self.assertIsNotNone(yellow)
        self.assertIn("Category II", yellow["classification"])
        self.assertIn("POISON", yellow["signal_word"])

        # Red = Extremely toxic
        red = evaluate_toxicity_diamond("bright red")
        self.assertIsNotNone(red)
        self.assertIn("Category I", red["classification"])

    def test_agent_skills_packaging(self):
        skill_text = AgentSkillPackage.create_skill_markdown(
            skill_name="mandishield-auditor",
            description="Forensic agro-chemical and seed inspector",
            instructions="1. Upload label 2. Verify CIBRC 3. Issue verdict",
            author="Team MandiShield"
        )
        self.assertIn("---", skill_text)
        self.assertIn("name: mandishield-auditor", skill_text)
        self.assertIn("https://agentskills.io/specification", skill_text)

    def test_prompt_integrity(self):
        self.assertIn("CIB&RC", PESTICIDE_LABEL_AUDIT_PROMPT)
        self.assertIn("Insecticides Act 1968", PESTICIDE_LABEL_AUDIT_PROMPT)
        self.assertIn("Seeds Act 1966", SEED_MORPHOLOGY_AUDIT_PROMPT)

if __name__ == "__main__":
    unittest.main()
