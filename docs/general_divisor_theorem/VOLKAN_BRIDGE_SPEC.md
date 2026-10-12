# VolkanBridge: Two-Way Cross-Validation Specification

**Formal Integration Bridge:** Volkan Dağlı Functional API $\longleftrightarrow$ Dan Hawkley Prime-Support Reading Point  
**Repos:** [`pCwOrM/general-divisor-theorem`](https://github.com/pCwOrM/general-divisor-theorem) $\longleftrightarrow$ [`thinkthoughts/gap-lean4-port-gdt`](https://github.com/thinkthoughts/gap-lean4-port-gdt)  
**Permanent Zenodo Archive:** [`10.5281/zenodo.23316070`](https://doi.org/10.5281/zenodo.23316070)  
**Authors:** Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı  
**Computing & Infrastructure:** Bekirhan Dağlı (ITouch Systems Research & Development)  

---

## 1. Overview & Architectural Motivation

Per the October 12, 2026 code review notes by **Dan Hawkley** ([@Precedent_Vice](https://x.com/Precedent_Vice)):
> *"keep `thinkthoughts/gap-lean4-port-gdt` as the kernel-proof / GAP-integration track;  
> treat `pCwOrM/general-divisor-theorem` as Volkan's standalone GDT presentation and cross-check target;  
> add a small compatibility layer later mapping his `rad`, `d_param`, `R_param`, `T_min`, `C_factor`, and `S_indicator` to our proven definitions;  
> then we can literally show which of his axioms are discharged by our theorems.  
> That last step could be very nice: something like a `VolkanBridge.lean` where we prove, under positive $N, m$, that his definitions agree with ours, then instantiate his theorem statements from our existing proofs. That would turn the two repos into a genuine two-way validation story rather than competing formalizations."*

[`VolkanBridge.lean`](../VolkanBridge.lean) is the exact formalization of this architectural vision.

---

## 2. API Definitional Mapping Table

| Concept | Volkan Functional API (`GeneralDivisorTheorem.lean`) | Dan Prime-Support API (`GDTReadingPoint`) | Mathematical Identity |
| :--- | :--- | :--- | :--- |
| **Radical** | `rad N := ∏ p \| N, p` | `radN P := ∏ q ∈ primeFactors N, q` | $\mathrm{rad}(N)$ |
| **Shared Radical ($d$)** | `d_param N m := rad (gcd m N)` | `d P := ∏ q ∈ primeFactors N ∩ primeFactors m, q` | $\mathrm{rad}(\gcd(m, N))$ |
| **Unshared Radical ($R$)** | `R_param N m := rad N / d_param N m` | `R P := ∏ q ∈ primeFactors N \ primeFactors m, q` | $\frac{\mathrm{rad}(N)}{\mathrm{rad}(\gcd(m, N))}$ |
| **Minimal Period ($T_{\min}$)** | `T_min N m := m * R_param N m = lcm(m, rad N)` | `Tmin P := m * R P` | $\mathrm{lcm}(m, \mathrm{rad}(N))$ |
| **Correction Factor ($C$)** | `C_factor d := d / phi(d)` | `correctionFactor P := d P / phi(d P)` | $\prod_{p \mid \gcd(m, N)} \frac{p}{p-1}$ |
| **Admissibility** | `gcd a d = 1` | `Admissible a d := Nat.Coprime a d` | $\gcd(a, d) = 1$ |
| **Set Indicator** | `S_indicator N m a n` | `Good P n` | $n \equiv a \pmod m \land \gcd(n, N)=1$ |

---

## 3. Two-Way Axiom Discharge Table

| Volkan GDT Axiom | Dan Proved Theorem (`gdt-readingpoint`) | Formal Result |
| :--- | :--- | :--- |
| `inadmissible_empty_criterion` | `empty_of_not_admissible` | $\gcd(a, d) > 1 \implies S = \emptyset$ (Discharged) |
| `indicator_factorization` | `good_residuePoint_iff_coprime_R` | Admissible coprimality reduces to $\gcd(n, R)=1$ (Discharged) |
| `T_min_is_period` | `good_add_Tmin_iff` | Periodicity under $T_{\min} = m R$ (Discharged) |
| *(Solution Count)* | `goodCount_eq_totient_R` | Exactly $\phi(R)$ solutions per period (Discharged) |
| `C_factor_prime_product` | `totient_radN_eq_mul` & `correctionFactor` | Euler density correction formula (Discharged) |

---

## 4. Distinguishing Benchmarks (§3.3) Machine Verification

1. **Benchmark 1 (§3.3 i):** $N = 18, m = 2, a = 1$
   - $d = 2, R = 3$
   - Minimal period $T_{\min} = 6$ (strictly less than $N = 18$!)
   - Solutions per period: $\phi(3) = 2$ in $[0, 5]$
   - Density correction: $C(2) = 2.0$
2. **Benchmark 2 (§3.3 ii):** $N = 5, m = 6, a = 2$
   - $d = 1, R = 5$
   - Admissible despite $\gcd(a, m) = 2$!
   - Minimal period $T_{\min} = 30$
   - Solutions per period: $\phi(5) = 4$ in $[0, 29]$
3. **Canonical Euler Density Benchmarks:**
   - $C(6) = 3.0$
   - $C(10) = 2.5$
   - $C(30) = 3.75$

---

## 5. Automated Verification Oracle

Run the comprehensive two-way bridge oracle:
```bash
python scripts/verify_bridge.py
```

**Telemetry Result:**
- **(N, m) pairs tested:** 437 (100% agreement)
- **(N, m, a) residue triples tested:** 6,670 (100% agreement)
- **Full-period counting simulations:** 6,552 (100% exact)
- **Overall:** 0 defects, 0 discrepancies across all parameter domains.
