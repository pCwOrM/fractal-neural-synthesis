"""
Werracle & Werr Technology — Official Commercial Invoice PDF Generator
Issued by: ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK SANAYİ VE TİCARET LİMİTED ŞİRKETİ
Tax Office: Yüreğir V.D. | Tax ID (VKN): 4690944558 | MERSİS: 0469094455800001
Address: Balcalı Mah. Güney Kampüs/5 Sk. No: 4/1 İç Kapı No: 26 (Çukurova Teknokent), 01330 Sarıçam / Adana, Türkiye
Bank: TEB (Türk Ekonomi Bankası A.Ş.) — Adana Toros Şubesi (446) | SWIFT: TEBUTRIS
  • TRY IBAN: TR920003200000000070575465
  • USD IBAN: TR830003200000000088946748
  • EUR IBAN: TR280003200000000088946768
"""

import io
import os
import time
import hashlib
from typing import Dict, Any

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
LOGO_PATH = "/opt/apps/answerr/api/itouch_sys_logo_transparent.png"

TEB_BANK_ACCOUNTS = {
    "bank_name": "TEB (Türk Ekonomi Bankası A.Ş.) — Adana Toros Şubesi (446)",
    "account_holder": "ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK SANAYİ VE TİCARET LTD. ŞTİ.",
    "customer_no": "23764109",
    "swift_bic": "TEBUTRIS",
    "iban_try": "TR92 0003 2000 0000 0070 5754 65",
    "iban_usd": "TR83 0003 2000 0000 0088 9467 48",
    "iban_eur": "TR28 0003 2000 0000 0088 9467 68",
}

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
    Supports both PAID (verified on-chain / card / confirmed wire) and UNPAID (pending wire / proforma) stamps.
    """
    _ensure_fonts()
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4  # 595.27 x 841.89 pt

    is_paid = str(payment.get("status", "paid")).lower() in ("paid", "verified", "completed", "active")

    # Metadata
    inv_no = payment.get("invoice_no") or f"INV-{time.strftime('%Y', time.gmtime())}-{hashlib.sha256(str(payment.get('tx_hash', 'sample')).encode()).hexdigest()[:8].upper()}"
    c.setTitle(f"Commercial Invoice {inv_no} ({'PAID' if is_paid else 'UNPAID'}) - ITouch Systems / Werracle")
    c.setAuthor("ITouch Bilişim Sistemleri Ltd. Şti.")
    c.setSubject("Werracle / Werr Technology Commercial Invoice (%0 KDV Teknopark R&D Exemption)")

    # Top Accent Bar
    c.setFillColor(colors.HexColor("#0A1230"))
    c.rect(0, height - 10 * mm, width, 10 * mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#38BDF8" if is_paid else "#F59E0B"))
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
    c.setFont(_f("DejaVu-Bold"), 14.5)
    c.setFillColor(colors.HexColor("#0A1230"))
    c.drawRightString(width - 18 * mm, y_top + 8 * mm, "COMMERCIAL INVOICE" if is_paid else "COMMERCIAL INVOICE (PROFORMA)")
    c.setFont(_f("DejaVu"), 8)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawRightString(
        width - 18 * mm,
        y_top + 2.5 * mm,
        "TİCARİ FATURA / ÖDEME MAKBUZU (%0 KDV AR-GE)" if is_paid else "TİCARİ FATURA / ÖDEME BEKLEYEN TAHAKKUK (%0 KDV AR-GE)"
    )

    # PAID vs UNPAID Stamp Pill
    if is_paid:
        c.setFillColor(colors.HexColor("#DCFCE7"))
        c.setStrokeColor(colors.HexColor("#16A34A"))
        c.roundRect(width - 56 * mm, y_top - 6.5 * mm, 38 * mm, 6.5 * mm, 2 * mm, fill=1, stroke=1)
        c.setFont(_f("DejaVu-Bold"), 8.5)
        c.setFillColor(colors.HexColor("#15803D"))
        c.drawCentredString(width - 37 * mm, y_top - 4.5 * mm, "PAID / ÖDENDİ")
    else:
        c.setFillColor(colors.HexColor("#FEF3C7"))
        c.setStrokeColor(colors.HexColor("#D97706"))
        c.roundRect(width - 68 * mm, y_top - 6.5 * mm, 50 * mm, 6.5 * mm, 2 * mm, fill=1, stroke=1)
        c.setFont(_f("DejaVu-Bold"), 8)
        c.setFillColor(colors.HexColor("#B45309"))
        c.drawCentredString(width - 43 * mm, y_top - 4.5 * mm, "UNPAID / ÖDEME BEKLİYOR")

    # Divider Line
    y_cursor = y_top - 11.5 * mm
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.7)
    c.line(18 * mm, y_cursor, width - 18 * mm, y_cursor)

    # Seller & Invoice Meta Grid
    y_cursor -= 5.5 * mm
    c.setFont(_f("DejaVu-Bold"), 8)
    c.setFillColor(colors.HexColor("#0284C7"))
    c.drawString(18 * mm, y_cursor, "ISSUED BY (SELLER / SATICI KURUM)")
    c.drawString(width - 82 * mm, y_cursor, "INVOICE DETAILS (FATURA BİLGİLERİ)")

    y_cursor -= 4.3 * mm
    c.setFont(_f("DejaVu-Bold"), 8.2)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(18 * mm, y_cursor, "ITOUCH BİLİŞİM SİSTEMLERİ MÜHENDİSLİK DANIŞMANLIK")
    y_cursor -= 3.8 * mm
    c.drawString(18 * mm, y_cursor, "SANAYİ VE TİCARET LİMİTED ŞİRKETİ")

    c.setFont(_f("DejaVu"), 7.8)
    c.setFillColor(colors.HexColor("#334155"))
    seller_lines = [
        "Operating Brand: Werracle® & Werr® & Answerr® (ITouch Systems)",
        "Address: Balcalı Mah. Güney Kampüs/5 Sk. No: 4/1 İç Kapı No: 26",
        "Çukurova Teknokent, 01330 Sarıçam / Adana, Türkiye",
        "Tax Office & ID (VKN): Yüreğir V.D. — 4690944558  |  MERSİS: 0469094455800001",
        "KEP: itouchbilisim@hs01.kep.tr  |  Tel: +90 850 311 52 03",
        "Web: https://werracle.com • https://werr.io • https://answerr.me",
        "Contact: billing@werr.io • contact@werracle.com • ask@answerr.me"
    ]
    sy = y_cursor - 4.0 * mm
    for sl in seller_lines:
        c.drawString(18 * mm, sy, sl)
        sy -= 3.7 * mm

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
        ("Payment Status:", "PAID (VERIFIED)" if is_paid else "UNPAID (AWAITING VERIFICATION)")
    ]
    my = y_cursor + 3.5 * mm
    for k_lbl, v_val in meta_rows:
        c.setFont(_f("DejaVu"), 7.8)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(width - 82 * mm, my, k_lbl)
        c.setFont(_f("DejaVu-Bold"), 7.8)
        c.setFillColor(colors.HexColor("#15803D" if (k_lbl == "Payment Status:" and is_paid) else ("#B45309" if k_lbl == "Payment Status:" else "#0F172A")))
        c.drawRightString(width - 18 * mm, my, str(v_val)[:34])
        my -= 4.3 * mm

    # Buyer Block
    y_cursor = min(sy, my) - 3 * mm
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.roundRect(18 * mm, y_cursor - 24 * mm, width - 36 * mm, 26 * mm, 2 * mm, fill=1, stroke=1)

    by = y_cursor - 3.2 * mm
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
    buyer_tax = billing.get("tax_id") or "N/A (B2B Subscriber)"
    buyer_tax_office = billing.get("tax_office") or ""
    if buyer_tax_office:
        buyer_tax = f"{buyer_tax} ({buyer_tax_office})"
    buyer_addr = billing.get("address") or "Digital Delivery / Electronic API Provisioning"
    buyer_city_country = " / ".join(filter(None, [billing.get("city", ""), billing.get("country", "")]))
    if buyer_city_country:
        buyer_addr = f"{buyer_addr} — {buyer_city_country}"
    buyer_email = payment.get("email") or billing.get("email") or billing.get("invoice_email") or "-"
    payer_wallet = payment.get("payer_address") or "-"

    by -= 4.6 * mm
    c.setFont(_f("DejaVu-Bold"), 8.8)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(22 * mm, by, str(buyer_company)[:75])
    c.setFont(_f("DejaVu"), 7.8)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawRightString(width - 22 * mm, by, f"Email: {buyer_email}")

    by -= 4.2 * mm
    c.drawString(22 * mm, by, f"Contact / Authorized: {str(buyer_contact)[:55]}")
    c.drawRightString(width - 22 * mm, by, f"Tax ID / VKN: {str(buyer_tax)[:40]}")

    by -= 4.2 * mm
    c.drawString(22 * mm, by, f"Address: {str(buyer_addr)[:85]}")

    by -= 4.2 * mm
    c.setFont(_f("DejaVu-Mono"), 7.3)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(22 * mm, by, f"Payer Wallet / Account Ref: {payer_wallet}")

    # Line Items Table
    y_cursor = y_cursor - 30 * mm
    c.setFillColor(colors.HexColor("#0A1230"))
    c.rect(18 * mm, y_cursor - 6.8 * mm, width - 36 * mm, 6.8 * mm, fill=1, stroke=0)
    c.setFont(_f("DejaVu-Bold"), 7.8)
    c.setFillColor(colors.white)
    c.drawString(21 * mm, y_cursor - 4.7 * mm, "ITEM / DESCRIPTION (AR-GE YAZILIM HİZMETİ AÇIKLAMASI)")
    c.drawCentredString(width - 78 * mm, y_cursor - 4.7 * mm, "QTY")
    c.drawRightString(width - 48 * mm, y_cursor - 4.7 * mm, "UNIT PRICE")
    c.drawRightString(width - 21 * mm, y_cursor - 4.7 * mm, "TOTAL")

    tier = (payment.get("tier") or "pro").lower()
    product_title = payment.get("product_title") or (
        "Werracle B2B Risk Radar & OEV DaaS API — Institutional Curator Tier (30 Days)"
        if tier == "institutional" else
        "Werracle B2B Risk Radar & OEV DaaS API — Pro Researcher & Searcher Tier (30 Days)"
    )
    rate_limit = payment.get("rate_limit_per_min") or (3000 if tier == "institutional" else 600)
    product_subtitle = payment.get("product_subtitle") or f"Includes real-time Morpho Blue HF surveillance, SVR solver margins, Push Alerts & API access ({rate_limit} req/min)"
    amount_val = float(payment.get("amount_usdc") or (499.0 if tier == "institutional" else 149.0))
    net_val = amount_val

    row_y = y_cursor - 18.5 * mm
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.rect(18 * mm, row_y, width - 36 * mm, 11.7 * mm, fill=1, stroke=1)

    c.setFont(_f("DejaVu-Bold"), 8.2)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(21 * mm, row_y + 6.8 * mm, product_title[:68])
    c.setFont(_f("DejaVu"), 7.2)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(21 * mm, row_y + 2.4 * mm, product_subtitle[:95])

    c.setFont(_f("DejaVu"), 8.2)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawCentredString(width - 78 * mm, row_y + 4.6 * mm, "1")
    c.drawRightString(width - 48 * mm, row_y + 4.6 * mm, f"{net_val:,.2f} {currency}")
    c.setFont(_f("DejaVu-Bold"), 8.2)
    c.drawRightString(width - 21 * mm, row_y + 4.6 * mm, f"{net_val:,.2f} {currency}")

    # Totals Box & Tax Exemption Box
    tot_y = row_y - 21 * mm
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.roundRect(width - 96 * mm, tot_y, 78 * mm, 19 * mm, 2 * mm, fill=1, stroke=1)

    c.setFont(_f("DejaVu"), 7.8)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(width - 92 * mm, tot_y + 13.5 * mm, "Subtotal (Net):")
    c.drawRightString(width - 21 * mm, tot_y + 13.5 * mm, f"{net_val:,.2f} {currency}")

    c.drawString(width - 92 * mm, tot_y + 8.8 * mm, "KDV / VAT (0% — 3065 Geçici 20/1):")
    c.drawRightString(width - 21 * mm, tot_y + 8.8 * mm, f"0.00 {currency}")

    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(width - 92 * mm, tot_y + 6.5 * mm, width - 21 * mm, tot_y + 6.5 * mm)

    c.setFont(_f("DejaVu-Bold"), 9)
    c.setFillColor(colors.HexColor("#0A1230"))
    c.drawString(width - 92 * mm, tot_y + 2.0 * mm, "TOTAL PAID:" if is_paid else "TOTAL DUE:")
    c.setFillColor(colors.HexColor("#15803D" if is_paid else "#B45309"))
    c.drawRightString(width - 21 * mm, tot_y + 2.0 * mm, f"{amount_val:,.2f} {currency}")

    # Tax Exemption Legal Box (Left of Totals Box — strictly 4691 & 3065 Geçici 20/1 Teknopark R&D Exemption)
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.roundRect(18 * mm, tot_y, width - 118 * mm, 19 * mm, 2 * mm, fill=1, stroke=1)
    c.setFont(_f("DejaVu-Bold"), 7.3)
    c.setFillColor(colors.HexColor("#0284C7"))
    c.drawString(21 * mm, tot_y + 13.5 * mm, "TAX / VAT EXEMPTION (%0 KDV TEKNOPARK AR-GE İSTİSNASI)")
    c.setFont(_f("DejaVu"), 6.7)
    c.setFillColor(colors.HexColor("#475569"))
    c.drawString(21 * mm, tot_y + 9.0 * mm, "4691 s. Teknoloji Geliştirme Bölgeleri Kanunu ve 3065 s. KDV")
    c.drawString(21 * mm, tot_y + 5.0 * mm, "Kanunu Geçici 20/1 md. uyarınca Teknopark Ar-Ge yazılım")
    c.drawString(21 * mm, tot_y + 1.2 * mm, "teslim ve hizmetleri KDV'den müstesnadır (%0 KDV).")

    # Bank Accounts & Cryptographic Settlement Box
    ver_y = tot_y - 45 * mm
    c.setFillColor(colors.HexColor("#F0F9FF" if is_paid else "#FFFBEB"))
    c.setStrokeColor(colors.HexColor("#BAE6FD" if is_paid else "#FDE68A"))
    c.roundRect(18 * mm, ver_y, width - 36 * mm, 42 * mm, 2 * mm, fill=1, stroke=1)

    c.setFont(_f("DejaVu-Bold"), 7.8)
    c.setFillColor(colors.HexColor("#0369A1" if is_paid else "#B45309"))
    c.drawString(
        22 * mm,
        ver_y + 36.8 * mm,
        "SETTLEMENT & OFFICIAL BANK / TREASURY ACCOUNTS (ÖDEME DOĞRULAMA VE BANKA HESAPLARI)"
    )

    tx_hash = str(payment.get("tx_hash") or "-")
    recipient_addr = payment.get("recipient_address") or (
        "TLMhaDJTVYBHBSGJ9nCQGLvqnYFPsBgLJu (TRON TRC20)"
        if "trc20" in str(payment.get("network", "")).lower() or "trx" in str(payment.get("network", "")).lower()
        else "0x4945ef6e124eea2176ddf050b33db42b0ae8c7f7 (EVM Treasury)"
    )
    key_prefix = payment.get("key_prefix") or (f"wrk_{tier[:4]}_live_***" if is_paid else "PENDING PAYMENT VERIFICATION")

    c.setFont(_f("DejaVu-Mono"), 7.2)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(22 * mm, ver_y + 31.8 * mm, f"Transaction / Ref    : {tx_hash}")
    c.drawString(22 * mm, ver_y + 27.5 * mm, f"Settlement Channel   : {recipient_addr}")
    c.drawString(22 * mm, ver_y + 23.2 * mm, f"API Key Provisioning : {key_prefix} ({'Active' if is_paid else 'Issued upon payment confirmation'})")

    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(22 * mm, ver_y + 20.5 * mm, width - 22 * mm, ver_y + 20.5 * mm)

    c.setFont(_f("DejaVu-Bold"), 7.2)
    c.setFillColor(colors.HexColor("#0F172A"))
    c.drawString(22 * mm, ver_y + 16.5 * mm, "Official Bank Wire / EFT Accounts — TEB (Türk Ekonomi Bankası A.Ş., Adana Toros Şb. 446, SWIFT: TEBUTRIS):")
    c.setFont(_f("DejaVu-Mono"), 7.1)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(22 * mm, ver_y + 12.2 * mm, "TRY (TL) IBAN : TR92 0003 2000 0000 0070 5754 65  (Acc No: 70575465 | Customer No: 23764109)")
    c.drawString(22 * mm, ver_y + 8.0 * mm,  "USD ($)  IBAN : TR83 0003 2000 0000 0088 9467 48  (Acc No: 88946748 | SWIFT/BIC: TEBUTRIS)")
    c.drawString(22 * mm, ver_y + 3.8 * mm,  "EUR (€)  IBAN : TR28 0003 2000 0000 0088 9467 68  (Acc No: 88946768 | Beneficiary: ITOUCH BİLİŞİM SİSTEMLERİ LTD. ŞTİ.)")

    # Corporate Governance & Legal Footer
    foot_y = 22 * mm
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(18 * mm, foot_y + 11 * mm, width - 18 * mm, foot_y + 11 * mm)

    c.setFont(_f("DejaVu-Bold"), 7.2)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(18 * mm, foot_y + 6.8 * mm, "CORPORATE & INTELLECTUAL PROPERTY GOVERNANCE NOTICE:")
    c.setFont(_f("DejaVu"), 6.7)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(18 * mm, foot_y + 3.0 * mm, "• Commercial Operating Entity: ITouch Bilişim Sistemleri Ltd. Şti. (Partners: Volkan Dağlı [Major Partner & CTO] & Bekirhan Dağlı [Partner]).")
    c.drawString(18 * mm, foot_y - 0.6 * mm, "• Exclusive Commercial IP & Trademarks (Werr®, Werracle®, Answerr®): Held and operated exclusively by ITouch Bilişim Sistemleri Ltd. Şti.")
    c.drawString(18 * mm, foot_y - 4.2 * mm, "• Official e-Fatura / e-Arşiv Invoice is issued under Law No. 4691 & KDV Law No. 3065 Temp. Art. 20/1 (%0 KDV) upon verified payment.")

    c.showPage()
    c.save()
    return buf.getvalue()
