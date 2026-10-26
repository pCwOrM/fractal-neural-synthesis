# Update werracle/radar.html, docs/EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md, and docs/MORPHO_DAO_GRANT_APPLICATION_FINAL.md to v1.2 ground truth

from pathlib import Path

WERRACLE_DIR = Path(r"c:\Users\maat\Documents\antigravity\werracle")

# 1. Update radar.html
radar_path = WERRACLE_DIR / "radar.html"
html = radar_path.read_text(encoding="utf-8")

replacements_radar = [
    (
        "Sub-second health factor surveillance across 83 Morpho Blue markets and empirical research into Oracle Extractable Value (OEV) recapture on Base L2 (Chainlink SVR) and Ethereum L1.",
        "Sub-second health factor surveillance across 38 verified Morpho Blue markets ($2.20B monitored debt, 45 unlisted spam markets filtered) and empirical research into Oracle Extractable Value (OEV) recapture on Base L2 (Chainlink SVR) and Ethereum L1."
    ),
    (
        '<div class="val gold" id="metricMarkets">83 Markets</div>\n          <div class="sub" id="metricPositions">69,341 Tracked Positions</div>',
        '<div class="val gold" id="metricMarkets">38 Markets</div>\n          <div class="sub" id="metricPositions">$2.20B Debt | 68,573 Positions</div>'
    ),
    (
        '<div class="val revert" id="metricHot">Active Risk</div>\n          <div class="sub" id="metricBadDebt">Bad Debt (HF &lt; 0.95): Tracking</div>',
        '<div class="val revert" id="metricHot">5,083 Hot</div>\n          <div class="sub" id="metricBadDebt">Bad Debt (HF &lt; 0.95): 82 positions</div>'
    ),
    (
        '<div class="val permit" id="metricRecapture">98.10%</div>\n          <div class="sub">$186,889.85 / $190,506.31 gross</div>',
        '<div class="val permit" id="metricRecapture">94.38%</div>\n          <div class="sub">$179,807.38 / $190,506.31 (Med: 98.3%)</div>'
    ),
    (
        '<div class="val" id="metricMargin" style="color:var(--mist)">-1.55%</div>\n          <div class="sub">61.9% subzero / breakeven</div>',
        '<div class="val" id="metricMargin" style="color:var(--mist)">+1.26%</div>\n          <div class="sub">33/105 (31.4%) subzero / breakeven</div>'
    ),
    (
        '<div class="val" style="color:var(--ice)">20 Solvers</div>\n          <div class="sub">27 Signers | Top Solver Vol: 31.6% (Zero Cartel)</div>',
        '<div class="val" style="color:var(--ice)">17 Solvers</div>\n          <div class="sub">Top-3 Vol: 77.05% | HHI: 2,216</div>'
    ),
    (
        '<div class="sub">68/105 Multi-Calls | Up to 32 Sub-Calls/Tx</div>',
        '<div class="sub">68/105 Multi-Calls | 513 Liquidations</div>'
    ),
    (
        "Empirical multi-call decoding across Base Morpho Blue liquidations during the high-volatility window (Oct 12–19, 2026). Atlas permissionless solvers bid aggressively, transferring ~98% of liquidation MEV to protocols.",
        "Empirical on-chain re-derivation across 105 Base SVR transactions (86 Morpho Blue, 19 Aave v3; 513 sub-liquidations). Atlas permissionless solvers bid aggressively, returning 94.38% of liquidation OEV (median 98.3%) to protocols."
    ),
    (
        '<div class="v-segment" style="width:98.1%;background:var(--permit)" title="Protocol Bids: 98.10%"></div>\n              <div class="v-segment" style="width:1.86%;background:var(--gold)" title="Solver Pre-Swap: 1.86%"></div>',
        '<div class="v-segment" style="width:94.38%;background:var(--permit)" title="Protocol Bids: 94.38%"></div>\n              <div class="v-segment" style="width:5.58%;background:var(--gold)" title="Solver Pre-Swap: 5.58%"></div>'
    ),
    (
        '<span><i class="v-sq" style="background:var(--permit)"></i> Protocol Recapture: <b>98.10% ($186.9k)</b></span>\n              <span><i class="v-sq" style="background:var(--gold)"></i> Solvers Pre-Swap: <b>1.86% ($3.5k)</b></span>',
        '<span><i class="v-sq" style="background:var(--permit)"></i> Protocol Recapture: <b>94.38% ($179.8k)</b></span>\n              <span><i class="v-sq" style="background:var(--gold)"></i> Solvers Pre-Swap: <b>5.58% ($10.6k)</b></span>'
    ),
    (
        '<span class="k">Value Recaptured to Protocol Bids</span>\n              <span class="v" style="color:var(--permit)">$186,889.85 USD</span>',
        '<span class="k">Value Recaptured to Protocol Bids</span>\n              <span class="v" style="color:var(--permit)">$179,807.38 USD (94.38%)</span>'
    ),
    (
        '<span class="k">Solvers Retained (Pre-DEX Slippage)</span>\n              <span class="v" style="color:var(--gold)">$3,545.73 USD</span>',
        '<span class="k">Solvers Retained (Oracle Pre-Swap)</span>\n              <span class="v" style="color:var(--gold)">$10,630.95 USD (5.58%)</span>'
    ),
    (
        '<span class="k">Median Transaction Margin</span>\n              <span class="v" style="color:var(--revert)">-1.55%</span>',
        '<span class="k">Median Transaction Margin</span>\n              <span class="v" style="color:var(--permit)">+1.26% (Median Bid: 98.3%)</span>'
    ),
    (
        '<span class="k">Transactions with Margin &le; 0.00%</span>\n              <span class="v">65 / 105 (61.9%)</span>',
        '<span class="k">Transactions with Margin &le; 0.00%</span>\n              <span class="v">33 / 105 (31.4%)</span>'
    ),
    (
        '<span class="k">Cumulative Negative Margin Losses</span>\n              <span class="v">~$2,500 USD</span>',
        '<span class="k">Total Repaid Debt (513 Sub-Calls)</span>\n              <span class="v">$1,898,755.19 USD</span>'
    ),
    (
        '<span><i class="v-sq" style="background:var(--gold)"></i> Whale Bribes: <b>Top 22 Tx = $344.2k (96.0%)</b></span>',
        '<span><i class="v-sq" style="background:var(--gold)"></i> Whale Bribes: <b>Top 22 Tx = $351.3k (95.94%)</b></span>'
    ),
    (
        '<span class="k">Total MEV-Boost Builder Payments</span>\n              <span class="v">$358,316.62 USD</span>',
        '<span class="k">Total MEV-Boost Builder Payments</span>\n              <span class="v">$366,112.89 USD</span>'
    ),
    (
        '<span class="k">Median Builder Payment</span>\n              <span class="v" style="color:var(--permit)">$0.08 USD</span>',
        '<span class="k">Median Builder Payment</span>\n              <span class="v" style="color:var(--permit)">$0.09 USD</span>'
    ),
    (
        "Because Chainlink SVR captures ~98% of post-breach liquidation value",
        "Because Chainlink SVR captures 94.38% (median 98.3%) of post-breach liquidation value"
    )
]

# Normalize line endings to \n for replacement
html_norm = html.replace("\r\n", "\n")
for old, new in replacements_radar:
    assert old in html_norm, f"Missing target in radar.html: {old[:50]}"
    html_norm = html_norm.replace(old, new, 1)

# Also update the JS fetchRadarData block in radar.html to support the v2.0 schema!
old_js = """      if (data.portfolio_surveillance) {
        document.getElementById("metricMarkets").textContent = data.portfolio_surveillance.total_monitored_markets + " Markets";
        document.getElementById("metricPositions").textContent = data.portfolio_surveillance.total_tracked_positions.toLocaleString() + " Tracked Positions";
        if (data.portfolio_surveillance.near_liquidation_active != null) {
          document.getElementById("metricHot").textContent = data.portfolio_surveillance.near_liquidation_active.toLocaleString();
        } else if (data.portfolio_surveillance.hot_positions_near_liquidation != null) {
          document.getElementById("metricHot").textContent = data.portfolio_surveillance.hot_positions_near_liquidation.toLocaleString();
        }
        if (data.portfolio_surveillance.insolvent_bad_debt_legacy != null) {
          document.getElementById("metricBadDebt").textContent = "Bad Debt (HF < 0.95): " + data.portfolio_surveillance.insolvent_bad_debt_legacy.toLocaleString() + " legacy";
        }
      }
      if (data.verified_svr_findings) {
        document.getElementById("metricRecapture").textContent = data.verified_svr_findings.protocol_capture_rate_pct.toFixed(2) + "%";
        document.getElementById("metricMargin").textContent = data.verified_svr_findings.median_transaction_margin_pct.toFixed(2) + "%";
      }
      document.getElementById("headerLiveStatus").textContent = "Live Telemetry (" + (data.sensory_membrane?.flashblocks_processed?.toLocaleString() || "Sync") + " blocks)";"""

new_js = """      const b2 = data.realtime_surveillance?.base_l2;
      if (b2) {
        document.getElementById("metricMarkets").textContent = b2.markets_monitored + " Verified Markets";
        const debtB = (b2.total_monitored_debt_usd / 1e9).toFixed(2);
        document.getElementById("metricPositions").textContent = "$" + debtB + "B Debt | " + b2.open_positions_tracked.toLocaleString() + " Positions";
        if (b2.hot_positions_hf_below_1_10 != null) {
          document.getElementById("metricHot").textContent = b2.hot_positions_hf_below_1_10.toLocaleString() + " Hot";
        }
        if (b2.bad_debt_positions != null) {
          document.getElementById("metricBadDebt").textContent = "Bad Debt (HF < 0.95): " + b2.bad_debt_positions.toLocaleString() + " positions";
        }
        document.getElementById("headerLiveStatus").textContent = "Live Telemetry (" + (b2.flashblocks_processed?.toLocaleString() || "Active") + " blocks)";
      }
      const svr = data.verified_svr_baseline;
      if (svr) {
        document.getElementById("metricRecapture").textContent = svr.protocol_capture_rate_pct.toFixed(2) + "%";
        const m = svr.median_tx_solver_margin_pct;
        document.getElementById("metricMargin").textContent = (m >= 0 ? "+" : "") + m.toFixed(2) + "%";
      }"""

assert old_js in html_norm, "Missing old_js in radar.html"
html_norm = html_norm.replace(old_js, new_js, 1)

radar_path.write_text(html_norm, encoding="utf-8")
print("Updated werracle/radar.html to v1.2 ground truth & v2.0 live API schema!")

# 2. Update docs/EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md
doc_path = WERRACLE_DIR / "docs" / "EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md"
doc = doc_path.read_text(encoding="utf-8").replace("\r\n", "\n")

doc = doc.replace(
    "[`werracle_oev_empirical_dataset_2026.json`](file:///c:/Users/maat/Documents/antigravity/wonderful-raman/data/werracle_oev_empirical_dataset_2026.json)",
    "[Zenodo v2 Replication Package (DOI: `10.5281/zenodo.23642090`)](https://doi.org/10.5281/zenodo.23642090)"
)
doc = doc.replace(
    "redirected **\\$186,889.85 (98.10%)** directly back to lending protocols and depositors as bids. Solvers retained a pre-swap gross margin of only **1.86% (\\$3,545.73)**, with median transaction margins compressed to **-1.55%**. Over **61.9%** (65 of 105) of transactions concluded at zero or negative net profit prior to off-chain DEX slippage.",
    "redirected **\\$179,807.38 (94.38%, median tx recapture 98.33%)** directly back to lending protocols and depositors as bids across 513 sub-liquidations (\\$1,898,755.19 repaid debt). Solvers retained an oracle pre-swap margin of **5.58% (\\$10,630.95)**, with median transaction margins compressed to **+1.26%**. **31.4%** (33 of 105) of transactions concluded at zero or negative net profit prior to off-chain DEX slippage."
)
doc = doc.replace(
    "the top 22 transactions accounted for **\\$344,155.62** of the total \\$358,316.62 paid to builders",
    "the top 22 transactions accounted for **\\$351,268.00 (95.94%)** of the total \\$366,112.89 paid to builders"
)
doc = doc.replace(
    'G1["Brüt Tasfiye Değeri: $190.5k"] -->|"%98.10 Protokol Teklifi"| P1["Borç Verme Protokolü & Kasa ($186.9k)"]\n        G1 -->|"%1.86 Pay (Medyan -%1.55)"| S1["Solver Payı ($3.5k pre-swap)"]',
    'G1["Brüt Tasfiye Teşviki: $190.5k"] -->|"%94.38 Protokol Teklifi (Medyan %98.3)"| P1["Borç Verme Protokolü & Kasa ($179.8k)"]\n        G1 -->|"%5.58 Pay (Medyan +%1.26)"| S1["Solver Payı ($10.6k pre-swap)"]'
)
doc = doc.replace(
    'B1["Toplam Builder Ödemesi: $358.3k"] -->|"Top 22 İşlem (%96.0)"| Whale["Balina İşlemleri ($344.2k)"]',
    'B1["Toplam Builder Ödemesi: $366.1k"] -->|"Top 22 İşlem (%95.94)"| Whale["Balina İşlemleri ($351.3k)"]'
)
doc = doc.replace("-1.55%", "+1.26%").replace("98.10%", "94.38%").replace("186,889.85", "179,807.38").replace("358,316.62", "366,112.89")
doc_path.write_text(doc, encoding="utf-8")
print("Updated docs/EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md!")

# 3. Update docs/MORPHO_DAO_GRANT_APPLICATION_FINAL.md
morpho_path = WERRACLE_DIR / "docs" / "MORPHO_DAO_GRANT_APPLICATION_FINAL.md"
m_doc = morpho_path.read_text(encoding="utf-8").replace("\r\n", "\n")
m_doc = m_doc.replace("98.10% ($186,889.85 USD)", "94.38% ($179,807.38 USD; median tx recapture 98.33%)")
m_doc = m_doc.replace("recapturing 98.10%", "recapturing 94.38% (median 98.33%)")
morpho_path.write_text(m_doc, encoding="utf-8")
print("Updated docs/MORPHO_DAO_GRANT_APPLICATION_FINAL.md!")
