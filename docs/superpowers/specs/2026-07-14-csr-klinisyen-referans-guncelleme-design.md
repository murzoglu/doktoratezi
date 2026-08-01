# CSR Güncelleme — Klinisyen Zenginleştirme + Referans Bağlama (Tasarım/Spec)

**Tarih:** 2026-07-14 · **Hedef belge:** `docs/CLINICAL-STUDY-REPORT-FINAL.md` (7280 satır, Quarto)
**Durum:** onaylandı (kullanıcı: "uygun") — uygulama planına hazır
**Bağlayıcı kaynaklar:** `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md`, `tez-yazim/README.md`, `docs/tez-kilavuz/`, `/referans-kapisi` (7-adım atıf kapısı)

---

## 0. Amaç ve kapsam

CSR'ye dört güncelleme, aşağıdaki kullanıcı direktifiyle:
1. Tablo-şekil-diyagram numaralandırma + her birinin altına açıklama metni.
2. Nihai dil kontrolü.
3. Klinisyen-odaklı anlatım zenginleştirme (istatistik ağırlığını hafifletmek; daha açıklayıcı, klinisyen gözüyle).
4. Referansları metine bağla.

**Onaylanan yaklaşım kararları:**
- Referans: **Quarto bib-wiring + `[@key]`** (manuel çift-yönlü değil).
- Zenginleştirme: **alt-açıklama + bölüm-girişi** (yalnız biri değil).
- Kapsam: **§9–§17** (sonuç/yorum ağırlıklı bölümler).

**Recon durumu (diskten doğrulandı):**
- Numaralandırma **büyük ölçüde mevcut**: 30 `**Şekil N.N**` kalın-caption, ~24 `Tablo N.N` (§9–§17 aralığında).
- Metin-içi `[@key]` = **0**; `bibliography`/`csl` YAML **yok**; refs §21.3/§21.4/Ek B'de manuel APA + ~25 düz-metin "Yazar, YYYY".
- `references.bib` = 219 kayıt, **kısmi** kapsam (Helgeson/Sharpe/Cousino/Cinelli/Olsen/Enders var; Buist/Cameron/Wysocki/Rumburg yok).
- `references/apa.csl` mevcut.
- CSR figürleri **gömülü veri çerçevesi** kullanır (0 canlı `read.csv`/`tar_read`) → **bağımsız render edilebilir**; bib-wiring standalone render'da etki eder.

---

## 1. WS-A — Referans sistemi (bib-wiring + `[@key]`)

**A1. YAML.** CSR front-matter'a ekle:
```yaml
bibliography: ../references/references.bib
csl: ../references/apa.csl
```
(Yollar `docs/`'ten görelidir.)

**A2. Metin-içi dönüşüm.** ~25 düz "Yazar, YYYY" mention → `[@key]`. Her mention için:
- references.bib'de eşleşen anahtar varsa onu kullan.
- Yoksa → **A4 kuyruğuna** (eksik künye).

**A3. Kaynakça bölümü.** §21.3/§21.4/Ek B manuel listeleri tek Quarto-üretimli `# Kaynaklar` (`::: {#refs}`) listesine dönüştürülür. Kategorizasyon (metodolojik / Türkiye-özgü / açık-bilim) kısa nesir başlık-notu olarak korunur; ama tam liste tek doğruluk kaynağı `references.bib`'ten üretilir. Yalnız arka-plan olarak listelenip metinde geçmeyen künyeler için `nocite` kullanılır (kaybolmasınlar).

**A4. Eksik künye kapısı (GATE).** Metin-içi veya §21 listesinde olup references.bib'de olmayan her künye:
- **`/referans-kapisi`** ile DOI + tam-metin + Zotero doğrulaması + iki-kol AI-reliability.
- Doğrulanırsa references.bib'e eklenir (`bib_hygiene.py` ile temiz-mutabakat).
- **Doğrulanamayan künye eklenmez** ("VERİ BULUNAMADI" → düşer; ilgili metin-içi iddia kaynaksız kalamaz → ya alternatif doğrulanmış kaynak ya iddia yumuşatma).

**A5. Sınır.** Yeni bilimsel iddia eklenmez; yalnız MEVCUT mention'lar bağlanır + eksik künyeler doğrulanır. references.bib'e eklenen her künye commit'te gerekçelenir.

---

## 2. WS-B — Numaralandırma denetimi + caption

**B1.** Mevcut `Şekil N.N` / `Tablo N.N` şeması korunur (yeniden numaralamaz).
**B2.** §9–§17 taranıp **numarasız veya caption'sız** kalan tablo/şekil/diyagram (§8.6 DAG dâhil, kapsam kenarı) tespit edilir ve tamamlanır.
**B3.** Caption biçimi ev-stiliyle tutarlı: `**Şekil N.N. <başlık>.**` / `**Tablo N.N. <başlık>.**` (kalın, nokta ile).
**B4.** "Diyagram" = şekil olarak ele alınır (Şekil N.N).

---

## 3. WS-C — Klinisyen zenginleştirme (§9–§17)

**C1. Alt-açıklama.** Her tablo/şekil caption'ının altına kısa **"Klinik yorum:"** paragrafı (~2–4 cümle):
- O tablodaki/şekildeki **gerçek** sayıyı klinik anlama çevirir.
- **Sayı uydurma YOK** (Davranış Kuralı): her yorum ilgili tablo/şekilden okunan değere dayanır; yeni sayı/etki/iddia üretmez.
- Nedensel dil yok (kesitsel); "ilişkili", "algılanan", "bu örneklemde".
- Örnek kalıp: "Klinik yorum: Reddetme boyutundaki bu fark (d ≈ …) klinikte, diyabetli çocuğun anne tutumunu akranından daha olumsuz algılayabileceği anlamına gelir; bu, öz-bildirime ek olarak çocuk perspektifinin sorulmasını destekler."

**C2. Bölüm-girişi çerçeve.** §9–§17'nin yoğun bölüm başlarına 1 kısa klinisyen-okuması paragrafı: "Bu bölüm klinikte şunu yanıtlar…" / "Sayıların ötesinde pratikte…". İstatistik gövdesi korunur; klinik köprü önüne/çevresine eklenir.

**C3. Denge.** Amaç istatistiği SİLMEK değil, klinik yorum katmanıyla **erişilebilir** kılmak. Her ağır sayısal paragrafın klinik "ne demek" karşılığı olur.

**C4. Kapsam listesi (§9–§17):** §9 popülasyon/betimleyici, §10 psikometri, §11 birincil hipotez (H1–H5), §12 aracılık, §13 sağlamlık, §14 Bayes, §15 keşifsel-ikincil, §16 bağlamsal, §17 tartışma. (§16.16/§16.17 zaten klinik-okuma cümleleri taşıyor — tutarlılık için gözden geçirilir.)

---

## 4. WS-D — Nihai dil + render doğrulama

**D1. Nihai dil.** Tüm CSR'de:
- Faz/sürüm/aşama/süreç-anlatısı sıfır-kalıntı taraması (önceki turda §16.16/16.17 + omurga temizlendi; yeni eklenen metinde tekrar).
- sci-audit **Axis G** (Türkçe stil, ondalık virgül, register) — 0 blocker hedefi.
- sci-audit **Axis C** (yeni "Klinik yorum" sayıları tablo/şekildeki ile tutarlı mı) + **Axis B** (yeni atıflar grounded mı).
**D2. Render.** `quarto render docs/CLINICAL-STUDY-REPORT-FINAL.md` → exit 0; atıf çözümleme + caption + `# Kaynaklar` üretimi görsel doğrulanır.

---

## 5. Yürütme sırası ve aşamalar

Tek turda bitmez (~54 klinik yorum + referans dönüşümü). Sıra:
1. **WS-A** (referans altyapısı + eksik künye kapısı) — çünkü render + atıf zeminini kurar.
2. **WS-B** (numaralandırma boşlukları) — hızlı.
3. **WS-C** bölüm-bölüm: §9 → §10 → §11 → §12 → §13 → §14 → §15 → §16 → §17. Her bölüm sonunda ara-doğrulama (sayı-tutarlılık).
4. **WS-D** (nihai dil + render) — kapanış.

Her aşama sonunda kısa ilerleme raporu; büyük olduğundan çok-turlu.

---

## 6. Başarı ölçütleri (kabul kriterleri)

- [ ] CSR YAML'da `bibliography` + `csl`; metin-içi düz "Yazar, YYYY" mention'ları `[@key]`'e dönüştürülmüş (0 kaynaksız düz-metin klinik iddia).
- [ ] Eksik künyeler `/referans-kapisi`'ndan geçmiş; references.bib'e yalnız doğrulanmış künye eklenmiş; `bib_hygiene.py all` exit 0.
- [ ] §9–§17'deki her tablo/şekil/diyagram numaralı + caption'lı + altında "Klinik yorum".
- [ ] §9–§17 bölüm başlarında klinisyen-okuması çerçevesi.
- [ ] Klinik yorumlarda sıfır uydurma-sayı (Axis C tablo-tutarlı); nedensel dil yok.
- [ ] Faz/süreç sıfır-kalıntı; Axis G 0 blocker.
- [ ] `quarto render` exit 0; kaynakça + caption'lar üretiliyor.

## 7. Sınırlar / kapsam-dışı

- H1–H5 doğrulayıcı çekirdek, kanonik kilit, mevcut sayısal sonuçlar **DEĞİŞMEZ**.
- §1–§8 (giriş/yöntem/etik) ve §18–§22 klinik-zenginleştirme kapsam-dışı (yalnız WS-A referans + WS-D dil dokunur).
- Yeni analiz/veri yok. certified-final yalnız açık kullanıcı/danışman onayıyla (bu spec kapsamı dışı).
