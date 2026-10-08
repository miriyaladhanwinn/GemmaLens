"""
Generate Synthetic High-Resolution Agricultural Test Samples for MandiShield
Includes:
1. counterfeit_pesticide_sample.png (Misspelled molecule, wrong toxicity diamond, invalid CIB&RC code)
2. genuine_pesticide_sample.png (CIB&RC compliant, yellow toxicity diamond, antidote statement)
3. spurious_cotton_seeds.png (Uneven dyed non-hybrid grains with high inert matter)
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_counterfeit_pesticide():
    img = Image.new("RGB", (800, 1000), color=(248, 249, 250))
    draw = ImageDraw.Draw(img)

    # Header border
    draw.rectangle([(20, 20), (780, 980)], outline=(180, 40, 40), width=6)
    
    # Header Banner
    draw.rectangle([(20, 20), (780, 120)], fill=(180, 40, 40))
    draw.text((40, 45), "CHLOR-STRIKE 20 EC (COUNTERFEIT TEST)", fill=(255, 255, 255))

    # Details
    y = 150
    draw.text((40, y), "MANUFACTURER: Kisan Chemical Traders (Unverified)", fill=(30, 30, 30))
    y += 40
    # Misspelled active ingredient ('Chlorpyriphos' instead of 'Chlorpyrifos')
    draw.text((40, y), "ACTIVE INGREDIENT: Chlorpyriphos 20% EC [MISSPELLED]", fill=(200, 0, 0))
    y += 40
    # Invalid CIB&RC code (Year 1965 precedes Insecticides Act 1968)
    draw.text((40, y), "CIB&RC REGISTRATION: CIR-0014/1965/INVALID-CODE", fill=(200, 0, 0))
    y += 40
    draw.text((40, y), "MFG. LIC. NO: LIC-UNKNOWN-9912", fill=(60, 60, 60))
    y += 50

    # Contradictory Toxicity Diamond (Green Caution instead of Yellow/Red Poison!)
    draw.rectangle([(40, y), (760, y + 220)], fill=(230, 245, 230), outline=(50, 150, 50), width=2)
    # Draw Green diamond
    cx, cy = 150, y + 110
    draw.polygon([(cx, cy - 60), (cx + 60, cy), (cx, cy + 60), (cx - 60, cy)], fill=(56, 142, 60))
    draw.text((230, y + 50), "FLAGRANT VIOLATION DETECTED:", fill=(180, 0, 0))
    draw.text((230, y + 90), "Printed as GREEN 'CAUTION' (Oral LD50 > 5000 mg/kg)", fill=(30, 30, 30))
    draw.text((230, y + 130), "Actual Chlorpyrifos requires YELLOW POISON (LD50: 135 mg/kg)", fill=(200, 0, 0))

    y += 260
    # Flat offset batch printing (not dot-matrix inkjet)
    draw.rectangle([(40, y), (760, y + 140)], fill=(240, 240, 240), outline=(100, 100, 100), width=1)
    draw.text((60, y + 20), "BATCH NO: BATCH-8889-OFFSET-PRINT [FLAT INK DETECTED]", fill=(150, 30, 30))
    draw.text((60, y + 60), "MFG DATE: 01/2026   EXP DATE: 12/2030 (5-Year shelf life is illegal)", fill=(150, 30, 30))
    draw.text((60, y + 100), "ANTIDOTE: No antidote provided [RULE 19 VIOLATION]", fill=(200, 0, 0))

    y += 180
    draw.rectangle([(40, y), (760, y + 120)], fill=(255, 230, 230), outline=(200, 50, 50), width=3)
    draw.text((60, y + 25), "SECURITY ASSESSMENT:", fill=(180, 0, 0))
    draw.text((60, y + 60), "STATUS: CONFIRMED COUNTERFEIT / CRITICAL HAZARD (Score: 12/100)", fill=(180, 0, 0))

    target = os.path.join(OUTPUT_DIR, "counterfeit_pesticide_sample.png")
    img.save(target)
    print(f"Generated {target}")

def create_genuine_pesticide():
    img = Image.new("RGB", (800, 1000), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Header border
    draw.rectangle([(20, 20), (780, 980)], outline=(46, 125, 50), width=6)
    
    # Header Banner
    draw.rectangle([(20, 20), (780, 120)], fill=(46, 125, 50))
    draw.text((40, 45), "CONFIDOR 17.8 SL (GENUINE CIB&RC CERTIFIED)", fill=(255, 255, 255))

    y = 150
    draw.text((40, y), "MANUFACTURER: Bayer CropScience Limited (Authorized)", fill=(30, 30, 30))
    y += 40
    draw.text((40, y), "ACTIVE INGREDIENT: Imidacloprid 17.8% SL (w/w)", fill=(30, 30, 30))
    y += 40
    draw.text((40, y), "CIB&RC REGISTRATION: CIR-14820/2014/Imidacloprid(SL)-512", fill=(46, 125, 50))
    y += 40
    draw.text((40, y), "MFG. LIC. NO: G/25/1042 (Ankleshwar, Gujarat)", fill=(60, 60, 60))
    y += 50

    # Genuine Toxicity Diamond (Yellow POISON)
    draw.rectangle([(40, y), (760, y + 220)], fill=(255, 253, 230), outline=(230, 180, 0), width=2)
    cx, cy = 150, y + 110
    draw.polygon([(cx, cy - 60), (cx + 60, cy), (cx, cy + 60), (cx - 60, cy)], fill=(251, 192, 45))
    draw.text((230, y + 35), "STATUTORY TOXICITY CLASSIFICATION:", fill=(30, 30, 30))
    draw.text((230, y + 70), "COLOR: BRIGHT YELLOW | CATEGORY II (HIGHLY TOXIC)", fill=(180, 100, 0))
    draw.text((230, y + 105), "SIGNAL WORD: POISON / विष / நஞ்சு", fill=(180, 0, 0))
    draw.text((230, y + 140), "ANTIDOTE: Gastric lavage with 5% sodium bicarbonate.", fill=(46, 125, 50))

    y += 260
    # Dot-matrix inkjet batch print
    draw.rectangle([(40, y), (760, y + 140)], fill=(245, 245, 245), outline=(150, 150, 150), width=1)
    draw.text((60, y + 20), "B.No.: B40291 (High-Speed Inkjet Dot-Matrix Verified)", fill=(30, 30, 30))
    draw.text((60, y + 60), "MFG: 03/2026   EXP: 02/2028 (24 Month statutory limit)", fill=(30, 30, 30))
    draw.text((60, y + 100), "MRP: Rs. 485.00 (Incl. of all taxes) | Net: 100 ml", fill=(30, 30, 30))

    y += 180
    draw.rectangle([(40, y), (760, y + 120)], fill=(235, 250, 235), outline=(46, 125, 50), width=3)
    draw.text((60, y + 25), "SECURITY ASSESSMENT:", fill=(46, 125, 50))
    draw.text((60, y + 60), "STATUS: VERIFIED GENUINE & STATUTORY COMPLIANT (Score: 98/100)", fill=(46, 125, 50))

    target = os.path.join(OUTPUT_DIR, "genuine_pesticide_sample.png")
    img.save(target)
    print(f"Generated {target}")

def create_spurious_seeds():
    img = Image.new("RGB", (800, 700), color=(250, 245, 240))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(20, 20), (780, 680)], outline=(190, 80, 0), width=5)
    draw.rectangle([(20, 20), (780, 100)], fill=(190, 80, 0))
    draw.text((40, 40), "SPURIOUS HYBRID COTTON SEED LOT (FORENSIC SAMPLE)", fill=(255, 255, 255))

    y = 130
    draw.text((40, y), "DECLARED VARIETY: BG-II Bollgard Hybrid Cotton F1", fill=(30, 30, 30))
    y += 35
    draw.text((40, y), "LAB FORENSIC MACRO-MORPHOLOGY AUDIT:", fill=(180, 0, 0))
    
    y += 45
    # Simulated seed grain defects
    draw.rectangle([(40, y), (760, y + 260)], fill=(255, 255, 255), outline=(180, 180, 180), width=2)
    draw.text((60, y + 20), "• Defect 1: Uneven Dyeing - Pink food color wash stains fingers upon touch.", fill=(200, 0, 0))
    draw.text((60, y + 60), "• Defect 2: Missing Thiram/Captan chemical fungicide signature smell.", fill=(200, 0, 0))
    draw.text((60, y + 100), "• Defect 3: Non-Viable Embryos: 22% grains have visible weevil bore-holes.", fill=(200, 0, 0))
    draw.text((60, y + 140), "• Defect 4: Inert Matter / Chaff: 7.8% (Permissible limit <= 2.0%).", fill=(200, 0, 0))
    draw.text((60, y + 180), "• Defect 5: Seed Size Variance: CV > 28% (indicates mixed reject grain).", fill=(200, 0, 0))
    draw.text((60, y + 220), "GERMINATION TEST: 38% (Statutory Minimum: 75%).", fill=(180, 0, 0))

    y += 290
    draw.rectangle([(40, y), (760, y + 100)], fill=(255, 230, 230), outline=(200, 0, 0), width=2)
    draw.text((60, y + 20), "VERDICT: CRITICAL SPURIOUS BATCH DETECTED (Seeds Act 1966 Sec 7)", fill=(200, 0, 0))
    draw.text((60, y + 55), "Action: Reject lot immediately. Sowing will cause 60%+ germination failure.", fill=(180, 0, 0))

    target = os.path.join(OUTPUT_DIR, "spurious_seeds_sample.png")
    img.save(target)
    print(f"Generated {target}")

if __name__ == "__main__":
    create_counterfeit_pesticide()
    create_genuine_pesticide()
    create_spurious_seeds()
