# Üç Faz Denetimi ve Hata Tespiti (23 Ekim 2026 - 05:30)

Üç fazda doğru işler de var, ama herkese açık yayında ciddi hatalar duruyor.

## Kritik: kurtarma simülasyonu geçersiz ve şu an yayında
- **Seçilen pozisyonlar kurtarılabilir değil:** Panodaki "Rescue Shield" sekmesinde ve `/v1/radar/rescue-simulation` ucunda gösterilen 20 "kurtarmanın" 20'si de sağlık faktörü 0,03 civarında olan pozisyonlar. Örneğin bir USR/USDC pozisyonunda borç 24,5 milyon $, teminat 0,77 milyon $. Bunlar kurtarılabilecek pozisyonlar değil, zaten batmış kötü borç. "40 bin $ ücret, 96 bin $ tasarruf, yıllık 25 bin $ gelir" rakamlarının hepsi bu yanlış seçimden çıkıyor.
- **Hesap tutmuyor:** Sağlık faktörü 1,02 olan bir pozisyonda borcun %12,5'ini teminat satarak kapatmak sağlık faktörünü 1,25'e değil, yaklaşık 1,04'e çıkarır. Makaledeki 11,2 WETH örneği de aynı hatayı taşıyor.
- **Yetki atlanmış:** Akışta "borçludan teminat çek" adımı var. Morpho'da bu, borçlunun açıkça yetki vermesini gerektiriyor. Ne simülasyon ne makale bundan bahsediyor; aynı işi zaten yapan Morpho ön-likidasyonu da anılmıyor.
- **İki doğrulanmamış iddia:** "Binance, Chainlink'ten 15–45 saniye önde" hiçbir ölçüme dayanmıyor; bizim Base ölçümümüzde fark 2–3 saniyeydi. Ayrıca Base'de halka açık mempool yok, "işlem mempool'a sunulur" ifadesi yanlış.

## Araştırma makalesi
**Doğru kısımlar:** Base SVR tablosu (105 işlem, değerin %98,1'i protokole, %1,9'u solver'a, medyan marj −%1,5), 0x8b61… botuyla ilgili düzeltme ve metodoloji sınırları bölümü.

**Düzeltilmesi gerekenler:**

| Makalede yazan | Veride olan |
|---|---|
| "L1 likidasyonlarının %72'si toz (net <1 $)" | Bu sayı builder'a ödenen tutarı ölçüyor; likidasyonun değerini değil. Veride builder ödemesi <1 $ olan işlem 848 (%81). L1 brüt değeri hiç ölçülmedi. |
| "Searcher gelirinin neredeyse tamamı builder'a gidiyor (%99,4)" | Ölçülmedi. Medyan builder ödemesi 0,08 $; bu, çoğu L1 likidasyonunda builder'a çok az ödendiğini gösteriyor. |
| "22 büyük olay 317.467 $" | 317.467 $, Aave v3'ün 133 işleminin toplamı. En büyük 22 işlemin toplamı 344.156 $. |
| p75 4,21 $, p99 1.842 $ | p75 0,56 $, p99 2.639 $ |
| "Onaylı (certified) solver'lar" | Atlas'a katılım izinsiz. |
| Tarih aralığı 9–23 Ekim | Base verisi ağırlıkla 12–19 Ekim. |

"Likidasyon avcılığının ölümü" başlığı veriyi aşıyor: tek bir volatil hafta ve yalnızca SVR olan pazarlar ölçüldü. 4. ve 5. bölüm (kalkan ve CEX öncülüğü) bulgu değil, test edilmemiş öneriler; ya çıkarılmalı ya da "hipotez" olarak yazılmalı.

## Veri seti ucu
- `/v1/radar/dataset` ucu 131 SVR kaydı gösteriyor. Bunların 23'ü hâlâ eski, hatalı brütle; yalnızca doğrulanmış 108 kayıt kullanılmalı.
- Uçta toz oranı %80,8, makalede %72,2 yazıyor; ikisi birbirini tutmuyor.

## Morpho gölge servisindeki yama
- **Gizli bir hata eklenmiş:** Stabil para listesine WETH, cbBTC ve cbETH eklenmiş. Servis bu listedeki borçları 1 $ sayıyor. Bir sonraki tam taramada WETH borçlu pazarların borcu ve brütü yaklaşık 2.400 kat düşük hesaplanır. Servis şu an önbellekten çalıştığı için hata henüz devrede değil; ama geri alınmalı.
- **Bu kısım doğru:** Bilinmeyen borçluyu yarış anında izleme listesine ekleme düzeltmesi.
- **Mühürlenmemiş:** Değişiklik mühürlenmemiş; kasa kontrolü 1 sapma gösteriyor.

## answerr-api servisi
Ana servis dosyası hâlâ değiştirilemez olarak kilitli ve içinde API'yi dışarı açan `0.0.0.0` ayarı duruyor. Şu an benim eklediğim ayar dosyası sayesinde API yalnızca sunucunun içinden dinliyor (4 worker). Kilit kaldırılıp ana dosya `127.0.0.1`'e çekilmeli.

## Önerilen Uygulama Sırası
1. **Hemen:** Rescue sekmesi ve `/rescue-simulation` ucu yayından kaldırılsın. Ya da yalnızca gerçekten riskteki pozisyonlarla (sağlık faktörü 1,0–1,05, teminat borçtan büyük) yeniden üretilsin ve "hipotetik model" diye etiketlensin.
2. Makalenin L1 bölümü verilere göre düzeltilsin; 4. ve 5. bölümler hipotez olarak yeniden yazılsın.
3. Stabil para listesindeki değişiklik geri alınsın ve Morpho servisi mühürlensin.
4. answerr-api ana servis dosyasının kilidi kaldırılıp `127.0.0.1`'e çekilsin.
