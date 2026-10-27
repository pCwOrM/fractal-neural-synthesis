# Morpho Governance Forum (`forum.morpho.org`) — Araştırma Paylaşımı Paketi

> [!IMPORTANT]
> **Kesin Yayın Kategorisi (`forum.morpho.org` Canlı API Verisiyle Doğrulandı):**
> - **Seçilecek Kategori:** **[`Vaults` (`https://forum.morpho.org/c/vaults/17`)](https://forum.morpho.org/c/vaults/17)** *(122 aktif konu ile tüm MetaMorpho küratörlerinin — SteakHouse Financial, Gauntlet, BlockAnalitica, RE7, MEV Capital, Llama Risk, Clearstar Labs, Spark, Wintermute/Armitage — aktif olarak takip ettiği ana kategori. `Morpho Blue → General` kategorisinde Ocak 2024'ten beri yalnızca 1 konu bulunduğu için kesinlikle kullanılmamalıdır.)*
>
> **Amaç:** Morpho ekosistemi küratörlerini ve risk ekiplerini doğrudan **[`radar.werracle.com`](https://radar.werracle.com/v1/radar/dashboard)** canlı API ve 1-Tık Kurumsal Abonelik (`499 USDC/ay`) sayfasına çekmek.

---

## 1. Forum Başlığı (Topic Title) ve Kesin Kategori

- **Title (Başlık):**
  `[Empirical Study & Live Tooling] 94.38% OEV Recapture in Base Morpho Blue SVR Liquidations & Dual-Chain ($4.73B) MetaMorpho Vault Stress Telemetry`
- **Category (Kesin Kategori):** **`Vaults`** ([`https://forum.morpho.org/c/vaults/17`](https://forum.morpho.org/c/vaults/17)) *(Alt kategori seçmeden doğrudan ana `Vaults` kategorisi)*

---

## 2. Doğrudan Kopyala-Yapıştır Forum Metni (Markdown — `forum.morpho.org` Uyumlu)

Aşağıdaki İngilizce metin, `forum.morpho.org` editörüne doğrudan yapıştırılabilecek şekilde standart Discourse Markdown formatında hazırlanmıştır:

````markdown
# Empirical Analysis of Chainlink SVR Liquidations on Base Morpho Blue (94.38% OEV Recapture) & Live Dual-Chain ($4.73B) MetaMorpho Vault Stress Telemetry

**Authors:** Volkan Dağlı, Dr. Zerrin Dağlı, Dağhan Dağlı  
**Engineering & Infrastructure:** ITouch Systems · Çukurova University Science Park ([werracle.com](https://werracle.com) · [werracle.io](https://werracle.io))  
**Live Public Dashboard & REST API:** [https://radar.werracle.com/v1/radar/dashboard](https://radar.werracle.com/v1/radar/dashboard)  
**Interactive Swagger / OpenAPI:** [https://radar.werracle.com/docs](https://radar.werracle.com/docs)  
**Archival Dataset & Paper (CERN Zenodo v2):** [https://doi.org/10.5281/zenodo.23642090](https://doi.org/10.5281/zenodo.23642090)

---

## TL;DR (Executive Summary for Curators & Risk Teams)

1. **Base Morpho Blue Chainlink SVR Recapture (`94.38%` Aggregate / `98.30%` Median):**  
   By decoding full internal call traces (`debug_traceTransaction`) across **105 multi-call Chainlink SVR / FastLane Atlas liquidation transactions** (`513` underlying Morpho Blue `Liquidate` events, **$3,871,334.72** in repaid debt), we find that permissionless Dutch-style OEV auctions recapture **$168,857.16 (`94.38%`)** of the **$178,904.60** gross liquidation incentive for the protocol/oracle layer, leaving solvers a competitive net margin of **`+1.26%` (`$2,262.13`)** after gas and flash-loan costs.
2. **Contrast with Ethereum L1 PBS (`0.00%` Protocol Recapture):**  
   Across **1,049 historical Ethereum L1 liquidations** (**$32.16M** debt repaid), **$366,113.48** in priority fees and `block.coinbase` bribes leaked entirely to block builders (`0.00%` protocol recapture), with the top 22 macro-cascade transactions accounting for **`95.9%`** of all extracted MEV.
3. **Live Dual-Chain (`Base L2` + `Ethereum Mainnet`) Morpho Blue Surveillance (`$4.73B` Monitored Debt):**  
   We operate a real-time shadow indexer and REST API ([`radar.werracle.com`](https://radar.werracle.com/v1/radar/dashboard)) tracking **377 verified listed Morpho Blue markets** (`38` on Base L2 + `339` on Ethereum Mainnet), **$4.73 Billion in active borrow**, and **74,314 live borrower positions** (`68,534` on Base + `5,780` on Ethereum Mainnet).
4. **Pro-Rata MetaMorpho Vault Stress Testing & Instant Push Telemetry (`HF < 1.05`):**  
   Curators can query live collateral shock simulations (`-5%`, `-10%`, `-15%`, `-20%`, `-30%`) attributed pro-rata to each MetaMorpho vault’s exact market allocation (`supplyAssetsUsd / market.SupplyAssetsUsd`), alongside HMAC-SHA256 signed Webhook & Telegram push alerts.

---

## 1. Methodology: Why Multi-Call Trace Decoding Matters on Morpho Blue

Standard event-log scrapers that inspect only a single `Liquidate` log per transaction systematically mismeasure solver margins on Base L2 because professional solvers batch multiple borrower liquidations inside a single FastLane Atlas `metacall` bundle.

In our v1.2 audit ([Zenodo DOI: `10.5281/zenodo.23642090`](https://doi.org/10.5281/zenodo.23642090)):
- We aggregate **all `513` Morpho Blue `Liquidate` events** emitted across the **105 multi-call SVR transactions** on Base.
- We value repaid debt and seized collateral at the **exact liquidation block’s oracle price** (`collateralPrice / 10^(36 + loanDecimals - collateralDecimals)`).
- We separate gross liquidation incentive (`seized_usd - repaid_usd`) into:
  1. **Protocol / SVR Auction Bid Recapture (`$168,857.16`)**
  2. **Net Solver Margin (`+$2,262.13`, or `+1.26%` of gross incentive; `+4.28%` median per-tx)**

| Chain | OEV / MEV Architecture | Sample Size | Total Debt Repaid (USD) | Gross Liquidation Incentive / MEV | Protocol / Oracle Recapture | Solver / Builder Share |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Base L2** (`chainId: 8453`) | Chainlink SVR / Atlas Metacall | 105 tx (`513` liquidations) | `$3,871,334.72` | `$178,904.60` | **`94.38%`** (Median `98.30%`, `$168,857.16`) | **`+1.26%`** (Median `+4.28%`, `$2,262.13`) |
| **Ethereum Mainnet** (`chainId: 1`) | PBS / MEV-Boost Bribes | 1,049 liquidations | `$32,164,890.15` | `$366,113.48` (Builder Bribes) | **`0.00%`** | **`100.00%`** to Block Builders (Top 22 tx = `95.9%`) |

---

## 2. Live Dual-Chain Morpho Blue Surveillance (`Base L2` + `Ethereum Mainnet`)

To ensure institutional risk metrics are never distorted by unverified or spam markets with artificial oracle prices, our indexer strictly filters for `listed: true` markets and cross-checks position-level health factors (`HF < 1.10` and `HF < 1.05`):

- **Base L2 (`chainId: 8453`):** `38` verified listed markets (`47` unlisted filtered) • **`$2.21B`** monitored borrow • **`68,534`** tracked positions.
- **Ethereum Mainnet (`chainId: 1`):** `339` verified listed markets (`1,227` unlisted filtered) • **`$2.52B`** monitored borrow • **`5,780`** tracked positions.
- **Combined Surveillance:** **`377` verified listed Morpho Blue markets** • **`$4.73B` monitored debt** • **`74,314` open positions**.

### Free Public Verification Endpoints (No API Key Required)
Anyone in the Morpho community can verify the live telemetry right now via `curl` or browser:
- **Dual-Chain Overview:** [`GET https://radar.werracle.com/v1/radar/overview`](https://radar.werracle.com/v1/radar/overview)
- **Cross-Chain OEV Breakdown:** [`GET https://radar.werracle.com/v1/radar/chains`](https://radar.werracle.com/v1/radar/chains)
- **Supported MetaMorpho Vaults (Base & ETH Mainnet):** [`GET https://radar.werracle.com/v1/radar/curator/vaults`](https://radar.werracle.com/v1/radar/curator/vaults)
- **Empirical Dataset Summary:** [`GET https://radar.werracle.com/v1/radar/dataset`](https://radar.werracle.com/v1/radar/dataset)

---

## 3. Live Pro-Rata MetaMorpho Vault Stress Testing (`Steakhouse`, `Gauntlet`, `Spark`, `Moonwell`)

When a MetaMorpho vault supplies liquidity to a Morpho Blue market, its exposure to liquidatable debt and bad debt under a sudden collateral drawdown (`-5%` to `-30%`) is proportional to its share of that market's total supply (`vault_allocation_usd / market_total_supply_usd`).

Our engine (`/v1/radar/curator/{vault}`) fetches the live borrower positions (`up to 100 largest positions per allocated market`) and computes:
1. **Vault-Attributed Liquidatable Debt (`HF' < 1.00`)** at `-5%`, `-10%`, `-15%`, `-20%`, and `-30%` instant collateral price shocks.
2. **Estimated Liquidation Incentive (OEV)** generated according to each market’s exact `LLTV` and Morpho Blue’s `LIF` formula (`min(1.15, 1 / (1 - 0.3 * (1 - LLTV)))`).
3. **Vault-Attributed Bad Debt Exposure** (`repaid_debt_usd > post_shock_collateral_usd / LIF`).
4. **Recommended Liquidation Reserve Buffer (bps of TVL).**

### Snapshot of Live MetaMorpho Vault Stress Telemetry (October 2026)

| MetaMorpho Vault | Chain | Vault TVL (USD) | Active Borrowers Sampled | `-10%` Shock Liquidatable Debt | `-15%` Shock Liquidatable Debt | `-20%` Shock Bad-Debt Exposure | Recommended Reserve Buffer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Steakhouse Prime USDC** (`steakhouse-eth`) | Ethereum L1 | `$364.86M` | 200 | `$494.6K` | `$51.42M` | `$189.2K` | `35 bps` |
| **Gauntlet USDC Prime** (`gauntlet-eth`) | Ethereum L1 | `$185.64M` | 400 | `$3.29M` | `$24.66M` | `$172.9K` | `35 bps` |
| **Steakhouse High Yield** (`steakhouse`) | Base L2 | `$10.31M` | 300 | `$163.3K` | `$1.32M` | `$19.4K` | `39 bps` |
| **Moonwell Flagship USDC** (`moonwell`) | Base L2 | `$17.64M` | 200 | `$161.4K` | `$1.50M` | `$3.9K` | `35 bps` |

---

## 4. Real-Time Webhook & Telegram Push Alerts (`HF < 1.05`)

In addition to polling the REST API, curators and liquidators can subscribe to real-time push alerts via [`POST /v1/radar/alerts/subscribe`](https://radar.werracle.com/v1/radar/dashboard#alerts-section):
- **HMAC-SHA256 Signed Webhooks:** Delivers structured JSON payloads with `X-Werracle-Signature-256` whenever a monitored market breaches a configurable Health Factor threshold (default `HF < 1.05`) or collateral shock threshold.
- **Telegram Bot API Push:** Instant formatted alerts delivered directly to your risk team's Telegram channel.

---

## 5. Open Access for Researchers & Curators

- **Explorer & Academic Tier (`$0 / Free`):** Open access (`30 req/min`, no API key required) to `/overview`, `/chains`, `/dataset`, `/curator/vaults`, and top-25 `/hot-positions`.
- **Pro & Institutional Curator Tiers:** Instant self-serve API key provisioning via Base USDC (`1-Click Wallet`), Multi-Chain USDT/USDC, or Credit Card on [`radar.werracle.com`](https://radar.werracle.com/v1/radar/dashboard#subscribe-section).
- **Complimentary Curator Review Keys:** We are happy to provide complimentary Institutional VIP API keys (`3,000 req/min` + full `/curator/{vault}` stress endpoints) to active MetaMorpho curators and Morpho governance contributors—reply in this thread or reach out at `contact@werracle.com`.
````

---

## 3. Yayınlama Adımları (3 Dakikalık Kontrol Listesi)

1. Tarayıcıdan [`https://forum.morpho.org`](https://forum.morpho.org) adresine giriş yapın ve sağ üstteki **"+ New Topic"** butonuna tıklayın.
2. **Title** alanına yukarıdaki 1. bölümdeki başlığı, **Category** alanına doğrudan **`Vaults`** ([`https://forum.morpho.org/c/vaults/17`](https://forum.morpho.org/c/vaults/17)) kategorisini seçin.
3. Yukarıdaki 2. bölümdeki Markdown kutusunun sağ üst köşesindeki **Kopyala** butonuna basıp forum gövdesine yapıştırın.
4. Paylaşım sonrası oluşan forum linkini `werracle.com` ve `radar.werracle.com` üzerindeki referans bağlantılarına da ekleyebiliriz.
