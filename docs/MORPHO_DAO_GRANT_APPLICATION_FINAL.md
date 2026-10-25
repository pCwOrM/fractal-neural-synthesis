# [MIP 93 Grant Application] Werracle: MetaMorpho Curator Risk Radar & Independent SVR Telemetry Suite

**Project Title:** Werracle: MetaMorpho Curator Risk Radar & Independent SVR Telemetry Suite  
**Organization name:** ITouch Systems / Werracle Research & Security Desk  
**Organization website and/or social media links:**  
- **Public Risk Radar:** https://radar.werracle.com | https://werracle.io/radar.html  
- **Live Telemetry API:** https://api.werracle.com/v1/radar/overview  
- **Open-Source Repository:** https://github.com/pCwOrM/werracle  
- **CERN Zenodo Research DOI:** https://doi.org/10.5281/zenodo.23623588 (Record: 23623589)  
- **Elsevier SSRN Abstract:** https://papers.ssrn.com/abstract=7668638  
- **Hugging Face Dataset:** https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026  
- **Lead Contact & Twitter/X:** https://x.com/pcworm | `pcworm@pcworm.net`  

---

### About us + prior experience:
ITouch Systems Research & Development Desk (headquartered at Adana Çukurova Technopark) is an independent blockchain engineering and cryptoeconomic research group specializing in high-throughput on-chain telemetry, formal verification, and empirical protocol risk analysis. Our focus is developing reliable, open-source public-good infrastructure for decentralized finance protocols.

**Prior Track Record & Existing Morpho Footprint:**
Before requesting any grant funding, our desk self-funded, built, and actively deployed a production-grade monitoring suite for the Morpho Blue ecosystem on Base:
1. **Live High-Frequency Telemetry:** We run a continuous, bare-metal observation daemon (`pcworm-root`) that has processed over **285,000 Base flashblocks** and decoded **5.6M+ transactions**, tracking **83 Morpho Blue markets** and **69,000+ borrower positions** in real time.
2. **Empirical OEV & Liquidation Proof:** During the acute market volatility regime of October 12–19, 2026, we captured and audited all 105 Chainlink Smart Value Recapture (SVR) multi-call liquidation transactions on Base Morpho ($190,506.31 gross collateral). Our findings independently proved to the DeFi ecosystem that **98.10% ($186,889.85 USD)** of gross liquidation value was successfully recaptured and returned directly to Morpho vaults and depositors.
3. **Open Science & Peer Verification:** This research and its underlying 1,157-transaction dataset have been formally registered on **CERN Zenodo** under permanent DOI `10.5281/zenodo.23623588`, indexed on **Elsevier SSRN** ([Abstract: 7668638](https://papers.ssrn.com/abstract=7668638)), and open-sourced on **Hugging Face** (`pCwOrM/werracle-oev-liquidation-dataset-2026`) with 15/15 mathematical validation invariants passing at 100%.

---

### Leading Contributor(s):
- **Volkan Dağlı (@pcworm)** — Systems Architect & Lead Researcher (ITouch Systems)  
  *Background:* Systems programming, high-frequency distributed telemetry, and formal verification in Lean 4.  
  *Profiles:* [GitHub](https://github.com/pCwOrM) | [ORCID: 0009-0000-1587-8703](https://orcid.org/0009-0000-1587-8703) | [Twitter/X](https://x.com/pcworm)
- **Dağhan Dağlı (@lexovian)** — Cryptoeconomic & MEV Researcher  
  *Affiliation:* Toros Science High School / Toros University MEV Research. Focus on Order Flow Auctions (OFA) and solver game theory.  
  *Profile:* [ORCID: 0009-0003-2492-8313](https://orcid.org/0009-0003-2492-8313)
- **Bekirhan Dağlı (@bdagli-web)** — Infrastructure & Bare-Metal Engineering  
  *Affiliation:* Co-Founder & Managing Partner, ITouch Systems. Dedicated bare-metal computing resources and network infrastructure sponsorship.
- **Dr. Z. D. (@jesmaat)** — External Academic & Statistical Advisor (Voluntary / Non-funded)  
  *Background:* Quantitative empirical data modeling, statistical invariants, and academic methodology review.

---

### Requested budget:
**15k MORPHO** *(or 15,000 USDC equivalent)*

In strict accordance with MIP 93 guidelines, **100% of this budget is dedicated entirely to forward-looking scope, maintenance, and technical expansion**. All preliminary development (Base Radar, SVR multi-call parser, Zenodo monograph, and 285k+ flashblock ingestion) has already been fully delivered and open-sourced as a free public good.

Disbursement aligns with the MIP 93 structure:
- **20% (3,000 MORPHO):** Upfront mobilization upon grant approval.
- **20% (3,000 MORPHO):** Upon completion of Month 1 deliverables (Curator Suite & Webhook Engine).
- **60% (9,000 MORPHO):** Upon delivery of Month 2 deliverables and attainment of the objective impact metrics.

---

### Scope of Work:
While Morpho Blue provides unmatched mathematical elegance and modular isolation, MetaMorpho vault curators (e.g., Steakhouse Financial, Gauntlet, Re7 Labs, Flagship, B.Protocol) and large depositors face specific visibility challenges:
1. **Curator Horizon Blurring:** Current dashboards often conflate active pre-liquidation vulnerability ($0.95 \le HF < 1.10$) with dormant, isolated legacy bad debt ($HF < 0.95$), diluting actionable risk response.
2. **Atomic Multi-Call Blindspots:** Over 64.7% of Base SVR liquidations occur via multi-call transactions executing up to 32 bundled sub-calls. Standard single-event log decoders undercount volume and miscalculate solver margin compression.
3. **Cross-Chain Telemetry Asymmetry:** Solvers and curators lack comparative telemetry contrasting L2 SVR protocol recapture efficiency against Ethereum L1 private builder payments.

**Deliverables over the 2-Month Scope:**
1. **MetaMorpho Curator Risk Dashboard (Month 1):**
   - Direct mapping of collateral positions to specific MetaMorpho vaults (e.g. Flagship USDC, Steakhouse USDC, Re7 WETH).
   - Delineation of active collateral stress horizons versus legacy non-liquidatable positions.
2. **Automated Curator Alert Webhook Engine (Month 1):**
   - Low-latency webhook dispatchers (Discord, Telegram, Slack) triggering when aggregate debt near liquidation ($1.00 \le HF < 1.05$) exceeds configurable thresholds ($500k+) in any market.
3. **Cross-Chain Multi-Call Decoder Expansion (Month 2):**
   - Expansion of our atomic receipt sub-call decoder to **Arbitrum Morpho Blue** markets and **Ethereum L1**.
   - Continuous comparative telemetry tracking SVR recapture percentages vs. L1 MEV-Boost priority fees.
4. **Automated Bi-Weekly Governance Risk Digest (Month 2):**
   - Standardized, machine-generated bi-weekly risk and liquidation reports posted directly to the Morpho Governance Forum.

---

### Benefit for the Morpho Ecosystem:
1. **Public Good with Zero Gating:** In full adherence to MIP 93 rules, every tool, dashboard, API endpoint, and dataset is 100% free, open-source (MIT / CC-BY-4.0), and devoid of paywalls or subscription tiers.
2. **Independent Curator Validation:** Provides MetaMorpho vault managers with a neutral, third-party observatory to safeguard depositor capital and calibrate LLTV allocations.
3. **Scientific Proof of SVR Efficacy:** Our empirical research provides empirical proof that Chainlink SVR on Morpho Blue succeeds in eliminating toxic liquidation MEV, recapturing 98.10% for vault depositors. This strengthens institutional trust in Morpho's architecture.

---

### Metrics:
We define objective, machine-verifiable impact metrics:
1. **Market Coverage:** Expand real-time surveillance from 83 Base markets to **120+ active Morpho Blue markets** across Base and Arbitrum.
2. **Curator Integration:** Map and monitor at least **5 major MetaMorpho vaults** with dedicated health-distribution API endpoints (`/v1/radar/curator/{vault_address}`).
3. **Governance Reporting:** Publish at least **4 consecutive bi-weekly comprehensive liquidation & SVR risk digests** on the Morpho forum.
4. **Uptime & Telemetry Reliability:** Maintain **$\ge$ 99.8% uptime** on the public telemetry API (`api.werracle.com`) and observatory frontend throughout the grant period.

---

### Timeline:
- **Month 1 (Weeks 1–4): MetaMorpho Curator Architecture & Webhooks**
  - Week 1–2: Deploy MetaMorpho vault-to-market allocation schema and curator health breakdown charts.
  - Week 3–4: Build and test the configurable Discord/Telegram/Slack webhook alert engine for near-LLTV cohorts.
- **Month 2 (Weeks 5–8): Cross-Chain SVR Expansion & Governance Digest**
  - Week 5–6: Deploy Arbitrum Morpho Blue WebSocket ingestion and atomic multi-call receipt decoder.
  - Week 7–8: Implement automated forum digest reporting daemon and comparative L1 vs. L2 OEV analytics.

---

### Future directions (optional):
Following the successful completion of this pilot grant, our desk plans to introduce:
- An open-source **Predictive Bad Debt Simulation Engine** incorporating orderbook liquidity depth from Aerodrome and Uniswap v3 to model cascading slippage during extreme black-swan events.
- An interactive **Curator Allocation Simulator** allowing MetaMorpho managers to stress-test hypothetical market supply reallocations before on-chain execution.
