# Cover Letter — Elsevier *Neurocomputing* (Q1 Extended Journal Edition, Subscription / $0 APC Track)

**Date:** November 25, 2026  
**To:** Editorial Board, *Neurocomputing* (Elsevier)  
**Publishing Model Requested:** **Subscription (No Article Publishing Charge / $0 APC)**  
**Manuscript Title:** *Fractal Neural Synthesis: Constant-Storage Procedural Weight Derivation via Complex Quadratic Boundary Dynamics*  
**Authors:** Volkan Dağlı$^{1,2,*}$, Zerrin Dağlı$^{3,4}$, Dağhan Dağlı$^{5}$  
**Affiliations (Printed / Portal ROR Mapping):**
- $^1$ Anadolu University, Eskişehir, Türkiye *(Portal ROR: Anadolu University)*
- $^2$ ITouch Systems, Cukurova University Technopark, Adana, Türkiye
- $^3$ Mersin University, Mersin, Türkiye *(Portal ROR: Mersin University)*
- $^4$ Yusuf Kalkavan Anatolian High School, Ministry of National Education, Mersin, Türkiye
- $^5$ Toros Science High School, MEV (Toros University), Mersin, Türkiye *(Portal ROR: Toros University)*  

**ORCIDs:** V. Dağlı `0009-0000-1587-8703` (DBLP: `https://dblp.org/pid/117/8590.html`) • Z. Dağlı `0000-0001-9490-6425` • D. Dağlı `0009-0003-2492-8313`  
**Corresponding Author:** Volkan Dağlı (Editorial / Academic: `vdagli@aof.anadolu.edu.tr` • Public Manuscript Correspondence: `ask@answerr.me`)

---

Dear Editors,

We respectfully submit our original full-length research article, **"Fractal Neural Synthesis: Constant-Storage Procedural Weight Derivation via Complex Quadratic Boundary Dynamics,"** for consideration in *Neurocomputing* under the **Subscription (no-fee / $0 APC)** publishing track.

### Scientific Motivation and Fit with *Neurocomputing*
*Neurocomputing* has long served as a premier venue for foundational research on Extreme Learning Machines (ELMs; Huang et al., *Neurocomputing* 2006), random-feature reservoirs, TinyML compression, and backpropagation-free optimization. On resource-bounded microcontrollers and autonomous edge sensors, storing explicit dense weights incurs linear $O(W)$ non-volatile Flash scaling. In this 18-page extended manuscript, we formulate, theoretically bound, and exhaustively evaluate **Fractal Neural Synthesis (FNS)**, replacing explicit hidden-layer and convolutional kernel matrices with a constant $24\text{-byte}$ IEEE-754 Float64 coordinate seed $\Theta = (c_x, c_y, \ell) \in \mathbb{F}_{64}^3$ anchored near the complex quadratic bifurcation boundary $\partial\mathcal{M}$ of $f_c(z) = z^2 + c$.

### Relationship to Preliminary Preprint (~40% Substantial Journal Extensions)
In full compliance with Elsevier's preprint sharing policy, a shorter foundational preprint (14 pages, covering dense reservoirs, 4 apertures, multi-scale generator ablations, and Python profiling) is deposited on CERN Zenodo (Concept DOI `10.5281/zenodo.22774934`, v4.0 DOI `10.5281/zenodo.24495977`), arXiv (`arXiv:2611.32393 [cs.LG]`), and SSRN (`10.2139/ssrn.7659198`, revised November 25, 2026). **This Q1 journal submission substantially extends the preprint by approximately 40% (18 dense two-column `elsarticle` pages, 9 vector figures, 13 tables, and a complete 4-table statistical/sensitivity appendix)** with six major new technical contributions not present in the preprint:

1. **24-Byte Procedural 2D Convolutional Neural Network & 5th Retinal Aperture (Section 6, Fig. 7):** We formalize a fifth Retinal Center-Surround aperture and synthesize 32 zero-storage $3\times 3$ 2D convolutional kernels directly from $24\text{ B}$ via $3\times 3$ Rule-of-Thirds sub-apertures on $\partial\mathcal{M}$, reaching **$97.38\% \pm 0.98\%$** on native $8\times 8$ UCI Optical Digits ($53.3\times$ convolutional Flash compression vs.\ explicit filters, outperforming flattened FNS-Tripod at identical total Flash).
2. **Leak-Free Nested Inner-CV Coordinate Adaptation (Section 6.3, Table 7):** Under a strictly leak-free nested inner-CV protocol ($24$ inner evaluations/fold), we benchmark adaptive $\Theta^*$ hill-climbing against Best-of-24 Seeded-PRNG RFF, candidly exposing both multi-class gains ($+0.22$ to $+0.50$ pp) and small-sample inner-validation overfitting.
3. **Compiled Pure-Integer ANSI C99 Q16.16 Kernel & Real ARM Cortex-M4 ELF Footprint (Section 7.1, Fig. 8, Table 8):** We implement and compile a dependency-free, zero-FPU, zero-`libm` ANSI C99 Q16.16 engine (`fns_q16.c`). Cross-compiling for bare-metal ARM Cortex-M4 Thumb-2 (`-Os`) verifies an exact binary footprint of **`.text = 1,302 B`, `.rodata = 24 B`, `.bss = 0 B` (`1,326 B` total Flash code)**, accelerating boot synthesis **$4.2\times$--$7.6\times$** ($1.07$--$5.01\text{ ms}$) with **$9.69$--$23.22\,\mu\text{s}$** single-sample pure-integer inference, $18$--$66\text{ KB}$ SRAM, and $-0.15$ to $+0.17$ pp multi-class parity versus FP64.
4. **Steganographic Weight Obfuscation & Coordinate Key-Sensitivity Curve (Section 7.2, Fig. 8c):** Holding the trained INT8 readout exposed to an adversary, perturbing the secret $24\text{-byte}$ seed by $\|\Delta\Theta\|_2 = 10^{-3}$ collapses 10-class accuracy from $97.2\%$ to $14.9\%$ (and to random chance $10.7\%\text{--}11.8\%$ by $10^{-2}$), providing zero-overhead functional obfuscation while maintaining local navigability for $\|\Delta\Theta\|_2 \le 10^{-5}$.
5. **Differentiable Soft-Escape SPSA-Adam vs.\ Gradient-Free Hybrid Evolution (Section 8, Fig. 9a, Table 9):** Under a strict equal budget ($32$ evals/gen, $144\text{ B}$, $0\text{ B}$ readout), we demonstrate empirically and explain dynamically why gradient-free Elitist Walk ($86.00\%$) and Hybrid Elitist + Rank-1 ES ($80.90\%$) outperform differentiable Soft-Escape SPSA-Adam ($57.05\%\text{--}62.65\%$) by $+18.3$ to $+29.0$ pp due to exponential derivative blow-up across chaotic boundary filaments.
6. **Complete Sensitivity & Holm--Bonferroni Appendix (Appendix A, Fig. 9b--c, Tables A.10--A.13):** We verify $M_{\max}=70$ as the monotonic accuracy/latency Pareto elbow, bisect $59$--$66$ exterior escape-lemniscate crossings to $10^{-12}$ precision to prove **$126{,}318\times$ jump suppression** at $R=256$, demonstrate **$+33.0$ pp Two-Spirals readout recovery** ($58.5\% \to 91.5\%$) via packed INT12 in just $+33\text{ B}$, and confirm that FNS+INT8 survives step-down Holm--Bonferroni correction against Linear-INT8 on all four datasets ($p_{\mathrm{Holm}} \le 0.0254$) while remaining statistically indistinguishable from converged FP32 MLPs on three of four datasets.

### Declarations
- This manuscript is original, is not under consideration by any other journal, and has been approved by all authors.
- Pending patent applications (`TR 2026/016285`, `TR 2026/016633`, `TR 2026/020266`) are fully disclosed in the manuscript.
- All source code (including `fns_q16.c` and the ARM Cortex-M4 cross-compilation harness), deterministic seeds, and raw JSON telemetry are provided for independent academic verification.

Thank you for your time and consideration.

Sincerely,  
**Volkan Dağlı** *(on behalf of Zerrin Dağlı and Dağhan Dağlı)*  
Anadolu University & ITouch Systems, Cukurova University Technopark, Türkiye  
`vdagli@aof.anadolu.edu.tr` | `ask@answerr.me`
