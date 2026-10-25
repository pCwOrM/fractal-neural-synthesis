#!/usr/bin/env python3
"""
Generate Camera-Ready Academic PDF Monograph for Zenodo & SSRN:
"Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR
 and Structural Centralization on Ethereum L1"

Authors: Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı
Contributor: Bekirhan Dağlı (ITouch Systems)
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register TrueType fonts from Windows Fonts for complete Unicode glyphs
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
            self.drawString(54, 752, "Dağlı, Dağlı & Dağlı — Empirical OEV & Liquidation Dynamics in Chainlink SVR")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 746, 558, 746)

        # Running footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)
        
        self.drawString(54, 30, "Open Science Preprint | ITouch Systems Research & Development | CC-BY-4.0")
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
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=14.5,
        leading=18.5,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=9.2,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=7
    )

    authors_style = ParagraphStyle(
        'Authors',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=9.0,
        leading=12.5,
        textColor=colors.HexColor("#1e293b"),
        alignment=1,
        spaceAfter=3
    )

    affil_style = ParagraphStyle(
        'Affiliations',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=7.3,
        leading=10.5,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=7
    )

    abstract_title = ParagraphStyle(
        'AbstractTitle',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=8.8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,
        spaceAfter=3
    )

    abstract_style = ParagraphStyle(
        'Abstract',
        parent=styles['Normal'],
        fontName=MAIN_ITALIC,
        fontSize=8.0,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        alignment=4,
        leftIndent=12,
        rightIndent=12,
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=10.0,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=7,
        spaceAfter=3
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=5,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=8.0,
        leading=11.5,
        textColor=colors.HexColor("#1e293b"),
        alignment=4,
        spaceAfter=4
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=MAIN_FONT,
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName=MAIN_BOLD,
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Empirical OEV & Liquidation Dynamics: Protocol Value Recapture in Chainlink SVR and Structural Centralization on Ethereum L1", title_style))
    story.append(Paragraph("An Open Science Microstructure Audit Across 1,157 On-Chain Liquidations &bull; CERN Zenodo DOI: 10.5281/zenodo.23623588", subtitle_style))
    
    # Authors
    authors_text = "<b>Volkan Dağlı</b><sup>1,2</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Zerrin Dağlı</b><sup>3,4</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Dağhan Dağlı</b><sup>5</sup>"
    story.append(Paragraph(authors_text, authors_style))
    
    affils_text = (
        "<sup>1</sup>Anadolu University, Eskişehir, Türkiye &nbsp;&nbsp; "
        "<sup>2</sup>ITouch Systems Research Desk, Adana, Türkiye (ORCID: 0009-0000-1587-8703)<br/>"
        "<sup>3</sup>Mersin University, Mersin, Türkiye (ORCID: 0000-0001-9490-6425) &nbsp;&nbsp; "
        "<sup>4</sup>Yusuf Kalkavan Anadolu Lisesi, Mersin, Türkiye<br/>"
        "<sup>5</sup>Toros Science High School, MEV (Toros University), Mersin, Türkiye (ORCID: 0009-0003-2492-8313)<br/>"
        "<b>Infrastructure & Contributor Attribution:</b> Bekirhan Dağlı (ITouch Systems, Adana Çukurova Teknokent, Türkiye)"
    )
    story.append(Paragraph(affils_text, affil_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=5))

    # Abstract
    story.append(Paragraph("ABSTRACT", abstract_title))
    abstract_content = (
        "Order Flow Auctions (OFA) and Proposer-Builder Separation (PBS) have fundamentally reshaped decentralized finance (DeFi) "
        "liquidation mechanics. We present an exhaustive empirical study of <b>1,157 verified on-chain liquidations</b> encompassing "
        "<b>1,049 Ethereum L1 transactions</b> and <b>108 multi-call decoded Chainlink Smart Value Recapture (SVR) transactions (105 on Base L2, 3 on Arbitrum)</b> "
        "recorded during the acute volatility regime of October 12–19, 2026. Across 105 verified Base SVR transactions totaling <b>$190,506.31 in gross liquidated collateral</b>, "
        "we provide the first independent empirical proof that Chainlink SVR redirects <b>98.10% ($186,889.85 USD)</b> of gross liquidation value directly back to lending "
        "protocols and depositors as competitive bids. Unconstrained Bertrand price competition among permissionless solvers compresses gross margins to <b>1.86% ($3,545.73 USD pre-swap)</b>, "
        "with median transaction margin settling at <b>-1.55%</b>. In 61.9% of transactions (65/105), solvers concluded at zero or negative net margin prior to off-chain DEX slippage. "
        "We identify active participation from <b>20 distinct solver contract architectures and 27 signing EOAs</b>, debunking monopolistic capture (top solver captured only 31.64% volume share). "
        "Furthermore, we document that <b>64.76% (68/105) of SVR transactions were atomic multi-call bundles</b> executing up to 32 sub-calls in a single transaction, explaining why naive single-event "
        "indexers severely misreport liquidation accounting. In contrast, analysis of 1,049 Ethereum L1 liquidations reveals an acute power-law distribution where <b>80.84% (848 txs)</b> "
        "of block builder priority fees are micro-dust (< $1.00 USD, median $0.08 USD), while the top 22 whale liquidations capture 96.05% ($344,155.62 USD) of all builder revenue via private PBS bundles. "
        "All dataset records, replication scripts, and decoding tools are fully open-sourced in this Zenodo archive."
    )
    story.append(Paragraph(abstract_content, abstract_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=5))

    # Section 1
    story.append(Paragraph("1. Introduction & Theoretical Background", h1_style))
    story.append(Paragraph(
        "In decentralized lending protocols (such as Morpho Blue and Aave v3), solvency is preserved via programmatic liquidations: when a borrower's Health Factor (HF) "
        "falls below 1.00, third-party liquidators seize collateral at a pre-configured bonus to repay outstanding debt. On transparent mempools, this design induces "
        "destructive Priority Gas Auctions (PGA) and Miner/Maximal Extractable Value (MEV) leakage, transferring surplus away from depositors to block builders. "
        "To mitigate this, Layer-2 rollups have introduced Order Flow Auctions (OFA), exemplified by <b>Chainlink Smart Value Recapture (SVR)</b> operating via Atlas metacalls. "
        "Despite significant theoretical interest, empirical measurement of SVR performance under severe market volatility has remained absent from peer-reviewed literature. "
        "This monograph provides the first machine-verified empirical accounting of SVR value recapture, solver competition, and multi-call bundling complexity.",
        body_style
    ))

    # Section 2
    story.append(Paragraph("2. Base L2: Chainlink SVR Financial Breakdown & Value Recapture", h1_style))
    story.append(Paragraph(
        "During the high-volatility window of October 12–19, 2026, 105 SVR liquidation events occurred on Base across 83 monitored Morpho Blue markets and Aave v3. "
        "Table 1 summarizes the macroeconomic value distribution across these 105 audited multi-call events.",
        body_style
    ))

    # Table 1: Financial Summary
    t1_data = [
        [Paragraph("<b>Financial Metric</b>", table_cell_bold), Paragraph("<b>Amount (USD)</b>", table_cell_bold), Paragraph("<b>Share of Gross (%)</b>", table_cell_bold), Paragraph("<b>Microstructure Role</b>", table_cell_bold)],
        [Paragraph("Gross Seized Collateral", table_cell), Paragraph("$190,506.31", table_cell), Paragraph("100.00%", table_cell), Paragraph("Total borrower collateral liquidated", table_cell)],
        [Paragraph("Protocol Recaptured Bids", table_cell_bold), Paragraph("<b>$186,889.85</b>", table_cell_bold), Paragraph("<b>98.10%</b>", table_cell_bold), Paragraph("Returned directly to protocol & depositors", table_cell)],
        [Paragraph("Solver Retained Margin (Pre-Swap)", table_cell), Paragraph("$3,545.73", table_cell), Paragraph("1.86%", table_cell), Paragraph("Pre-DEX slippage gross solver compensation", table_cell)],
        [Paragraph("L2 Network Gas Fees", table_cell), Paragraph("$70.73", table_cell), Paragraph("0.04%", table_cell), Paragraph("Base sequencer execution gas", table_cell)],
    ]
    t1 = Table(t1_data, colWidths=[150, 85, 95, 174])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Bertrand Margin Compression:</b> Across the 105 transactions, solver margins exhibited severe downward compression. The median margin was <b>-1.55%</b>. "
        "Exactly <b>65 of 105 transactions (61.9%)</b> concluded at zero or negative net profit prior to DEX pool swap slippage. Only 9 transactions (8.6%) realized margins &ge; 5.00%. "
        "This confirms that permissionless order flow auctions force searchers into intense Bertrand competition where bids approach the theoretical collateral ceiling.",
        body_style
    ))

    # Section 3
    story.append(Paragraph("3. Solver Decentralization & The Absence of Monopolistic Capture", h1_style))
    story.append(Paragraph(
        "A critical governance question is whether MEV order flow auctions concentrate into monopolistic cartels. We identified <b>20 unique solver contract architectures</b> "
        "and <b>27 unique signing EOAs</b> actively competing on-chain. Table 2 provides the volume and transaction distribution among the top solvers.",
        body_style
    ))

    t2_data = [
        [Paragraph("<b>Solver Contract Address</b>", table_cell_bold), Paragraph("<b>Tx Count</b>", table_cell_bold), Paragraph("<b>Gross Vol (USD)</b>", table_cell_bold), Paragraph("<b>Vol Share (%)</b>", table_cell_bold), Paragraph("<b>Net Pre-Swap PnL</b>", table_cell_bold)],
        [Paragraph("0x8b61f5925f4515edb0b7b76c38036aaf9a818472", table_cell), Paragraph("51 (48.6%)", table_cell), Paragraph("$60,269.18", table_cell), Paragraph("31.64%", table_cell), Paragraph("+$447.20", table_cell)],
        [Paragraph("0x3ae5122d62e78dc14b98d8d30aca4faf9d1f1bba", table_cell), Paragraph("6 (5.7%)", table_cell), Paragraph("$53,452.63", table_cell), Paragraph("28.06%", table_cell), Paragraph("+$1,968.45", table_cell)],
        [Paragraph("0xbd0dd817c608e552d5f1ae701ab6c4da4fb00005", table_cell), Paragraph("4 (3.8%)", table_cell), Paragraph("$33,057.97", table_cell), Paragraph("17.35%", table_cell), Paragraph("+$620.40", table_cell)],
        [Paragraph("0xd12810b19b596347a3afac206d3ca65d08594b3f", table_cell), Paragraph("15 (14.3%)", table_cell), Paragraph("$17,842.90", table_cell), Paragraph("9.37%", table_cell), Paragraph("+$182.15", table_cell)],
        [Paragraph("0xa3eec55f71e62431b4afdb6b6734c11204f29a93", table_cell), Paragraph("1 (1.0%)", table_cell), Paragraph("$8,705.60", table_cell), Paragraph("4.57%", table_cell), Paragraph("+$212.80", table_cell)],
        [Paragraph("Remaining 15 Solvers", table_cell), Paragraph("28 (26.6%)", table_cell), Paragraph("$17,178.03", table_cell), Paragraph("9.01%", table_cell), Paragraph("+$114.73", table_cell)],
    ]
    t2 = Table(t2_data, colWidths=[180, 70, 84, 80, 90])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>No Single-Entity Monopoly:</b> Although solver `0x8b61...` won 48.6% of transaction counts by dominating micro-liquidations, it accounted for only <b>31.64% of total dollar volume</b>. "
        "Large liquidations were vigorously contested by independent solvers `0x3ae5...` and `0xbd0d...`, driving bids up to 96%–98% on major positions.",
        body_style
    ))

    # Section 4
    story.append(Paragraph("4. Multi-Call Bundling Complexity & The Fallacy of Single-Event Indexers", h1_style))
    story.append(Paragraph(
        "A critical methodological contribution of this research is identifying the prevalence of atomic multi-call bundling. "
        "<b>64.76% (68 of 105 transactions)</b> contained multiple liquidation sub-calls bundled into a single transaction execution. "
        "Single transactions executed up to <b>32 liquidation sub-calls</b> atomically in a single block. "
        "The distribution was: 1 call (37 txs, 35.2%), 2 calls (14 txs, 13.3%), 3 calls (12 txs, 11.4%), 15 calls (8 txs, 7.6%), 4 calls (7 txs, 6.7%), 6 calls (5 txs, 4.8%). "
        "Naive indexers evaluating only the initial log receipt produce massive accounting errors (e.g. misreporting that solvers suffered -$58k losses). "
        "Accurate SVR measurement requires recursive sub-call transaction trace decoding.",
        body_style
    ))

    # Section 5
    story.append(Paragraph("5. Market Risk Distribution & Empirical Case Studies", h1_style))
    story.append(Paragraph(
        "Liquidation activity during the volatility window concentrated heavily in specific collateral assets across the 83 monitored Morpho Blue markets:<br/>"
        "• <b>cbXRP/USDC (LLTV 62.5%):</b> 10 SVR transactions, $88,801.33 gross (46.61% of total volume), 96.19% recaptured.<br/>"
        "• <b>SOL/USDC (LLTV 62.5%):</b> 8 SVR transactions, $27,790.95 gross (14.59% of total volume), 96.10% recaptured.<br/>"
        "• <b>cbLTC/USDC (LLTV 62.5%):</b> 8 SVR transactions, $17,056.41 gross (8.95% of total volume), 95.50% recaptured.<br/>"
        "• <b>WETH/USDC (LLTV 86.0%):</b> 9 SVR transactions, $14,907.65 gross (7.82% of total volume), 98.40% recaptured.<br/>"
        "• <b>cbADA/USDC (LLTV 62.5%):</b> 11 SVR transactions, $10,488.43 gross (5.51% of total volume), 98.20% recaptured.",
        body_style
    ))

    # Case Studies Box
    t3_data = [
        [Paragraph("<b>Case Study</b>", table_cell_bold), Paragraph("<b>Tx Hash</b>", table_cell_bold), Paragraph("<b>Market</b>", table_cell_bold), Paragraph("<b>Gross ($)</b>", table_cell_bold), Paragraph("<b>Bid ($)</b>", table_cell_bold), Paragraph("<b>Recapture</b>", table_cell_bold), Paragraph("<b>Key Microstructure Finding</b>", table_cell_bold)],
        [
            Paragraph("<b>Case A: 32-Call Multi-Bundle</b>", table_cell_bold),
            Paragraph("0xc0a519...1f9", table_cell),
            Paragraph("cbXRP/USDC", table_cell),
            Paragraph("$20,969.08", table_cell),
            Paragraph("$19,979.88", table_cell),
            Paragraph("95.28%", table_cell),
            Paragraph("Largest atomic bundle. Solvers liquidated 32 positions simultaneously while returning 95.28% value to depositors.", table_cell)
        ],
        [
            Paragraph("<b>Case B: Whale Overbid</b>", table_cell_bold),
            Paragraph("0x76a4c8...616", table_cell),
            Paragraph("cbXRP/USDC", table_cell),
            Paragraph("$18,539.32", table_cell),
            Paragraph("$19,056.49", table_cell),
            Paragraph("<b>102.79%</b>", table_cell_bold),
            Paragraph("Winner's curse: Intense auction competition forced solver to bid 102.79% of collateral, absorbing a -$522.48 loss.", table_cell)
        ],
    ]
    t3 = Table(t3_data, colWidths=[90, 70, 65, 55, 55, 50, 119])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t3)
    story.append(Spacer(1, 4))

    # Section 6
    story.append(Paragraph("6. Ethereum L1 MEV-Boost Builder Payment Anatomy", h1_style))
    story.append(Paragraph(
        "To contextualize L2 SVR efficiency, we analyzed <b>1,049 verified liquidations on Ethereum L1</b> across Morpho Blue, Aave v3, Fluid, Spark, and Euler v2. "
        "We measured the priority payment transferred from searchers to block builders (`block.coinbase.transfer()`). The data reveals an extreme power-law distribution:<br/>"
        "• <b>Micro-Dust Majority:</b> In <b>848 of 1,049 events (80.84%)</b>, builder payments were strictly under <b>$1.00 USD</b>, with a median of <b>$0.08 USD</b> (p25: $0.012, p75: $0.56, p99: $2,639.23).<br/>"
        "• <b>Whale Concentration:</b> Total builder payments were $358,316.62 USD. The top 22 transactions accounted for <b>$344,155.62 (96.05%)</b> of all builder revenue. "
        "Aave v3 liquidations (133 events) accounted for $317,467.00. Routine liquidations on L1 generate negligible builder competition, whereas whale liquidations route exclusively through private builder bundles.",
        body_style
    ))

    # Section 7
    story.append(Paragraph("7. Methodological Scope, Limitations & Reproducibility", h1_style))
    story.append(Paragraph(
        "<b>Scope Boundaries:</b> (1) Base measurements reflect the acute volatility regime of October 12–19, 2026. (2) Realized solver net profit is lower than reported pre-swap margin "
        "due to DEX swap slippage and price impact. (3) L1 measurements quantify MEV-Boost priority payments to builders, not gross collateral volume.<br/>"
        "<b>Open Science Reproducibility:</b> The complete JSON dataset (1,157 records) and automated verification scripts are permanently archived on CERN Zenodo "
        "(DOI: 10.5281/zenodo.23623588, Record: 23623589) and mirrored on Hugging Face Datasets (pCwOrM/werracle-oev-liquidation-dataset-2026). "
        "Live network surveillance is open at https://radar.werracle.com. Executing `python scripts/verify_dataset_metrics.py` mechanically certifies all 15 core empirical invariants in under two seconds.",
        body_style
    ))

    # Acknowledgments
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=4))
    story.append(Paragraph("<b>Acknowledgments & Infrastructure Support:</b> High-throughput Bare-metal execution nodes, archival RPC connections, and 24/7 autonomous monitoring daemons were sponsored and maintained by <b>Bekirhan Dağlı</b> (Managing Partner) and <b>ITouch Systems Research & Development Desk</b> (Adana Çukurova Teknokent, Türkiye).", affil_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully built camera-ready PDF: {filename}")

if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    zenodo_pkg = os.path.join(base_dir, "..", "zenodo_oev_liquidation_package")
    ssrn_pkg = os.path.join(base_dir, "..", "ssrn_oev_liquidation_package")
    
    os.makedirs(zenodo_pkg, exist_ok=True)
    os.makedirs(ssrn_pkg, exist_ok=True)
    
    out_zenodo = os.path.join(zenodo_pkg, "Empirical_OEV_and_Liquidation_Dynamics_Research_Monograph.pdf")
    out_ssrn = os.path.join(ssrn_pkg, "Empirical_OEV_and_Liquidation_Dynamics_Research_Monograph.pdf")
    
    build_pdf(out_zenodo)
    import shutil
    shutil.copy2(out_zenodo, out_ssrn)
    print(f"Copied camera-ready PDF to SSRN package: {out_ssrn}")
