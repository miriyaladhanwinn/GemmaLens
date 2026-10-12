"""Unit tests for MandiShield Advanced Features Module."""

import unittest
from advanced_features import (
    get_outbreak_dataframe,
    generate_dao_alert_message,
    calculate_dosage,
    analyze_hologram_diffraction,
    simulate_seedling_growth,
    generate_whatsapp_bot_payload,
    CROP_DATABASE,
    EMERGENCY_ANTIDOTES,
)


class TestAdvancedFeatures(unittest.TestCase):
    def test_outbreak_dataframe_structure(self):
        df = get_outbreak_dataframe()
        self.assertGreaterEqual(len(df), 5)
        self.assertIn("lat", df.columns)
        self.assertIn("lon", df.columns)
        self.assertIn("district", df.columns)
        self.assertIn("chemical_flagged", df.columns)

    def test_dao_alert_generation(self):
        msg = generate_dao_alert_message("Guntur")
        self.assertIn("DISTRICT RED ALERT", msg)
        self.assertIn("Guntur", msg)
        self.assertIn("Section 21/29", msg)

    def test_precision_dosage_calculation(self):
        dosage = calculate_dosage("Paddy (Rice)", acres=3.0, tank_liters=15.0)
        self.assertEqual(dosage["crop"], "Paddy (Rice)")
        self.assertEqual(dosage["acres"], 3.0)
        self.assertGreater(dosage["total_chemical_ml"], 0)
        self.assertGreater(dosage["total_tanks_needed"], 0)
        self.assertGreater(dosage["ml_per_tank"], 0)
        self.assertIn("backpack sprayer", dosage["spraying_advice"])

    def test_emergency_antidote_presence(self):
        self.assertIn("Organophosphates (Chlorpyrifos, Monocrotophos, Malathion, Profenofos)", EMERGENCY_ANTIDOTES)
        op_info = EMERGENCY_ANTIDOTES["Organophosphates (Chlorpyrifos, Monocrotophos, Malathion, Profenofos)"]
        self.assertIn("Atropine", op_info["antidote"])
        self.assertIn("Pralidoxime", op_info["antidote"])

    def test_hologram_counterfeit_detection(self):
        # Low spectral shift indicates flat 2D photocopy
        res = analyze_hologram_diffraction(spectral_shift_variance=0.03, edge_blur_index=0.5)
        self.assertTrue(res["is_counterfeit"])
        self.assertIn("COUNTERFEIT", res["verdict"])

    def test_hologram_genuine_detection(self):
        # High spectral shift indicates multi-layer diffraction grating
        res = analyze_hologram_diffraction(spectral_shift_variance=0.18, edge_blur_index=0.1)
        self.assertFalse(res["is_counterfeit"])
        self.assertIn("GENUINE", res["verdict"])

    def test_seedling_growth_simulation(self):
        # Good seed lot
        sim_good = simulate_seedling_growth(purity_percent=99.2, germination_potential=96.0, coating_type="polymer")
        self.assertGreaterEqual(sim_good["effective_germination_pct"], 90.0)
        self.assertEqual(len(sim_good["timeline"]), 4)

        # Spurious dyed seed lot
        sim_bad = simulate_seedling_growth(purity_percent=88.0, germination_potential=70.0, coating_type="textile dye")
        self.assertLess(sim_bad["effective_germination_pct"], 50.0)
        self.assertIn("CRITICAL", sim_bad["yield_loss_risk"])

    def test_whatsapp_payload_generator(self):
        payload = generate_whatsapp_bot_payload(
            phone_number="+919876543210",
            farmer_name="Murugan",
            product_name="Chlor-Strike 20 EC",
            verdict="REJECTED (Counterfeit)",
            confidence=0.96,
            lang="ta",
        )
        self.assertEqual(payload["recipient"], "+919876543210")
        self.assertIn("Murugan", payload["whatsapp_formatted_text"])
        self.assertEqual(payload["confidence_pct"], 96)
        self.assertEqual(len(payload["interactive_buttons"]), 3)

    def test_hyperspectral_raman_adulteration(self):
        from advanced_features import analyze_hyperspectral_raman
        res = analyze_hyperspectral_raman(
            chemical_name="Chlorpyrifos",
            measured_primary_peak=0.35,  # heavily attenuated
            solvent_aliphatic_peak=0.62, # high kerosene/diesel peak
        )
        self.assertTrue(res["is_adulterated"])
        self.assertIn("ADULTERATED", res["verdict"])
        self.assertIn("Kerosene", res["adulterant_identified"])
        self.assertGreater(len(res["spectral_curve"]), 4)

    def test_hyperspectral_raman_authentic(self):
        from advanced_features import analyze_hyperspectral_raman
        res = analyze_hyperspectral_raman(
            chemical_name="Chlorpyrifos",
            measured_primary_peak=0.92,
            solvent_aliphatic_peak=0.08,
        )
        self.assertFalse(res["is_adulterated"])
        self.assertIn("AUTHENTIC", res["verdict"])
        self.assertGreaterEqual(res["measured_active_purity_pct"], 90.0)

    def test_benchmark_edge_gemma4(self):
        from advanced_features import benchmark_edge_gemma4
        bench = benchmark_edge_gemma4("INT4 (MandiShield Edge Quant)")
        self.assertTrue(bench["offline_ready"])
        self.assertLess(bench["memory_ram_gb"], 2.0)
        self.assertGreater(bench["tokens_per_second"], 20.0)
        self.assertGreater(bench["accuracy_retention_pct"], 98.0)

    def test_generate_statutory_fir_complaint(self):
        from advanced_features import generate_statutory_fir_complaint
        fir = generate_statutory_fir_complaint(
            complainant_name="Murugan R.",
            village_mandi="Sulur Gram Panchayat",
            district_state="Coimbatore, Tamil Nadu",
            accused_shop="Sri Lakshmi Fertilizers",
            seized_chemical_lot="LOT-COIMB-9912",
            statutory_violations="Banned Monocrotophos detected under Gazette Notification.",
        )
        self.assertIn("FIRST INFORMATION REPORT", fir)
        self.assertIn("Section 318(4)", fir)
        self.assertIn("Section 29", fir)
        self.assertIn("Sulur Gram Panchayat", fir)
        self.assertIn("Coimbatore, Tamil Nadu", fir)

    def test_simulate_soil_ecotoxicity(self):
        from advanced_features import simulate_soil_ecotoxicity
        eco = simulate_soil_ecotoxicity("Monocrotophos", dosage_multiplier=1.5)
        self.assertIn("CRITICAL", eco["groundwater_leaching_hazard"])
        self.assertIn("EXTREME HAZARD", eco["honeybee_pollinator_risk"])
        self.assertGreater(eco["soil_rhizobium_inhibition_pct"], 50.0)


if __name__ == "__main__":
    unittest.main()

