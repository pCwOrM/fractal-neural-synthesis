import os
import matplotlib.pyplot as plt
import numpy as np

# Set dark tech aesthetic style for matplotlib
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'Segoe UI, Helvetica, Arial'
plt.rcParams['font.family'] = 'sans-serif'

CHARTS_DIR = os.path.join(os.getcwd(), "deck_assets")
os.makedirs(CHARTS_DIR, exist_ok=True)

BG_COLOR = "#0f172a"      # slate-900
CARD_BG = "#1e293b"       # slate-800
TEXT_COLOR = "#f8fafc"    # slate-50
ACCENT_BLUE = "#38bdf8"   # sky-400
ACCENT_GREEN = "#10b981"  # emerald-500
ACCENT_AMBER = "#f59e0b"  # amber-500
ACCENT_RED = "#ef4444"    # red-500
ACCENT_PURPLE = "#a855f7" # purple-500

# -------------------------------------------------------------
# 1. Chart: OEV Recapture on Base vs. Ethereum L1 Builder Payments
# -------------------------------------------------------------
def gen_chart_oev():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), facecolor=BG_COLOR)
    ax1.set_facecolor(CARD_BG)
    ax2.set_facecolor(CARD_BG)

    # Panel 1: Base SVR Recapture
    sizes1 = [94.38, 5.58]
    labels1 = ['Protocol & Chainlink\nRecaptured (94.38%)', 'Solver Gross\nMargin (5.58%)']
    colors1 = [ACCENT_GREEN, ACCENT_BLUE]
    explode1 = (0.05, 0)
    wedges1, texts1, autotexts1 = ax1.pie(
        sizes1, explode=explode1, labels=labels1, colors=colors1, autopct='%1.1f%%',
        startangle=140, pctdistance=0.75,
        textprops=dict(color=TEXT_COLOR, fontsize=11, weight='bold'),
        wedgeprops=dict(width=0.45, edgecolor=BG_COLOR, linewidth=2)
    )
    for at in autotexts1:
        at.set_color('#ffffff')
        at.set_fontsize(13)
    ax1.set_title("Base Mainnet: Chainlink SVR (105 Tx)\n$190.5k Liquidation Incentive", color=TEXT_COLOR, fontsize=12, pad=15, weight='bold')

    # Panel 2: Ethereum L1 Fat-Tail Concentration
    sizes2 = [95.94, 4.06]
    labels2 = ['Top 22 Transactions\n($351.3k - 95.9%)', 'Remaining 1,027 Tx\n($14.8k - 4.1%)']
    colors2 = [ACCENT_RED, '#64748b']
    explode2 = (0.05, 0)
    wedges2, texts2, autotexts2 = ax2.pie(
        sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%',
        startangle=140, pctdistance=0.75,
        textprops=dict(color=TEXT_COLOR, fontsize=11, weight='bold'),
        wedgeprops=dict(width=0.45, edgecolor=BG_COLOR, linewidth=2)
    )
    for at in autotexts2:
        at.set_color('#ffffff')
        at.set_fontsize(13)
    ax2.set_title("Ethereum L1: Builder Payments (1,049 Tx)\n$366.1k Total Priority Fees", color=TEXT_COLOR, fontsize=12, pad=15, weight='bold')

    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "chart_oev_comparison.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 2. Chart: Live Parametric Shock Stress Curve (Steakhouse USDC)
# -------------------------------------------------------------
def gen_chart_stress():
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor=BG_COLOR)
    ax.set_facecolor(CARD_BG)

    shocks = ['0%\n(Current)', '-5%', '-10%', '-15%', '-20%', '-30%']
    liquidatable = [0.0, 9.98, 60.62, 131.17, 209.39, 496.06] # Millions USD
    bad_debt = [0.0, 0.0, 0.0, 0.17, 2.41, 21.66]           # Millions USD

    x = np.arange(len(shocks))
    width = 0.38

    rects1 = ax.bar(x - width/2, liquidatable, width, label='Liquidatable Debt ($M)', color=ACCENT_BLUE, edgecolor='none', alpha=0.9)
    rects2 = ax.bar(x + width/2, bad_debt, width, label='Market Bad Debt ($M)', color=ACCENT_RED, edgecolor='none', alpha=0.9)

    ax.set_ylabel('Volume in Millions USD ($M)', color=TEXT_COLOR, fontsize=11, weight='bold')
    ax.set_title('Steakhouse USDC Live Allocation: Stress Test Shock Scenarios\n($116.2M Vault TVL Across 5 Base Collateral Markets)', color=TEXT_COLOR, fontsize=12, weight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(shocks, color=TEXT_COLOR, fontsize=10)
    ax.tick_params(colors=TEXT_COLOR)
    ax.grid(axis='y', linestyle='--', alpha=0.2, color='#94a3b8')

    for rect in rects1:
        h = rect.get_height()
        if h > 5:
            ax.annotate(f'${h:.1f}M', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                        textcoords="offset points", ha='center', va='bottom', color='#38bdf8', fontsize=9, weight='bold')
    for rect in rects2:
        h = rect.get_height()
        if h > 0.1:
            ax.annotate(f'${h:.1f}M', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                        textcoords="offset points", ha='center', va='bottom', color='#f87171', fontsize=9, weight='bold')

    ax.legend(facecolor=BG_COLOR, edgecolor='#334155', labelcolor=TEXT_COLOR, fontsize=10)
    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "chart_stress_curve.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 3. Chart: ARR & Subscriber Growth Projections (2027 - 2029)
# -------------------------------------------------------------
def gen_chart_financials():
    fig, ax1 = plt.subplots(figsize=(9, 4.5), facecolor=BG_COLOR)
    ax1.set_facecolor(CARD_BG)

    years = ['Year 1 (2027)', 'Year 2 (2028)', 'Year 3 (2029)']
    arr = [364.26, 1373.46, 3822.24] # in Thousands ($k)
    pro_subs = [120, 450, 1200]
    inst_subs = [25, 95, 280]

    x = np.arange(len(years))
    width = 0.45

    bars = ax1.bar(x, arr, width, label='ARR ($k USD)', color=ACCENT_GREEN, alpha=0.85, edgecolor='none')
    ax1.set_ylabel('Annual Run-Rate ARR ($k USD)', color=ACCENT_GREEN, fontsize=11, weight='bold')
    ax1.tick_params(axis='y', labelcolor=ACCENT_GREEN)
    ax1.tick_params(axis='x', labelcolor=TEXT_COLOR, labelsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, weight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.2, color='#94a3b8')

    for bar in bars:
        h = bar.get_height()
        val_str = f"${h/1000:.2f}M" if h >= 1000 else f"${h:.0f}k"
        ax1.annotate(val_str, xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 5),
                    textcoords="offset points", ha='center', va='bottom', color='#34d399', fontsize=11, weight='bold')

    # Secondary axis for total paid institutions/users
    ax2 = ax1.twinx()
    total_clients = [p + i for p, i in zip(pro_subs, inst_subs)]
    line = ax2.plot(x, total_clients, color=ACCENT_AMBER, marker='o', linewidth=2.5, markersize=8, label='Total Paid Subscribers')
    ax2.set_ylabel('Active Paid Subscribers', color=ACCENT_AMBER, fontsize=11, weight='bold')
    ax2.tick_params(axis='y', labelcolor=ACCENT_AMBER)
    ax2.set_ylim(0, 1600)

    for i, txt in enumerate(total_clients):
        ax2.annotate(f"{txt} Clients\n({inst_subs[i]} Inst.)", xy=(x[i], txt), xytext=(0, 10),
                    textcoords="offset points", ha='center', color=ACCENT_AMBER, fontsize=9, weight='bold')

    ax1.set_title('3-Year Financial Projections: ARR & Subscriber Scaling\n(88% Average Gross Margin, 12.4x LTV/CAC)',
                  color=TEXT_COLOR, fontsize=12, weight='bold', pad=15)

    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "chart_arr_projection.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")

# -------------------------------------------------------------
# 4. Chart: Use of Funds ($1.5M Seed Allocation)
# -------------------------------------------------------------
def gen_chart_use_of_funds():
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=BG_COLOR)
    ax.set_facecolor(CARD_BG)

    sizes = [40, 25, 20, 15]
    labels = [
        'Core Engineering & Protocol Decoders\n($600k - 40%)',
        'Infrastructure & Dedicated Archive RPCs\n($375k - 25%)',
        'Curator BD & Institutional Partnerships\n($300k - 20%)',
        'Security Audits, Compliance & Legal\n($225k - 15%)'
    ]
    colors = [ACCENT_BLUE, ACCENT_GREEN, ACCENT_AMBER, ACCENT_PURPLE]
    explode = (0.04, 0.04, 0.04, 0.04)

    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors, autopct='%1.0f%%',
        startangle=130, pctdistance=0.75,
        textprops=dict(color=TEXT_COLOR, fontsize=10, weight='bold'),
        wedgeprops=dict(width=0.45, edgecolor=BG_COLOR, linewidth=2)
    )
    for at in autotexts:
        at.set_color('#ffffff')
        at.set_fontsize(12)

    ax.set_title("Use of Funds: $1,500,000 Seed Round\n18-Month Runway to $1.3M+ ARR", color=TEXT_COLOR, fontsize=12, pad=12, weight='bold')

    plt.tight_layout()
    out_path = os.path.join(CHARTS_DIR, "chart_use_of_funds.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    gen_chart_oev()
    gen_chart_stress()
    gen_chart_financials()
    gen_chart_use_of_funds()
    print("All charts generated successfully.")
