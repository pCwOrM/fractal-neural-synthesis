# 📜 REPLICATION PACKAGE: ZERO-STORAGE PROCEDURAL NEURAL SYNTHESIS VIA BOUNDARY DYNAMICS
### Formal Verification in Lean 4 and Bare-Metal 40-Core Gauntlet Validation

**Authors:** Volkan Dağlı$^{1,2}$, Dr. Zerrin Dağlı$^3$, Dağhan Dağlı$^4$  
**Affiliations:**  
$^1$Anadolu University, Turkey  
$^2$ITouch Systems, Turkey (ORCID: 0009-0000-1587-8703)  
$^3$Mersin University, Turkey (ORCID: 0000-0001-9490-6425)  
$^4$Toros Science College, Turkey (ORCID: 0009-0003-2492-8313)  

**Permanent Archival Identifiers:**  
- CERN Zenodo Concept DOIs: `10.5281/zenodo.22896856`, `10.5281/zenodo.22774934`, `10.5281/zenodo.22939253`, `10.5281/zenodo.22942599`
- Preprints: arXiv:2609.25498, arXiv:2609.30115
- TÜRKPATENT Priority: TR 2026/016285 (Priority Date: 22 September 2026)

---

## 1. Package Contents

| File | Description | SHA-256 Checksum |
| :--- | :--- | :--- |
| `WerracleProof.lean` | Complete Lean 4 formal machine proof (Mathlib4, 0 sorry, 0 unproven axioms) | `66b7d41c372d95cbc6b45dcc60f78fd9b7b7ae278c50be006eba3cb076b9a348` |
| `werracle_lean4_formal_verification_certificate.md` | Cryptographic verification certificate & theorem audit | Verified |
| `OED_40CORE_GAUNTLET_SEAL.json` | Bare-metal 40-core gauntlet benchmark seal (100k decisions, 15,397 dec/s) | `94ddaefb17989c9031697779d95f35f7cd5ea3a2bea36ef4c91db1a270061550` |
| `benchmark_oed_40cores.py` | Standalone Python 3 benchmark script reproducing 40-core gauntlet | Reproducible |
| `ablation_experiment_3arms.py` | 3-arm ablation script across 180 semi-primes (40–56 bits) | Reproducible |
| `main.tex` | Full LaTeX manuscript source | Validated |
| `Zero_Storage_Neural_Synthesis_Lean4_OED.pdf` | Camera-ready two-column publication PDF | Complete |
| `ACADEMIC_RESEARCH_PAPER_FULL.md` | Full-length comprehensive academic treatise & empirical report | Complete |

---

## 2. Replicating the Lean 4 Formal Verification

### Prerequisites:
- Lean 4 toolchain (v4.34.1 or compatible)
- Lake (Lean 4 build system)
- Mathlib4

### Verification Command:
```bash
# Type-check and verify all theorems with zero axioms beyond propositional extensionality (propext)
lean WerracleProof.lean
```

### Verified Theorems:
1. `escape_halts_bounded`: $\forall (c_x, c_y) \in \mathbb{Z}^2, \text{escape\_zmod9}(c_x, c_y) \le 9$.
2. `tripod_point_count_invariant`: $\text{sparse\_tripod\_eval\_count} = 12$.
3. `global_execution_bound`: $\text{sparse\_tripod\_eval\_count} \times 9 = 108\text{ steps}$.
4. `gas_ceiling_passed`: $22,568 \le 24,000\text{ gas}$.

---

## 3. Replicating the Bare-Metal Gauntlet Benchmark

### Execution:
```bash
python benchmark_oed_40cores.py
python ablation_experiment_3arms.py
```

### Hardware Reference:
- Dual Intel Xeon E5-2630 v4 (20 Physical Cores / 40 Threads)
- 256 GB DDR4 ECC RAM
- Ubuntu 24.04 LTS (Performance governor)
- Measured Throughput: **15,397.4 decisions/s** at **0 Bytes VRAM**

---

## 4. License & Citation
This replication package is released under the **Creative Commons Attribution 4.0 International (CC-BY-4.0)** license.
