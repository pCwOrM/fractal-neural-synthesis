#!/usr/bin/env python3
"""Assertion-free, float-free verification test suite for su2_procedural_transport_verify.py.

Covers all invariant guards and boolean conditions, plus verifies
results_su2_transport_and_s73.json integrity.
Emits 0 stdout bytes on PASS across -I -B, -I -O -B, and -I -B -W error.
"""

from __future__ import annotations

import copy
import io
import json
import sys
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable

_ROOT = str(Path(__file__).resolve().parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import run_s73_adaptive_and_su2_transport as runner
import su2_procedural_transport_verify as su2v


def fail(msg: str) -> None:
    raise RuntimeError(f"R5_SU2_FAIL: {msg}")


def check(cond: bool, msg: str) -> None:
    if cond is not True:
        fail(msg)


def check_raises_val(fn: Callable[[], Any], label: str, match: str | None = None) -> None:
    raised = False
    text = ""
    try:
        fn()
    except ValueError as exc:
        raised = True
        text = str(exc)
    if not raised:
        fail(f"Expected ValueError for {label}")
    if match is not None and match not in text:
        fail(f"Message mismatch for {label}: expected {match!r} in {text!r}")


def test_primitives_and_boundaries() -> None:
    check(su2v.check_source_zero_floats_and_logs(Path(su2v.__file__).resolve()) == 0, "Target AST has floats/logs")
    check(su2v.check_source_zero_floats_and_logs(Path(__file__).resolve()) == 0, "Test AST has floats/logs")

    # CayleySU2 exact boundary (r2 == 16/25 valid, r2 > 16/25 rejected)
    w_edge = (Fraction(4, 5), su2v.ZERO, su2v.ZERO)
    q_edge = su2v.cayley_su2_q(w_edge)
    check(su2v.q_norm2(q_edge) == su2v.ONE, "Edge Cayley quaternion not unit norm")
    check(q_edge[0] == Fraction(9, 41), "Edge Cayley q0 != 9/41")
    w_over = (Fraction(81, 100), su2v.ZERO, su2v.ZERO)
    check_raises_val(lambda: su2v.cayley_su2_q(w_over), "cayley_su2_q over t_max", "t_max")

    # cayley_pair_denom_sq exact boundary 81/625 and rejections
    check(su2v.cayley_pair_denom_sq(w_edge, w_edge) == Fraction(81, 625), "Edge denom_sq != 81/625")
    check_raises_val(lambda: su2v.cayley_pair_denom_sq(w_over, w_edge), "pair denom wa over", "First Cayley")
    check_raises_val(lambda: su2v.cayley_pair_denom_sq(w_edge, w_over), "pair denom wb over", "Second Cayley")

    # Unit-norm & 16-byte checkpoint guards
    non_unit = (su2v.TWO, su2v.ZERO, su2v.ZERO, su2v.ZERO)
    check_raises_val(lambda: su2v.quat_to_su2_matrix(non_unit), "quat_to_su2_matrix non-unit", "unit quaternion")
    check_raises_val(lambda: su2v.quat_to_so3(non_unit), "quat_to_so3 non-unit", "unit quaternion")
    check_raises_val(lambda: su2v.pack_checkpoint_pi16(non_unit), "pack_checkpoint_pi16 non-unit", "unit quaternion")
    check_raises_val(lambda: su2v.algebraic_rollback_su2(non_unit, su2v.Q_ID), "rollback bad u_t0", "u_t0")
    check_raises_val(lambda: su2v.algebraic_rollback_su2(su2v.Q_ID, non_unit), "rollback bad u_trial", "u_trial")
    check_raises_val(lambda: su2v.unpack_checkpoint_pi16(b"\x00" * 15), "unpack 15B", "16 bytes")
    check_raises_val(lambda: su2v.unpack_checkpoint_pi16(b"\x00" * 17), "unpack 17B", "16 bytes")

    # Procedural quadratic potential & omega boundaries
    p1 = su2v.rational_quadratic_potential(su2v.ZERO, su2v.ZERO, max_iter=1)
    check(-su2v.ONE <= p1 <= su2v.ONE, "potential max_iter=1 out of [-1, 1]")
    p_hi = su2v.rational_quadratic_potential(Fraction(10, 1), su2v.ZERO, max_iter=1)
    check(-su2v.ONE <= p_hi <= su2v.ONE, "escaped potential out of [-1, 1]")
    check_raises_val(lambda: su2v.rational_quadratic_potential(su2v.ZERO, su2v.ZERO, max_iter=0), "max_iter=0", "max_iter")

    w0 = su2v.procedural_omega_q(su2v.ZERO, su2v.ZERO, Fraction(1, 4), step_k=0, max_iter=2)
    check(su2v.v3_norm2(w0) <= su2v.ACUTE_BASIN_MAX_R2, "step_k=0 omega exceeded basin")
    check_raises_val(lambda: su2v.procedural_omega_q(su2v.ZERO, su2v.ZERO, su2v.ZERO, step_k=0), "scale=0", "scale")
    check_raises_val(lambda: su2v.procedural_omega_q(su2v.ZERO, su2v.ZERO, Fraction(-1, 4), step_k=0), "scale<0", "scale")
    check_raises_val(lambda: su2v.procedural_omega_q(su2v.ZERO, su2v.ZERO, Fraction(1, 4), step_k=-1), "step_k=-1", "step_k")

    # Round-half-to-even edge cases killing BoolOp mutations
    check(su2v._round_fraction_to_int(Fraction(1, 2)) == 0, "half-to-even 1/2")
    check(su2v._round_fraction_to_int(Fraction(3, 2)) == 2, "half-to-even 3/2")
    check(su2v._round_fraction_to_int(Fraction(3, 4)) == 1, "round up 3/4")
    check(su2v._round_fraction_to_int(Fraction(5, 4)) == 1, "round down odd q 5/4")

    # Log-free escape-time kernel exact boundaries & guard rejections
    b1, u1 = su2v.dyadic_log2_surrogate_q(su2v.ONE)
    check(b1 == 0 and u1 == su2v.ZERO, "dyadic_log2(1) != (0, 0)")
    check_raises_val(lambda: su2v.dyadic_log2_surrogate_q(Fraction(99, 100)), "s < 1", "s must be >= 1")

    m_e, nu_e = su2v.logfree_escape_potential_q(0, su2v.FOUR)
    check(m_e == 1 and nu_e == su2v.ONE, "logfree_escape(0, 4) != (1, 1)")
    check_raises_val(lambda: su2v.logfree_escape_potential_q(-1, su2v.FOUR), "n_esc < 0", "n_esc")
    check_raises_val(lambda: su2v.logfree_escape_potential_q(0, Fraction(39, 10)), "z_norm_sq < 4", "z_norm_sq")

    n_ok, sq_ok = su2v.mandelbrot_escape_exact_q(su2v.TWO, su2v.ZERO, max_iter=1)
    check(n_ok == 1 and sq_ok == su2v.FOUR, "mandelbrot_escape(2, 0, 1) != (1, 4)")
    check_raises_val(lambda: su2v.mandelbrot_escape_exact_q(su2v.TWO, su2v.ZERO, max_iter=0), "esc max_iter=0", "max_iter must be >= 1")
    check_raises_val(lambda: su2v.mandelbrot_escape_exact_q(su2v.ZERO, su2v.ZERO, max_iter=3), "non-escaping c=0", "escape")


def test_certificate_cli_and_tamper_controls() -> None:
    buf_json = io.StringIO()
    with redirect_stdout(buf_json):
        rc = su2v.main(["--json"])
    check(rc == 0, "CLI --json rc != 0")
    cert = json.loads(buf_json.getvalue())
    su2v.validate_certificate(cert)

    buf_check = io.StringIO()
    with redirect_stdout(buf_check):
        rc2 = su2v.main(["--check"])
    check(rc2 == 0 and f"PASS SU2_PROCEDURAL_TRANSPORT result_sha256={cert['result_sha256']}" in buf_check.getvalue(), "CLI --check failed")

    buf_sum = io.StringIO()
    with redirect_stdout(buf_sum):
        rc3 = su2v.main([])
    check(rc3 == 0 and cert["result_sha256"] in buf_sum.getvalue(), "CLI summary failed")

    def tamper_rehash(mutator: Callable[[dict[str, Any]], None], label: str) -> None:
        bad = copy.deepcopy(cert)
        mutator(bad)
        bad["result_sha256"] = su2v.canonical_cert_sha256(bad)
        check_raises_val(lambda: su2v.validate_certificate(bad), label)

    # Forged-hash refusal (without updating hash)
    bad_hash = copy.deepcopy(cert)
    bad_hash["result_sha256"] = "0" * 64
    check_raises_val(lambda: su2v.validate_certificate(bad_hash), "forged result_sha256", "result_sha256")

    # Valid exact boundary certificate killing <= -> < and >= -> > mutants
    ok_edge = copy.deepcopy(cert)
    ok_edge["acute_2i_basin_integer_proof"]["max_procedural_r2"] = "12/25"
    ok_edge["pole_safety"]["min_single_step_denom"] = "1"
    ok_edge["pole_safety"]["min_pair_denom_sq"] = "81/625"
    ok_edge["nonabelian_commutator"]["nonabelian_pairs_count"] = 20
    ok_edge["result_sha256"] = su2v.canonical_cert_sha256(ok_edge)
    su2v.validate_certificate(ok_edge)

    # Atomic tamper controls for every single guard in validate_certificate
    tamper_rehash(lambda d: d.__setitem__("ast_float_and_log_count", 1), "ast_float_and_log_count")
    tamper_rehash(lambda d: d["acute_2i_basin_integer_proof"].__setitem__("lhs_20_times_625", 12769), "basin_int_eq")
    tamper_rehash(lambda d: d["acute_2i_basin_integer_proof"].__setitem__("max_procedural_r2", "13/25"), "max_r2_over")
    tamper_rehash(lambda d: d["acute_2i_basin_integer_proof"].__setitem__("min_scalar_q0", "0"), "min_q0_zero")
    tamper_rehash(lambda d: d["pole_safety"].__setitem__("min_single_step_denom", "99/100"), "min_single_denom")
    tamper_rehash(lambda d: d["pole_safety"].__setitem__("min_pair_denom_sq", "80/625"), "min_pair_denom_sq")
    tamper_rehash(lambda d: d["pole_safety"].__setitem__("boundary_4_5_denom_sq", "80/625"), "boundary_4_5")

    def _ops_7(d: dict[str, Any]) -> None:
        su = d["su2_unitarity_and_isometry"]
        for key in (
            "operators_tested",
            "unitarity_exact_count",
            "unitarity_right_exact_count",
            "det_one_exact_count",
            "spinor_isometry_exact_count",
            "so3_isometry_exact_count",
            "so3_det_one_exact_count",
        ):
            su[key] = 7

    tamper_rehash(_ops_7, "operators_tested")
    tamper_rehash(lambda d: d["su2_unitarity_and_isometry"].__setitem__("unitarity_exact_count", 7), "unitarity_left")
    tamper_rehash(lambda d: d["su2_unitarity_and_isometry"].__setitem__("unitarity_right_exact_count", 7), "unitarity_right")
    tamper_rehash(lambda d: d["su2_unitarity_and_isometry"].__setitem__("det_one_exact_count", 7), "det_one")
    tamper_rehash(lambda d: d["su2_unitarity_and_isometry"].__setitem__("spinor_isometry_exact_count", 7), "spinor_iso")
    tamper_rehash(lambda d: d["su2_unitarity_and_isometry"].__setitem__("so3_isometry_exact_count", 7), "so3_iso")
    tamper_rehash(lambda d: d["su2_unitarity_and_isometry"].__setitem__("so3_det_one_exact_count", 7), "so3_det")

    def _pairs_27(d: dict[str, Any]) -> None:
        nc = d["nonabelian_commutator"]
        nc["pairs_tested"] = 27
        nc["trace_identity_exact_count"] = 27

    tamper_rehash(_pairs_27, "pairs_tested")
    tamper_rehash(lambda d: d["nonabelian_commutator"].__setitem__("nonabelian_pairs_count", 19), "nonabelian_lt_20")
    tamper_rehash(lambda d: d["nonabelian_commutator"].__setitem__("trace_identity_exact_count", 27), "trace_id")
    tamper_rehash(lambda d: d["nonabelian_commutator"].__setitem__("sample_comm_diff_norm2", "0"), "sample_comm_0")

    tamper_rehash(lambda d: d["checkpoint_16b_rollback"].__setitem__("checkpoint_bytes", 15), "ckpt_bytes")
    tamper_rehash(lambda d: d["checkpoint_16b_rollback"].__setitem__("algebraic_rollback_drift", "1/100"), "alg_drift")
    tamper_rehash(lambda d: d["checkpoint_16b_rollback"].__setitem__("pi16_dyadic_roundtrip_drift", "1/100"), "dyadic_drift")
    tamper_rehash(lambda d: d["checkpoint_16b_rollback"].__setitem__("pi16_proc_quant_err2_within_bound", False), "quant_bound")
    tamper_rehash(lambda d: d["checkpoint_16b_rollback"].__setitem__("trial_changed_state", False), "trial_moved")

    def _lem_2(d: dict[str, Any]) -> None:
        lf = d["logfree_escape_kernel"]
        lf["lemniscates_tested"] = 2
        lf["lemniscate_exact_count"] = 2
        lf["seam_zero_jump_count"] = 2

    tamper_rehash(_lem_2, "lemniscates_tested")
    tamper_rehash(lambda d: d["logfree_escape_kernel"].__setitem__("lemniscate_exact_count", 2), "lemniscate_exact")
    tamper_rehash(lambda d: d["logfree_escape_kernel"].__setitem__("seam_zero_jump_count", 2), "seam_zero_jump")
    tamper_rehash(lambda d: d["logfree_escape_kernel"].__setitem__("radius_monotonicity_steps_ok", 4), "radius_mono")
    tamper_rehash(lambda d: d["logfree_escape_kernel"].__setitem__("orbit_monotonicity_steps_ok", 3), "orbit_mono")


def test_combined_receipt_verification() -> None:
    receipt_path = Path(__file__).resolve().parent / "results_su2_transport_and_s73.json"
    if not receipt_path.is_file():
        return
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = runner.main(["--verify-receipts"])
    check(rc == 0 and "PASS RESULTS_SU2_TRANSPORT_AND_S73" in buf.getvalue(), "Combined receipt verification failed")


def main() -> int:
    test_primitives_and_boundaries()
    test_certificate_cli_and_tamper_controls()
    test_combined_receipt_verification()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
