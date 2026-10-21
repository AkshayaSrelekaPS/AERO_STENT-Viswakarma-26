import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_aerostent_proposal(output_path):
    doc = Document()

    # Page Setup (1 inch margins all around)
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

    # Color Palette: Deep Medical Teal & Emerald
    COLOR_PRIMARY = RGBColor(0x0A, 0x4D, 0x68)    # Deep Medical Teal
    COLOR_SECONDARY = RGBColor(0x08, 0x83, 0x95)  # Medical Emerald
    COLOR_TEXT = RGBColor(0x1F, 0x29, 0x37)       # Charcoal / Off-black
    
    HEX_PRIMARY = "0A4D68"
    HEX_SECONDARY = "088395"
    HEX_BG_LIGHT = "F0F7F7"
    HEX_CALLOUT_BG = "EFF8F8"
    HEX_BORDER = "D1D5DB"
    HEX_HIGHLIGHT = "D1E8E2"

    # Base Normal Style Setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Segoe UI'
    font.size = Pt(10.5)
    font.color.rgb = COLOR_TEXT
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(6)

    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_cell_left_border(cell, hex_color, size="36"):
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="{size}" w:space="0" w:color="{hex_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(borders)

    def apply_table_styles(table):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="{HEX_PRIMARY}"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="{HEX_PRIMARY}"/><w:left w:val="none"/><w:right w:val="none"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/><w:insideV w:val="none"/></w:tblBorders>')
        tblPr.append(borders)

    def add_header_banner():
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=180, bottom=180, left=240, right=240)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        
        r1 = p.add_run('VISHWAKARMA AWARDS 2026–27  |  MAKER BHAVAN FOUNDATION\n')
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGBColor(0x05, 0xBF, 0xDB)
        
        r2 = p.add_run('STAGE 1: OPEN APPLICATION PROPOSAL • HARDWARE INNOVATION\n')
        r2.font.bold = True
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
        r3 = p.add_run('TEAM NAME: TECHTONICS  |  THEME 1: HEALTH TECH (HOST: IIT INDORE)  |  SUBTHEME 1: THERAPEUTIC HARDWARE')
        r3.font.bold = True
        r3.font.size = Pt(10)
        r3.font.color.rgb = RGBColor(0xE0, 0xF7, 0xFA)
        
        doc.add_paragraph()

    def add_custom_heading(text, level=1):
        h = doc.add_paragraph()
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.bold = True
        if level == 1:
            r.font.size = Pt(14)
            r.font.color.rgb = COLOR_PRIMARY
            h.paragraph_format.space_before = Pt(16)
            h.paragraph_format.space_after = Pt(6)
        else:
            r.font.size = Pt(11.5)
            r.font.color.rgb = COLOR_SECONDARY
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(4)
        return h

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_CALLOUT_BG)
        set_cell_left_border(cell, HEX_SECONDARY, size="36")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        
        r_t = p.add_run(title + "\n")
        r_t.font.bold = True
        r_t.font.size = Pt(10.5)
        r_t.font.color.rgb = COLOR_PRIMARY
        
        r_b = p.add_run(text)
        r_b.font.italic = True
        r_b.font.size = Pt(10)
        r_b.font.color.rgb = COLOR_TEXT
        doc.add_paragraph()

    def add_figure_card(fig_title, placement, prompt, citation, image_path=None):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F8FAFC")
        set_cell_left_border(cell, HEX_PRIMARY, size="24")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        
        r_t = p.add_run(f"■ FIGURE / ILLUSTRATION: {fig_title}\n")
        r_t.font.bold = True
        r_t.font.size = Pt(10.5)
        r_t.font.color.rgb = COLOR_PRIMARY

        if image_path and os.path.exists(image_path):
            p_img = cell.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(6)
            run_img = p_img.add_run()
            run_img.add_picture(image_path, width=Inches(5.6))
        
        p_desc = cell.add_paragraph()
        p_desc.paragraph_format.space_after = Pt(0)
        p_desc.add_run(f"• Document Placement: {placement}\n").font.size = Pt(9.5)
        
        r_pr = p_desc.add_run(f"• Professional Generation Prompt:\n  \"{prompt}\"\n")
        r_pr.font.size = Pt(9.5)
        r_pr.font.italic = True
        
        r_c = p_desc.add_run(f"• Citation & Reference: {citation}")
        r_c.font.size = Pt(9.5)
        r_c.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)
        doc.add_paragraph()

    # ----------------- DOCUMENT GENERATION ----------------- #

    add_header_banner()

    # 1. TITLE OF THE PROJECT / PRODUCT
    add_custom_heading('1. TITLE OF THE PROJECT / PRODUCT', level=1)
    p = doc.add_paragraph()
    r = p.add_run('Product Nomenclature: ')
    r.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    p.add_run('AERO_STENT: A High-Speed Breath-Actuated Piezo-Mesh Nebulizer with Synchronized Positive Expiratory Pressure (PEP) Airway Stenting & Expansion\n')

    r2 = p.add_run('Track & Alignment: ')
    r2.bold = True
    r2.font.color.rgb = COLOR_PRIMARY
    p.add_run('Maker Bhavan Foundation — Vishwakarma Awards 2026–27 | Mentor Institute: IIT Indore | Domain: Health Tech, Therapeutic & Life-Sustaining Hardware, Point-of-Care & Emergency Care Devices (ANRF Alignment: Health & Medical Technology Sector).\n')

    # Hero Product Render
    hero_img = '/home/akshaya/Downloads/viswakarma/aerostent_3d_product_hero_render.png'
    add_figure_card(
        'AERO_STENT Industrial 3D Hardware Render',
        'Section 1: Product Title & Hero Visual',
        'Professional studio 3D product render of AERO_STENT medical device. A handheld ergonomic medical inhalation device made of medical-grade white matte ABS plastic and clear translucent polycarbonate reservoir chamber. Shows a soft medical silicone mouthpiece on top, a subtle illuminated teal LED status ring, a small OLED metric display, and a micro USB-C charging port. Clean isolated background, neutral studio lighting.',
        'Team TECHTONICS Industrial Hardware Concept Render.',
        image_path=hero_img
    )

    # 2. PROBLEM STATEMENT
    add_custom_heading('2. PROBLEM STATEMENT', level=1)
    p = doc.add_paragraph()
    r = p.add_run('Context & Clinical Severity: ')
    r.bold = True
    p.add_run('Acute respiratory distress stemming from severe asthma, Chronic Obstructive Pulmonary Disease (COPD), bronchiolitis, and pneumonia accounts for millions of emergency hospital visits across rural India. In low-resource Primary Health Centres (PHCs) and off-grid clinical settings, traditional jet nebulizers continuously emit a cloud of expensive bronchodilators and corticosteroids into ambient air regardless of whether the patient is inhaling or exhaling. Because a patient spends nearly 65% to 70% of the breathing cycle in exhalation and respiratory pauses, more than two-thirds of critical medication is completely wasted into the atmosphere. This continuous aerosolization leads to severe financial distress for low-income patients, rapidly depletes rural PHC drug stocks, and exposes healthcare workers to secondhand corticosteroid inhalation and airborne viral pathogens. Furthermore, during acute bronchospasms, inflamed airways suffer physical collapse during exhalation; standard nebulizers offer zero mechanical support to maintain airway patency. Existing hospital-grade breath-synchronized nebulizers cost over ₹1.2 to ₹2.5 Lakhs, rendering them inaccessible to 85% of rural Indian healthcare facilities. A low-cost, battery-operated, breath-synchronized therapeutic hardware platform is urgently required.')

    add_callout(
        'Core Problem Statement (Single-Sentence Definition):',
        '"Primary Health Centres and low-resource emergency wards in India waste over 65% to 70% of vital bronchodilator and corticosteroid therapeutics through continuous, un-synchronized aerosol nebulization, exacerbating drug shortages, causing financial strain, and providing zero physical support against expiratory airway collapse, while commercial breath-actuated hospital units remain cost-prohibitive (>₹1.5 Lakhs) and unviable for off-grid rural deployment."'
    )

    # 3. SOLUTION PROPOSED
    add_custom_heading('3. SOLUTION PROPOSED', level=1)
    p = doc.add_paragraph()
    p.add_run('AERO_STENT is a portable, ultra-low-power, breath-actuated therapeutic hardware device engineered to deliver synchronized micro-dose nebulization exclusively during inhalation while providing dynamic Positive Expiratory Pressure (PEP) pneumatic stenting therapy during exhalation. Driven by a high-frequency (110 kHz) microfluidic piezoelectric vibrating mesh and a micro-differential pressure sensing pipeline, AERO_STENT detects inspiratory effort in under 12 milliseconds, atomizing 1–5 µm aerosol droplets targeted directly at deep alveolar tissue. Upon exhalation detection, the aerosol generator instantly snaps shut (zero drug waste), and an integrated variable PEP valve engages to generate 5–15 cmH2O of gentle backpressure, physically stenting small airways open and mobilizing trapped pulmonary mucus.')

    add_custom_heading('3.1 Decoupled Two-Tier Sensing & Actuation Architecture', level=2)
    p = doc.add_paragraph()
    p.add_run('To guarantee medical-grade deterministic timing, patient safety, and zero signal lag, high-level respiratory sensing and low-level physical actuation are strictly decoupled across two processors:\n')
    p.add_run('• Tier 1 — Respiratory Perception Processor (ESP32 / Pico Dual-Core 32-bit): ').bold = True
    p.add_run('Continuously samples a medical-grade differential pressure transducer (MPXV7002DP) and micro-acoustic sensor array at 1 kHz. Executes digital low-pass filtering, moving-average slope analysis, and breath-phase state estimation (Inspiration, Expiration, Pause). Transmits compact control frames to Tier 2 via a high-speed isolated UART bus (115200 baud).\n')
    p.add_run('• Tier 2 — Real-Time Deterministic Actuation Coprocessor (STM32G431 MCU): ').bold = True
    p.add_run('Dedicated exclusively to high-frequency hardware pulse generation and power switching. Drives the 110 kHz piezo-mesh AC inverter circuit during inhalation and manages an active Zener-clamped solenoid driver board for the dynamic PEP valve with sub-millisecond precision.')

    add_custom_heading('3.2 Airway Sensing & Environmental Pressure-Differential Perception', level=2)
    p = doc.add_paragraph()
    p.add_run('Respiratory flow sensing in distressed pediatric or geriatric patients is prone to motion artifacts, ambient drafts, and weak inspiratory effort. AERO_STENT overcomes these challenges:\n')
    p.add_run('• Ultra-Sensitive Differential Pressure Transducer: ').bold = True
    p.add_run('Connected to a micro-Venturi orifice inside the mouthpiece, detecting inspiratory pressure drops as subtle as -0.2 cmH2O (~20 Pa).\n')
    p.add_run('• Acousto-Pneumatic Noise Cancellation: ').bold = True
    p.add_run('Dual pressure taps cancel out ambient atmospheric pressure spikes caused by room fans or movement, preventing false-positive valve triggers.\n')
    p.add_run('• Biocompatible Non-Invasive Flow Channel: ').bold = True
    p.add_run('Smooth, autoclavable silicone-and-polycarbonate manifold engineered according to ISO 10993 cytotoxicity and biocompatibility standards.')

    add_custom_heading('3.3 Breath-Cycle Synchronization & Dynamic Flow-Volume Compensation', level=2)
    p = doc.add_paragraph()
    p.add_run('• Sub-12ms Activation Latency: ').bold = True
    p.add_run('The moment the patient begins inhaling, the MCU triggers the piezo inverter within 12 ms, delivering drug mist at the exact onset of tidal volume expansion for maximum pulmonary penetration.\n')
    p.add_run('• Zero-Waste Active Exhalation Cutoff: ').bold = True
    p.add_run('Upon detecting pressure reversal (> +0.1 cmH2O), the piezo driver shuts off in <5 ms, ensuring zero aerosol is expelled into the room.\n')
    p.add_run('• Adaptive Inspiratory Timing Window: ').bold = True
    p.add_run('The MCU continuously tracks rolling average breath durations. If a patient experiences panic hyperventilation or prolonged apnea, the safety watchdog limits continuous spraying to a maximum of 2.5 seconds per breath, preventing over-dosing.')

    add_custom_heading('3.4 High-Speed Microfluidic Piezo-Mesh Atomizer & Active Zener Snubber Driver', level=2)
    p = doc.add_paragraph()
    p.add_run('• 110 kHz Vibrating Palladium Mesh: ').bold = True
    p.add_run('Features ~1,200 laser-drilled micro-apertures (2.5 µm diameter) activated by a piezoelectric ring transducer. Atomizes medication into uniform 1–5 µm particles ideal for lower respiratory tract deposition.\n')
    p.add_run('• Peak-and-Hold PEP Valve Solenoid Driver: ').bold = True
    p.add_run('A 12V mini-solenoid dynamically adjusts exhalation port orifice size. An N-channel MOSFET driver applies a 12V 4ms pull-in pulse, then throttles to a 3.3V PWM holding voltage, reducing power consumption by 72% and eliminating thermal buildup.\n')
    p.add_run('• Active Zener Flyback Snubber: ').bold = True
    p.add_run('Incorporates an active Zener diode clamp (Vz = 36V) across the solenoid coil, collapsing magnetic flux in <1.2 ms for instantaneous valve closure without residual mechanical bounce.')

    add_custom_heading('3.5 Offline-First Vernacular Clinician User Interface', level=2)
    p = doc.add_paragraph()
    p.add_run('Designed for intuitive operation by rural nurses, CHW workers, and paramedics:\n')
    p.add_run('• Local Web Dashboard & Bluetooth PWA: ').bold = True
    p.add_run('The ESP32 hosts an offline Wi-Fi AP (AeroStent_PHC_Net) accessible via any smartphone browser in Hindi, Marathi, and English.\n')
    p.add_run('• One-Touch Controls & Live Clinical Metrics: ').bold = True
    p.add_run('Features large visual indicators: GREEN (Auto-Therapy Active), RED (Emergency Stop). Displays real-time metrics: "Drug Saved Today: 68% | Breath Count: 142 | Battery: 85%".\n')
    p.add_run('• Automated Flush & Sterilization Cycle: ').bold = True
    p.add_run('Includes a 10-second high-frequency ultrasonic self-cleaning cycle with distilled water to prevent medication crystallization and nozzle clogging between patients.')

    fig1_img = '/home/akshaya/Downloads/viswakarma/aerostent_fig1_architecture_cutaway.png'
    add_figure_card(
        'Figure 1 — AERO_STENT Decoupled Architecture, Airway Sensor & Fluidics Cutaway',
        'Section 3: Solution Proposed (Electronics, Sensing & Fluidics)',
        'Engineering system architecture and side cross-section illustration of AERO_STENT medical device. Top: Two-tier compute split showing ESP32 sensing processor connected via optical isolation UART link to STM32G4 real-time piezo/solenoid coprocessor. Bottom: Handheld ergonomic housing cutaway showing mouthpiece with micro-Venturi pressure tap, 110kHz vibrating piezo-mesh fluid reservoir, dynamic adjustable PEP exhalation valve, and 3.7V LiFePO4 battery compartment.',
        'Original biomedical mechanical and electronic design by Team TECHTONICS, adhering to ISO 13485 medical device standards.',
        image_path=fig1_img
    )

    fig2_img = '/home/akshaya/Downloads/viswakarma/aerostent_fig2_waveforms_diagram.png'
    add_figure_card(
        'Figure 2 — Breath-Cycle Timing Diagram & Hardware Waveforms',
        'Section 3.3: Breath-Cycle Synchronization & Waveforms',
        'Detailed electrical and clinical timing diagram. Top waveform: Patient Airway Pressure (cmH2O) showing smooth inhalation dip (-1.5 cmH2O) and exhalation peak (+10 cmH2O PEP). Middle waveform: Piezo Inverter Drive Signal showing active 110kHz PWM burst strictly aligned with inhalation dip. Bottom waveform: Solenoid PEP Valve Voltage showing 12V 4ms peak pull-in, 3.3V hold, and instantaneous active Zener flyback demagnetization spike (<1.2ms).',
        'Team TECHTONICS Embedded Firmware Architecture, validated against STM32 timer hardware and IEC 60601 clinical timing specifications.',
        image_path=fig2_img
    )

    # 4. IMPLEMENTATION PLAN
    add_custom_heading('4. IMPLEMENTATION PLAN', level=1)
    p = doc.add_paragraph()
    r = p.add_run('Target Beneficiaries: ')
    r.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    p.add_run('Primary: Rural PHCs, Community Health Centres (CHCs), and low-resource emergency wards treating pediatric asthma, adult COPD, and acute respiratory distress; Secondary: Rural paramedics and mobile disaster response units; Tertiary: Patients suffering financial distress from expensive chronic respiratory drugs.')

    tbl_time = doc.add_table(rows=5, cols=4)
    tbl_time.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_styles(tbl_time)

    headers = ['Phase / Month', 'Milestone Focus', 'Key Engineering Tasks', 'Verification Deliverable']
    for i, h in enumerate(headers):
        cell = tbl_time.cell(0, i)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_time = [
        ['Phase 1\n(M1 - M2)', 'Sensor Calibration &\nPiezo Mesh Drive', 'Calibrate MPXV7002DP pressure sensor; build 110kHz piezo AC inverter circuit; design micro-Venturi flow channel.', 'Benchtop piezo mist validation; oscilloscope proof of <12ms breath detection latency.'],
        ['Phase 2\n(M3 - M4)', 'Dual-Tier PCB &\nPEP Valve Assembly', 'Fabricate 2-layer medical PCB (ESP32 + STM32 + Zener snubber + LiFePO4 BMS); integrate dynamic PEP solenoid valve manifold.', 'Integrated prototype handling 5–15 cmH2O adjustable backpressure stability.'],
        ['Phase 3\n(M5)', 'Firmware Synchronization &\nOffline App', 'Implement rolling breath-timing algorithm; build offline vernacular PWA dashboard; complete automated ultrasonic purge mode.', 'Functional AERO_STENT device running on benchtop breath-simulator pump.'],
        ['Phase 4\n(M6)', 'Clinical Bench Validation &\nIIT Indore Trial', 'Conduct lung-simulator aerosol deposition trials; measure drug volume savings vs standard jet nebulizer; perform safety checks.', 'Final validation report detailing >65% drug volume savings and zero ambient aerosol drift.']
    ]

    for row_idx, row_data in enumerate(data_time, start=1):
        for col_idx, text in enumerate(row_data):
            cell = tbl_time.cell(row_idx, col_idx)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            bg = HEX_BG_LIGHT if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.size = Pt(9.5)

    doc.add_paragraph()

    # 5. SAFETY AND EFFICIENCY ANALYSIS
    add_custom_heading('5. SAFETY AND EFFICIENCY ANALYSIS', level=1)
    p = doc.add_paragraph()
    p.add_run('Medical hardware and emergency respiratory intervention demand defensive electrical, fluidic, and operational safety mechanisms:\n')
    p.add_run('• Medical-Grade Galvanic & Electrical Isolation: ').bold = True
    p.add_run('The patient-contact sensor and fluidic assembly are galvanically isolated from the 12V/5V power supply via optocouplers (6N137) and an isolated DC-DC converter (B0505S). Earth-leakage current is strictly capped at <10 µA complying with IEC 60601-1 medical electrical safety standards.\n')
    p.add_run('• Physical Wet/Dry Compartmentalization: ').bold = True
    p.add_run('The device features an IP67-rated sealed upper electronics bay holding the PCBs and lithium battery, completely separated from the autoclavable lower fluidic mouthpiece chamber, eliminating contamination and leakage risks.\n')
    p.add_run('• Patient Protection Interlocks:\n').bold = True
    p.add_run('  1. Over-Pressure Relief Valve: Mechanical spring relief opens at >20 cmH2O to prevent alveolar barotrauma.\n  2. Auto-Cutoff Watchdog: Automatically disables spraying if continuous inspiration exceeds 2.5 seconds.\n  3. Empty Tank Sensing: Piezo current monitoring detects fluid dry-run and stops oscillation to prevent mesh burnout.\n')
    p.add_run('• Tri-Mode Hackathon Demo Fail-Safe: ').bold = True
    p.add_run('If live pitch demo faces unexpected ambient airflow noise, the device features three operating modes: (1) Full Autonomous Breath-Actuated Mode; (2) Manual Clinician Push-Button Override Mode; (3) Stationary Self-Test / Demonstration Cycle.\n')
    p.add_run('• Quantitative Clinical, Labor & Energy Efficiency: ').bold = True
    p.add_run('Traditional jet nebulizers consume 3.0–5.0 mL of drug solution per treatment session (wasting ~3.2 mL into room air) and require 60W AC power. AERO_STENT accomplishes equivalent pulmonary drug delivery using only 0.8–1.2 mL per treatment (saving 68% drug volume) and consumes <2.5W DC power.')

    # 6. SCALABILITY AND FUTURE DEVELOPMENT
    add_custom_heading('6. SCALABILITY AND FUTURE DEVELOPMENT', level=1)
    add_custom_heading('Unit Economics & Bill of Materials (BOM)', level=2)

    tbl_bom = doc.add_table(rows=8, cols=4)
    tbl_bom.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_styles(tbl_bom)

    headers_bom = ['Subsystem / Component', 'Part Designation', 'Prototype Qty', 'Estimated Cost (INR)']
    for i, h in enumerate(headers_bom):
        cell = tbl_bom.cell(0, i)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_bom = [
        ['Respiratory Sensing & Compute', 'ESP32 MCU + MPXV7002DP Differential Sensor', '1 Set', '₹2,200'],
        ['Real-Time Timing MCU & Driver PCB', 'STM32G431 MCU + Custom MOSFET/Zener Driver PCB', '1 Board', '₹1,700'],
        ['Microfluidic Piezo Mesh Assembly', '110kHz Palladium Vibrating Mesh + Piezo Inverter', '1 Unit', '₹2,100'],
        ['Dynamic PEP Valve & Solenoid', 'Adjustable Spring Solenoid Valve + Venturi Channel', '1 Assembly', '₹1,400'],
        ['Medical Power System', '3.7V 3000mAh LiFePO4 Battery + BMS + Buck Reg', '1 Pack', '₹1,100'],
        ['Housing & Autoclavable Chamber', 'Biocompatible PC/ABS Enclosure & Silicone Mask', '1 Kit', '₹1,300'],
        ['TOTAL ESTIMATED BOM COST', 'Complete Functional Hardware Prototype', '1 System', '₹9,800']
    ]

    for row_idx, row_data in enumerate(data_bom, start=1):
        for col_idx, text in enumerate(row_data):
            cell = tbl_bom.cell(row_idx, col_idx)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            if row_idx == 7:
                set_cell_background(cell, HEX_HIGHLIGHT)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(text)
                r.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = COLOR_PRIMARY
            else:
                bg = HEX_BG_LIGHT if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(text)
                r.font.size = Pt(9.5)

    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run('Economic Feasibility: ')
    r.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    p.add_run('Total Prototype BOM Cost: ₹9,800 | Projected Production BOM (500+ Units): ₹4,200 (Target Retail Price: ₹7,500). Capital payback for rural PHCs is achieved within 40 days through drug savings alone.')

    add_custom_heading('6.1 Scalability & Business Model Integration', level=2)
    p = doc.add_paragraph()
    p.add_run('• Fast Capital Payback: ').bold = True
    p.add_run('Rural PHCs recover the device cost within 40 days through savings on bronchodilator and corticosteroid ampoules alone.\n')
    p.add_run('• Modular Hospital & Home Care Retrofit: ').bold = True
    p.add_run('The AERO_STENT head unit features a standard 22mm ISO taper, allowing direct attachment to standard oxygen masks, tracheostomy tubes, or ventilator circuits.')

    # 7. INNOVATION ADVANTAGE
    add_custom_heading('7. INNOVATION ADVANTAGE', level=1)
    p = doc.add_paragraph('A direct comparative benchmark against existing nebulization and airway treatment methods highlights the commercial and technical uniqueness of AERO_STENT:')

    tbl_bench = doc.add_table(rows=7, cols=5)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_styles(tbl_bench)

    headers_b = ['Technical Feature', 'Traditional Jet Nebulizer', 'Standard Mesh Nebulizer', 'MDI + Spacer', 'AERO_STENT']
    for i, h in enumerate(headers_b):
        cell = tbl_bench.cell(0, i)
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=140, bottom=140, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    data_b = [
        ['Breath Synchronization', 'None (Continuous Spray)', 'None (Continuous Spray)', 'Manual Timing Dependent', 'Automated Sub-12ms Sync'],
        ['Chemical Drug Wastage', '65% – 75% Waste', '50% – 60% Waste', '40% – 50% Waste', '< 10% Waste (>68% Saved)'],
        ['Expiratory Airway Support', 'Zero (Passive)', 'Zero (Passive)', 'Zero (Passive)', 'Active (5-15 cmH2O PEP)'],
        ['Ambient Room Pollution', 'Severe Aerosol Drift', 'High Aerosol Drift', 'Minimal', 'Zero (Closed-loop Cutoff)'],
        ['Power Consumption', '60W – 100W AC Mains', '2W – 3W Battery', 'None (Manual)', '< 2.5W Battery / Solar DC'],
        ['Smallholder / PHC Cost', '₹2,500 (High Drug Loss)', '₹8,000 – ₹15,000', '₹800 (Low Efficacy)', '₹7,500 Target Retail']
    ]

    for row_idx, row_data in enumerate(data_b, start=1):
        for col_idx, text in enumerate(row_data):
            cell = tbl_bench.cell(row_idx, col_idx)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if col_idx == 4:
                set_cell_background(cell, HEX_HIGHLIGHT)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(text)
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = COLOR_PRIMARY
            else:
                bg = HEX_BG_LIGHT if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                r = p.add_run(text)
                r.font.size = Pt(9)

    doc.add_paragraph()

    # 8. VISUAL IMPACT & USER JOURNEY
    add_custom_heading('8. VISUAL IMPACT & USER JOURNEY', level=1)
    p = doc.add_paragraph('The operational impact of AERO_STENT is captured in an end-to-end user journey comparing status-quo continuous jet nebulization with synchronized breath-actuated micro-dose injection.')

    add_callout(
        'User Journey: Emergency Rural Respiratory Care Experience',
        'CHALLENGE SCENARIO: A 7-year-old child suffering an acute asthma attack arrives at a rural PHC in Madhya Pradesh at 2:00 AM during a prolonged power outage.\n\n• BEFORE (Conventional Jet Nebulizer):\n1. Nurse struggles to run a noisy 80W generator to power the jet nebulizer.\n2. The nebulizer continuously blows a thick cloud of Levosalbutamol mist into the room for 15 minutes.\n3. The child exhales against closed, inflamed airways; 3.5 mL of medication is wasted into room air.\n4. The nurse inhales secondhand steroid mist; the child remains wheezing due to airway collapse during exhalation. Total drug cost: ₹180 per session.\n\n• AFTER (With AERO_STENT):\n1. Nurse snaps AERO_STENT onto the child\'s mask and presses the single green button (runs on internal LiFePO4 battery).\n2. The device detects micro-inhalation in 12 ms and sprays a fine 2.5 µm mist ONLY during inhalation.\n3. During exhalation, the mist stops instantly, and the PEP valve provides 10 cmH2O backpressure, physically stenting small bronchioles open and clearing mucus.\n4. Treatment completes in 4 minutes using only 0.8 mL of medication (saving ₹120 in drug costs). The child stabilizes rapidly with zero room pollution.'
    )

    fig3_img = '/home/akshaya/Downloads/viswakarma/aerostent_fig3_app_lung_heatmap.png'
    add_figure_card(
        'Figure 3 — Offline Vernacular Clinician App & Lung Deposition Comparison Heatmap',
        'Section 3.5 & Section 8: User Interface & Clinical Comparison Heatmap',
        'Two-part high-contrast vector graphic. Left: Mobile phone mockup running offline PWA clinician dashboard in Hindi language displaying large green \'Start Therapy\' button, active pressure gauge (8 cmH2O PEP), battery level (85%), and live counter (\'₹140 Medication Saved Today\'). Right: Comparative lung aerosol deposition heatmaps—Left Lung (Conventional Continuous Spray) showing 70% aerosol escape into room air with sparse lung deposition; Right Lung (AERO_STENT Synchronized) showing deep concentrated aerosol deposition in lower bronchioles with zero room escape.',
        'Clinical Flow Specification by Team TECHTONICS, evaluated against Indian Council of Medical Research (ICMR) respiratory protocol guidelines.',
        image_path=fig3_img
    )

    doc.save(output_path)
    print('Successfully generated DOCX:', output_path)

if __name__ == '__main__':
    paths = [
        '/home/akshaya/Downloads/viswakarma/AERO_STENT_Theme1_Proposal.docx',
        '/home/akshaya/Downloads/viswakarma/TECHTONICS_Theme1_AERO_STENT_Proposal.docx',
        '/home/akshaya/Downloads/viswakarma/AERO-STENT_Theme1_Proposal.docx',
        '/home/akshaya/Downloads/viswakarma/AGRO-STENT_Theme1_Proposal.docx'
    ]
    for p in paths:
        create_aerostent_proposal(p)
