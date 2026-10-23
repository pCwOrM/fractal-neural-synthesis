import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

# Canvas size 1920x1080 at 150 dpi (High-Resolution 16:9 for LinkedIn)
fig = plt.figure(figsize=(12.8, 7.2), dpi=150, facecolor='#07061a')
ax = fig.add_subplot(111)
ax.set_facecolor('#07061a')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# 1. Top Header Banner
header_box = patches.FancyBboxPatch((3, 85), 94, 12, boxstyle="round,pad=1.0",
                                    fc='#0f0d2b', ec='#2a2760', lw=1.8)
ax.add_patch(header_box)

ax.text(5.5, 93.2, "ITOUCH SYSTEMS | RESMI DUYURU & AR-GE BILDIRISI",
        ha='left', va='center', color='#ffc857', fontsize=11, weight='bold', fontfamily='sans-serif')
ax.text(5.5, 88.5, "Werracle: EVM Icin Sifir Depolamali Yapay Zeka Kahini ve OEV Risk Radar",
        ha='left', va='center', color='#ffffff', fontsize=15, weight='bold', fontfamily='sans-serif')
ax.text(94.5, 90.8, "Adana Cukurova Teknokent\narXiv: 2609.30719",
        ha='right', va='center', color='#9fe8ff', fontsize=10, weight='semibold', fontfamily='monospace')

# 2. Left Column: Brand Emblem & Core Concept
logo_path = r"C:\Users\maat\Documents\antigravity\werracle\assets\werracle_logo_oracle_trans.png"
try:
    logo_img = Image.open(logo_path)
    # Extent: [left, right, bottom, top] in data coords
    ax.imshow(logo_img, extent=[5, 33, 40, 78], aspect='auto', zorder=5)
except Exception as e:
    print("Logo load note:", e)

# Brand name and subtitle below logo
ax.text(19, 34, "WERRACLE",
        ha='center', va='center', color='#ffffff', fontsize=24, weight='bold', fontfamily='sans-serif')
ax.text(19, 29, "Decisions a blockchain can check. In 32 bytes.",
        ha='center', va='center', color='#ffc857', fontsize=10.5, style='italic', fontfamily='sans-serif')
ax.text(19, 24, "werracle.com  |  radar.werracle.com",
        ha='center', va='center', color='#7cf5c4', fontsize=11, weight='bold', fontfamily='monospace')

# Divider Line
line = patches.ConnectionPatch((36, 12), (36, 80), "data", "data",
                              color='#2a2760', lw=1.5, linestyle='--')
ax.add_patch(line)

# 3. Right Column: 4 Pillar Capability Cards
cards_data = [
    {
        "y": 66,
        "tag": "01 | DEPOLAMASIZ MIMARI (ZERO-STORAGE)",
        "tag_color": "#ffc857",
        "title": "32 Bayt EVM Depolama & ~20k Gaz Karar Motoru",
        "desc": "Model agirlik saklamaz; Mandelbrot fraktal koordinatindan aninda turetir. solc 0.8.20 uzerinde ayni islem icinde intra-block koruma saglar.",
        "badge": "32 Bytes Slot"
    },
    {
        "y": 48.5,
        "tag": "02 | MATEMATIKSEL GUVENCE (FORMAL VERIFICATION)",
        "tag_color": "#7cf5c4",
        "title": "Lean 4 Cekirdegiyle Kanitlanmis 40 Teorem",
        "desc": "Kacis donguleri kesin durur, Q16.16 aritmetigi asla tasmaz, gaz tavan altinda kalir. Sifir 'sorry', sifir varsayim; makine onayli sertifika.",
        "badge": "Lean 4 Certified"
    },
    {
        "y": 31,
        "tag": "03 | DEFI & OEV RISK GOZLEMEVI (CANLI RADAR)",
        "tag_color": "#9fe8ff",
        "title": "83 Morpho Pazari & %98.10 SVR Deger Geri Kazanimi",
        "desc": "Base L2'de 105 coklu cagrili tasfiye analiz edildi: Chainlink SVR, mevduat sahiplerine %98.1 degeri geri kazandirirken solver marjlarini -%1.55'e sikistirdi.",
        "badge": "Live Observatory"
    },
    {
        "y": 13.5,
        "tag": "04 | FIKRI MULKIYET VE AKADEMIK KULLIYAT",
        "tag_color": "#c084fc",
        "title": "2 Patent Basvurusu, arXiv, SSRN ve CERN Zenodo",
        "desc": "TURKPATENT TR 2026/016285 ve TR 2026/016633 patent basvurulari; acik kaynak Solidity, Cairo ve Lean 4 kutuphaneleri.",
        "badge": "IP & Papers"
    }
]

for card in cards_data:
    y = card["y"]
    # Background card
    card_patch = patches.FancyBboxPatch((39, y), 58, 14.5, boxstyle="round,pad=0.8",
                                        fc='#0f0d2b', ec='#2a2760', lw=1.2)
    ax.add_patch(card_patch)
    
    # Tag
    ax.text(40.5, y + 11.5, card["tag"],
            ha='left', va='center', color=card["tag_color"], fontsize=8.5, weight='bold', fontfamily='monospace')
    
    # Badge on right
    ax.text(95.5, y + 11.5, card["badge"],
            ha='right', va='center', color=card["tag_color"], fontsize=8, weight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#1a1840', ec=card["tag_color"], lw=0.8))
    
    # Title
    ax.text(40.5, y + 7.2, card["title"],
            ha='left', va='center', color='#ffffff', fontsize=11.5, weight='bold', fontfamily='sans-serif')
    
    # Description
    ax.text(40.5, y + 2.8, card["desc"],
            ha='left', va='center', color='#a7a2cf', fontsize=9.2, fontfamily='sans-serif')

# 4. Bottom Footer Bar
footer_box = patches.FancyBboxPatch((3, 2), 94, 6.5, boxstyle="round,pad=0.6",
                                    fc='#0a0820', ec='#1a1840', lw=1.0)
ax.add_patch(footer_box)

ax.text(5.5, 5.2, "ITOUCH SYSTEMS BILISIM VE ILETISIM SAN. TIC. LTD. STI.",
        ha='left', va='center', color='#ffffff', fontsize=9.5, weight='bold', fontfamily='sans-serif')
ax.text(5.5, 3.2, "Cukurova Teknokent, Saricam / Adana | itouch.com.tr | werracle.com | werr.io",
        ha='left', va='center', color='#a7a2cf', fontsize=8.5, fontfamily='sans-serif')
ax.text(94.5, 4.2, "GitHub: pCwOrM/werracle | Lean 4 | EVM | Base L2 | Arbitrum",
        ha='right', va='center', color='#7cf5c4', fontsize=9, weight='semibold', fontfamily='monospace')

out_path = "itouch_linkedin_werracle_launch_card.png"
plt.tight_layout()
plt.savefig(out_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved high-res card to:", out_path)
