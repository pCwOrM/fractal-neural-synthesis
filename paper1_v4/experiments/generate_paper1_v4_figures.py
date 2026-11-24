"""
Fractal Neural Synthesis (FNS) — Publication-Grade Vector Figures (Figures 2 through 6)
Reads exact verified outputs from paper1_v4/data/paper1_v4_results.json (Rev2 schema).
"""

import json
import math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_paper1_v4_suite import (
    compute_patch_grid,
    synthesize_weights_aperture,
    ridge_fit_predict,
    make_two_moons,
    make_two_spirals,
    GOLDEN_ANGLE,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "paper1_v4_results.json"
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

C_BLUE = "#0072B2"
C_ORANGE = "#D55E00"
C_GREEN = "#009E73"
C_PURPLE = "#CC79A7"
C_YELLOW = "#E69F00"
C_SKY = "#56B4E9"
C_DARK = "#1E293B"
C_GRAY = "#64748B"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "mathtext.fontset": "dejavusans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.28,
    "grid.linestyle": "--",
    "axes.labelsize": 9.3,
    "axes.titlesize": 10.0,
    "xtick.labelsize": 8.4,
    "ytick.labelsize": 8.4,
    "legend.fontsize": 7.9,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def save_fig(fig, stem: str):
    for ext in ("pdf", "png"):
        out = FIG_DIR / f"{stem}.{ext}"
        fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.08)
    print(f"Saved: {stem}.pdf / .png")
    plt.close(fig)


# ==============================================================================
# FIGURE 2: GENERATOR ABLATION (RANK COLLAPSE, CONTINUITY & DRIFT TRACKING)
# ==============================================================================

def make_fig2(res):
    ms = res["exp2"]["multiscale"]
    dr = res["exp2"]["drift_tracking_48b"]

    meta = [
        ("mandelbrot_boundary", "Complex Quadratic $\\partial\\mathcal{M}$ (FNS)", C_BLUE, "o", "-"),
        ("prng_sha256", "SHA-256 PRNG (24B Key)", C_ORANGE, "s", "--"),
        ("fourier_smooth", "Smooth 2D Fourier Basis", C_GREEN, "^", "-."),
        ("lattice_value", "Fixed-Lattice Value Noise", C_PURPLE, "D", ":"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.15), dpi=300)

    # Panel (a): Standardized 16x16 Effective Matrix Rank across magnification ell=0..8
    ax = axes[0]
    for key, label, col, mk, ls in meta:
        rows = ms[key]
        ells = [r["ell"] for r in rows]
        rk = [r["std_eff_rank_16x16_mean"] for r in rows]
        rksd = [r["std_eff_rank_16x16_sd"] for r in rows]
        ax.plot(ells, rk, color=col, marker=mk, linestyle=ls, lw=2.0, ms=5.3, label=label)
        ax.fill_between(ells, np.array(rk) - np.array(rksd), np.array(rk) + np.array(rksd), color=col, alpha=0.12)
    ax.axhline(2.0, color="#64748B", lw=1.0, ls=":")
    ax.annotate("$C^1$ Taylor-Ramp Bound\n($\\mathrm{rank}_{\\mathrm{eff}} \\leq 2$)", xy=(5.0, 2.0), xytext=(2.8, 4.3),
                fontsize=7.6, color="#475569", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#475569", lw=1.0))
    ax.set_xlabel("Log-Magnification $\\ell = \\log_{10}(\\zeta)$")
    ax.set_ylabel("Standardized $16\\times 16$ Effective Rank")
    ax.set_title("(a) Post-Standardization Rank vs. Zoom", fontweight="bold", pad=8)
    ax.set_xticks(range(0, 9))
    ax.set_ylim(0.5, 16.5)

    # Panel (b): Local Coordinate Smoothness / Continuity rho(Theta, Theta + delta)
    ax = axes[1]
    for key, label, col, mk, ls in meta:
        rows = ms[key]
        ells = [r["ell"] for r in rows]
        cs = [r["local_corr_mean"] for r in rows]
        sds = [r["local_corr_sd"] for r in rows]
        ax.plot(ells, cs, color=col, marker=mk, linestyle=ls, lw=2.0, ms=5.3, label=label)
        ax.fill_between(ells, np.clip(np.array(cs) - np.array(sds), -0.2, 1.05),
                        np.clip(np.array(cs) + np.array(sds), -0.2, 1.05), color=col, alpha=0.12)
    ax.axhline(0.0, color="#94A3B8", lw=0.9)
    ax.annotate("PRNG Avalanche\n($\\rho \\approx 0$, Discontinuous)", xy=(4.0, 0.02), xytext=(3.4, 0.28),
                fontsize=7.6, color=C_ORANGE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_ORANGE, lw=1.0))
    ax.set_xlabel("Log-Magnification $\\ell = \\log_{10}(\\zeta)$")
    ax.set_ylabel("Local Step Correlation $\\rho(\\Theta, \\Theta+\\boldsymbol{\\delta})$")
    ax.set_title("(b) Coordinate-Space Search Continuity", fontweight="bold", pad=8)
    ax.set_xticks(range(0, 9))
    ax.set_ylim(-0.18, 1.08)

    # Panel (c): 48B Zero-Readout Continuous Domain-Drift Tracking (Two-Moons 0 -> 60 deg)
    ax = axes[2]
    angles = dr["mandelbrot_boundary"]["angles"]
    for key, label, col, mk, ls in meta:
        m_arr = np.array(dr[key]["mean_acc_by_angle"]) * 100.0
        s_arr = np.array(dr[key]["sd_acc_by_angle"]) * 100.0
        ax.plot(angles, m_arr, color=col, marker=mk, linestyle=ls, lw=2.1, ms=5.5, label=label)
        ax.fill_between(angles, m_arr - s_arr, m_arr + s_arr, color=col, alpha=0.13)
    ax.set_xlabel("Manifold Rotation Drift Angle $\\theta$ (deg)")
    ax.set_ylabel("Held-Out Test Accuracy (%)")
    ax.set_title("(c) 48B Online Drift Tracking (Standardized)", fontweight="bold", pad=8)
    ax.set_xticks(angles)
    ax.set_ylim(42, 100)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, frameon=True,
               facecolor="#F8FAFC", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, -0.06), fontsize=8.4)
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    save_fig(fig, "fig2_generator_continuity_ablation")


# ==============================================================================
# FIGURE 3: FOUR GEOMETRIC APERTURES & SPECTRAL/ACCURACY ABLATION (EXP 3)
# ==============================================================================

def make_fig3(res):
    exp3 = res["exp3"]
    cx, cy, lz = -0.743643887037151, 0.131825904205330, 2.15
    nu_bg, _ = compute_patch_grid(cx, cy, lz, res=160, max_iter=70)

    fig = plt.figure(figsize=(13.6, 6.8), dpi=300)
    gs = GridSpec(2, 4, height_ratios=[1.05, 1.15], hspace=0.38, wspace=0.28, figure=fig)

    n_vis = 81
    ap_vis = [
        ("cartesian_grid", "(A) Cartesian Grid", C_GRAY),
        ("rule_of_thirds", "(B) 3×3 Rule-of-Thirds ($\\mathbb{Z}/9\\mathbb{Z}$)", C_YELLOW),
        ("vogel_spiral", "(C) $\\phi$-Vogel Spiral", C_GREEN),
        ("harmonic_tripod", "(D) Multi-Scale Harmonic Tripod", C_BLUE),
    ]
    for idx, (ap, title, col) in enumerate(ap_vis):
        ax = fig.add_subplot(gs[0, idx])
        ax.imshow(nu_bg, origin="lower", extent=[-1, 1, -1, 1], cmap="magma", alpha=0.88, aspect="equal")
        if ap == "cartesian_grid":
            xs = np.linspace(-0.92, 0.92, 9)
            gx, gy = np.meshgrid(xs, xs)
            ax.scatter(gx.ravel(), gy.ravel(), s=13, c="#FFFFFF", edgecolors=C_DARK, linewidths=0.45, zorder=5)
            for v in [-0.5, 0.0, 0.5]:
                ax.axvline(v, color="#FFFFFF", lw=0.6, alpha=0.45)
                ax.axhline(v, color="#FFFFFF", lw=0.6, alpha=0.45)
        elif ap == "rule_of_thirds":
            for v in [-1.0 / 3.0, 1.0 / 3.0]:
                ax.axvline(v, color="#FDE047", lw=1.3, ls="--", alpha=0.9)
                ax.axhline(v, color="#FDE047", lw=1.3, ls="--", alpha=0.9)
            k = np.arange(n_vis)
            cell = k % 9
            layer = k // 9
            row = (cell // 3) - 1
            col_i = (cell % 3) - 1
            sr = ((layer * 5) % 3) / 2.0 - 0.5
            sc_v = (((layer // 3) * 7 + cell * 3) % 3) / 2.0 - 0.5
            px = col_i * (2.0 / 3.0) + sc_v * (2.0 / 3.0) * 0.72
            py = row * (2.0 / 3.0) + sr * (2.0 / 3.0) * 0.72
            ax.scatter(px, py, s=16, c="#FEF08A", edgecolors="#713F12", linewidths=0.5, zorder=5)
        elif ap == "vogel_spiral":
            k = np.arange(n_vis, dtype=float)
            r = 0.95 * np.sqrt((k + 0.5) / n_vis)
            th = k * GOLDEN_ANGLE
            px, py = r * np.cos(th), r * np.sin(th)
            ax.plot(px, py, color="#A7F3D0", lw=0.55, alpha=0.65, zorder=4)
            ax.scatter(px, py, s=16, c="#34D399", edgecolors="#064E3B", linewidths=0.45, zorder=5)
        else:
            tier_cols = ["#38BDF8", "#FBBF24", "#FB7185"]
            scales_rel = [0.95, 0.62, 0.38]
            for t_i, (sr_val, tc) in enumerate(zip(scales_rel, tier_cols)):
                circ = plt.Circle((0, 0), sr_val, fill=False, ec=tc, ls="--", lw=1.0, alpha=0.85)
                ax.add_patch(circ)
                k = np.arange(27, dtype=float)
                r = sr_val * np.sqrt((k + 0.5) / 27.0)
                th = k * GOLDEN_ANGLE + t_i * (2.0 * math.pi / 3.0)
                ax.scatter(r * np.cos(th), r * np.sin(th), s=15, c=tc, edgecolors="#0F172A", linewidths=0.4, zorder=5)
        ax.set_title(title, fontsize=9.0, fontweight="bold", pad=5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for sp in ax.spines.values():
            sp.set_visible(True)
            sp.set_color(col)
            sp.set_linewidth(1.5)

    ax_r = fig.add_subplot(gs[1, 0:2])
    ds_names = list(exp3.keys())
    short_ds = [d.replace("UCI ", "").replace("Statlog ", "") for d in ds_names]
    x = np.arange(len(ds_names))
    w = 0.19
    aps = [
        ("cartesian_grid", "Cartesian Grid", C_GRAY),
        ("rule_of_thirds", "3×3 Rule-of-Thirds", C_YELLOW),
        ("vogel_spiral", "$\\phi$-Vogel Spiral", C_GREEN),
        ("harmonic_tripod", "Harmonic Tripod", C_BLUE),
    ]
    for i, (ap, lbl, col) in enumerate(aps):
        vals = [exp3[d][ap]["spectral"]["rank_utilization"] * 100.0 for d in ds_names]
        ax_r.bar(x + (i - 1.5) * w, vals, width=w, color=col, edgecolor="#1E293B", linewidth=0.5, label=lbl)
    ax_r.set_xticks(x)
    ax_r.set_xticklabels(short_ds, fontsize=8.5)
    ax_r.set_ylabel("Effective Spectral Rank Utilization (%)")
    ax_r.set_title("(E) Weight Matrix Spectral Rank Utilization ($H=256$)", fontweight="bold", pad=7)
    ax_r.set_ylim(0, 108)

    ax_a = fig.add_subplot(gs[1, 2:4])
    for i, (ap, lbl, col) in enumerate(aps):
        means = [exp3[d][ap]["acc"]["mean"] * 100.0 for d in ds_names]
        sds = [exp3[d][ap]["acc"]["sd"] * 100.0 for d in ds_names]
        ax_a.bar(x + (i - 1.5) * w, means, width=w, yerr=sds, capsize=2.5,
                 color=col, edgecolor="#1E293B", linewidth=0.5, error_kw=dict(lw=0.9), label=lbl)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(short_ds, fontsize=8.5)
    ax_a.set_ylabel("10-Fold Stratified CV Accuracy (%)")
    ax_a.set_title("(F) Out-of-Sample Accuracy by Geometric Aperture", fontweight="bold", pad=7)
    ax_a.set_ylim(75, 102)

    handles, labels = ax_r.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, frameon=True,
               facecolor="#F8FAFC", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, -0.02), fontsize=8.5)
    save_fig(fig, "fig3_geometric_apertures")


# ==============================================================================
# FIGURE 4: UNIFIED 10-FOLD REAL-WORLD PARETO FRONTIERS (EXP 4)
# ==============================================================================

def make_fig4(res):
    pareto = res["exp4"]["pareto_sweep_cv10"]
    cv10 = res["exp4"]["cv10_summary"]
    ds_names = list(pareto.keys())

    fig, axes = plt.subplots(2, 2, figsize=(12.4, 7.8), dpi=300)
    axes_flat = axes.ravel()

    for idx, ds_name in enumerate(ds_names):
        ax = axes_flat[idx]
        rows = pareto[ds_name]
        meta = cv10[ds_name]["meta"]

        b_f8 = [r["FNS_INT8"]["bytes"] for r in rows]
        a_f8 = [r["FNS_INT8"]["acc"] * 100.0 for r in rows]
        b_r8 = [r["Seeded_RFF_INT8"]["bytes"] for r in rows]
        a_r8 = [r["Seeded_RFF_INT8"]["acc"] * 100.0 for r in rows]
        b_m4 = [r["MLP_INT4"]["bytes"] for r in rows]
        a_m4 = [r["MLP_INT4"]["acc"] * 100.0 for r in rows]
        b_m32 = [r["MLP_FP32"]["bytes"] for r in rows]
        a_m32 = [r["MLP_FP32"]["acc"] * 100.0 for r in rows]

        ax.semilogx(b_f8, a_f8, color=C_BLUE, marker="o", lw=2.3, ms=6.3, label="FNS-Tripod + INT8 (24B Hidden)")
        ax.semilogx(b_r8, a_r8, color=C_GREEN, marker="^", lw=1.9, ms=5.8, ls="--", label="Seeded-PRNG RFF + INT8 (8B Hidden)")
        ax.semilogx(b_m4, a_m4, color=C_ORANGE, marker="s", lw=1.8, ms=5.3, ls="-.", label="Quantized INT4 MLP")
        ax.semilogx(b_m32, a_m32, color=C_DARK, marker="D", lw=1.8, ms=5.3, ls=":", label="Dense FP32 MLP (ReLU)")

        # Add Linear-INT8 (0 hidden) and Hashed-ELM (256B, H=256) markers
        lin_m = cv10[ds_name]["models"]["Linear_INT8"]
        hsh_m = cv10[ds_name]["models"]["Hashed_ELM_256B"]
        ax.scatter([lin_m["storage"]["total_bytes"]], [lin_m["acc"]["mean"] * 100.0],
                   marker="X", s=105, color="#DC2626", edgecolors="#0F172A", lw=0.6, zorder=8, label="Linear-INT8 (0 Hidden)")
        ax.scatter([hsh_m["storage"]["total_bytes"]], [hsh_m["acc"]["mean"] * 100.0],
                   marker="P", s=80, color=C_PURPLE, edgecolors="#0F172A", lw=0.6, zorder=8, label="Hashed-ELM (256B, $H=256$)")

        # Highlight H=256 FNS-INT8 compression vs FP32 MLP
        i_top = len(rows) - 1
        ratio = b_m32[i_top] / max(1, b_f8[i_top])
        gain_lin = a_f8[i_top] - lin_m["acc"]["mean"] * 100.0
        ymin = min(min(a_f8), min(a_r8), min(a_m4), lin_m["acc"]["mean"] * 100.0) - 4.0
        ax.set_ylim(max(50, ymin), 101.2)
        y_box = ymin + (100.0 - max(50, ymin)) * 0.22
        ax.annotate(f"FNS ($H$=256): {b_f8[i_top]} B\n({ratio:.0f}× vs MLP, {gain_lin:+.1f} pp vs Lin)",
                    xy=(b_f8[i_top], a_f8[i_top]),
                    xytext=(b_f8[i_top] * 1.45, y_box),
                    fontsize=7.3, fontweight="bold", color=C_BLUE, zorder=9,
                    bbox=dict(boxstyle="round,pad=0.22", fc="#EDF6FC", ec=C_BLUE, lw=0.75),
                    arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.0))

        ax.set_title(f"{ds_name} ($N={meta['N']},\\; d={meta['d']},\\; C={meta['classes']}$)",
                     fontweight="bold", pad=6)
        ax.set_xlabel("Total Persistent Flash Storage (Bytes, Log Scale, 0 Scaler B)")
        ax.set_ylabel("10-Fold Stratified CV Accuracy (%)")

    handles, labels = axes_flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=True,
               facecolor="#F8FAFC", edgecolor="#CBD5E1", bbox_to_anchor=(0.5, -0.02), fontsize=8.3)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    save_fig(fig, "fig4_real_world_pareto")


# ==============================================================================
# FIGURE 5: 2D MANIFOLDS + EQUAL-BUDGET MULTI-PATCH ES SCALING (EXP 1 & 5)
# ==============================================================================

def make_fig5(res):
    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.15), dpi=300)
    seed_coord = (-0.743643887037151, 0.131825904205330, 2.15)
    W_gs, b_gs = synthesize_weights_aperture(*seed_coord, 2, 64, aperture="vogel_spiral", gamma=2.8)

    # Panel (a): Two-Moons Held-Out Contour
    X_m, y_m = make_two_moons(1000, 0.10, 42)
    Xtr_m, Xte_m, ytr, yte = train_test_split(X_m, y_m, test_size=200, stratify=y_m, random_state=42)
    sc = StandardScaler()
    Xtr, Xte = sc.fit_transform(Xtr_m), sc.transform(Xte_m)
    _, rb8, W_out = ridge_fit_predict(np.tanh(Xtr @ W_gs + b_gs), ytr, np.tanh(Xte @ W_gs + b_gs), 2, reg=1e-3, quantize_int8=True)
    acc_m = res["exp1"]["manifolds_cv10"]["Two-Moons"]["FNS_Spiral_INT8"]["acc"]

    gx, gy = np.meshgrid(np.linspace(-2.5, 2.5, 180), np.linspace(-2.4, 2.4, 180))
    Gpts = np.c_[gx.ravel(), gy.ravel()]
    Hg = np.hstack([np.tanh(Gpts @ W_gs + b_gs), np.ones((len(Gpts), 1))])
    Z = (1.0 / (1.0 + np.exp(-np.clip((Hg @ W_out).ravel() * 3.0, -15, 15)))).reshape(gx.shape)

    ax = axes[0]
    ax.contourf(gx, gy, Z, levels=20, cmap="RdBu_r", alpha=0.45)
    ax.contour(gx, gy, Z, levels=[0.5], colors=[C_DARK], linewidths=1.8)
    ax.scatter(Xte[yte == 0, 0], Xte[yte == 0, 1], c=C_BLUE, s=16, alpha=0.85, edgecolors="white", lw=0.35, label="Class 0 (Test)")
    ax.scatter(Xte[yte == 1, 0], Xte[yte == 1, 1], c=C_ORANGE, s=16, alpha=0.85, edgecolors="white", lw=0.35, label="Class 1 (Test)")
    ax.set_title(f"(a) Two-Moons Held-Out ({acc_m['mean']*100:.2f}% ± {acc_m['sd']*100:.2f}%)\n24B Hidden + {rb8}B INT8 Head", fontweight="bold", fontsize=9.0)
    ax.set_xlabel("$x_1$ (Standardized)")
    ax.set_ylabel("$x_2$ (Standardized)")
    ax.legend(loc="lower left", fontsize=7.3, frameon=True)

    # Panel (b): Two-Spirals Held-Out Contour
    X_s, y_s = make_two_spirals(200, 0.04, 42)
    Xtr_s, Xte_s, ytr2, yte2 = train_test_split(X_s, y_s, test_size=40, stratify=y_s, random_state=42)
    sc2 = StandardScaler()
    Xtr2, Xte2 = sc2.fit_transform(Xtr_s), sc2.transform(Xte_s)
    _, rb_s, W_out2 = ridge_fit_predict(np.tanh(Xtr2 @ W_gs + b_gs), ytr2, np.tanh(Xte2 @ W_gs + b_gs), 2, reg=1e-3, quantize_int8=False)
    acc_s = res["exp1"]["manifolds_cv10"]["Two-Spirals"]["FNS_Spiral_FP32"]["acc"]

    gx2, gy2 = np.meshgrid(np.linspace(-2.5, 2.5, 180), np.linspace(-2.5, 2.5, 180))
    Gpts2 = np.c_[gx2.ravel(), gy2.ravel()]
    Hg2 = np.hstack([np.tanh(Gpts2 @ W_gs + b_gs), np.ones((len(Gpts2), 1))])
    Z2 = (1.0 / (1.0 + np.exp(-np.clip((Hg2 @ W_out2).ravel() * 3.0, -15, 15)))).reshape(gx2.shape)

    ax = axes[1]
    ax.contourf(gx2, gy2, Z2, levels=20, cmap="RdBu_r", alpha=0.45)
    ax.contour(gx2, gy2, Z2, levels=[0.5], colors=[C_DARK], linewidths=1.8)
    ax.scatter(Xte2[yte2 == 0, 0], Xte2[yte2 == 0, 1], c=C_BLUE, s=22, alpha=0.9, edgecolors="white", lw=0.4, label="Arm 0 (Test)")
    ax.scatter(Xte2[yte2 == 1, 0], Xte2[yte2 == 1, 1], c=C_ORANGE, s=22, alpha=0.9, edgecolors="white", lw=0.4, label="Arm 1 (Test)")
    ax.set_title(f"(b) Two-Spirals Held-Out ({acc_s['mean']*100:.2f}% ± {acc_s['sd']*100:.2f}%)\n24B Hidden + {rb_s}B FP32 Head", fontweight="bold", fontsize=9.0)
    ax.set_xlabel("$x_1$ (Standardized)")
    ax.set_ylabel("$x_2$ (Standardized)")
    ax.legend(loc="lower left", fontsize=7.3, frameon=True)

    # Panel (c): Exp 5 — Strict Equal-Budget (32 evals/gen) Optimization Scaling
    ax = axes[2]
    exp5 = res["exp5"]
    es_meta = [
        ("hybrid_elitist_rank1_es", "Hybrid Elitist + Rank-1 ES", C_BLUE, "-"),
        ("elitist_coord_walk", "Elitist Coordinate Walk", C_ORANGE, "-."),
        ("eggroll_rank1_es", "EGGROLL-Style Rank-1 ES", C_GREEN, "--"),
        ("antithetic_full_es", "Antithetic Full-Rank ES", C_PURPLE, ":"),
    ]
    gens = np.arange(1, len(exp5["elitist_coord_walk"]["curve_acc_mean"]) + 1)
    for k, lbl, col, ls in es_meta:
        m = np.array(exp5[k]["curve_acc_mean"]) * 100.0
        s = np.array(exp5[k]["curve_acc_sd"]) * 100.0
        ax.plot(gens, m, color=col, linestyle=ls, lw=2.1, label=lbl)
        ax.fill_between(gens, m - s, m + s, color=col, alpha=0.12)
    ax.set_title("(c) Equal-Budget 0-Readout Scaling\n(6 Patches = 144B, 32 Evals/Gen, $N_{\\mathrm{runs}}=10$)", fontweight="bold", fontsize=9.0)
    ax.set_xlabel("Optimization Generation")
    ax.set_ylabel("Held-Out Test Accuracy (%)")
    ax.set_xlim(1, len(gens))
    ax.legend(loc="lower right", fontsize=7.3, frameon=True)

    plt.tight_layout()
    save_fig(fig, "fig5_manifolds_and_es_scaling")


# ==============================================================================
# FIGURE 6: SYSTEMS STORAGE REDUCTION & WARMED-UP BOOT AMORTIZATION (EXP 4)
# ==============================================================================

def make_fig6(res):
    cv10 = res["exp4"]["cv10_summary"]
    ds_names = list(cv10.keys())
    short_ds = [f"{d.replace('UCI ', '').replace('Statlog ', '')}\n($d={cv10[d]['meta']['d']}$)" for d in ds_names]

    fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.35), dpi=300)

    # Panel (a): Persistent Hidden-Layer Storage (Log Scale Bytes, H=256)
    ax = axes[0]
    x = np.arange(len(ds_names))
    w = 0.25
    b_mlp32 = [cv10[d]["models"]["MLP_FP32"]["storage"]["hidden_bytes"] for d in ds_names]
    b_mlp4 = [cv10[d]["models"]["MLP_INT4"]["storage"]["hidden_bytes"] for d in ds_names]
    b_fns = [24 for _ in ds_names]

    ax.bar(x - w, b_mlp32, width=w, color=C_DARK, edgecolor="#0F172A", lw=0.6, label="Dense FP32 MLP Hidden ($O(dH)$)")
    ax.bar(x, b_mlp4, width=w, color=C_ORANGE, edgecolor="#0F172A", lw=0.6, label="INT4 Quantized MLP Hidden")
    ax.bar(x + w, b_fns, width=w, color=C_BLUE, edgecolor="#0F172A", lw=0.6, label="FNS Coordinate Seed ($O(1) = 24$ B)")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(short_ds, fontsize=8.4)
    ax.set_ylabel("Hidden-Layer Persistent Flash (Bytes, Log)")
    ax.set_title("(a) $O(1)$ vs. $O(dH)$ Persistent Hidden Storage ($H=256$)", fontweight="bold", pad=8)
    ax.set_ylim(10, 1.4e6)

    for idx in range(len(ds_names)):
        ratio = b_mlp32[idx] / 24.0
        ax.text(x[idx] + w + 0.02, 30, f"24 B\n({ratio:.0f}×)", ha="center", va="bottom",
                fontsize=6.9, fontweight="bold", color=C_BLUE,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
        ax.text(x[idx] - w, b_mlp32[idx] * 1.15, f"{b_mlp32[idx]/1024:.1f} KB",
                ha="center", va="bottom", fontsize=7.0, color=C_DARK)
    ax.legend(loc="upper left", fontsize=7.8, frameon=True)

    # Panel (b): Warmed-Up Boot Synthesis Amortization (Host CPU, Apples-to-Apples Batch-1 SRAM)
    ax = axes[1]
    cycles = np.logspace(0, 5, 200)
    cols = [C_BLUE, C_GREEN, C_ORANGE, C_PURPLE]
    for idx, d in enumerate(ds_names):
        m = cv10[d]["meta"]
        boot_us = m["boot_synthesis_ms_mean"] * 1000.0
        inf_us = m["sram_infer_b1_us_fns"]
        amortized_us = (boot_us / cycles) + inf_us
        lbl = f"{d.replace('UCI ', '').replace('Statlog ', '')} (boot {m['boot_synthesis_ms_mean']:.1f} ms, $b=1$: {inf_us:.1f} $\\mu$s)"
        ax.loglog(cycles, amortized_us, color=cols[idx], lw=2.1, label=lbl)

    ax.axhline(50.0, color="#64748B", ls=":", lw=1.1)
    ax.text(1.5, 62.0, "50 $\\mu$s Host-CPU Envelope", fontsize=7.5, color="#475569", style="italic")
    ax.set_xlabel("Consecutive SRAM Inferences per Boot ($N_{\\mathrm{cycles}}$)")
    ax.set_ylabel("Amortized Latency per Inference ($\\mu$s, Log)")
    ax.set_title("(b) Warmed-Up Boot Amortization (Host CPU, $b=1$)", fontweight="bold", pad=8)
    ax.legend(loc="upper right", fontsize=7.1, frameon=True)

    plt.tight_layout()
    save_fig(fig, "fig6_cross_domain_verification")


def main():
    res = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    make_fig2(res)
    make_fig3(res)
    make_fig4(res)
    make_fig5(res)
    make_fig6(res)
    print("All revised figures 2-6 generated cleanly.")


if __name__ == "__main__":
    main()
