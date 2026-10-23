# Radar Lansman Planı Değerlendirmesi ve Düzeltilmiş Yol Haritası (23 Ekim 2026)

## 1. Yayınlanmaması Gereken Hatalı / Abartılı İddialar

1. **"Solver'ların %75,6'sı zararda, medyan marj −%18,7":**
   * Bu rakamlar Adım 2'deki token ondalık/filtreleme hatasından kaynaklanmıştır.
   * Zincirden doğrulanan gerçek rakamlar: **Medyan marj −%1,5**.
   * Marjı negatif kalan işlemlerin toplam zararı sektör genelinde yalnızca **yaklaşık 2.500 $**.
   * Yani ortada kitlesel bir sektör batışı yoktur; teklif açık artırması (OFA) kârı neredeyse sıfıra kadar sıkıştırmaktadır.

2. **"0x8b61… botu 58 bin $ zarar yazdı":**
   * **Yanlış ve riskli.** Bu bot 51 işlemde yaklaşık **+447 $** net kârdadır.
   * Gerçek bir botu adıyla "58 bin $ zararda" diye duyurmak hem yanıltıcı bilgi hem de itibar ve hukuk riski doğurur.

3. **"Bytecode loglarından tersine mühendislik":**
   * Abartılı bir retoriktir. Kullanılan veri, EVM üzerindeki herkese açık standart olay kayıtlarıdır (`SolverTxResult`).

4. **"Dünyada tek":**
   * Doğrulanmamış bir iddiadır. Chainlink SVR'nin topladığı protokol gelirini kendisi de duyurmaktadır. "Değerin çoğu protokole gidiyor" bulgusu şaşırtıcı değil; SVR tam olarak bu amaçla (OEV'yi protokole geri kazandırmak için) tasarlanmıştır.

---

## 2. Gerçek ve Bilimsel Olarak Savunulabilir Bulgular

* **Doğrulanmış Ölçüm:** Son 14 günde Base ağındaki 105 SVR likidasyonunda brüt değer yaklaşık **190.000 $**'dır.
* **Protokol Yakalama Oranı:** Bu değerin **yaklaşık %98'i** teklif (bid) olarak borç verme protokollerine geri aktarılmıştır.
* **Solver Kalan Payı:** Solver'lara swap kaybı (slippage) öncesi brüt kârın **yaklaşık %2'si** kalmıştır.
* **İşlem Dağılımı:** İşlemlerin **%61'i** sıfır ya da sıfırın hemen altında bir marjla sonuçlanmıştır.
* **Sonuç:** Bu ölçüm, Chainlink SVR mekanizmasının teoride vaat ettiği gibi pratikte de çalıştığını, OEV'yi arama botlarından alıp borç verenlere iade ettiğini bağımsız olarak kanıtlayan somut ve saygın bir çalışmadır.

### Raporlanması Gereken Metodolojik Sınırlar:
1. Ölçüm büyük oranda tek bir volatil haftaya (15 Ekim haftası) dayanmaktadır.
2. Arbitrum'da yalnızca 3 işlem doğrulanabilmiştir (veri seti küçüktür).
3. Solver'ların DEX arbitrajındaki swap kaybı (slippage) ve gas fiyat dalgalanması hesaba katılmamıştır.

---

## 3. Gerçekçi İş Modeli ve Gelir Stratejisi

1. **Hibe Başvuruları (En Gerçekçi ve Hızlı Finansman):**
   * Morpho Forumu: [MIP 81 (Morpho Grants Pilot Program)](https://forum.morpho.org/t/mip-81-morpho-grants-pilot-program/1082) ve [MIP 93 (Call for Grants)](https://forum.morpho.org/t/mip-93-call-for-grants/1177).
   * Kapsam: Bağımsız, açık kaynak, kamu yararı (public good) niteliğinde ekosistem risk ve likidasyon radarı.
2. **Kurumsal Satış Varsayımlarının Düzeltilmesi:**
   * Gauntlet, Chaos Labs ve büyük kasa yöneticilerinin kendi iç altyapıları mevcuttur; aylık 999-2999 $ doğrudan API satışı ilk etapta gerçekçi değildir.
   * L1 ön-likidasyonları neredeyse tamamen tozdur; "ön-likidasyon alfa beslemesi" ticarileştirilebilir bir ürün değildir.
3. **Altyapı Dengesi:**
   * Radar API trafiği ve veri sunumu için 2–4 Uvicorn worker fazlasıyla yeterlidir; 20 worker'a gerek yoktur.

---

## 4. Düzeltilmiş Uygulama Sırası (Yol Haritası)

1. **Veri Düzeltme & Metodoloji:**
   * Radar API ve Dashboard üzerindeki hatalı marjları (medyan -%1.5, %98 protokol yakalaması, %2 solver payı) doğrulanmış gerçek rakamlarla güncelle.
   * Bot adreslerini ifşa/suçlama listesinden kaldır; anonimleştirilmiş/genel metrik olarak göster.
   * Arbitrum ölçümünü tamamla ve ölçüm metodolojisini doğrudan panoya şeffafça yaz.
2. **Kamu Yararı Hibe Başvurusu:**
   * Morpho ve Chainlink için abartısız, bilimsel ve kamu yararı odaklı hibe başvuru metnini hazırla.
3. **Doğrulanmış Sosyal Medya Duyurusu:**
   * Sansasyonel ve agresif iddialardan arındırılmış, saygın veri analitiği dilinde doğrulanmış rakamlarla duyuru hazırla.
