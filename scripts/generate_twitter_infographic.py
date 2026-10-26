import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('deck_assets', exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.0

# 1200 x 675 pixels (16:9 Twitter optimal card size) at 150 dpi -> 8 x 4.5 inches
fig = plt.figure(figsize=(10, 5.625), dpi=200)
fig.patch.set_facecolor('#070a12')

# Header Title
fig.text(0.06, 0.91, "EMPIRICAL OEV & LIQUIDATION VALUE RECAPTURE ON BASE",
         fontsize=15, fontweight='bold', color='#f8fafc', family='DejaVu Sans')
fig.text(0.06, 0.86, "Chainlink SVR & Morpho Blue Telemetry (October 2026 Sample | 105 Audited Multi-Call Tx)",
         fontsize=10.5, color='#38bdf8', family='DejaVu Sans')

# Top 4 KPI Boxes using annotations / patches
kpis = [
    ("94.38%", "SVR Recaptured", "$179.8k / $190.5k Gross", "#34d399"),
    ("98.30%", "Median Recapture", "Per-Transaction Median", "#38bdf8"),
    ("-1.55%", "Solver Margin", "Subzero / Gas Subsidized", "#c084fc"),
    ("95.94%", "L1 Top 22 Leak", "$351k / $366k Builder Bribe", "#fb7185")
]

for i, (metric, title, sub, col) in enumerate(kpis):
    x0 = 0.06 + i * 0.225
    y0 = 0.63
    w = 0.205
    h = 0.18
    rect = plt.Rectangle((x0, y0), w, h, transform=fig.transFigure,
                         facecolor='#0f172a', edgecolor=col, linewidth=1.5,
                         alpha=0.9, zorder=2)
    fig.patches.append(rect)
    fig.text(x0 + w/2, y0 + 0.105, metric, fontsize=19, fontweight='heavy',
             color=col, ha='center', va='center', family='DejaVu Sans')
    fig.text(x0 + w/2, y0 + 0.055, title, fontsize=9.5, fontweight='bold',
             color='#f8fafc', ha='center', va='center')
    fig.text(x0 + w/2, y0 + 0.02, sub, fontsize=7.5, color='#94a3b8',
             ha='center', va='center')

# Left Subplot: Value Destination Comparison (Base SVR vs L1)
ax1 = fig.add_axes([0.08, 0.15, 0.40, 0.40])
ax1.set_facecolor('#0f172a')

categories = ['Base SVR\n(105 Tx)', 'Ethereum L1\n(1,049 Tx)']
recaptured_shares = [94.38, 0.0]
leak_shares = [5.62, 95.94]

b1 = ax1.bar(categories, recaptured_shares, width=0.45, label='Protocol/Depositor Recapture (%)', color='#34d399', edgecolor='#059669', alpha=0.9)
b2 = ax1.bar(categories, leak_shares, width=0.45, bottom=recaptured_shares, label='Builder / Searcher Capture (%)', color='#f43f5e', edgecolor='#e11d48', alpha=0.9)

ax1.set_ylabel('Value Distribution (%)', color='#94a3b8', fontsize=9, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#94a3b8', labelsize=8)
ax1.tick_params(axis='x', labelcolor='#f8fafc', labelsize=9)
ax1.set_ylim(0, 115)
ax1.grid(True, linestyle='--', alpha=0.15, color='#94a3b8', axis='y')
ax1.legend(loc='upper center', fontsize=7.5, facecolor='#1e293b', edgecolor='#334155', labelcolor='#f8fafc')

ax1.text(0, 96, "94.38%\nRecaptured", ha='center', va='bottom', color='#34d399', fontsize=8.5, fontweight='bold')
ax1.text(1, 98, "95.94%\nTop 22 Leak", ha='center', va='bottom', color='#f43f5e', fontsize=8.5, fontweight='bold')
ax1.set_title('Recapture vs MEV Leakage', color='#f8fafc', fontsize=10.5, fontweight='bold', pad=8)

# Right Subplot: Monitored Debt & Health Factor
ax2 = fig.add_axes([0.56, 0.15, 0.38, 0.40])
ax2.set_facecolor('#0f172a')

stages = ['Clean Monitored\nDebt ($2.20B)', 'Filtered Spam\nDebt ($2.31B)', 'Near Liquidation\nDistress (HF<1.1)', 'Bad Debt\n(HF<0.95)']
values = [2198.0, 2313.0, 14.8, 0.0]
colors = ['#38bdf8', '#64748b', '#fbbf24', '#f43f5e']

bars = ax2.bar(stages, values, width=0.55, color=colors, edgecolor='#334155')
ax2.set_ylabel('Debt Volume ($M, Log Scale)', color='#94a3b8', fontsize=9, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#94a3b8', labelsize=8)
ax2.tick_params(axis='x', labelcolor='#f8fafc', labelsize=8)
ax2.set_yscale('log')
ax2.set_ylim(1, 5000)
ax2.grid(True, linestyle='--', alpha=0.15, color='#94a3b8', axis='y')

for b in bars:
    h = b.get_height()
    lbl = f"${h:,.0f}M" if h >= 10 else (f"${h:.1f}M" if h > 0 else "$0.0")
    ax2.text(b.get_x() + b.get_width()/2., max(h * 1.2, 1.2), lbl,
             ha='center', va='bottom', color='#f8fafc', fontsize=8, fontweight='bold')

ax2.set_title('Live Surveillance: 38 Verified Markets', color='#f8fafc', fontsize=10.5, fontweight='bold', pad=8)

# Footer Info
fig.text(0.06, 0.04, "Observatory: radar.werracle.com  |  Dataset v1.2: Hugging Face (CC-BY-4.0)  |  Preprint: arXiv:2609.30719",
         fontsize=8.5, color='#94a3b8', family='DejaVu Sans')
fig.text(0.94, 0.04, "ITouch Systems R&D", fontsize=8.5, color='#38bdf8', ha='right', fontweight='bold')

output_path = 'deck_assets/twitter_werracle_svr_infographic.png'
root_path = 'twitter_werracle_svr_infographic.png'
plt.savefig(output_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.savefig(root_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print(f"Generated {output_path} and {root_path}")
