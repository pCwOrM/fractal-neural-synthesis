import os
import json
import csv
import shutil
import zipfile
from pathlib import Path
from huggingface_hub import HfApi

STAGING_DIR = Path("hf_dataset_staging")
ZIP_PATH = Path(r"C:\Setup\pcworm_server\oev_v2\replication_package_v2.zip")

def main():
    print("=== PREPARING HUGGING FACE DATASET v1.2 ===")
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    
    (STAGING_DIR / "data").mkdir(parents=True, exist_ok=True)
    (STAGING_DIR / "scripts").mkdir(parents=True, exist_ok=True)
    
    # 1. Extract files from replication_package_v2.zip
    with zipfile.ZipFile(ZIP_PATH) as z:
        raw_json_bytes = z.read("oev_replication_package_v2/data/werracle_oev_empirical_dataset_2026_v1.2.json")
        verify_py_bytes = z.read("oev_replication_package_v2/scripts/verify_onchain.py")
        reproduce_py_bytes = z.read("oev_replication_package_v2/scripts/reproduce_summary.py")
        
    data = json.loads(raw_json_bytes.decode("utf-8"))
    svr_data = data["svr_liquidations"]
    l1_data = data["l1_liquidations"]
    
    print(f"Loaded {len(svr_data)} SVR records and {len(l1_data)} L1 records.")
    
    # 2. Write SVR CSV
    svr_csv_path = STAGING_DIR / "data" / "svr_liquidations.csv"
    svr_cols = list(svr_data[0].keys())
    with open(svr_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=svr_cols)
        writer.writeheader()
        writer.writerows(svr_data)
    print(f"Saved {svr_csv_path} ({svr_csv_path.stat().st_size} bytes)")

    # 3. Write L1 CSV
    l1_csv_path = STAGING_DIR / "data" / "l1_liquidations.csv"
    l1_cols = list(l1_data[0].keys())
    with open(l1_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=l1_cols)
        writer.writeheader()
        writer.writerows(l1_data)
    print(f"Saved {l1_csv_path} ({l1_csv_path.stat().st_size} bytes)")

    # 4. Save JSON and scripts
    with open(STAGING_DIR / "data" / "werracle_oev_empirical_dataset_2026_v1.2.json", "wb") as f:
        f.write(raw_json_bytes)
    with open(STAGING_DIR / "scripts" / "verify_onchain.py", "wb") as f:
        f.write(verify_py_bytes)
    with open(STAGING_DIR / "scripts" / "reproduce_summary.py", "wb") as f:
        f.write(reproduce_py_bytes)
        
    # 5. Create updated README.md Dataset Card
    readme_content = """---
annotations_creators:
- machine-derived
- expert-generated
language:
- en
license: cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- tabular-regression
- tabular-classification
task_ids: []
pretty_name: "Werracle Verified Empirical OEV & Liquidation Dynamics Dataset (v1.2)"
tags:
- defi
- mev
- oev
- liquidations
- morpho-blue
- aave-v3
- chainlink-svr
- ethereum
- base
- arbitrum
- web3
- open-science
configs:
- config_name: svr_liquidations
  data_files: "data/svr_liquidations.csv"
- config_name: l1_liquidations
  data_files: "data/l1_liquidations.csv"
---

# Werracle Verified Empirical OEV & Liquidation Dynamics Dataset (v1.2)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23623588.svg)](https://doi.org/10.5281/zenodo.23623588)
[![Zenodo v2 Record](https://img.shields.io/badge/Zenodo_v2-Record_23642090-blue)](https://zenodo.org/records/23642090)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Observatory](https://img.shields.io/badge/Live_Observatory-radar.werracle.com-00ffcc)](https://radar.werracle.com)

## Summary (Dataset v1.2 / Monograph v2)

This dataset provides verified empirical execution records of **105 Chainlink Smart Value Recapture (SVR) transactions (513 liquidations)** across **Base L2** (plus 3 Arbitrum transactions) and **1,049 MEV-Boost liquidation transactions** across **Ethereum Mainnet (L1)**. Every figure in this version is re-derived on-chain using public RPC nodes.

It accompanies the academic research monograph:
> **"Empirical OEV and Liquidation Dynamics: Chainlink SVR Bid Recapture on Base and Builder-Payment Concentration on Ethereum L1"**  
> *Zenodo v2 Record:* [https://zenodo.org/records/23642090](https://zenodo.org/records/23642090)  
> *Parent Concept DOI:* [https://doi.org/10.5281/zenodo.23623588](https://doi.org/10.5281/zenodo.23623588)  
> *SSRN Abstract ID:* [7668638](https://papers.ssrn.com/abstract=7668638)

### Authors & Affiliations
- **Volkan Dağlı** (Anadolu University & ITouch Systems Research Desk, ORCID: [0009-0000-1587-8703](https://orcid.org/0009-0000-1587-8703))
- **Zerrin Dağlı** (Mersin University & Yusuf Kalkavan Anadolu Lisesi, ORCID: [0000-0001-9490-6425](https://orcid.org/0000-0001-9490-6425))
- **Dağhan Dağlı** (Toros Science High School, MEV / Toros University, ORCID: [0009-0003-2492-8313](https://orcid.org/0009-0003-2492-8313))
- **Contributor / Infrastructure Attribution:** Bekirhan Dağlı (ITouch Systems, Adana Çukurova Teknokent)

---

## Key Empirical Findings (v1.2 Re-Derived)

1. **Chainlink SVR Captures 94.38% of the Liquidation Incentive (OEV):**
   - Across 105 verified Base SVR transactions (86 on Morpho Blue, 19 on Aave v3), liquidators repaid **$1,898,755.19 ($1.90M)** of debt.
   - The gross **liquidation incentive (OEV pool)**—defined as seized collateral value minus repaid debt at oracle prices—was **$190,506.31**.
   - Winning solvers bid back **$179,807.38 (94.38%)** through the SVR auction directly into protocol SVR proceeds contracts (median transaction returned **98.30%**).
   - Solvers retained an aggregate gross margin of **5.58% ($10,630.95)** at oracle prices before DEX swap slippage (median transaction margin: **+1.26%**; 33 of 105 transactions were non-positive margin).
   - 17 solver contracts won auctions; the top 3 solvers captured **77.05%** of the incentive (Herfindahl-Hirschman Index **HHI ≈ 2,216**, indicating moderate-high concentration).
   - *Correction Note:* Bids accrue to SVR proceeds contracts shared between the protocol DAO and Chainlink; proceeds do not flow directly to individual depositors' wallets.

2. **Extreme Power-Law Centralization on Ethereum L1:**
   - Across 1,049 Ethereum L1 liquidations (22 Sep–22 Oct 2026), searchers paid **$366,112.89** in direct priority bribes to block builders via MEV-Boost.
   - The distribution exhibits extreme skew: **848 transactions (80.8%)** had builder priority payments under **$1.00 USD** (median: **$0.09 USD**).
   - The top **22 whale liquidations** accounted for **95.94%** of all builder fee payments.

---

## Dataset Schema

### 1. `svr_liquidations` (108 records: 105 Base L2 + 3 Arbitrum)
- `tx_hash` (string): On-chain transaction hash.
- `chain` (string): `base` or `arbitrum`.
- `venue` (string): `morpho_blue` or `aave_v3`.
- `timestamp_utc` (string): ISO 8601 block execution timestamp.
- `block` (int): Block height.
- `repaid_debt_usd` (float): Value of debt repaid in USD.
- `seized_collateral_usd` (float): Oracle-priced collateral seized in USD.
- `liquidation_incentive_usd` (float): Seized collateral minus repaid debt ($190,506.31 aggregate).
- `svr_bid_usd` (float): Actual ETH bid converted at transaction-time ETH price ($179,807.38 aggregate).
- `bid_share_pct` (float): `svr_bid_usd / liquidation_incentive_usd * 100`.
- `solver_margin_oracle_usd` (float): `liquidation_incentive_usd - svr_bid_usd`.
- `solver_margin_pct_of_incentive` (float): Margin percentage of the incentive.
- `liquidation_events` (int): Number of sub-liquidation calls bundled in the transaction (1 to 32).
- `winning_solver_contract` (string): Contract address of the winning solver.
- `status` (int): `1` for execution success.

### 2. `l1_liquidations` (1,049 records: Ethereum Mainnet)
- `tx_hash` (string): Ethereum transaction hash.
- `chain` (string): `ethereum_l1`.
- `protocol` (string): Lending protocol (`morpho_blue`, `aave_v2_v3`, `spark`, `euler_v2`, `fluid`, `compound`).
- `block` (int): Block height.
- `builder_payment_usd` (float): Priority fee bribe paid to block builder in USD ($366,112.89 total).
- `status` (int): `1` for execution success.

---

## Replication & Verification

The dataset includes offline and on-chain verification scripts:
```bash
# 1. Internal consistency check across all 54 headline metrics:
python scripts/reproduce_summary.py

# 2. Re-derive every metric from raw blockchain transaction receipts:
python scripts/verify_onchain.py --rpc-base https://mainnet.base.org --rpc-l1 https://eth.llamarpc.com
```

---

## Citation

```bibtex
@dataset{dagli_2026_werracle_oev_v2,
  author       = {Dağlı, Volkan and Dağlı, Zerrin and Dağlı, Dağhan and Dağlı, Bekirhan},
  title        = {{Empirical OEV and Liquidation Dynamics: Chainlink SVR 
                   Bid Recapture on Base and Builder-Payment Concentration 
                   on Ethereum L1}},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v2},
  doi          = {10.5281/zenodo.23642090},
  url          = {https://doi.org/10.5281/zenodo.23642090}
}
```

## Links & Live Observatory
- **Zenodo v2 Record:** [https://zenodo.org/records/23642090](https://zenodo.org/records/23642090)
- **Concept DOI:** [https://doi.org/10.5281/zenodo.23623588](https://doi.org/10.5281/zenodo.23623588)
- **Live Werracle Radar:** [https://radar.werracle.com](https://radar.werracle.com)
- **Production API:** [https://api.werracle.com/v1/radar/overview](https://api.werracle.com/v1/radar/overview)
- **GitHub Repository:** [https://github.com/pCwOrM/werracle](https://github.com/pCwOrM/werracle)
"""
    readme_path = STAGING_DIR / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Created {readme_path}")
    
    # 6. Upload to Hugging Face
    print("\nConnecting to Hugging Face API...")
    token_file = Path(r"C:\Users\maat\.cache\huggingface\token")
    with open(token_file, "r", encoding="utf-8") as f:
        token = f.read().strip()
        
    api = HfApi(token=token)
    repo_id = "pCwOrM/werracle-oev-liquidation-dataset-2026"
    
    print(f"Uploading staging folder to repo: {repo_id}...")
    api.upload_folder(
        folder_path=str(STAGING_DIR),
        repo_id=repo_id,
        repo_type="dataset",
        commit_message="v1.2: Re-derived on-chain metrics, liquidation incentive $190K / repaid debt $1.90M, SVR recapture 94.38% (Zenodo v2: 10.5281/zenodo.23642090)"
    )
    print(f"\nUpload complete! View at: https://huggingface.co/datasets/{repo_id}")

if __name__ == "__main__":
    main()
