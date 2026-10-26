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
    print("=== EXTRACTING FULL REPLICATION PACKAGE FOR HUGGING FACE ===")
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Extract scripts/ and data/ from replication_package_v2.zip
    with zipfile.ZipFile(ZIP_PATH) as z:
        for member in z.namelist():
            if member.startswith("oev_replication_package_v2/scripts/") or member.startswith("oev_replication_package_v2/data/"):
                rel_path = member.replace("oev_replication_package_v2/", "")
                dest_path = STAGING_DIR / rel_path
                if member.endswith("/"):
                    dest_path.mkdir(parents=True, exist_ok=True)
                else:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(dest_path, "wb") as f:
                        f.write(z.read(member))
                    print(f"Extracted: {rel_path} ({dest_path.stat().st_size} bytes)")

    # 2. Also extract and convert v1.2 JSON to CSV for Hugging Face Web Viewer
    v12_json_path = STAGING_DIR / "data" / "werracle_oev_empirical_dataset_2026_v1.2.json"
    with open(v12_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    svr_data = data["svr_liquidations"]
    l1_data = data["l1_liquidations"]
    print(f"Extracted v1.2: {len(svr_data)} SVR rows, {len(l1_data)} L1 rows.")

    svr_csv_path = STAGING_DIR / "data" / "svr_liquidations.csv"
    with open(svr_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(svr_data[0].keys()))
        writer.writeheader()
        writer.writerows(svr_data)
    print(f"Generated {svr_csv_path} ({svr_csv_path.stat().st_size} bytes)")

    l1_csv_path = STAGING_DIR / "data" / "l1_liquidations.csv"
    with open(l1_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(l1_data[0].keys()))
        writer.writeheader()
        writer.writerows(l1_data)
    print(f"Generated {l1_csv_path} ({l1_csv_path.stat().st_size} bytes)")

    # 3. Create updated, clean README.md Dataset Card
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
> *arXiv Preprint:* [arXiv:2609.30719](https://arxiv.org/abs/2609.30719)  
> *SSRN Abstract ID:* [7626279](https://papers.ssrn.com/abstract=7626279)

### Authors & Affiliations
- **Volkan Dağlı** (ITouch Systems & Anadolu University, ORCID: [0009-0000-1587-8703](https://orcid.org/0009-0000-1587-8703))
- **Dr. Zerrin Dağlı** (Mersin University & Yusuf Kalkavan Anadolu Lisesi, ORCID: [0000-0001-9490-6425](https://orcid.org/0000-0001-9490-6425))
- **Dağhan Dağlı** (Toros Science High School / Toros University, ORCID: [0009-0003-2492-8313](https://orcid.org/0009-0003-2492-8313))
- **Contributor / Infrastructure Attribution:** Bekirhan Dağlı and the ITouch Systems Core Engineering Team (Adana Çukurova Teknokent)

---

## Dataset Subsets & Schemas

### 1. `svr_liquidations` (108 records: 105 Base L2 + 3 Arbitrum)
Audited multi-call liquidation transactions routed through **Chainlink Smart Value Recapture (SVR)** via Atlas permissionless execution:
- `id` (string): Record identifier (`SVR-001` to `SVR-108`)
- `chain` (string): Blockchain network (`base`, `arbitrum`)
- `protocol` (string): Lending protocol (`Morpho Blue`, `Aave v3`)
- `market` (string): Target collateral/loan asset pair
- `tx_hash` (string): Transaction hash
- `block_number` (int): Block number
- `timestamp_utc` (string): UTC execution timestamp
- `gross_liquidation_incentive_usd` (float): Gross collateral liquidation premium in USD
- `bid_amount_usd` (float): SVR recapture bid returned to protocol contracts
- `bid_share_pct` (float): Empirical recapture percentage (`bid / gross * 100`)
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
- `protocol` (string): Protocol classification (`morpho_blue`, `aave_v3`, `euler_v2`, `fluid`, `compound`)
- `tx_hash` (string): Ethereum transaction hash
- `block` (int): Ethereum block number
- `builder_payment_usd` (float): Direct bribe paid by MEV searcher to block builder in USD
- `success` (bool): Execution success status (`True`)

---

## Key Empirical Findings

1. **Chainlink SVR Captures 94.38% (Incentive-Weighted):**
   Across 105 multi-call verified Base SVR transactions (513 sub-liquidations) totaling **$190,506.31** in gross liquidation incentive ($1,898,755.19 repaid debt), solvers submitted **$179,807.38 (94.38%)** directly back to lending protocols. Median transaction recapture rate reached **98.33%**, with median solver margins compressed to **+1.26%** (and 33 of 105 transactions at zero or negative pre-swap margin).
2. **Extreme Fat-Tail Concentration on Ethereum L1:**
   Across 1,049 Ethereum L1 liquidations, the 22 largest whale liquidation transactions accounted for **$351,268.00 (95.94%)** of all builder payments ($366,112.89 total), while 848 transactions (80.84%) paid under $1.00 (median $0.09).

---

## Replication Scripts (Included in `scripts/`)

- `scripts/reproduce_summary.py`: Independently recalculates all 54 core summary statistics from `data/werracle_oev_empirical_dataset_2026_v1.2.json`.
- `scripts/verify_onchain.py`: Verifies transaction hashes against live Base and Ethereum RPC nodes.
- `scripts/build_v12.py`: Compiles the canonical v1.2 dataset bundle from v1.1 and audited additions.
- `scripts/make_figures.py`: Reproduces all research figures and charts.

---

## Citation

If you utilize this dataset in academic research, protocol analysis, or MEV studies, please cite:

```bibtex
@dataset{dagli_2026_werracle_oev_v12,
  author       = {Dağlı, Volkan and Dağlı, Zerrin and Dağlı, Dağhan},
  title        = {{Empirical OEV and Liquidation Dynamics: Chainlink SVR 
                   Bid Recapture on Base and Builder-Payment Concentration 
                   on Ethereum L1 (Dataset v1.2)}},
  month        = oct,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.2},
  doi          = {10.5281/zenodo.23623588},
  url          = {https://doi.org/10.5281/zenodo.23623588}
}
```

## Links & Live Infrastructure
- **Zenodo v2 Record:** [https://zenodo.org/records/23642090](https://zenodo.org/records/23642090)
- **Live Werracle Radar:** [https://radar.werracle.com](https://radar.werracle.com)
- **Protocol Portal:** [https://werracle.io](https://werracle.io)
- **Corporate Portal:** [https://werracle.com](https://werracle.com)
"""
    readme_path = STAGING_DIR / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"Created {readme_path}")
    
    # 4. Upload to Hugging Face
    print("\nConnecting to Hugging Face API...")
    token_file = Path(r"C:\Users\maat\.cache\huggingface\token")
    with open(token_file, "r", encoding="utf-8") as f:
        token = f.read().strip()
        
    api = HfApi(token=token)
    repo_id = "pCwOrM/werracle-oev-liquidation-dataset-2026"
    
    print(f"Uploading complete staging folder to repo: {repo_id}...")
    api.upload_folder(
        folder_path=str(STAGING_DIR),
        repo_id=repo_id,
        repo_type="dataset",
        commit_message="Release v1.2: Complete Zenodo replication package (scripts, data v1.2, build_v12.py, and tabular CSVs)"
    )
    print(f"Upload complete! View at: https://huggingface.co/datasets/{repo_id}")

if __name__ == "__main__":
    main()
