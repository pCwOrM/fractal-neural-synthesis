import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set 1920x1080 figure at 150 DPI for ultra-crisp LinkedIn rendering
fig = plt.figure(figsize=(12.8, 7.2), dpi=150, facecolor='#080c14')
ax = fig.add_subplot(111)
ax.set_facecolor('#080c14')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# 1. Header Banner
header_rect = patches.FancyBboxPatch((3, 83), 94, 14, boxstyle="round,pad=1.2",
                                     fc='#0f172a', ec='#3b82f6', lw=2)
ax.add_patch(header_rect)

ax.text(5.5, 92.5, "ITOUCH SYSTEMS | R&D & FORMAL MATHEMATICS DISPATCH",
        ha='left', va='center', color='#38bdf8', fontsize=11, weight='bold', fontfamily='sans-serif')
ax.text(5.5, 86.8, "General Divisor Theorem (GDT): Lean 4 Machine Proof & Two-Way Bridge",
        ha='left', va='center', color='#ffffff', fontsize=12.5, weight='bold', fontfamily='sans-serif')

doi_badge = patches.FancyBboxPatch((76, 85.5), 19.5, 9.5, boxstyle="round,pad=0.5",
                                   fc='#064e3b', ec='#10b981', lw=1.2)
ax.add_patch(doi_badge)
ax.text(85.75, 91.5, "CERN ZENODO ARCHIVE",
        ha='center', va='center', color='#6ee7b7', fontsize=8.5, weight='bold', fontfamily='sans-serif')
ax.text(85.75, 87.5, "DOI: 10.5281/zenodo.23316070",
        ha='center', va='center', color='#ffffff', fontsize=8, weight='bold', fontfamily='sans-serif')

# 2. Left Box: Formal Verification & Core Theorems
box1 = patches.FancyBboxPatch((3, 30), 45.5, 50, boxstyle="round,pad=1.2",
                              fc='#0f172a', ec='#1e293b', lw=1.5)
ax.add_patch(box1)

ax.text(5.5, 76.5, "LEAN 4 MACHINE PROOF & THEOREM PARAMETERS", color='#38bdf8', fontsize=11, weight='bold')

# Metric 1: Exact Period
ax.text(6, 70.8, "1. Minimal Period & Radical Decomposition:", color='#94a3b8', fontsize=9.5)
b1 = patches.FancyBboxPatch((5.5, 61), 40.5, 8.5, boxstyle="round,pad=0.5",
                            fc='#064e3b', ec='#10b981', lw=1.2)
ax.add_patch(b1)
ax.text(25.75, 65.2, "d = rad(gcd(m, N)),  R = rad(N) / d\nT_min = m · R = lcm(m, rad(N))",
        ha='center', va='center', color='#6ee7b7', fontsize=10.5, weight='bold')

# Metric 2: Euler Correction
ax.text(6, 56.5, "2. Exact Euler Density Correction Factor:", color='#94a3b8', fontsize=9.5)
b2 = patches.FancyBboxPatch((5.5, 47), 40.5, 8.5, boxstyle="round,pad=0.5",
                            fc='#1e1b4b', ec='#6366f1', lw=1.2)
ax.add_patch(b2)
ax.text(25.75, 51.2, "C(N, m) = d / φ(d) = ∏ [p / (p - 1)]\n(p | gcd(m, N))",
        ha='center', va='center', color='#c7d2fe', fontsize=10.5, weight='bold')

# Metric 3: Dichotomy
ax.text(6, 42.5, "3. Exact Dichotomy & Solution Count:", color='#94a3b8', fontsize=9.5)
ax.text(6, 38.5, "• gcd(a, d) > 1 ⟹ S = ∅ (Inadmissible Branch / 0 Solutions)", color='#f87171', fontsize=9, weight='bold')
ax.text(6, 34.5, "• gcd(a, d) = 1 ⟹ Exactly φ(R) solutions per minimal period!", color='#34d399', fontsize=9, weight='bold')

# 3. Right Box: Two-Way Bridge & Infrastructure
box2 = patches.FancyBboxPatch((51.5, 30), 45.5, 50, boxstyle="round,pad=1.2",
                              fc='#0f172a', ec='#1e293b', lw=1.5)
ax.add_patch(box2)

ax.text(54, 76.5, "TWO-WAY VALIDATION BRIDGE (VolkanBridge.lean)", color='#38bdf8', fontsize=11, weight='bold')

ax.text(54, 70.8, "thinkthoughts (Dan) Collaboration & Cross-Validation:", color='#94a3b8', fontsize=9.5)
b3 = patches.FancyBboxPatch((53.5, 59.5), 41.5, 10, boxstyle="round,pad=0.5",
                            fc='#312e81', ec='#818cf8', lw=1.2)
ax.add_patch(b3)
ax.text(74.25, 64.5, "Volkan Dağlı API  ⟷  Dan Hawkley Spec\nVolkanBridge.lean (0 SORRY)\nCanonical Isomorphisms & Axiom Discharge",
        ha='center', va='center', color='#e0e7ff', fontsize=10, weight='bold')

# Verification Telemetry
ax.text(54, 55, "Verification Oracle & Proof Telemetry:", color='#94a3b8', fontsize=9.5)
b4 = patches.FancyBboxPatch((53.5, 45), 41.5, 9, boxstyle="round,pad=0.5",
                            fc='#022c22', ec='#059669', lw=1.2)
ax.add_patch(b4)
ax.text(74.25, 49.5, "6,670+ Parameter Triples  |  6,552 Simulations\n100% PASS  |  0 DEFECTS  |  0 SORRY",
        ha='center', va='center', color='#a7f3d0', fontsize=10.5, weight='bold')

ax.text(54, 38.5, "Computing Infrastructure: ITouch Systems R&D", color='#fbbf24', fontsize=9.5, weight='bold')
ax.text(54, 34.5, "Authors: Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı", color='#cbd5e1', fontsize=9)

# 4. Bottom Footer
footer_rect = patches.FancyBboxPatch((3, 3), 94, 23.5, boxstyle="round,pad=1.2",
                                     fc='#0f172a', ec='#1e293b', lw=1.5)
ax.add_patch(footer_rect)

ax.text(5.5, 22.5, "METADATA, LICENSING & ACADEMIC IMPRINT", color='#38bdf8', fontsize=10.5, weight='bold')
ax.text(5.5, 17, "• Archival Preprint: Machine-Certified Lean 4 Formalization of the General Divisor Theorem (Draft v3.3)",
        color='#e2e8f0', fontsize=9)
ax.text(5.5, 12.5, "• CERN Zenodo Permanent DOI: 10.5281/zenodo.23316070  |  DataCite Registered  |  Apache-2.0 / CC-BY-4.0",
        color='#38bdf8', fontsize=9)
ax.text(5.5, 8, "• Open Repositories: github.com/pCwOrM/general-divisor-theorem  &  thinkthoughts/gap-lean4-port-gdt",
        color='#94a3b8', fontsize=9)

plt.tight_layout()
plt.savefig("itouch_linkedin_gdt_card_en.png", dpi=150, facecolor='#080c14')
plt.close()
print("SUCCESS: itouch_linkedin_gdt_card_en.png created successfully!")
