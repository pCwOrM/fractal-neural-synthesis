import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# 1. Render Matplotlib background card at 1920x1080
fig = plt.figure(figsize=(12.8, 7.2), dpi=150, facecolor='#07061a')
ax = fig.add_subplot(111)
ax.set_facecolor('#07061a')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Header Box
header_box = patches.FancyBboxPatch((3, 85), 94, 12, boxstyle="round,pad=1.0",
                                    fc='#0f0d2b', ec='#2a2760', lw=1.8)
ax.add_patch(header_box)

ax.text(5.5, 93.2, "ITOUCH SYSTEMS | DEEP TECH & WEB3 INFRASTRUCTURE",
        ha='left', va='center', color='#ffc857', fontsize=11, weight='bold', fontfamily='sans-serif')
ax.text(5.5, 88.5, "Werracle: Zero-Storage On-Chain AI Decision Oracle & OEV Risk Observatory",
        ha='left', va='center', color='#ffffff', fontsize=14, weight='bold', fontfamily='sans-serif')
ax.text(94.5, 90.8, "Adana Cukurova Technopark\narXiv: 2609.30719",
        ha='right', va='center', color='#9fe8ff', fontsize=10, weight='bold', fontfamily='monospace')

# Brand Title and details in Left Column
ax.text(19, 36.5, "WERRACLE",
        ha='center', va='center', color='#ffffff', fontsize=25, weight='bold', fontfamily='sans-serif')
ax.text(19, 31.5, "Decisions a blockchain can check. In 32 bytes.",
        ha='center', va='center', color='#ffc857', fontsize=10.5, style='italic', fontfamily='sans-serif')
ax.text(19, 26.5, "werracle.com  |  radar.werracle.com",
        ha='center', va='center', color='#7cf5c4', fontsize=11, weight='bold', fontfamily='monospace')
ax.text(19, 21.5, "werracle.io (Simulator) | werr.io (Corpus)",
        ha='center', va='center', color='#a7a2cf', fontsize=9.5, fontfamily='monospace')

# Vertical dashed divider line
line = patches.ConnectionPatch((36, 12), (36, 80), "data", "data",
                              color='#2a2760', lw=1.5, linestyle='--')
ax.add_patch(line)

# Right Column: 4 Capability Cards in English
cards_data = [
    {
        "y": 66,
        "tag": "01 | ZERO-STORAGE EVM ARCHITECTURE",
        "tag_color": "#ffc857",
        "title": "32-Byte Storage Slot & ~20.7k Execution Gas",
        "desc": "No stored weight matrices; decisions derive deterministically from Mandelbrot dynamics in one EVM word. Sub-cent intra-block execution inside the same call it guards.",
        "badge": "One bytes32 Slot"
    },
    {
        "y": 48.5,
        "tag": "02 | FORMAL VERIFICATION & ZERO AXIOMS",
        "tag_color": "#7cf5c4",
        "title": "40 Theorems Machine-Checked in Lean 4",
        "desc": "Loop termination guaranteed, Q16.16 fixed-point arithmetic never overflows int64, execution gas ceiling provably bounded. Zero 'sorry', verified proof certificate.",
        "badge": "Lean 4 Certified"
    },
    {
        "y": 31,
        "tag": "03 | EMPIRICAL DEFI & OEV OBSERVATORY",
        "tag_color": "#9fe8ff",
        "title": "83 Morpho Markets & 98.10% SVR Recapture",
        "desc": "105 audited multi-call SVR events on Base L2 ($190.5k gross): Chainlink SVR redirected 98.10% back to depositors, compressing solver margins to -1.55% pre-swap.",
        "badge": "Live Observatory"
    },
    {
        "y": 13.5,
        "tag": "04 | INTELLECTUAL PROPERTY & OPEN RESEARCH",
        "tag_color": "#c084fc",
        "title": "2 Patent Applications, arXiv, SSRN & Zenodo",
        "desc": "TURKPATENT patent filings TR 2026/016285 & TR 2026/016633. Complete open-source corpus across Solidity, Cairo, and Lean 4 libraries.",
        "badge": "Patents & Preprints"
    }
]

for card in cards_data:
    y = card["y"]
    card_patch = patches.FancyBboxPatch((39, y), 58, 14.5, boxstyle="round,pad=0.8",
                                        fc='#0f0d2b', ec='#2a2760', lw=1.2)
    ax.add_patch(card_patch)
    
    ax.text(40.5, y + 11.5, card["tag"],
            ha='left', va='center', color=card["tag_color"], fontsize=8.5, weight='bold', fontfamily='monospace')
    
    ax.text(95.5, y + 11.5, card["badge"],
            ha='right', va='center', color=card["tag_color"], fontsize=8, weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#1a1840', ec=card["tag_color"], lw=0.8))
    
    ax.text(40.5, y + 7.2, card["title"],
            ha='left', va='center', color='#ffffff', fontsize=11.5, weight='bold', fontfamily='sans-serif')
    
    ax.text(40.5, y + 2.8, card["desc"],
            ha='left', va='center', color='#a7a2cf', fontsize=9.2, fontfamily='sans-serif')

# Footer Bar
footer_box = patches.FancyBboxPatch((3, 2), 94, 6.5, boxstyle="round,pad=0.6",
                                    fc='#0a0820', ec='#1a1840', lw=1.0)
ax.add_patch(footer_box)

ax.text(5.5, 5.2, "ITOUCH SYSTEMS | BILISIM VE ILETISIM SAN. TIC. LTD. STI.",
        ha='left', va='center', color='#ffffff', fontsize=9.5, weight='bold', fontfamily='sans-serif')
ax.text(5.5, 3.2, "Cukurova Technopark, Adana, Turkey | itouch.com.tr | werracle.com | werr.io",
        ha='left', va='center', color='#a7a2cf', fontsize=8.5, fontfamily='sans-serif')
ax.text(94.5, 4.2, "Open Source: pCwOrM/werracle | EVM | Base L2 | Arbitrum | Lean 4",
        ha='right', va='center', color='#7cf5c4', fontsize=9, weight='bold', fontfamily='monospace')

temp_bg = "temp_linkedin_bg.png"
plt.tight_layout()
plt.savefig(temp_bg, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

# 2. Pixel-Perfect PIL Compositing for Logo (1:1 Exact Aspect Ratio)
bg_img = Image.open(temp_bg)
logo_path = r"C:\Users\maat\Documents\antigravity\werracle\assets\werracle_logo_oracle_trans.png"
logo_img = Image.open(logo_path).convert("RGBA")

# Desired logo size on 1920x1080 canvas: exactly square (400x400 pixels)
logo_size = 380
logo_resized = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

# Position: center horizontally in left column
# Left column occupies X pixels ~ 50 to 650 (center ~ 350)
# Top coord in 1080 canvas: Y coords ~ 220 to 600
logo_x = int(350 - (logo_size / 2))
logo_y = 210

# Paste logo using alpha channel as mask
bg_img.paste(logo_resized, (logo_x, logo_y), logo_resized)

final_card = "itouch_linkedin_werracle_en.png"
bg_img.save(final_card, "PNG", quality=95)
print(f"Successfully generated pixel-perfect English card: {final_card} ({bg_img.size})")
