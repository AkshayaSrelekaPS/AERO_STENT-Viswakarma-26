"""
================================================================================
  AERO-STENT CAD — FULLY ASSEMBLED NEBULIZER
  Team: TECHTONICS | Vishwakarma Awards 2026-27 | Theme 1: Health Tech
  Host: IIT Indore

  ASSEMBLY LAYOUT (bottom -> top, central axis):
  ------------------------------------------------
  Z   0-14   : Bottom cap + IP67 O-ring
  Z  14-140  : Outer housing shell (semi-transparent ABS)
  Z   5-32   : [INTERNAL] LiFePO4 Battery pack (2x 18650)
  Z  35-70   : [INTERNAL] Dual-tier PCB bay (ESP32 + STM32G431)
  Z  65-105  : [INTERNAL] PEP solenoid valve (vertical internal)
  Z  85-89   : [INTERNAL] Piezo-mesh atomizer disk
  Z  90-132  : [INTERNAL] Drug reservoir chamber (clear, upper housing)
  Z  80-103  : [FRONT FACE] OLED display + teal LED ring + buttons
  Z ~100     : [SIDE] Over-pressure relief valve (stub port)
  Z 138-160  : Venturi flow manifold (transition neck)
  Z 160-215  : Silicone mouthpiece (patient interface)

  CMD TO OPEN IN BLENDER GUI:
    /home/akshaya/Downloads/blender-5.2.1-linux-x64/blender \
        /home/akshaya/Downloads/viswakarma/aerostent_assembled.blend
================================================================================
"""

import bpy, math

OUTPUT_BLEND = "/home/akshaya/Downloads/viswakarma/aerostent_assembled.blend"
OUTPUT_STL   = "/home/akshaya/Downloads/viswakarma/aerostent_assembled.stl"
OUTPUT_OBJ   = "/home/akshaya/Downloads/viswakarma/aerostent_assembled.obj"

MM = 0.001   # mm -> Blender metres

# ──────────────────────────────────────────────────────────────────────────────
#  SCENE UTILS
# ──────────────────────────────────────────────────────────────────────────────

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in (bpy.data.meshes, bpy.data.materials,
                bpy.data.curves, bpy.data.lights, bpy.data.cameras):
        for item in list(col):
            col.remove(item)


def mat(name, rgb, rough=0.35, metal=0.0, alpha=1.0,
        emit=None, emit_str=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    if alpha < 1.0:
        m.blend_method = 'BLEND'
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value  = (*rgb[:3], 1.0)
    b.inputs["Roughness"].default_value   = rough
    b.inputs["Metallic"].default_value    = metal
    b.inputs["Alpha"].default_value       = alpha
    if emit:
        b.inputs["Emission Color"].default_value    = (*emit[:3], 1.0)
        b.inputs["Emission Strength"].default_value = emit_str
    return m


def asgn(o, m):
    if o.type not in ('MESH','FONT','CURVE'):
        return
    if o.data.materials:
        o.data.materials[0] = m
    else:
        o.data.materials.append(m)


def cyl(name, r, h, loc, rot=(0,0,0), verts=64):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts,
        radius=r*MM, depth=h*MM,
        location=(loc[0]*MM, loc[1]*MM, loc[2]*MM),
        rotation=rot)
    o = bpy.context.active_object
    o.name = name
    return o


def box(name, dims, loc, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(
        location=(loc[0]*MM, loc[1]*MM, loc[2]*MM),
        rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = (dims[0]*MM/2, dims[1]*MM/2, dims[2]*MM/2)
    bpy.ops.object.transform_apply(scale=True)
    return o


def torus(name, R, r, loc):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=R*MM, minor_radius=r*MM,
        major_segments=64, minor_segments=24,
        location=(loc[0]*MM, loc[1]*MM, loc[2]*MM))
    o = bpy.context.active_object
    o.name = name
    return o


def sph(name, r, loc):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=r*MM, segments=32, ring_count=16,
        location=(loc[0]*MM, loc[1]*MM, loc[2]*MM))
    o = bpy.context.active_object
    o.name = name
    return o


# ──────────────────────────────────────────────────────────────────────────────
#  MATERIAL PALETTE
# ──────────────────────────────────────────────────────────────────────────────

def build_mats():
    return {
        # Outer shell — white ABS (slightly transparent so internals show)
        'shell'   : mat("M_Shell_ABS",    (0.94,0.94,0.92), rough=0.38,
                        alpha=0.60),
        # Fully opaque white ABS for external solid parts
        'abs'     : mat("M_ABS_Solid",    (0.94,0.94,0.92), rough=0.38),
        # Matte dark ABS for grip waist / textured zone
        'grip'    : mat("M_Grip_ABS",     (0.18,0.18,0.18), rough=0.82),
        # Translucent polycarbonate — drug reservoir
        'pc'      : mat("M_PC_Clear",     (0.78,0.94,1.00), rough=0.04,
                        alpha=0.35),
        # Medical silicone — mouthpiece
        'sil'     : mat("M_Silicone",     (0.12,0.48,0.78), rough=0.70),
        # Palladium mesh
        'pd'      : mat("M_Palladium",    (0.55,0.50,0.55), rough=0.10,
                        metal=0.97),
        # Stainless steel
        'ss'      : mat("M_Steel",        (0.76,0.76,0.78), rough=0.16,
                        metal=0.92),
        # Copper / solenoid coil
        'cu'      : mat("M_Copper",       (0.72,0.45,0.20), rough=0.26,
                        metal=0.88),
        # PCB green
        'pcb'     : mat("M_PCB_Green",    (0.05,0.30,0.10), rough=0.55,
                        metal=0.04),
        # IC / chip black
        'ic'      : mat("M_IC_Black",     (0.08,0.08,0.08), rough=0.48),
        # Battery black
        'bat'     : mat("M_Battery",      (0.10,0.10,0.10), rough=0.55),
        # OLED screen
        'oled'    : mat("M_OLED",         (0.02,0.02,0.02), rough=0.80),
        # Teal LED glow
        'led'     : mat("M_Teal_LED",     (0.00,0.85,0.90), rough=0.04,
                        emit=(0.0,0.85,0.90), emit_str=9.0),
        # Green button
        'gbtn'    : mat("M_GreenBtn",     (0.10,0.82,0.22), rough=0.45),
        # Red button
        'rbtn'    : mat("M_RedBtn",       (0.90,0.10,0.10), rough=0.45),
        # Spring steel
        'spr'     : mat("M_Spring",       (0.65,0.65,0.68), rough=0.14,
                        metal=0.95),
        # Rubber / O-ring
        'rub'     : mat("M_Rubber",       (0.14,0.14,0.14), rough=0.88),
        # Medical polysulfone — venturi
        'psf'     : mat("M_Polysulfone",  (0.88,0.84,0.74), rough=0.28),
        # Teal OLED ring accent
        'teal_acc': mat("M_TealAccent",   (0.00,0.78,0.85), rough=0.30,
                        emit=(0.0,0.78,0.85), emit_str=3.0),
    }


# ══════════════════════════════════════════════════════════════════════════════
#   ASSEMBLED NEBULIZER — all parts on central axis (0, 0)
#   Y+ = front face (where display sits)
#   Z  = vertical height
# ══════════════════════════════════════════════════════════════════════════════

def build_assembled_nebulizer(M):

    # ── PART 1: OUTER HOUSING SHELL ──────────────────────────────────────────
    # Semi-transparent so internal components are visible
    # Height: 0 – 140 mm  |  OD: 55 mm  |  grip waist at z=30-80

    shell = cyl("P1_Housing_Shell", 27.5, 130, (0, 0, 70))
    asgn(shell, M['shell'])

    # Textured grip zone (dark, middle section)
    grip = cyl("P1_Grip_Zone", 24.0, 55, (0, 0, 48))
    asgn(grip, M['grip'])

    # Bottom cap (solid, opaque)
    bot_cap = cyl("P1_Bottom_Cap", 27.5, 14, (0, 0, 7))
    asgn(bot_cap, M['abs'])

    # IP67 O-ring groove at bottom cap split-line
    oring = torus("P1_IP67_Oring", 26.5, 1.2, (0, 0, 13))
    asgn(oring, M['rub'])

    # Slight chamfer ring at top of housing
    top_rim = torus("P1_HousingTopRim", 26.5, 1.5, (0, 0, 135))
    asgn(top_rim, M['abs'])

    # USB-C charging port slot (bottom-right side)
    usbc = box("P1_USBC_Port", (9, 4, 3.5), (0, -26, 20))
    asgn(usbc, M['oled'])

    # ── PART 7: LiFePO4 BATTERY PACK (z: 5 – 32 mm) ─────────────────────────
    # Two 18650 cells horizontal inside bottom of housing

    bat_tray = box("P7_Battery_Tray", (52, 22, 26), (0, 0, 18))
    asgn(bat_tray, M['bat'])

    for xo in (-13, 13):
        cell = cyl(f"P7_18650_Cell_{xo}", 8.5, 48,
                   (xo, 0, 18), rot=(0, math.pi/2, 0))
        asgn(cell, M['bat'])
        term = cyl(f"P7_PosTerminal_{xo}", 2, 2,
                   (xo + (24 if xo > 0 else -24), 0, 18),
                   rot=(0, math.pi/2, 0))
        asgn(term, M['ss'])

    bms = box("P7_BMS_Board", (44, 18, 1.8), (0, 0, 29))
    asgn(bms, M['pcb'])
    bms_ic = box("P7_BMS_Chip", (8, 6, 2), (-8, 0, 31))
    asgn(bms_ic, M['ic'])

    bat_latch = box("P7_SlideLock", (16, 5, 3), (0, -22, 5))
    asgn(bat_latch, M['ss'])

    # ── PART 6: ELECTRONICS PCB BAY (z: 35 – 72 mm) ─────────────────────────
    # Dual-tier board stack inside housing

    pcb_tray = box("P6_PCBCarrier_Tray", (50, 36, 4), (0, 0, 52))
    asgn(pcb_tray, M['abs'])

    # Upper board — ESP32 + MPXV7002DP
    upper = box("P6_ESP32_Board", (46, 30, 1.6), (0, 0, 64))
    asgn(upper, M['pcb'])
    esp32 = box("P6_ESP32_Module", (16, 18, 3.2), (-8, 0, 66))
    asgn(esp32, M['ic'])
    mpxv  = box("P6_MPXV7002DP", (7, 5, 4.5), (13, 7, 66))
    asgn(mpxv, M['ic'])

    # Pressure sense tube from MPXV to Venturi (small cylinder going up)
    sense_tube = cyl("P6_SenseTube", 1.2, 80, (13, 7, 108),
                     rot=(0, 0, 0))
    asgn(sense_tube, M['abs'])

    # Lower board — STM32G431 + driver
    lower = box("P6_STM32_Board", (46, 30, 1.6), (0, 0, 52))
    asgn(lower, M['pcb'])
    stm32 = box("P6_STM32G431", (10, 10, 2.5), (-7, -4, 54))
    asgn(stm32, M['ic'])
    for i, xo in enumerate((-6, 3, 12)):
        fet = box(f"P6_MOSFET_{i}", (5, 5, 3), (xo, 9, 54))
        asgn(fet, M['ic'])
    opto = box("P6_Opto_6N137", (5, 6, 3.8), (17, -6, 54))
    asgn(opto, M['ic'])

    # DC/DC converter
    dcdc = box("P6_B0505S_DCDC", (11, 7, 5), (-17, 8, 52))
    asgn(dcdc, M['ic'])

    # Standoffs connecting the two boards
    for dx, dy in ((-18,-11),(18,-11),(-18,11),(18,11)):
        so = cyl(f"P6_Standoff_{dx}_{dy}", 1.4, 10, (dx, dy, 57))
        asgn(so, M['ss'])

    # Isolated UART connection ribbon (flat box)
    uart_ribbon = box("P6_UART_Ribbon", (2, 26, 10), (22, 0, 58))
    asgn(uart_ribbon, M['ic'])

    # ── PART 5: PEP SOLENOID VALVE (z: 68 – 105 mm, internal) ───────────────
    # Mounted vertically inside the housing, at rear

    pep_body = cyl("P5_PEPValve_Body", 10.5, 36, (0, -12, 86))
    asgn(pep_body, M['abs'])

    pep_coil = cyl("P5_Solenoid_Coil", 9, 24, (0, -12, 80))
    asgn(pep_coil, M['cu'])

    pep_plunger = cyl("P5_Plunger", 3.2, 26, (0, -12, 80))
    asgn(pep_plunger, M['ss'])

    for i in range(7):
        sc = torus(f"P5_Spring_{i}", 3.5, 0.5, (0, -12, 93 + i*1.4))
        asgn(sc, M['spr'])

    # PEP exhalation port — short stub out through housing side
    pep_port = cyl("P5_ExhPort_Stub", 3.5, 12, (0, -26, 100),
                   rot=(math.pi/2, 0, 0))
    asgn(pep_port, M['abs'])
    pep_cap  = cyl("P5_ExhPort_Cap",  5.0, 3,  (0, -32, 100),
                   rot=(math.pi/2, 0, 0))
    asgn(pep_cap, M['abs'])

    # PEP exhalation bore (clear channel through valve)
    pep_bore = cyl("P5_ExhBore", 3.5, 36, (0, -12, 86))
    asgn(pep_bore, M['pc'])

    # ── PART 4: PIEZO-MESH ATOMIZER (z: 86 – 90 mm) ──────────────────────────
    # Sits at the base of the drug reservoir, inside housing

    pd_disk = cyl("P4_PalladiumMesh_Disk", 10.5, 0.10,
                  (0, 0, 88), verts=128)
    asgn(pd_disk, M['pd'])

    piezo_ring = torus("P4_PiezoRing", 11.5, 1.8, (0, 0, 88))
    asgn(piezo_ring, M['cu'])

    retainer = torus("P4_RetainerRing", 13.0, 2.0, (0, 0, 88))
    asgn(retainer, M['ss'])

    # Drive wires going down to PCB
    for ang in (0, math.pi):
        wx = 13*math.cos(ang)
        wy = 13*math.sin(ang)
        wire = cyl(f"P4_DriveWire_{int(math.degrees(ang))}", 0.5, 30,
                   (wx, wy, 73))
        asgn(wire, M['cu'])

    # Fluid feed channel from reservoir to mesh (inner tube)
    fluid_feed = cyl("P4_FluidFeed_Tube", 3.5, 44, (0, 0, 110))
    asgn(fluid_feed, M['pc'])

    # ── PART 3: DRUG RESERVOIR (z: 88 – 132 mm) ──────────────────────────────
    # Translucent chamber sitting above the piezo mesh, inside upper housing

    reservoir = cyl("P3_Reservoir_Body", 13.5, 44, (0, 0, 110))
    asgn(reservoir, M['pc'])

    res_neck = cyl("P3_Reservoir_Neck", 9.5, 10, (0, 0, 134))
    asgn(res_neck, M['abs'])

    fill_port = cyl("P3_FillPort_Plug", 2.8, 8,
                    (12, 0, 136), rot=(0, math.pi/2, 0))
    asgn(fill_port, M['sil'])

    # Volume graduation rings (every 8mm = 1mL)
    for i in range(5):
        vm = torus(f"P3_VolRing_{i+1}mL", 13.7, 0.4,
                   (0, 0, 91 + i*8))
        asgn(vm, M['abs'])

    # ── PART 8: OVER-PRESSURE RELIEF VALVE (z ~105, side port) ───────────────
    # Small stub valve on right side of housing

    relief_body = cyl("P8_ReliefValve", 6.0, 20,
                      (26, 0, 105), rot=(0, math.pi/2, 0))
    asgn(relief_body, M['ss'])

    relief_diaphragm = cyl("P8_Diaphragm", 4, 1.5,
                           (36, 0, 105), rot=(0, math.pi/2, 0))
    asgn(relief_diaphragm, M['sil'])

    for i in range(5):
        relief_spr = torus(f"P8_Spr_{i}", 3.2, 0.5,
                           (29 + i*1.2, 0, 105))
        asgn(relief_spr, M['spr'])

    relief_cap = cyl("P8_ReliefCap", 7.0, 3,
                     (37, 0, 105), rot=(0, math.pi/2, 0))
    asgn(relief_cap, M['abs'])

    # ── PART 9: OLED DISPLAY + LED RING (front face z ~75-105) ───────────────
    # Embedded in front face of housing (y+ side)

    # Display window cutout frame (raised bezel)
    bezel = box("P9_Display_Bezel", (30, 3.5, 18), (0, 27, 96))
    asgn(bezel, M['abs'])

    oled_panel = box("P9_OLED_Panel", (24, 2.5, 14), (0, 27.5, 96))
    asgn(oled_panel, M['oled'])

    # OLED text labels rendered as thin box (UI simulation)
    oled_ui = box("P9_OLED_UI_Content", (22, 1.5, 12), (0, 28, 96))
    asgn(oled_ui, mat("M_OLED_UI", (0.0,0.78,0.88), rough=0.2,
                       emit=(0.0,0.78,0.88), emit_str=2.0))

    # Teal LED status ring
    led_ring = torus("P9_LED_StatusRing", 16, 1.6, (0, 23, 78))
    asgn(led_ring, M['teal_acc'])

    for i in range(8):
        ang = i * math.pi / 4
        lx = 16*math.cos(ang)
        lz = 78 + 16*math.sin(ang)
        led = sph(f"P9_WS2812_{i}", 2.3, (lx, 23, lz))
        asgn(led, M['led'])

    # Green start button (left side of display)
    btn_g = cyl("P9_GreenBtn_Start", 5.5, 4.5,
                (0, 27, 80))
    asgn(btn_g, M['gbtn'])
    btn_g_ring = torus("P9_GreenBtn_Ring", 5.8, 0.7, (0, 25, 80))
    asgn(btn_g_ring, M['abs'])

    # Red emergency stop button (right)
    btn_r = cyl("P9_RedBtn_Stop", 4.0, 4.5,
                (0, 27, 112))
    asgn(btn_r, M['rbtn'])
    btn_r_ring = torus("P9_RedBtn_Ring", 4.3, 0.6, (0, 25, 112))
    asgn(btn_r_ring, M['abs'])

    # ── PART 10: MICRO-VENTURI MANIFOLD (z: 138 – 160 mm) ────────────────────
    # Transition neck between housing top and mouthpiece
    # Outer OD tapers from 27mm → 20mm

    venturi_body = cyl("P10_VenturiManifold", 11, 22, (0, 0, 149))
    asgn(venturi_body, M['psf'])

    venturi_throat = cyl("P10_VenturiThroat", 5.5, 8, (0, 0, 149))
    asgn(venturi_throat, M['pc'])

    # Upstream pressure tap
    tap_up = cyl("P10_UpstreamTap", 1.2, 12,
                 (11, 0, 154), rot=(0, math.pi/2, 0))
    asgn(tap_up, M['ss'])

    # Downstream pressure tap
    tap_dn = cyl("P10_DownstreamTap", 1.2, 12,
                 (-11, 0, 149), rot=(0, math.pi/2, 0))
    asgn(tap_dn, M['ss'])

    # Small sensor port block (leads to MPXV on PCB)
    sensor_blk = box("P10_SensorPort", (8, 5, 5), (0, 10, 152))
    asgn(sensor_blk, M['cu'])

    # Locking collar ring between housing top and venturi
    collar_ring = torus("P10_LockCollar", 13, 2.0, (0, 0, 140))
    asgn(collar_ring, M['ss'])

    # ── PART 2: SILICONE MOUTHPIECE (z: 160 – 210 mm) ────────────────────────
    # 22mm ISO taper, Shore-30A medical silicone

    # Smooth outer silicone body
    mouth_outer = cyl("P2_Mouthpiece_Outer", 15.5, 48, (0, 0, 184))
    asgn(mouth_outer, M['sil'])

    # Inner bore (air channel)
    mouth_bore = cyl("P2_Mouthpiece_Bore", 10.5, 52, (0, 0, 184))
    asgn(mouth_bore, M['pc'])

    # Lip flare at patient end (top)
    mouth_lip = cyl("P2_Mouthpiece_Lip", 18, 9, (0, 0, 207))
    asgn(mouth_lip, M['sil'])

    # Ribbed grip texture rings on mouthpiece (5 rings)
    for i in range(5):
        rrib = torus(f"P2_GripRib_{i}", 15.8, 0.8, (0, 0, 165+i*6))
        asgn(rrib, M['sil'])

    # ISO 22mm taper collar connecting to venturi
    iso_collar = cyl("P2_ISO22_Collar", 11, 10, (0, 0, 163))
    asgn(iso_collar, M['abs'])

    # Silicone seal ring at mouthpiece-venturi junction
    mouth_seal = torus("P2_JunctionSeal", 11.2, 1.0, (0, 0, 160))
    asgn(mouth_seal, M['rub'])

    # ── ANNOTATION LABELS ─────────────────────────────────────────────────────
    add_cad_labels(M)

    print("  All parts assembled.")


# ──────────────────────────────────────────────────────────────────────────────
#  CAD ANNOTATION CALLOUT LABELS
# ──────────────────────────────────────────────────────────────────────────────

def add_cad_labels(M):
    """Leader-line style labels pointing to key sub-assemblies."""
    label_mat = mat("M_Label_Text", (0.95,0.95,1.0), rough=0.9)

    annotations = [
        # (text, text_loc_mm, arrow_start_mm, arrow_end_mm)
        ("Silicone Mouthpiece\n22mm ISO Taper | Shore-30A",
         (55, 0, 210), (16, 0, 205), (40, 0, 210)),
        ("Venturi Flow Manifold\n−0.2 cmH₂O sensitivity",
         (55, 0, 152), (11, 0, 150), (40, 0, 152)),
        ("Drug Reservoir (5 mL)\nTranslucent Polycarbonate",
         (55, 0, 112), (14, 0, 110), (40, 0, 112)),
        ("Piezo-Mesh Atomizer\n110 kHz | Palladium | 1200 apertures",
         (55, 0, 88), (13, 0, 88), (40, 0, 88)),
        ("PEP Solenoid Valve\n5-15 cmH₂O | 12V/3.3V PWM",
         (-60, 0, 86), (-11, -12, 86), (-35, 0, 86)),
        ("OLED Display + LED Ring\n0.96in | 8x WS2812 Teal",
         (55, 0, 96), (15, 27, 96), (40, 0, 96)),
        ("Over-Pressure Relief\n> 20 cmH₂O | Anti-Barotrauma",
         (55, 0, 105), (28, 0, 105), (40, 0, 105)),
        ("ESP32 + STM32G431 PCB\nDual-Tier | 6N137 Isolated",
         (55, 0, 58), (23, 0, 58), (40, 0, 58)),
        ("LiFePO4 Battery\n3.7V 3000mAh | BMS | USB-C",
         (55, 0, 18), (23, 0, 18), (40, 0, 18)),
        ("IP67 Housing\nPC/ABS | 160×55mm Dia",
         (-60, 0, 70), (-27.5, 0, 70), (-35, 0, 70)),
    ]

    for text, tloc, aend, amid in annotations:
        # Text label
        bpy.ops.object.text_add(
            location=(tloc[0]*MM, tloc[1]*MM, tloc[2]*MM))
        t = bpy.context.active_object
        t.name = f"LBL_{text[:20].replace(chr(10),'_')}"
        t.data.body = text
        t.data.size = 2.2 * MM
        t.data.align_x = 'LEFT'
        if tloc[0] < 0:
            t.data.align_x = 'RIGHT'
        t.data.align_y = 'CENTER'
        if t.data.materials:
            t.data.materials[0] = label_mat
        else:
            t.data.materials.append(label_mat)

        # Leader arrow line (thin cylinder)
        dx = amid[0] - aend[0]
        dy = amid[1] - aend[1]
        dz = amid[2] - aend[2]
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        if length > 0.5:
            cx = (amid[0]+aend[0])/2
            cy = (amid[1]+aend[1])/2
            cz = (amid[2]+aend[2])/2

            rot_y = math.atan2(math.sqrt(dx*dx+dy*dy), dz)
            rot_z = math.atan2(dy, dx)

            arrow = cyl(f"ARR_{text[:15]}", 0.4, length,
                        (cx, cy, cz),
                        rot=(0, rot_y, rot_z))
            asgn(arrow, mat(f"M_Arrow_{text[:10]}", (0.6,0.75,0.85),
                            rough=0.9))


# ──────────────────────────────────────────────────────────────────────────────
#  BRANDING BAND on housing surface
# ──────────────────────────────────────────────────────────────────────────────

def add_branding(M):
    """Add AERO-STENT logo text band on housing surface."""
    bpy.ops.object.text_add(
        location=(-8*MM, 27.6*MM, 52*MM),
        rotation=(math.pi/2, 0, 0)
    )
    logo = bpy.context.active_object
    logo.name = "Branding_AEROSTENT_Logo"
    logo.data.body = "AERO-STENT"
    logo.data.size = 5.5 * MM
    logo.data.align_x = 'LEFT'
    logo_mat = mat("M_Logo", (0.00,0.75,0.85), rough=0.25,
                   emit=(0.0,0.75,0.85), emit_str=1.5)
    asgn(logo, logo_mat)

    bpy.ops.object.text_add(
        location=(-9*MM, 27.6*MM, 44*MM),
        rotation=(math.pi/2, 0, 0)
    )
    sub = bpy.context.active_object
    sub.name = "Branding_Subtitle"
    sub.data.body = "TECHTONICS  |  Vishwakarma 2026-27"
    sub.data.size = 2.0 * MM
    sub.data.align_x = 'LEFT'
    sub_mat = mat("M_SubBranding", (0.88,0.88,0.92), rough=0.9)
    asgn(sub, sub_mat)


# ──────────────────────────────────────────────────────────────────────────────
#  CAMERA + LIGHTING
# ──────────────────────────────────────────────────────────────────────────────

def setup_camera_and_lighting():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 3840
    scene.render.resolution_y = 2160
    scene.render.filepath = \
        "/home/akshaya/Downloads/viswakarma/aerostent_assembled_render.png"

    # World background — dark studio
    world = bpy.data.worlds.new("World_Studio")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value    = (0.04, 0.045, 0.06, 1.0)
    bg.inputs['Strength'].default_value = 0.20

    # ── Camera — angled hero product shot ──────────────────────────────
    # Position: 45° front-right, elevated to show full height of device
    cam_x =  260 * MM
    cam_y = -380 * MM
    cam_z =  200 * MM   # elevated to show the mouthpiece
    bpy.ops.object.camera_add(
        location=(cam_x, cam_y, cam_z),
        rotation=(math.radians(72), 0, math.radians(34))
    )
    cam = bpy.context.active_object
    cam.name = "HeroCamera"
    cam.data.lens = 85              # telephoto → less distortion
    cam.data.sensor_width = 36
    cam.data.dof.use_dof = True
    # Focus at device centre (~z=110mm)
    cam.data.dof.focus_distance = \
        math.sqrt(cam_x**2 + cam_y**2 + (cam_z - 110*MM)**2)
    cam.data.dof.aperture_fstop = 5.6
    scene.camera = cam

    # ── 3-point studio lighting ───────────────────────────────────────

    # Key light (warm, top-left front)
    bpy.ops.object.light_add(type='AREA',
        location=(200*MM, 150*MM, 500*MM))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.energy = 8000
    key.data.size   = 300*MM
    key.data.color  = (1.0, 0.96, 0.90)
    key.rotation_euler = (math.radians(-40), math.radians(25), 0)

    # Fill light (cool, right side, soft)
    bpy.ops.object.light_add(type='AREA',
        location=(-350*MM, -80*MM, 200*MM))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 2000
    fill.data.size   = 500*MM
    fill.data.color  = (0.80, 0.88, 1.0)

    # Teal rim / back light (product accent)
    bpy.ops.object.light_add(type='SPOT',
        location=(0, 500*MM, 400*MM))
    rim = bpy.context.active_object
    rim.name = "RimLight_Teal"
    rim.data.energy    = 5000
    rim.data.spot_size = math.radians(35)
    rim.data.color     = (0.0, 0.85, 0.90)
    rim.rotation_euler = (math.radians(-50), 0, math.radians(180))

    # Bottom bounce (soft upward fill, gives floating look)
    bpy.ops.object.light_add(type='AREA',
        location=(0, 0, -50*MM))
    bounce = bpy.context.active_object
    bounce.name = "BounceFill"
    bounce.data.energy = 800
    bounce.data.size   = 400*MM
    bounce.data.color  = (0.90, 0.90, 1.0)
    bounce.rotation_euler = (math.pi, 0, 0)

    # Ground plane — infinite glossy dark surface
    bpy.ops.mesh.primitive_plane_add(size=2.5, location=(0, 0, 0))
    gnd = bpy.context.active_object
    gnd.name = "StudioGround"
    asgn(gnd, mat("M_Ground", (0.06, 0.06, 0.08), rough=0.15, metal=0.0))


# ──────────────────────────────────────────────────────────────────────────────
#  TITLE CARD
# ──────────────────────────────────────────────────────────────────────────────

def add_title_card():
    entries = [
        ("AERO-STENT",                              12*MM, (0.00,0.78,0.88)),
        ("Breath-Actuated Piezo-Mesh Nebulizer",     4.5*MM,(0.88,0.90,0.95)),
        ("with Positive Expiratory Pressure Stenting",4.0*MM,(0.70,0.72,0.78)),
        ("Team TECHTONICS  |  Vishwakarma Awards 2026-27  |  Theme 1: Health Tech",
         3.0*MM, (0.55,0.58,0.64)),
        ("Host: IIT Indore  |  Stage 1 CAD Submission  |  Blender 5.2",
         2.6*MM, (0.40,0.42,0.48)),
    ]
    z0 = 270*MM
    for i,(txt,sz,col) in enumerate(entries):
        bpy.ops.object.text_add(
            location=(-15*MM, -90*MM, z0 - i*14*MM))
        t = bpy.context.active_object
        t.name = f"TC_Line{i}"
        t.data.body = txt
        t.data.size = sz
        t.data.align_x = 'LEFT'
        asgn(t, mat(f"M_TC{i}", col, rough=0.9))


# ──────────────────────────────────────────────────────────────────────────────
#  EXPORT
# ──────────────────────────────────────────────────────────────────────────────

def export_all():
    bpy.ops.object.select_all(action='SELECT')
    for o in list(bpy.context.selected_objects):
        if o.type == 'FONT':
            o.select_set(False)

    # STL
    try:
        bpy.ops.wm.stl_export(
            filepath=OUTPUT_STL, check_existing=False,
            ascii_format=False, apply_modifiers=True,
            export_selected_objects=True, global_scale=1.0)
        print(f"  [OK] STL  -> {OUTPUT_STL}")
    except Exception as e:
        print(f"  [WARN] STL: {e}")

    # OBJ
    try:
        bpy.ops.wm.obj_export(
            filepath=OUTPUT_OBJ, check_existing=False,
            apply_modifiers=True, export_selected_objects=True,
            export_materials=True, global_scale=1.0)
        print(f"  [OK] OBJ  -> {OUTPUT_OBJ}")
    except Exception as e:
        print(f"  [WARN] OBJ: {e}")


# ──────────────────────────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 72)
    print("  AERO-STENT  |  FULLY ASSEMBLED NEBULIZER CAD")
    print("  Team TECHTONICS  |  Vishwakarma Awards 2026-27  |  Theme 1")
    print("  Host: IIT Indore  |  Therapeutic Hardware  |  Blender 5.2")
    print("=" * 72)

    clear_scene()
    print("[1/6] Scene cleared.")

    print("[2/6] Building material palette...")
    M = build_mats()

    print("[3/6] Building assembled nebulizer (all 10 parts)...")
    build_assembled_nebulizer(M)

    print("[4/6] Adding branding...")
    add_branding(M)

    print("[5/6] Setting up camera + 4-point lighting...")
    setup_camera_and_lighting()

    print("[6/6] Adding title card...")
    add_title_card()

    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
    print(f"[OK] .blend saved -> {OUTPUT_BLEND}")

    export_all()

    print()
    print("=" * 72)
    print("  ASSEMBLED CAD BUILD COMPLETE!")
    print()
    print("  Files generated:")
    print(f"    .blend -> {OUTPUT_BLEND}")
    print(f"    .stl   -> {OUTPUT_STL}")
    print(f"    .obj   -> {OUTPUT_OBJ}")
    print()
    print("  ┌───────────────────────────────────────────────────────────┐")
    print("  │  CMD TO OPEN IN BLENDER GUI:                              │")
    print("  │                                                           │")
    print("  │  /home/akshaya/Downloads/blender-5.2.1-linux-x64/blender \\")
    print(f"  │      {OUTPUT_BLEND}  │")
    print("  └───────────────────────────────────────────────────────────┘")
    print("=" * 72)
    print()


main()
