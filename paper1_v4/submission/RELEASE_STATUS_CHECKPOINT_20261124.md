# Paper 1 v4.0 — Release Status & Dual-Tier Checkpoint (2026-11-24)

**Canonical Title:** *Fractal Neural Synthesis: Constant-Storage Procedural Weight Derivation via Complex Quadratic Boundary Dynamics*  
**Authors (Printed PDF):** Volkan Dağlı$^{1,2,*}$, Zerrin Dağlı$^{3,4}$, Dağhan Dağlı$^{5}$  
**Authors (Online Portals ASCII):** `Volkan Dagli`, `Zerrin Dagli`, `Daghan Dagli`  
**ORCIDs:** V. Dagli `0009-0000-1587-8703` (DBLP: `https://dblp.org/pid/117/8590.html`) • Z. Dagli `0000-0001-9490-6425` • D. Dagli `0009-0003-2492-8313`  
**Correspondence:** Public PDF: `ask@answerr.me` • Academic Portals / Editorial: `vdagli@aof.anadolu.edu.tr`  
**Funding Statement:** *This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors; computational infrastructure was made available free of charge by ITouch Systems solely for non-commercial open scientific research.*

---

## 1. Publication Pipeline Status

| Stage | Platform | Identifier / Link | Status |
| :--- | :--- | :--- | :--- |
| **Tier-1 (Step 1)** | **CERN Zenodo (v4.0)** | Concept DOI: `10.5281/zenodo.22774934` • v4.0 DOI: `10.5281/zenodo.24495977` | **LIVE & VERIFIED** (`OpenAIRE` indexed; MD5 bit-exact match; 4-version chain intact) |
| **Tier-1 (Step 2)** | **arXiv (`cs.LG` + `cs.NE`)** | `arXiv:submit/8419869` (`arXiv.org perpetual, non-exclusive license`) | **SUBMITTED** (AutoTeX compiled 14p cleanly, 0 errors — awaiting `arXiv:2611.XXXXX` announcement) |
| **Tier-1 (Step 3)** | **Elsevier SSRN** | `https://papers.ssrn.com/abstract=7659198` (DOI: `10.2139/ssrn.7659198`) | **PENDING** (Revise immediately after arXiv ID announces) |
| **Tier-2 (Q1)** | **Elsevier *Neurocomputing*** | **Subscription ($0 APC)** — 18-page extended journal edition | **SEALED & READY** (`paper1_v4/q1_extended/Paper1_v4_Elsevier_Q1_Extended.pdf` + `Q1_SUBMISSION_BUNDLE.zip`) |

---

## 2. Verified Live Zenodo v4.0 Artifacts (`10.5281/zenodo.24495977`)
- `Paper1_v4_Preprint_FINAL.pdf` — 14 pages, `0 Overfull \hbox`, MD5 `8f9c657f658f3b806bbe79b32b34a3ae`
- `zenodo_v4_bundle.zip` — 27 files (including `experiments/*.py`, clean JSON/CSV, 6 vector PDFs/PNGs + Draw.io/SVG, LaTeX, Reproducibility log; `0` Q1/vault leaks), MD5 `54b6590be5f393aa0b15060c5e0d106b`

## 3. Sealed Tier-2 Q1 Extended Artifacts (`paper1_v4/q1_extended/`)
- `Paper1_v4_Elsevier_Q1_Extended.pdf` — 18 pages (`elsarticle 5p`), `0` content `Overfull \hbox`, 9 vector figures, 13 tables, 47 references (`8.5%` self-citation rate)
- `fns_q16.c` & `fns_q16_cortex_m4.o` — Dependency-free pure-integer ANSI C99 Q16.16 kernel (`1,326 B` ARM Cortex-M4 Thumb-2 `-Os` Flash code, 0 FPU/libm)
- `Q1_SUBMISSION_BUNDLE.zip` + `COVER_LETTER_NEUROCOMPUTING_Q1.md` + `HIGHLIGHTS_Q1.md` (5 bullets verified `<= 85` chars)

## 4. Next Actions Upon arXiv Announcement
1. Add `arXiv:2611.XXXXX` (`Is identical to`, `Scheme: arXiv`) to Zenodo v4.0 (`24495977` → Edit).
2. Revise SSRN `7659198` with `Paper1_v4_Preprint_FINAL.pdf` + Concept DOI + live arXiv ID.
3. Insert live arXiv ID into `COVER_LETTER_NEUROCOMPUTING_Q1.md` and submit Tier-2 Q1 Extended package to Elsevier *Neurocomputing* (**Subscription / $0 APC**).
4. Replace `arXiv:submit/8419869` across all synced GitHub repos with the live `arXiv:2611.XXXXX` link.
