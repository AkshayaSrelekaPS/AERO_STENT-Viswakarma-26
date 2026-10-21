# AERO-STENT PCB & Hardware Electronics Bay
### High-Speed Breath-Actuated Nebulizer & PEP Stent Embedded Hardware
**Team TECHTONICS | Vishwakarma Awards 2026–27 | Theme 1: Health Tech | IIT Indore**

---

## ⚡ Electronics Architecture Overview

The AERO-STENT hardware platform integrates high-precision differential pressure sensing with ultra-fast inductive and ultrasonic actuation circuits on an isolated medical-grade PCB.

### Core Circuit Modules:
1. **Power Management & Li-Ion Charging:**
   * **TP4056-42-ESOP8** linear charger for 3.7V LiFePO4 / Li-Ion cells with constant-current/constant-voltage profiling.
   * Thermal regulation, reverse-polarity protection, and automatic recharge cutoff.
   * Onboard micro-USB / USB-C charging input with ESD transient suppression diodes.

2. **110 kHz Ultrasonic Piezo-Mesh Gate Driver:**
   * High-speed N-Channel MOSFET switching network driving the 110.0 kHz PZT-5H ceramic resonance disc.
   * Fast gate discharge pull-down to ensure clean square-wave acoustic drive without inductive ringing.

3. **Active Zener Snubber Solenoid Driver (Sub-1.2 ms Cutoff):**
   * High-power low-side MOSFET switch with peak-and-hold capability (12V 4 ms pull-in, 3.3V hold).
   * **36V Zener + Schottky flyback demagnetization clamp** across the solenoid coil, reducing current decay latency from 35 ms down to **< 1.2 ms** to eliminate post-exhalation drug dripping.

4. **Analog Sensing Front-End (MPXV7002DP Transducer):**
   * Low-noise active RC anti-aliasing filter interfacing the differential pressure sensor with the ADC.
   * Calibrated for $-0.20\text{ cmH}_2\text{O}$ inspiratory threshold detection and $5.0 - 15.0\text{ cmH}_2\text{O}$ PEP tracking.

---

## 📁 PCB Files Directory

| File / Folder | Type | Description |
|:---|:---:|:---|
| **`AERO_STENT.kicad_pro`** | KiCad Project | Master KiCad 8.x / 10.x project workspace |
| **`AERO_STENT.kicad_sch`** | KiCad Schematic | Complete electrical schematic with TP4056, drivers, and MCU pinouts (51 KB) |
| **`AERO_STENT.kicad_pcb`** | KiCad PCB Layout | 2-layer board layout with continuous ground plane isolation |
| **`AERO_STENT.kicad_prl`** | Project Settings | Local design rules and layer visibility presets |
| **`gerber/`** | Manufacturing Package | Production-ready Gerber RS-274X files |
| **`gerber/AERO_STENT_Gerber_Fabrication.zip`** | Production Zip | Ready-to-upload archive for PCB fabrication houses (JLCPCB, PCBWay, LionCircuits) |

---

## 🏭 Fabrication & Manufacturing Specifications

- **Layers:** 2-Layer Rigid FR4
- **Board Thickness:** 1.60 mm
- **Copper Weight:** 1 oz (35 µm) outer layers
- **Surface Finish:** Lead-Free HASL / Electroless Nickel Immersion Gold (ENIG)
- **Solder Mask:** Medical Matte Green / Black
- **Silkscreen:** High-Contrast White
- **Minimum Trace / Space:** 6 mil / 6 mil (0.15 mm)
- **Minimum Drill Hole:** 0.30 mm

---

## 🚀 How to Open and Review

Open the project in **KiCad**:
```bash
kicad pcb/AERO_STENT.kicad_pro
```
Or inspect the schematic directly in Eeschema:
```bash
eeschema pcb/AERO_STENT.kicad_sch
```
