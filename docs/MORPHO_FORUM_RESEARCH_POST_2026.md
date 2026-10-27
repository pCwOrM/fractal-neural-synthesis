# Morpho Governance Forum (`forum.morpho.org`) — Doğrulanmış Nihai Araştırma Paylaşımı Paketi (v2)

> [!IMPORTANT]
> **Kesin Yayın Kategorisi (`forum.morpho.org` Canlı API Verisiyle Doğrulandı):**
> - **Kategori:** **[`Vaults` (`https://forum.morpho.org/c/vaults/17`)](https://forum.morpho.org/c/vaults/17)** *(122 aktif konu ile tüm MetaMorpho küratörlerinin — SteakHouse Financial, Gauntlet, BlockAnalitica, RE7, MEV Capital, Llama Risk, Clearstar Labs, Spark, Wintermute/Armitage — aktif olarak takip ettiği ana kategori.)*
> - **Başlık:** `[Research] Chainlink SVR liquidations on Base Morpho Blue: 94.4% of the liquidation incentive returned via auction bids (open dataset + live vault stress tool)`
> - **Durum:** Kaydedildi ve saklandı (`docs/MORPHO_FORUM_RESEARCH_POST_2026.md`). Forum hesabınız hazır olduğunda doğrudan kopyala-yapıştır ile yayınlanabilir.

---

## Doğrudan Kopyala-Yapıştır Forum Metni (Markdown — `forum.morpho.org` Uyumlu)

````markdown
**Authors:** Volkan Dağlı, Dr. Zerrin Dağlı, Dağhan Dağlı  
**Engineering & Infrastructure:** ITouch Systems · Cukurova University Science Park ([werracle.com](https://werracle.com) · [werracle.io](https://werracle.io))  
**Paper and data (open, CC BY 4.0):** [https://doi.org/10.5281/zenodo.23642090](https://doi.org/10.5281/zenodo.23642090) · [https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026](https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026)  
**Live Interactive Radar & API:** [https://radar.werracle.com](https://radar.werracle.com) · [https://radar.werracle.com/docs](https://radar.werracle.com/docs)

---

### Summary

We traced every Chainlink Smart Value Recapture (SVR) liquidation transaction our collector observed on Base between 2 and 22 October 2026 and re-derived all values from public RPC data (`debug_traceTransaction` internal call traces and exact liquidation-block oracle prices).

| Metric | Base L2 (Chainlink SVR / FastLane Atlas) |
|---|---|
| **Transactions** | `105` (`86` Morpho Blue, `19` Aave v3) |
| **Underlying Liquidations** | `513` (`65%` of transactions are multi-liquidation bundles) |
| **Repaid Debt** | **`$1.90M`** (`$1,901,711`) |
| **Gross Liquidation Incentive** (`seized collateral − repaid debt` at venue oracle price) | **`$190,506`** |
| **Winning SVR Bids** | **`$179,807` (`94.38%` of the incentive)** |
| **Kept by Solvers** (at oracle prices, before DEX price impact) | **`$10,631` (`5.58%` aggregate)** |
| **Median Transaction** | **`98.30%`** of incentive bid back; **median solver margin `+1.26%`** |
| **Winning Solver Contracts** | `17` unique contracts; top 3 capture `77%` of incentive (`HHI 2,216`) |

On **Morpho Blue alone**: `86` transactions, `484` liquidations, **`94.0%`** of the liquidation incentive bid back via SVR auctions.

For contrast, across `1,049` Ethereum Mainnet liquidations (`22 Sep – 22 Oct 2026`), direct builder payments (`priority fees + coinbase transfers`) totalled **`$366,113`**, with the `22` largest macro-cascade transactions accounting for **`95.9%`** of that amount. All figures reproduce deterministically from our open replication package (`verify_onchain.py`, `reproduce_summary.py`).

---

### What This Means for MetaMorpho Vaults

SVR auction bids flow to the SVR proceeds contracts shared by the protocol and Chainlink, not directly to vault depositors. For MetaMorpho curators, the critical operational question remains the liquidation path itself: **which borrowers become liquidatable, and how much bad debt the collateral cannot cover, if collateral prices drop.**

---

### Live Dual-Chain (`$4.73B`) Stress Tool Built on the Same Pipeline

We operate a real-time dual-chain surveillance index (`377` verified listed Morpho Blue markets across **Base L2** and **Ethereum Mainnet**, tracking **`$4.73B`** in active borrow and **`74,314`** open borrower positions) and publish a live MetaMorpho vault stress endpoint that reads up to the **10,000 largest positions per market** (~`95%` of total debt in the largest Base markets) and applies uniform collateral shocks of `5%–30%`:

- **Liquidatable condition:** $\text{debt} > \text{collateral} \times (1 - \text{shock}) \times \text{LLTV}$
- **Repayable debt:** $R = \min\!\left(\text{debt},\; \text{collateral}' / \text{LIF}\right)$, where $\text{LIF} = \min\!\left(1.15,\; \frac{1}{0.3 \cdot \text{LLTV} + 0.7}\right)$
- **Vault-attributed bad debt:** $(\text{debt} - R) \times \frac{\text{vault supply in market}}{\text{total market supply}}$

#### Live Model Output Snapshot (27 Oct 2026 — Estimates for Research & Risk Monitoring)

| MetaMorpho Vault | Chain | Vault TVL | Vault Bad Debt at `−20%` Shock | Vault Bad Debt at `−30%` Shock (% of TVL) |
|---|---|---|---|---|
| **Steakhouse USDC** | Base L2 | `$115.7M` | `$152K` | `$1.29M` (`1.1%`) |
| **Gauntlet USDC Prime** | Base L2 | `$412.5M` | `$588K` | `$4.93M` (`1.2%`) |
| **Steakhouse USDC** | Ethereum L1 | `$63.6M` | `$445K` | `$1.91M` (`3.0%`) |
| **Gauntlet USDC Prime** | Ethereum L1 | `$23.8M` | `$1.6K` | `$214K` (`0.9%`) |

*Scope note:* Uniform collateral shock curves cover volatile-collateral markets; correlated pairs (stable/stable, LST/ETH, BTC/BTC) are reported separately on our live radar because a uniform price drop does not move correlated pegs. Price paths, cascades, DEX depth, and pre-liquidations are not modelled.

---

### Back-Test Against the 12–19 October 2026 Base Sell-Off

We replayed our position-flagging model day by day against the 12–19 October 2026 sell-off on Base: with a daily refresh, positions flagged in advance covered **`99.8%` (`606 / 615` positions, `$1.67M` debt)** of the debt that was actually liquidated (precision `70.7%`, as many flagged borrowers added collateral or repaid in time).

- **Live Interactive Radar & Shock Simulator:** [https://radar.werracle.com](https://radar.werracle.com) (free public endpoints require no API key)
- **Methodology, Back-Test & OpenAPI Docs:** [https://radar.werracle.com/docs](https://radar.werracle.com/docs)

Curators and risk researchers who would like a complimentary Institutional API key for the live `/v1/radar/curator/{vault}` stress and Webhook/Telegram alert endpoints can reply in this thread or write to `contact@werracle.com`. Feedback on the methodology—especially regarding correlated pairs and pre-liquidation hooks—is very welcome.
````
