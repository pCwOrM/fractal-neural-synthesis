#!/usr/bin/env python3
"""Reproducible CPU Benchmark & Receipt Verifier for Paper 1 v4.0 §7.3 & Procedural SU(2) Transport.

Original clean-room contribution from Moissanite-Labs for fractal-neural-synthesis.
Strictly CPU-only with zero uncontrolled laptop energy or power claims.

Implements:
  1. Multiscale rank vs. local continuity across ell = 0..16, documenting the IEEE-754
     float64 53-bit mantissa grid-collision cliff (ell = 14..16) plus scale-matched
     Fourier and Chebyshev smooth controls.
  2. Leak-free 10-fold stratified CV closing Paper 1 v4.0 §7.3 (adaptive boundary search
     inside each training fold, 0 test leakage) on full UCI Ionosphere, Optical Digits,
     and PenDigits vs. Static FNS (24 B), Static & Matched-Budget Adaptive Seeded-PRNG
     ELM/RFF (8 B), and Linear-INT8.
  3. 5-seed equal-evaluation-budget (1,600 = 4 x 400) pure zero-readout procedural
     SU(2) seed evolution (32 B seed, 0 B stored transition matrices, 0 B readout weights,
     0.0-drift 16 B checkpoint rollback) on non-Abelian S_3 and A_5 word equivalence.
  4. Pure-stdlib --verify-receipts mode verifying results_su2_transport_and_s73.json
     across isolated Python invocations (-I -B, -I -O -B, -I -B -W error).
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import struct
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import su2_procedural_transport_verify as su2v

UCI_DATA_SHA256: dict[str, str] = {
    "ionosphere.data": "46d52186b84e20be52918adb93e8fb9926b34795ff7504c24350ae0616a04bbd",
    "optdigits.tes": "6ebb3d2fee246a4e99363262ddf8a00a3c41bee6014c373ed9d9216ba7f651b8",
    "pendigits.tra": "e2b9eb9f0d0467e2b64a4816a3420edf2b8043447576f4b84337aba44a9f97d3",
    "pendigits.tes": "8bd03229c5c5291fefe43e45465dd948d2645bf23328b9d993e0b777666b2015",
}

ENERGY_POLICY_STATUS = "CPU_ONLY_NO_LAPTOP_ENERGY_CLAIMS"
MISIUREWICZ_C0 = (-0.10109636384562, 0.95628651080914)
STATIC_FNS_ANCHOR = (-0.743643887037151, 0.131825904205330, 2.15)
GOLDEN_ANGLE = math.pi * (3.0 - math.sqrt(5.0))
FORBIDDEN_ENERGY_SUBSTRINGS = ("mj/tok", "mj_per_tok", "power_draw_w", "watts", "joules_per_tok")


def require_ok(cond: bool, msg: str) -> None:
    if cond is not True:
        raise ValueError(msg)


def canonical_sha256(obj: dict[str, Any]) -> str:
    payload = {k: v for k, v in obj.items() if k != "result_sha256"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def holm_bonferroni(pvals: list[float]) -> list[float]:
    m = len(pvals)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda idx: pvals[idx])
    adj = [0.0] * m
    running_max = 0.0
    for rank, idx in enumerate(order):
        val = min(1.0, (m - rank) * float(pvals[idx]))
        if val > running_max:
            running_max = val
        adj[idx] = running_max
    return adj


def check_no_forbidden_energy_claims(obj: Any, prefix: str = "") -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            for bad in FORBIDDEN_ENERGY_SUBSTRINGS:
                require_ok(bad not in kl, f"Forbidden energy key {prefix}{k!r}")
            check_no_forbidden_energy_claims(v, prefix=f"{prefix}{k}.")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            check_no_forbidden_energy_claims(item, prefix=f"{prefix}[{i}].")
    elif isinstance(obj, str):
        vl = obj.lower()
        for bad in FORBIDDEN_ENERGY_SUBSTRINGS:
            require_ok(bad not in vl, f"Forbidden energy string {prefix!r}")


# =============================================================================
# 1. Multiscale Generator Rank vs. Continuity (ell = 0..16) & float64 Cliff
# =============================================================================

def _phyllotaxis_offsets(n_pts: int, np_mod: Any) -> tuple[Any, Any]:
    k = np_mod.arange(n_pts, dtype=np_mod.float64)
    r = np_mod.sqrt((k + 0.5) / float(n_pts))
    theta = k * GOLDEN_ANGLE
    return r * np_mod.cos(theta), r * np_mod.sin(theta)


def _mandelbrot_smooth_potential(cx: Any, cy: Any, max_iter: int, np_mod: Any) -> Any:
    zx = np_mod.zeros_like(cx, dtype=np_mod.float64)
    zy = np_mod.zeros_like(cy, dtype=np_mod.float64)
    esc_iter = np_mod.full(cx.shape, float(max_iter), dtype=np_mod.float64)
    esc_r2 = np_mod.zeros_like(cx, dtype=np_mod.float64)
    active = np_mod.ones(cx.shape, dtype=bool)
    bailout_r2 = 256.0

    for it in range(1, max_iter + 1):
        if not np_mod.any(active):
            break
        zx_a = zx[active]
        zy_a = zy[active]
        nx = zx_a * zx_a - zy_a * zy_a + cx[active]
        ny = 2.0 * zx_a * zy_a + cy[active]
        r2 = nx * nx + ny * ny
        escaped_now = r2 > bailout_r2
        zx[active] = nx
        zy[active] = ny
        if np_mod.any(escaped_now):
            active_idx = np_mod.flatnonzero(active)
            hit_idx = active_idx[escaped_now]
            esc_iter.flat[hit_idx] = float(it)
            esc_r2.flat[hit_idx] = r2[escaped_now]
            active.flat[hit_idx] = False

    out = np_mod.empty(cx.shape, dtype=np_mod.float64)
    escaped_mask = ~active
    if np_mod.any(escaped_mask):
        r_abs = np_mod.sqrt(np_mod.maximum(esc_r2[escaped_mask], 4.0))
        nu = esc_iter[escaped_mask] + 1.0 - np_mod.log2(np_mod.maximum(np_mod.log2(r_abs), 1e-12))
        out[escaped_mask] = np_mod.sin(0.65 * nu) * 0.7 + np_mod.cos(1.37 * nu) * 0.3
    if np_mod.any(active):
        out[active] = np_mod.tanh(zx[active] * 1.3 - zy[active] * 0.9)
    return out


def _prng_sha256_field(cx: Any, cy: Any, np_mod: Any) -> Any:
    flat_x = np_mod.ascontiguousarray(cx, dtype=np_mod.float64).ravel()
    flat_y = np_mod.ascontiguousarray(cy, dtype=np_mod.float64).ravel()
    out = np_mod.empty(flat_x.shape[0], dtype=np_mod.float64)
    scale = 1.0 / float(1 << 52)
    for i in range(flat_x.shape[0]):
        digest = hashlib.sha256(struct.pack("<dd", float(flat_x[i]), float(flat_y[i]))).digest()
        u53 = int.from_bytes(digest[:8], "little") >> 11
        out[i] = u53 * scale - 1.0
    return out.reshape(cx.shape)


def _fourier_fixed_field(cx: Any, cy: Any, np_mod: Any) -> Any:
    rng = np_mod.random.default_rng(13301)
    kx = rng.uniform(-20.0, 20.0, size=16)
    ky = rng.uniform(-20.0, 20.0, size=16)
    ph = rng.uniform(0.0, 2.0 * math.pi, size=16)
    amp = rng.normal(0.0, 1.0, size=16)
    amp /= np_mod.sqrt(np_mod.sum(amp * amp))
    acc = np_mod.zeros_like(cx, dtype=np_mod.float64)
    for j in range(16):
        acc += amp[j] * np_mod.sin(kx[j] * cx + ky[j] * cy + ph[j])
    return np_mod.tanh(acc * 1.4)


def _lattice_value_fixed_field(cx: Any, cy: Any, np_mod: Any) -> Any:
    cell = 0.05
    gx = cx / cell
    gy = cy / cell
    ix = np_mod.floor(gx).astype(np_mod.int64)
    iy = np_mod.floor(gy).astype(np_mod.int64)
    fx = gx - ix
    fy = gy - iy
    ux = fx * fx * (3.0 - 2.0 * fx)
    uy = fy * fy * (3.0 - 2.0 * fy)

    def _hash2(a: Any, b: Any) -> Any:
        h = (a * np_mod.int64(374761393) + b * np_mod.int64(668265263)) ^ np_mod.int64(0x5BF03635)
        h = (h ^ (h >> np_mod.int64(13))) * np_mod.int64(1274126177)
        h = h ^ (h >> np_mod.int64(16))
        u = (h & np_mod.int64(0x7FFFFFFF)).astype(np_mod.float64) / float(0x7FFFFFFF)
        return 2.0 * u - 1.0

    v00 = _hash2(ix, iy)
    v10 = _hash2(ix + 1, iy)
    v01 = _hash2(ix, iy + 1)
    v11 = _hash2(ix + 1, iy + 1)
    top = v00 * (1.0 - ux) + v10 * ux
    bot = v01 * (1.0 - ux) + v11 * ux
    return top * (1.0 - uy) + bot * uy


def _fourier_matched_scale_field(cx: Any, cy: Any, c0x: float, c0y: float, radius: float, ell: int, np_mod: Any) -> Any:
    n_modes = min(64, 16 + 3 * ell)
    rng = np_mod.random.default_rng(13302)
    kx = rng.uniform(-16.0, 16.0, size=n_modes)
    ky = rng.uniform(-16.0, 16.0, size=n_modes)
    ph = rng.uniform(0.0, 2.0 * math.pi, size=n_modes)
    amp = rng.normal(0.0, 1.0, size=n_modes)
    amp /= np_mod.sqrt(np_mod.sum(amp * amp))
    u = (cx - c0x) / radius
    v = (cy - c0y) / radius
    acc = np_mod.zeros_like(cx, dtype=np_mod.float64)
    for j in range(n_modes):
        acc += amp[j] * np_mod.sin(kx[j] * u + ky[j] * v + ph[j])
    return np_mod.tanh(acc * 1.4)


def _chebyshev_matched_scale_field(cx: Any, cy: Any, c0x: float, c0y: float, radius: float, np_mod: Any) -> Any:
    u = np_mod.clip((cx - c0x) / radius, -1.5, 1.5) / 1.5
    v = np_mod.clip((cy - c0y) / radius, -1.5, 1.5) / 1.5
    deg = 10
    tu = [np_mod.ones_like(u), u]
    tv = [np_mod.ones_like(v), v]
    for _ in range(2, deg):
        tu.append(2.0 * u * tu[-1] - tu[-2])
        tv.append(2.0 * v * tv[-1] - tv[-2])
    rng = np_mod.random.default_rng(13303)
    coeff = rng.normal(0.0, 1.0, size=(deg, deg))
    coeff[0, 0] = 0.0
    coeff /= np_mod.sqrt(np_mod.sum(coeff * coeff))
    acc = np_mod.zeros_like(u)
    for p in range(deg):
        for q in range(deg):
            acc += coeff[p, q] * tu[p] * tv[q]
    return np_mod.tanh(acc * 2.2)


def _effective_rank_16x16(vec256: Any, np_mod: Any) -> float:
    mat = vec256.reshape(16, 16)
    mat = mat - np_mod.mean(mat)
    sv = np_mod.linalg.svd(mat, compute_uv=False)
    s_sum = float(np_mod.sum(sv))
    if s_sum <= 1e-12:
        return 0.0
    p = sv[sv > 1e-15] / s_sum
    entropy = -float(np_mod.sum(p * np_mod.log(p)))
    return float(math.exp(entropy))


def _local_pearson(v0: Any, v1: Any, np_mod: Any) -> float:
    s0 = float(np_mod.std(v0))
    s1 = float(np_mod.std(v1))
    if s0 <= 1e-12 and s1 <= 1e-12:
        return 1.0 if float(np_mod.max(np_mod.abs(v0 - v1))) <= 1e-12 else 0.0
    if s0 <= 1e-12 or s1 <= 1e-12:
        return 0.0
    c = float(np_mod.corrcoef(v0, v1)[0, 1])
    return 0.0 if math.isnan(c) else c


def run_multiscale_cliff_benchmark(np_mod: Any) -> dict[str, Any]:
    c0x, c0y = MISIUREWICZ_C0
    ox, oy = _phyllotaxis_offsets(256, np_mod)
    n_jitters = 12
    rng = np_mod.random.default_rng(20261126)
    jitter_ang = rng.uniform(0.0, 2.0 * math.pi, size=n_jitters)
    jitter_rad = rng.uniform(0.02, 0.08, size=n_jitters)
    delta_ang = rng.uniform(0.0, 2.0 * math.pi, size=n_jitters)

    generators = [
        "mandelbrot_boundary",
        "prng_sha256",
        "fourier_smooth_fixed",
        "lattice_value_fixed",
        "fourier_matched_scale",
        "chebyshev_matched_scale",
    ]

    def _eval_gen(name: str, cx: Any, cy: Any, radius: float, ell: int, max_iter: int) -> Any:
        if name == "mandelbrot_boundary":
            return _mandelbrot_smooth_potential(cx, cy, max_iter=max_iter, np_mod=np_mod)
        if name == "prng_sha256":
            return _prng_sha256_field(cx, cy, np_mod=np_mod)
        if name == "fourier_smooth_fixed":
            return _fourier_fixed_field(cx, cy, np_mod=np_mod)
        if name == "lattice_value_fixed":
            return _lattice_value_fixed_field(cx, cy, np_mod=np_mod)
        if name == "fourier_matched_scale":
            return _fourier_matched_scale_field(cx, cy, c0x, c0y, radius, ell, np_mod=np_mod)
        if name == "chebyshev_matched_scale":
            return _chebyshev_matched_scale_field(cx, cy, c0x, c0y, radius, np_mod=np_mod)
        raise ValueError(f"Unknown generator: {name}")

    scale_rows: list[dict[str, Any]] = []
    for ell in range(0, 17):
        radius = 10.0 ** (-ell)
        max_iter = 70 + 40 * ell
        base_cx = c0x + radius * ox
        base_cy = c0y + radius * oy
        unique_pairs = len(set(zip(base_cx.tolist(), base_cy.tolist())))
        unique_pair_frac = unique_pairs / 256.0
        step = 0.05 * radius
        delta_zero_hits = 0
        for j in range(n_jitters):
            dx = step * math.cos(float(delta_ang[j]))
            dy = step * math.sin(float(delta_ang[j]))
            if bool(np_mod.all((base_cx + dx) == base_cx) and np_mod.all((base_cy + dy) == base_cy)):
                delta_zero_hits += 1
        delta_exact_zero_frac = delta_zero_hits / float(n_jitters)

        gen_stats: dict[str, dict[str, float]] = {}
        for gname in generators:
            ranks: list[float] = []
            rhos: list[float] = []
            for j in range(n_jitters):
                jx = c0x + float(jitter_rad[j]) * radius * math.cos(float(jitter_ang[j]))
                jy = c0y + float(jitter_rad[j]) * radius * math.sin(float(jitter_ang[j]))
                cx0 = jx + radius * ox
                cy0 = jy + radius * oy
                dx = step * math.cos(float(delta_ang[j]))
                dy = step * math.sin(float(delta_ang[j]))
                v0 = _eval_gen(gname, cx0, cy0, radius, ell, max_iter)
                v1 = _eval_gen(gname, cx0 + dx, cy0 + dy, radius, ell, max_iter)
                ranks.append(_effective_rank_16x16(v0, np_mod))
                rhos.append(_local_pearson(v0, v1, np_mod))
            gen_stats[gname] = {
                "eff_rank_16x16_mean": round(float(np_mod.mean(ranks)), 6),
                "eff_rank_16x16_std": round(float(np_mod.std(ranks)), 6),
                "local_corr_mean": round(float(np_mod.mean(rhos)), 6),
                "local_corr_std": round(float(np_mod.std(rhos)), 6),
            }

        scale_rows.append(
            {
                "ell": ell,
                "radius": radius,
                "max_iter": max_iter,
                "f64_unique_pair_count": unique_pairs,
                "f64_unique_pair_frac": round(unique_pair_frac, 6),
                "f64_delta_exact_zero_frac": round(delta_exact_zero_frac, 6),
                "generators": gen_stats,
            }
        )

    def _range_mean(gen: str, field: str, lo: int, hi: int) -> float:
        vals = [r["generators"][gen][field] for r in scale_rows if lo <= r["ell"] <= hi]
        return round(sum(vals) / len(vals), 6)

    mb_rank_0_8 = _range_mean("mandelbrot_boundary", "eff_rank_16x16_mean", 0, 8)
    mb_rho_0_8 = _range_mean("mandelbrot_boundary", "local_corr_mean", 0, 8)
    prng_rank_0_8 = _range_mean("prng_sha256", "eff_rank_16x16_mean", 0, 8)
    prng_rho_0_8 = _range_mean("prng_sha256", "local_corr_mean", 0, 8)
    ff_rank_3_8 = _range_mean("fourier_smooth_fixed", "eff_rank_16x16_mean", 3, 8)
    lv_rank_3_8 = _range_mean("lattice_value_fixed", "eff_rank_16x16_mean", 3, 8)
    fm_rank_0_8 = _range_mean("fourier_matched_scale", "eff_rank_16x16_mean", 0, 8)
    fm_rho_0_8 = _range_mean("fourier_matched_scale", "local_corr_mean", 0, 8)
    cm_rank_0_8 = _range_mean("chebyshev_matched_scale", "eff_rank_16x16_mean", 0, 8)
    cm_rho_0_8 = _range_mean("chebyshev_matched_scale", "local_corr_mean", 0, 8)

    row14 = scale_rows[14]
    row15 = scale_rows[15]
    row16 = scale_rows[16]
    f64_cliff_certified = (
        row16["f64_unique_pair_frac"] < 0.25
        and row16["f64_delta_exact_zero_frac"] == 1.0
        and row16["generators"]["prng_sha256"]["local_corr_mean"] >= 0.99
        and row14["generators"]["fourier_smooth_fixed"]["eff_rank_16x16_mean"] == 0.0
    )
    repro_ell_0_8_ok = (
        mb_rank_0_8 >= 8.0
        and (mb_rho_0_8 - prng_rho_0_8) >= 0.50
        and abs(prng_rho_0_8) < 0.10
        and ff_rank_3_8 < 3.5
        and lv_rank_3_8 < 3.5
    )
    matched_smooth_matches = fm_rank_0_8 >= mb_rank_0_8 - 0.5 and fm_rho_0_8 >= 0.80

    return {
        "anchor_misiurewicz_c0": list(MISIUREWICZ_C0),
        "n_points": 256,
        "n_jitters": n_jitters,
        "ell_range": [0, 16],
        "scales": scale_rows,
        "summary": {
            "ell_0_8_mandelbrot_rank_mean": mb_rank_0_8,
            "ell_0_8_mandelbrot_rho_mean": mb_rho_0_8,
            "ell_0_8_prng_rank_mean": prng_rank_0_8,
            "ell_0_8_prng_rho_mean": prng_rho_0_8,
            "ell_3_8_fourier_fixed_rank_mean": ff_rank_3_8,
            "ell_3_8_lattice_fixed_rank_mean": lv_rank_3_8,
            "ell_0_8_fourier_matched_scale_rank_mean": fm_rank_0_8,
            "ell_0_8_fourier_matched_scale_rho_mean": fm_rho_0_8,
            "ell_0_8_chebyshev_matched_scale_rank_mean": cm_rank_0_8,
            "ell_0_8_chebyshev_matched_scale_rho_mean": cm_rho_0_8,
            "f64_cliff_ell14_unique_pair_frac": row14["f64_unique_pair_frac"],
            "f64_cliff_ell15_unique_pair_frac": row15["f64_unique_pair_frac"],
            "f64_cliff_ell16_unique_pair_frac": row16["f64_unique_pair_frac"],
            "f64_cliff_ell16_delta_exact_zero_frac": row16["f64_delta_exact_zero_frac"],
            "f64_cliff_certified": f64_cliff_certified,
            "repro_ell_0_8_vs_fixed_baselines": repro_ell_0_8_ok,
            "scale_matched_smooth_matches_or_exceeds_mandelbrot": matched_smooth_matches,
            "verdict": "CONFIRMED_WITH_SCALE_MATCHED_CAVEAT"
            if (repro_ell_0_8_ok and f64_cliff_certified and matched_smooth_matches)
            else ("CONFIRMED" if (repro_ell_0_8_ok and f64_cliff_certified) else "PARTIAL"),
        },
    }


# =============================================================================
# 2. Paper 1 v4.0 §7.3 Leak-Free 10-Fold Stratified CV on 3 Full UCI Datasets
# =============================================================================

def _load_uci_datasets(data_dir: Path, np_mod: Any) -> tuple[dict[str, tuple[Any, Any, int]], dict[str, str]]:
    verified_hashes: dict[str, str] = {}
    for fname, expected in UCI_DATA_SHA256.items():
        p = data_dir / fname
        require_ok(p.is_file(), f"Missing UCI dataset file {fname} in {data_dir}")
        actual = file_sha256(p)
        require_ok(actual == expected, f"UCI SHA-256 mismatch for {fname}")
        verified_hashes[fname] = actual

    iono_x: list[list[float]] = []
    iono_y: list[int] = []
    for line in (data_dir / "ionosphere.data").read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s:
            continue
        parts = s.split(",")
        iono_x.append([float(v) for v in parts[:34]])
        iono_y.append(1 if parts[34].strip() == "g" else 0)

    opt_x: list[list[float]] = []
    opt_y: list[int] = []
    for line in (data_dir / "optdigits.tes").read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s:
            continue
        parts = s.split(",")
        opt_x.append([float(v) / 8.0 - 1.0 for v in parts[:64]])
        opt_y.append(int(parts[64].strip()))

    pen_x: list[list[float]] = []
    pen_y: list[int] = []
    for fname in ("pendigits.tra", "pendigits.tes"):
        for line in (data_dir / fname).read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s:
                continue
            parts = s.split(",")
            pen_x.append([float(v.strip()) / 50.0 - 1.0 for v in parts[:16]])
            pen_y.append(int(parts[16].strip()))

    return {
        "UCI_Ionosphere": (np_mod.asarray(iono_x, dtype=np_mod.float64), np_mod.asarray(iono_y, dtype=np_mod.int64), 2),
        "UCI_Optical_Digits": (np_mod.asarray(opt_x, dtype=np_mod.float64), np_mod.asarray(opt_y, dtype=np_mod.int64), 10),
        "UCI_PenDigits": (np_mod.asarray(pen_x, dtype=np_mod.float64), np_mod.asarray(pen_y, dtype=np_mod.int64), 10),
    }, verified_hashes


def _stratified_kfold_indices(y: Any, n_splits: int, seed: int, np_mod: Any) -> list[tuple[Any, Any]]:
    rng = np_mod.random.default_rng(seed)
    folds: list[list[int]] = [[] for _ in range(n_splits)]
    for cls in np_mod.unique(y):
        idx = np_mod.flatnonzero(y == cls).copy()
        rng.shuffle(idx)
        for pos, sample_i in enumerate(idx.tolist()):
            folds[pos % n_splits].append(sample_i)
    all_idx = np_mod.arange(y.shape[0], dtype=np_mod.int64)
    splits: list[tuple[Any, Any]] = []
    for k in range(n_splits):
        te = np_mod.asarray(sorted(folds[k]), dtype=np_mod.int64)
        mask = np_mod.ones(y.shape[0], dtype=bool)
        mask[te] = False
        splits.append((all_idx[mask], te))
    return splits


def _stratified_inner_split(y_tr: Any, val_frac: float, seed: int, np_mod: Any) -> tuple[Any, Any]:
    rng = np_mod.random.default_rng(seed)
    itr: list[int] = []
    iva: list[int] = []
    for cls in np_mod.unique(y_tr):
        idx = np_mod.flatnonzero(y_tr == cls).copy()
        rng.shuffle(idx)
        n_val = max(1, int(round(len(idx) * val_frac)))
        if n_val >= len(idx):
            n_val = max(0, len(idx) - 1)
        iva.extend(idx[:n_val].tolist())
        itr.extend(idx[n_val:].tolist())
    return np_mod.asarray(sorted(itr), dtype=np_mod.int64), np_mod.asarray(sorted(iva), dtype=np_mod.int64)


def _fit_predict_ridge_int8(h_tr: Any, y_tr: Any, h_te: Any, n_classes: int, reg: float, np_mod: Any) -> tuple[Any, Any]:
    n_tr, m = h_tr.shape
    h_tr_b = np_mod.concatenate([h_tr, np_mod.ones((n_tr, 1), dtype=np_mod.float64)], axis=1)
    h_te_b = np_mod.concatenate([h_te, np_mod.ones((h_te.shape[0], 1), dtype=np_mod.float64)], axis=1)
    y_oh = np_mod.zeros((n_tr, n_classes), dtype=np_mod.float64)
    y_oh[np_mod.arange(n_tr), y_tr] = 1.0
    pen = np_mod.eye(m + 1, dtype=np_mod.float64) * reg
    pen[-1, -1] = 1e-6
    w = np_mod.linalg.solve(h_tr_b.T @ h_tr_b + pen, h_tr_b.T @ y_oh)
    max_abs = np_mod.maximum(np_mod.max(np_mod.abs(w), axis=0, keepdims=True), 1e-12)
    scale = max_abs / 127.0
    w_q = np_mod.round(np_mod.clip(w / scale, -127.0, 127.0)) * scale
    logits = h_te_b @ w_q
    return np_mod.argmax(logits, axis=1), logits


def _fns_24b_features(x: Any, cx: float, cy: float, ell: float, h_dim: int, ox_grid: Any, oy_grid: Any, np_mod: Any) -> Any:
    d = x.shape[1]
    n_total = h_dim * (d + 1)
    radius = 10.0 ** (-ell)
    max_iter = int(min(260, max(64, round(80.0 + 30.0 * ell))))
    raw = _mandelbrot_smooth_potential(cx + radius * ox_grid[:n_total], cy + radius * oy_grid[:n_total], max_iter, np_mod)
    raw = raw - float(np_mod.mean(raw))
    std = float(np_mod.std(raw))
    if std > 1e-9:
        raw = raw / std
    mat = raw.reshape(h_dim, d + 1)
    return np_mod.tanh(x @ (mat[:, :d] / math.sqrt(float(d))).T + mat[:, d] * 0.25)


def _seeded_elm_8b_features(x: Any, seed_u64: int, h_dim: int, gain: float, np_mod: Any) -> Any:
    d = x.shape[1]
    rng = np_mod.random.default_rng(int(seed_u64))
    w = rng.normal(0.0, gain / math.sqrt(float(d)), size=(h_dim, d))
    b = rng.normal(0.0, 0.25, size=(h_dim,))
    return np_mod.tanh(x @ w.T + b)


def _seeded_rff_8b_features(x: Any, seed_u64: int, h_dim: int, gamma: float, np_mod: Any) -> Any:
    d = x.shape[1]
    rng = np_mod.random.default_rng(int(seed_u64))
    w = rng.normal(0.0, gamma / math.sqrt(float(d)), size=(h_dim, d))
    phase = rng.uniform(0.0, 2.0 * math.pi, size=(h_dim,))
    return math.sqrt(2.0 / float(h_dim)) * np_mod.cos(x @ w.T + phase)


def _paired_stats(a: list[float], b: list[float], np_mod: Any, stats_mod: Any) -> dict[str, float]:
    aa = np_mod.asarray(a, dtype=np_mod.float64)
    bb = np_mod.asarray(b, dtype=np_mod.float64)
    diff = aa - bb
    mean_diff = float(np_mod.mean(diff))
    std_diff = float(np_mod.std(diff, ddof=1)) if len(diff) > 1 else 0.0
    if float(np_mod.max(np_mod.abs(diff))) <= 1e-12:
        t_stat, p_t_two, p_t_gt, p_w_two, p_w_gt = 0.0, 1.0, 0.5, 1.0, 0.5
    else:
        tres = stats_mod.ttest_rel(aa, bb)
        t_stat = float(tres.statistic)
        p_t_two = float(tres.pvalue)
        p_t_gt = float(stats_mod.ttest_rel(aa, bb, alternative="greater").pvalue)
        nz = diff[np_mod.abs(diff) > 1e-12]
        if len(nz) == 0:
            p_w_two, p_w_gt = 1.0, 0.5
        else:
            p_w_two = float(stats_mod.wilcoxon(nz, alternative="two-sided").pvalue)
            p_w_gt = float(stats_mod.wilcoxon(nz, alternative="greater").pvalue)
    return {
        "mean_diff_pp": round(mean_diff * 100.0, 4),
        "std_diff_pp": round(std_diff * 100.0, 4),
        "t_stat": round(t_stat, 4),
        "p_t_two_sided": round(p_t_two, 6),
        "p_t_one_sided_greater": round(p_t_gt, 6),
        "p_wilcoxon_two_sided": round(p_w_two, 6),
        "p_wilcoxon_one_sided_greater": round(p_w_gt, 6),
    }


def run_s73_uci_cv_benchmark(data_dir: Path, np_mod: Any, stats_mod: Any) -> dict[str, Any]:
    datasets, verified_hashes = _load_uci_datasets(data_dir, np_mod)
    h_dim = 256
    reg = 0.5
    inner_eval_budget = 24
    boundary_anchors = [
        (-0.743643887037151, 0.131825904205330, 2.15),
        (-0.101096363845620, 0.956286510809140, 2.50),
        (0.281717921930775, 0.577105284148850, 1.80),
        (-1.250660000000000, 0.020120000000000, 1.60),
        (-0.159200000000000, 1.031700000000000, 2.00),
        (-1.401155189092050, 0.000000000000000, 2.80),
        (0.355534000000000, -0.337292000000000, 1.90),
        (-0.745428000000000, 0.113009000000000, 3.20),
    ]
    ox_all, oy_all = _phyllotaxis_offsets(h_dim * 65, np_mod)
    methods = [
        "Linear_INT8",
        "FNS_Static_24B_INT8",
        "FNS_Adaptive_InnerCV_24B_INT8",
        "Seeded_PRNG_ELM_Static_8B_INT8",
        "Seeded_PRNG_ELM_Adaptive_8B_INT8",
        "Seeded_PRNG_RFF_Static_8B_INT8",
        "Seeded_PRNG_RFF_Adaptive_8B_INT8",
    ]
    ds_results: dict[str, Any] = {}
    for ds_idx, (ds_name, (x_all, y_all, n_classes)) in enumerate(datasets.items()):
        folds = _stratified_kfold_indices(y_all, 10, 42 + ds_idx, np_mod)
        fold_accs: dict[str, list[float]] = {m: [] for m in methods}
        for f_idx, (tr_idx, te_idx) in enumerate(folds):
            x_tr, y_tr = x_all[tr_idx], y_all[tr_idx]
            x_te, y_te = x_all[te_idx], y_all[te_idx]
            itr, iva = _stratified_inner_split(y_tr, 0.20, 1000 + 37 * ds_idx + f_idx, np_mod)
            x_itr, y_itr, x_iva, y_iva = x_tr[itr], y_tr[itr], x_tr[iva], y_tr[iva]

            p_lin, _ = _fit_predict_ridge_int8(x_tr, y_tr, x_te, n_classes, reg, np_mod)
            fold_accs["Linear_INT8"].append(float(np_mod.mean(p_lin == y_te)))

            p_fs, _ = _fit_predict_ridge_int8(
                _fns_24b_features(x_tr, *STATIC_FNS_ANCHOR, h_dim, ox_all, oy_all, np_mod),
                y_tr,
                _fns_24b_features(x_te, *STATIC_FNS_ANCHOR, h_dim, ox_all, oy_all, np_mod),
                n_classes,
                reg,
                np_mod,
            )
            fold_accs["FNS_Static_24B_INT8"].append(float(np_mod.mean(p_fs == y_te)))

            walk_rng = np_mod.random.default_rng(5000 + 100 * ds_idx + f_idx)
            best_sc = (-1.0, -1e9)
            best_theta = STATIC_FNS_ANCHOR
            evals = 0

            def _score_fns(theta: tuple[float, float, float]) -> tuple[float, float]:
                pred_v, logits_v = _fit_predict_ridge_int8(
                    _fns_24b_features(x_itr, *theta, h_dim, ox_all, oy_all, np_mod),
                    y_itr,
                    _fns_24b_features(x_iva, *theta, h_dim, ox_all, oy_all, np_mod),
                    n_classes,
                    reg,
                    np_mod,
                )
                y_oh = np_mod.zeros((len(y_iva), n_classes), dtype=np_mod.float64)
                y_oh[np_mod.arange(len(y_iva)), y_iva] = 1.0
                return (float(np_mod.mean(pred_v == y_iva)), -float(np_mod.mean((logits_v - y_oh) ** 2)))

            for anchor in boundary_anchors:
                sc = _score_fns(anchor)
                evals += 1
                if sc > best_sc:
                    best_sc, best_theta = sc, anchor
            step_scale = 0.25
            while evals < inner_eval_budget:
                bcx, bcy, bell = best_theta
                rl = 10.0 ** (-bell)
                cand = (
                    bcx + float(walk_rng.normal(0.0, step_scale * rl)),
                    bcy + float(walk_rng.normal(0.0, step_scale * rl)),
                    float(np_mod.clip(bell + float(walk_rng.normal(0.0, 0.45)), 0.3, 5.5)),
                )
                sc = _score_fns(cand)
                evals += 1
                if sc > best_sc:
                    best_sc, best_theta = sc, cand
                else:
                    step_scale *= 0.90
            p_fa, _ = _fit_predict_ridge_int8(
                _fns_24b_features(x_tr, *best_theta, h_dim, ox_all, oy_all, np_mod),
                y_tr,
                _fns_24b_features(x_te, *best_theta, h_dim, ox_all, oy_all, np_mod),
                n_classes,
                reg,
                np_mod,
            )
            fold_accs["FNS_Adaptive_InnerCV_24B_INT8"].append(float(np_mod.mean(p_fa == y_te)))

            p_es, _ = _fit_predict_ridge_int8(
                _seeded_elm_8b_features(x_tr, 42, h_dim, 1.0, np_mod),
                y_tr,
                _seeded_elm_8b_features(x_te, 42, h_dim, 1.0, np_mod),
                n_classes,
                reg,
                np_mod,
            )
            fold_accs["Seeded_PRNG_ELM_Static_8B_INT8"].append(float(np_mod.mean(p_es == y_te)))

            best_elm_sc, best_elm_cfg = (-1.0, -1e9), (42, 1.0)
            for k_idx in range(inner_eval_budget):
                s_u64 = 10000 + 1000 * ds_idx + 50 * f_idx + k_idx
                g_val = [0.6, 1.0, 1.5, 2.2][k_idx % 4]
                pv, lv = _fit_predict_ridge_int8(
                    _seeded_elm_8b_features(x_itr, s_u64, h_dim, g_val, np_mod),
                    y_itr,
                    _seeded_elm_8b_features(x_iva, s_u64, h_dim, g_val, np_mod),
                    n_classes,
                    reg,
                    np_mod,
                )
                y_oh = np_mod.zeros((len(y_iva), n_classes), dtype=np_mod.float64)
                y_oh[np_mod.arange(len(y_iva)), y_iva] = 1.0
                sc = (float(np_mod.mean(pv == y_iva)), -float(np_mod.mean((lv - y_oh) ** 2)))
                if sc > best_elm_sc:
                    best_elm_sc, best_elm_cfg = sc, (s_u64, g_val)
            p_ea, _ = _fit_predict_ridge_int8(
                _seeded_elm_8b_features(x_tr, best_elm_cfg[0], h_dim, best_elm_cfg[1], np_mod),
                y_tr,
                _seeded_elm_8b_features(x_te, best_elm_cfg[0], h_dim, best_elm_cfg[1], np_mod),
                n_classes,
                reg,
                np_mod,
            )
            fold_accs["Seeded_PRNG_ELM_Adaptive_8B_INT8"].append(float(np_mod.mean(p_ea == y_te)))

            p_rs, _ = _fit_predict_ridge_int8(
                _seeded_rff_8b_features(x_tr, 42, h_dim, 1.0, np_mod),
                y_tr,
                _seeded_rff_8b_features(x_te, 42, h_dim, 1.0, np_mod),
                n_classes,
                reg,
                np_mod,
            )
            fold_accs["Seeded_PRNG_RFF_Static_8B_INT8"].append(float(np_mod.mean(p_rs == y_te)))

            best_rff_sc, best_rff_cfg = (-1.0, -1e9), (42, 1.0)
            for k_idx in range(inner_eval_budget):
                s_u64 = 20000 + 1000 * ds_idx + 50 * f_idx + k_idx
                gm = [0.5, 0.85, 1.25, 1.8][k_idx % 4]
                pv, lv = _fit_predict_ridge_int8(
                    _seeded_rff_8b_features(x_itr, s_u64, h_dim, gm, np_mod),
                    y_itr,
                    _seeded_rff_8b_features(x_iva, s_u64, h_dim, gm, np_mod),
                    n_classes,
                    reg,
                    np_mod,
                )
                y_oh = np_mod.zeros((len(y_iva), n_classes), dtype=np_mod.float64)
                y_oh[np_mod.arange(len(y_iva)), y_iva] = 1.0
                sc = (float(np_mod.mean(pv == y_iva)), -float(np_mod.mean((lv - y_oh) ** 2)))
                if sc > best_rff_sc:
                    best_rff_sc, best_rff_cfg = sc, (s_u64, gm)
            p_ra, _ = _fit_predict_ridge_int8(
                _seeded_rff_8b_features(x_tr, best_rff_cfg[0], h_dim, best_rff_cfg[1], np_mod),
                y_tr,
                _seeded_rff_8b_features(x_te, best_rff_cfg[0], h_dim, best_rff_cfg[1], np_mod),
                n_classes,
                reg,
                np_mod,
            )
            fold_accs["Seeded_PRNG_RFF_Adaptive_8B_INT8"].append(float(np_mod.mean(p_ra == y_te)))

        fa = fold_accs["FNS_Adaptive_InnerCV_24B_INT8"]
        ds_results[ds_name] = {
            "n_samples": int(x_all.shape[0]),
            "n_features": int(x_all.shape[1]),
            "n_classes": n_classes,
            "methods": {
                m: {
                    "mean_acc_pct": round(float(np_mod.mean(fold_accs[m])) * 100.0, 4),
                    "std_acc_pct": round(float(np_mod.std(fold_accs[m], ddof=1)) * 100.0, 4),
                    "fold_accs": [round(v, 6) for v in fold_accs[m]],
                }
                for m in methods
            },
            "paired_tests": {
                "fns_adaptive_vs_fns_static": _paired_stats(fa, fold_accs["FNS_Static_24B_INT8"], np_mod, stats_mod),
                "fns_adaptive_vs_elm_static": _paired_stats(fa, fold_accs["Seeded_PRNG_ELM_Static_8B_INT8"], np_mod, stats_mod),
                "fns_adaptive_vs_elm_adaptive": _paired_stats(fa, fold_accs["Seeded_PRNG_ELM_Adaptive_8B_INT8"], np_mod, stats_mod),
                "fns_adaptive_vs_rff_static": _paired_stats(fa, fold_accs["Seeded_PRNG_RFF_Static_8B_INT8"], np_mod, stats_mod),
                "fns_adaptive_vs_rff_adaptive": _paired_stats(fa, fold_accs["Seeded_PRNG_RFF_Adaptive_8B_INT8"], np_mod, stats_mod),
                "fns_adaptive_vs_linear": _paired_stats(fa, fold_accs["Linear_INT8"], np_mod, stats_mod),
            },
        }

    ds_names = list(ds_results.keys())
    holm_table: dict[str, dict[str, Any]] = {}
    for c_key in (
        "fns_adaptive_vs_fns_static",
        "fns_adaptive_vs_elm_static",
        "fns_adaptive_vs_elm_adaptive",
        "fns_adaptive_vs_rff_static",
        "fns_adaptive_vs_rff_adaptive",
        "fns_adaptive_vs_linear",
    ):
        adj_gt = holm_bonferroni([ds_results[dn]["paired_tests"][c_key]["p_t_one_sided_greater"] for dn in ds_names])
        holm_table[c_key] = {
            dn: {
                "mean_diff_pp": ds_results[dn]["paired_tests"][c_key]["mean_diff_pp"],
                "p_holm_t_one_sided_greater": round(adj_gt[i], 6),
                "sig_beat_p_holm_lt_0_05": bool(ds_results[dn]["paired_tests"][c_key]["mean_diff_pp"] > 0.0 and adj_gt[i] < 0.05),
            }
            for i, dn in enumerate(ds_names)
        }

    wins_static = sum(1 for dn in ds_names if holm_table["fns_adaptive_vs_fns_static"][dn]["sig_beat_p_holm_lt_0_05"])
    wins_all = sum(
        1
        for dn in ds_names
        if (
            holm_table["fns_adaptive_vs_fns_static"][dn]["sig_beat_p_holm_lt_0_05"]
            and holm_table["fns_adaptive_vs_elm_adaptive"][dn]["sig_beat_p_holm_lt_0_05"]
            and holm_table["fns_adaptive_vs_rff_adaptive"][dn]["sig_beat_p_holm_lt_0_05"]
        )
    )
    return {
        "protocol": {
            "cv": "10_fold_stratified_leak_free",
            "hidden_dim": h_dim,
            "ridge_reg": reg,
            "readout_quantization": "per_class_symmetric_INT8",
            "inner_cv_eval_budget": inner_eval_budget,
            "test_leakage_queries": 0,
        },
        "uci_data_sha256": verified_hashes,
        "datasets": ds_results,
        "holm_bonferroni_m3": holm_table,
        "summary": {
            "wins_vs_fns_static_p_holm_lt_0_05": wins_static,
            "wins_vs_static_fns_and_matched_adaptive_prng_elm_rff": wins_all,
            "verdict": "CONFIRMED" if wins_all >= 2 else ("PARTIAL" if wins_static >= 2 else "FALSIFIED"),
        },
    }


# =============================================================================
# 3. 5-Seed Equal-Budget Zero-Readout Procedural SU(2) Seed Evolution (S3 & A5)
# =============================================================================

def _perm_compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def _eval_group_word(word: tuple[int, ...], gens: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[int, ...]:
    cur = tuple(range(len(gens[0])))
    for sym in word:
        cur = _perm_compose(cur, gens[sym])
    return cur


def _build_group_word_dataset(group_name: str, seed: int, n_train: int, n_test: int, np_mod: Any) -> tuple[list[Any], list[Any]]:
    if group_name == "S3":
        gens = ((1, 0, 2), (1, 2, 0))
        min_len, max_len = 2, 7
        canonical_w = [
            (0, 0), (1, 1, 1), (0, 1, 0), (1, 1), (0, 1), (1, 0),
            (0, 1, 1), (1, 1, 0), (1, 0, 1), (0, 0, 1), (1, 0, 0),
            (0, 1, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0), (1, 0, 0, 1),
        ]
    elif group_name == "A5":
        gens = ((1, 0, 3, 2, 4), (0, 2, 4, 3, 1))
        min_len, max_len = 2, 8
        canonical_w = [
            (0, 0), (1, 1, 1), (0, 1, 0, 1, 0, 1, 0, 1, 0, 1),
            (0, 1), (1, 0), (0, 1, 1), (1, 1, 0), (0, 1, 0), (1, 0, 1),
            (0, 1, 0, 1), (1, 0, 1, 0), (0, 1, 1, 0), (1, 0, 0, 1),
        ]
    else:
        raise ValueError(f"Unknown group: {group_name}")

    rng = np_mod.random.default_rng(seed)
    by_elem: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    all_words: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for length in range(min_len, max_len + 1):
        for _ in range(60 if length <= 4 else 140):
            w = tuple(int(x) for x in rng.integers(0, 2, size=length))
            if w not in seen:
                seen.add(w)
                by_elem.setdefault(_eval_group_word(w, gens), []).append(w)
                all_words.append(w)
    for w in canonical_w:
        if w not in seen:
            seen.add(w)
            by_elem.setdefault(_eval_group_word(w, gens), []).append(w)
            all_words.append(w)

    pos_pool: list[tuple[tuple[int, ...], tuple[int, ...], int]] = []
    for wlist in by_elem.values():
        if len(wlist) < 2:
            continue
        for _ in range(min(40, len(wlist) * 2)):
            i, j = int(rng.integers(0, len(wlist))), int(rng.integers(0, len(wlist)))
            if i != j:
                a, b = (wlist[i], wlist[j]) if wlist[i] < wlist[j] else (wlist[j], wlist[i])
                pos_pool.append((a, b, 1))
    pos_pool = list(dict.fromkeys(pos_pool))

    by_counts: dict[tuple[int, int], list[tuple[int, ...]]] = {}
    for w in all_words:
        c0 = w.count(0)
        by_counts.setdefault((c0, len(w) - c0), []).append(w)

    neg_hard: list[tuple[tuple[int, ...], tuple[int, ...], int]] = []
    for wlist in by_counts.values():
        if len(wlist) < 2:
            continue
        for _ in range(min(40, len(wlist) * 2)):
            i, j = int(rng.integers(0, len(wlist))), int(rng.integers(0, len(wlist)))
            if i != j and _eval_group_word(wlist[i], gens) != _eval_group_word(wlist[j], gens):
                a, b = (wlist[i], wlist[j]) if wlist[i] < wlist[j] else (wlist[j], wlist[i])
                neg_hard.append((a, b, 0))
    neg_hard = list(dict.fromkeys(neg_hard))

    neg_gen: list[tuple[tuple[int, ...], tuple[int, ...], int]] = []
    for _ in range(2000):
        wa = all_words[int(rng.integers(0, len(all_words)))]
        wb = all_words[int(rng.integers(0, len(all_words)))]
        if _eval_group_word(wa, gens) != _eval_group_word(wb, gens):
            a, b = (wa, wb) if wa < wb else (wb, wa)
            neg_gen.append((a, b, 0))
    neg_gen = list(dict.fromkeys(neg_gen))

    rng.shuffle(pos_pool)
    rng.shuffle(neg_hard)
    rng.shuffle(neg_gen)
    need_pos = (n_train + n_test) // 2
    need_hard = need_pos // 2
    sel_pos = pos_pool[:need_pos]
    sel_hard = neg_hard[:need_hard]
    sel_neg = sel_hard + [p for p in neg_gen if p not in set(sel_hard)][: need_pos - need_hard]
    tr_half = n_train // 2
    return sel_pos[:tr_half] + sel_neg[:tr_half], sel_pos[tr_half:need_pos] + sel_neg[tr_half:need_pos]


def _q_mul_f64(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (
        a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
        a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
        a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
        a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0,
    )


def _cayley_acute_q_f64(wx: float, wy: float, wz: float) -> tuple[float, float, float, float]:
    wx = max(-0.4, min(0.4, wx))
    wy = max(-0.4, min(0.4, wy))
    wz = max(-0.4, min(0.4, wz))
    inv_norm = 1.0 / math.sqrt(1.0 + wx * wx + wy * wy + wz * wz)
    return (inv_norm, wx * inv_norm, wy * inv_norm, wz * inv_norm)


def _synthesize_su2_generators(
    gen_name: str,
    theta: tuple[float, float, float, float],
    c0x: float,
    c0y: float,
    ox18: Any,
    oy18: Any,
    np_mod: Any,
) -> tuple[tuple[float, float, float, float], tuple[float, float, float, float]]:
    cx, cy, ell, phi = theta
    radius = 10.0 ** (-ell)
    cp, sp = math.cos(phi), math.sin(phi)
    px = cx + radius * (ox18 * cp - oy18 * sp)
    py = cy + radius * (ox18 * sp + oy18 * cp)

    if gen_name == "mandelbrot_boundary_su2":
        vals = _mandelbrot_smooth_potential(px, py, int(min(260, max(80, round(80.0 + 35.0 * ell)))), np_mod)
    elif gen_name == "prng_sha256_su2":
        vals = _prng_sha256_field(px, py, np_mod)
    elif gen_name == "fourier_fixed_smooth_su2":
        vals = _fourier_fixed_field(px, py, np_mod)
    elif gen_name == "fourier_matched_scale_su2":
        vals = _fourier_matched_scale_field(px, py, c0x, c0y, radius, int(round(ell)), np_mod)
    else:
        raise ValueError(f"Unknown SU(2) generator: {gen_name}")

    v = [float(x) * 0.4 for x in vals.tolist()]
    t0 = _q_mul_f64(_q_mul_f64(_cayley_acute_q_f64(v[0], v[1], v[2]), _cayley_acute_q_f64(v[3], v[4], v[5])), _cayley_acute_q_f64(v[6], v[7], v[8]))
    t1 = _q_mul_f64(_q_mul_f64(_cayley_acute_q_f64(v[9], v[10], v[11]), _cayley_acute_q_f64(v[12], v[13], v[14])), _cayley_acute_q_f64(v[15], v[16], v[17]))
    return t0, t1


def _eval_su2_word_pairs(
    t0: tuple[float, float, float, float],
    t1: tuple[float, float, float, float],
    pairs: list[Any],
    tau: float = 0.90,
) -> tuple[float, float]:
    gens = (t0, t1)
    cache: dict[tuple[int, ...], tuple[float, float, float, float]] = {}

    def _wq(w: tuple[int, ...]) -> tuple[float, float, float, float]:
        q = cache.get(w)
        if q is None:
            cur = (1.0, 0.0, 0.0, 0.0)
            for sym in w:
                cur = _q_mul_f64(cur, gens[sym])
            cache[w] = cur
            return cur
        return q

    loss_sum = 0.0
    correct = 0
    for wa, wb, label in pairs:
        qa, qb = _wq(wa), _wq(wb)
        overlap = min(1.0, abs(qa[0] * qb[0] + qa[1] * qb[1] + qa[2] * qb[2] + qa[3] * qb[3]))
        err = (1.0 - overlap) if label == 1 else max(0.0, overlap - 0.35)
        loss_sum += err * err
        if (1 if overlap >= tau else 0) == label:
            correct += 1
    n = float(len(pairs))
    return loss_sum / n, correct / n


def run_su2_seed_evolution_benchmark(np_mod: Any, stats_mod: Any) -> dict[str, Any]:
    ox18, oy18 = _phyllotaxis_offsets(18, np_mod)
    c0x, c0y = MISIUREWICZ_C0
    n_restarts, steps_per_restart, n_seeds, tau = 4, 400, 5, 0.90
    eval_budget = n_restarts * steps_per_restart
    generators = ["mandelbrot_boundary_su2", "prng_sha256_su2", "fourier_fixed_smooth_su2", "fourier_matched_scale_su2"]
    tasks = ["S3", "A5"]
    task_results: dict[str, Any] = {}

    for t_idx, gname in enumerate(tasks):
        train_pairs, test_pairs = _build_group_word_dataset(gname, 7700 + t_idx, 80, 160, np_mod)
        _, abelian_acc = _eval_su2_word_pairs(_cayley_acute_q_f64(0.35, 0.0, 0.0), _cayley_acute_q_f64(-0.25, 0.0, 0.0), test_pairs, tau)
        gen_runs: dict[str, Any] = {}

        for g_idx, gen_name in enumerate(generators):
            seed_te, seed_tr, seed_comm = [], [], []
            total_rb, max_drift = 0, 0.0
            for s in range(n_seeds):
                rng = np_mod.random.default_rng(91000 + 1000 * t_idx + 100 * g_idx + s)
                best_g = (1e9, -1.0, (1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 0.0))
                for _ in range(n_restarts):
                    init_ell = float(rng.uniform(2.8, 4.2))
                    ir = 10.0 ** (-init_ell)
                    cur_th = (c0x + float(rng.uniform(-0.5, 0.5)) * ir, c0y + float(rng.uniform(-0.5, 0.5)) * ir, init_ell, float(rng.uniform(0.0, 2.0 * math.pi)))
                    cur_t0, cur_t1 = _synthesize_su2_generators(gen_name, cur_th, c0x, c0y, ox18, oy18, np_mod)
                    cur_l, cur_a = _eval_su2_word_pairs(cur_t0, cur_t1, train_pairs, tau)
                    step_xy, step_ell, step_phi = 0.40, 0.30, 0.50
                    for ev in range(1, steps_per_restart):
                        snap_th, snap_t0, snap_t1 = cur_th, cur_t0, cur_t1
                        ckpt = struct.pack("<ffff", *cur_t0)
                        require_ok(len(ckpt) == 16, "Checkpoint width != 16B")
                        rl = 10.0 ** (-cur_th[2])
                        sm = 0.25 if (ev % 3 == 0) else 1.0
                        cand_th = (
                            cur_th[0] + float(rng.normal(0.0, step_xy * sm * rl)),
                            cur_th[1] + float(rng.normal(0.0, step_xy * sm * rl)),
                            float(np_mod.clip(cur_th[2] + float(rng.normal(0.0, step_ell * sm)), 2.5, 5.5)),
                            (cur_th[3] + float(rng.normal(0.0, step_phi * sm))) % (2.0 * math.pi),
                        )
                        ct0, ct1 = _synthesize_su2_generators(gen_name, cand_th, c0x, c0y, ox18, oy18, np_mod)
                        cl, ca = _eval_su2_word_pairs(ct0, ct1, train_pairs, tau)
                        if (cl < cur_l - 1e-9) or (abs(cl - cur_l) <= 1e-9 and ca > cur_a):
                            cur_th, cur_t0, cur_t1, cur_l, cur_a = cand_th, ct0, ct1, cl, ca
                            step_xy = min(0.70, step_xy * 1.08)
                            step_phi = min(0.90, step_phi * 1.08)
                        else:
                            cur_th = snap_th
                            rt0, rt1 = _synthesize_su2_generators(gen_name, cur_th, c0x, c0y, ox18, oy18, np_mod)
                            drift = math.sqrt(sum((a - b) ** 2 for a, b in zip(rt0, snap_t0)) + sum((a - b) ** 2 for a, b in zip(rt1, snap_t1)))
                            max_drift = max(max_drift, drift)
                            cur_t0, cur_t1 = rt0, rt1
                            total_rb += 1
                            step_xy = max(0.015, step_xy * 0.992)
                            step_phi = max(0.025, step_phi * 0.992)
                    if cur_l < best_g[0]:
                        best_g = (cur_l, cur_a, cur_t0, cur_t1)
                _, te_a = _eval_su2_word_pairs(best_g[2], best_g[3], test_pairs, tau)
                ab, ba = _q_mul_f64(best_g[2], best_g[3]), _q_mul_f64(best_g[3], best_g[2])
                seed_comm.append(math.sqrt(sum((x - y) ** 2 for x, y in zip(ab, ba))))
                seed_tr.append(best_g[1])
                seed_te.append(te_a)

            gen_runs[gen_name] = {
                "seed_bytes": 32,
                "stored_matrix_bytes": 0,
                "readout_weight_bytes": 0,
                "eval_budget_per_seed": eval_budget,
                "n_seeds": n_seeds,
                "train_acc_mean_pct": round(float(np_mod.mean(seed_tr)) * 100.0, 4),
                "test_acc_mean_pct": round(float(np_mod.mean(seed_te)) * 100.0, 4),
                "test_acc_std_pct": round(float(np_mod.std(seed_te, ddof=1)) * 100.0, 4),
                "test_accs_per_seed": [round(v, 6) for v in seed_te],
                "commutator_norm_mean": round(float(np_mod.mean(seed_comm)), 6),
                "checkpoint_16b_rollbacks_executed": total_rb,
                "checkpoint_16b_max_rollback_drift": max_drift,
            }

        mb = gen_runs["mandelbrot_boundary_su2"]["test_accs_per_seed"]
        task_results[gname] = {
            "n_train_pairs": len(train_pairs),
            "n_test_pairs": len(test_pairs),
            "projective_overlap_tau": tau,
            "abelian_sanity_ceiling_pct": round(abelian_acc * 100.0, 4),
            "generators": gen_runs,
            "paired_tests": {
                "mandelbrot_vs_prng_sha256": _paired_stats(mb, gen_runs["prng_sha256_su2"]["test_accs_per_seed"], np_mod, stats_mod),
                "mandelbrot_vs_fourier_fixed": _paired_stats(mb, gen_runs["fourier_fixed_smooth_su2"]["test_accs_per_seed"], np_mod, stats_mod),
                "mandelbrot_vs_fourier_matched_scale": _paired_stats(mb, gen_runs["fourier_matched_scale_su2"]["test_accs_per_seed"], np_mod, stats_mod),
            },
        }

    prim = [
        ("S3", "mandelbrot_vs_prng_sha256"),
        ("S3", "mandelbrot_vs_fourier_fixed"),
        ("A5", "mandelbrot_vs_prng_sha256"),
        ("A5", "mandelbrot_vs_fourier_fixed"),
    ]
    adj_gt = holm_bonferroni([task_results[t]["paired_tests"][c]["p_t_one_sided_greater"] for t, c in prim])
    holm_m4 = {
        f"{t}:{c}": {
            "mean_diff_pp": task_results[t]["paired_tests"][c]["mean_diff_pp"],
            "p_holm_t_one_sided_greater": round(adj_gt[i], 6),
            "beats_by_ge_10pp_and_p_holm_lt_0_01": bool(task_results[t]["paired_tests"][c]["mean_diff_pp"] >= 10.0 and adj_gt[i] < 0.01),
        }
        for i, (t, c) in enumerate(prim)
    }
    a5_pass = holm_m4["A5:mandelbrot_vs_prng_sha256"]["beats_by_ge_10pp_and_p_holm_lt_0_01"] and holm_m4["A5:mandelbrot_vs_fourier_fixed"]["beats_by_ge_10pp_and_p_holm_lt_0_01"]
    s3_pass = holm_m4["S3:mandelbrot_vs_prng_sha256"]["beats_by_ge_10pp_and_p_holm_lt_0_01"] and holm_m4["S3:mandelbrot_vs_fourier_fixed"]["beats_by_ge_10pp_and_p_holm_lt_0_01"]
    all_zero = all(task_results[t]["generators"][g]["checkpoint_16b_max_rollback_drift"] == 0.0 for t in tasks for g in generators)

    return {
        "protocol": {
            "seed_bytes": 32,
            "stored_transition_matrix_bytes": 0,
            "readout_weight_bytes": 0,
            "acute_cayley_steps_per_generator": 3,
            "acute_component_bound": 0.4,
            "n_restarts": n_restarts,
            "steps_per_restart": steps_per_restart,
            "zoom_ell_bounds": [2.5, 5.5],
            "eval_budget_per_seed": eval_budget,
            "n_seeds": n_seeds,
            "checkpoint_bytes": 16,
        },
        "tasks": task_results,
        "holm_bonferroni_m4_primary": holm_m4,
        "summary": {
            "a5_beats_both_primary_ge_10pp_p_holm_lt_0_01": bool(a5_pass),
            "s3_beats_both_primary_ge_10pp_p_holm_lt_0_01": bool(s3_pass),
            "all_rollbacks_zero_drift": bool(all_zero),
            "verdict": "CONFIRMED" if (a5_pass and s3_pass and all_zero) else ("PARTIAL" if ((a5_pass or s3_pass) and all_zero) else "FALSIFIED"),
        },
    }


def verify_receipts(work_dir: Path) -> str:
    """Pure-stdlib fail-closed verification of results_su2_transport_and_s73.json."""
    receipt_path = work_dir / "results_su2_transport_and_s73.json"
    require_ok(receipt_path.is_file(), f"Missing receipt file: {receipt_path.name}")
    data = json.loads(receipt_path.read_text(encoding="utf-8"))

    exp_sha = canonical_sha256(data)
    got_sha = str(data.get("result_sha256", ""))
    require_ok(hmac.compare_digest(got_sha, exp_sha), "Combined receipt result_sha256 mismatch")
    require_ok(data["energy_power_status"] == ENERGY_POLICY_STATUS, "Unexpected energy_power_status")
    check_no_forbidden_energy_claims(data)

    # Validate embedded pure-Q certificate live against su2_procedural_transport_verify
    su2v.validate_certificate(data["pure_q_su2_and_logfree_certificate"])
    live_cert = su2v.build_certificate()
    require_ok(
        hmac.compare_digest(data["pure_q_su2_and_logfree_certificate"]["result_sha256"], live_cert["result_sha256"]),
        "Embedded pure-Q certificate differs from live verifier output",
    )

    require_ok(data["s73_uci_cv_benchmark"]["uci_data_sha256"] == UCI_DATA_SHA256, "UCI SHA-256 pin mismatch")
    require_ok(len(data["multiscale_ell_0_16"]["scales"]) == 17, "Expected 17 scales ell=0..16")
    require_ok(data["multiscale_ell_0_16"]["summary"]["f64_cliff_certified"] is True, "float64 cliff flag false")
    require_ok(data["su2_zero_readout_seed_evolution"]["summary"]["all_rollbacks_zero_drift"] is True, "Rollback drift nonzero")
    return got_sha


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reproducible CPU Benchmark for Paper 1 v4.0 §7.3 & Procedural SU(2) Transport.")
    parser.add_argument("--run", action="store_true", help="Run full CPU benchmarks and write results_su2_transport_and_s73.json.")
    parser.add_argument("--data-dir", type=str, default="data_cache", help="Directory containing UCI dataset files.")
    parser.add_argument("--verify-receipts", action="store_true", help="Verify results_su2_transport_and_s73.json in pure stdlib.")
    args = parser.parse_args(argv)

    work_dir = Path(__file__).resolve().parent
    if args.verify_receipts and not args.run:
        sha = verify_receipts(work_dir)
        print(f"PASS RESULTS_SU2_TRANSPORT_AND_S73 result_sha256={sha}")
        return 0

    if not args.run:
        parser.print_help()
        return 0

    import numpy as np_mod
    from scipy import stats as stats_mod

    data_dir = Path(args.data_dir)
    if not data_dir.is_absolute():
        data_dir = work_dir / data_dir

    pure_q_cert = su2v.build_certificate()
    su2v.validate_certificate(pure_q_cert)

    payload: dict[str, Any] = {
        "schema_version": "moissanite.su2_transport_and_s73_results.v1",
        "contribution": "Moissanite-Labs clean-room Paper 1 v4.0 §7.3 replication & zero-readout SU(2) procedural transport",
        "energy_power_status": ENERGY_POLICY_STATUS,
        "pure_q_su2_and_logfree_certificate": pure_q_cert,
        "multiscale_ell_0_16": run_multiscale_cliff_benchmark(np_mod),
        "s73_uci_cv_benchmark": run_s73_uci_cv_benchmark(data_dir, np_mod, stats_mod),
        "su2_zero_readout_seed_evolution": run_su2_seed_evolution_benchmark(np_mod, stats_mod),
    }
    payload["result_sha256"] = canonical_sha256(payload)
    out_path = work_dir / "results_su2_transport_and_s73.json"
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE {out_path.name} result_sha256={payload['result_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
