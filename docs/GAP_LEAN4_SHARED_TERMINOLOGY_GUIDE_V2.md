# Shared Terminology Guide, v2 (draft)

**Status:** draft for team agreement. Changes from v1 are marked **[v2]** and listed in the changelog at the end. Each term has one meaning here.

## 1. What we claim, and what we don't

We build a **Lean model** of selected GAP code, prove properties of the model, and check runtime **traces** of a real binary against the model. The link between model and code is human review of anchors, plus trace conformance.

We do **not** claim to have verified the C or GAP code itself. Every status report states which rung a result reached, and whether its trace evidence is operator-level or boundary-level.

| Rung | Name | Meaning |
|---|---|---|
| 0 | **Anchored** | Chunk pinned to a commit, file, symbol, and body hash |
| 1 | **Modeled** | A Lean model exists, follows the code branch by branch, and type-checks |
| 2 | **Reviewed** | A named GAP developer signed off the model-to-code correspondence |
| 3 | **Proved** | Contract proved for the model, no `sorry`, axiom set listed |
| 4a | **Witnessed (operator)** **[v2]** | Traces of a GAP-level operation (for example `*`) satisfy the contract |
| 4b | **Witnessed (boundary)** **[v2]** | Traces at the C function boundary, on a build with recorded provenance, satisfy the contract |
| 5 | **Zipped** | Contract composes with callers and callees (seams checked) |

Rung 4a is real evidence but weaker than 4b: it also exercises method selection and wrappers, so a mismatch cannot be blamed on the chunk alone, and a match cannot rule out errors the wrapper masks. Reports must never write a bare "Witnessed".

## 2. Code-side terms

- **Chunk (C):** the unit of work: a function or small group of functions. One anchor per chunk.
- **Scope:** function ⊂ file ⊂ module ⊂ package ⊂ repo.
- **Epoch:** a commit range; changes across it are renames, additions, and removals.
- **Anchor (`CodeAnchor`):** repo, commit, file, symbol, line range, and a SHA-256 of the function text.
- **Stale anchor:** **[v2]** the body hash no longer matches the source. The hash alone decides freshness. Line ranges are informational only and may move between commits without making an anchor stale.
- **Build-id:** the identifier of a binary, recorded in every trace.
- **Provenance** **[v2]**: the verifiable link from a build-id to the anchored source. A build has provenance only if its source commit and build recipe are recorded and reproducible (for example a pinned Nix derivation). A distribution binary with no such record has **no provenance**, and its traces cap at rung 4a.
- **V1 / V2:** V1 is the C-side vocabulary. V2 is the GAP-side vocabulary. A **kernel binding** is a V1 to V2 pair taken from the registration tables.
- **Reference bridge (R):** the ground-truth vocabulary mapping, extracted mechanically from source, never written by an LLM.
- **Degree** **[v2]**: always qualify it.
  - **Support degree:** the largest point moved by the permutation (GAP's `LargestMovedPoint`). Depends only on the group element.
  - **Storage degree:** the length of the permutation's internal representation. Two equal permutations can have different storage degrees.
  - A contract's Post must say which degree it means. The `ProdPerm` model uses **storage degree** (a bag's length is its degree, and Post requires the result to have length `max degL degR`). Storage degree is not visible through GAP's `*` operator or `ListPerm(x, n)` output, so a trace at operator level cannot check that part of Post. It needs a boundary-level probe (rung 4b).

## 3. Lean-side terms

- **Model:** a Lean definition of a chunk's behavior. An abstraction, not the C.
- **State (S_lean / S_gap):** S_lean is a Lean term. S_gap is an abstracted observation of the running system.
- **Decoder (α):** turns raw runtime data into an S_gap state, at chunk boundaries only.
- **Contract:** the uniform record for a chunk:
  - **Pre:** what must hold on entry.
  - **Post:** what holds on exit, relating input and output.
  - **Frame:** **[v2]** what is guaranteed unchanged, including aliasing. Frame must state, for each output, whether it may be one of the inputs (returned by identity) or must be fresh. A result that is an operand itself is a legitimate case, not an exception (for example the short cuts in `ProdPerm`).
  - **Label, calls, proof status, trace counts.**
- **Invariant / inductive invariant:** as in v1.
- **Simulation:** every observed GAP step is matched by a model step inside R_C.
- **Axiom rollup:** `#print axioms` output for a theorem. `sorry` and custom axioms are always reported.

## 4. Bridge and label terms

- **Label structure L(C):** a small finite poset of meaning-tags (`Perm`, `GroupElt`, `Orbit`, `Error`, …).
- **Labeling (λ)** and **arrow (R_C):** labels on states, and a label-respecting relation between GAP and Lean states.
- **Translator (T):** any function between symbol tables, including an LLM step. Always untrusted.
- **Symmetry group (G), orbit invariant, canonical form:** as in v1.
- **Equivariance defect:** how far a translator is from commuting with G.

## 5. Evidence terms

- **Trace:** a recorded execution: a control stream plus a data stream.
- **Trace level** **[v2]**: **operator-level** (a GAP-visible operation such as `*`) or **boundary-level** (the C function itself, via probes or a debugger). Every trace and every witness count carries its level.
- **Witness:** one trace event whose decoded input satisfies Pre and whose output satisfies Post.
- **Verdict:** each checked event gets exactly one of `witness`, `out-of-domain`, `violation`, `undecodable`. The meaning of each is unchanged from v1.
- **Synthetic event** **[v2]**: a hand-written or generated event used to test the checker itself (for example to confirm a `violation` verdict is reachable). Synthetic events are reported in a separate column and never counted as witnesses.
- **Coverage:** lines, branches, or model cases exercised, reported as counts.
- **Post strength:** how much Post says. A Post that determines the output completely (uniquely, up to G) is the strongest form, and is what makes an output "forced".

## 6. Composition terms

- **Zip:** a join of lemma and trace over the same anchor, label, and build-id. It tests the model against the binary and adds no proof strength.
- **Seam, seam-OK, gluing condition, cover, uncovered edge:** as in v1.
- **Worker / coordinator:** any producer of a Contract, and the deterministic checker that composes them.
- **Edge status:** `zipped`, `seam-failed`, `label-mismatch`, `overlap-conflict`, or `uncovered`.

## 7. Measurement and indexing terms

- **Bandwidth:** static bound, realized entropy, and useful information I(in; out).
- **Forced (determined):** given the invariants and observable inputs, the state is unique up to G. Stronger than **confined**. For a chunk, "forced" is a property of its contract in the model, and becomes a statement about the real function only after rungs 2 and 4b.
- **Spectrum:** always specify temporal, structural, or channel.
- **Galois connection** vs. **Galois field GF(2^k):** different things, never abbreviated to "Galois" alone.
- **Field tower / group tower / extension edge:** as in v1.
- **Stratum, core, level** **[v2]**: coarse indexes of a module by the numbers it uses. Stratum is the lcm of those numbers (ordered by divisibility), core is the product of the distinct primes of the stratum, and level is the largest prime occurring. The stratum sees prime support and multiplicity only, so it cannot distinguish chunks by what they compute. Use it as an index alongside labels, never in place of them.

## 8. Words we use carefully

| Say | Instead of |
|---|---|
| "The model's property is proved" | "GAP is verified" |
| "Witnessed at operator level on N runs" | "tested" or "confirmed" |
| "Out-of-domain" | "passed" (when Pre failed) |
| "Uncovered" | "not needed" |
| "Stale (hash mismatch)" | "outdated" |
| "Forced by the contract" | "deterministic" |
| "Support degree" or "storage degree" | "degree" |

## 9. Decisions still open

1. **Fragment:** which code after `ProdPerm` (inverse, orbit, stabilizer-chain step)?
2. **Chunk granularity:** function only, or function plus helpers?
3. **Decoder boundaries:** which representations are decodable, and where is decoding unsafe?
4. **Minimum bar per rung:** must rung 2 precede rung 3 in reports?
5. **Trace method for rung 4b:** debugger or eBPF, on a Nix-built GAP from pinned sources with debug info. Owner of that build?
6. **Provenance rule:** what evidence makes a build count as having provenance (pinned derivation hash, recorded source commit, recorded flags)?
7. **Label set:** initial contents of L(C), under 20 labels.
8. **Reviewers:** who signs off each chunk at rung 2?

## 10. Reference row

The first completed row is `ProdPerm` (`src/permutat.cc`, tag v4.14.0): rungs 0, 1, and 3 reached; rung 4a partly reached (operator-level, 64 events, all four C branches exercised, no violations); rungs 2, 4b, and 5 not reached. Its table columns are:

`anchor | lemma | axioms | trace level | events | witness | out-of-domain | violation | undecodable | synthetic | anchor fresh?`

The `trace level` and `synthetic` columns are new in v2.

## Changelog from v1

1. Added **degree** (support vs. storage), and required Post to say which.
2. Split rung 4 into 4a (operator) and 4b (boundary); added **trace level**.
3. Anchor freshness is decided by the body hash only; line ranges are informational.
4. Frame must state whether an output may alias an input.
5. Added **synthetic event**, reported separately from witnesses.
6. Added **provenance**, linking a build-id to source (Nix derivation planned).
7. Added **stratum / core / level** as coarse indexes, with the caveat about what they cannot see.
