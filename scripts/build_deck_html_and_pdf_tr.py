import os
import base64
import shutil
from playwright.sync_api import sync_playwright

WORKSPACE = os.getcwd()
CHARTS_DIR = os.path.join(WORKSPACE, "deck_assets")
ARTIFACT_DIR = r"C:\Users\maat\.gemini\antigravity\brain\9cfb8917-acbb-4be8-8bb2-995d94af3274"

def img_to_b64(filename):
    path = os.path.join(CHARTS_DIR, filename)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"

b64_oev = img_to_b64("chart_oev_comparison_tr.png")
b64_stress = img_to_b64("chart_stress_curve_tr.png")
b64_arr = img_to_b64("chart_arr_projection_tr.png")
b64_funds = img_to_b64("chart_use_of_funds_tr.png")

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Werracle Radar - Yatırımcı Sunumu</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: 16in 9in;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    background: #090d16;
    color: #f8fafc;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .slide {{
    width: 16in;
    height: 9in;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 48px 64px;
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at top right, rgba(56, 189, 248, 0.08), transparent 40%),
                radial-gradient(circle at bottom left, rgba(16, 185, 129, 0.05), transparent 40%),
                #0b0f19;
  }}

  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 16px;
  }}

  .header-left {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .brand {{
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  .category-pill {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 10px;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    border-radius: 999px;
  }}

  .header-title {{
    font-size: 14px;
    color: #94a3b8;
    font-weight: 500;
  }}

  .content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 24px 0;
  }}

  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 14px;
    font-size: 12px;
    color: #64748b;
  }}

  .footer a {{
    color: #38bdf8;
    text-decoration: none;
  }}

  /* Typography */
  h1.slide-title {{
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.15;
    margin-bottom: 12px;
    color: #ffffff;
  }}

  h2.slide-sub {{
    font-size: 18px;
    font-weight: 400;
    color: #94a3b8;
    margin-bottom: 24px;
    max-width: 90%;
  }}

  /* Cards & Layouts */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
    align-items: center;
  }}

  .grid-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }}

  .grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }}

  .card {{
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 24px;
    backdrop-filter: blur(10px);
  }}

  .card-highlight {{
    border-color: rgba(56, 189, 248, 0.35);
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
  }}

  .card-title {{
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .card-desc {{
    font-size: 14px;
    color: #94a3b8;
    line-height: 1.5;
  }}

  .kpi-box {{
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
  }}

  .kpi-num {{
    font-size: 32px;
    font-weight: 800;
    color: #38bdf8;
    line-height: 1.1;
    font-family: 'JetBrains Mono', monospace;
  }}

  .kpi-label {{
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #94a3b8;
    margin-top: 6px;
  }}

  .chart-img {{
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
  }}

  /* Tables */
  table.deck-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}

  table.deck-table th {{
    background: rgba(15, 23, 42, 0.95);
    color: #38bdf8;
    font-weight: 700;
    text-align: left;
    padding: 12px 16px;
    border-bottom: 2px solid rgba(56, 189, 248, 0.3);
  }}

  table.deck-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    color: #cbd5e1;
  }}

  table.deck-table tr:hover td {{
    background: rgba(56, 189, 248, 0.04);
  }}

  .tag-green {{
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
  }}

  .tag-blue {{
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 11px;
  }}

  .hero-tag {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    color: #38bdf8;
    margin-bottom: 18px;
  }}
</style>
</head>
<body>

<!-- SLIDE 1: KAPAK -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">DeFi Risk Telemetrisi</div>
    </div>
    <div class="header-title">ITouch Bilişim Sistemleri &bull; Tohum / Stratejik Yatırım Turu</div>
  </div>
  <div class="content" style="align-items: flex-start; justify-content: center; max-width: 1000px;">
    <div class="hero-tag">
      <span>●</span> Base Ana Ağında Canlı &bull; 2,20 Milyar $+ İzlenen Borç Hacmi
    </div>
    <h1 style="font-size: 56px; font-weight: 800; line-height: 1.08; letter-spacing: -1.5px; margin-bottom: 20px;">
      Modüler DeFi İçin Yüksek Frekanslı Risk ve OEV Altyapısı
    </h1>
    <h2 style="font-size: 22px; color: #94a3b8; font-weight: 400; line-height: 1.5; margin-bottom: 40px;">
      MetaMorpho kasa küratörlerini, kredi masalarını ve kurumsal sermayeyi koruyan alt-20ms parametrik stres testi ve tasfiye gözetim motoru.
    </h2>
    <div class="grid-4" style="width: 100%;">
      <div class="kpi-box">
        <div class="kpi-num">2,20 M$</div>
        <div class="kpi-label">İzlenen Borç (Base)</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">~15 ms</div>
        <div class="kpi-label">Karar Hesaplama Hızı</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">%94,38</div>
        <div class="kpi-label">Doğrulanmış SVR Kazanımı</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">%100,0</div>
        <div class="kpi-label">30 Günlük Doğrulanmış Uptime</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Kurucu Ekip: Volkan Dağlı (CTO) &bull; Dr. Zerrin Dağlı (Danışman) &bull; Dağhan Dağlı</div>
    <div>Yönetici Hattı: <a href="mailto:ask@answerr.me">ask@answerr.me</a> &bull; <a href="https://radar.werracle.com">radar.werracle.com</a></div>
    <div>Slayt 01 / 12</div>
  </div>
</div>

<!-- SLIDE 2: PROBLEM -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Piyasa Problemi</div>
    </div>
    <div class="header-title">Trilyon Dolarlık Borçlanma Piyasasının Kör Noktası</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Modüler Kredi Riski Gerçek Zamanlı Denetim Rayları Olmadan Büyüyor</h1>
    <h2 class="slide-sub">Morpho Blue ve Aave v3 milyarlarca dolarlık borçlanma hacmi yarattı, ancak kritik risk kör noktaları doğurdu.</h2>
    <div class="grid-3">
      <div class="card card-highlight">
        <div class="card-title" style="color: #f87171;">
          <span style="font-size: 20px;">⚡</span> 1. Risk Bölünmesi & OEV Kanaması
        </div>
        <div class="card-desc">
          Monolitik havuzlar yerine kredi yüzlerce izole pazara dağıldı. Piyasa düşüşlerinde tasfiye primleri gaz savaşlarıyla blok üreticilerine (builder) akar. Ethereum L1'de builder rüşvetlerinin <strong>%95,94'ü</strong> uç tasfiyelerde toplanır.
        </div>
      </div>
      <div class="card card-highlight">
        <div class="card-title" style="color: #f59e0b;">
          <span style="font-size: 20px;">📉</span> 2. Küratörlerin Kör Uçuşu
        </div>
        <div class="card-desc">
          1,5 Milyar $+ TVL yöneten MetaMorpho küratörleri sermayeyi izole pazarlara dağıtır. Mevcut analiz araçları yalnızca statik günlük özetlere dayanır; anlık teminat çöküşünü ve zincirleme batık borcu kriz anından önce simüle edemez.
        </div>
      </div>
      <div class="card card-highlight">
        <div class="card-title" style="color: #38bdf8;">
          <span style="font-size: 20px;">🔒</span> 3. Kurumsal Sermaye Denetim İster
        </div>
        <div class="card-desc">
          Kurumsal kredi masaları ve hazineler, izinsiz DeFi'ye sermaye bağlamadan önce kesintisiz parametrik stres testleri, doğrulanabilir zincir üstü denetimler ve anlık Temerrüt Halinde Kayıp (LGD) metrikleri talep eder.
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Yatırımcı Sunumu &bull; Gizli</div>
    <div>Canlı Telemetri: <a href="https://api.werracle.com/v1/radar/overview">api.werracle.com</a></div>
    <div>Slayt 02 / 12</div>
  </div>
</div>

<!-- SLIDE 3: ÇÖZÜM -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Tescilli Mimari</div>
    </div>
    <div class="header-title">Alt-Saniyelik Parametrik Risk ve Tasfiye Motoru</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Werracle Reflex Karar Motoru: Canlı Risk DaaS</h1>
    <h2 class="slide-sub">Layer-2 flashblock'larını doğrudan kurumsal risk modellerine bağlayan üretim sınıfı telemetri boru hattı.</h2>
    <div class="grid-3" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-title"><span style="color:#38bdf8;">01.</span> L2 Flashblock Gözetimi</div>
        <div class="card-desc">
          Base 200 ms flashblock'ları ve Morpho Blue GraphQL olaylarının anlık toplanması. 68.700+ açık pozisyon takibi ve 45 listelenmemiş/sentetik pazarın kurumsal veriden ayıklanması.
        </div>
      </div>
      <div class="card">
        <div class="card-title"><span style="color:#10b981;">02.</span> Parametrik Şok Simülasyonu</div>
        <div class="card-desc">
          Her aktif borçlu üzerinde anlık teminat fiyat şokları (%0, -%5, -%10, -%15, -%20, -%30). LLTV ve Tasfiye Teşvik Çarpanı (LIF) ile batık borcun kasa payına pro-rata atfı.
        </div>
      </div>
      <div class="card">
        <div class="card-title"><span style="color:#a855f7;">03.</span> Doğrulanmış SVR OEV Kazanımı</div>
        <div class="card-desc">
          Tasfiye gelirlerini, Chainlink Smart Value Recapture (SVR) mekanizmasının <strong>%94,38 değer geri kazandırdığını</strong> kanıtlayan bağımsız ampirik modelimizle kalibre eder.
        </div>
      </div>
    </div>
    <div class="card" style="background: rgba(15, 23, 42, 0.9); border-color: rgba(56, 189, 248, 0.4); padding: 18px 24px;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span style="font-weight: 700; color: #38bdf8;">Canlı Küratör API'si:</span>
          <code style="font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #f8fafc; margin-left: 10px;">GET https://api.werracle.com/v1/radar/curator/steakhouse</code>
        </div>
        <span class="tag-green">HTTP 200 OK &bull; Canlıda Doğrulandı</span>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Yatırımcı Sunumu &bull; Gizli</div>
    <div>Canlı Telemetri: <a href="https://api.werracle.com/v1/radar/overview">api.werracle.com</a></div>
    <div>Slayt 03 / 12</div>
  </div>
</div>

<!-- SLIDE 4: AMPİRİK KEŞİF VE KANIT -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Akademik Kanıt</div>
    </div>
    <div class="header-title">Canlı Ağda Chainlink SVR'yi Ölçen İlk Çalışma</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Çığır Açan Ampirik Doğrulama: %94,38 Geri Kazanım</h1>
    <h2 class="slide-sub">Base üzerinde 105 doğrulanmış SVR tasfiye işlemini (1,90 M$ ödenen borç) denetleyen yayınlanmış bilimsel monografi.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_oev}" class="chart-img" alt="OEV Karsilastirmasi">
      </div>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="card" style="padding: 16px;">
          <div style="font-size: 20px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">%94,38 (179,8k $)</div>
          <div style="font-size: 13px; color: #94a3b8; font-weight: 600;">Protokol Gelir Kontratına Geri Kurtarılan OEV</div>
          <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Tekil işlemlerin medyanında tasfiye teşvikinin <strong>%98,30'u</strong> kurtarılır.</div>
        </div>
        <div class="card" style="padding: 16px;">
          <div style="font-size: 20px; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono';">+%1,26 Medyan</div>
          <div style="font-size: 13px; color: #94a3b8; font-weight: 600;">Kahin Fiyatlarına Göre Solver Brüt Kârı</div>
          <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Yoğun rekabet kartelleşmeyi önler (İlk 3 solver = %77,05, HHI = 2.216).</div>
        </div>
        <div class="card" style="padding: 16px;">
          <div style="font-size: 20px; font-weight: 800; color: #f87171; font-family: 'JetBrains Mono';">%95,94 L1 Kuyruk Yoğunlaşması</div>
          <div style="font-size: 13px; color: #94a3b8; font-weight: 600;">En Büyük 22 İşlem 351,3k $ Öncelik Ücreti Ödedi</div>
          <div style="font-size: 12px; color: #64748b; margin-top: 4px;">L2 SVR mimarisinin L1'deki MEV builder sızıntısını ortadan kaldırdığını ampirik olarak kanıtlar.</div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>DOI: 10.5281/zenodo.23642090 &bull; Hugging Face: pCwOrM/werracle-oev-liquidation-dataset-2026</div>
    <div>Slayt 04 / 12</div>
  </div>
</div>

<!-- SLIDE 5: CANLI ÜRETİM VE DURUM -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Canlı Operasyon</div>
    </div>
    <div class="header-title">Canlı Üretim Telemetrisi (Day 0 Kanıtı)</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Base Ana Ağında Kesintisiz Piyasa Gözetimi</h1>
    <h2 class="slide-sub">Sıfır sahte veri. Morpho Blue GraphQL ve Base RPC düğümlerinden tam otomatik günlük senkronizasyon.</h2>
    <div class="grid-4" style="margin-bottom: 24px;">
      <div class="kpi-box">
        <div class="kpi-num">2.197.760.378 $</div>
        <div class="kpi-label">Temiz İzlenen Borç</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">38 Pazar</div>
        <div class="kpi-label">Listelenmiş & Güvenli</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">68.727</div>
        <div class="kpi-label">Açık Kredi Pozisyonu</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-num">45 Pazar</div>
        <div class="kpi-label">Filtrelenmiş Unlisted / Spam</div>
      </div>
    </div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title"><span style="color:#38bdf8;">●</span> Kurumsal Veri Hijyeni</div>
        <div class="card-desc">
          Ham Morpho verileri 2,31 Milyar $ tutarında sentetik pazar (HERMES, test_cbBTC vb.) içerir. Werracle, listelenmemiş teminatları filtreleyerek kurumlara saf ve denetlenebilir kredi verisi sağlayan <strong>tek altyapıdır</strong>.
        </div>
      </div>
      <div class="card">
        <div class="card-title"><span style="color:#10b981;">●</span> Bağımsız Frankfurt Sağlık Düğümü</div>
        <div class="card-desc">
          Frankfurt'ta konuşlu bağımsız bir gözetleme süreci (<code>mechsrv</code>), API'yi her 5 dakikada bir sorgular ve saatlik veritabanı kopyası alır. %100 30 günlük çalışma süresi ve 191 ms küresel medyan gecikme.
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Canlı Durum Sayfası: <a href="https://radar.werracle.com/status">radar.werracle.com/status</a></div>
    <div>Slayt 05 / 12</div>
  </div>
</div>

<!-- SLIDE 6: KÜRATOR STRES TESTİ DEMO -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Amiral Gemisi Ürün</div>
    </div>
    <div class="header-title">Canlı Dinamik Kasa Stres Testi</div>
  </div>
  <div class="content">
    <h1 class="slide-title">MetaMorpho Küratörleri İçin Canlı Risk Simülasyonu</h1>
    <h2 class="slide-sub">Steakhouse, Gauntlet ve Re7 kasaları üzerinde gerçek zamanlı Temerrüt Halinde Kayıp (LGD) modellemesi.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_stress}" class="chart-img" alt="Stres Egrisi">
      </div>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="card card-highlight">
          <div class="card-title" style="color: #38bdf8;">Vaka Analizi: Steakhouse USDC (116,2 M$ TVL)</div>
          <div class="card-desc">
            5 teminat pazarındaki (cbBTC, cbETH, wstETH vb.) canlı kasa paylarını çeker ve parametrik fiyat çöküşlerini simüle eder.
          </div>
        </div>
        <div class="grid-2">
          <div class="kpi-box" style="padding: 14px;">
            <div class="kpi-num" style="font-size: 24px;">0,00 $</div>
            <div class="kpi-label">Mevcut Batık Borç</div>
          </div>
          <div class="kpi-box" style="padding: 14px;">
            <div class="kpi-num" style="font-size: 24px; color: #f87171;">%1,06</div>
            <div class="kpi-label">En Kötü Senaryo Kaybı (-%30)</div>
          </div>
        </div>
        <div class="card" style="padding: 16px;">
          <div style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">
            <strong>Pro-Rata Kasa Atfı:</strong> -%20 teminat düşüşünde 209,4 M$ borç tasfiye edilebilir hale gelir, piyasada 2,41 M$ batık borç oluşur; Steakhouse'un kıdemli tahsis yapısı sayesinde kasa payına düşen maruziyet 0$ seviyesinde kalır.
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Küratör Uç Noktası: <code>api.werracle.com/v1/radar/curator/{{vault}}</code></div>
    <div>Slayt 06 / 12</div>
  </div>
</div>

<!-- SLIDE 7: İŞ MODELİ VE BİRİM EKONOMİ -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">İş Modeli</div>
    </div>
    <div class="header-title">Yüksek Marjlı B2B SaaS ve Veri Aboneliği</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Tekrarlayan Kurumsal Katmanlar ve Üstün Birim Ekonomi</h1>
    <h2 class="slide-sub">Geliştiriciler için sürtünmesiz başlangıç, kurumsal küratörler için yüksek değerli analitik sözleşmeleri.</h2>
    <div class="grid-3" style="margin-bottom: 24px;">
      <div class="card">
        <div class="card-title">Topluluk / Kamu Malı</div>
        <div style="font-size: 28px; font-weight: 800; color: #ffffff; font-family: 'JetBrains Mono'; margin-bottom: 8px;">0 $</div>
        <div class="card-desc" style="font-size: 13px;">
          &bull; Halka açık durum ve özet API<br>
          &bull; Desteklenen kasa dizini<br>
          &bull; Zenodo ve HF açık verisi (CC-BY)<br>
          &bull; Kurumsal müşteri adayı hunisi
        </div>
      </div>
      <div class="card card-highlight">
        <div class="card-title" style="color: #38bdf8;">Pro Araştırmacı</div>
        <div style="font-size: 28px; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono'; margin-bottom: 8px;">149 $ <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">/ ay</span></div>
        <div class="card-desc" style="font-size: 13px;">
          &bull; Tam REST API erişimi<br>
          &bull; 600 istek / dakika<br>
          &bull; Geçmiş SVR ve tasfiye kayıtları<br>
          &bull; MEV araştırmacıları ve bot operatörleri
        </div>
      </div>
      <div class="card card-highlight" style="border-color: #10b981;">
        <div class="card-title" style="color: #10b981;">Kurumsal Küratör</div>
        <div style="font-size: 28px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono'; margin-bottom: 8px;">499 $ <span style="font-size: 14px; font-weight: 500; color: #94a3b8;">/ ay</span></div>
        <div class="card-desc" style="font-size: 13px;">
          &bull; Dinamik kasa stres testi API'si<br>
          &bull; 3.000 istek / dakika<br>
          &bull; Parametrik şok simülasyonları<br>
          &bull; %99,9 SLA & öncelikli kurumsal destek
        </div>
      </div>
    </div>
    <div class="grid-2">
      <div class="card" style="padding: 16px 20px;">
        <div class="card-title"><span style="color:#10b981;">●</span> Çift Kanallı Yasal Tahsilat Mimarisi</div>
        <div class="card-desc">
          Paddle (Merchant of Record) ile küresel kart & KDV uyumu + ITouch SWIFT banka havalesi + EIP-191/1271 imzalı Base USDC.
        </div>
      </div>
      <div class="card" style="padding: 16px 20px;">
        <div class="card-title"><span style="color:#38bdf8;">●</span> Teknokent Vergi Avantajı: %100 İstisna</div>
        <div class="card-desc">
          Çukurova Üniversitesi Teknokent bünyesinde: Yabancı kurumlara yazılım ihracatı <strong>%100 Kurumlar Vergisi indirimine</strong> tabidir (CB Kararı 11257).
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Birim Ekonomi: %88 Brüt Marj &bull; 12.4x LTV/CAC Oranı</div>
    <div>Slayt 07 / 12</div>
  </div>
</div>

<!-- SLIDE 8: PAZAR BÜYÜKLÜĞÜ (TAM / SAM / SOM) -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Pazar Büyüklüğü</div>
    </div>
    <div class="header-title">Modüler Kredi Riskinin Genişleyen Sınırları</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Milyarlarca Dolarlık Zincir Üstü Kredi Genişlemesi</h1>
    <h2 class="slide-sub">Kurumsal RWA'lar ve merkeziyetsiz borçlanma Layer-2 ağlarına taşınırken gerçek zamanlı risk altyapısı zorunlu hale geliyor.</h2>
    <div class="grid-3" style="margin-bottom: 24px;">
      <div class="card">
        <div style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">TAM &bull; 2028 Ufku</div>
        <div style="font-size: 42px; font-weight: 800; color: #ffffff; font-family: 'JetBrains Mono'; margin: 10px 0;">45 Milyar $</div>
        <div class="card-desc">
          Toplam kurumsal zincir üstü borçlanma, kredi delegasyonu ve RWA yapılandırılmış borç hacmi.
        </div>
      </div>
      <div class="card card-highlight">
        <div style="font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase;">SAM &bull; Aktif Modüler TVL</div>
        <div style="font-size: 42px; font-weight: 800; color: #38bdf8; font-family: 'JetBrains Mono'; margin: 10px 0;">8,5 Milyar $</div>
        <div class="card-desc">
          Modüler ve izole borç verme protokollerindeki (Morpho Blue, Aave v3, Fluid, Euler v2) aktif kilitli değer.
        </div>
      </div>
      <div class="card card-highlight" style="border-color: #10b981;">
        <div style="font-size: 13px; font-weight: 700; color: #10b981; text-transform: uppercase;">SOM &bull; Yıllık Risk Harcaması</div>
        <div style="font-size: 42px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono'; margin: 10px 0;">120 Milyon $</div>
        <div class="card-desc">
          Özel risk kürasyonu, tasfiye telemetrisi ve otomatik stres testlerine yapılan yıllık kurumsal harcama.
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Temel Sektörel Rüzgar: Morpho Blue'nun Hızlı Yükselişi</div>
      <div class="card-desc">
        Morpho Blue 18 aydan kısa sürede 0'dan 1,5 Milyar $+ TVL'ye ulaşarak Coinbase, Spark ve Steakhouse için temel teminat katmanı haline geldi. Dağıtılan her yeni izole pazar, Werracle Radar için yeni bir kurumsal temas noktasıdır.
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Yatırımcı Sunumu &bull; Gizli</div>
    <div>Slayt 08 / 12</div>
  </div>
</div>

<!-- SLIDE 9: REKABET ORTAMI VE KALE -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Rekabet Kalesi</div>
    </div>
    <div class="header-title">Haksız Rekabet Avantajları ve Fikri Mülkiyet</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Yüksek Frekanslı Veri ile Risk Analitiğinin Kesişimi</h1>
    <h2 class="slide-sub">Geleneksel risk şirketleri yavaş ve pahalı danışmanlık satar. Werracle, alt-saniyelik otomatik DaaS API'si sunar.</h2>
    <div style="margin-bottom: 20px;">
      <table class="deck-table">
        <thead>
          <tr>
            <th>Önemli Metrik / Yetenek</th>
            <th>Werracle Radar</th>
            <th>Chaos Labs / Gauntlet</th>
            <th>Block Analitica</th>
            <th>Dune Analytics</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Gecikme / Çözünürlük</strong></td>
            <td><span class="tag-green">~15ms Karar Hesaplama</span></td>
            <td>Periyodik / Blok Düzeyi</td>
            <td>Günlük Statik Raporlar</td>
            <td>Saniyeler ila Dakikalar</td>
          </tr>
          <tr>
            <td><strong>Canlı Dinamik Kasa Şokları</strong></td>
            <td><span class="tag-green">Parametrik (%0 ila -%30)</span></td>
            <td>Özel İç Modeller</td>
            <td>Statik Tablolar</td>
            <td>Yok (Yalnızca Geçmiş)</td>
          </tr>
          <tr>
            <td><strong>Doğrulanmış SVR OEV Kazanımı</strong></td>
            <td><span class="tag-green">%94,38 Kalibre Edilmiş</span></td>
            <td>Yok</td>
            <td>Yok</td>
            <td>Temel Panolar</td>
          </tr>
          <tr>
            <td><strong>Fiyatlandırma & Erişim</strong></td>
            <td><span class="tag-blue">149$ – 499$ / ay (Self-Serve)</span></td>
            <td>50k$ – 250k$ / yıl (Danışmanlık)</td>
            <td>30k$+ / yıl (Kurumsal)</td>
            <td>4.800$ / yıl (Genel SQL)</td>
          </tr>
          <tr>
            <td><strong>Fikri Mülkiyet Koruması</strong></td>
            <td><span class="tag-green">TR 2026/016285 Patent & BSL</span></td>
            <td>Özel Şirket İçi</td>
            <td>Özel Şirket İçi</td>
            <td>Açık SQL Sorguları</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="grid-2">
      <div class="card">
        <div class="card-title">Patent ve Lisanslama Kalesi</div>
        <div class="card-desc">
          Çekirdek yürütme motorumuz <strong>TÜRKPATENT TR 2026/016285</strong> patent başvurusu ile korunmakta ve Business Source License 1.1 (BSL 1.1 - 2030-01-01'e kadar korumalı, sonra Apache 2.0) altında lisanslanmaktadır.
        </div>
      </div>
      <div class="card">
        <div class="card-title">L2 OEV Veri Tekeli</div>
        <div class="card-desc">
          Kanıtlanmış ampirik SVR veri setinin ilk yayıncısı olarak ilk-hamle avantajı. Küratörler ve protokoller temel risk varsayımlarını doğrudan bizim açık Zenodo modellerimiz üzerine inşa etmektedir.
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Werracle Radar Yatırımcı Sunumu &bull; Gizli</div>
    <div>Slayt 09 / 12</div>
  </div>
</div>

<!-- SLIDE 10: FİNANSAL PROJEKSİYONLAR -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Finansal Projeksiyon</div>
    </div>
    <div class="header-title">3 Yıllık Projeksiyonlar ve 3,8 M$+ ARR Hedefi</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Öngörülebilir, Yüksek Marjlı Yazılım Genişlemesi</h1>
    <h2 class="slide-sub">Minimum altyapı gideri, %88 brüt kâr marjı ile hızlı bileşik ARR büyümesi sağlar.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_arr}" class="chart-img" alt="ARR Buyume">
      </div>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">1. Yıl (2027) Run-Rate</span>
            <span style="font-size: 22px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">364.260 $ ARR</span>
          </div>
          <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
            120 Pro Abone &bull; 25 MetaMorpho Küratörü & Risk Masası &bull; 8. ayda başabaş noktası.
          </div>
        </div>
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">2. Yıl (2028) Run-Rate</span>
            <span style="font-size: 22px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">1.373.460 $ ARR</span>
          </div>
          <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
            450 Pro Abone &bull; Base, Arbitrum ve Ethereum L1 genelinde 95 Kurumsal Müşteri.
          </div>
        </div>
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <span style="font-size: 16px; font-weight: 700; color: #ffffff;">3. Yıl (2029) Run-Rate</span>
            <span style="font-size: 22px; font-weight: 800; color: #10b981; font-family: 'JetBrains Mono';">3.822.240 $ ARR</span>
          </div>
          <div style="font-size: 13px; color: #94a3b8; margin-top: 6px;">
            1.200 Pro Kullanıcı &bull; 280 Kurumsal Küratör &bull; Kurumsal DeFi'nin standart risk katmanı.
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Birim Ekonomi: %88 Ortalama Brüt Marj &bull; 12.4x LTV/CAC Oranı</div>
    <div>Slayt 10 / 12</div>
  </div>
</div>

<!-- SLIDE 11: EKİP VE KURUMSAL GÜVENCE -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Yönetim Ekibi ve Yönetişim</div>
    </div>
    <div class="header-title">ITouch Bilişim Sistemleri (8 Kişilik Ekip) ve Akademik Katman</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Üst Yönetim, Mühendislik Kadrosu ve Akademik Yönetişim</h1>
    <h2 class="slide-sub">Çukurova Üniversitesi Teknokent'te yerleşik ITouch Bilişim Sistemleri Ltd. Şti. ticari kadrosu ve bağımsız akademik araştırma katmanı.</h2>
    <div class="grid-3" style="margin-bottom: 22px;">
      <div class="card card-highlight">
        <div class="card-title">Yönetim ve Ortaklar</div>
        <div class="card-desc" style="font-size: 13px; line-height: 1.55;">
          <strong>Volkan Dağlı — Kurucu & CTO</strong><br>
          Fizikçi, Yönetim Bilişim Sistemleri Uzmanı & Bilişim Teknolojileri YL (M.Sc. IT). Werracle ve WERR çekirdeğinin baş mimarı.<br><br>
          <strong>Bekirhan Dağlı — Ortak & CEO</strong><br>
          Çevre Mühendisi. ITouch Bilişim Sistemleri bünyesinde kurumsal strateji, iş geliştirme ve kurumsal operasyonlara liderlik etmektedir.
        </div>
      </div>
      <div class="card">
        <div class="card-title">Mühendislik, Finans ve Operasyon</div>
        <div class="card-desc" style="font-size: 12.5px; line-height: 1.55;">
          &bull; <strong>Burak Salar</strong> — Mekatronik Mühendisi, MBA<br>
          &bull; <strong>Fatih İlkin Sercan</strong> — Ekonomist, Sermaye Piyasası ve Borsa YL<br>
          &bull; <strong>Mustafa Kalender</strong> — Bilgisayar Mühendisi<br>
          &bull; <strong>Mustafa Ünal</strong> — Yazılım Geliştirme Uzmanı & Usta Öğretici<br>
          &bull; <strong>Prenses Metin</strong> — Bilgisayar Programcısı<br>
          &bull; <strong>Semih Salar</strong> — İşletme Uzmanı
        </div>
      </div>
      <div class="card">
        <div class="card-title">Akademik Araştırma ve Patentler</div>
        <div class="card-desc" style="font-size: 12.5px; line-height: 1.55;">
          &bull; <strong>Volkan Dağlı</strong> — Baş Araştırmacı (Anadolu Üniversitesi)<br>
          &bull; <strong>Dr. Zerrin Dağlı</strong> — Akademik Danışman ve Ortak Yazar (Mersin Üniv.)<br>
          &bull; <strong>Dağhan Dağlı</strong> — Araştırma Stajyeri (Toros Üniv. — Toros Fen Lisesi)
        </div>
      </div>
    </div>
    <div class="grid-3">
      <div class="card" style="padding: 16px;">
        <div style="font-weight: 700; color: #ffffff; font-size: 14px;">Çukurova Üniversitesi Teknokent</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">ITouch Bilişim Sistemleri Ar-Ge Merkezi.</div>
      </div>
      <div class="card" style="padding: 16px;">
        <div style="font-weight: 700; color: #ffffff; font-size: 14px;">TÜRKPATENT TR 2026/016285 & 016633</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Münhasır ticari lisans ve markalar (Werr®, Werracle®, Answerr®).</div>
      </div>
      <div class="card" style="padding: 16px;">
        <div style="font-weight: 700; color: #ffffff; font-size: 14px;">BSL 1.1 Ticari Lisanslama</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Açık akademik ve testnet erişimi; ITouch Bilişim Sistemleri üzerinden kurumsal ana ağ ve DaaS lisansı.</div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Doğrudan Yönetici İletişimi: <a href="mailto:contact@werracle.com">contact@werracle.com</a> &bull; <a href="mailto:ask@answerr.me">ask@answerr.me</a></div>
    <div>Slayt 11 / 12</div>
  </div>
</div>

<!-- SLIDE 12: YATIRIM TALEBİ VE FON KULLANIMI -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="brand">WERRACLE RADAR</div>
      <div class="category-pill">Yatırım Talebi</div>
    </div>
    <div class="header-title">Tohum / Stratejik Sermaye Tahsisi</div>
  </div>
  <div class="content">
    <h1 class="slide-title">Kurumsal DeFi Risk Pazarında Ölçeklenmek İçin 1,5M $ Yatırım</h1>
    <h2 class="slide-sub">1,3 M$+ ARR hedefine ulaşmak, çoklu zincir hakimiyeti kurmak ve küratör pazarına derin nüfuz için 18 aylık pist.</h2>
    <div class="grid-2">
      <div>
        <img src="{b64_funds}" class="chart-img" alt="Fon Kullanimi">
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div class="card">
          <div style="font-weight: 700; color: #38bdf8; font-size: 14px;">Mühendislik Genişlemesi (%40 - 600k $)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Arbitrum, Optimism ve Ethereum L1 üzerinde milisaniyelik EVM veri akışlarını işleyecek 3 kıdemli Rust/Go sistem mühendisi istihdamı.</div>
        </div>
        <div class="card">
          <div style="font-weight: 700; color: #10b981; font-size: 14px;">Özel Archive Altyapısı (%25 - 375k $)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Kurumsal düşük gecikmeli veri akışları için tescilli bare-metal Archive Node'ları ve alt-saniyelik WebSocket dağıtım kümeleri.</div>
        </div>
        <div class="card">
          <div style="font-weight: 700; color: #f59e0b; font-size: 14px;">Küratör & Kurumsal İş Geliştirme (%20 - 300k $)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">MetaMorpho küratörleri (Steakhouse, Gauntlet, Re7), Aave risk DAO'ları ve kurumsal borç masalarıyla doğrudan entegrasyon.</div>
        </div>
        <div class="card">
          <div style="font-weight: 700; color: #a855f7; font-size: 14px;">Güvenlik Denetimleri ve Hukuk (%15 - 225k $)</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">SOC2 Type II kurumsal güvenlik sertifikasyonu, akıllı sözleşme denetimleri ve uluslararası kurumsal sözleşmeler için hukuk danışmanlığı.</div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <div>Canlı Demo: <a href="https://radar.werracle.com">radar.werracle.com</a> &bull; İletişim: <a href="mailto:ask@answerr.me">ask@answerr.me</a></div>
    <div>Slayt 12 / 12</div>
  </div>
</div>

</body>
</html>
"""

HTML_PATH = os.path.join(WORKSPACE, "deck_assets", "investor_deck_tr.html")
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML presentation written: {HTML_PATH}")

LOCAL_PDF = os.path.join(WORKSPACE, "Werracle_Radar_Yatirimci_Sunumu_TR.pdf")
ARTIFACT_PDF = os.path.join(ARTIFACT_DIR, "Werracle_Radar_Yatirimci_Sunumu_TR.pdf")

print("Rendering Turkish PDF via Playwright Chromium...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(f"file:///{HTML_PATH.replace(os.sep, '/')}", wait_until="networkidle")
    page.pdf(
        path=LOCAL_PDF,
        width="16in",
        height="9in",
        print_background=True,
        display_header_footer=False
    )
    browser.close()

shutil.copy2(LOCAL_PDF, ARTIFACT_PDF)
print(f"SUCCESS: Rendered local Turkish PDF -> {LOCAL_PDF}")
print(f"SUCCESS: Copied artifact Turkish PDF -> {ARTIFACT_PDF}")
print(f"PDF Size: {os.path.getsize(LOCAL_PDF):,} bytes")
