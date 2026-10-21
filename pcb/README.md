# AERO-STENT PCB Design Bay

> ⚠️ **Status: Hardware Engineering in Progress**

This directory is reserved for the custom embedded electronics schematics, PCB layout routing, bill of materials (BOM), and Gerber production files.

### 📐 Target Board Specifications:
- **Dual-MCU Architecture:**
  - **Core 1 (STM32G474):** High-resolution timer (HRTIM) driving 110 kHz resonant Piezo-PWM & MPXV7002DP 1 kHz ADC sampling.
  - **Core 2 (ESP32-S3):** Bluetooth Low Energy (BLE 5.0) telemetry, OLED display driver, and local clinical logging.
- **Form Factor:** Custom dual-stacked rigid FR4 boards (55.0 × 35.0 mm), 4-layer stackup with continuous ground plane isolation.
- **Power Management:** Integrated Texas Instruments BQ25895 battery management IC with 3.7V LiFePO4 charging and 12V boost for solenoid pull-in.
- **Files to be added:**
  - `schematics/` (KiCad 8.0 / Altium `.kicad_sch` / `.SchDoc`)
  - `layout/` (`.kicad_pcb` / `.PcbDoc`)
  - `gerber/` (RS-274X production zips)
  - `bom/` (Interactive HTML BOM)
