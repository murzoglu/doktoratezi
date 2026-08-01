# 05 TARTIŞMA ve SONUÇ — Bölüm Finalizasyon Sertifikası (ADAY)

> **Tarih:** 2026-07-13 · **Dal:** `feat/nitel-kanonik-lit-derinlestirme`
> **Durum:** `candidate-final` — **certified-final yalnız açık kullanıcı onayıyla**
> (bolum-sertifika kuralı). Kalan kapanış adımları §Bekleyen'de.
> **Kaynak:** spec `docs/superpowers/specs/2026-07-13-tartisma-sonuc-derin-lit-design.md`;
> plan `docs/superpowers/plans/2026-07-13-tartisma-sonuc-derin-lit.md`.

## İş özeti

Bölüm, tüm bulguları (H1–H5 + [KEŞFİSEL] + nitel 4 tema + karma) en geniş
tam-metin literatürle tartışan akıcı (alt başlıksız) Marmara-uyumlu bölüm olarak
yeniden yazıldı. Literatür 2 Workflow fan-out'uyla toplandı (Faz-A 8 küme D0–D6;
Faz-C 42 künye BibTeX çözümleme), hepsi connector-doğrulanmış.

- Kanıt matrisi: `tez-yazim/02_kanit-haritalari/tartisma-kanit-matrisi.tsv` (79 satır)
- Bölüm: `chapters/05_tartisma_ve_sonuc.qmd` (~3000 kelime, 75 benzersiz atıf)
- Yeni künye: 42 (references.bib'e connector-doğrulanmış eklendi; bib 219 giriş)

## Kapı 0–5 durumu

| Kapı | Durum | Kanıt |
|---|---|---|
| **0 — Kapsam** | ✓ | Yorum bölümü; H1–H5 + keşfisel + nitel + karma kapsandı; bulgu *anlamı* (sunumu değil). |
| **1 — Kanıt** | ✓ | 79-satır kanıt matrisi (benzer 45/boşluk-doldurur 27/farklı 7); iç sayılar CSR+apa_t*'a ankrajlı; dış iddialar connector-doğrulanmış. |
| **2 — Atıf** | ✓ (kısmi) | `bib_hygiene reconcile` HARD atıflı-tanımsız **0**; render **0 çözümsüz atıf** (78 kaynakça girişi); 42 yeni künye DOI/PMID connector-doğrulanmış + claim-destekli. **Bekleyen:** Zotero import + iki-kol AI-reliability (tam `cite-ok`). |
| **3 — Nedensellik sınırı** | ✓ | Nedensellik-dili grep **0**; kesitsel/ilişkisel dil ("ilişkili/öngörüyor") korundu; Maxwell-Cole kesitsel-SEM sınırı açıkça yazıldı. |
| **4 — Karma etiket** | ✓ | Joint display etiketleri (uyum/tamamlayıcılık/ayrışma/açıklayıcı-genişleme); ayrışma teorik katkı olarak okundu; örneklem asimetrisi (241/7) disiplini; nitel tema ≠ nicel etki kanıtı. |
| **5 — Finalizasyon** | ✓ (kısmi) | sci-audit A–G **0 blocker**; axis G sentence-too-long 7→2, Ateşman -2,66→4,19; bölüm-izole render temiz. **Bekleyen:** iki-kol AI-reliability + açık kullanıcı onayı. |

## sci-audit A–G özeti (0 blocker)

- **A (atıf bütünlüğü):** 44 yeni kaynak **iki bağımsız connector fan-out'unda** (Faz-A + Faz-C BibTeX) DOI/PMID ile çözüldü; 31 mevcut key önceden `cite-ok`. Render 0 çözümsüz. Not: bağımsız üçüncü citation-verifier pass'i istenirse çalıştırılabilir.
- **B (kaynaksız iddia):** deterministik taban 0.
- **C (istatistik):** 0 tutarsızlık (bulgu-tekrarı kaçınıldı).
- **D (halüsinasyon sinyali):** 0.
- **E (kılavuz):** tartışma bölümünde zorunlu yapısal bölüm yok.
- **F (AI şeffaflık):** 1 uyarı — bölüm-düzeyi AI-beyanı yok (tez düzeyinde `ai_use_log.csv` ile ele alınır).
- **G (Türkçe bilimsel dil):** 0 hata; 42 tavsiye (okunabilirlik + kısaltma-review info + 3 decimal-dot bölüm-ref yanlış-pozitifi).

## Bekleyen (bölüm kapanışı için)

1. **Zotero mutabakatı (9ZFDHMZA):** 42 yeni künye Zotero kütüphanesine import edilmeli. Mevcut `zotero-refs` araçları var-olan item'ı koleksiyona ekler; BibTeX'ten item oluşturma kütüphane yazımıdır ve **açık kullanıcı onayı** gerektirir. Ledger'da bu künyeler `full-text-ok` (Zotero item-key boş).
2. **İki-kol AI-reliability:** `/tez-dogrulama` (nicel) + `t1dm-qual-ai-audit` (nitel kol) bölüm kapanışında koşulmalı → künyeler `cite-ok`'a yükselir.
3. **Açık kullanıcı onayı:** certified-final için zorunlu.

## Provenans

- Faz-A fan-out: Workflow `w0ig004uh` (8/8, ~2,1M token, 199 araç)
- Faz-C BibTeX fan-out: Workflow `wuvx1ckm2` (7/7, ~1,6M token, 38 araç)
- Commit zinciri: `238025a` (spec) → `dc86ac2` (plan) → `a474037` (matris) → `03d2d88` (taslak) → `f580cfd` (bib+cand) → ledger → `style` (okunabilirlik)

## 2026-07-13 tam-metin somutlaştırma zenginleştirmesi

Kullanıcı direktifiyle her ampirik atıf 'uyumludur' kalıbından çıkarılıp çalışma bağlamı (tasarım+N) + somut sonuçlarla (sayılarla) yeniden dokundu. 41 ampirik referans tam-metin çalışma-kartı fan-out'u (Workflow `w6dgz0jai`, 7/7, ~2M token; 25/41 tam-metin erişildi). Sonuç: 'uyumludur/tutarlıdır' 9 kez; somut sayı işareti 50 kez (g/r/α/ICC/%/p). 3009→4021 kelime. Yeniden doğrulama: sci-audit axis G **0 hata/blocker**; bib_hygiene HARD undefined 0; render 0 çözümsüz atıf (78 kaynakça). Dürüst düzeltmeler ledger'da. **Kalan okunabilirlik:** 51 warning (yoğunluk arttı; tavsiye düzeyi, blocker değil) — istenirse hedefli cümle-bölme geçişi yapılabilir.

## 2026-07-14 — Dört-parçalı denetim + Faz-4 derin-lit zenginleştirme

Kullanıcı direktifi (dört-parçalı Tartışma denetimi): (1) tüm bulguların yorumlanıp
literatür bağlamında tartışılması; (2) CSR güncellemelerinin ch05'e yansıması;
(3) doğruluk/tutarlılık/referans/akış/Marmara/insan-Türkçesi kontrolü; (4) kapılar
geçtikten sonra tam-metin derin-literatür zenginleştirme.

**Kapı 1 — Kapsam (coverage checklist):** `04_bulgular` → `05_tartisma` eşleştirmesi;
H1–H5 + [KEŞFİSEL] katmanlar + nitel 4 tema + karma joint-display'in tümü ch05'te
yorumlanmış olarak doğrulandı; boşluk kalemleri kapatıldı.

**Kapı 2 — CSR→ch05 senkron:** CSR §17 bugünkü zenginleştirmeleri (WS-C 8-boşluk
narratif derin-lit `f4ae14c`; §17.3/§17.5 tam-metin temellendirme `087b3be`; H4
skalar nihai dil + kaynakça hijyeni `d7aef9b`) ch05'e yansıtıldı; sayısal
tutarsızlık taranıp giderildi.

**Kapı 3 — Doğruluk/akış/dil (deterministik):** bib_hygiene HARD atıflı-tanımsız
**0** (render-güvenli); nedensellik-dili grep 4 eşleşme, **hepsi sınırlılık/yöntem
ifadesi** (nedensel iddia yok); gövde alt-başlık **0** (Marmara akıcı-format);
axis G Ateşman **+9,74**, **0 blocker**.

**Kapı 4 — Faz-4 derin-lit fan-out (üç kol, 9 künye):**
- *Seçilim/dönem yanlılığı (Sınırlılıklar):* `hernan2004selectionBias` +
  `luqueFernandez2016paradox` → alım-dönemi caveat'ını yapısal seçilim-yanlılığı
  çerçevesine oturttu.
- *Maternal depresyon → çocuk algısı (H4 köprüsü):* `akdoganDuken2026caregiver`
  (Türk T1DM SEM; r=0,51–0,77; β=0,52–0,66), `abadula2024maternalDepr` (T1DM;
  d=0,48), `esposito2025discrepancy` (bilgi-verici-ıraksak sıcaklık) → Beck≥17
  köprüsünü derinleştirdi.
- *T1DM kardeş (H2 + nitel tema):* `erdim2022siblings` (Türk 54 T1DM-kardeş vs
  200 kontrol, fark yok → H2 null'unu Türkiye örneğiyle destekler),
  `blamires2024umbrella` + `linimayr2025scoping` (vekil-bildirim baskın),
  `litchman2025family` (ebeveynleşme/bakım rolü).

Tam-metin durumu: 4 künye PMC/OA tam-metin (`full-text-ok`), 5 künye künye+tam
abstract doğrulandı (`abstract-doğrulandı`; metne işlenen her sayı abstract'ta
birebir) — ayrıntı ledger `2026-07-14 — Faz-4` bölümünde. Kaçınma-listesi
(elhabashy2023, kirchhofer2025, De Los Reyes, Maxwell-Cole, Lakens,
VanderWeele-Ding) tekrar alınmadı. references.bib 309→317 (8 yeni + `abadula2024`
orphan→atıflı).

**Nihai doğrulama (bu tur):** bib HARD **0**; ch05 **93** benzersiz atıf hepsi
tanımlı; nedensellik gerçek-iddia **0**; alt-başlık **0**; **5** provenans ankrajı;
axis G Ateşman **+9,74**, **0 blocker**; ~5442 kelime.

**Commit:** `8897824` (ch05 + references.bib) + bu sertifika/ledger commit'i.

**Bekleyen (değişmedi):** (1) Zotero item-key import (9 yeni künye; kütüphane
yazımı → açık onay); (2) iki-kol AI-reliability (`/tez-dogrulama` + nitel kol) →
künyeler `cite-ok`'a yükselir; (3) certified-final için açık kullanıcı onayı.
Bölüm durumu **`candidate-final`** olarak kalır.
