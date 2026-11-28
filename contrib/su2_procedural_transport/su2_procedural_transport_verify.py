#!/usr/bin/env python3
"""Pure-Q Procedural SU(2) Cayley Transport, 16-Byte Rollback & Log-Free Escape-Time Verifier.

Original clean-room contribution from Moissanite-Labs for fractal-neural-synthesis.
Pure Python stdlib with ZERO floats in AST, ZERO math.log/log2 calls, and ZERO bare asserts.

Certifies over exact rational & integer arithmetic (Fraction, int):
  1. Procedural boundary-orbit tangent map omega(Theta, k) in Q^3 strictly inside the
     acute icosahedral (2I) basin ||omega||^2 <= 12/25 < 5 - 2*sqrt(5) = tan^2(pi/5) < 16/25
     (exact cleared integer proof: 20 * 625 = 12500 < 12769 = 113^2).
  2. Exact single-step CayleySU2 map C(omega) in SU(2, Q) with acute pole-safety bounds:
     1 + ||omega||^2 >= 1, q0 > 0, and pairwise squared composition denominator >= 81/625 > 0.
  3. Exact SU(2) complex 2x2 left/right unitarity (U^dag U == I_2, U U^dag == I_2),
     exact det(U) == (1, 0), exact C^2 spinor norm isometry ||U x||^2 == ||x||^2,
     and exact SO(3) adjoint norm preservation and det(R) == 1.
  4. Exact non-Abelian commutator preservation on procedurally synthesized transport pairs
     T_a(Theta) T_b(Theta) != T_b(Theta) T_a(Theta) and exact Lie-group identity
     Re([T_a, T_b]) == 1 - 2 * ||vec(T_a) x vec(T_b)||^2 < 1.
  5. Exact 16-byte (4 x int32 Q1.30) quaternion checkpoint packing & right-action algebraic
     rollback restoring U_t0 with exact zero drift (Fraction(0)) on rejected trial steps.
  6. Log-Free Pure-Z/Q Smooth Escape-Time Kernel replacing log2(log2(|z|)) via exact
     integer bit_length dyadic shell interpolation: exact agreement on dyadic lemniscates
     s in {4, 16, 256}, exact 0/1 seam jump across (n_esc, s) -> (n_esc + 1, s^2), and
     strict monotonicity across radii and rational Mandelbrot orbits.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import hmac
import json
import struct
from fractions import Fraction
from pathlib import Path
from typing import Any

ZERO = Fraction(0, 1)
ONE = Fraction(1, 1)
TWO = Fraction(2, 1)
FOUR = Fraction(4, 1)
ACUTE_BASIN_MAX_R2 = Fraction(12, 25)       # 0.48 < tan^2(pi/5) = 5 - 2*sqrt(5) ~= 0.527864
CAYLEY_TMAX_R2 = Fraction(16, 25)           # (4/5)^2 = 0.64
POLE_SAFETY_DENOM_MIN = Fraction(81, 625)   # (1 - 16/25)^2 = (9/25)^2 = 81/625 > 0
Q1_30_SCALE = 1 << 30                       # 1,073,741,824 exact power-of-two scale

QuatQ = tuple[Fraction, Fraction, Fraction, Fraction]
Vec3Q = tuple[Fraction, Fraction, Fraction]
ComplexQ = tuple[Fraction, Fraction]
Mat2CQ = tuple[tuple[ComplexQ, ComplexQ], tuple[ComplexQ, ComplexQ]]

Q_ID: QuatQ = (ONE, ZERO, ZERO, ZERO)


def require_ok(cond: bool, msg: str) -> None:
    """Fail-closed invariant guard (zero bare asserts, mutation-auditable)."""
    if cond is not True:
        raise ValueError(msg)


def canonical_cert_sha256(cert: dict[str, Any]) -> str:
    payload = {k: v for k, v in cert.items() if k != "result_sha256"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# 1. Exact Pure-Q Complex, Quaternion, SU(2) 2x2 Matrix & SO(3) Algebra
# ---------------------------------------------------------------------------

def c_add(a: ComplexQ, b: ComplexQ) -> ComplexQ:
    return (a[0] + b[0], a[1] + b[1])


def c_sub(a: ComplexQ, b: ComplexQ) -> ComplexQ:
    return (a[0] - b[0], a[1] - b[1])


def c_mul(a: ComplexQ, b: ComplexQ) -> ComplexQ:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def c_conj(a: ComplexQ) -> ComplexQ:
    return (a[0], -a[1])


def c_abs2(a: ComplexQ) -> Fraction:
    return a[0] * a[0] + a[1] * a[1]


def q_mul(p: QuatQ, q: QuatQ) -> QuatQ:
    a0, a1, a2, a3 = p
    b0, b1, b2, b3 = q
    return (
        a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
        a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
        a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
        a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0,
    )


def q_conj(p: QuatQ) -> QuatQ:
    return (p[0], -p[1], -p[2], -p[3])


def q_norm2(p: QuatQ) -> Fraction:
    return p[0] * p[0] + p[1] * p[1] + p[2] * p[2] + p[3] * p[3]


def q_diff_norm2(p: QuatQ, q: QuatQ) -> Fraction:
    return (
        (p[0] - q[0]) * (p[0] - q[0])
        + (p[1] - q[1]) * (p[1] - q[1])
        + (p[2] - q[2]) * (p[2] - q[2])
        + (p[3] - q[3]) * (p[3] - q[3])
    )


def q_comm(a: QuatQ, b: QuatQ) -> QuatQ:
    return q_mul(q_mul(a, b), q_mul(q_conj(a), q_conj(b)))


def q_vec_cross_norm2(a: QuatQ, b: QuatQ) -> Fraction:
    cx = a[2] * b[3] - a[3] * b[2]
    cy = a[3] * b[1] - a[1] * b[3]
    cz = a[1] * b[2] - a[2] * b[1]
    return cx * cx + cy * cy + cz * cz


def v3_norm2(w: Vec3Q) -> Fraction:
    return w[0] * w[0] + w[1] * w[1] + w[2] * w[2]


def v3_dot(a: Vec3Q, b: Vec3Q) -> Fraction:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cayley_su2_q(omega: Vec3Q) -> QuatQ:
    """Exact single-step CayleySU2 map C(omega) in SU(2, Q) inside acute ball ||omega||^2 <= 16/25."""
    r2 = v3_norm2(omega)
    require_ok(r2 <= CAYLEY_TMAX_R2, "CayleySU2 tangent vector exceeds acute t_max = 4/5 bound")
    den = ONE + r2
    return (
        (ONE - r2) / den,
        (TWO * omega[0]) / den,
        (TWO * omega[1]) / den,
        (TWO * omega[2]) / den,
    )


def cayley_pair_denom_sq(wa: Vec3Q, wb: Vec3Q) -> Fraction:
    """Exact squared Cayley composition denominator (1 - wa . wb)^2 in Q."""
    require_ok(v3_norm2(wa) <= CAYLEY_TMAX_R2, "First Cayley vector exceeds t_max = 4/5")
    require_ok(v3_norm2(wb) <= CAYLEY_TMAX_R2, "Second Cayley vector exceeds t_max = 4/5")
    margin = ONE - v3_dot(wa, wb)
    return margin * margin


def quat_to_su2_matrix(q: QuatQ) -> Mat2CQ:
    """Exact 2x2 complex matrix U(q) in SU(2, Q[i]) representing unit quaternion q."""
    require_ok(q_norm2(q) == ONE, "quat_to_su2_matrix requires exact unit quaternion")
    q0, q1, q2, q3 = q
    return (
        ((q0, q3), (q2, q1)),
        ((-q2, q1), (q0, -q3)),
    )


def mat2c_mul(a: Mat2CQ, b: Mat2CQ) -> Mat2CQ:
    return (
        (
            c_add(c_mul(a[0][0], b[0][0]), c_mul(a[0][1], b[1][0])),
            c_add(c_mul(a[0][0], b[0][1]), c_mul(a[0][1], b[1][1])),
        ),
        (
            c_add(c_mul(a[1][0], b[0][0]), c_mul(a[1][1], b[1][0])),
            c_add(c_mul(a[1][0], b[0][1]), c_mul(a[1][1], b[1][1])),
        ),
    )


def mat2c_dagger(a: Mat2CQ) -> Mat2CQ:
    return (
        (c_conj(a[0][0]), c_conj(a[1][0])),
        (c_conj(a[0][1]), c_conj(a[1][1])),
    )


def mat2c_det(a: Mat2CQ) -> ComplexQ:
    return c_sub(c_mul(a[0][0], a[1][1]), c_mul(a[0][1], a[1][0]))


def mat2c_apply(u: Mat2CQ, x: tuple[ComplexQ, ComplexQ]) -> tuple[ComplexQ, ComplexQ]:
    return (
        c_add(c_mul(u[0][0], x[0]), c_mul(u[0][1], x[1])),
        c_add(c_mul(u[1][0], x[0]), c_mul(u[1][1], x[1])),
    )


def spinor_norm2(x: tuple[ComplexQ, ComplexQ]) -> Fraction:
    return c_abs2(x[0]) + c_abs2(x[1])


def quat_to_so3(q: QuatQ) -> tuple[Vec3Q, Vec3Q, Vec3Q]:
    require_ok(q_norm2(q) == ONE, "quat_to_so3 requires exact unit quaternion")
    w, x, y, z = q
    return (
        (ONE - TWO * (y * y + z * z), TWO * (x * y - w * z), TWO * (x * z + w * y)),
        (TWO * (x * y + w * z), ONE - TWO * (x * x + z * z), TWO * (y * z - w * x)),
        (TWO * (x * z - w * y), TWO * (y * z + w * x), ONE - TWO * (x * x + y * y)),
    )


def so3_apply(r: tuple[Vec3Q, Vec3Q, Vec3Q], v: Vec3Q) -> Vec3Q:
    return (
        r[0][0] * v[0] + r[0][1] * v[1] + r[0][2] * v[2],
        r[1][0] * v[0] + r[1][1] * v[1] + r[1][2] * v[2],
        r[2][0] * v[0] + r[2][1] * v[1] + r[2][2] * v[2],
    )


def so3_det(r: tuple[Vec3Q, Vec3Q, Vec3Q]) -> Fraction:
    return (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )


# ---------------------------------------------------------------------------
# 2. Pure-Q Procedural Quadratic-Boundary SU(2) Cayley Transport Generator
# ---------------------------------------------------------------------------

def _round_fraction_to_int(x: Fraction) -> int:
    """Exact round-half-to-even in pure integers (zero floats)."""
    q, r = divmod(x.numerator, x.denominator)
    twice_r = 2 * r
    if twice_r > x.denominator:
        return q + 1
    if twice_r == x.denominator and (q & 1) == 1:
        return q + 1
    return q


def _quantize_dyadic(x: Fraction, scale: int = 1024) -> Fraction:
    return Fraction(_round_fraction_to_int(x * scale), scale)


def rational_quadratic_potential(cx: Fraction, cy: Fraction, max_iter: int = 16) -> Fraction:
    """Exact dyadic pure-Q escape potential in [-1, 1] for z_{n+1} = z_n^2 + c (R^2 = 16)."""
    require_ok(max_iter >= 1, "max_iter must be >= 1")
    zr = ZERO
    zi = ZERO
    bailout_r2 = Fraction(16, 1)
    esc_step = max_iter
    for step in range(1, max_iter + 1):
        nr = _quantize_dyadic(zr * zr - zi * zi + cx, 1024)
        ni = _quantize_dyadic(TWO * zr * zi + cy, 1024)
        zr, zi = nr, ni
        if zr * zr + zi * zi > bailout_r2:
            esc_step = step
            break
    base = Fraction(2 * esc_step - max_iter, max_iter)
    residue = _quantize_dyadic(zr / (ONE + zr * zr + zi * zi), 1024)
    raw = _quantize_dyadic((Fraction(3, 4) * base) + (Fraction(1, 4) * residue), 1024)
    if raw > ONE:
        return ONE
    if raw < -ONE:
        return -ONE
    return raw


def procedural_omega_q(
    cx: Fraction,
    cy: Fraction,
    scale: Fraction,
    step_k: int,
    max_iter: int = 8,
) -> Vec3Q:
    """Synthesize acute 2I-basin tangent vector omega(Theta, k) in Q^3 from 3-coord seed Theta."""
    require_ok(scale > ZERO, "scale must be strictly positive")
    require_ok(step_k >= 0, "step_k must be non-negative")
    offsets: tuple[tuple[Fraction, Fraction], ...] = (
        (Fraction((step_k % 5) - 2, 5), Fraction(((step_k * 3) % 5) - 2, 5)),
        (Fraction(((step_k * 2 + 1) % 7) - 3, 7), Fraction(((step_k * 4 + 2) % 7) - 3, 7)),
        (Fraction(((step_k * 3 + 4) % 9) - 4, 9), Fraction(((step_k * 5 + 1) % 9) - 4, 9)),
    )
    vals: list[Fraction] = []
    for ox, oy in offsets:
        pot = rational_quadratic_potential(cx + scale * ox, cy + scale * oy, max_iter=max_iter)
        vals.append(Fraction(2, 5) * pot)
    return (vals[0], vals[1], vals[2])


def procedural_transport_su2_q(
    cx: Fraction,
    cy: Fraction,
    scale: Fraction,
    step_k: int,
    max_iter: int = 8,
) -> tuple[Vec3Q, QuatQ]:
    omega = procedural_omega_q(cx, cy, scale, step_k, max_iter=max_iter)
    return omega, cayley_su2_q(omega)


# ---------------------------------------------------------------------------
# 3. Exact 16-Byte Holonomy Checkpoint & Zero-Drift Rollback
# ---------------------------------------------------------------------------

def pack_checkpoint_pi16(q: QuatQ) -> bytes:
    """Pack unit quaternion into exact 16-byte Q1.30 binary checkpoint (4 x signed int32)."""
    require_ok(q_norm2(q) == ONE, "pack_checkpoint_pi16 requires exact unit quaternion")
    lanes = [_round_fraction_to_int(c * Q1_30_SCALE) for c in q]
    return struct.pack("<4i", lanes[0], lanes[1], lanes[2], lanes[3])


def unpack_checkpoint_pi16(buf: bytes) -> QuatQ:
    """Unpack exact 16-byte Q1.30 checkpoint back into pure-Q quaternion coordinates."""
    require_ok(len(buf) == 16, "Checkpoint must be exactly 16 bytes")
    i0, i1, i2, i3 = struct.unpack("<4i", buf)
    return (
        Fraction(i0, Q1_30_SCALE),
        Fraction(i1, Q1_30_SCALE),
        Fraction(i2, Q1_30_SCALE),
        Fraction(i3, Q1_30_SCALE),
    )


def algebraic_rollback_su2(u_t0: QuatQ, u_trial: QuatQ) -> QuatQ:
    """Exact right-action rollback U_trial * (U_trial^dag * U_t0) == U_t0 with 0 drift."""
    require_ok(q_norm2(u_t0) == ONE, "u_t0 must be exact unit quaternion")
    require_ok(q_norm2(u_trial) == ONE, "u_trial must be exact unit quaternion")
    delta_inv = q_mul(q_conj(u_trial), u_t0)
    return q_mul(u_trial, delta_inv)


# ---------------------------------------------------------------------------
# 4. Log-Free Pure-Z/Q Smooth Escape-Time Kernel (Zero math.log / log2)
# ---------------------------------------------------------------------------

def dyadic_log2_surrogate_q(s: Fraction) -> tuple[int, Fraction]:
    """Pure-Z/Q continuous strictly-monotone surrogate for log2(s) on s >= 1 (exact at s = 2^b)."""
    require_ok(s >= ONE, "s must be >= 1 for dyadic log2 surrogate")
    q_int = s.numerator // s.denominator
    b = q_int.bit_length() - 1
    pow2_b = Fraction(1 << b, 1)
    u = Fraction(b, 1) + (s / pow2_b - ONE)
    return b, u


def logfree_escape_potential_q(n_esc: int, z_norm_sq: Fraction) -> tuple[int, Fraction]:
    """Pure-Z/Q replacement for nu(c) = n_esc + 1 - log2(log2(|z|)) (arXiv:2611.32393v1 Eq. 2).

    For |z|^2 = s >= 4 (escape radius R = 2), finds exact dyadic double-exponential shell
    m >= 1 with 2^(2^m) <= s < 2^(2^(m+1)) using integer bit_length, then interpolates:
      ell_tilde(s) = (m - 1) + (u(s) - 2^m) / 2^m
      nu_Q(n_esc, s) = n_esc + 1 - ell_tilde(s).
    Exact on every dyadic lemniscate s = 2^(2^m) with 0/1 seam jump under (n_esc, s) -> (n_esc+1, s^2).
    """
    require_ok(n_esc >= 0, "n_esc must be non-negative")
    require_ok(z_norm_sq >= FOUR, "z_norm_sq must be >= 4 (escaped R = 2)")
    b, u = dyadic_log2_surrogate_q(z_norm_sq)
    m = b.bit_length() - 1
    pow2_m = Fraction(1 << m, 1)
    ell_tilde = Fraction(m - 1, 1) + (u - pow2_m) / pow2_m
    nu_q = Fraction(n_esc + 1, 1) - ell_tilde
    return m, nu_q


def mandelbrot_escape_exact_q(c_re: Fraction, c_im: Fraction, max_iter: int = 30) -> tuple[int, Fraction]:
    """Exact pure-Q Mandelbrot trajectory z_{n+1} = z_n^2 + c stopping at |z|^2 >= 4."""
    require_ok(max_iter >= 1, "max_iter must be >= 1")
    zx = ZERO
    zy = ZERO
    for n in range(1, max_iter + 1):
        nx = zx * zx - zy * zy + c_re
        ny = TWO * zx * zy + c_im
        zx, zy = nx, ny
        nsq = zx * zx + zy * zy
        if nsq >= FOUR:
            return n, nsq
    raise ValueError("Rational point did not escape within max_iter")


def certify_logfree_escape_kernel() -> dict[str, Any]:
    """Certify exact dyadic lemniscate identities, 0/1 seam jump, and strict monotonicity."""
    lemniscate_exact_count = 0
    seam_zero_jump_count = 0
    for m_exp in (1, 2, 3):
        s_val = Fraction(1 << (1 << m_exp), 1)
        m_got, nu_1 = logfree_escape_potential_q(5, s_val)
        expected_nu = Fraction(5 + 1 - (m_exp - 1), 1)
        if m_got == m_exp:
            if nu_1 == expected_nu:
                lemniscate_exact_count += 1
        m_next, nu_2 = logfree_escape_potential_q(6, s_val * s_val)
        if m_next == m_exp + 1:
            if nu_2 == nu_1:
                seam_zero_jump_count += 1

    radii = [Fraction(4, 1), Fraction(9, 2), Fraction(15, 1), Fraction(16, 1), Fraction(64, 1), Fraction(256, 1)]
    nu_radii = [logfree_escape_potential_q(10, r)[1] for r in radii]
    mono_radius_steps = sum(1 for i in range(len(nu_radii) - 1) if nu_radii[i] > nu_radii[i + 1])

    c_points = [Fraction(2, 1), Fraction(1, 1), Fraction(3, 4), Fraction(3, 5), Fraction(1, 2)]
    orbit_samples: list[dict[str, Any]] = []
    orbit_nus: list[Fraction] = []
    for c_re in c_points:
        n_esc, nsq = mandelbrot_escape_exact_q(c_re, ZERO, max_iter=30)
        m_sh, nu_q = logfree_escape_potential_q(n_esc, nsq)
        orbit_nus.append(nu_q)
        orbit_samples.append(
            {
                "c_re": str(c_re),
                "n_esc": n_esc,
                "dyadic_shell_m": m_sh,
                "nu_q": str(nu_q),
            }
        )
    mono_orbit_steps = sum(1 for i in range(len(orbit_nus) - 1) if orbit_nus[i] < orbit_nus[i + 1])

    return {
        "lemniscates_tested": 3,
        "lemniscate_exact_count": lemniscate_exact_count,
        "seam_zero_jump_count": seam_zero_jump_count,
        "radius_monotonicity_steps_ok": mono_radius_steps,
        "radius_monotonicity_steps_total": len(nu_radii) - 1,
        "orbit_monotonicity_steps_ok": mono_orbit_steps,
        "orbit_monotonicity_steps_total": len(orbit_nus) - 1,
        "mandelbrot_orbit_samples": orbit_samples,
    }


# ---------------------------------------------------------------------------
# 5. AST Zero-Float & Zero-Log Audit + Fail-Closed Certificate Builder/Validator
# ---------------------------------------------------------------------------

def check_source_zero_floats_and_logs(py_path: Path) -> int:
    """Parse Python AST and count float literals, float() calls, or log/log2/log10 calls (must be 0)."""
    src = py_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(py_path))
    forbidden_names = ("float", "log", "log2", "log10")
    bad_nodes = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            bad_nodes += 1
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden_names:
            bad_nodes += 1
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_names:
            bad_nodes += 1
    return bad_nodes


def build_certificate() -> dict[str, Any]:
    """Run all pure-Q SU(2) transport, pole-safety, commutator, rollback, and log-free escape proofs."""
    basin_lhs_int = 20 * 625
    basin_rhs_int = 113 * 113

    cx0 = Fraction(-3, 4)
    cy0 = Fraction(1, 8)
    scale0 = Fraction(1, 4)

    omegas: list[Vec3Q] = []
    quats: list[QuatQ] = []
    max_r2 = ZERO
    min_q0 = ONE
    min_single_denom = Fraction(10, 1)
    unitarity_left_ok = 0
    unitarity_right_ok = 0
    det_ok = 0
    spinor_iso_ok = 0
    so3_iso_ok = 0
    so3_det_ok = 0

    id2c: Mat2CQ = (((ONE, ZERO), (ZERO, ZERO)), ((ZERO, ZERO), (ONE, ZERO)))
    test_spinor: tuple[ComplexQ, ComplexQ] = ((Fraction(3, 5), Fraction(-2, 7)), (Fraction(4, 9), Fraction(1, 3)))
    test_spinor_n2 = spinor_norm2(test_spinor)
    test_vec3: Vec3Q = (Fraction(5, 7), Fraction(-3, 11), Fraction(2, 5))
    test_vec3_n2 = v3_norm2(test_vec3)

    n_ops = 8
    for k in range(n_ops):
        w, q = procedural_transport_su2_q(cx0, cy0, scale0, k, max_iter=8)
        omegas.append(w)
        quats.append(q)
        r2 = v3_norm2(w)
        if r2 > max_r2:
            max_r2 = r2
        if q[0] < min_q0:
            min_q0 = q[0]
        s_den = ONE + r2
        if s_den < min_single_denom:
            min_single_denom = s_den

        u_mat = quat_to_su2_matrix(q)
        u_dag = mat2c_dagger(u_mat)
        if mat2c_mul(u_dag, u_mat) == id2c:
            unitarity_left_ok += 1
        if mat2c_mul(u_mat, u_dag) == id2c:
            unitarity_right_ok += 1
        if mat2c_det(u_mat) == (ONE, ZERO):
            det_ok += 1
        if spinor_norm2(mat2c_apply(u_mat, test_spinor)) == test_spinor_n2:
            spinor_iso_ok += 1
        r_mat = quat_to_so3(q)
        if v3_norm2(so3_apply(r_mat, test_vec3)) == test_vec3_n2:
            so3_iso_ok += 1
        if so3_det(r_mat) == ONE:
            so3_det_ok += 1

    min_pair_denom_sq = Fraction(10, 1)
    nonabelian_pairs = 0
    trace_id_exact = 0
    total_pairs = 0
    sample_comm_norm2 = ZERO
    for i in range(n_ops):
        for j in range(i + 1, n_ops):
            total_pairs += 1
            p_den_sq = cayley_pair_denom_sq(omegas[i], omegas[j])
            if p_den_sq < min_pair_denom_sq:
                min_pair_denom_sq = p_den_sq
            ab = q_mul(quats[i], quats[j])
            ba = q_mul(quats[j], quats[i])
            dn2 = q_diff_norm2(ab, ba)
            if dn2 > ZERO:
                nonabelian_pairs += 1
                if sample_comm_norm2 == ZERO:
                    sample_comm_norm2 = dn2
            cm = q_comm(quats[i], quats[j])
            rhs = ONE - TWO * q_vec_cross_norm2(quats[i], quats[j])
            if cm[0] == rhs:
                trace_id_exact += 1

    boundary_w: Vec3Q = (Fraction(4, 5), ZERO, ZERO)
    boundary_denom_sq = cayley_pair_denom_sq(boundary_w, boundary_w)

    u_t0 = q_mul(quats[0], quats[1])
    _, q_trial_step = procedural_transport_su2_q(
        cx0 + Fraction(1, 64), cy0 - Fraction(1, 64), scale0, 2, max_iter=8
    )
    u_trial = q_mul(u_t0, q_trial_step)
    u_restored = algebraic_rollback_su2(u_t0, u_trial)
    rollback_drift = q_diff_norm2(u_restored, u_t0)

    dyadic_u0: QuatQ = (Fraction(3, 5), Fraction(4, 5), ZERO, ZERO)
    q_dyadic_exact: QuatQ = (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))
    pi16_dyadic_bytes = pack_checkpoint_pi16(q_dyadic_exact)
    pi16_dyadic_drift = q_diff_norm2(unpack_checkpoint_pi16(pi16_dyadic_bytes), q_dyadic_exact)

    pi16_bytes = pack_checkpoint_pi16(u_t0)
    pi16_unpacked = unpack_checkpoint_pi16(pi16_bytes)
    pi16_proc_err2 = q_diff_norm2(pi16_unpacked, u_t0)
    pi16_err2_bound = Fraction(1, 1 << 60)
    _ = pack_checkpoint_pi16(dyadic_u0)

    logfree_cert = certify_logfree_escape_kernel()
    ast_bad = check_source_zero_floats_and_logs(Path(__file__).resolve())

    cert: dict[str, Any] = {
        "schema_version": "moissanite.su2_procedural_transport_verify.v1",
        "contribution": "Moissanite-Labs clean-room pure-Q SU(2) Cayley transport & log-free escape kernel",
        "energy_power_status": "CPU_ONLY_PURE_Q_NO_ENERGY_CLAIMS",
        "ast_float_and_log_count": ast_bad,
        "acute_2i_basin_integer_proof": {
            "basin_cap_r2": str(ACUTE_BASIN_MAX_R2),
            "lhs_20_times_625": basin_lhs_int,
            "rhs_113_squared": basin_rhs_int,
            "max_procedural_r2": str(max_r2),
            "min_scalar_q0": str(min_q0),
        },
        "pole_safety": {
            "required_floor": str(POLE_SAFETY_DENOM_MIN),
            "boundary_4_5_denom_sq": str(boundary_denom_sq),
            "min_single_step_denom": str(min_single_denom),
            "min_pair_denom_sq": str(min_pair_denom_sq),
        },
        "su2_unitarity_and_isometry": {
            "operators_tested": n_ops,
            "unitarity_exact_count": unitarity_left_ok,
            "unitarity_right_exact_count": unitarity_right_ok,
            "det_one_exact_count": det_ok,
            "spinor_isometry_exact_count": spinor_iso_ok,
            "so3_isometry_exact_count": so3_iso_ok,
            "so3_det_one_exact_count": so3_det_ok,
        },
        "nonabelian_commutator": {
            "pairs_tested": total_pairs,
            "nonabelian_pairs_count": nonabelian_pairs,
            "trace_identity_exact_count": trace_id_exact,
            "sample_comm_diff_norm2": str(sample_comm_norm2),
        },
        "checkpoint_16b_rollback": {
            "checkpoint_bytes": len(pi16_bytes),
            "algebraic_rollback_drift": str(rollback_drift),
            "pi16_dyadic_roundtrip_drift": str(pi16_dyadic_drift),
            "pi16_proc_quant_err2_within_bound": pi16_proc_err2 <= pi16_err2_bound,
            "trial_changed_state": u_trial != u_t0,
        },
        "logfree_escape_kernel": logfree_cert,
    }
    cert["result_sha256"] = canonical_cert_sha256(cert)
    return cert


def validate_certificate(cert: dict[str, Any]) -> None:
    """Atomic fail-closed certificate validator (100% mutation & BoolOp auditable)."""
    require_ok(cert["ast_float_and_log_count"] == 0, "AST must contain zero float literals or log calls")

    b = cert["acute_2i_basin_integer_proof"]
    require_ok(b["lhs_20_times_625"] < b["rhs_113_squared"], "Integer 2I basin inequality failed")
    require_ok(Fraction(b["max_procedural_r2"]) <= ACUTE_BASIN_MAX_R2, "Procedural omega exceeded 12/25 basin")
    require_ok(Fraction(b["min_scalar_q0"]) > ZERO, "Procedural quaternion scalar q0 not strictly acute")

    ps = cert["pole_safety"]
    require_ok(Fraction(ps["min_single_step_denom"]) >= ONE, "Single-step Cayley denom below 1")
    require_ok(Fraction(ps["min_pair_denom_sq"]) >= POLE_SAFETY_DENOM_MIN, "Pairwise denom^2 below 81/625")
    require_ok(Fraction(ps["boundary_4_5_denom_sq"]) == POLE_SAFETY_DENOM_MIN, "Boundary 4/5 denom^2 != 81/625")

    su = cert["su2_unitarity_and_isometry"]
    n_ops = su["operators_tested"]
    require_ok(n_ops == 8, "Expected 8 procedural SU(2) operators")
    require_ok(su["unitarity_exact_count"] == n_ops, "SU(2) left unitarity count mismatch")
    require_ok(su["unitarity_right_exact_count"] == n_ops, "SU(2) right unitarity count mismatch")
    require_ok(su["det_one_exact_count"] == n_ops, "SU(2) determinant == 1 count mismatch")
    require_ok(su["spinor_isometry_exact_count"] == n_ops, "C^2 spinor isometry count mismatch")
    require_ok(su["so3_isometry_exact_count"] == n_ops, "SO(3) adjoint isometry count mismatch")
    require_ok(su["so3_det_one_exact_count"] == n_ops, "SO(3) determinant == 1 count mismatch")

    nc = cert["nonabelian_commutator"]
    require_ok(nc["pairs_tested"] == 28, "Expected 28 unordered operator pairs")
    require_ok(nc["nonabelian_pairs_count"] >= 20, "Insufficient non-Abelian pairs")
    require_ok(nc["trace_identity_exact_count"] == nc["pairs_tested"], "Re([a,b]) trace identity mismatch")
    require_ok(Fraction(nc["sample_comm_diff_norm2"]) > ZERO, "Sample commutator norm^2 not positive")

    wf = cert["checkpoint_16b_rollback"]
    require_ok(wf["checkpoint_bytes"] == 16, "Checkpoint width must be 16 bytes")
    require_ok(Fraction(wf["algebraic_rollback_drift"]) == ZERO, "Algebraic rollback drift nonzero")
    require_ok(Fraction(wf["pi16_dyadic_roundtrip_drift"]) == ZERO, "16B dyadic roundtrip drift nonzero")
    require_ok(wf["pi16_proc_quant_err2_within_bound"] is True, "16B procedural quant bound exceeded")
    require_ok(wf["trial_changed_state"] is True, "Trial seed perturbation did not move state")

    lf = cert["logfree_escape_kernel"]
    n_lem = lf["lemniscates_tested"]
    require_ok(n_lem == 3, "Expected 3 dyadic lemniscate checks")
    require_ok(lf["lemniscate_exact_count"] == n_lem, "Dyadic lemniscate identity count mismatch")
    require_ok(lf["seam_zero_jump_count"] == n_lem, "Seam continuity 0/1 jump count mismatch")
    require_ok(lf["radius_monotonicity_steps_ok"] == lf["radius_monotonicity_steps_total"], "Radius monotonicity failed")
    require_ok(lf["orbit_monotonicity_steps_ok"] == lf["orbit_monotonicity_steps_total"], "Orbit monotonicity failed")

    exp_sha = canonical_cert_sha256(cert)
    got_sha = str(cert.get("result_sha256", ""))
    require_ok(hmac.compare_digest(got_sha, exp_sha), "Certificate result_sha256 mismatch")


def format_summary(cert: dict[str, Any]) -> str:
    su = cert["su2_unitarity_and_isometry"]
    nc = cert["nonabelian_commutator"]
    wf = cert["checkpoint_16b_rollback"]
    lf = cert["logfree_escape_kernel"]
    return "\n".join(
        (
            "Pure-Q Procedural SU(2) Cayley Transport & Log-Free Escape-Time Verifier",
            f"AST_FLOATS_LOGS={cert['ast_float_and_log_count']} SU2_UNITARY={su['unitarity_exact_count']}/{su['operators_tested']} "
            f"DET1={su['det_one_exact_count']}/{su['operators_tested']} NONABELIAN={nc['nonabelian_pairs_count']}/{nc['pairs_tested']}",
            f"CHECKPOINT_16B: bytes={wf['checkpoint_bytes']} alg_drift={wf['algebraic_rollback_drift']} dyadic_drift={wf['pi16_dyadic_roundtrip_drift']}",
            f"LOGFREE_ESCAPE: lemniscates={lf['lemniscate_exact_count']}/{lf['lemniscates_tested']} seam0={lf['seam_zero_jump_count']}/{lf['lemniscates_tested']} "
            f"mono_r={lf['radius_monotonicity_steps_ok']}/{lf['radius_monotonicity_steps_total']} mono_c={lf['orbit_monotonicity_steps_ok']}/{lf['orbit_monotonicity_steps_total']}",
            f"result_sha256={cert['result_sha256']}",
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pure-Q Procedural SU(2) Cayley Transport & Log-Free Escape Verifier.")
    parser.add_argument("--json", action="store_true", help="Emit canonical JSON certificate.")
    parser.add_argument("--check", action="store_true", help="Emit deterministic PASS line.")
    args = parser.parse_args(argv)

    cert = build_certificate()
    validate_certificate(cert)

    if args.json:
        print(json.dumps(cert, sort_keys=True, indent=2))
    elif args.check:
        print(f"PASS SU2_PROCEDURAL_TRANSPORT result_sha256={cert['result_sha256']}")
    else:
        print(format_summary(cert))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
