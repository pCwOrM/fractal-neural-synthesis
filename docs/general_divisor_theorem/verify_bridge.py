#!/usr/bin/env python3
"""
Exhaustive Two-Way Bridge Verification: Volkan's Functional API vs Dan's Prime-Support Specification
Connecting:
  - Volkan Dağlı: pCwOrM/general-divisor-theorem (GeneralDivisorTheorem.lean)
  - Dan Hawkley:  thinkthoughts/gap-lean4-port-gdt (gdt-readingpoint)
  - Zenodo:       10.5281/zenodo.23316070
"""

import math
import sys
from fractions import Fraction as Q

sys.stdout.reconfigure(encoding='utf-8')

def prime_factors(n: int) -> set:
    if n <= 1:
        return set()
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors

def prod(s) -> int:
    res = 1
    for x in s:
        res *= x
    return res

def phi(n: int) -> int:
    if n <= 0:
        return 0
    res = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            res -= res // p
        p += 1
    if temp > 1:
        res -= res // temp
    return res

# ==========================================
# 1. Volkan's Functional API Implementation
# ==========================================
def volkan_rad(n: int) -> int:
    if n <= 0: return 0
    return prod(prime_factors(n))

def volkan_d(N: int, m: int) -> int:
    return volkan_rad(math.gcd(m, N))

def volkan_R(N: int, m: int) -> int:
    d = volkan_d(N, m)
    return volkan_rad(N) // d if d > 0 else 0

def volkan_Tmin(N: int, m: int) -> int:
    return m * volkan_R(N, m)

def volkan_C(d: int) -> Q:
    p = phi(d)
    return Q(d, p) if p > 0 else Q(0)

def volkan_is_admissible(N: int, m: int, a: int) -> bool:
    d = volkan_d(N, m)
    return math.gcd(a, d) == 1

def volkan_S_indicator(N: int, m: int, a: int, n: int) -> bool:
    return (n % m == a % m) and (math.gcd(n, N) == 1)

# ==========================================
# 2. Dan's Prime-Support API Implementation
# ==========================================
def dan_radN(N: int) -> int:
    return prod(prime_factors(N))

def dan_d(N: int, m: int) -> int:
    return prod(prime_factors(N) & prime_factors(m))

def dan_Rset(N: int, m: int) -> set:
    return prime_factors(N) - prime_factors(m)

def dan_R(N: int, m: int) -> int:
    return prod(dan_Rset(N, m))

def dan_Tmin(N: int, m: int) -> int:
    return m * dan_R(N, m)

def dan_correction_factor(d: int) -> Q:
    p = phi(d)
    return Q(d, p) if p > 0 else Q(0)

def dan_is_admissible(a: int, d: int) -> bool:
    return math.gcd(a, d) == 1

def dan_Good(N: int, m: int, a: int, n: int) -> bool:
    return (n % m == a % m) and (math.gcd(n, N) == 1)


# ==========================================
# 3. Main Verification Suite
# ==========================================
def main():
    print("=" * 70)
    print("  TWO-WAY GDT BRIDGE VERIFICATION (VolkanBridge.lean)")
    print("  Volkan API (Functional) <===> Dan API (Prime-Support)")
    print("=" * 70)

    # 1. Distinguishing Benchmark Checks (§3.3)
    print("\n[Phase 1] §3.3 Distinguishing Benchmarks Verification:")
    
    # Case 1: N=18, m=2, a=1
    v_d18, d_d18 = volkan_d(18, 2), dan_d(18, 2)
    v_R18, d_R18 = volkan_R(18, 2), dan_R(18, 2)
    v_T18, d_T18 = volkan_Tmin(18, 2), dan_Tmin(18, 2)
    assert v_d18 == d_d18 == 2, "d mismatch on N=18, m=2"
    assert v_R18 == d_R18 == 3, "R mismatch on N=18, m=2"
    assert v_T18 == d_T18 == 6, f"T_min mismatch on N=18, m=2: expected 6, got {v_T18}"
    assert v_T18 < 18, "T_min must be strictly less than N=18"
    assert volkan_is_admissible(18, 2, 1) == dan_is_admissible(1, d_d18) == True
    print("  ✓ Benchmark §3.3(i) N=18, m=2, a=1 -> d=2, R=3, T_min=6 (< 18) [PASS]")

    # Case 2: N=5, m=6, a=2
    v_d5, d_d5 = volkan_d(5, 6), dan_d(5, 6)
    v_R5, d_R5 = volkan_R(5, 6), dan_R(5, 6)
    v_T5, d_T5 = volkan_Tmin(5, 6), dan_Tmin(5, 6)
    assert v_d5 == d_d5 == 1, "d mismatch on N=5, m=6"
    assert v_R5 == d_R5 == 5, "R mismatch on N=5, m=6"
    assert v_T5 == d_T5 == 30, "T_min mismatch on N=5, m=6"
    assert volkan_is_admissible(5, 6, 2) == dan_is_admissible(2, d_d5) == True
    print("  ✓ Benchmark §3.3(ii) N=5, m=6, a=2 -> d=1, R=5, T_min=30, Admissible=True [PASS]")

    # Canonical C-factors
    assert volkan_C(6) == dan_correction_factor(6) == Q(3, 1)
    assert volkan_C(10) == dan_correction_factor(10) == Q(5, 2)
    assert volkan_C(30) == dan_correction_factor(30) == Q(15, 4)
    print("  ✓ Canonical C-factors: C(6)=3.0, C(10)=2.5, C(30)=3.75 [PASS]")

    # 2. Comprehensive Parameter Sweep
    print("\n[Phase 2] Parameter Space Exhaustive Sweep:")
    total_pairs = 0
    total_triples = 0
    total_period_solutions = 0

    N_samples = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 42, 60, 84, 90, 120, 180, 210, 420]
    m_samples = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 18, 20, 24, 30, 42, 60]

    for N in N_samples:
        for m in m_samples:
            vd = volkan_d(N, m)
            dd = dan_d(N, m)
            assert vd == dd, f"d mismatch at N={N}, m={m}"

            vR = volkan_R(N, m)
            dR = dan_R(N, m)
            assert vR == dR, f"R mismatch at N={N}, m={m}"

            vT = volkan_Tmin(N, m)
            dT = dan_Tmin(N, m)
            lcm_val = math.lcm(m, volkan_rad(N))
            assert vT == dT == lcm_val, f"T_min mismatch at N={N}, m={m}"

            vC = volkan_C(vd)
            dC = dan_correction_factor(dd)
            assert vC == dC, f"C mismatch at N={N}, m={m}"

            total_pairs += 1

            # Test residues
            for a in range(m):
                v_adm = volkan_is_admissible(N, m, a)
                d_adm = dan_is_admissible(a, dd)
                assert v_adm == d_adm, f"Admissibility mismatch at N={N}, m={m}, a={a}"

                total_triples += 1

                # If T_min is reasonable, verify solution count and indicator equality
                if vT <= 500:
                    sol_count = 0
                    for n in range(vT):
                        v_ind = volkan_S_indicator(N, m, a, n)
                        d_good = dan_Good(N, m, a, n)
                        assert v_ind == d_good, f"Indicator mismatch at n={n}"
                        if v_ind:
                            sol_count += 1

                    if v_adm:
                        expected_sol = phi(vR)
                        assert sol_count == expected_sol, f"Count mismatch: got {sol_count}, expected {expected_sol}"
                    else:
                        assert sol_count == 0, f"Inadmissible must have 0 solutions, got {sol_count}"

                    total_period_solutions += 1

    print(f"  ✓ (N, m) parameter pairs tested: {total_pairs} (100% agreement)")
    print(f"  ✓ (N, m, a) residue triples tested: {total_triples} (100% agreement)")
    print(f"  ✓ Full-period solution counting simulations: {total_period_solutions} (100% exact)")
    print("\n" + "=" * 70)
    print("  TWO-WAY BRIDGE CROSS-VALIDATION: 100% PASS (0 DEFECTS)")
    print("=" * 70)

if __name__ == "__main__":
    main()
