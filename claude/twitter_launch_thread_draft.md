# [X / Twitter Launch Thread Draft] Independent SVR & OEV Risk Observatory

**Status:** DRAFT FOR INTERNAL REVIEW (NOT PUBLISHED)  
**Format:** 5-Tweet Technical Thread  
**Tone:** Objective, data-driven, empirical protocol research  

---

### Tweet 1 (Hook & Core Finding)
How effectively do Order Flow Auctions (OFA) recapture liquidation value for DeFi depositors?

We conducted an independent on-chain audit of all 105 Chainlink Smart Value Recapture (SVR) liquidations on Base Morpho ($190.5k gross) and 1,049 Ethereum L1 liquidations.

The data reveals a major shift in liquidation economics: 🧵👇

---

### Tweet 2 (Base SVR Efficiency)
Across 105 multi-call audited Base Morpho liquidations during the Oct 12–19 volatility window:

• Gross liquidated collateral: $190,506
• Recaptured protocol bids: $186,890 (98.10%)
• Solver gross share: $3,546 (1.86% pre-DEX slippage)
• L2 network gas: $71 (0.04%)

Competitive solver bidding returned ~98% of liquidation MEV directly back to Morpho depositors.

---

### Tweet 3 (Bertrand Compression)
Bertrand competition among permissionless Atlas solvers compresses margins to near zero:

• Median transaction margin: -1.55%
• 65 of 105 transactions (61.9%) concluded at breakeven or subzero margin before off-chain DEX slippage
• Cumulative negative margin losses: ~$2,500 USD

Liquidators are no longer extracting large windfalls; auction competition leaves thin operational spreads.

---

### Tweet 4 (Ethereum L1 Contrast)
In contrast, analyzing 1,049 Ethereum L1 liquidations via MEV-Boost shows extreme power-law centralization:

• 848 of 1,049 transactions (80.84%) paid < $1.00 in builder priority fees (median $0.08)
• Top 22 transactions accounted for $344,156 (96.05% of all builder bribes)
• Routine liquidations trigger minimal builder competition; whale events route through private builder auctions.

---

### Tweet 5 (Public Good Observatory & Research Paper)
We are releasing our surveillance radar and audited dataset as an open public good:

• Live Health Factor Surveillance (83 Morpho markets): https://radar.werracle.com
• Public Good Observatory: https://werracle.io/radar.html
• Full Academic Paper & Methodology: https://werracle.io/docs/EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md
• Raw Audited Dataset: https://radar.werracle.com/v1/radar/dataset

Built by @Werracle / ITouch Systems. Feedback from @MorphoLabs and risk curators welcome!
