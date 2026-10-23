# [Grant Application Proposal] Werracle: Independent SVR & OEV Risk Observatory for Morpho Blue

**Target Forum:** Morpho DAO Forum (Grants & Risk Research Category)  
**Status:** DRAFT FOR INTERNAL REVIEW (NOT PUBLISHED)  
**Authors:** Werracle Research & Security Desk (`pcworm@pcworm.net`)  
**Observatory URLs:**  
- Web Dashboard: [https://radar.werracle.com](https://radar.werracle.com)  
- Public Good Observatory: [https://werracle.io/radar.html](https://werracle.io/radar.html)  
- JSON Telemetry API: [https://api.werracle.com/v1/radar/overview](https://api.werracle.com/v1/radar/overview)  
- Empirical Research Dataset: [https://radar.werracle.com/v1/radar/dataset](https://radar.werracle.com/v1/radar/dataset)  

---

### 1. Executive Summary

As decentralized lending scales, understanding Oracle Extractable Value (OEV) recapture dynamics is vital for depositors and risk curators. While Proposer-Builder Separation (PBS) on Ethereum L1 directs significant MEV priority fees to block builders, Chainlink Smart Value Recapture (SVR) on Base utilizes permissionless order flow auctions via Atlas metacalls.

We built and operate an **independent, public-good surveillance radar and telemetry observatory** monitoring 83 Morpho Blue markets and 69,000+ positions.

Through multi-call on-chain decoding of all 105 SVR liquidations occurring on Base Morpho during the October 12–19, 2026 volatility window ($190,506.31 gross liquidated collateral), our empirical data independently verifies that:
- **98.10% ($186,889.85 USD)** of gross liquidation value was recaptured and returned directly to Morpho vaults and depositors as competitive bids.
- Solver gross margins were compressed via intense Bertrand competition to **1.86% ($3,545.73 USD pre-DEX swap slippage)**.
- **61.9% (65 of 105 transactions)** concluded at zero or negative net margin prior to pool slippage, with median solver margin settling at **-1.55%**.

---

### 2. The Problem & Motivation

Lending protocols and risk curators (e.g. Gauntlet, Steakhouse, B.Protocol) require independent, real-time verification of liquidation auction performance:
1. **Auction Transparency:** Do OEV recapture mechanisms reliably return value to depositors during acute volatility?
2. **Health Factor Surveillance:** Providing public sub-second surveillance that clearly delineates active pre-liquidation risk horizons ($0.95 \le HF < 1.10$) from deeply insolvent bad debt ($HF < 0.95$, e.g. legacy oracle outliers).
3. **Multi-Chain Expansion:** Expanding verified empirical ingestion to Arbitrum and Ethereum L1.

---

### 3. Deliverables & What We Provide

1. **Live Independent Risk Observatory:**
   - 24/7 sub-second monitoring across all 83 Base Morpho Blue markets.
   - Clean risk categorization: Near Liquidation ($0.95 \le HF < 1.10$) vs Insolvent Bad Debt ($HF < 0.95$).
   - Publicly accessible at `https://radar.werracle.com` and `https://werracle.io/radar.html`.

2. **Open-Source Empirical Dataset & Multi-Call Decoder:**
   - Audited dataset of 108 verified SVR transactions and 1,049 L1 liquidation builder priority payments.
   - Reusable open-source scripts for community auditing of Atlas and Morpho liquidation logs.

3. **Theoretical Research on Upstream Protection:**
   - Formal exploration of permissioned borrower self-deleveraging delegations via Morpho's native `setAuthorization` mechanism.

---

### 4. Requested Grant Funding & Milestone Roadmap

We are applying under the Morpho Grants Program for tooling, risk research, and public infrastructure.

| Milestone | Deliverable | Scope | Timeline |
| :--- | :--- | :--- | :--- |
| **Milestone 1** (Completed) | Live Base Observatory & Verified SVR Dataset | 83 Morpho markets monitored, public JSON API, 105 audited SVR events | Delivered |
| **Milestone 2** | Arbitrum Morpho Ingestion & Rate-Limited Indexer | Expanding verified multi-call SVR decoding to Arbitrum Morpho instances with archival RPC handling | 4 Weeks |
| **Milestone 3** | Automated Weekly OEV Recapture Reports & Curator Alerts | Automated risk reporting module for Morpho vault curators and governance forum updates | 4 Weeks |

**Requested Funding:** 10,000 – 15,000 USDC (milestone-based distribution aligned with standard pilot grant allocations).

---

### 5. Team & Verification References

- **Lead:** Volkan Dağlı (ITouch Systems / Werracle Research)  
- **Codebase & Proofs:** [https://github.com/pCwOrM/werracle](https://github.com/pCwOrM/werracle)  
- **Empirical Paper:** [`docs/EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md`](https://github.com/pCwOrM/werracle/blob/main/docs/EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md)  
- **Live Status:** [https://radar.werracle.com/v1/radar/overview](https://radar.werracle.com/v1/radar/overview)  
