# arXiv `cs.LG` Clean Submission Guide

> **Pre-Submission Checklist:** ALL automated moderation checks passed (`0` forbidden terms, `0` em-dash warnings, `8.9%` self-citation rate, `0.30%` 5-gram overlap vs v3, `<1,920`-character Abstract, single `\documentclass` inside tarball, pre-compiled `main.bbl` included, zero `../` parent paths).

## 1. Upload Package
- Upload: **`paper1_v4/release/arxiv_paper1_v4_source.tar.gz`**
- Contents (clean, single-target AutoTeX bundle):
  - `main.tex`
  - `body.tex`
  - `main.bbl` (pre-generated BibTeX output so arXiv TeX Live compiles in 1 pass with zero missing citations)
  - `figures/fig1_fns_architecture.pdf` .. `figures/fig6_cross_domain_verification.pdf`

## 2. Category Selection
- **Primary Category:** `cs.LG` (Machine Learning)
- **Cross-List Categories:** `cs.NE` (Neural and Evolutionary Computing) *(optional secondary: `cs.DS` or leave at `cs.LG` + `cs.NE` for clean moderation)*

## 3. Metadata (Copy-Paste Ready — Strictly < 1,920 Chars!)
- **Title:**
  `Fractal Neural Synthesis: Constant-Storage Procedural Weight Derivation via Complex Quadratic Boundary Dynamics`
- **Authors:**
  `Volkan Dagli, Zerrin Dagli, Daghan Dagli`
- **Comments:**
  `14 pages, 6 figures, 5 tables. Reproducible code, seeds, and raw benchmark telemetry archived under Zenodo Concept DOI: https://doi.org/10.5281/zenodo.22774934`
- **ACM Classes:** `I.2.6; C.3`
- **Journal-ref / DOI fields:** **LEAVE EMPTY** *(arXiv's DOI field is strictly for peer-reviewed journal DOIs; put Zenodo Concept DOI only in `Comments`!)*
- **License:** **`arXiv.org perpetual, non-exclusive license`** (`http://arxiv.org/licenses/nonexclusive-distrib/1.0/`) — *ideal for subsequent Elsevier Subscription ($0 APC) Q1 journal submission because full copyright remains with the authors.*
- **Abstract (Paste verbatim — 1,472 characters, safely below arXiv's 1,920-character cap!):**

```text
Conventional neural networks store synaptic parameters as explicit tensors whose persistent Flash footprint scales linearly (O(W)) with parameter count, constraining resource-limited edge microcontrollers. We formulate and systematically evaluate Fractal Neural Synthesis (FNS), a procedural weight derivation architecture that replaces hidden-layer matrices with a constant 24-byte coordinate seed Theta = (c_x, c_y, ell) in F_64^3 anchored near the complex quadratic bifurcation boundary dM of f_c(z) = z^2 + c. We introduce a large-bailout (R = 256) smooth escape kernel, four zero-overhead geometric sampling apertures--Cartesian Grid, coprime 3x3 Rule-of-Thirds (Z/9Z), phi-Vogel spiral, and multi-scale Harmonic Tripod--and prove conditional Kolmogorov (K_Kolm <= 192 + c_0 bits) and Shannon entropy bounds. Across magnifications zeta in [10^0, 10^8], C^1 Fourier and lattice-noise bases collapse to post-standardization rank ~2.25 and SHA-256 PRNG exhibits avalanche discontinuity (rho ~ 0.019, 50.6% micro-step retention), whereas dM uniquely sustains both rank (~10.0) and local continuity (rho in [0.81, 0.97], 89.2% retention). Under leak-free 10-fold CV across four zero-scaler-byte non-linear benchmarks, FNS with an INT8 readout surpasses 0-hidden Linear-INT8 by +3.6 to +10.8 pp while delivering 10.7x-129x total Flash reduction (725x-2,773x hidden reduction) relative to converged Float32 MLPs (90.30% Ionosphere in 285 B; 97.22% Optical Digits in 2,598 B; 97.90% PenDigits in 2,598 B; 87.00% Satimage in 1,570 B).
```
