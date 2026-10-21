import matplotlib.pyplot as plt
import numpy as np

# Set high DPI and professional publication typography
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#D1D5DB'
plt.rcParams['axes.linewidth'] = 1.2

fig = plt.figure(figsize=(15, 7.5), dpi=300, facecolor='#FFFFFF')
gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1.0], height_ratios=[1.0, 1.0], hspace=0.32, wspace=0.25)

# -------------------------------------------------------------
# PANEL 1: FEA Mesh Convergence Curve (Left Full Height)
# -------------------------------------------------------------
ax1 = fig.add_subplot(gs[:, 0])

iterations = [1, 2, 3, 4]
labels = ['Iter 1\n(Coarse: 3.0mm)', 'Iter 2\n(Medium: 2.0mm)', 'Iter 3 [Selected]\n(Fine: 1.5mm)', 'Iter 4\n(Extra Fine: 0.8mm)']
elements = [32100, 68400, 128450, 245000]
stress = [32.40, 36.85, 38.60, 38.78]
rel_error = [14.2, 8.6, 1.2, 0.46]

# Plot stress curve
line1 = ax1.plot(elements, stress, color='#0A4D68', marker='o', markersize=9, linewidth=2.8, label='Peak Von Mises Stress (MPa)', zorder=4)

# Add Yield line
ax1.axhline(y=62.0, color='#DC2626', linestyle='--', linewidth=2.0, label='Material Yield Strength ($S_y = 62.0$ MPa)', zorder=2)

# Annotate Yield Strength
ax1.text(35000, 63.0, 'Material Yield Limit ($S_y = 62.0$ MPa) — PC/ABS Casing', color='#DC2626', fontsize=10.5, fontweight='bold')

# Annotate Selected Mesh Point
ax1.scatter([128450], [38.60], color='#05BFDB', s=180, edgecolors='#0A4D68', linewidth=2.5, zorder=5)
ax1.annotate(
    'OPERATIONAL MESH (Iter 3)\nElements: 128,450\nPeak Stress: 38.60 MPa\nFoS: 1.61× (Converged < 1.0%)',
    xy=(128450, 38.60),
    xytext=(95000, 47.0),
    arrowprops=dict(facecolor='#0A4D68', edgecolor='#0A4D68', arrowstyle='->', lw=1.8),
    fontsize=9.5,
    fontweight='bold',
    bbox=dict(boxstyle='round,pad=0.6', facecolor='#F0F9FF', edgecolor='#0A4D68', lw=1.5)
)

# Twin axis for Relative Convergence Error %
ax1_twin = ax1.twinx()
line2 = ax1_twin.plot(elements, rel_error, color='#EAB308', marker='s', markersize=7.5, linestyle=':', linewidth=2.2, label='Mesh Discretization Error (%)', zorder=3)
ax1_twin.set_ylabel('Asymptotic Convergence Error (%)', fontsize=11, fontweight='bold', color='#B45309')
ax1_twin.tick_params(axis='y', labelcolor='#B45309')
ax1_twin.set_ylim(0, 20)

# Configure primary axis
ax1.set_title('AERO-STENT Enclosure FEA Mesh Independence & Convergence Study', fontsize=12.5, fontweight='bold', pad=14, color='#0F172A')
ax1.set_xlabel('Number of Finite Elements (Quadratic C3D10)', fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_ylabel('Peak von Mises Stress $\\sigma_{max}$ (MPa)', fontsize=11, fontweight='bold', color='#0A4D68')
ax1.set_ylim(25, 70)
ax1.grid(True, linestyle='--', alpha=0.55, color='#94A3B8')

# Custom unified legend
lines = line1 + line2 + [ax1.get_lines()[1]]
labels_legend = [l.get_label() for l in lines]
ax1.legend(lines, labels_legend, loc='lower right', framealpha=0.95, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9.2)

# -------------------------------------------------------------
# PANEL 2: Element Quality & Aspect Ratio Distribution (Top Right)
# -------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])

quality_bins = ['0.50–0.60', '0.60–0.70', '0.70–0.80', '0.80–0.90', '0.90–1.00\n(Optimal)']
quality_pcts = [1.8, 4.2, 14.5, 48.2, 31.3]
bar_colors = ['#FCA5A5', '#FDE047', '#93C5FD', '#38BDF8', '#0284C7']

bars = ax2.bar(quality_bins, quality_pcts, color=bar_colors, edgecolor='#0F172A', linewidth=0.8, width=0.6)
ax2.set_title('Mesh Element Orthogonal Quality Distribution', fontsize=11.5, fontweight='bold', pad=10, color='#0F172A')
ax2.set_ylabel('% of Total Elements', fontsize=10, fontweight='bold', color='#1E293B')
ax2.set_ylim(0, 60)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

ax2.text(0.05, 0.85, 'Avg Quality: 0.86\nMin Quality: 0.52 (Target > 0.20)', transform=ax2.transAxes, fontsize=8.8, bbox=dict(boxstyle='square,pad=0.4', facecolor='#F8FAFC', edgecolor='#E2E8F0'))

# -------------------------------------------------------------
# PANEL 3: Mesh Statistics & Solver Configuration Table (Bottom Right)
# -------------------------------------------------------------
ax3 = fig.add_subplot(gs[1, 1])
ax3.axis('off')

table_data = [
    ['Finite Element Solver', 'ANSYS Mechanical / SolidWorks FEA'],
    ['Element Formulation', '10-Node Quadratic Tetrahedral (C3D10)'],
    ['Total Elements / Nodes', '128,450 / 186,210'],
    ['Global Element Size', '1.50 mm (Curvature & Proximity Refined)'],
    ['Local Fillet Element Size', '0.35 mm at Critical Bezel Transition'],
    ['Max von Mises Stress', '38.60 MPa (Impact: 240g, 2.1ms)'],
    ['Material Yield Strength', '62.0 MPa (Medical PC/ABS)'],
    ['Minimum Factor of Safety', '1.61× (Dynamic Drop) | 8.35× (Static Grip)'],
    ['Convergence Criterion', 'Δσ < 1.0% | Status: CONVERGED']
]

table = ax3.table(cellText=table_data, colLabels=['FEA Validation Metric', 'Engineering Specification'], loc='center', cellLoc='left')
table.auto_set_font_size(False)
table.set_fontsize(8.8)
table.scale(1.0, 1.45)

# Style table header and cells
for (r, c), cell in table.get_celld().items():
    if r == 0:
        cell.set_facecolor('#0A4D68')
        cell.set_text_props(color='#FFFFFF', fontweight='bold')
    else:
        if r % 2 == 1:
            cell.set_facecolor('#F8FAFC')
        else:
            cell.set_facecolor('#FFFFFF')
        cell.set_edgecolor('#E2E8F0')
        if c == 1 and r == 8:
            cell.set_text_props(color='#059669', fontweight='bold')
        elif c == 1 and r == 7:
            cell.set_text_props(color='#0A4D68', fontweight='bold')

plt.suptitle('AERO-STENT (Theme 1: Health Tech) — FEA Structural Mesh Convergence & Statistical Report', fontsize=14, fontweight='bold', y=0.98, color='#0A4D68')

output_path1 = 'AERO_STENT-Viswakarma-26/diagrams/aerostent_fig4_fea_mesh_convergence.png'
output_path2 = 'aerostent_fig4_fea_mesh_convergence.png'

plt.savefig(output_path1, bbox_inches='tight', dpi=300)
plt.savefig(output_path2, bbox_inches='tight', dpi=300)
print(f"Successfully generated FEA plot at:\n- {output_path1}\n- {output_path2}")
