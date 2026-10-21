# AERO-STENT 3D CAD & Mechanical Design Bay

This directory contains the production-grade parametric 3D CAD models, exploded assemblies, 3D print mesh files, and high-resolution rendering assets for **AERO-STENT**.

---

## 📦 CAD Files Manifest

| File | Format | Description | Compatibility |
|------|--------|-------------|---------------|
| `aerostent_assembled.blend` | Blender 3D (`.blend`) | Fully assembled 10-part master assembly stacked on single central axis with semi-transparent outer shell | Blender 4.x / 5.2+ |
| `aerostent_cad_model.blend` | Blender 3D (`.blend`) | Exploded mechanical assembly with annotated sub-assemblies | Blender 4.x / 5.2+ |
| `aerostent_assembled.stl` | Stereolithography (`.stl`) | High-resolution watertight solid mesh for additive manufacturing / 3D printing | Cura, PrusaSlicer, Bambu Studio |
| `aerostent_cad_model.stl` | Stereolithography (`.stl`) | Exploded view layout for multi-part manufacturing validation | Any Slicer |
| `aerostent_assembled.obj` / `.mtl` | Universal Wavefront OBJ | Textured 3D mesh for import into SolidWorks, Autodesk Fusion 360, FreeCAD, or WebGL viewers | CAD / WebGL |
| `aerostent_cad_model.obj` / `.mtl` | Universal Wavefront OBJ | Exploded 3D mesh with material assignments | CAD / WebGL |

---

## 🛠️ The 10 Sub-Assemblies Breakdown

1. **Outer Housing Shell:** Medical-grade PC/ABS (160×55mm Ø, 2.5mm wall), IP67 hermetic barrier.
2. **Silicone Mouthpiece:** Shore-30A Liquid Silicone Rubber, ISO 5356-1 compliant 22mm conical taper.
3. **Drug Reservoir:** Medical Polycarbonate (Makrolon 2858), 5.0 mL capacity, M30×1.5 thread.
4. **Piezo-Mesh Atomizer:** PZT-5H ceramic ring + 99.95% palladium disc (110 kHz, 1,280 nozzles × 2.5 µm).
5. **PEP Solenoid Valve:** SS430 plunger + PBT body (stroke 3.5 mm, active 5–15 cmH₂O resistance).
6. **Electronics PCB Tray:** Flame-retardant PC tray with 8.0 mm standoffs for STM32 + ESP32 boards.
7. **LiFePO4 Battery Cradle:** 0.8 mm steel retention tray for 3000 mAh cell with 2.0 mm EVA shock pads.
8. **Over-Pressure Relief Valve:** SS 316L spring-loaded safety pop-off (cracks at >20 cmH₂O barotrauma limit).
9. **Display & LED Ring Bezel:** Optical PMMA window for 0.96" OLED + 16-LED circular halo ring.
10. **Venturi Flow Manifold:** Polysulfone (PSU Radel) throat (22mm → 12mm, 15° taper angle).

---

## 🖨️ 3D Printing & Fabrication Settings

- **Recommended Material:** Polycarbonate (PC) or PETG for rigid casing; Medical Shore-30A Liquid Silicone for mouthpiece.
- **Layer Height:** 0.12 mm – 0.16 mm (Adaptive layers recommended for threads).
- **Infill:** 40% Gyroid for structural rigidity; 100% solid around threaded collar.
- **Wall Perimeters:** 4 perimeters minimum (1.6 mm effective skin).
- **Sterilization Compatibility:** Autoclavable at 134°C (fluidic parts) / 70% IPA wipe-down (housing).
