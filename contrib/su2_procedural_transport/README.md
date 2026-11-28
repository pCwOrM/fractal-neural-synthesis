# Procedural `SU(2)` Cayley Transport, Log-Free Escape-Time Kernel & Paper 1 v4.0 §7.3 Independent Audit

*Original clean-room research contribution from **Moissanite-Labs** (purely additive under `contrib/su2_procedural_transport/`, zero modifications to existing repository files; clean-room academic contribution compatible with upstream BSL-1.1 / `TR 2026/016285` non-commercial research terms).*

This contribution offers three complementary, deterministically reproducible additions directly addressing open questions in **Paper 1 v4.0 (`arXiv:2611.32393v1`)**:

1. **Paper 1 v4.0 §7.3 (Adaptive Boundary Search) & Multiscale $\ell = 0 \dots 16$ Audit:** An independent, leak-free 10-fold stratified CV evaluation on the three real UCI benchmarks (`Ionosphere`, `Optical Digits`, `PenDigits`), an extension of the multiscale rank-vs-continuity sweep to $\ell = 0 \dots 16$ documenting the IEEE-754 `float64` 53-bit mantissa grid-collision boundary, and explicit scale-matched Fourier/Chebyshev controls.
2. **Procedural `SU(2)` Cayley Transport Operators ($T_{ij} = G(c, i, j)$):** A pure-$\mathbb{Q}$ verifier proving exact `SU(2)` unitarity, acute-basin pole safety, non-Abelian commutator preservation, and `0`-drift `16 B` quaternion checkpoint rollback, paired with a 5-seed equal-evaluation-budget empirical benchmark showing **where $\partial\mathcal{M}$ decisively outperforms both `SHA-256` PRNG and smooth Fourier bases**: pure **zero-readout** (`0 B` stored matrices, `0 B` readout weights) `32 B` seed evolution on non-Abelian $A_5$ word equivalence (`92.38% ± 5.16%`, **`+37.50 pp`** over `SHA-256`, **`+52.38 pp`** over fixed Fourier, and **`+22.88 pp`** over scale-matched Fourier!).
3. **Log-Free Pure-$\mathbb{Z}/\mathbb{Q}$ Smooth Escape-Time Kernel:** An exact integer/rational replacement for `nu(c) = n_esc + 1 - log2(log2(|z|))` (`arXiv:2611.32393v1` Eq. 2) using integer `bit_length` dyadic shell interpolation with exact `0/1` seam jump across dyadic lemniscates $s \in \{4, 16, 256\}$.

> **Compute & Telemetry Note:** All benchmarks were executed strictly on CPU (`CUDA_VISIBLE_DEVICES=""`, single-threaded BLAS) with zero uncontrolled laptop power or energy claims.

---

## 1. Key Findings Summary

### 1.1 Multiscale Rank vs. Local Continuity ($\ell = 0 \dots 16$) & IEEE-754 `float64` Boundary
Anchored at the Misiurewicz parameter $c_0 = (-0.10109636384562,\; 0.95628651080914)$ (`256`-point phyllotaxis disc, `max_iter = 70 + 40 * ell`, `12` jitters):
- **$\ell = 0 \dots 8$ vs. Fixed-Scale Baselines (Reproduced):** `mandelbrot_boundary` sustains high spectral effective rank (`rank16 = 11.954`) and positive local continuity (`rho = 0.656`), while `prng_sha256` loses continuity (`rho = 0.005`) and fixed-frequency smooth baselines collapse in rank at $\ell = 3 \dots 8$ (`fourier_smooth_fixed = 2.264`, `lattice_value_fixed = 2.575`).
- **IEEE-754 `float64` 53-Bit Mantissa Cliff ($\ell = 14 \dots 16$):** Fixed-frequency smooth fields underflow to constant vectors (`rank16 = 0.00`) at $\ell = 14$. At $\ell = 15$, `25%` of $0.05 \cdot 10^{-\ell}$ local steps round to exact `0.0` in `float64` (spurious `prng_sha256` $\rho = 0.25$). At $\ell = 16$, `85.2%` of the 256 phyllotaxis coordinates collide onto duplicate `float64` bit patterns (`38/256 = 14.84%` unique pairs) and `100%` of local steps vanish (`delta_exact_zero_frac = 1.00`), forcing all 6 generators—including `prng_sha256`—to spuriously report $\rho = 1.00$. Zooming beyond $\ell \ge 15$ strictly requires higher-precision or rational perturbation arithmetic.
- **Scale-Matched Smooth Controls:** When explicit zoom radius $r_\ell = 10^{-\ell}$ is passed to smooth bases (`fourier_matched_scale`: `rank16 = 12.633, rho = 0.893`; `chebyshev_matched_scale`: `rank16 = 10.369, rho = 0.980`), smooth bases match or exceed `mandelbrot_boundary` across $\ell = 0 \dots 15$. The distinguishing property of $\partial\mathcal{M}$ is therefore **intrinsic scale-free detail without frequency rescaling**, rather than an impossibility for smooth functions at known scale.

### 1.2 Closing Paper 1 v4.0 §7.3: Leak-Free 10-Fold Stratified CV on 3 Full UCI Benchmarks
Full datasets (`Ionosphere`: `351 × 34`, `Optical Digits`: `1,797 × 64`, `PenDigits`: `10,992 × 16`, SHA-256 pinned), `H = 256`, per-class symmetric INT8 ridge readout (`reg = 0.5`). Adaptive methods use a strictly matched **`24`-evaluation inner-CV budget** inside an 80/20 split of each training fold (`0` test leakage):

| Method | Seed Size | UCI Ionosphere | UCI Optical Digits | UCI PenDigits |
|---|---:|---:|---:|---:|
| `Linear_INT8` | `0 B` | `86.56% ± 4.47%` | `93.44% ± 2.49%` | `86.53% ± 0.86%` |
| `FNS_Static_24B_INT8` | `24 B` | `89.67% ± 4.71%` | `97.94% ± 1.13%` | `99.03% ± 0.24%` |
| **`FNS_Adaptive_InnerCV_24B_INT8`** | **`24 B`** | **`89.98% ± 5.54%`** | **`98.00% ± 1.10%`** | **`98.93% ± 0.33%`** |
| `Seeded_PRNG_ELM_Static_8B_INT8` | `8 B` | `90.88% ± 5.30%` | `97.71% ± 1.38%` | **`99.06% ± 0.23%`** |
| `Seeded_PRNG_ELM_Adaptive_8B_INT8` | `8 B` | `90.01% ± 3.36%` | **`98.22% ± 0.74%`** | `98.93% ± 0.28%` |
| `Seeded_PRNG_RFF_Static_8B_INT8` | `8 B` | `90.60% ± 2.68%` | `97.16% ± 1.33%` | `97.48% ± 0.39%` |
| `Seeded_PRNG_RFF_Adaptive_8B_INT8` | `8 B` | **`93.44% ± 3.53%`** | `97.60% ± 0.93%` | `98.79% ± 0.40%` |

- **Result:** Both static and adaptive `24 B` FNS significantly beat `Linear_INT8` on `3/3` datasets ($p_{\text{Holm}} < 0.01$). However, inner-fold adaptive boundary search yields **no statistically significant gain** over static `24 B` FNS (`+0.31 / +0.06 / -0.10 pp`, all $p_{\text{Holm}} = 1.000$) and wins **`0/3`** against equal-budget `8 B` Seeded-PRNG ELM/RFF. Behind an analytical ridge readout, tabular performance is governed by the aggregate random-feature kernel spectrum, where an `8 B` PRNG seed already matches or exceeds `24 B` FNS.

### 1.3 Where $\partial\mathcal{M}$ Shines: Zero-Readout Procedural `SU(2)` Transport Evolution ($A_5$ & $S_3$)
Replacing stored matrices and readout weights entirely (`32 B` seed $\Theta = (c_x, c_y, \ell, \phi)$, **`0 B` stored transition matrices**, **`0 B` readout weights**), each group generator $T_a(\Theta) \in SU(2)$ composes 3 acute-basin Cayley steps ($|\omega_i| \le 2/5$, guaranteed pole-safe with squared denominator $\ge 81/625$). Word equivalence on disjoint `80` train / `160` unseen test pairs (50% of negatives are Abelian-blind equal-letter-count swaps) is decided purely by intrinsic projective overlap $|\langle U(w_A), U(w_B)\rangle| \ge 0.90$. All 4 generators share an identical `1,600`-evaluation budget (`4 × 400`, $\ell \in [2.5, 5.5]$) across `5` independent seeds, guarded by `16 B` quaternion checkpoints (`59,358` total verified rollbacks — `29,409` on $A_5$ + `29,949` on $S_3$ — with **`0.0` max drift**):

| Task (Abelian Ceiling) | Generator (`32 B` seed, `0 B` readout) | Held-Out Test Acc (`5` Seeds) | $\Delta$ (`∂M` minus Baseline) | $p_{\text{Holm}}$ (`m=4`, 1-sided) |
|---|---|---:|---:|---:|
| **`A5`** (`41.88%`) | **`mandelbrot_boundary_su2` (`∂M`)** | **`92.38% ± 5.16%`** (`[91.9, 93.8, 83.8, 96.2, 96.2]%`) | — | — |
| `A5` | `prng_sha256_su2` | `54.88% ± 9.56%` | **`+37.50 pp`** ($t=9.959$) | **`0.000858`** (`< 0.01`) |
| `A5` | `fourier_fixed_smooth_su2` | `40.00% ± 0.00%` (`comm = 0.095`) | **`+52.38 pp`** ($t=22.690$) | **`0.000044`** (`< 0.01`) |
| `A5` | `fourier_matched_scale_su2` *(control)* | `69.50% ± 10.49%` | **`+22.88 pp`** ($t=6.346$) | *(raw $p = 0.001579$)* |
| **`S3`** (`41.25%`) | **`mandelbrot_boundary_su2` (`∂M`)** | **`69.62% ± 14.37%`** (`[65.0, 71.9, 62.5, 55.6, 93.1]%`) | — | — |
| `S3` | `prng_sha256_su2` | `53.25% ± 2.27%` | `+16.38 pp` ($t=2.502$) | `0.033306` (`> 0.01`) |
| `S3` | `fourier_fixed_smooth_su2` | `38.12% ± 0.00%` (`comm = 0.066`) | **`+31.50 pp`** ($t=4.903$) | **`0.008026`** (`< 0.01`) |
| `S3` | `fourier_matched_scale_su2` *(control)* | `66.25% ± 14.39%` | `+3.38 pp` ($t=0.409$) | *(raw $p = 0.351842$)* |

- **Interpretation:** In pure zero-readout group-transport seed evolution, `SHA-256` breaks local continuity ($\rho = 0$), fixed-frequency Fourier collapses to near-Abelian rank (`comm = 0.066–0.095`), and even scale-matched stationary Fourier trails `∂M` by `22.88 pp` on $A_5$ ($p = 0.0016$). Sliding 4 floats on $\partial\mathcal{M}$ reliably self-discovers accurate non-commuting order-2 ($180^\circ$) and order-3 ($120^\circ$) $SU(2)$ generators (`|T0^2 · I| ≈ 0.993`, `|T1^3 · I| ≈ 0.995`) across all 5 seeds on $A_5$ (`83.8%–96.2%`). On $S_3$, the additional dihedral axis-orthogonality constraint $srs = r^{-1}$ increases cross-seed variance (1 seed reaches `93.1%`), leaving $S_3$ vs. `SHA-256` at $p_{\text{Holm}} = 0.033$.

### 1.4 Pure-$\mathbb{Q}$ Exact Verifier & Log-Free Escape-Time Kernel
`su2_procedural_transport_verify.py` uses **zero floats** and **zero `math.log`/`log2` calls** in its AST and certifies:
- Exact integer acute `2I`-basin proof $20 \times 625 = 12{,}500 < 12{,}769 = 113^2$ ($\|\vec{\omega}\|^2 \le 12/25 < \tan^2(\pi/5)$) and worst-case pairwise pole-safety floor $(1 - 16/25)^2 = 81/625 > 0$.
- `8/8` exact `SU(2)` left/right unitarity, `det = 1`, $\mathbb{C}^2$ spinor isometry, `SO(3)` isometry & `det = 1`, and `28/28` non-Abelian pairs satisfying $\mathrm{Re}([a, b]) = 1 - 2\|\vec{v}_a \times \vec{v}_b\|^2$.
- Exact `16 B` `Q1.30` checkpoint packing and `0`-drift right-action rollback.
- **Log-Free Escape-Time Kernel:** Exact `3/3` dyadic lemniscate identities ($s \in \{4, 16, 256\}$), `3/3` exact `0/1` seam continuity across $(n_{\text{esc}}, s) \mapsto (n_{\text{esc}} + 1, s^2)$, and strict monotonicity across radii (`5/5`) and rational Mandelbrot orbits (`4/4`).

---

## 2. Offline Verification & Reproduction

```bash
cd contrib/su2_procedural_transport

# 1. Pure-stdlib, float-free, log-free exact verifier (3-mode isolated -I parity)
python3 -I -B su2_procedural_transport_verify.py --check
python3 -I -O -B su2_procedural_transport_verify.py --check
python3 -I -B -W error su2_procedural_transport_verify.py --check

# 2. Pure-stdlib R5 unit, boundary, tamper & receipt test suite (0 stdout bytes on PASS)
python3 -I -B test_su2_procedural_transport_r5.py

# 3. Pure-stdlib verification of canonical SHA-256-bound results receipt
python3 -I -B run_s73_adaptive_and_su2_transport.py --verify-receipts

# 4. Full CPU empirical reproduction (requires numpy + scipy + UCI datasets in data_cache/)
CUDA_VISIBLE_DEVICES="" OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3 -B run_s73_adaptive_and_su2_transport.py --run --data-dir data_cache
```
