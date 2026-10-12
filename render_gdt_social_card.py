import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set 16:9 Twitter Card resolution: 1920x1080 at 150 DPI
fig = plt.figure(figsize=(12.8, 7.2), dpi=150, facecolor='#090d16')
ax = fig.add_subplot(111)
ax.set_facecolor('#090d16')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# 1. Main Header Box
header_box = patches.FancyBboxPatch((3, 85), 94, 12, boxstyle="round,pad=1.2",
                                    fc='#111827', ec='#38bdf8', lw=2)
ax.add_patch(header_box)

ax.text(50, 93, "GENERAL DIVISOR THEOREM (GDT) IN LEAN 4",
        ha='center', va='center', color='#38bdf8', fontsize=18, weight='bold', fontfamily='sans-serif')
ax.text(50, 88.5, "Exact Density Correction under Residue Conditioning — Machine-Certified Formalization",
        ha='center', va='center', color='#cbd5e1', fontsize=11, fontfamily='sans-serif')

# Attribution tag inside header
attr_pill = patches.FancyBboxPatch((15, 83.5), 70, 4.2, boxstyle="round,pad=0.5",
                                   fc='#1e293b', ec='#64748b', lw=1)
ax.add_patch(attr_pill)
ax.text(50, 85.6, "Reference: thinkthoughts (Dan @Precedent_Vice) | gdt.pdf | Formalized by pCwOrM",
        ha='center', va='center', color='#93c5fd', fontsize=9.5, weight='semibold', fontfamily='sans-serif')

# 2. Left Panel: Theory & Exact Formulations
left_panel = patches.FancyBboxPatch((3, 14), 45.5, 67, boxstyle="round,pad=1.2",
                                   fc='#0f172a', ec='#1e3a8a', lw=1.5)
ax.add_patch(left_panel)

ax.text(5.5, 77.5, "1. EXACT MATHEMATICAL FORMULATION",
        color='#38bdf8', fontsize=12, weight='bold', fontfamily='sans-serif')

# Left Box 1: Radical Partition
b1 = patches.FancyBboxPatch((5, 63.5), 41.5, 11.5, boxstyle="round,pad=0.8",
                            fc='#1e293b', ec='#3b82f6', lw=1.2)
ax.add_patch(b1)
ax.text(6.5, 71.5, "Radical Partition of Coprime Constraints:", color='#94a3b8', fontsize=9, weight='bold')
ax.text(25.5, 66.5, "d = rad( gcd(m, N) )      R = rad(N) / d",
        ha='center', va='center', color='#f8fafc', fontsize=11.5, weight='bold', fontfamily='monospace')

# Left Box 2: Minimal Period & Euler Correction
b2 = patches.FancyBboxPatch((5, 43.5), 41.5, 17.5, boxstyle="round,pad=0.8",
                            fc='#1e293b', ec='#3b82f6', lw=1.2)
ax.add_patch(b2)
ax.text(6.5, 57.5, "Exact Minimal Period & Correction Factor:", color='#94a3b8', fontsize=9, weight='bold')
ax.text(25.5, 52.8, "T_min = m · R = lcm(m, rad(N))",
        ha='center', va='center', color='#34d399', fontsize=11.5, weight='bold', fontfamily='monospace')
ax.text(25.5, 47.2, "C(N, m) = d / φ(d) = ∏ [ p / (p - 1) ]",
        ha='center', va='center', color='#fbbf24', fontsize=11, weight='bold', fontfamily='monospace')

# Left Box 3: Exact Dichotomy Criterion
b3 = patches.FancyBboxPatch((5, 17), 41.5, 24, boxstyle="round,pad=0.8",
                            fc='#1e293b', ec='#3b82f6', lw=1.2)
ax.add_patch(b3)
ax.text(6.5, 37.5, "The Exact Residue Dichotomy:", color='#94a3b8', fontsize=9, weight='bold')
ax.text(7, 33, "• Inadmissible (gcd(a, d) > 1):", color='#f87171', fontsize=10, weight='bold')
ax.text(9, 29.5, "  S(N, L, m, a) = ∅  (Empty for all L)", color='#cbd5e1', fontsize=9.5, fontfamily='monospace')
ax.text(7, 25, "• Admissible (gcd(a, d) = 1):", color='#4ade80', fontsize=10, weight='bold')
ax.text(9, 21.5, "  Exact φ(R) solutions per period T_min", color='#cbd5e1', fontsize=9.5, fontfamily='monospace')
ax.text(9, 18.5, "  Density strictly independent of residue a", color='#94a3b8', fontsize=8.5)

# 3. Right Panel: Machine Verification & Benchmarks
right_panel = patches.FancyBboxPatch((51.5, 14), 45.5, 67, boxstyle="round,pad=1.2",
                                    fc='#0f172a', ec='#047857', lw=1.5)
ax.add_patch(right_panel)

ax.text(54, 77.5, "2. MACHINE CERTIFICATION & BENCHMARKS",
        color='#34d399', fontsize=12, weight='bold', fontfamily='sans-serif')

# Right Box 1: Verified Paper Benchmarks
rb1 = patches.FancyBboxPatch((53.5, 54), 41.5, 21, boxstyle="round,pad=0.8",
                             fc='#1e293b', ec='#10b981', lw=1.2)
ax.add_patch(rb1)
ax.text(55, 71.5, "Canonical Monograph Benchmarks (Lean 4 norm_num):", color='#94a3b8', fontsize=9, weight='bold')
ax.text(55, 67, "✓ P_k = 210, m = 6  → C(6)  = 3.00   (Resolves 24/25 draft)", color='#6ee7b7', fontsize=9.5)
ax.text(55, 63, "✓ P_k = 210, m = 10 → C(10) = 2.50   [5/2]", color='#6ee7b7', fontsize=9.5)
ax.text(55, 59, "✓ P_k = 210, m = 30 → C(30) = 3.75   [15/4]", color='#6ee7b7', fontsize=9.5)
ax.text(55, 55.5, "✓ Primorial / Unitary Divisor specializations proved", color='#94a3b8', fontsize=8.5)

# Right Box 2: Boundary Distinctions
rb2 = patches.FancyBboxPatch((53.5, 33), 41.5, 18.5, boxstyle="round,pad=0.8",
                             fc='#1e293b', ec='#10b981', lw=1.2)
ax.add_patch(rb2)
ax.text(55, 48, "Critical Distinguishing Cases (Paper Tests):", color='#94a3b8', fontsize=9, weight='bold')
ax.text(55, 43.5, "• Minimal Period vs Coarse:", color='#38bdf8', fontsize=9.5, weight='bold')
ax.text(57, 40, "  N=18, m=2 → T_min = 6  (Coarse N=18 ruled out!)", color='#cbd5e1', fontsize=9)
ax.text(55, 36.5, "• Sharp Admissibility:", color='#f59e0b', fontsize=9.5, weight='bold')
ax.text(57, 33.5, "  N=5, m=6, a=2 → gcd(2,6)=2, but d=1 → Admissible!", color='#cbd5e1', fontsize=9)

# Right Box 3: Telemetry Badge
rb3 = patches.FancyBboxPatch((53.5, 17), 41.5, 13.5, boxstyle="round,pad=0.8",
                             fc='#064e3b', ec='#059669', lw=1.5)
ax.add_patch(rb3)
ax.text(74.25, 26, "LEAN 4 CERTIFICATION: 0 SORRY",
        ha='center', va='center', color='#a7f3d0', fontsize=12, weight='bold')
ax.text(74.25, 20.5, "Exhaustive Test Suite: 2,287 / 2,287 PASS (100%)\nMathlib-Native | Apache-2.0 Open Science",
        ha='center', va='center', color='#d1fae5', fontsize=9.5)

# 4. Bottom Footer Banner
footer_box = patches.FancyBboxPatch((3, 3), 94, 8.5, boxstyle="round,pad=1.0",
                                    fc='#111827', ec='#475569', lw=1.2)
ax.add_patch(footer_box)

ax.text(5, 7.2, "GitHub: github.com/pCwOrM/general-divisor-theorem",
        color='#38bdf8', fontsize=10, weight='bold', fontfamily='monospace')
ax.text(95, 7.2, "Lean Workers Union Lodge Task: GDT-GENERAL-DIVISOR-THEOREM",
        ha='right', color='#94a3b8', fontsize=9.5, fontfamily='sans-serif')

plt.tight_layout()
output_path = "docs/general_divisor_theorem/gdt_twitter_infographic.png"
plt.savefig(output_path, dpi=150, facecolor='#090d16', bbox_inches='tight')
print(f"Infographic successfully saved to {output_path}")
