# Formally Verified Lean 4 Port of GAP: Computational Discrete Algebra

[![Lean 4](https://img.shields.io/badge/Lean_4-v4.28.0-blue.svg)](https://lean-lang.org/)
[![Lean 4 CI](https://github.com/pCwOrM/gap-lean4-port/actions/workflows/lean_build.yml/badge.svg)](https://github.com/pCwOrM/gap-lean4-port/actions/workflows/lean_build.yml)
[![Zulip Chat](https://img.shields.io/badge/zulip-solfunmeme-blue.svg)](https://solfunmeme.zulipchat.com/)
[![Mathlib 4](https://img.shields.io/badge/Mathlib_4-compatible-green.svg)](https://github.com/leanprover-community/mathlib4)
[![Release](https://img.shields.io/badge/Release-v0.2.0-orange.svg)](https://github.com/pCwOrM/gap-lean4-port/releases/tag/v0.2.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23045504.svg)](https://doi.org/10.5281/zenodo.23045504)
[![Concept DOI](https://img.shields.io/badge/Concept_DOI-10.5281%2Fzenodo.23045503-blue.svg)](https://doi.org/10.5281/zenodo.23045503)
[![Verification](https://img.shields.io/badge/Verification-35_Theorems_%7C_0_sorry_%7C_0_admit-brightgreen.svg)](https://github.com/pCwOrM/gap-lean4-port)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository provides **machine-checked formal verifications in Lean 4 / Mathlib** for the core computational discrete algebra algorithms and representations of the [GAP System](https://www.gap-system.org/) (Groups, Algorithms, Programming).

Developed by the **ITouch Systems Formal Verification Lab** (Volkan Dagli [@pCwOrM] & Family).

---

## What's New in Release v0.2.0 (Phase 2 Milestone)

Release **v0.2.0** advances beyond static residue structures into **verified operational computational group theory and backtrack combinatorial algorithms**, formalizing three major modules from GAP 4's core library with **0 sorry, 0 admit, and 0 external axioms**:

1. **GAP-0299 (`lib/stbc.gi`): Schreier-Sims Stabiliser Chains & Transversal Invariants**
2. **GAP-0332 (`lib/partitio.gi`): Backtrack Ordered Partitions & Cell Refinement Invariants**
3. **GAP-0332 (`lib/zmodnze.gi`): Rings $\mathbb{Z}/n\mathbb{Z}(\varepsilon_m)$ of Cyclotomic Extensions**
4. **GAP-0331 (`lib/zmodnz.gi`): Modular Residue Methods, Invertibility & Extended Euclidean GCD**

---

## 1. Stabiliser Chains & Schreier-Sims Algorithms (`lib/stbc.gi`)

Module: `RequestProject.Gap.Library.Stbc`  
GAP Reference: `lib/stbc.gi` (by Heiko Theißen and Ákos Seress)

Faithfully models GAP's stabiliser chain hierarchy, transversal trees, sifting reductions, and Base & Strong Generating Set (BSGS) membership testing:

* **Core Structures:**
  * `GAP.Stbc.StabLevel`: Models each chain level $(\beta_i, \Delta_i, S_i, u_i)$ with base point, basic orbit, generators, and inverse transversal representatives.
  * `GAP.Stbc.StabChain`: The complete descending stabiliser chain $[G^{(1)}, G^{(2)}, \dots, G^{(k)}]$.
* **Operational Algorithms:**
  * `siftOneLevel`: Single-level coset reduction $g \mapsto u_y^{-1} \cdot g$.
  * `siftFull` / `siftedPermutation`: Full multi-level Schreier sifting across the base.
  * `membershipTestKnownBase`: Group membership decision procedure using sifting.
  * `extendSchreierPoint`: Transversal tree extension step.
* **Verified Theorems (0 sorry):**
  * `siftOneLevel_fixes_basePoint`: Proves that single-level sifting strictly fixes the base point $\beta_i$.
  * `siftFull_fixes_all_basePoints`: Proves that a fully sifted element fixes every base point in the base sequence $(\beta_1, \dots, \beta_k)$.
  * `siftedPermutation_mem_subgroup_iff`: Invariant preservation during coset reduction.
  * `membershipTestKnownBase_sound`: Proves that if membership test returns `true`, then $g \in G$.
  * `membershipTestKnownBase_iff_mem`: Soundness and completeness equivalence for subgroup membership.
  * `extendSchreierPoint_invariant`: Invariant preservation of the transversal tree under tree extension.

---

## 2. Ordered Partitions for Backtrack Searching (`lib/partitio.gi`)

Module: `RequestProject.Gap.Library.Partitio`  
GAP Reference: `lib/partitio.gi` (by Heiko Theißen)

Models ordered partitions and cell refinement operations fundamental to GAP's permutation group backtrack search, partition backtracks, and automorphism computation:

* **Core Structures:**
  * `GAP.Partitio.OrderedPartition`: Partition of $\Omega$ into ordered, non-empty, pairwise disjoint cells.
  * `fixcells`: Identifies cells consisting of a single fixed point (size 1).
  * `splitCellByPred`: Core cell-splitting primitive underlying `SplitCell` and `IsolatePoint`.
* **Verified Theorems (0 sorry):**
  * `splitCellByPred_disjoint`: Formally proves that cell splitting always yields mutually disjoint subcells.
  * `splitCellByPred_union`: Proves exact element conservation (the union of subcells equals the original cell).
  * `splitCellByPred_length_sum`: Proves cardinality conservation $|C_{yes}| + |C_{no}| = |C|$.
  * `mem_splitCellByPred_iff`: Characterizes exact predicate-driven membership in split cells.

---

## 3. Cyclotomic Extension Rings $\mathbb{Z}/n\mathbb{Z}(\varepsilon_m)$ (`lib/zmodnze.gi`)

Module: `RequestProject.Gap.Library.Zmodnze`  
GAP Reference: `lib/zmodnze.gi` (by Alexander Konovalov)

Formalizes elements and arithmetic of GAP's cyclotomic extension rings $\mathbb{Z}/n\mathbb{Z}(\varepsilon)$, where $\varepsilon^m = 1$:

* **Core Structures:**
  * `ZmodnZepsObj`: Formal representation via coefficient vectors `Fin m → GAP.ZModnZObj n`.
  * `AddCommGroup` and convolution group-ring multiplication `mulOp`.
* **Verified Theorems (0 sorry):**
  * `card_eq`: Machine-checks GAP's exact `Size` formula:
    $$\text{card}(\mathbb{Z}/n\mathbb{Z}(\varepsilon_m)) = n^m$$

---

## 4. $\mathbb{Z}/n\mathbb{Z}$ Modular Residue Methods (`lib/zmodnz.gi`)

Module: `RequestProject.Gap.Library.Zmodnz`  
GAP Reference: `lib/zmodnz.gi` (by Thomas Breuer)

Dual verification architecture combining abstract mathematical isomorphism with operational executable algorithms:

1. **Semantic Model Isomorphism:** Canonical bijection `ZModnZObj n ≃ ZMod n`, deriving `CommRing` and `Field` (for prime $n$), with unit theorem `IsUnit a ↔ a.val.Coprime n`.
2. **Constructive Executable Algorithms:** Verified `isUnitExec` and constructive `inverseOpExec` via the Extended Euclidean Algorithm (`Nat.gcdA` Bézout coefficients) without non-constructive choice:
   ```lean
   theorem inverseOpExec_correct (a : ZModnZObj n) (h : isUnitExec a = true) :
       ∃ inv : ZModnZObj n, inverseOpExec a = some inv ∧ mulExec a inv = oneExec
   ```

---

## Axiomatic Purity Audit

Every theorem in this repository has been audited with `#print axioms`:

| Module | GAP Source | Theorems | `sorry` | External Axioms | Foundations |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `Stbc.lean` | `lib/stbc.gi` | 8 | **0** | **0** | `propext, Classical.choice, Quot.sound` |
| `Partitio.lean` | `lib/partitio.gi` | 6 | **0** | **0** | `propext, Classical.choice, Quot.sound` |
| `Zmodnze.lean` | `lib/zmodnze.gi` | 4 | **0** | **0** | `propext, Classical.choice, Quot.sound` |
| `Zmodnz.lean` | `lib/zmodnz.gi` | 17 | **0** | **0** | `propext, Classical.choice, Quot.sound` |
| **Total** | | **35** | **0** | **0** | Standard Lean 4 Core |

---

## Build Instructions

```bash
# Clone the repository
git clone https://github.com/pCwOrM/gap-lean4-port.git
cd gap-lean4-port

# Build the entire verified library
lake build RequestProject
```

---

## Authors & Citation

**ITouch Systems Formal Verification Lab**  
* Volkan Dagli ([@pCwOrM](https://github.com/pCwOrM)) & Family  
* Research Lab: Mersin / Istanbul, Turkey  

Correspondence: `ask@answerr.me` | `pcworm@pcworm.net`

---

## Community, Collaboration & Standards

* **Zulip Channel:** Join real-time technical discussions on our Zulip realm at [solfunmeme.zulipchat.com](https://solfunmeme.zulipchat.com/) (Streams: `#general > greetings`, `#general > architecture`).
* **Shared Terminology Standard:** Collaborative formal verification standard defined in [Shared Terminology Guide v2](docs/SharedTerminologyGuide.md) (DuPont–Dağlı Specification).
* **Rung 0–5 Verification Ledger:** Formal accounting of chunks, anchors, pre/post/frame contracts, and degree qualifiers in [docs/RUNG_LEDGER.md](docs/RUNG_LEDGER.md).
* **Distributed Architecture:** Dual-engine Lean 4 + eBPF/Nix architecture in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

### Citation

If you build upon or reference this formal verification, please cite:

```bibtex
@software{dagli_2026_gap_lean4,
  author       = {Dağlı, Volkan and Dağlı, Zerrin and Dağlı, Dağhan},
  title        = {{Machine-Checked Computational Group Theory in Lean 4: Operational Schreier-Sims Stabilizer Chains, BSGS Sifting, and Backtrack Ordered Partitions}},
  month        = sep,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v0.2.0},
  doi          = {10.5281/zenodo.23045504},
  url          = {https://doi.org/10.5281/zenodo.23045504}
}
```
