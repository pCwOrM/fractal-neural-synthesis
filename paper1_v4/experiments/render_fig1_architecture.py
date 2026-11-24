"""
Render Figure 1: Publication-Grade Vector End-to-End FNS v4.0 Architecture Diagram
Outputs:
  paper1_v4/figures/fig1_fns_architecture.pdf  (Vector PDF for LaTeX)
  paper1_v4/figures/fig1_fns_architecture.svg  (Vector SVG)
  paper1_v4/figures/fig1_fns_architecture.png  (300-DPI PNG for Visual Critic audit)
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def draw_box(ax, x, y, w, h, title, body, fc, ec, title_color="#111827", body_color="#1F2937",
             lw=1.3, title_size=8.6, body_size=7.4, header_h=None, bold_border=False, pad=0.006):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad},rounding_size=0.014",
        facecolor=fc, edgecolor=ec, linewidth=(lw * 1.35 if bold_border else lw),
        zorder=3,
    )
    ax.add_patch(box)
    if header_h is not None:
        ax.text(x + w / 2, y + h - header_h / 2, title,
                ha="center", va="center", fontsize=title_size, fontweight="bold",
                color=title_color, zorder=5)
        ax.plot([x + 0.008, x + w - 0.008], [y + h - header_h, y + h - header_h],
                color=ec, lw=0.8, alpha=0.55, zorder=4)
    else:
        if body:
            ax.text(x + w / 2, y + h * 0.72, title,
                    ha="center", va="center", fontsize=title_size, fontweight="bold",
                    color=title_color, zorder=5)
            ax.text(x + w / 2, y + h * 0.34, body,
                    ha="center", va="center", fontsize=body_size, linespacing=1.28,
                    color=body_color, zorder=5)
        else:
            ax.text(x + w / 2, y + h / 2, title,
                    ha="center", va="center", fontsize=title_size, fontweight="bold",
                    color=title_color, zorder=5)


def draw_arrow(ax, x1, y1, x2, y2, color="#334155", rad=0.0, ls="-", lw=1.8):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle="-|>,head_length=6,head_width=3.6",
        color=color, linewidth=lw, linestyle=ls, zorder=6,
    )
    ax.add_patch(arr)


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig, ax = plt.subplots(figsize=(13.2, 5.4), dpi=300)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.axis("off")

    # Colorblind-safe Okabe-Ito-inspired refined academic palette
    c_s1_bg, c_s1_ec, c_s1_hd = "#EDF6FC", "#0072B2", "#004C77"
    c_s2_bg, c_s2_ec, c_s2_hd = "#F5EFFA", "#7A3E9D", "#4E2268"
    c_s3_bg, c_s3_ec, c_s3_hd = "#FEF6EC", "#D55E00", "#8C3B00"
    c_s4_bg, c_s4_ec, c_s4_hd = "#ECF9F2", "#009E73", "#006348"
    c_s5_bg, c_s5_ec, c_s5_hd = "#F1F5F9", "#334155", "#0F172A"

    # Main Title
    ax.text(0.50, 0.962,
            "Fractal Neural Synthesis (FNS): End-to-End Procedural Weight Derivation & Verification Pipeline",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color="#0F172A")

    # Five horizontal stages with clean inter-stage spacing
    y_bot, h_stage = 0.200, 0.720
    w_col = 0.166
    gap = 0.035
    xs = [0.015 + i * (w_col + gap) for i in range(5)]

    # --- Stage 1 ---
    draw_box(ax, xs[0], y_bot, w_col, h_stage,
             "1. $O(1)$ Persistent Seed", "", c_s1_bg, c_s1_ec, c_s1_hd,
             lw=1.6, title_size=8.8, header_h=0.068)
    draw_box(ax, xs[0] + 0.010, 0.655, w_col - 0.020, 0.175,
             "Coordinate Tuple $\\Theta$",
             "$(c_x, c_y, \\ell) \\in \\mathbb{F}_{64}^3$\n3 × IEEE-754 Float64\n= 24 Bytes (192 bits)",
             "#FFFFFF", c_s1_ec, c_s1_hd, title_size=8.0, body_size=7.1, bold_border=True)
    draw_box(ax, xs[0] + 0.010, 0.440, w_col - 0.020, 0.175,
             "Multi-Patch Ensembles",
             "$\\boldsymbol{\\Theta} \\in \\mathbb{F}_{64}^{P \\times 3}$ ($24P$ B)\nZero Persistent Hidden\nTensor in Flash ROM",
             "#FFFFFF", "#5B9BD5", c_s1_hd, title_size=7.9, body_size=7.0)
    draw_box(ax, xs[0] + 0.010, 0.225, w_col - 0.020, 0.175,
             "Backprop-Free Search",
             "Elitist Coordinate Walk &\nLow-Rank ES (EGGROLL)\nGradient-Free Updates",
             "#FFFBEB", "#B45309", "#78350F", title_size=7.9, body_size=7.0)

    # --- Stage 2 ---
    draw_box(ax, xs[1], y_bot, w_col, h_stage,
             "2. Boundary Kernel", "", c_s2_bg, c_s2_ec, c_s2_hd,
             lw=1.6, title_size=8.8, header_h=0.068)
    draw_box(ax, xs[1] + 0.010, 0.655, w_col - 0.020, 0.175,
             "Complex Quadratic Map",
             "$z_{n+1} = z_n^2 + c,\\; z_0 = 0$\nSmooth Bailout $R = 256$\nCutoff $M_{\\max} = 70$",
             "#FFFFFF", c_s2_ec, c_s2_hd, title_size=8.0, body_size=7.1, bold_border=True)
    draw_box(ax, xs[1] + 0.010, 0.432, w_col - 0.020, 0.185,
             "Bifurcation Frontier $\\partial\\mathcal{M}$",
             "$\\dim_H(\\partial\\mathcal{M}\\cap U)=2$\nScale-Free ($10^0\\to 10^8$)\nSmooth Escape $\\tilde{\\nu}(c)$\nZero Lookup Tables",
             "#FFFFFF", "#A78BFA", c_s2_hd, title_size=7.9, body_size=6.8)
    draw_box(ax, xs[1] + 0.010, 0.225, w_col - 0.020, 0.170,
             "Formal Safety Gate",
             "Lean 4 Escape Invariance\n($|z_n|>2 \\Rightarrow |z_{n+k}|\\to\\infty$)\n0 sorry / 0 custom axioms",
             "#ECFDF5", "#0F766E", "#115E59", title_size=7.9, body_size=6.7)

    # --- Stage 3 ---
    draw_box(ax, xs[2], y_bot, w_col, h_stage,
             "3. Geometric Apertures", "", c_s3_bg, c_s3_ec, c_s3_hd,
             lw=1.6, title_size=8.8, header_h=0.068)
    draw_box(ax, xs[2] + 0.010, 0.700, w_col - 0.020, 0.130,
             "(A) Cartesian Grid",
             "Uniform spatial lattice\n(baseline sampling)",
             "#FFFFFF", "#E69F00", c_s3_hd, title_size=7.8, body_size=6.8)
    draw_box(ax, xs[2] + 0.010, 0.542, w_col - 0.020, 0.130,
             "(B) 3×3 Rule-of-Thirds",
             "$\\mathbb{Z}/9\\mathbb{Z}$ modular residue\nnodal grid stencil",
             "#FFFFFF", "#E69F00", c_s3_hd, title_size=7.8, body_size=6.8)
    draw_box(ax, xs[2] + 0.010, 0.384, w_col - 0.020, 0.130,
             "(C) $\\phi$-Vogel Spiral",
             "Golden angle $2\\pi/\\phi^2$\narea-preserving disk",
             "#FFFFFF", "#E69F00", c_s3_hd, title_size=7.8, body_size=6.8)
    draw_box(ax, xs[2] + 0.010, 0.225, w_col - 0.020, 0.132,
             "(D) Harmonic Tripod",
             "$\\{0.60, 1.00, 1.60\\}$ zoom\nmulti-scale cascade",
             "#FFF7ED", c_s3_ec, c_s3_hd, title_size=7.9, body_size=6.8, bold_border=True)

    # --- Stage 4 ---
    draw_box(ax, xs[3], y_bot, w_col, h_stage,
             "4. SRAM & Readout", "", c_s4_bg, c_s4_ec, c_s4_hd,
             lw=1.6, title_size=8.8, header_h=0.068)
    draw_box(ax, xs[3] + 0.010, 0.645, w_col - 0.020, 0.185,
             "Volatile SRAM Buffer",
             "$\\mathbf{W}\\in\\mathbb{R}^{d\\times H},\\;\\mathbf{b}\\in\\mathbb{R}^H$\nSynthesized Once at Boot\nLeCun Fan-In (0 Extra B)",
             "#FFFFFF", c_s4_ec, c_s4_hd, title_size=8.0, body_size=6.9, bold_border=True)
    draw_box(ax, xs[3] + 0.010, 0.435, w_col - 0.020, 0.172,
             "Mode I: 0-Byte Readout",
             "Fully Procedural Gates &\nContinuous Drift Tracking\n(24–144 B Total Flash)",
             "#FFFFFF", "#34D399", c_s4_hd, title_size=7.8, body_size=6.8)
    draw_box(ax, xs[3] + 0.010, 0.225, w_col - 0.020, 0.172,
             "Mode II: Compact Head",
             "Closed-Form Ridge Readout\nFP32 or INT8 Quantized\nFast $O(dH)$ SRAM Pass",
             "#FFFFFF", "#34D399", c_s4_hd, title_size=7.8, body_size=6.8)

    # --- Stage 5 ---
    draw_box(ax, xs[4], y_bot, w_col, h_stage,
             "5. Verified Targets", "", c_s5_bg, c_s5_ec, c_s5_hd,
             lw=1.6, title_size=8.8, header_h=0.068)
    draw_box(ax, xs[4] + 0.010, 0.700, w_col - 0.020, 0.130,
             "Edge TinyML MCUs",
             "ARM Cortex-M4 Flash $O(1)$\n$<1\\,\\mu$W SRAM retention",
             "#FFFFFF", "#64748B", c_s5_hd, title_size=7.8, body_size=6.8)
    draw_box(ax, xs[4] + 0.010, 0.542, w_col - 0.020, 0.130,
             "40-Core NUMA Metal",
             "Bare-metal throughput &\nzero-lock scaling",
             "#FFFFFF", "#64748B", c_s5_hd, title_size=7.8, body_size=6.8)
    draw_box(ax, xs[4] + 0.010, 0.384, w_col - 0.020, 0.130,
             "On-Chain Reflex Oracles",
             "Deterministic EVM\nintra-block circuit breakers",
             "#FFFFFF", "#64748B", c_s5_hd, title_size=7.8, body_size=6.8)
    draw_box(ax, xs[4] + 0.010, 0.225, w_col - 0.020, 0.132,
             "Hybrid System-1 / 2 AI",
             "Deterministic reflex gate +\nSystem-2 LLM reasoning",
             "#FFFFFF", "#64748B", c_s5_hd, title_size=7.8, body_size=6.8)

    # Inter-stage arrows (cleanly centered in the 0.035 gap)
    arrow_colors = [c_s1_ec, c_s2_ec, c_s3_ec, c_s4_ec]
    for i in range(4):
        draw_arrow(ax, xs[i] + w_col + 0.008, 0.56, xs[i + 1] - 0.008, 0.56,
                   color=arrow_colors[i], lw=2.2)

    # Clean orthogonal elbow feedback loop routed strictly BELOW the 5 stage containers
    x_src = xs[3] + w_col * 0.5
    x_dst = xs[0] + w_col * 0.5
    y_top_fb = y_bot - 0.009
    y_bus = 0.132
    ax.plot([x_src, x_src, x_dst], [y_top_fb, y_bus, y_bus],
            color="#B45309", ls="--", lw=1.6, zorder=4)
    draw_arrow(ax, x_dst, y_bus, x_dst, y_top_fb + 0.002,
               color="#B45309", ls="--", lw=1.6)
    ax.text((x_src + x_dst) / 2, y_bus,
            "  Fitness Feedback $\\mathcal{L}(\\Theta)$ (Offline Coordinate / Low-Rank ES Optimization — Zero Backpropagation)  ",
            ha="center", va="center", fontsize=7.5, style="italic", color="#92400E", zorder=6,
            bbox=dict(boxstyle="round,pad=0.22", fc="#FFFBEB", ec="#D97706", lw=0.85))

    # Footer Epistemic Scope Bar
    footer = FancyBboxPatch(
        (0.015, 0.015), 0.970, 0.062,
        boxstyle="round,pad=0.006,rounding_size=0.012",
        facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.0, zorder=3
    )
    ax.add_patch(footer)
    ax.text(0.50, 0.046,
            "Information-Theoretic Capacity Scope: Conditional Kolmogorov complexity $K_{\\mathrm{Kolm}}(\\mathbf{W},\\mathbf{b}\\mid d,H) \\leq 192 + c_0$ bits, "
            "$H(\\mathbf{W},\\mathbf{b}) \\leq 192$ bits per seed — optimal for $O(1)$-Flash System-1 edge boundaries; complementary to System-2 LLMs.",
            ha="center", va="center", fontsize=7.3, color="#1E293B", zorder=5)

    plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
    for ext in ["pdf", "svg", "png"]:
        out = FIG_DIR / f"fig1_fns_architecture.{ext}"
        fig.savefig(out, dpi=300, bbox_inches="tight", pad_inches=0.06)
        print(f"Saved: {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
