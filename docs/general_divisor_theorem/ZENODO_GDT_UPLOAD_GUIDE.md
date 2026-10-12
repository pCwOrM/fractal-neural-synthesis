# Zenodo Upload Guide: Machine-Certified Lean 4 Formalization of the General Divisor Theorem (GDT)

Bu rehber, **General Divisor Theorem (GDT)** Lean 4 makine kanıtı ve monografisinin CERN Zenodo üzerinde kalıcı bir **DOI** ile arşivlenmesi için hazırlanmıştır.

---

## 1. Yazar ve Kurum Bilgileri (Eksiksiz & Sıralı)

Zenodo yükleme ekranında yazarlar **yalnızca** şu şekilde girilecektir:

1. **Volkan Dağlı** (Birinci Yazar / Muhabir)
   - **Family name, given names:** `Dağlı, Volkan`
   - **Affiliation:** `Anadolu University & ITouch Systems, Turkey`
   - **ORCID:** `0009-0000-1587-8703`

2. **Zerrin Dağlı**
   - **Family name, given names:** `Dağlı, Zerrin`
   - **Affiliation:** `Mersin University, Mersin, Turkey`
   - **ORCID:** `0000-0001-9490-6425`

3. **Dağhan Dağlı**
   - **Family name, given names:** `Dağlı, Dağhan`
   - **Affiliation:** `Toros Science College, Mersin, Turkey`
   - **ORCID:** `0009-0003-2492-8313`

> **Önemli Not:** Dan (`thinkthoughts`), bu kanıtın yazarı **değildir**. Kendisi teorinin ilk fikir babası ve makalenin yazarı olarak atıf / referanslar kısmında (`References` ve `Related identifiers`) yer almaktadır.

---

## 2. Temel Yayın Üstverileri (Metadata)

- **Upload type:** `Publication` -> `Preprint` (veya `Software` / `Other`)
- **Title:**
  ```text
  Machine-Certified Lean 4 Formalization of the General Divisor Theorem: Exact Density Correction under Residue Conditioning
  ```
- **Publication date:** `2026-10-12`
- **License:** `Apache License 2.0` (`Apache-2.0`)
- **Language:** `English` (`eng`)

---

## 3. Açıklama / Özet (Description)

Aşağıdaki metni Zenodo **Description / Abstract** kutusuna doğrudan kopyalayıp yapıştırabilirsiniz:

```html
<p>We present an exhaustive, machine-certified formalization of the <b>General Divisor Theorem (GDT)</b> in the Lean 4 interactive theorem prover. Developed originally as a discrete analytic framework by thinkthoughts (2026), the General Divisor Theorem provides exact density corrections for arithmetic coprime residue sets <i>S(N, L, m, a) = {1 ≤ n ≤ L : n ≡ a (mod m), gcd(n, N) = 1}</i> under conditions where the modulus <i>m</i> and constraint <i>N</i> share prime factors.</p>

<p>While naive independent-density heuristics dramatically overestimate or double-count restrictions, GDT isolates the shared-prime radical <i>d = rad(gcd(m, N))</i> and unshared component <i>R = rad(N)/d</i>. We formally construct the exact arithmetic dichotomy in Lean 4: the empty set condition for inadmissible residues (<i>gcd(a, d) &gt; 1</i>), and the exact minimal periodicity <i>T_min = lcm(m, rad(N))</i> possessing exactly <i>φ(R)</i> admissible solutions per period with invariant Euler correction factor <i>C(N, m) = d / φ(d) = ∏_{p|gcd(m,N)} [p/(p-1)]</i>.</p>

<p>All core definitions, factorization lemmas, and specializations (unitary divisors, squarefree primorials) are proven without unadmitted goals (<b>0 sorry</b>). The formal library is complemented by an exhaustive automated Python verification sweep across 2,287 parameter combinations with a 100% pass rate.</p>

<h3>Key Highlights</h3>
<ul>
  <li><b>Target:</b> Lean 4 (v4.21.0) & Mathlib-native foundations</li>
  <li><b>Axioms:</b> Standard Lean 4 core [propext, Classical.choice, Quot.sound]</li>
  <li><b>Concrete Benchmarks Verified:</b> C(6) = 3.00, C(10) = 2.50, C(30) = 3.75 via norm_num</li>
  <li><b>Boundary Cases:</b> Minimal period distinction N=18, m=2 → T_min=6 (≠ 18); Sharp admissibility N=5, m=6, a=2 → d=1 → Admissible</li>
  <li><b>Empirical Validation:</b> 2,287 / 2,287 automated parameter checks PASS (100%)</li>
</ul>
```

---

## 4. Anahtar Kelimeler (Keywords)

```text
Lean 4, General Divisor Theorem, Formal Mathematics, Number Theory, Residue Conditioning, Coprimality, Euler Totient, Mathlib, Interactive Theorem Proving, Machine-Certified Proofs
```

---

## 5. İlgili Tanımlayıcılar (Related / Alternate Identifiers)

| Identifier | Relationship | Resource Type |
| :--- | :--- | :--- |
| `https://github.com/pCwOrM/general-divisor-theorem` | `isSupplementTo` | Software |
| `https://antiviolence.ai/gdt.pdf` | `isDerivedFrom` | Publication / Preprint |
| `https://github.com/thinkthoughts/mathematical-basis` | `references` | Software |
| `10.5281/zenodo.23072120` | `references` | Publication / Preprint |

---

## 6. Yüklenecek Dosyalar (Files)

Zenodo'ya yüklenecek ana dosya seçenekleri:

1. **Monografi PDF (Öncelikli & Görünür Yayın):**
   - [`General_Divisor_Theorem_Lean4_Formalization.pdf`](General_Divisor_Theorem_Lean4_Formalization.pdf) (221 KB)
   - *Yazarlar: Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı*
   - *3 sayfalık eksiksiz akademik makale, infografik ve teorem tablosu içerir.*

2. **Kaynak Kod ve Kanıt Arşivi (Zip):**
   - [`zenodo_gdt_package_v1.0.0.zip`](../../zenodo_gdt_package_v1.0.0.zip) (209 KB)
   - *İçeriği: Lean 4 kaynak kodları (`GeneralDivisorTheorem.lean`), Lake yapılandırması, Python doğrulama betiği, infografik, lisans ve `.zenodo.json`.*

---

## 7. Yükleme Adımları

1. Tarayıcıda [https://zenodo.org/deposit/new](https://zenodo.org/deposit/new) adresine gidin ve giriş yapın.
2. Yukarıdaki 2 dosyayı (`General_Divisor_Theorem_Lean4_Formalization.pdf` ve `zenodo_gdt_package_v1.0.0.zip`) sürükleyip bırakın.
3. PDF dosyasını **Main file / Preview** olarak işaretleyin.
4. Bölüm 1'deki yazar bilgilerini (Volkan Dağlı, Zerrin Dağlı, Dağhan Dağlı) eksiksiz girin.
5. Bölüm 2, 3, 4 ve 5'teki başlık, özet ve anahtar kelimeleri yapıştırın.
6. Lisans olarak **Apache License 2.0** seçin.
7. **Save** ve ardından **Publish** butonuna tıklayın.
8. Zenodo'nun tahsis ettiği yeni **DOI**'yi (`10.5281/zenodo.xxxxxxx`) kopyalayarak külliyatımıza ekleyin.
