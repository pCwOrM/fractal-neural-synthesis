import os
import base64
import shutil
from playwright.sync_api import sync_playwright

WORKSPACE = os.getcwd()
CHARTS_DIR = os.path.join(WORKSPACE, "deck_assets")
ARTIFACT_DIR = r"C:\Users\maat\.gemini\antigravity\brain\dda702fe-3efa-4434-83d5-3111cadb22cf"

def img_to_b64(filename):
    path = os.path.join(CHARTS_DIR, filename)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"

b64_oev = img_to_b64("chart_oev_comparison.png")
b64_stress = img_to_b64("chart_stress_curve.png")
b64_arr = img_to_b64("chart_arr_projection.png")
b64_funds = img_to_b64("chart_use_of_funds.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Werracle Radar - Investor Pitch Deck</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: 16in 9in;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    background: #090d16;
    color: #f8fafc;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .slide {{
    width: 16in;
    height: 9in;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 48px 64px;
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at top right, rgba(56, 189, 248, 0.08), transparent 40%),
                radial-gradient(circle at bottom left, rgba(16, 185, 129, 0.05), transparent 40%),
                #0b0f19;
  }}

  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 16px;
  }}

  .header-left {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .brand {{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  .category-pill {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 10px;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    border-radius: 999px;
  }}

  .header-title {{
    font-size: 14px;
    color: #94a3b8;
    font-weight: 500;
  }}

  .content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 24px 0;
  }}

  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 14px;
    font-size: 12px;
    color: #64748b;
  }}

  .footer a {{
    color: #38bdf8;
    text-decoration: none;
  }}

  /* Typography */
  h1.slide-title {{
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.15;
    margin-bottom: 12px;
    color: #ffffff;
  }}

  h2.slide-sub {{
    font-size: 18px;
    font-weight: 400;
    color: #94a3b8;
    margin-bottom: 24px;
    max-width: 90%;
  }}

  /* Cards & Layouts */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
    align-items: center;
  }}

  .grid-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }}

  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }}

  .card {{
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 24px;
    backdrop-filter: blur(10px);
  }}

  .card-highlight {{
    border-color: rgba(56, 189, 248, 0.35);
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
  }}

  .card-title {{
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .card-desc {{
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.5;
  }}

  .kpi-box {{
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
  }}

  .kpi-num {{
    font-size: 32px;
    font-weight: 800;
    color: #38bdf8;
    line-height: 1.1;
    font-family: 'JetBrains Mono', monospace;
  }}

  .kpi-label {{
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #94a3b8;
    margin-top: 6px;
  }}

  .chart-img {{
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  }}

  /* Tables */
  table.deck-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}

  table.deck-table th {{
    background: rgba(15, 23, 42, 0.95);
    color: #38bdf8;
    font-weight: 700;
    text-align: left;
    padding: 12px 16px;
    border-bottom: 2px solid rgba(56, 189, 248, 0.3);
  }}

  table.deck-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    color: #cbd5e1;
  }}

  table.deck-table tr:hover td {{
    background: rgba(56, 189, 248, 0.04);
  }}

  .tag-green {{
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
  }}

  .tag-blue {{
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
  }}

  .hero-tag {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    color: #38bdf8;
    margin-bottom: 18px;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: COVER -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">DeFi Risk Telemetry</div>
    </div>
    <div class="header-title">ITouch Systems &bull; Seed / Strategic Round</div>
  </div>
  <div class="content" style="align-items: flex-start; justify-content: center; max-width: 1000px;">
    <div class="hero-tag">
      <span>●</span> Live on Base Mainnet &bull; $2.20B+ Monitored Debt
    </div>
    <h1 style="font-size: 56px; font-weight: 800; line-height: 1.08; letter-spacing: -1.5px; margin-bottom: 20px;">
      The High-Frequency Risk & OEV Infrastructure for Modular DeFi
    </h1>
    <h2 style="font-size: 22px; color: #94a3b8; font-weight: 400; line-height: 1.5; margin-bottom: 40px;">
      Sub-20ms parametric stress-testing and liquidation surveillance protecting MetaMorpho vault curators, credit desks, and institutional capital.
    </h2>
    <div class="grid-4" style="width: 100%;">
      <div class="kpi-box">
        <div class="kpi-num">$2.20B</div>
        <div class="kpi-label">Monitored Debt (Base)</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">~15 ms</div>
        <div class="kpi-label">Decision Compute Latency</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">94.38%</div>
        <div class="kpi-label">Verified SVR Recapture</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">100.0%</div>
        <div class="kpi-label">30-Day Verified Uptime</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Founders: Volkan Dağlı (CTO) &bull; Dr. Zerrin Dağlı (Advisor) &bull; Dağhan Dağlı</div>
    <div>Executive Line: <a href="mailto:ask@answerr.me">ask@answerr.me</a> &bull; <a href="https://radar.werracle.com">radar.werracle.com</a></div>
    <div>Slide 01 / 12</div>
  </div>
</div>

<!-- SLIDE 2: THE PROBLEM -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Market Problem</div>
    </div>
    <div class="header-title">The Trillion-Dollar Lending Blindspot</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Modular Credit Unbundled Without Real-Time Risk Rails</h1>
    <h2 class="slide-sub">Protocols like Morpho Blue and Aave v3 have unlocked billions in modular lending, but created massive risk blindspots.</h2>
    <div class="grid-3">
      <div class="card card-highlight">
        <div class="card-title" style="color: #f87171;">
          <span style="font-size: 20px;">⚡</span> 1. Fragmentation & OEV Leakage
        </div>
        <div class="card-desc">
          Instead of monolithic pools, lending is scattered across hundreds of isolated markets. During market drops, liquidation bonuses leak to centralized builder cartels via gas wars. On Ethereum L1, <strong>95.9% of builder payments</strong> concentrate in extreme tail liquidations.
        </div>
      </div>
      <div class="card card-highlight">
        <div class="card-title" style="color: #f59e0b;">
          <span style="font-size: 20px;">📉</span> 2. Curators Flying Blind
        </div>
        <div class="card-desc">
          MetaMorpho curators (managing $1.5B+ TVL) allocate capital across multiple markets. Current analytics rely on static daily snapshots that cannot simulate real-time collateral drops, cascading liquidations, or pro-rata bad debt before market shocks hit.
        </div>
      </div>
      <div class="card card-highlight">
        <div class="card-title" style="color: #38bdf8;">
          <span style="font-size: 20px;">🔒</span> 3. Institutional Capital Demands Proof
        </div>
        <div class="card-desc">
          Institutional credit desks and enterprise treasuries require continuous parametric stress-testing, verifiable on-chain audits, and sub-second loss-given-default (LGD) metrics before deploying capital into permissionless DeFi.
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Pitch Deck &bull; Confidential</div>
    <div>Live Telemetry: <a href="https://api.werracle.com/v1/radar/overview">api.werracle.com</a></div>
    <div>Slide 02 / 12</div>
  </div>
</div>

<!-- SLIDE 3: THE SOLUTION -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Proprietary Architecture</div>
    </div>
    <div class="header-title">Sub-Second Parametric Risk & Liquidation Engine</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Werracle Reflex Decision Engine: Real-Time Risk DaaS</h1>
    <h2 class="slide-sub">A production-hardened pipeline connecting Layer-2 flashblocks directly to institutional risk models.</h2>
    <div class="grid-3" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-title"><span style="color:#38bdf8;">01.</span> L2 Flashblock Surveillance</div>
        <div class="card-desc">
          Direct ingestion of Base 200ms flashblocks and Morpho Blue GraphQL events. Tracks 68,700+ open positions and isolates 45 unlisted/synthetic markets to deliver pure, unpolluted data.
        </div>
      </div>
      <div class="card">
        <div class="card-title"><span style="color:#10b981;">02.</span> Parametric Shock Simulation</div>
        <div class="card-desc">
          Applies real-time collateral price shocks (0%, -5%, -10%, -15%, -20%, -30%) across every live borrower. Evaluates exact solvency against LLTV and Liquidation Incentive Factors (LIF).
        </div>
      </div>
      <div class="card">
        <div class="card-title"><span style="color:#a855f7;">03.</span> Verified SVR OEV Recapture</div>
        <div class="card-desc">
          Calibrates expected liquidation recoveries against our empirical baseline proving <strong>94.38% value recapture</strong> via Chainlink Smart Value Recapture (SVR) proceeds contracts.
        </div>
      </div>
    </div>
    <div class="card" style="background: rgba(15, 23, 42, 0.9); border-color: rgba(56, 189, 248, 0.4); padding: 18px 24px;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span style="font-weight: 700; color: #38bdf8;">Live Curator API:</span>
          <code style="font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #f8fafc; margin-left: 10px;">GET https://api.werracle.com/v1/radar/curator/steakhouse</code>
        </div>
        <span class="tag-green">HTTP 200 OK &bull; Live Tested</span>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Pitch Deck &bull; Confidential</div>
    <div>Live Telemetry: <a href="https://api.werracle.com/v1/radar/overview">api.werracle.com</a></div>
    <div>Slide 03 / 12</div>
  </div>
</div>

<!-- SLIDE 4: EMPIRICAL DISCOVERY & PROOF -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Academic Proof</div>
    </div>
    <div class="header-title">First On-Chain Measurement of Chainlink SVR</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Groundbreaking Empirical Validation: 94.38% Recapture</h1>
    <h2 class="slide-sub">Published research monograph auditing 105 verified SVR liquidation transactions ($1.90M debt repaid) on Base.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_oev}" class="chart-img" alt="OEV Comparison">
      </div>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="card" style="padding: 16px;">
          <div style="font-size: 20px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">94.38% ($179.8k)</div>
          <div style="font-size: 13px; color: #94a3b8; font-weight: 600;">OEV Pool Recaptured into Protocol Proceeds</div>
          <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Median transaction recaptures <strong>98.30%</strong> of the liquidation bonus.</div>
        </div>
        <div class="card" style="padding: 16px;">
          <div style="font-size: 20px; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono';">+1.26% Median</div>
          <div style="font-size: 13px; color: #94a3b8; font-weight: 600;">Solver Gross Margin at Oracle Prices</div>
          <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Fierce competition prevents solver cartels (Top-3 = 77.05%, HHI = 2,216).</div>
        </div>
        <div class="card" style="padding: 16px;">
          <div style="font-size: 20px; font-weight: 800; color: #f87171; font-family: 'JetBrains Mono';">95.94% L1 Fat-Tail</div>
          <div style="font-size: 13px; color: #94a3b8; font-weight: 600;">22 Largest L1 Liquidations Account for $351.3k in Fees</div>
          <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Empirically proves that Layer-2 SVR eliminates the L1 MEV priority fee black hole.</div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>DOI: 10.5281/zenodo.23642090 &bull; Hugging Face: pCwOrM/werracle-oev-liquidation-dataset-2026</div>
    <div>Slide 04 / 12</div>
  </div>
</div>

<!-- SLIDE 5: LIVE TRACTION & STATUS -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Traction & Scale</div>
    </div>
    <div class="header-title">Live Production Telemetry (Day 0 Proof)</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Active Market Surveillance on Base Mainnet</h1>
    <h2 class="slide-sub">Zero mock data. Full automated synchronization from Morpho Blue GraphQL and Base RPC nodes.</h2>
    <div class="grid-4" style="margin-bottom: 24px;">
      <div class="kpi-box">
        <div class="kpi-num">$2,197,760,378</div>
        <div class="kpi-label">Clean Monitored Debt</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">38 Markets</div>
        <div class="kpi-label">Whitelisted & Listed</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">68,727</div>
        <div class="kpi-label">Open Borrower Positions</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">45 Markets</div>
        <div class="kpi-label">Unlisted / Spam Filtered</div>
      </div>
    </div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title"><span style="color:#38bdf8;">●</span> Enterprise Data Hygiene</div>
        <div class="card-desc">
          Raw Morpho queries contain $2.31B in synthetic, unlisted markets (e.g. HERMES, test_cbBTC). Werracle is the <strong>only engine</strong> that filters unlisted and unrecognized collateral, providing institutions with pure, audited credit figures.
        </div>
      </div>
      <div class="card">
        <div class="card-title"><span style="color:#10b981;">●</span> Independent Frankfurt Health Node</div>
        <div class="card-desc">
          A dedicated remote monitoring daemon in Frankfurt (<code>mechsrv</code>) pings the API every 5 minutes and maintains hourly hot-replica database backups. 100% 30-day uptime and 191ms median global latency.
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Live Health Page: <a href="https://radar.werracle.com/status">radar.werracle.com/status</a></div>
    <div>Slide 05 / 12</div>
  </div>
</div>

<!-- SLIDE 6: CURATOR STRESS PRODUCT DEMO -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Flagship Product</div>
    </div>
    <div class="header-title">Live Dynamic Vault Stress Testing</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Institutional Stress-Testing for MetaMorpho Curators</h1>
    <h2 class="slide-sub">Simulating real-time loss-given-default (LGD) across live Steakhouse, Gauntlet, and Re7 vaults.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_stress}" class="chart-img" alt="Stress Curve">
      </div>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="card card-highlight">
          <div class="card-title" style="color: #38bdf8;">Case Study: Steakhouse USDC ($116.2M TVL)</div>
          <div class="card-desc">
            Directly ingests live allocations across 5 collateral markets (cbBTC, cbETH, wstETH, etc.) and models collateral price drops.
          </div>
        </div>
        <div class="grid-2">
          <div class="kpi-box" style="padding: 14px;">
            <div class="kpi-num" style="font-size: 24px;">$0.00</div>
            <div class="kpi-label">Current Bad Debt</div>
          </div>
          <div class="kpi-box" style="padding: 14px;">
            <div class="kpi-num" style="font-size: 24px; color: #f87171;">1.06%</div>
            <div class="kpi-label">Worst-Case TVL Loss (-30%)</div>
          </div>
        </div>
        <div class="card" style="padding: 16px;">
          <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
            <strong>Pro-Rata Attribution:</strong> Under a -20% collateral shock, $209.4M in debt becomes liquidatable, causing $2.41M in market-wide bad debt. Steakhouse's pro-rata loss remains near $0.00 due to senior allocation tiers.
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Dedicated Curator Endpoint: <code>api.werracle.com/v1/radar/curator/{{vault}}</code></div>
    <div>Slide 06 / 12</div>
  </div>
</div>

<!-- SLIDE 7: BUSINESS MODEL & UNIT ECONOMICS -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Business Model</div>
    </div>
    <div class="header-title">High-Margin B2B SaaS & Data Subscription</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Recurring Enterprise Tiers & High-Margin Unit Economics</h1>
    <h2 class="slide-sub">Zero-friction developer onboarding combined with high-value institutional curation contracts.</h2>
    <div class="grid-3" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-title">Free / Public Goods</div>
        <div style="font-size: 28px; font-weight: 800; color: #ffffff; font-family: 'JetBrains Mono'; margin-bottom: 8px;">$0</div>
        <div class="card-desc" style="font-size: 13px;">
          &bull; Public status & overview API<br>
          &bull; Supported vault registry<br>
          &bull; Zenodo & HF open data (CC-BY)<br>
          &bull; Funnel for institutional leads
        </div>
      </div>
      <div class="card card-highlight">
        <div class="card-title" style="color: #38bdf8;">Pro Researcher</div>
        <div style="font-size: 28px; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono'; margin-bottom: 8px;">$149 <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">/ mo</span></div>
        <div class="card-desc" style="font-size: 13px;">
          &bull; Full REST API access<br>
          &bull; 600 requests / minute<br>
          &bull; Historical SVR & liquidation logs<br>
          &bull; Searchers & MEV researchers
        </div>
      </div>
      <div class="card card-highlight" style="border-color: #10b981;">
        <div class="card-title" style="color: #10b981;">Institutional Curator</div>
        <div style="font-size: 28px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono'; margin-bottom: 8px;">$499 <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">/ mo</span></div>
        <div class="card-desc" style="font-size: 13px;">
          &bull; Dynamic vault stress-testing API<br>
          &bull; 3,000 requests / minute<br>
          &bull; Parametric shock simulations<br>
          &bull; 99.9% uptime SLA & priority support
        </div>
      </div>
    </div>
    <div class="grid-2">
      <div class="card" style="padding: 16px 20px;">
        <div class="card-title"><span style="color:#10b981;">●</span> Dual Compliant Billing Rails</div>
        <div class="card-desc">
          Paddle (Merchant of Record) for automated global cards & VAT + ITouch SWIFT bank invoices for institutional enterprise + EIP-191/1271 signed Base USDC.
        </div>
      </div>
      <div class="card" style="padding: 16px 20px;">
        <div class="card-title"><span style="color:#38bdf8;">●</span> Tax Advantage: 100% Export Exemption</div>
        <div class="card-desc">
          Headquartered in Çukurova Teknokent: Software exports to foreign institutions qualify for <strong>100% Corporate Tax exemption</strong> (Pres. Decree 11257).
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Unit Economics: 88% Gross Margin &bull; 12.4x LTV/CAC</div>
    <div>Slide 07 / 12</div>
  </div>
</div>

<!-- SLIDE 8: MARKET OPPORTUNITY (TAM / SAM / SOM) -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Market Size</div>
    </div>
    <div class="header-title">The Expanding Frontier of Modular Credit Risk</div>
  </div>
  <div class="content">
    <h1 class="slide-title">A Multi-Billion Dollar On-Chain Credit Expansion</h1>
    <h2 class="slide-sub">As institutional RWAs and decentralized credit migrate to Layer-2s, real-time risk infrastructure becomes mandatory.</h2>
    <div class="grid-3" style="margin-bottom: 24px;">
      <div class="card">
        <div style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">TAM &bull; 2028 Horizon</div>
        <div style="font-size: 42px; font-weight: 800; color: #ffffff; font-family: 'JetBrains Mono'; margin: 10px 0;">$45B</div>
        <div class="card-desc">
          Total institutional on-chain lending, credit delegation, and RWA structured debt volume.
        </div>
      </div>
      <div class="card card-highlight">
        <div style="font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase;">SAM &bull; Active Modular TVL</div>
        <div style="font-size: 42px; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono'; margin: 10px 0;">$8.5B</div>
        <div class="card-desc">
          Active TVL across modular and isolated lending protocols (Morpho Blue, Aave v3, Fluid, Euler v2).
        </div>
      </div>
      <div class="card card-highlight" style="border-color: #10b981;">
        <div style="font-size: 13px; font-weight: 700; color: #10b981; text-transform: uppercase;">SOM &bull; Annual Risk Spend</div>
        <div style="font-size: 42px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono'; margin: 10px 0;">$120M</div>
        <div class="card-desc">
          Annual institutional spend on specialized risk curation, liquidation telemetry, and automated stress testing.
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Key Industry Tailwind: Morpho Blue's Hyper-Growth</div>
      <div class="card-desc">
        Morpho Blue has expanded from $0 to over $1.5B+ in TVL in under 18 months, becoming the collateral backend for Coinbase, Spark, and Steakhouse. Every new isolated market deployed creates another customer touchpoint for Werracle Radar.
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Pitch Deck &bull; Confidential</div>
    <div>Slide 08 / 12</div>
  </div>
</div>

<!-- SLIDE 9: COMPETITIVE LANDSCAPE & MOAT -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Competitive Moat</div>
    </div>
    <div class="header-title">Unfair Advantages & IP Defensibility</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Positioned at the Intersection of High-Frequency & Risk</h1>
    <h2 class="slide-sub">Legacy risk providers offer slow, expensive consulting. Werracle offers sub-second, automated DaaS APIs.</h2>
    <div style="margin-bottom: 20px;">
      <table class="deck-table">
        <thead>
          <tr>
            <th>Key Metric / Capability</th>
            <th>Werracle Radar</th>
            <th>Chaos Labs / Gauntlet</th>
            <th>Block Analitica</th>
            <th>Dune Analytics</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Latency / Resolution</strong></td>
            <td><span class="tag-green">~15ms Decision Compute</span></td>
            <td>Periodic / Block-level</td>
            <td>Daily Static Reports</td>
            <td>Seconds to Minutes</td>
          </tr>
          <tr>
            <td><strong>Live Dynamic Vault Shocks</strong></td>
            <td><span class="tag-green">Parametric (0 to -30%)</span></td>
            <td>Custom Internal Models</td>
            <td>Static Spreadsheets</td>
            <td>No (Historical Only)</td>
          </tr>
          <tr>
            <td><strong>Verified SVR / OEV Recapture</strong></td>
            <td><span class="tag-green">94.38% Calibrated</span></td>
            <td>None</td>
            <td>None</td>
            <td>Basic Dashboards</td>
          </tr>
          <tr>
            <td><strong>Pricing & Accessibility</strong></td>
            <td><span class="tag-blue">$149 – $499 / mo (Self-Serve)</span></td>
            <td>$50k – $250k / yr (Consulting)</td>
            <td>$30k+ / yr (Enterprise)</td>
            <td>$4,800 / yr (General SQL)</td>
          </tr>
          <tr>
            <td><strong>IP Protection</strong></td>
            <td><span class="tag-green">TR 2026/016285 Patent & BSL</span></td>
            <td>Proprietary</td>
            <td>Proprietary</td>
            <td>Open SQL / Queries</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title">Patent & Licensing Moat</div>
        <div class="card-desc">
          Core procedural execution engine is protected under pending patent application <strong>TÜRKPATENT TR 2026/016285</strong> and licensed under Business Source License 1.1 (BSL 1.1 until 2030-01-01, converting to Apache 2.0).
        </div>
      </div>
      <div class="card">
        <div class="card-title">Data Monopoly in L2 OEV</div>
        <div class="card-desc">
          First-mover advantage as the publisher of the canonical empirical SVR dataset. Curators and protocols build their baseline risk assumptions directly on our open Zenodo decoders.
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Pitch Deck &bull; Confidential</div>
    <div>Slide 09 / 12</div>
  </div>
</div>

<!-- SLIDE 10: FINANCIAL PROJECTIONS -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Financials</div>
    </div>
    <div class="header-title">3-Year Projections & Path to $3.8M+ ARR</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Predictable, High-Margin Software Expansion</h1>
    <h2 class="slide-sub">Minimal infrastructure overhead drives an 88% gross margin with rapid compounding ARR.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_arr}" class="chart-img" alt="ARR Growth">
      </div>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">Year 1 (2027) Run-Rate</span>
            <span style="font-size: 22px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">$364,260 ARR</span>
          </div>
          <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
            120 Pro Subscribers &bull; 25 MetaMorpho Curators & Risk Desks &bull; Breakeven achieved in Month 8.
          </div>
        </div>
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">Year 2 (2028) Run-Rate</span>
            <span style="font-size: 22px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">$1,373,460 ARR</span>
          </div>
          <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
            450 Pro Subscribers &bull; 95 Institutional Clients across Base, Arbitrum, and Ethereum L1.
          </div>
        </div>
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">Year 3 (2029) Run-Rate</span>
            <span style="font-size: 22px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">$3,822,240 ARR</span>
          </div>
          <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
            1,200 Pro Users &bull; 280 Institutional Curators &bull; Standard risk layer for institutional DeFi.
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Unit Economics: 88% Average Gross Margin &bull; 12.4x LTV/CAC Ratio</div>
    <div>Slide 10 / 12</div>
  </div>
</div>

<!-- SLIDE 11: TEAM & INSTITUTIONAL BACKING -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Founding Team</div>
    </div>
    <div class="header-title">Technical Rigor & Academic Precision</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Engineered by Formal Verification & Quantitative Researchers</h1>
    <h2 class="slide-sub">Bridging theoretical econometrics, high-frequency blockchain engineering, and enterprise delivery.</h2>
    <div class="grid-3" style="margin-bottom: 24px;">
      <div class="card card-highlight">
        <div class="card-title">Volkan Dağlı</div>
        <div style="font-size: 13px; font-weight: 700; color: #38bdf8; margin-bottom: 10px;">Co-Founder & CTO / Lead Developer</div>
        <div class="card-desc">
          Co-Founder & CTO at ITOUCH BİLİŞİM SİSTEMLERİ LTD. ŞTİ. Formal verification researcher affiliated with Anadolu University. Lead architect of Werracle Reflex Engine and author of 4 verified Zenodo open-science monographs.
        </div>
      </div>
      <div class="card">
        <div class="card-title">Dr. Zerrin Dağlı</div>
        <div style="font-size: 13px; font-weight: 700; color: #10b981; margin-bottom: 10px;">Academic & Econometric Advisor</div>
        <div class="card-desc">
          Academic advisor affiliated with Mersin University and Yusuf Kalkavan Anadolu Lisesi. Quantitative methodology specialist leading the statistical verification and econometric modeling for liquidation dynamics.
        </div>
      </div>
      <div class="card">
        <div class="card-title">Dağhan Dağlı</div>
        <div style="font-size: 13px; font-weight: 700; color: #a855f7; margin-bottom: 10px;">Student Researcher & Contributor</div>
        <div class="card-desc">
          Toros Science High School, MEV (Toros University). Focus on smart contract unit testing, RPC decoding pipelines, and automated liquidation simulation environments.
        </div>
      </div>
    </div>
    <div class="grid-3">
      <div class="card" style="padding: 16px;">
        <div style="font-weight: 700; color: #ffffff; font-size: 14px;">Çukurova Teknokent</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Official technology incubator & R&D lab support.</div>
      </div>
      <div class="card" style="padding: 16px;">
        <div style="font-weight: 700; color: #ffffff; font-size: 14px;">TÜRKPATENT TR 2026/016285</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Registered patent application for procedural arbitration.</div>
      </div>
      <div class="card" style="padding: 16px;">
        <div style="font-weight: 700; color: #ffffff; font-size: 14px;">100% Tax Advantage</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Corporate export tax exemption under Pres. Decree 11257.</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Direct Executive Contact: <a href="mailto:ask@answerr.me">ask@answerr.me</a></div>
    <div>Slide 11 / 12</div>
  </div>
</div>

<!-- SLIDE 12: THE ASK & USE OF FUNDS -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">The Ask</div>
    </div>
    <div class="header-title">Seed / Strategic Capital Allocation</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Raising $1.5M Seed to Scale Institutional DeFi Risk</h1>
    <h2 class="slide-sub">18-month runway to reach $1.3M+ ARR, multi-chain dominance, and deep curation market penetration.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_funds}" class="chart-img" alt="Use of Funds">
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div class="card">
          <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">Engineering Expansion (40% - $600k)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Hire 3 senior Rust/Go EVM systems engineers to scale cross-chain stream processing across Arbitrum, Optimism, and Ethereum L1.</div>
        </div>
        <div class="card">
          <div style="font-weight: 700; color: #10b981; font-size: 14px;">Dedicated Archive Infrastructure (25% - $375k)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Deploy proprietary bare-metal Archive Nodes and sub-second WebSocket distribution clusters for institutional low-latency feeds.</div>
        </div>
        <div class="card">
          <div style="font-weight: 700; color: #f59e0b; font-size: 14px;">Institutional BD & Curators (20% - $300k)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Direct integrations with MetaMorpho curators (Steakhouse, Gauntlet, Re7), Aave risk DAOs, and institutional lending desks.</div>
        </div>
        <div class="card">
          <div style="font-weight: 700; color: #a855f7; font-size: 14px;">Security Audits & Compliance (15% - $225k)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Complete SOC2 Type II compliance, enterprise security hardening, and legal advisory for international institutional contracts.</div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Live Demo: <a href="https://radar.werracle.com">radar.werracle.com</a> &bull; Inquiries: <a href="mailto:ask@answerr.me">ask@answerr.me</a></div>
    <div>Slide 12 / 12</div>
  </div>
</div>

</body>
</html>
"""

HTML_PATH = os.path.join(WORKSPACE, "deck_assets", "investor_deck.html")
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML presentation written: {HTML_PATH}")

LOCAL_PDF = os.path.join(WORKSPACE, "Werracle_Radar_Investor_Pitch_Deck.pdf")
ARTIFACT_PDF = os.path.join(ARTIFACT_DIR, "Werracle_Radar_Investor_Pitch_Deck.pdf")

print("Rendering PDF via Playwright Chromium...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(f"file:///{HTML_PATH.replace(os.sep, '/')}", wait_until="networkidle")
    page.pdf(
        path=LOCAL_PDF,
        width="16in",
        height="9in",
        print_background=True,
        display_header_footer=False
    )
    browser.close()

shutil.copy2(LOCAL_PDF, ARTIFACT_PDF)
print(f"SUCCESS: Rendered local PDF -> {LOCAL_PDF}")
print(f"SUCCESS: Copied artifact PDF -> {ARTIFACT_PDF}")
print(f"PDF Size: {os.path.getsize(LOCAL_PDF):,} bytes")
