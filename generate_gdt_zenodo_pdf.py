import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register TrueType fonts from Windows Fonts for complete Unicode and Turkish glyph support
try:
    pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:\\Windows\\Fonts\\ariali.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'C:\\Windows\\Fonts\\arialbi.ttf'))
    MAIN_FONT = 'Arial'
    MAIN_BOLD = 'Arial-Bold'
    MAIN_ITALIC = 'Arial-Italic'
    MAIN_BOLD_ITALIC = 'Arial-BoldItalic'
except Exception as e:
    MAIN_FONT = 'Helvetica'
    MAIN_BOLD = 'Helvetica-Bold'
    MAIN_ITALIC = 'Helvetica-Oblique'
    MAIN_BOLD_ITALIC = 'Helvetica-Bold'


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont(MAIN_FONT, 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Running header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 752, "Dağlı, Dağlı & Dağlı — Lean 4 Formalization of the General Divisor Theorem (v3.0)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 746, 558, 746)

        # Running footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)
        
        self.drawString(54, 30, "Preprint Monograph | ITouch Systems Research & Development | Apache-2.0")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_str)
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    # Custom styles with TrueType Arial
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=15.5,
        leading=19.5,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=9.8,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=8
    )

    authors_style = ParagraphStyle(
        'Authors',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=9.2,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        alignment=1,
        spaceAfter=3
    )

    affil_style = ParagraphStyle(
        'Affiliations',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=7.4,
        leading=11,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=8
    )

    abstract_title = ParagraphStyle(
        'AbstractTitle',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,
        spaceAfter=3
    )

    abstract_style = ParagraphStyle(
        'Abstract',
        parent=styles['Normal'],
        fontName=MAIN_ITALIC,
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#1e293b"),
        alignment=4,
        leftIndent=15,
        rightIndent=15,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=3
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=5,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=8.3,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
        alignment=4,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor("#0f172a"),
        leftIndent=6,
        spaceAfter=3
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Machine-Certified Lean 4 Formalization of the General Divisor Theorem:<br/>Unified Density, Arbitrary-Bound Counting, and Finite Error Bounds", title_style))
    story.append(Paragraph("A Formalization Monograph & Lean 4 Kernel Audit Report (Release v3.0 — 81 Theorems, 0 Sorry)", subtitle_style))
    
    # Canonical Institutional Künye
    authors_text = "<b>Volkan Dağlı</b><sup>1,2</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Zerrin Dağlı</b><sup>3,4</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Dağhan Dağlı</b><sup>5</sup>"
    story.append(Paragraph(authors_text, authors_style))
    
    affils_text = (
        "<sup>1</sup>Anadolu University, Eskişehir, Türkiye &nbsp;&nbsp; "
        "<sup>2</sup>ITouch Systems, Adana, Türkiye (ORCID: 0009-0000-1587-8703)<br/>"
        "<sup>3</sup>Mersin University, Mersin, Türkiye (ORCID: 0000-0001-9490-6425) &nbsp;&nbsp; "
        "<sup>4</sup>Yusuf Kalkavan Anadolu Lisesi, Mersin, Türkiye<br/>"
        "<sup>5</sup>Toros Science High School, MEV (Toros University), Mersin, Türkiye (ORCID: 0009-0003-2492-8313)"
    )
    story.append(Paragraph(affils_text, affil_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=6))

    # Abstract
    story.append(Paragraph("ABSTRACT", abstract_title))
    abstract_content = (
        "We present the machine-certified formalization (Release v3.0) of the <b>General Divisor Theorem (GDT)</b> "
        "in the Lean 4 interactive theorem prover, encompassing <b>81 kernel-checked theorems and lemmas</b> across seven "
        "modular components with <b>zero project axioms</b> and <b>zero unadmitted goals (0 sorry)</b>. Originally formulated by "
        "Dan Hawkley (thinkthoughts, 2026), GDT provides exact density corrections for arithmetic coprime residue sets "
        "<i>S(N, L, m, a) = {1 ≤ n ≤ L : n ≡ a (mod m), gcd(n, N) = 1}</i> where modulus <i>m</i> and constraint <i>N</i> "
        "share prime factors. In this unified formalization, incorporating milestone Pull Requests #1 and #2, we construct: "
        "(1) the complete arithmetic dichotomy (inadmissible empty branch for <i>gcd(a, d) &gt; 1</i> vs. admissible periodic branch for "
        "<i>gcd(a, d) = 1</i>, where <i>d = rad(gcd(m, N))</i> and <i>R = rad(N)/d</i>); (2) exact single-period counting "
        "showing exactly <i>φ(R)</i> solutions in minimal period <i>T_min = lcm(m, rad(N))</i> via affine unit permutations on <i>ZMod R</i>; "
        "(3) closed-form arbitrary-bound counting <i>C(q T_min + s) = q φ(R) + C(s)</i> computable in <i>O(1)</i> arithmetic operations; "
        "(4) strict finite-period error bounding <i>|T_min C(X) - φ(R) X| ≤ T_min²</i>; and (5) constructive natural density convergence "
        "<i>δ(S) = lim_{X→∞} C(X)/X = φ(R)/(mR)</i> proved via the real squeeze theorem. All proofs rely exclusively on standard classical "
        "foundations [propext, Classical.choice, Quot.sound] and pass 100% of 2,287 automated empirical verification instances."
    )
    story.append(Paragraph(abstract_content, abstract_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=6))

    # Section 1: Introduction
    story.append(Paragraph("1. Introduction & Theoretical Motivation", h1_style))
    story.append(Paragraph(
        "In analytic number theory and arithmetic sieve theory, counting integers up to <i>L</i> satisfying simultaneous congruence "
        "<i>n ≡ a (mod m)</i> and coprimality <i>gcd(n, N) = 1</i> has traditionally relied upon statistical independence heuristics:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;|S_naive(N, L, m, a)| ≈ (φ(N) / N) · (L / m)",
        body_style
    ))
    story.append(Paragraph(
        "Whenever <i>gcd(m, N) &gt; 1</i>, this naive hypothesis breaks down completely due to prime collision. "
        "The General Divisor Theorem resolves this by decomposing <i>rad(N)</i> into shared-prime radical <i>d = rad(gcd(m, N))</i> "
        "and coprime residue radical <i>R = rad(N) / d</i> with <i>gcd(m, R) = 1</i>. This yields the exact Euler density correction factor:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>C(N, m) = d / φ(d) = ∏_{p | gcd(m, N)} [ p / (p - 1) ]</b>",
        body_style
    ))

    # Section 2: Mathematical Formulation
    story.append(Paragraph("2. Exact Arithmetic Dichotomy & Density Limit", h1_style))
    story.append(Paragraph(
        "<b>Theorem (Admissibility Dichotomy & Arbitrary-Bound Counting):</b> Let <i>N, m, a ∈ ℕ</i> with <i>N, m ≥ 1</i>. "
        "Let <i>d = rad(gcd(m, N))</i> and <i>R = rad(N)/d</i>. Then:<br/>"
        "&nbsp;&nbsp;<b>1. Inadmissible Branch:</b> If <i>gcd(|a|, d) &gt; 1</i>, then <i>S(N, m, a) = ∅</i> (cardinality is 0 for all bounds).<br/>"
        "&nbsp;&nbsp;<b>2. Admissible Branch:</b> If <i>gcd(|a|, d) = 1</i>, the indicator is periodic with minimal period "
        "<i>T_min = m · R = lcm(m, rad(N))</i> and accepts exactly <i>φ(R)</i> values per period.<br/>"
        "&nbsp;&nbsp;<b>3. Arbitrary-Bound Count:</b> For any bound <i>X = q · T_min + s</i> with <i>0 ≤ s &lt; T_min</i>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>C(X) = q · φ(R) + C(s)</b> &nbsp;&nbsp;&nbsp;&nbsp; (computable in <i>O(1)</i> period blocks)<br/>"
        "&nbsp;&nbsp;<b>4. Natural Density Limit & Finite Error:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>|T_min · C(X) - φ(R) · X| ≤ T_min²</b> &nbsp;&nbsp; and &nbsp;&nbsp; "
        "<b>lim_{X → ∞} C(X) / X = φ(R) / (m · R)</b>",
        body_style
    ))

    # Add Infographic figure
    infographic_path = "gdt_twitter_infographic.png"
    if not os.path.exists(infographic_path):
        infographic_path = "docs/general_divisor_theorem/gdt_twitter_infographic.png"
    if os.path.exists(infographic_path):
        story.append(Spacer(1, 3))
        story.append(Image(infographic_path, width=480, height=270))
        fig_cap = ParagraphStyle('FigCap', parent=styles['Normal'], fontName=MAIN_ITALIC, fontSize=7.2, leading=9.5, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=4)
        story.append(Paragraph("Figure 1: Lean 4 Kernel Verification Architecture across 7 Production Modules (81 Theorems, 0 Sorry).", fig_cap))

    # Section 3: Lean 4 Kernel Verification Inventory (81 Theorems)
    story.append(Paragraph("3. Lean 4 Formal Architecture & Kernel Inventory", h1_style))
    story.append(Paragraph(
        "The repository is organized into 7 production modules, verified on <code>leanprover/lean4:v4.21.0</code> and <code>mathlib4:v4.21.0</code>. "
        "No unverified axioms, no <code>sorry</code> holes, and no <code>native_decide</code> shortcuts are employed:",
        body_style
    ))

    module_data = [
        ["Module File", "Theorems", "Axioms", "sorry", "Core Formal Role & Contribution"],
        ["GeneralDivisorTheorem.lean", "39", "0", "0", "Foundational arithmetic, radical algebra, Theorems 1, 1', and 2"],
        ["VolkanBridge.lean", "10", "0", "0", "Two-way isomorphism bridging Volkan's API with Dan's specification"],
        ["DensityBridge.lean", "14", "0", "0", "Per-period count #{n < T_min : n≡a, gcd(n,N)=1} = φ(R) via ZMod R units"],
        ["DensityCount.lean", "7", "0", "0", "Arbitrary-bound counting C(q·T_min + s) = q·φ(R) + C(s) via period blocks"],
        ["DensityLimit.lean", "6", "0", "0", "Finite error bound |T_min C(X) - φ(R)X| ≤ T_min² and real squeeze density limit"],
        ["CorrectionBridge.lean", "2", "0", "0", "Totient radical multiplicativity & Euler correction factor identity"],
        ["GDTMain.lean", "3", "0", "0", "Master unified packaging resolving complete GDT dichotomy"],
        ["Total Across Repository", "81", "0", "0", "100% Kernel-Checked ([propext, Classical.choice, Quot.sound] only)"]
    ]
    t_mod = Table(module_data, colWidths=[120, 48, 42, 38, 256])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), MAIN_BOLD),
        ('FONTSIZE', (0,0), (-1,0), 6.8),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e2e8f0")),
        ('FONTNAME', (0,1), (-1,-1), MAIN_FONT),
        ('FONTNAME', (0,-1), (-1,-1), MAIN_BOLD),
        ('FONTSIZE', (0,1), (-1,-1), 6.8),
        ('ALIGN', (1,0), (3,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 4))

    # Section 4: Lean Code Callout
    story.append(Paragraph("4. Core Lean 4 Formal Theorems", h1_style))
    lean_code_sample = """-- Master Unified GDT Dichotomy (GDTMain.lean)
theorem general_divisor_theorem (N m : Nat) (a : Int) (hN : 0 < N) (hm : 0 < m) :
    (1 < Nat.gcd a.natAbs (d_param N m) ∧ (∀ n, ¬ S_indicator N m a n)) ∨
    (Nat.gcd a.natAbs (d_param N m) = 1 ∧
     (∀ n, S_indicator N m a (n + T_min N m) = S_indicator N m a n) ∧
     Tendsto (fun X : Nat => (countBelow N m a X : Real) / (X : Real))
             atTop (𝓝 ((Nat.totient (R_param N m) : Real) / ((T_min N m : Real)))))

-- Finite Period Error Bound (DensityLimit.lean)
theorem density_error_bound (N m : Nat) (a : Int) (hN : 0 < N) (hm : 0 < m)
    (ha : Nat.gcd a.natAbs (d_param N m) = 1) (X : Nat) :
    |(T_min N m : Real) * (countBelow N m a X : Real) - (Nat.totient (R_param N m) : Real) * (X : Real)|
      ≤ ((T_min N m : Real) ^ 2)"""

    callout_data = [[Paragraph(lean_code_sample.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]]
    t_callout = Table(callout_data, colWidths=[504])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 4))

    # Section 5: Benchmark Table
    story.append(Paragraph("5. Canonical Benchmark Instances & Boundary Distinctions", h1_style))
    table_data = [
        ["Constraint N", "Modulus m", "Residue a", "Shared d", "Period T_min", "Exact C(N,m)", "Status in Lean 4"],
        ["210 (P_4)", "6", "5", "6", "210", "3.00 (3)", "Verified (norm_num)"],
        ["210 (P_4)", "10", "3", "10", "210", "2.50 (5/2)", "Verified (norm_num)"],
        ["210 (P_4)", "30", "7", "30", "210", "3.75 (15/4)", "Verified (norm_num)"],
        ["18", "2", "1", "2", "6 (≠ 18)", "2.00", "benchmark_3_3_i_Tmin_lt_N"],
        ["5", "6", "2", "1", "30", "1.00", "benchmark_3_3_ii_sharp_admissibility"]
    ]
    t_bench = Table(table_data, colWidths=[70, 60, 55, 55, 75, 75, 114])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), MAIN_BOLD),
        ('FONTSIZE', (0,0), (-1,0), 7.2),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f1f5f9")]),
        ('FONTNAME', (0,1), (-1,-1), MAIN_FONT),
        ('FONTSIZE', (0,1), (-1,-1), 7.2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 4))

    # Section 6: Verification & Open Access
    story.append(Paragraph("6. Empirical Verification & Open Science Infrastructure", h1_style))
    story.append(Paragraph(
        "<b>Exhaustive Verification Suite:</b> Automated oracle sweeps (<code>scripts/verify_gdt.py</code> and <code>scripts/verify_bridge.py</code>) "
        "tested 2,287 parameter combinations over bounds <i>N ∈ [2 .. 60]</i> and <i>m ∈ [2 .. 30]</i> with 100% agreement between "
        "theoretical closed-form formulas and brute-force counting.<br/>"
        "<b>Theoretical Origin & Landmark PR Contributions:</b> The theoretical framework of GDT originates with <b>Dan Hawkley</b> "
        "(@thinkthoughts / antiviolence.ai). We gratefully acknowledge his contributions authoring milestone Pull Requests #1 "
        "(merge <code>a5ef2b6</code>) and #2 (merge <code>f97b6c2</code>), formalizing the density bridge, arbitrary-bound counting, and density limits.<br/>"
        "<b>Infrastructure & Support:</b> High-performance computing cluster nodes and verification hosting provided by "
        "<b>Bekirhan Dağlı</b> (Managing Partner) and <b>ITouch Systems Research & Development</b>.<br/>"
        "<b>Open Repository:</b> https://github.com/pCwOrM/general-divisor-theorem &nbsp;|&nbsp; "
        "<b>Zenodo Concept DOI:</b> 10.5281/zenodo.23316068 (Apache-2.0)",
        body_style
    ))

    # References
    story.append(Spacer(1, 3))
    story.append(Paragraph("References", h1_style))
    refs = [
        "[1] Hawkley, D. (thinkthoughts) (2026). <i>The General Divisor Theorem: Exact Density Correction under Residue Conditioning</i>. Monograph Draft v3.3. antiviolence.ai: https://antiviolence.ai/gdt.pdf | Mirror: https://github.com/pCwOrM/general-divisor-theorem/blob/main/docs/gdt.pdf",
        "[2] Dağlı, V., Dağlı, Z., & Dağlı, D. (2026). <i>Machine-Certified Lean 4 Formalization of the General Divisor Theorem: Unified Density, Arbitrary-Bound Counting, and Finite Error Bounds</i>. CERN Zenodo, Concept DOI: 10.5281/zenodo.23316068.",
        "[3] Dağlı, V., Dağlı, Z., & Dağlı, D. (2026). <i>Mandelbrot Fractal Neural Synthesis & Discrete Harmonic Modular Closures</i>. CERN Zenodo, DOI: 10.5281/zenodo.23072120.",
        "[4] The Lean Community (2026). <i>The Lean 4 Interactive Theorem Prover and Mathlib4 Mathematical Library</i>. https://leanprover.github.io/"
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', parent=styles['Normal'], fontName=MAIN_FONT, fontSize=7, leading=9.2, textColor=colors.HexColor("#334155"), spaceAfter=2)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {filename}")


if __name__ == '__main__':
    # Build in wonderful-raman
    out1 = "General_Divisor_Theorem_Lean4_Formalization.pdf"
    build_pdf(out1)
    
    # Also mirror into general-divisor-theorem repo
    repo_pdf = "c:/Users/maat/Documents/antigravity/general-divisor-theorem/General_Divisor_Theorem_Lean4_Formalization.pdf"
    build_pdf(repo_pdf)
