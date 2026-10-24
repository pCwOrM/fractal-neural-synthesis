# CERN Zenodo Güncelleme (Edit) ve Yayın Rehberi
## Empirical OEV & Liquidation Dynamics: 98.10% Value Recapture in Chainlink SVR Auctions and Structural MEV Power-Law Distribution on Ethereum L1

**Canlı Zenodo Kaydı:** [https://zenodo.org/records/23623589](https://zenodo.org/records/23623589)  
**Çatı DOI:** [`https://doi.org/10.5281/zenodo.23623588`](https://doi.org/10.5281/zenodo.23623588)  
**Hugging Face Dataset:** [https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026](https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026)

---

## ⚡ 1. Stratejik Karar: Neden "Yeni Versiyon" Değil de "Edit" (Düzenleme)?

> [!IMPORTANT]
> **En İdeal ve Temiz Bilimsel Karar: Mevcut kaydı "Edit" (Düzenle) yaparak güncellemektir.**

1. **DOI Değişmez:** Zenodo'da kayıtlı bir yayını "Edit" yaptığınızda metadata (açıklama metni, ilişkili linkler) güncellenir ancak **DOI numarası (`10.5281/zenodo.23623588` / `23623589`) birebir aynı kalır**.
2. **Versiyon Karmaşası Önlenir:** Hibe başvurumuzda, GitHub repomuzda ve Hugging Face kartımızda bu DOI tescillenmiştir. Yeni versiyon (Version 2) çıkarmak gereksiz bir alt-DOI türetir; oysa dosyalarımız (PDF monograf, JSON veri seti, doğrulama kodları) zaten sıfır hatalıdır.
3. **DataCite Standartlarına Tam Uyum:** Zenodo kurallarına göre dosya değişimi gerekmedikçe harici veri platformu bağlantıları (Hugging Face vb.) metadata düzenlemesiyle aynı kayda eklenir.

---

## 🛠️ 2. Zenodo'yu 2 Dakikada Güncelleme Adımları

### Adım 1: Kayıt Sayfasına Gidin ve "Edit"e Basın
1. Tarayıcınızda doğrudan şu linki açın:  
   👉 [https://zenodo.org/records/23623589](https://zenodo.org/records/23623589)
2. Giriş yapmış durumdayken sağ üstte yer alan turuncu **"Edit"** (Düzenle) butonuna tıklayın.

### Adım 2: Description (Açıklama) Kutusunu Güncelleyin
1. Klasördeki `zenodo_oev_liquidation_package/zenodo_description.html` dosyasının içeriğini kopyalayın.
2. Zenodo düzenleme sayfasındaki **Description** alanını silip bu güncel HTML metnini yapıştırın.  
   *(Bu metin tepeye Hugging Face interaktif bağlantısını ve Python kullanım örneğini ekler).*

### Adım 3: Related Identifiers (İlişkili Bağlantılar) Alanına Hugging Face'i Ekleyin
Sayfayı aşağı kaydırıp **Related works / identifiers** bölümüne gelin:
* **Identifier:**  
  ```text
  https://huggingface.co/datasets/pCwOrM/werracle-oev-liquidation-dataset-2026
  ```
* **Relation:** `is supplemented by this resource` (veya `isSupplementedBy`)
* **Resource type:** `Dataset`

*(Mevcut GitHub ve diğer linkler kalmaya devam edecektir).*

### Adım 4: Kaydedin ve Yayınlayın (Publish)
1. Sayfanın en üstündeki **"Save"** (Kaydet) butonuna basın.
2. Ardından **"Publish"** (Yayınla) butonuna basarak onaylayın.
3. Zenodo sayfanız anında güncellenecek, DOI numaranız hiç bozulmadan hem CERN arşivinde hem de Hugging Face'te birbirine çift taraflı bağlanmış olacaktır!

---

## 📦 Dosya Bilgileri & Arşiv Özeti (Referans)

* `Empirical_OEV_and_Liquidation_Dynamics_Research_Monograph.pdf` (3 sayfalık kamera-hazır PDF)
* `EMPIRICAL_OEV_AND_LIQUIDATION_RESEARCH_2026.md` (Markdown monograf)
* `zenodo_bundle_oev_liquidation_empirical_research.zip` (184 KB)
* `data/werracle_oev_empirical_dataset_2026.json` (1.157 doğrulanmış işlem)
* `scripts/verify_dataset_metrics.py` (15 ampirik değişmez testi)
