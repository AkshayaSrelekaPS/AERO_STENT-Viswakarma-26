# AERO-STENT Engineering Diagrams & Scientific Figures

This directory contains the primary system architecture schematics, fluidic waveforms, and clinical deposition heatmaps for **AERO-STENT**.

---

## 🖼️ Figures Index

### 1. System Architecture & Internal Cutaway
* **File:** `aerostent_fig1_architecture_cutaway.png`
* **Description:** Cross-sectional mechanical and pneumatic architecture illustrating the hermetic boundary separating the upper fluidic "Wet Zone" (Venturi throat, 110 kHz piezo-mesh, PEP solenoid) from the lower avionics "Dry Zone" (dual-MCU electronics and 3000 mAh LiFePO4 battery pack).

### 2. Breath-Actuated PEP Waveform Dynamics
* **File:** `aerostent_fig2_waveforms_diagram.png`
* **Description:** High-speed synchronization timing diagram showing:
  - Inhalation pressure drop detection (<8.4 ms latency)
  - 110 kHz piezo atomization window
  - Exhalation cutoff (<3.2 ms latency)
  - Active 5–15 cmH₂O Positive Expiratory Pressure (PEP) airway stenting plateau

### 3. Pulmonary Aerosol Deposition Heatmap & Clinical UI
* **File:** `aerostent_fig3_app_lung_heatmap.png`
* **Description:** In-silico lung deposition simulation comparing conventional continuous nebulizers (18–24% alveolar deposition, heavy oropharyngeal impaction) vs. AERO-STENT synchronized micro-dosing (>82% deep alveolar penetration, <10% waste).
