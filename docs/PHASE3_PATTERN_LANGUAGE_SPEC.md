# Phase 3 Pattern Language Specification & IPLD CAR Bridge
**Standard:** Shared Terminology Guide v2 (DuPont–Dağlı Specification)  
**Authors:** Volkan Dağlı (@pCwOrM) & Mike DuPont (@jmikedupont2)  
**Project:** Distributed Formal Verification of GAP in Lean 4  
**Taskset Root CID:** `baguqeeraykhbhp2afmcuxp7dpgb72dhnpkng2qpcybegfu3lqqdilezq3hzq`  
**Repository:** [pCwOrM/gap-lean4-port](https://github.com/pCwOrM/gap-lean4-port)  
**Status:** Canonical Pre-Execution Blueprint  

---

## 1. Executive Purpose & Scope

This specification formalizes the **Pattern Language** requested by collaborator Mike DuPont for Phase 3 execution, establishing a rigorous contract standard between:
1. **The Lean 4 Formal Verification Layer (`pCwOrM`):** Branch-by-branch modeling (Rung 1) and zero-`sorry` axiomatic proofs (Rung 3).
2. **The P2P Tracing & Provenance Layer (`lean-worker` / `aristotle-cli-rs`):** Pinned Nix derivation `build-id` provenance and eBPF C-boundary execution traces (Rung 4b).
3. **The IPLD CARv1 Task Ledger:** Content-addressed DAG-JSON distribution (`harmonic.gap-port-result/1`).

> [!NOTE]
> This document does **not** replace the interactive theorem proving process; rather, it formalizes the exact preconditions, postconditions, memory frames, degree qualifications, and tracing schemas required **before** initiating Sprint 1 Lean 4 implementation.

---

## 2. The Pattern Language Architecture

In strict conformance with Guide v2, every verification target is defined as a uniform 8-tuple contract:

$$\mathcal{C} = \langle \text{ChunkAnchor}, \text{Pre}, \text{Post}, \text{Frame}, \text{Degree}, \text{Invariants}, \text{Decoder}(\alpha), \text{RungTarget} \rangle$$

Where:
* **ChunkAnchor:** Commit hash, source file, symbol name, and SHA-256 text hash of the GAP/C function.
* **Pre:** Entry conditions on the state and operands ($S_{\text{gap}} \models \text{Pre}$).
* **Post:** Guaranteed exit relation between inputs and outputs ($S_{\text{gap}}' \models \text{Post}$).
* **Frame:** Explicit aliasing and preservation statement (identity vs fresh operand allocation).
* **Degree:** Unambiguous qualification as **Support degree** ($\max \text{supp}$) or **Storage degree** (array length).
* **Invariants:** Inductive properties maintained across recursive/loop iterations.
* **Decoder ($\alpha$):** Transformation from raw kernel/C traces into abstracted algebraic states.
* **RungTarget:** Progressive ladder milestone (Rung 1 $\to$ Rung 3 $\to$ Rung 4b $\to$ Rung 5).

---

## 3. Working Reference Implementations (Phase 2 Locked Ground-Truth)

Our existing, fully verified Phase 2 corpus serves as the concrete reference implementation of this Pattern Language:

### Reference A: `GAP-Kernel-ProdPerm` (`src/permutat.cc:ProdPerm`)
* **Anchor:** `GAP:src/permutat.cc:ProdPerm` (`T_PERM` bag memory representation).
* **Lean Model:** `RequestProject.Gap.Permutation` (`PermMem`, `prodPermMem`, `toEquivPerm`).
* **Pre:** Valid memory pointers to two permutation bags $p, q$.
* **Post:** Formally proved multiplicative anti-homomorphism to Mathlib `Equiv.Perm`:
  $$\text{toEquivPerm}(p \cdot q) = \text{toEquivPerm}(q) \circ \text{toEquivPerm}(p)$$
* **Frame:** Operands may be returned by identity (shortcut when operand is identity permutation).
* **Degree:** Stated over **Support degree** ($\text{largestMovedPoint}$) with bound $\le \max(\text{deg}(p), \text{deg}(q))$.
* **Axioms:** `[propext, Classical.choice, Quot.sound]`, 0 `sorry`. Current Status: **Rung 3 (Proved)**.

### Reference B: `GAP-0299` (`lib/stbc.gi:StabChainOp`, CID: `baguqeeradzipocbvrtw44fhnudpvjqziopiy2du7ldbnrqxqii2wfpcgty5a`)
* **Anchor:** `GAP:lib/stbc.gi:StabChainOp`, `lib/stbc.gi:SiftedPermutation`.
* **Lean Model:** `RequestProject.Gap.Library.Stbc` (`StabChain`, `siftOneLevel`, `siftFull`).
* **Pre:** Descending base sequence $(\beta_1, \dots, \beta_k)$, valid transversal trees.
* **Post:** Membership soundness and completeness:
  $$g \in G \iff \text{siftFull}(g) = 1$$
* **Frame:** Sifting returns residual permutation; transversal tree pointers invariant.
* **Degree:** Stated strictly over **Support degree**.
* **Axioms:** `[propext, Classical.choice, Quot.sound]`, 0 `sorry`. Current Status: **Rung 3 (Proved)**.

---

## 4. Phase 3 Formal Pattern Language Specifications

### 4.1. `GAP-0190` (`lib/grpperm.gi` — The Crown Jewel)

* **IPLD Task CID:** `baguqeerabfmumkhx4awa3al6rthhculmjln7lhbwsw72b2elwll5rxyb2e5a`
* **Source Anchor:** `GAP:lib/grpperm.gi:SizePermGroup`
* **Effort Estimation:** 31.78 Person-Days / 1,591 Lines

#### Formal Contract:
```yaml
Chunk: GAP-0190
Anchor:
  repo: "github.com/gap-system/gap"
  file: "lib/grpperm.gi"
  symbol: "SizePermGroup"
  target_lean: "RequestProject.Gap.Library.Grpperm"

Pre:
  condition: "chain : StabChain α is valid for generator set S ⊆ Sym(Ω)"
  invariants:
    - "Every basic orbit Δ_i at level i is non-empty"
    - "Base points β_1, ..., β_k are distinct in Ω"
    - "Generators at level i fix all prior base points β_1, ..., β_{i-1}"

Post:
  condition: "Calculated group order equals product of basic orbit lengths"
  formula: "Fintype.card (Subgroup.closure (generators : Set (Equiv.Perm α))) = G.chain.basicOrbitSizes.prod"
  strength: "Forced by contract (determines group cardinality uniquely)"

Degree:
  qualifier: "Support degree"
  definition: "LargestMovedPoint (independent of internal array allocation length)"
  storage_probe: "Separate probe verifies storageDegree >= supportDegree"

Frame:
  aliasing: "No mutation of input generators or transversal tree nodes"
  freshness: "Output natural number is fresh; generators preserved by reference"

Tracing_Decoder:
  boundary_syscall: "Size(G)"
  decoder_func: "α_Size(bag_ptr) -> Nat"
  synthetic_events: "Test empty generator set (order 1), cyclic generator (order n)"

Target_Rungs:
  - Rung 1: "Lean 4 structural model type-checks with valid StabChain integration"
  - Rung 3: "Axiomatic proof of permGroup_order_eq_prod_basicOrbits with zero sorry"
  - Rung 4b: "lean-worker eBPF trace on Nix-pinned GAP binary matching basicOrbitSizes.prod"
```

---

### 4.2. `GAP-0247` (`lib/oprtperm.gi` — The Orbit-Stabilizer Engine)

* **IPLD Task CID:** `baguqeerahef7xwqlnqsmlizu35dlth3x6sunnnzwvtech7fzfqph7e5zhlkq`
* **Source Anchor:** `GAP:lib/oprtperm.gi:OrbitPerms`, `lib/oprtperm.gi:Stabilizer`
* **Effort Estimation:** 23.28 Person-Days / 1,168 Lines

#### Formal Contract:
```yaml
Chunk: GAP-0247
Anchor:
  repo: "github.com/gap-system/gap"
  file: "lib/oprtperm.gi"
  symbols: ["OrbitPerms", "StabilizerPermGroup"]
  target_lean: "RequestProject.Gap.Library.Oprtperm"

Pre:
  condition: "G ≤ Sym(Ω), x ∈ Ω, action: OnPoints (or OnPairs, OnSets)"
  invariants: "G is closed under composition; Ω is finite and decidable"

Post:
  condition: "Orbit-Stabilizer cardinality bijection"
  formula: "Fintype.card G = (orbitOfPoint G x).length * Fintype.card (pointStabilizer G x)"
  bijection: "Left coset space G / Stab_G(x) ≃ Orb_G(x) via transversal lookup"

Degree:
  qualifier: "Support degree"
  definition: "Support of G restricts to action domain Ω"

Frame:
  aliasing: "Generators and point set Ω immutable"
  freshness: "Orbit list and stabilizer subgroup are freshly constructed"

Tracing_Decoder:
  boundary_syscall: "Orbit(G, x, OnPoints)"
  decoder_func: "α_Orbit(G_ptr, x) -> List Nat"

Target_Rungs:
  - Rung 1: "Lean 4 action dispatchers type-check"
  - Rung 3: "Proof of orbit_stabilizer_order_relation with zero sorry"
  - Rung 4b: "lean-worker eBPF trace verifying coset representative bijection"
```

---

## 5. The IPLD CARv1 to `lean-worker` Handshake Protocol

To automate the bridge between our content-addressed CAR taskset and Mike DuPont's p2p worker nodes, we define the JSON interchange schema:

### 5.1. Job Dispatch Schema (CAR $\to$ `lean-worker`)

```json
{
  "schema": "harmonic.gap-worker-job/1",
  "taskset_root_cid": "baguqeeraykhbhp2afmcuxp7dpgb72dhnpkng2qpcybegfu3lqqdilezq3hzq",
  "task_cid": "baguqeerabfmumkhx4awa3al6rthhculmjln7lhbwsw72b2elwll5rxyb2e5a",
  "task_id": "GAP-0190",
  "anchor": {
    "repo": "https://github.com/gap-system/gap",
    "file": "lib/grpperm.gi",
    "symbol": "SizePermGroup"
  },
  "nix_provenance": {
    "flake_ref": "github:meta-introspector/aristotle-cli-rs#gap-pinned",
    "build_id": "pinned-nix-derivation-sha256"
  },
  "lean_target": {
    "module": "RequestProject.Gap.Library.Grpperm",
    "theorems": ["permGroup_order_eq_prod_basicOrbits"]
  },
  "trace_level": "boundary"
}
```

### 5.2. Conformance Result Schema (`lean-worker` $\to$ `merged_ledger.json`)

```json
{
  "schema": "harmonic.gap-port-result/1",
  "task_cid": "baguqeerabfmumkhx4awa3al6rthhculmjln7lhbwsw72b2elwll5rxyb2e5a",
  "task_id": "GAP-0190",
  "status": "verified",
  "rung": "4b",
  "worker": "aleph-cloud-worker-node",
  "timestamp": "2026-10-01T00:00:00Z",
  "evidence": {
    "trace_level": "boundary",
    "witness_count": 100,
    "synthetic_events": 5,
    "verdict": "witness",
    "build_id": "pinned-nix-derivation-sha256"
  },
  "artifacts": [
    {
      "lean_module": "RequestProject.Gap.Library.Grpperm",
      "sha256": "<computed-sha256>",
      "axioms": ["propext", "Classical.choice", "Quot.sound"]
    }
  ]
}
```

---

## 6. Execution Protocol & Safety Boundary

1. **Security Isolation:** All p2p job transmissions and trace ingestion route strictly via the **Verification Relay Gateway (`mechsrv`)**; internal server topologies remain completely protected.
2. **Immutable Provenance:** Once a result satisfies Rung 3 (Axiomatic Lean 4) and Rung 4b (Boundary Trace), it is merged into `tasks/merged_ledger.json` and cryptographically signed.
3. **Sprint 1 Green Light:** With this specification approved, Phase 3 implementation begins directly on `RequestProject/Gap/Library/Grpperm.lean`.
