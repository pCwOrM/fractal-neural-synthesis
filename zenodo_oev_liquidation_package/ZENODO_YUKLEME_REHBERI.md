# CERN Zenodo Yükleme ve Yayın Rehberi
## Empirical OEV & Liquidation Dynamics: 98.10% Value Recapture in Chainlink SVR Auctions and Structural MEV Power-Law Distribution on Ethereum L1

Bu rehber, **Base L2 Chainlink SVR**, **Morpho Blue** ve **Ethereum L1 MEV-Boost** sistemleri üzerinde 1.157 doğrulanmış işlemle gerçekleştirdiğimiz ampirik araştırmayı **CERN Zenodo** üzerinde açık bilim standardında kalıcı bir **DOI** ile tescillemeniz için hazırlanmıştır.

---

### 📦 Zenodo Paket Klasörü & Dosya Ayrımı
**Klasör Yolu:** `c:\Users\maat\Documents\antigravity\wonderful-raman\zenodo_oev_liquidation_package\`

* **Zenodo'ya Yüklenecek Dosyalar (Web Arayüzüne Sürüklenecekler):**
  1. `Empirical_OEV_and_Liquidation_Dynamics_Research_Monograph.pdf` *(Doğrudan tarayıcıda önizlenecek 3 sayfalık kamera-hazır akademik monograf)*
  2. `EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md` *(Markdown monograf)*
  3. `zenodo_bundle_oev_liquidation_empirical_research.zip` *(1.157 kayıtlı veri setini, doğrulama scriptlerini ve SHA-256 özetlerini içeren temiz arşiv)*
* **Yardımcı Yerel Dosyalar (Yüklenmez, size rehberlik eder):**
  * `.zenodo.json` *(Zenodo API üstveri şeması)*
  * `zenodo_description.html` *(Açıklama alanına yapıştırılacak zengin HTML)*
  * `ZENODO_YUKLEME_REHBERI.md` *(Bu rehber)*

---

### 🚀 Adım Adım Yükleme Talimatı

#### Adım 1: Zenodo'ya Giriş Yapın
1. Tarayıcınızda [https://zenodo.org/deposit/new](https://zenodo.org/deposit/new) adresine gidin.
2. Giriş yapın (GitHub veya ORCID ile).

#### Adım 2: Dosyaları Yükleyin
`zenodo_oev_liquidation_package` klasöründeki şu 3 dosyayı sürükleyip bırakın:
* `Empirical_OEV_and_Liquidation_Dynamics_Research_Monograph.pdf`
* `EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md`
* `zenodo_bundle_oev_liquidation_empirical_research.zip`

#### Adım 3: Temel Üstveri Bilgilerini Doldurun

* **Resource type:**  
  * Type: `Dataset` *(veya Publication > Preprint)*

* **Title (Başlık):**  
  ```text
  Empirical OEV & Liquidation Dynamics: 98.10% Value Recapture in Chainlink SVR Auctions and Structural MEV Power-Law Distribution on Ethereum L1
  ```

* **Publication Date:** `2026-10-24`

* **Creators (Yazarlar - Tam Akademik Künye):**
  1. Family name: `Dağlı`, Given names: `Volkan`  
     * Affiliation: `Anadolu University, Eskişehir, Türkiye & ITouch Systems, Adana, Türkiye`  
     * ORCID: `0009-0000-1587-8703`
  2. Family name: `Dağlı`, Given names: `Zerrin`  
     * Affiliation: `Mersin University, Mersin, Türkiye & Yusuf Kalkavan Anadolu Lisesi, Mersin, Türkiye`  
     * ORCID: `0000-0001-9490-6425`
  3. Family name: `Dağlı`, Given names: `Dağhan`  
     * Affiliation: `Toros Science High School, MEV (Toros University), Mersin, Türkiye`  
     * ORCID: `0009-0003-2492-8313`

* **Contributors (Katkıda Bulunanlar / Altyapı Desteği):**
  1. Family name: `Dağlı`, Given names: `Bekirhan`  
     * Affiliation: `ITouch Systems, Adana, Türkiye`  
     * Contributor type: `Other` *(veya HostingInstitution / DataCollector)*

* **Description (Açıklama):**  
  Klasördeki `zenodo_description.html` dosyasının içeriğini kopyalayıp Zenodo'nun **Description** kutusuna yapıştırın.

* **License:**  
  `Creative Commons Attribution 4.0 International (CC-BY-4.0)`

* **Keywords (Anahtar Kelimeler):**  
  ```text
  DeFi Liquidations, Oracle Extractable Value (OEV), Chainlink SVR, Morpho Blue, Order Flow Auctions (OFA), Maximal Extractable Value (MEV), Proposer-Builder Separation (PBS), Bertrand Competition, Multi-Call Decoding, Base L2, Ethereum L1, Open Science, Werracle
  ```

* **Related Identifiers (İlişkili Bağlantılar):**
  * `https://github.com/pCwOrM/werracle` &rarr; `isSupplementTo` (Software)
  * `https://radar.werracle.com` &rarr; `isDocumentedBy` (Other)
  * `https://werracle.io/radar.html` &rarr; `isDocumentedBy` (Other)
  * `https://api.werracle.com/v1/radar/overview` &rarr; `isDocumentedBy` (Other)
  * `10.5281/zenodo.22939253` &rarr; `cites` (Dataset)

---

#### Adım 4: Kaydedin ve Yayınlayın (Publish)
1. Sayfanın en altındaki veya üstündeki **Save** (Taslağı Kaydet) butonuna basın.
2. Bilgilerin doğruluğunu kontrol edin.
3. **Publish** butonuna basarak yayını onaylayın.
4. Zenodo size anında kalıcı bir DOI tahsis edecektir: `10.5281/zenodo.XXXXXXX`.

---

### 🎯 Adım 5: Alınan DOI'nin Hibe Başvurusuna Entegrasyonu
DOI tahsis edildiğinde, [`docs/MORPHO_DAO_GRANT_APPLICATION_FINAL.md`](file:///c:/Users/maat/Documents/antigravity/wonderful-raman/docs/MORPHO_DAO_GRANT_APPLICATION_FINAL.md) dosyasındaki ilgili satırı güncelleyeceğiz:
```markdown
**Citable Research DOI:** https://doi.org/10.5281/zenodo.XXXXXXX
**Zenodo Open Science Archive:** https://zenodo.org/records/XXXXXXX
```
Ve başvurumuz, arkasında uluslararası CERN/Zenodo tescilli kalıcı akademik bir makaleyle Morpho DAO forumuna sunulacaktır!
