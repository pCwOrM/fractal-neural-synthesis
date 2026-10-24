import os
import json
import csv
import shutil
from pathlib import Path
from huggingface_hub import HfApi

STAGING_DIR = Path("hf_dataset_staging")
ZENODO_PKG_DIR = Path("zenodo_oev_liquidation_package")

def main():
    print("=== PREPARING HUGGING FACE DATASET ===")
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    
    (STAGING_DIR / "data").mkdir(parents=True, exist_ok=True)
    (STAGING_DIR / "scripts").mkdir(parents=True, exist_ok=True)
    
    # 1. Load consolidated JSON
    raw_json_path = ZENODO_PKG_DIR / "data" / "werracle_oev_empirical_dataset_2026.json"
    with open(raw_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
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

    # 4. Copy raw JSON & verify script
    shutil.copy2(raw_json_path, STAGING_DIR / "data" / "werracle_oev_empirical_dataset_2026.json")
    shutil.copy2(ZENODO_PKG_DIR / "scripts" / "verify_dataset_metrics.py", STAGING_DIR / "scripts" / "verify_dataset_metrics.py")
    
    # 5. Create README.md Dataset Card
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
pretty_name: "Werracle Verified Empirical OEV & Liquidation Dynamics Dataset (2026)"
tags:
- defi
- mev
- oev
- liquidations
- morpho-blue
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

# Werracle Verified Empirical OEV & Liquidation Dynamics Dataset (2026)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23623588.svg)](https://doi.org/10.5281/zenodo.23623588)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Observatory](https://img.shields.io/badge/Live_Observatory-radar.werracle.com-blue)](https://radar.werracle.com)

## Summary

This dataset provides verified empirical execution records of **1,157 on-chain liquidation events** across **Ethereum Mainnet (L1)** and **Base/Arbitrum (L2)** recorded during the high-volatility window of **October 12–19, 2026**.

It accompanies the academic research monograph:
> **"Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1"**  
> *Zenodo Record:* [https://zenodo.org/records/23623589](https://zenodo.org/records/23623589)  
> *Parent DOI:* [https://doi.org/10.5281/zenodo.23623588](https://doi.org/10.5281/zenodo.23623588)

### Authors & Affiliations
- **Volkan Dağlı** (Anadolu University & ITouch Systems Research Desk, ORCID: [0009-0000-1587-8703](https://orcid.org/0009-0000-1587-8703))
- **Zerrin Dağlı** (Mersin University & Yusuf Kalkavan Anadolu Lisesi, ORCID: [0000-0001-9490-6425](https://orcid.org/0000-0001-9490-6425))
- **Dağhan Dağlı** (Toros Science High School, MEV / Toros University, ORCID: [0009-0003-2492-8313](https://orcid.org/0009-0003-2492-8313))
- **Contributor / Infrastructure Attribution:** Bekirhan Dağlı (ITouch Systems, Adana Çukurova Teknokent)

---

## Dataset Subsets & Schemas

The dataset is partitioned into two distinct empirical configurations:

### 1. `svr_liquidations` (108 records: 105 Base L2 + 3 Arbitrum)
Audited multi-call liquidation transactions routed through **Chainlink Smart Value Recapture (SVR)** via Atlas permissionless execution:
- `id` (string): Record identifier (`SVR-001` to `SVR-108`)
- `chain` (string): Blockchain network (`base`, `arbitrum`)
- `protocol` (string): Lending protocol (`Morpho Blue`, `Aave v3`)
- `market` (string): Target collateral/borrow market (e.g. `cbZEC/USDC`, `WETH/USDC`)
- `tx_hash` (string): Transaction hash on block explorer
- `gross_liquidation_usd` (float): Verified gross collateral liquidation value in USD
- `protocol_recapture_bid_usd` (float): Value redirected back to the protocol/vault via SVR bid
- `protocol_recapture_pct` (float): Percentage of gross value recaptured by protocol (`bid / gross * 100`)
- `gas_usd` (float): Transaction execution gas fee in USD
- `solver_pre_swap_net_usd` (float): Pre-swap net margin retained by solver (`gross - bid - gas`)
- `solver_margin_pct` (float): Solver pre-swap margin percentage (`pre_swap_net / gross * 100`)
- `liquidations_in_tx` (int): Number of multi-call liquidation sub-calls bundled in the transaction (1 to 32)
- `solver_contract` (string): Execution contract address of the solver
- `solver_signer` (string): EOA signer address submitting the bundle

### 2. `l1_liquidations` (1,049 records: Ethereum Mainnet)
Audited priority builder payments transferred via **MEV-Boost** (`block.coinbase.transfer()`) during liquidation execution:
- `id` (string): Record identifier (`L1-0001` to `L1-1049`)
- `chain` (string): Blockchain network (`ethereum_l1`)
- `protocol` (string): Protocol classification (`morpho_blue`, `aave_tipi`, `euler_v2`, `fluid`, `compound`)
- `tx_hash` (string): Ethereum transaction hash
- `block` (int): Ethereum block number
- `builder_payment_usd` (float): Direct bribe paid by MEV searcher to block builder in USD
- `success` (bool): Execution success status (`True`)

---

## Key Empirical Findings

1. **Chainlink SVR Captures 98.10% for Protocols:**
   Across 105 multi-call verified Base SVR transactions totaling **$190,506.31** in gross liquidation value, solvers submitted **$186,889.85 (98.10%)** directly back to lending protocols. Solvers retained only **1.86% ($3,545.73)** before off-chain DEX slippage, with median transaction margins compressed to **-1.55%**.
2. **Extreme Power-Law Centralization on Ethereum L1:**
   Across 1,049 Ethereum L1 liquidations, **848 transactions (80.84%)** had builder priority payments under **$1.00 USD** (median: **$0.08 USD**). Conversely, the top 22 whale liquidations accounted for **$344,155.62 (96.05%)** of all observed builder fees ($358,316.62 total).

---

## Quickstart (Python Hugging Face Datasets)

```python
from datasets import load_dataset

# 1. Load Chainlink SVR Liquidations (Base & Arbitrum)
svr_ds = load_dataset("pCwOrM/werracle-oev-liquidation-dataset-2026", "svr_liquidations")
print("SVR Records:", len(svr_ds["train"]))
print("Sample SVR Record:", svr_ds["train"][0])

# 2. Load Ethereum L1 MEV-Boost Liquidations
l1_ds = load_dataset("pCwOrM/werracle-oev-liquidation-dataset-2026", "l1_liquidations")
print("L1 Records:", len(l1_ds["train"]))
print("Sample L1 Record:", l1_ds["train"][0])
```

---

## Citation

If you utilize this dataset in academic research, protocol analysis, or MEV studies, please cite:

```bibtex
@dataset{dagli_2026_werracle_oev,
  author       = {Dağlı, Volkan and Dağlı, Zerrin and Dağlı, Dağhan},
  title        = {{Empirical OEV \& Liquidation Dynamics: Protocol Value 
                   Recapture in Chainlink SVR and Structural Centralization 
                   on Ethereum L1}},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.23623588},
  url          = {https://doi.org/10.5281/zenodo.23623588}
}
```

## Links & Live Infrastructure
- **Zenodo Record:** [https://zenodo.org/records/23623589](https://zenodo.org/records/23623589)
- **Live Werracle Radar:** [https://radar.werracle.com](https://radar.werracle.com)
- **Protocol Portal:** [https://werracle.io/radar.html](https://werracle.io/radar.html)
- **GitHub Repository:** [https://github.com/pcworm/wonderful-raman](https://github.com/pcworm/wonderful-raman)
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
        commit_message="Initial release: Werracle empirical OEV and liquidation dataset (Zenodo DOI: 10.5281/zenodo.23623588)"
    )
    print(f"Upload complete! View at: https://huggingface.co/datasets/{repo_id}")

if __name__ == "__main__":
    main()
