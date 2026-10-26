import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('deck_assets', exist_ok=True)

# Common styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------
# Chart 1: Latency & Gas Comparison (Werracle vs ZK-ML vs Oracles vs Heuristics)
# -------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(9, 4.8), dpi=300)
fig.patch.set_facecolor('#0f172a')
ax1.set_facecolor('#0f172a')

solutions = ['Werracle Reflex\n(Procedural WERR)', 'ZK-ML Oracle\n(Modulus / EZKL)', 'Pull Oracle\n(Pyth Network)', 'Push Oracle\n(Chainlink Data Feeds)', 'Static Heuristics\n(Hard-coded Rules)']
gas_costs = [20.7, 450.0, 115.0, 85.0, 12.0] # in kGas
latencies = [0.012, 35.0, 2.5, 60.0, 0.005] # in seconds

x = np.arange(len(solutions))
width = 0.35

bars1 = ax1.bar(x - width/2, gas_costs, width, label='Gas Cost (kGas)', color='#38bdf8', edgecolor='#0284c7', alpha=0.9)
ax1.set_ylabel('EVM Execution Gas (kGas)', color='#38bdf8', fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#38bdf8')
ax1.set_yscale('log')
ax1.set_ylim(5, 1000)

ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, latencies, width, label='Execution Latency (sec)', color='#f43f5e', edgecolor='#e11d48', alpha=0.85)
ax2.set_ylabel('Execution Latency (Seconds, Log Scale)', color='#f43f5e', fontsize=11, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#f43f5e')
ax2.set_yscale('log')
ax2.set_ylim(0.001, 150)

ax1.set_xticks(x)
ax1.set_xticklabels(solutions, fontsize=9.5, fontweight='bold', color='#f8fafc')
ax1.grid(True, linestyle='--', alpha=0.15, color='#94a3b8', axis='y')

# Value annotations
for bar in bars1:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h * 1.15, f'{h:.1f}k',
             ha='center', va='bottom', color='#38bdf8', fontsize=8.5, fontweight='bold')

for bar in bars2:
    h = bar.get_height()
    lbl = f'{h*1000:.0f}ms' if h < 1 else f'{h:.1f}s'
    ax2.text(bar.get_x() + bar.get_width()/2., h * 1.25, lbl,
             ha='center', va='bottom', color='#f43f5e', fontsize=8.5, fontweight='bold')

plt.title('Execution Gas & Latency: Werracle vs Alternative Decision Engines',
          color='#f8fafc', fontsize=13, fontweight='bold', pad=15)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', framealpha=0.2, facecolor='#1e293b', labelcolor='#f8fafc')

plt.tight_layout()
plt.savefig('deck_assets/chart_latency_gas_comparison_en.png', facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Saved chart_latency_gas_comparison_en.png")

# -------------------------------------------------------------
# Chart 2: Werracle Ecosystem Map (High-contrast flow breakdown)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')

# We create an informative, clean multi-layer stack visualization
categories = ['werracle.io\n(On-Chain Protocol)', 'radar.werracle.com\n(Risk Telemetry DaaS)', 'werracle.com\n(Enterprise & SLA)', 'werr.io\n(Scientific Core)']
layers = ['Formal Proofs / Core IP', 'Execution Latency', 'Revenue Engine', 'Target Audience']

# Data matrix representation: Score / Capability rating (1 to 5)
matrix = np.array([
    [5, 4, 3, 5], # werracle.io
    [4, 5, 5, 2], # radar.werracle.com
    [3, 3, 5, 2], # werracle.com
    [5, 2, 2, 5]  # werr.io
])

# Stacked metrics display
y_pos = np.arange(len(categories))
bar_h = 0.55

# Color map
colors = ['#38bdf8', '#34d399', '#f59e0b', '#a855f7']
labels = ['Protocol Defense (Hooks & Breakers)', 'Real-Time DaaS & OEV Radar', 'Curator SLA & IP Licensing', 'Lean 4 Proofs & Academic Base']

b1 = ax.barh(y_pos, [95, 20, 10, 5], bar_h, label='On-Chain Execution Weight', color='#38bdf8', alpha=0.85)
b2 = ax.barh(y_pos, [10, 90, 15, 5], bar_h, left=[95, 20, 10, 5], label='Off-Chain Telemetry Weight', color='#34d399', alpha=0.85)
b3 = ax.barh(y_pos, [5, 15, 80, 5], bar_h, left=[105, 110, 25, 10], label='Enterprise / SLA Weight', color='#f59e0b', alpha=0.85)
b4 = ax.barh(y_pos, [10, 10, 10, 95], bar_h, left=[110, 125, 105, 15], label='Mathematical Rigor Weight', color='#a855f7', alpha=0.85)

ax.set_yticks(y_pos)
ax.set_yticklabels(categories, color='#f8fafc', fontsize=10, fontweight='bold')
ax.set_xlabel('Product Capability & Focus Allocation (%)', color='#94a3b8', fontsize=11, fontweight='bold')
ax.tick_params(axis='x', labelcolor='#94a3b8')
ax.set_xlim(0, 130)
ax.grid(True, linestyle='--', alpha=0.15, color='#94a3b8', axis='x')

plt.title('The Unified Werracle Product Stack: Synergistic Architecture',
          color='#f8fafc', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='lower right', framealpha=0.3, facecolor='#1e293b', labelcolor='#f8fafc', fontsize=8.5)

plt.tight_layout()
plt.savefig('deck_assets/chart_werracle_ecosystem_en.png', facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Saved chart_werracle_ecosystem_en.png")

# -------------------------------------------------------------
# Chart 3: Product ARR Projections (2026 - 2029) by Revenue Stream
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')

years = ['2026 (Live)', '2027 (Scale)', '2028 (Expansion)', '2029 (Maturity)']
radar_arr = [0.12, 0.65, 1.85, 3.20]       # Million $ (DaaS subscriptions)
hook_arr  = [0.05, 0.50, 1.60, 2.70]       # Million $ (Protocol hooks, fee split)
enterprise_arr = [0.07, 0.45, 0.95, 1.50] # Million $ (Curator SLA & IP licenses)

x = np.arange(len(years))
width = 0.50

p1 = ax.bar(x, radar_arr, width, label='Radar DaaS Subscriptions (USDC)', color='#38bdf8', edgecolor='#0284c7', alpha=0.9)
p2 = ax.bar(x, hook_arr, width, bottom=radar_arr, label='Protocol Hook Royalties (bps)', color='#34d399', edgecolor='#059669', alpha=0.9)
bottom_tot = np.array(radar_arr) + np.array(hook_arr)
p3 = ax.bar(x, enterprise_arr, width, bottom=bottom_tot, label='Curator SLA & Enterprise Licensing', color='#a855f7', edgecolor='#7e22ce', alpha=0.9)

total_arr = bottom_tot + np.array(enterprise_arr)

for i, tot in enumerate(total_arr):
    ax.text(i, tot + 0.15, f'${tot:.2f}M', ha='center', va='bottom', color='#f8fafc', fontsize=10, fontweight='bold')

ax.set_ylabel('Annual Recurring Revenue ($ Millions)', color='#f8fafc', fontsize=11, fontweight='bold')
ax.tick_params(axis='y', labelcolor='#94a3b8')
ax.set_xticks(x)
ax.set_xticklabels(years, color='#f8fafc', fontsize=10.5, fontweight='bold')
ax.set_ylim(0, 8.5)
ax.grid(True, linestyle='--', alpha=0.15, color='#94a3b8', axis='y')

plt.title('Werracle Consolidated ARR Projection: Multi-Engine Growth ($M)',
          color='#f8fafc', fontsize=13, fontweight='bold', pad=15)
ax.legend(loc='upper left', framealpha=0.25, facecolor='#1e293b', labelcolor='#f8fafc', fontsize=9)

plt.tight_layout()
plt.savefig('deck_assets/chart_product_arr_projection_en.png', facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Saved chart_product_arr_projection_en.png")

# -------------------------------------------------------------
# Chart 4: Seed Fund Allocation ($1.5M Round)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')

allocations = [40, 25, 20, 15]
labels = [
    'Core Protocol & Hook Engineering\n($600k - 40%)\nEVM, Cairo Sierra, Monad',
    'DeFi BD & Protocol Partnerships\n($375k - 25%)\nTop 15 Protocol Integrations',
    'Security Audits & Node Infra\n($300k - 20%)\nFormal Verification & Low-Latency Bare Metal',
    'Legal, IP & Corporate Operations\n($225k - 15%)\nGlobal IP, W-8BEN-E & US Entity'
]
colors = ['#38bdf8', '#34d399', '#a855f7', '#f59e0b']
explode = (0.05, 0.02, 0.02, 0.02)

wedges, texts, autotexts = ax.pie(
    allocations,
    explode=explode,
    labels=labels,
    colors=colors,
    autopct='%1.0f%%',
    pctdistance=0.8,
    startangle=140,
    textprops={'color': '#f8fafc', 'fontsize': 8.8, 'fontweight': 'bold'},
    wedgeprops={'edgecolor': '#0f172a', 'linewidth': 2}
)

for autotext in autotexts:
    autotext.set_color('#0f172a')
    autotext.set_fontweight('heavy')
    autotext.set_fontsize(10)

plt.title('Use of Funds: $1,500,000 Seed Round (18-Month Runway)',
          color='#f8fafc', fontsize=13, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('deck_assets/chart_fund_allocation_werracle_en.png', facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Saved chart_fund_allocation_werracle_en.png")
