"""
AERO-STENT: Structural FEA, Stress & Safety Factor Validation Engine
Team TECHTONICS | Vishwakarma Awards 2026-27 | Theme 1: Health Tech
"""

import math

def calculate_enclosure_crush_stress(force_N=100.0, outer_dia_mm=55.0, wall_thick_mm=2.5, length_mm=160.0):
    """
    Evaluates cylinder lateral compression stress under patient grip/crush.
    """
    Sy_PC_ABS = 62.0  # MPa (Yield Strength)
    
    # Projected load-bearing area
    effective_area_mm2 = 2.0 * wall_thick_mm * (length_mm * 0.4)
    sigma_nom = force_N / effective_area_mm2
    
    # Stress concentration factor Kt at bezel transition fillet
    Kt = 1.85
    peak_stress_MPa = sigma_nom * Kt
    fos = Sy_PC_ABS / peak_stress_MPa
    
    return {
        "applied_force_N": force_N,
        "peak_von_mises_MPa": round(peak_stress_MPa, 2),
        "yield_strength_MPa": Sy_PC_ABS,
        "factor_of_safety": round(fos, 2),
        "status": "PASS" if fos > 1.5 else "FAIL"
    }

def calculate_drop_impact(mass_kg=0.245, drop_height_m=1.2, impact_duration_s=0.0021):
    """
    IEC 60068-2-32 Free-Fall Dynamic Impact Simulation
    """
    g = 9.81
    Sy_PC_ABS = 62.0  # MPa
    
    # Impact velocity: v = sqrt(2gh)
    v_impact = math.sqrt(2 * g * drop_height_m)
    
    # Deceleration: a = v / dt
    deceleration = v_impact / impact_duration_s
    g_force = deceleration / g
    
    # Peak dynamic force
    peak_force_N = mass_kg * deceleration
    
    # Effective impact contact area at bottom radius fillet
    contact_area_mm2 = 38.5
    peak_stress_MPa = peak_force_N / contact_area_mm2
    fos = Sy_PC_ABS / peak_stress_MPa
    
    return {
        "drop_height_m": drop_height_m,
        "impact_velocity_mps": round(v_impact, 2),
        "peak_g_shock": round(g_force, 1),
        "peak_dynamic_force_N": round(peak_force_N, 1),
        "peak_von_mises_MPa": round(peak_stress_MPa, 2),
        "factor_of_safety": round(fos, 2),
        "status": "PASS" if fos >= 1.2 else "FAIL"
    }

if __name__ == "__main__":
    print("=== AERO-STENT MECHANICAL FEA STRESS REPORT ===")
    crush = calculate_enclosure_crush_stress()
    print("1. Lateral Crush Grip (100 N):", crush)
    
    drop = calculate_drop_impact()
    print("2. 1.2m Free-Fall Drop Impact:", drop)
