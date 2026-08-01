# Klinisyen-Uyarlama İlerleme Planı — ch04 (Bulgular) + ch05 (Tartışma) (2026-07-30)

İş akışı: tek ana ağaç, doğrudan `chapters/*.qmd`, onay-dokümanı/kapısı YOK; her dalga = Claude-authored →
`verify_authored_spans` → 4-mercek adversaryal → doğrudan uygula → grep-teyit → journal.
Standartlar: register v2 ([[klinisyen-uyarlama-register-standardi]]) + Bulgular 4-katman/hibrit-de-dup
([[klinisyen-uyarlama-bulgular-stratejisi]]) + DETAYLI-IZAHAT klinik-çerçeve kaynağı.
Kapsam (ch04/ch05): YALNIZ klinisyen-diline register/sunum düzeltmesi — analiz/sayı/bulgu DEĞİŞMEZ
(DOKUNULMAZ; sayı yalnız yer değiştirebilir: nesir→tablo/dipnot, kayıpsız + tabloda doğrulı).

## ch04 — BULGULAR

- [x] **Strateji + kaynak** — 4 katman + hibrit de-dup + DETAYLI-IZAHAT (belge + bellek).
- [x] **§Örneklem/Ölçek** — 1. şahıs; asiklik graf→nedensel diyagram.
- [x] **H1–H5** — H1 grup-içi grid→tablo de-dup; H4/H5 formül→dipnot + kestirimci→kestirim yöntemi; H2/H3 temiz.
- [x] **Keşifsel dalga-1** — 2023 duyarlılık böl+de-dup; DCA böl; NB formülü→dipnot.
- [ ] **Keşifsel dalga-2 (K2)** — artık-ilişki yüzeyi (§4.4.7) + gelişimsel-diadik yüzeyi (§4.4.8) + meta-forest uzun cümlesi (L1114-15) + within-case gloss (L1410); grid→tablo de-dup + uzun cümle böl.
- [ ] **Nitel dalga (N)** — Tema1–4 + alt-temalar + triadik okuma + çapraz neticeler + negatif vaka; katılımcı ALINTILARI DOKUNULMAZ (verbatim). İzahat destekli manşet/çerçeve. (Çoğu zaten anlatı; hafif register.)
- [ ] **Joint-display + Genel Sentez** — karma köprü (§sec-karma-joint-display) + genel bulgu sentezi; manşet netliği, uyum/tamamlayıcılık/ayrışma etiketleri DOKUNULMAZ.
- [ ] **ch04 KAPANIŞ KAPISI** — `csr_numeric_trace_audit.py` (ch04 yüksek-risk eşsiz=0; de-dup sonrası kalan nesir sayıları izli) + `sci-audit:check-turkish` + `verify-citations` + tam render + W8 iç-içe-`[]` dipnot göz-teyidi + de-dup gridlerinin tabloda fiili tamlığı (PDF-tablo kontrolü).

## ch05 — TARTIŞMA
- [ ] Kapsam taraması (coinage/1.şahıs/uzun-cümle/ağır-gloss); ch05 çoğunlukla yorum nesri → register hafif.
- [ ] Dalga(lar): bulgu-özet cümleleri (sayı yeniden-ifade → csr sürüklenme kapısı K5-NUM-02'ye tabi), nedensel-dil disiplini KORUNUR, formül/mekanik→dipnot.
- [ ] ch05 KAPANIŞ: csr_numeric_trace (ch05) + check-turkish + verify-citations + nedensel-etiket disiplini (K5-CAU-02).

## KAPANIŞ (ikisi de bitince)
- [ ] Tam tez render (freeze/thesis temizle → PDF) + PDF'te uyarlama teyidi.
- [ ] `tez_checklist_verify.py` ilgili eksenler; journal + bellek kapanış girdisi.

## Notlar
- Katılımcı alıntıları (nitel) ve tablo/şekil R-üretimi asla değiştirilmez.
- Her de-dup: sayı ancak ilgili tabloda doğrulanınca nesirden çıkar (kayıpsızlık).
- W8 render-riski: iç-içe `[...]` satır-içi dipnot; kırılırsa referans-dipnota çevir.
