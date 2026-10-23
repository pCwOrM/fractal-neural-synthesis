import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions: 1200 x 628 (Standard LinkedIn Landscape 1.91:1)
W, H = 1200, 628
img = Image.new("RGBA", (W, H), "#07061a")
draw = ImageDraw.Draw(img)

# Load Fonts from Windows
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
font_brand = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28)
font_h2 = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_mono = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
font_mono_bold = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)
font_tag = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 10)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)

# Helper function to wrap text
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# 1. Background accents (Subtle radial glow in top-left and right)
# Left glow
for r in range(250, 0, -5):
    alpha = int(18 * (1 - r / 250))
    glow_color = (42, 39, 96, alpha)
    draw.ellipse((100 - r, 200 - r, 100 + r, 200 + r), fill=glow_color)

# 2. Left Column Container
# Left column: x from 30 to 390 (width 360)
draw.rounded_rectangle((30, 25, 390, 595), radius=16, fill="#0c0a24", outline="#2a2760", width=1)

# Place Werracle Logo in Left Column
logo_path = r"C:\Users\maat\Documents\antigravity\werracle\assets\werracle_logo_oracle_trans.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = 200
    logo_thumb = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    # Center horizontally in left container: (390 - 30) = 360. Center = 30 + 180 = 210.
    logo_x = int(210 - (logo_size / 2))
    logo_y = 50
    img.paste(logo_thumb, (logo_x, logo_y), logo_thumb)

# Brand texts below logo
draw.text((210, 268), "WERRACLE", fill="#ffffff", font=font_brand, anchor="mt")
draw.text((210, 305), "Decisions a blockchain can check.", fill="#ffc857", font=font_sub, anchor="mt")
draw.text((210, 323), "In 32 bytes.", fill="#ffc857", font=font_h2, anchor="mt")

# Badge Pills in Left Column
# Pill 1: Zero-Storage EVM Core
draw.rounded_rectangle((65, 355, 355, 385), radius=15, fill="#131038", outline="#4a5cff", width=1)
draw.text((210, 370), "⚡ One bytes32 Slot • ~20.7k Gas", fill="#9fe8ff", font=font_mono_bold, anchor="mm")

# Pill 2: Lean 4 Formally Verified
draw.rounded_rectangle((65, 395, 355, 425), radius=15, fill="#131038", outline="#10b981", width=1)
draw.text((210, 410), "🛡️ Lean 4 Kernel • 0 Sorry", fill="#7cf5c4", font=font_mono_bold, anchor="mm")

# Pill 3: Live SVR Risk Radar
draw.rounded_rectangle((65, 435, 355, 465), radius=15, fill="#131038", outline="#ffc857", width=1)
draw.text((210, 450), "🛰️ 83 Morpho Markets • 98.1% Recaptured", fill="#ffc857", font=font_mono_bold, anchor="mm")

# URLs at bottom of Left Column
draw.line((50, 485, 370, 485), fill="#2a2760", width=1)
draw.text((210, 502), "radar.werracle.com", fill="#7cf5c4", font=font_mono_bold, anchor="mm")
draw.text((210, 524), "werracle.com  |  werracle.io", fill="#a7a2cf", font=font_mono, anchor="mm")
draw.text((210, 546), "pCwOrM / werracle (GitHub)", fill="#6b7280", font=font_mono, anchor="mm")
draw.text((210, 570), "ITOUCH SYSTEMS | TEKNOKENT", fill="#38bdf8", font=font_tag, anchor="mm")

# 3. Right Column: Top Header Banner
# Right column: x from 415 to 1170 (width 755)
draw.rounded_rectangle((415, 25, 1170, 115), radius=14, fill="#0c0a24", outline="#2a2760", width=1)

# Header tags & titles
draw.text((435, 42), "ITOUCH SYSTEMS | OFFICIAL ANNOUNCEMENT", fill="#ffc857", font=font_tag)
draw.text((1150, 42), "Adana Çukurova Technopark  •  arXiv:2609.30719", fill="#9fe8ff", font=font_mono, anchor="ra")
draw.text((435, 62), "Werracle: Zero-Storage On-Chain AI Oracle", fill="#ffffff", font=font_title)
draw.text((435, 93), "The first EVM decision model packed entirely into 32 bytes, verified in Lean 4, with live OEV radar.", fill="#a7a2cf", font=font_body)

# 4. Right Column: 4 Capability Cards
cards = [
    {
        "y": 128,
        "h": 105,
        "tag": "01 | ZERO-STORAGE EVM ARCHITECTURE",
        "tag_color": "#ffc857",
        "badge": "32 Bytes Slot",
        "badge_border": "#ffc857",
        "title": "One bytes32 Storage Word & ~20.7k Execution Gas",
        "desc": "Stores no heavy neural weight matrices; evaluates deterministic decision boundaries derived directly from Mandelbrot set dynamics. Executes intra-block inside the exact transaction it guards."
    },
    {
        "y": 243,
        "h": 105,
        "tag": "02 | FORMAL VERIFICATION & MATHEMATICAL CERTAINTY",
        "tag_color": "#7cf5c4",
        "badge": "Lean 4 Certified",
        "badge_border": "#10b981",
        "title": "40 Machine-Checked Theorems (Zero Sorry)",
        "desc": "Verified by the Lean 4 kernel with zero non-standard axioms: every escape loop provably halts, Q16.16 fixed-point arithmetic never overflows, and execution gas stays strictly below ceiling."
    },
    {
        "y": 358,
        "h": 115,
        "tag": "03 | EMPIRICAL DEFI RESEARCH & LIVE RISK OBSERVATORY",
        "tag_color": "#9fe8ff",
        "badge": "98.10% Recapture",
        "badge_border": "#38bdf8",
        "title": "83 Morpho Markets Monitored & 105 Audited SVR Events",
        "desc": "Live 24/7 sub-second surveillance on Base. Multi-call decoding of 105 Chainlink SVR liquidations ($190.5k gross) independently proved 98.10% ($186.9k) returned to depositors, compressing solver margins to -1.55%."
    },
    {
        "y": 483,
        "h": 102,
        "tag": "04 | INTELLECTUAL PROPERTY & OPEN RESEARCH CORPUS",
        "tag_color": "#c084fc",
        "badge": "Patents & Preprints",
        "badge_border": "#a855f7",
        "title": "2 Patent Applications, arXiv, SSRN & CERN Zenodo",
        "desc": "TÜRKPATENT patent filings TR 2026/016285 and TR 2026/016633. Full open-source implementation across Solidity, Cairo, and Lean 4 packages available for academic and DeFi integration."
    }
]

for c in cards:
    y = c["y"]
    h = c["h"]
    # Card box
    draw.rounded_rectangle((415, y, 1170, y + h), radius=10, fill="#0f0d2b", outline="#2a2760", width=1)
    
    # Tag on top-left of card
    draw.text((435, y + 10), c["tag"], fill=c["tag_color"], font=font_tag)
    
    # Badge on top-right of card
    badge_bbox = draw.textbbox((0, 0), c["badge"], font=font_tag)
    bw = badge_bbox[2] - badge_bbox[0] + 16
    draw.rounded_rectangle((1150 - bw, y + 8, 1150, y + 24), radius=6, fill="#1a1840", outline=c["badge_border"], width=1)
    draw.text((1150 - bw + 8, y + 12), c["badge"], fill=c["tag_color"], font=font_tag)
    
    # Title
    draw.text((435, y + 28), c["title"], fill="#ffffff", font=font_h2)
    
    # Description (wrapped)
    lines = wrap_text(c["desc"], font_body, max_width=715)
    line_y = y + 50
    for line in lines:
        draw.text((435, line_y), line, fill="#a7a2cf", font=font_body)
        line_y += 16

# Footer bar across bottom
draw.line((30, 608, 1170, 608), fill="#1f1c48", width=1)
draw.text((35, 614), "ITOUCH SYSTEMS BILISIM VE ILETISIM SAN. TIC. LTD. STI. • Çukurova Teknokent, Adana", fill="#6b7280", font=font_tag)
draw.text((1165, 614), "Open Infrastructure • Verified Metrics • Production Ready", fill="#10b981", font=font_tag, anchor="ra")

out_file = "itouch_linkedin_werracle_clean_en.png"
img.save(out_file, "PNG", quality=100)
print(f"Saved clean English social card to: {out_file} ({img.size})")
