# GAP-Lean 4: Entegrasyon, Lisanslama ve Faz 3 Durum Defteri
**Tarih:** 06 Ekim 2026  
**Durum:** İzole Edildi ve Kaydedildi  
**İlgililer:** @pCwOrM, @Lexovian, @jmikedupont2  

---

## 1. Faz 3 Section 1 (Crown Jewel: GAP-0190) Durumu
* **Modül:** `lib/grpperm.gi:SizePermGroup` — Permütasyon grupları, Sims transversal kelimeleri ve mertebe çarpım kanıtı ($\lvert G \rvert = \prod_{i=1}^k \lvert \Delta_i \rvert$).
* **Doğrulama Durumu:** 0 sorry, 0 admit, saf aksiyomatik Lean 4 (`[propext, Quot.sound]`).
* **Kasa Kimliği:** `VAULT-GAP-PHASE3-SEC1-20261004` altında air-gapped / dormant (uyku modunda) kilitlidir.
* **Yayın Kararı:** Zenodo v0.3.0 DOI ve arXiv v0.3.0 güncellemeleri, Faz 3 Section 2 (`GAP-0247: OrbitPerms, Stabilizer`) ile birleştirilerek tek bir büyük yayın paketi olarak stratejik zamanlamada açılmak üzere bekletilmektedir.

---

## 2. Topluluk ve GitHub Duyuru Stratejisi
* **GAP Depolarındaki Durum:** GAP organizasyonu repo bazlı bloklama uygulamıştır. Bu bloklama GitHub hesap düzeyinde bir yasaklama değildir.
* **İletişim Prensibi:** Polemiklerden ve agresif "show" üslubundan kaçınılacak; tüm duyurular salt akademik, nötr ve kernel doğrulanabilir kanıt referansları üzerinden yapılacaktır.
* **Lexovian Hesabı:** Duyurular gerektiğinde bağımsız akademik araştırmacı kimliğiyle, doğrudan Zenodo DOI ve arXiv linkleri referans verilerek paylaşılacaktır.

---

## 3. Lisans Stratejisi: Dual Licensing (Çift Lisanslama)
* **Açık Katman (Akademik & Saf Matematik):**
  * `Grpperm.lean`, `Stbc.lean`, `Zmodnz.lean` vb. temel matematiksel ispatlar.
  * **Lisans:** MIT / Apache-2.0 / GPLv2 (Mathlib ve akademik atıf uyumu için).
* **Korumalı Katman (Algoritmik Karar Motoru & EVM):**
  * Werracle, Mandelbrot fraktal karar sentezleyicisi, OED ve akıllı sözleşme kernel bileşenleri.
  * **Lisans:** BSL 1.1 (Business Source License) veya BBL.
  * **Kural:** Akademik ve bireysel araştırma serbest; ticari ve zincir üstü üretim ortamları lisansa tabidir.

---

## 4. Mike DuPont (@jmikedupont2) Entegrasyon Matrisi ve İşbölümü
* **Mevcut Durumda Sağlananlar (Statik Katman):**
  * Faz 2 Açık Reposu (`pCwOrM/gap-lean4-port` v0.2.0, 35 teorem).
  * `SharedTerminologyGuide.md` (Rung 0–5 Merdiven Standardı).
  * Zulip üzerindeki mimari şartnameler.
* **İşbölümü Sınırları:**
  * **Mike'ın Yükümlülüğü:** eBPF trace problarını C/C++ düzeyinde yazmak, Nix derivation GAP binary'sine kancalamak (hooking), P2P `lean-worker` düğümlerinde boundary trace altyapısını işletmek.
  * **Bizim Yükümlülüğümüz:** Sadece Lean 4 tarafındaki matematiksel ön/son şartları (Pre/Post/Frame/Degree invariantları) sözleşme olarak tanımlamak.
* **Gelecekteki Otomasyon Adımı (Canlı Task Feed):**
  * Mike'ın daemon'larının görevleri otomatik tüketebilmesi için repoya veya API'ye bir `tasks.json` / `manifest.json` uç noktası bağlanacaktır.
