"""
Werracle & Werr Technology — Official Commercial Invoice PDF Generator
Issued by: ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK SANAYİ VE TİCARET LİMİTED ŞİRKETİ
Tax Office: Yüreğir V.D. | Tax ID (VKN): 4690944558 | MERSİS: 0469094455800001
Address: Balcalı Mah. Güney Kampüs/5 Sk. No: 4/1 İç Kapı No: 26 (Çukurova Teknokent), 01330 Sarıçam / Adana, Türkiye
"""

import io
import os
import time
import hashlib
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
LOGO_PATH = "/opt/apps/answerr/api/itouch_sys_logo_transparent.png"

_FONTS_REGISTERED = False


def _ensure_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    try:
        pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
        pdfmetrics.registerFont(TTFont("DejaVu-Mono", os.path.join(FONT_DIR, "DejaVuSansMono.ttf")))
        _FONTS_REGISTERED = True
    except Exception:
        pass


def _f(name: str) -> str:
    if not _FONTS_REGISTERED:
        return {"DejaVu": "Helvetica", "DejaVu-Bold": "Helvetica-Bold", "DejaVu-Mono": "Courier"}.get(name, "Helvetica")
    return name


def generate_commercial_invoice_pdf(payment: Dict[str, Any]) -> bytes:
    """
    Generates an official A4 Commercial Invoice PDF in memory and returns raw PDF bytes.
    """
    _ensure_fonts()
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4  # 595.27 x 841.89 pt

    # Metadata
    inv_no = payment.get("invoice_no") or f"INV-{time.strftime('%Y', time.gmtime())}-{hashlib.sha256(str(payment.get('tx_hash', 'sample')).encode()).hexdigest()[:8].upper()}"
    c.setTitle(f"Commercial Invoice {inv_no} - ITouch Systems / Werracle")
    c.setAuthor("ITouch Bilişim Sistemleri Ltd. Şti.")
    c.setSubject("Werracle / Werr Technology Commercial Invoice")

    # Top Accent Bar
    c.setFillColor(colors.HexColor("#0A1230"))
    c.rect(0, height - 10 * mm, width, 10 * mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#38BDF8"))
    c.rect(0, height - 11.2 * mm, width, 1.2 * mm, fill=1, stroke=0)

    # Logo & Header
    y_top = height - 28 * mm
    if os.path.exists(LOGO_PATH):
        try:
            img = ImageReader(LOGO_PATH)
            iw, ih = img.getSize()
            aspect = iw / float(ih)
            target_h = 15 * mm
            target_w = target_h * aspect
            c.drawImage(img, 18 * mm, y_top - 2 * mm, width=target_w, height=target_h, mask="auto")
        except Exception:
            pass

    # Document Title (Right aligned)
    c.setFont(_f("DejaVu-Bold"), 15)
    c.setFillColor(colors.HexColor("#0A1230"))
    c.drawRightString(width - 18 * mm, y_top + 8 * mm, "COMMERCIAL INVOICE")
    c.setFont(_f("DejaVu"), 8.5)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawRightString(width - 18 * mm, y_top + 2.5 * mm, "TİCARİ FATURA / ÖDEME MAKBUZU (B2B DaaS & SaaS)")

    # Paid Stamp Pill
    c.setFillColor(colors.HexColor("#DCFCE7"))
    c.setStrokeColor(colors.HexColor("#16A34A"))
    c.roundRect(width - 52 * mm, y_top - 6.5 * mm, 34 * mm, 6.5 * mm, 2 * mm, fill=1, stroke=1)
    c.setFont(_f("DejaVu-Bold"), 8.5)
    c.setFillColor(colors.HexColor("#15803D"))
    c.drawCentredString(width - 35 * mm, y_top - 4.5 * mm, "PAID / ÖDENDİ")

    # Divider Line
    y_cursor = y_top - 12 * mm
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.7)
    c.line(18 * mm, y_cursor, width - 18 * mm, y_cursor)

    # Seller & Invoice Meta Grid
    y_cursor -= 6 * mm
    c.setFont(_f("DejaVu-Bold"), 8)
    c.setFillColor(colors.HexColor("#0284C7"))
    c.drawString(18 * mm, y_cursor, "ISSUED BY (SELLER / SATICI KURUM)")
    c.drawString(width - 82 * mm, y_cursor, "INVOICE DETAILS (FATURA BİLGİLERİ)")

    y_cursor -= 4.5 * mm
    c.setFont(_f("DejaVu-Bold"), 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(18 * mm, y_cursor, "ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK")
    y_cursor -= 4 * mm
    c.drawString(18 * mm, y_cursor, "SANAYİ VE TİCARET LİMİTED ŞİRKETİ")

    c.setFont(_f("DejaVu"), 8)
    c.setFillColor(colors.HexColor("#334155"))
    seller_lines = [
        "Operating Brand: Werracle & Werr Technology (ITouch Systems)",
        "Address: Balcalı Mah. Güney Kampüs/5 Sk. No: 4/1 İç Kapı No: 26",
        "Çukurova Teknokent, 01330 Sarıçam / Adana, Türkiye",
        "Tax Office & ID (VKN): Yüreğir V.D. — 4690944558",
        "MERSİS No: 0469094455800001  |  KEP: itouchbilisim@hs01.kep.tr",
        "Web: https://werracle.com • https://werr.io  |  Tel: +90 850 311 52 03",
        "Contact: billing@werr.io • contact@werracle.com • ask@answerr.me"
    ]
    sy = y_cursor - 4.2 * mm
    for sl in seller_lines:
        c.drawString(18 * mm, sy, sl)
        sy -= 3.9 * mm

    # Right side: Invoice Meta Box
    claimed_ts = float(payment.get("claimed_at") or time.time())
    expires_ts = float(payment.get("expires_at") or (claimed_ts + 30 * 86400))
    issue_utc = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(claimed_ts))
    period_str = f"{time.strftime('%Y-%m-%d', time.gmtime(claimed_ts))} to {time.strftime('%Y-%m-%d', time.gmtime(expires_ts))}"
    method_label = payment.get("payment_method") or f"On-Chain Crypto ({payment.get('network', 'Base Mainnet').upper()})"
    currency = payment.get("currency") or "USDC"

    meta_rows = [
        ("Invoice Number:", inv_no),
        ("Issue Date:", issue_utc),
        ("Service Period:", period_str),
        ("Payment Method:", method_label),
        ("Settlement Asset:", currency),
        ("Payment Status:", "PAID IN FULL (VERIFIED)")
    ]
    my = y_cursor + 3.5 * mm
    for k_lbl, v_val in meta_rows:
        c.setFont(_f("DejaVu"), 8)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(width - 82 * mm, my, k_lbl)
        c.setFont(_f("DejaVu-Bold"), 8)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawRightString(width - 18 * mm, my, str(v_val)[:34])
        my -= 4.5 * mm

    # Buyer Block
    y_cursor = min(sy, my) - 4 * mm
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.roundRect(18 * mm, y_cursor - 26 * mm, width - 36 * mm, 28 * mm, 2 * mm, fill=1, stroke=1)

    by = y_cursor - 3.5 * mm
    c.setFont(_f("DejaVu-Bold"), 8)
    c.setFillColor(colors.HexColor("#0284C7"))
    c.drawString(22 * mm, by, "BILLED TO (BUYER / ALICI KURUM BİLGİLERİ)")

    billing = payment.get("billing") or {}
    if isinstance(billing, str):
        try:
            import json
            billing = json.loads(billing)
        except Exception:
            billing = {}

    buyer_company = billing.get("company") or billing.get("legal_name") or payment.get("buyer_company") or "Valued B2B API Subscriber"
    buyer_contact = billing.get("contact_name") or payment.get("email") or "-"
    buyer_tax = billing.get("tax_id") or "N/A (International / Web3 B2B)"
    buyer_tax_office = billing.get("tax_office") or ""
    if buyer_tax_office:
        buyer_tax = f"{buyer_tax} ({buyer_tax_office})"
    buyer_addr = billing.get("address") or "Digital Delivery / Electronic API Provisioning"
    buyer_city_country = " / ".join(filter(None, [billing.get("city", ""), billing.get("country", "")]))
    if buyer_city_country:
        buyer_addr = f"{buyer_addr} — {buyer_city_country}"
    buyer_email = payment.get("email") or billing.get("email") or billing.get("invoice_email") or "-"
    payer_wallet = payment.get("payer_address") or "-"

    by -= 5 * mm
    c.setFont(_f("DejaVu-Bold"), 9)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(22 * mm, by, str(buyer_company)[:75])
    c.setFont(_f("DejaVu"), 8)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawRightString(width - 22 * mm, by, f"Email: {buyer_email}")

    by -= 4.5 * mm
    c.drawString(22 * mm, by, f"Contact / Authorized: {buyer_contact[:55]}")
    c.drawRightString(width - 22 * mm, by, f"Tax ID / VAT No: {buyer_tax[:40]}")

    by -= 4.5 * mm
    c.drawString(22 * mm, by, f"Address: {buyer_addr[:85]}")

    by -= 4.5 * mm
    c.setFont(_f("DejaVu-Mono"), 7.5)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(22 * mm, by, f"Payer Wallet / Account Ref: {payer_wallet}")

    # Line Items Table
    y_cursor = y_cursor - 33 * mm
    c.setFillColor(colors.HexColor("#0A1230"))
    c.rect(18 * mm, y_cursor - 7 * mm, width - 36 * mm, 7 * mm, fill=1, stroke=0)
    c.setFont(_f("DejaVu-Bold"), 8)
    c.setFillColor(colors.white)
    c.drawString(21 * mm, y_cursor - 4.8 * mm, "ITEM / DESCRIPTION (HİZMET AÇIKLAMASI)")
    c.drawCentredString(width - 78 * mm, y_cursor - 4.8 * mm, "QTY")
    c.drawRightString(width - 48 * mm, y_cursor - 4.8 * mm, "UNIT PRICE")
    c.drawRightString(width - 21 * mm, y_cursor - 4.8 * mm, "TOTAL")

    tier = (payment.get("tier") or "pro").lower()
    product_title = payment.get("product_title") or (
        "Werracle B2B Risk Radar & OEV DaaS API — Institutional Curator Tier (30 Days)"
        if tier == "institutional" else
        "Werracle B2B Risk Radar & OEV DaaS API — Pro Researcher & Searcher Tier (30 Days)"
    )
    rate_limit = payment.get("rate_limit_per_min") or (3000 if tier == "institutional" else 600)
    amount_val = float(payment.get("amount_usdc") or (499.0 if tier == "institutional" else 149.0))
    vat_val = float(payment.get("vat_amount") or 0.0)
    net_val = float(payment.get("net_amount") or (amount_val - vat_val))

    row_y = y_cursor - 19 * mm
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.rect(18 * mm, row_y, width - 36 * mm, 12 * mm, fill=1, stroke=1)

    c.setFont(_f("DejaVu-Bold"), 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(21 * mm, row_y + 7 * mm, product_title[:68])
    c.setFont(_f("DejaVu"), 7.5)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(21 * mm, row_y + 2.5 * mm, f"Includes real-time Morpho Blue HF surveillance, SVR solver margins & API access ({rate_limit} req/min)")

    c.setFont(_f("DejaVu"), 8.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawCentredString(width - 78 * mm, row_y + 4.8 * mm, "1")
    c.drawRightString(width - 48 * mm, row_y + 4.8 * mm, f"{net_val:,.2f} {currency}")
    c.setFont(_f("DejaVu-Bold"), 8.5)
    c.drawRightString(width - 21 * mm, row_y + 4.8 * mm, f"{net_val:,.2f} {currency}")

    # Totals Box
    tot_y = row_y - 22 * mm
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(width - 90 * mm, tot_y, 72 * mm, 20 * mm, 2 * mm, fill=1, stroke=1)

    c.setFont(_f("DejaVu"), 8)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(width - 86 * mm, tot_y + 14 * mm, "Subtotal (Net):")
    c.drawRightString(width - 21 * mm, tot_y + 14 * mm, f"{net_val:,.2f} {currency}")

    vat_label = "VAT / KDV (20%):" if vat_val > 0 else "VAT / Tax (Export / Web3 0%):"
    c.drawString(width - 86 * mm, tot_y + 9 * mm, vat_label)
    c.drawRightString(width - 21 * mm, tot_y + 9 * mm, f"{vat_val:,.2f} {currency}")

    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(width - 86 * mm, tot_y + 6.8 * mm, width - 21 * mm, tot_y + 6.8 * mm)

    c.setFont(_f("DejaVu-Bold"), 9.5)
    c.setFillColor(colors.HexColor("#0A1230"))
    c.drawString(width - 86 * mm, tot_y + 2.2 * mm, "TOTAL PAID:")
    c.setFillColor(colors.HexColor("#15803D"))
    c.drawRightString(width - 21 * mm, tot_y + 2.2 * mm, f"{amount_val:,.2f} {currency}")

    # Cryptographic & Settlement Verification Box
    ver_y = tot_y - 32 * mm
    c.setFillColor(colors.HexColor("#F0F9FF"))
    c.setStrokeColor(colors.HexColor("#BAE6FD"))
    c.roundRect(18 * mm, ver_y, width - 36 * mm, 28 * mm, 2 * mm, fill=1, stroke=1)

    c.setFont(_f("DejaVu-Bold"), 8)
    c.setFillColor(colors.HexColor("#0369A1"))
    c.drawString(22 * mm, ver_y + 22.5 * mm, "CRYPTOGRAPHIC & SETTLEMENT VERIFICATION (ÖDEME DOĞRULAMA KAYDI)")

    tx_hash = str(payment.get("tx_hash") or "-")
    recipient_addr = payment.get("recipient_address") or (
        "TLMhaDJTVYBHBSGJ9nCQGLvqnYFPsBgLJu (TRON TRC20)"
        if "trc20" in str(payment.get("network", "")).lower() or "trx" in str(payment.get("network", "")).lower()
        else "0x4945ef6e124eea2176ddf050b33db42b0ae8c7f7 (EVM Treasury)"
    )
    key_prefix = payment.get("key_prefix") or f"wrk_{tier[:4]}_live_***"

    c.setFont(_f("DejaVu-Mono"), 7.5)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(22 * mm, ver_y + 17 * mm, f"Transaction Hash / Ref : {tx_hash}")
    c.drawString(22 * mm, ver_y + 12 * mm, f"Treasury / Merchant    : {recipient_addr}")
    c.drawString(22 * mm, ver_y + 7 * mm,  f"Provisioned API Key    : {key_prefix} (Active for 30 days, {rate_limit} req/min)")
    c.drawString(22 * mm, ver_y + 2.2 * mm, f"Verification Timestamp : {issue_utc} (Verified On-Chain / Gateway)")

    # Corporate Governance & Legal Footer
    foot_y = 26 * mm
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(18 * mm, foot_y + 12 * mm, width - 18 * mm, foot_y + 12 * mm)

    c.setFont(_f("DejaVu-Bold"), 7.5)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(18 * mm, foot_y + 7.5 * mm, "CORPORATE & INTELLECTUAL PROPERTY GOVERNANCE NOTICE:")
    c.setFont(_f("DejaVu"), 7)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(18 * mm, foot_y + 3.5 * mm, "• Commercial Operating Entity: ITouch Bilişim Sistemleri Ltd. Şti. (Partners: Volkan Dağlı [Major Partner & CTO] & Bekirhan Dağlı [Partner]).")
    c.drawString(18 * mm, foot_y - 0.2 * mm, "• Exclusive Commercial IP & Trademarks (Werr®, Werracle®, Answerr®): Held and operated exclusively by ITouch Bilişim Sistemleri Ltd. Şti.")
    c.drawString(18 * mm, foot_y - 3.9 * mm, "• Patent Filings (TÜRKPATENT TR 2026/016285 & TR 2026/016633): Commercialized under exclusive licensing power of attorney held by Volkan Dağlı.")
    c.drawString(18 * mm, foot_y - 7.6 * mm, "• This computer-generated Commercial Invoice is valid without a wet signature. For tax/accounting inquiries: billing@werr.io")

    c.showPage()
    c.save()
    return buf.getvalue()
