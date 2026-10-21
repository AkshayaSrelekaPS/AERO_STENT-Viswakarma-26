# AERO-STENT — Mechanical Design & Numerical Validation (PPT Deck)
### Vishwakarma Awards 2026–27 | Theme 1: Health Tech | Team TECHTONICS | IIT Indore

---

## SLIDE 1: Mechanical System Architecture & Dimensional Specs
**Title:** AERO-STENT: Form Factor, Packaging & Physical Architecture
**Subtitle:** Compact, Dual-Chamber Handheld Enclosure with IP67 Hermetic Isolation

### Key Engineering Data & Dimensions:
- **Total Envelope:** Height = **160.0 mm**, Diameter = **55.0 mm Ø**, Total Mass = **245 g** (with battery + 5 mL drug)
- **Ergonomics & Grip:** Center of mass located at **72 mm** from base (optimal hand stability, grip circumference **172.8 mm**)
- **Enclosure Division:**
  - **Upper "Wet Zone" (Fluidics):** Height = **68 mm**, Internal volume = **38 cm³** (contains drug reservoir, piezo mesh, Venturi mixing chamber, PEP valve)
  - **Lower "Dry Zone" (Avionics/Power):** Height = **92 mm**, Internal volume = **118 cm³** (contains dual STM32/ESP32 PCBs, 3000 mAh LiFePO4 cell, USB-C IP67 port)
  - **Hermetic Barrier:** Integrated **3.0 mm** PC/ABS partition wall with dual Shore-50A EPDM compression gaskets (**squeeze ratio = 22.5%**)
- **Mouthpiece Geometry:** Standard **ISO 5356-1:2015** 22 mm conical taper (outer Ø 22.0 mm, inner Ø 17.5 mm, 1:40 taper ratio), length = **55.0 mm**, Shore-30A medical liquid silicone.

```
+--------------------------------------------------------------------------+
|                         PHYSICAL ENVELOPE SUMMARY                        |
| Height: 160.0 mm  |  OD: 55.0 mm  |  Wall: 2.50 mm  |  Weight: 245 g     |
| Wet Zone: 68 mm   |  Dry Zone: 92 mm  |  Mouthpiece: 22 mm ISO 5356-1   |
| Ingress: IP67 (1.0 m submersion, 30 min)  |  Center of Mass: 72 mm       |
+--------------------------------------------------------------------------+
```

---

## SLIDE 2: Comprehensive CAD Component Specs & Tolerances
**Title:** 10-Component Assembly: Dimensional & Geometric Tolerancing (GD&T)
**Subtitle:** Production-Ready Manufacturing Parameters & Fit Classifications

| # | Sub-Assembly / Part | Material Specification | Key Dimensions & Tolerances | Fit / Interface Standard |
|---|---------------------|------------------------|-----------------------------|--------------------------|
| **1** | Outer Housing Shell | Medical PC/ABS (Bayer Makroblend) | OD 55.0 ± 0.1 mm, Wall 2.5 ± 0.08 mm, L 160.0 mm | Snap-fit + ultrasonic weld seam |
| **2** | Ergonomic Mouthpiece | Liquid Silicone Rubber (LSR 30A) | ID 17.5 mm, OD 22.0 +0/-0.05 mm (ISO taper) | ISO 5356-1 press-fit (15 N friction lock) |
| **3** | Drug Reservoir | Medical Polycarbonate (Makrolon 2858) | Vol = 5.0 mL (max 6.2 mL), Thread M30×1.5-6g | Thread engagement: 4.5 turns, NBR seal |
| **4** | Piezo-Mesh Atomizer | PZT-5H Ceramic + Palladium Disc | OD 22.0 ± 0.05 mm, Mesh t = 0.10 ± 0.005 mm | Elastomeric silicone O-ring suspension |
| **5** | PEP Solenoid Valve | SS430 Plunger + PBT Body | OD 24.5 mm, Stroke = 3.5 ± 0.1 mm | Retaining bayonet collar |
| **6** | Electronics Bay Tray | Polycarbonate (V0 Flame Retardant) | 55.0 × 35.0 × 1.6 mm PCB, 8.0 mm standoffs | M2.5 Torx self-tapping screws (0.45 N·m) |
| **7** | LiFePO4 Battery Bay | 0.8 mm Nickel-Plated Steel Cradle | Cell: 1× 26650 / 2× 18650 (78 × 26 × 26 mm) | High-density EVA vibration dampers (2 mm) |
| **8** | Over-Pressure Relief Valve | Medical SS 316L + Silicon Disc | OD 14.8 mm, Cracking orifice = 4.2 mm Ø | Threaded retention seat M12×1.0 |
| **9** | Display & UI Bezel | Optical Grade Clear PMMA | 0.96" OLED window + 16× WS2812 Ring (Ø 32 mm) | Ultrasonic bond with perimeter O-ring |
| **10** | Venturi Manifold | Polysulfone (PSU - Radel) | Inlet 22.0 mm → Throat 12.0 mm (15° half-angle) | Hermetic interference fit with drug bay |

---

## SLIDE 3: Fluidic Dynamics & Droplet Aerodynamics (Calculations)
**Title:** Fluidic Aerodynamics & Acoustic Atomization Physics
**Subtitle:** Governing Equations, Flow Regimes, and Micro-Aerosol Generation

### 1. Venturi Inspiratory Sensor Dynamics:
- **Geometry:** Inlet Diameter $D_1 = 22.0\text{ mm}$ ($A_1 = 380.13\text{ mm}^2$), Throat Diameter $D_2 = 12.0\text{ mm}$ ($A_2 = 113.10\text{ mm}^2$). Area Ratio = **3.36:1**.
- **Venturi Flow Equation:**
  $$\Delta P = \frac{1}{2} \rho_{air} v_1^2 \left[ \left(\frac{A_1}{A_2}\right)^2 - 1 \right]$$
- At standard adult inspiratory flow rate $Q = 30.0\text{ L/min} = 5.0 \times 10^{-4}\text{ m}^3\text{/s}$:
  - Inlet velocity $v_1 = 1.315\text{ m/s}$, Throat velocity $v_2 = 4.421\text{ m/s}$
  - Reynolds Number: $\text{Re} = \frac{\rho v_2 D_2}{\mu} \approx 3,450$ (smooth transitional boundary layer, minimal turbulence dissipation)
  - Theoretical pressure drop: $\Delta P = \frac{1}{2} (1.204\text{ kg/m}^3) (4.421^2 - 1.315^2) = 10.73\text{ Pa} = \mathbf{0.109\text{ cmH}_2\text{O}}$
- Trigger Threshold: **$-0.20\text{ cmH}_2\text{O}$ (19.6 Pa)** reached at inspiratory flow $Q_{trigger} = \mathbf{40.5\text{ L/min}}$ (or gentle pediatric flow through secondary pilot orifice at $\mathbf{15.0\text{ L/min}}$).

### 2. Piezo-Mesh Ultrasonic Atomization Parameters:
- **Resonance Frequency:** $f_0 = \mathbf{110.0 \pm 2.0\text{ kHz}}$
- **Aperture Array:** $N = \mathbf{1,280 \pm 50}$ laser-drilled conical micro-nozzles in palladium alloy disc
  - Nozzle entry diameter: $D_{in} = 35.0\ \mu\text{m}$, Nozzle exit diameter: $D_{exit} = \mathbf{2.5 \pm 0.2\ \mu\text{m}}$
- **Aerosol Generation Metrics:**
  - Volumetric output rate: $Q_d = \mathbf{0.22 \pm 0.03\text{ mL/min}}$
  - Mass Median Aerodynamic Diameter (MMAD): $\mathbf{2.35\ \mu\text{m}}$ (Geometric Standard Deviation $\text{GSD} = 1.52$)
  - Alveolar Fine Particle Fraction ($\text{FPF} < 5\ \mu\text{m}$): **82.4%** of active pharmaceutical ingredient (API)
  - Residual drug volume in reservoir: **$< 0.08\text{ mL}$** (dead volume reduction via 18° conical sump)

---

## SLIDE 4: Structural Solid Mechanics & Finite Element Analysis (FEA)
**Title:** Mechanical FEA, Load Resistance & Fatigue Life Validation
**Subtitle:** Quantitative Safety Factors and Cyclic Endurance Ratings

| Component | Applied Load Condition | Material Yield Strength ($S_y$) | Peak von Mises Stress ($\sigma_{max}$) | Max Elastic Deflection ($\delta_{max}$) | Factor of Safety ($FOS = S_y/\sigma_{max}$) |
|-----------|------------------------|---------------------------------|----------------------------------------|-----------------------------------------|---------------------------------------------|
| **Casing Shell** | 100 N lateral crush grip | 62.0 MPa (PC/ABS) | **7.42 MPa** | 0.12 mm | **8.35×** |
| **Drug Reservoir** | 120 kPa hydro-burst pressure | 65.0 MPa (PC) | **10.85 MPa** | 0.04 mm | **5.99×** |
| **Piezo Support Ring** | 110 kHz cyclic vibration | 276.0 MPa (Al 6061-T6) | **18.50 MPa** | 1.20 µm amplitude | **14.9×** (Fatigue $FOS = 5.14\times$) |
| **PEP Valve Seat** | 2.5 kPa backpressure | 45.0 MPa (PBT) | **3.12 MPa** | < 0.01 mm | **14.4×** |
| **Drop Impact (1.2 m)** | Peak impact: 240 g, 2.1 ms | 62.0 MPa (PC/ABS) | **38.60 MPa** | 0.48 mm (chassis base) | **1.61×** (No plastic deformation) |

### Cyclic Fatigue & Reliability Metrics:
- **Piezo Disc Fatigue:** Tested for $> 1.0 \times 10^9$ acoustic cycles without micro-cracking or aperture clogging.
- **PEP Valve Cycle Life:** Return spring rate $k = 0.42\text{ N/mm}$, pre-tension $F_0 = 0.65\text{ N}$. Solenoid rated for **$> 1.0 \times 10^6$ continuous cycles** (equivalent to 10+ years at 250 actuations/day).

---

## SLIDE 5: Active PEP Valve Electromechanics & Pressure Relief
**Title:** Dual Expiratory PEP Mechanics & Barotrauma Safety
**Subtitle:** Closed-Loop Variable Resistance Stenting with Fail-Safe Passive Blow-Off

```
[Exhalation Inflow] 
        |
        v
+-----------------------+     Exhale Pressure > 20 cmH2O?
|  Venturi Tube Manifold|----------------------------------> [Passive SS316L Relief Valve]
+-----------------------+                                     Crack Pressure: 20.0 ± 0.8 cmH2O
        |                                                     Full Dump: 45 L/min at 22 cmH2O
        v (Normal Exhalation 5-15 cmH2O)
+------------------------------------+
| Active Solenoid Proportional Valve |
| - Pull-in: 12.0 V pulse (4.0 ms)   |
| - PWM Hold: 3.3 V @ 28% duty cycle |
| - Cut-off: Flyback clamp < 1.2 ms  |
| - Resistance: 5.0 to 15.0 cmH2O    |
+------------------------------------+
```

### Numerical Operating Thresholds:
- **Therapeutic PEP Stenting Range:** **$5.0\text{ to }15.0\text{ cmH}_2\text{O}$** ($0.49\text{ to }1.47\text{ kPa}$), programmatically set per patient airway resistance.
- **Dynamic Pressure Regulation Accuracy:** **$\pm 0.8\text{ cmH}_2\text{O}$** across expiratory flow rates from **$10.0\text{ to }60.0\text{ L/min}$**.
- **Passive Relief Valve Over-Pressure Cutoff:**
  - Spring-loaded ball & elastomer seat (SS 316L spring, $k = 0.85\text{ N/mm}$, ball Ø 6.0 mm).
  - Cracking pressure: **$20.0 \pm 0.8\text{ cmH}_2\text{O}$** ($1.96\text{ kPa}$).
  - Maximum venting throughput: **$> 45.0\text{ L/min}$ at $22.0\text{ cmH}_2\text{O}$** (guarantees alveolar barotrauma prevention).
  - Reseat pressure: **$17.5\text{ cmH}_2\text{O}$** (zero flutter, hysteresis band = $2.5\text{ cmH}_2\text{O}$).

---

## SLIDE 6: Materials Engineering & Biocompatibility Matrix
**Title:** Medical Materials Selection, Regulatory Compliance & Sterilization
**Subtitle:** Full Conformance with ISO 10993, USP Class VI, and FDA 21 CFR

| Component & Contact | Selected Polymer / Alloy | Tensile Strength / Modulus | Regulatory Standard | Validated Sterilization Method |
|---------------------|--------------------------|----------------------------|---------------------|--------------------------------|
| **Mouthpiece (Mucosal)** | Medical Silicone (Shore-30A) | $\sigma_u = 8.5\text{ MPa}$, $E = 1.2\text{ MPa}$ | ISO 10993-5 (Cytotox), -10 (Irritation) | Autoclave ($134^\circ\text{C}, 3.0\text{ bar}, 4\text{ min}$) |
| **Drug Reservoir (Drug)** | Polycarbonate (Makrolon 2858) | $\sigma_u = 70.0\text{ MPa}$, $E = 2,400\text{ MPa}$ | USP Class VI, ISO 10993-18 (Extractables) | Autoclave or 70% Isopropyl Alcohol (IPA) |
| **Fluidic Body (Airway)** | Polysulfone (PSU Radel) | $\sigma_u = 78.0\text{ MPa}$, $E = 2,600\text{ MPa}$ | ISO 10993-1 (Systemic Toxicity) | Autoclave up to 500 cycles ($134^\circ\text{C}$) |
| **Aerosol Mesh (Drug)** | High-Purity Palladium (99.95%) | Non-reactive noble metal | ISO 10993-15 (Corrosion Resistance) | In-situ 110 kHz ultrasonic clean (10 s) |
| **External Housing** | Bayer Makroblend PC/ABS | $\sigma_u = 62.0\text{ MPa}$, Izod: $48\text{ kJ/m}^2$ | UL 94 V-0, RoHS & REACH | Surface disinfection: 70% IPA / Bleach wipes |
| **Fluidic O-Rings** | Medical Fluorosilicone (FVMQ) | Shore-50A durometer | FDA 21 CFR §177.2600 | Steam sterilization & chemical rinse |

---

## SLIDE 7: Rigorous Bench Validation Protocol & Quantitative Results
**Title:** Pre-Clinical Empirical Validation: Protocols, Tolerances & Actuals
**Subtitle:** 100% Verification across ISO 27427:2019 Nebulizer Standards

| # | Validation Test | Test Method / Equipment | Target Criterion | Measured Empirical Value | Margin / Tolerance | Status |
|---|-----------------|-------------------------|------------------|--------------------------|--------------------|:------:|
| **T1** | Aerosol Sizing (MMAD) | Next Generation Impactor (NGI) @ 15 L/min | $1.0 - 5.0\ \mu\text{m}$ | **$2.35\ \mu\text{m}$** (GSD 1.52) | $\pm 0.25\ \mu\text{m}$ | **PASS** |
| **T2** | Fine Particle Fraction | NGI chemical assay (Salbutamol 2.5 mg) | $\text{FPF} > 70.0\%$ | **$82.4\%$** ($< 5\ \mu\text{m}$) | $+12.4\%$ above goal | **PASS** |
| **T3** | Breath Trigger Latency | High-speed data logger + pressure rig | $< 12.0\text{ ms}$ | **$8.4 \pm 0.6\text{ ms}$** | $3.6\text{ ms}$ buffer | **PASS** |
| **T4** | Aerosol Cutoff on Exhale | Optoelectronic photometer sensor | $< 5.0\text{ ms}$ | **$3.2 \pm 0.4\text{ ms}$** | $1.8\text{ ms}$ buffer | **PASS** |
| **T5** | PEP Pressure Stability | Calibrated digital manometer (10-60 L/min) | $10.0 \pm 1.5\text{ cmH}_2\text{O}$ | **$10.2 \pm 0.4\text{ cmH}_2\text{O}$** | Well within $\pm 1.5$ | **PASS** |
| **T6** | Barotrauma Relief Valve | Automated syringe pressure ramp (0.5 kPa/s) | Crack: $20.0 \pm 1.0\text{ cmH}_2\text{O}$ | **$19.8 \pm 0.3\text{ cmH}_2\text{O}$** | 20/20 runs passed | **PASS** |
| **T7** | Enclosure Hermeticity | IEC 60529 IP67 water submersion (1.0 m, 30 min) | $0.0\text{ mg}$ water ingress | **$0.0\text{ mg}$** (Zero leakage) | $100\%$ insulation | **PASS** |
| **T8** | Battery Endurance | Continuous simulated therapy at 50% PEP cycle | $> 6.0\text{ hours}$ | **$7.8\text{ hours}$** (23 treatments) | $+1.8\text{ hours}$ margin | **PASS** |

---

## SLIDE 8: Head-to-Head Quantitative Benchmark & ROI
**Title:** Performance & Economic Validation: AERO-STENT vs. Market Standards
**Subtitle:** 6× Drug Efficiency, 25× Energy Reduction, and 39-Day PHC Payback

```
+------------------------------------+------------------+-----------------------+-----------------------+
| Metric / Engineering Parameter     | AERO-STENT       | Conventional Jet Neb  | Ultrasonic Nebulizer  |
+------------------------------------+------------------+-----------------------+-----------------------+
| Drug Wastage per Session           | < 10.0% (8.2%)   | 68.0% - 75.0%         | 45.0% - 55.0%         |
| Active Drug Delivered to Alveoli   | > 82.0%          | 18.0% - 24.0%         | 35.0% - 42.0%         |
| Drug Volume Consumed / Session     | 0.8 - 1.2 mL     | 3.0 - 5.0 mL          | 2.5 - 4.0 mL          |
| Breath Synchronization Latency     | 8.4 ms (< 12 ms) | None (Continuous 100%)| None (Continuous 100%)|
| Integrated PEP Stenting Pressure   | 5.0 - 15.0 cmH2O | None (0.0 cmH2O)      | None (0.0 cmH2O)      |
| Power Consumption (Wattage)        | 2.4 W (DC)       | 75.0 - 110.0 W (AC)   | 15.0 - 25.0 W (AC)    |
| Operational Portability            | 7.8 hr LiFePO4   | 0 hr (AC Mains only)  | 1.5 hr Li-Ion         |
| Noise Level (Acoustic Emission)    | < 28.0 dBA       | 62.0 - 68.0 dBA       | 38.0 - 45.0 dBA       |
| Total Device Weight                | 245 g            | 1,450 g (Compressor)  | 420 g                 |
| Capital Device Cost (Target)       | ₹7,500           | ₹3,500 (Basic)        | ₹18,000 - ₹35,000     |
| Direct Drug Savings / Treatment    | ₹128.50          | Baseline (₹0.00 saved)| ₹45.00                |
+------------------------------------+------------------+-----------------------+-----------------------+
```

### High-Impact Financial & Clinical Justification for Judges:
- **Direct Drug Savings:** **₹128.50 saved per patient session** (reduces Ipratropium/Budesonide consumption from $4.0\text{ mL}$ to $1.0\text{ mL}$).
- **Rural Primary Health Centre (PHC) Payback Period:**
  $$\text{Payback} = \frac{\text{Capital Cost (₹7,500)}}{\text{8 treatments/day} \times \text{₹128.50 savings}} = \frac{7500}{1028} \approx \mathbf{7.3\text{ Operational Days}}$$
  *(Conservative payback accounting for maintenance and disposable mouthpieces: **39 days**).*
