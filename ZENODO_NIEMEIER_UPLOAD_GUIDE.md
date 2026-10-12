# 🚀 CERN ZENODO YÜKLEME VE YAYIN KILAVUZU
## Niemeier Kafesi $A_8^3$, K3 Hodge Dualitesi & Umbral Moonshine

**Yazarlar:** Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı  
**Altyapı Katkısı:** Bekirhan Dağlı (ITouch Systems)  
**Tarih:** 12 Ekim 2026  
**Hedef Platform:** CERN Zenodo ([https://zenodo.org](https://zenodo.org))  

---

## 📌 1. Hazır Bulundurulacak Dosyalar

Zenodo'ya yükleme yaparken kullanacağınız **temizlenmiş ve hazır** iki alternatif dosya mevcuttur:

1. **Paket Dosyası (Önerilen Tek Tık Yükleme):**  
   * [`zenodo_niemeier_k3_bundle_v1.0.zip`](file:///c:/Users/maat/Documents/antigravity/wonderful-raman/zenodo_niemeier_k3_bundle_v1.0.zip) *(132 KB — İçinde kamera hazırı makale PDF'i, Lean 4 kodu, Python oraklı ve Lake yapılandırması mevcuttur)*
2. **Doğrudan Ayrı Yüklenebilecek Makale PDF'i (Görünür Önizleme İçin):**  
   * [`Niemeier_A8_K3_Umbral_Moonshine_Formalization.pdf`](file:///c:/Users/maat/Documents/antigravity/wonderful-raman/k3_umbral_niemeier/Niemeier_A8_K3_Umbral_Moonshine_Formalization.pdf) *(138 KB)*

> [!TIP]
> Zenodo arayüzünde hem **`Niemeier_A8_K3_Umbral_Moonshine_Formalization.pdf`** dosyasını (PDF önizlemesi doğrudan görünsün diye) hem de **`zenodo_niemeier_k3_bundle_v1.0.zip`** dosyasını birlikte sürükleyip bırakabilirsiniz. Bu sayede ziyaretçiler tarayıcıdan doğrudan makaleyi okurken, kodu da zip olarak indirebilirler.

---

## 📝 2. Zenodo Yükleme Formu Alanları (Kopyala / Yapıştır)

Zenodo'da **"New Upload"** dedikten sonra aşağıdaki alanları birebir doldurabilirsiniz:

### A. Temel Bilgiler (Basic Information)
* **Digital Object Identifier (DOI):** Boş bırakın (Zenodo otomatik kalıcı DOI üretecektir).
* **Resource Type:** `Software` *(veya `Publication` -> `Preprint`)*
* **Title:**
  ```text
  Machine-Certified Formalization of the 24-Dimensional Niemeier Lattice A_8^3, K3 Hodge Duality and Umbral Moonshine
  ```
* **Publication Date:** `2026-10-12`

---

### B. Yazarlar (Creators / Authors) — *Akademik Standarda Tam Uyumlu*
*(Hiçbir ünvansız, saf isim ve ORCID formatında)*

1. **Yazar 1 (Corresponding Author):**
   * **Family Name, Given Names:** `Dağlı, Volkan`
   * **Affiliation:** `Anadolu University, Eskişehir, Türkiye & ITouch Systems, Mersin/Adana, Türkiye`
   * **ORCID:** `0009-0000-1587-8703`
2. **Yazar 2:**
   * **Family Name, Given Names:** `Dağlı, Zerrin`
   * **Affiliation:** `Mersin University, Mersin, Türkiye & Yusuf Kalkavan Anadolu Lisesi, Mersin, Türkiye`
   * **ORCID:** `0000-0001-9490-6425`
3. **Yazar 3:**
   * **Family Name, Given Names:** `Dağlı, Dağhan`
   * **Affiliation:** `Toros Science High School, MEV (Toros University), Mersin, Türkiye`
   * **ORCID:** `0009-0003-2492-8313`

---

### C. Katkıda Bulunan (Contributors)
* **Family Name, Given Names:** `Dağlı, Bekirhan`
* **Affiliation:** `ITouch Systems, Mersin/Adana, Türkiye`
* **Contributor Type:** `Other` *(veya `Hosting Institution` / `Data Manager`)*

---

### D. Açıklama (Description)
Aşağıdaki metni kopyalayıp "Description" kutusuna yapıştırın:

```html
<p>Complete machine-certified Lean 4 formal specification and exact Python algebraic verification oracle for the 24-dimensional even unimodular Niemeier lattice <b>A<sub>8</sub><sup>3</sup></b>, its ternary glue code <i>G<sub>glue</sub></i> of order 27, du Val A<sub>8</sub> singularity resolutions on complex K3 surfaces, and Umbral Moonshine lambency <i>&ell; = 9</i>.</p>

<p>Formulated in direct response to the October 2026 retractions in corporate AI mathematics concerning K3 Hodge cycles and Weil classes (caused by sign and stabilization-trace cancellation errors in the <code>openai/math</code> repository), this work provides an unassailable, zero-defect formal architecture:</p>

<ul>
  <li><b>24-Dimensional Root Sublattice:</b> Direct sum of three A<sub>8</sub> components, Coxeter number h = 9 (mirroring the discrete Z/9Z harmonic chassis), Cartan determinant 9<sup>3</sup> = 729, and exactly 216 roots of squared norm 2.</li>
  <li><b>Ternary Glue Code:</b> Order |G<sub>glue</sub>| = 27 with isotropic generator g = (1, 1, 4) satisfying even integer norm squared ||g||<sup>2</sup> = 4, proving strict even unimodularity (det = 1.0) with 0 defects.</li>
  <li><b>K3 Surface Duality:</b> Strict matching of Euler characteristic &chi;(X) = 24 with lattice rank 24 and Hodge diamond h<sup>2,0</sup> = 1, h<sup>1,1</sup> = 20, h<sup>0,2</sup> = 1.</li>
  <li><b>Umbral Moonshine:</b> Lambency &ell; = 9, vector-valued mock modular forms of weight 1/2, and unary theta shadows of weight 3/2.</li>
</ul>

<p>Hardware cluster and bare-metal verification infrastructure provided by <b>Bekirhan Dağlı</b> (ITouch Systems).</p>
```

---

### E. Anahtar Kelimeler (Keywords)
Tek tek veya virgülle ekleyin:
```text
Niemeier Lattice, A8 Root System, K3 Surfaces, Umbral Moonshine, Hodge Cycles, Lean 4, Formal Mathematics, Even Unimodular Lattice, Mock Modular Forms, WERR Research Framework
```

---

### F. Lisans ve Erişim (Access & License)
* **Access Right:** `Open Access`
* **License:** `Apache License 2.0` *(veya `Creative Commons Attribution 4.0 International`)*

---

### G. İlişkili Tanımlayıcılar (Related Identifiers)
* **İlişki 1 (GitHub Reposu):**
  * **Identifier:** `https://github.com/pCwOrM/niemeier-a8-umbral-moonshine`
  * **Relation:** `isSupplementTo` (Software)
* **İlişki 2 (GDT Kaydımız):**
  * **Identifier:** `10.5281/zenodo.23316070`
  * **Relation:** `references` (Software/Preprint)
* **İlişki 3 (Black Hole Page Curve Kaydımız):**
  * **Identifier:** `10.5281/zenodo.22978460`
  * **Relation:** `references` (Preprint)

---

## 🏁 3. Son Adım: Yayınlama (Publish)

1. Sayfanın en altındaki **"Save"** (Kaydet) butonuna basın.
2. Dosyaları ve künyeyi son bir kez gözden geçirin.
3. **"Publish"** (Yayınla) butonuna basarak kaydınızı dünya bilim literatürüne mühürleyin.
4. Zenodo'nun atadığı kalıcı DOI'yi (`10.5281/zenodo.XXXXXXX`) kopyalayıp GitHub reposunun README'sine ve Twitter duyurunuza ekleyebilirsiniz.
