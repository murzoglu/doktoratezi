# Giriş (01) Bölümü — Dış Sayısal İddia Doğrulama İzi (2026-07-21)

`chapters/01_giris_ve_amac.qmd` denetimi kapsamında, bölümün üç dış sayısal
iddiası `referans-kapisi`/evidentia akışıyla (DOI çözümleme → tam-metin/abstract →
claim eşleştirme) bağımsız doğrulandı. Tezdeki değerler kaynaklarla **tam uyumlu**;
metinde değişiklik gerekmedi (kanıt bölgesi dokunulmadı).

| Künye | DOI | Kaynak (Crossref) | Doğrulanan sayı(lar) — tez ↔ kaynak | Yöntem | Sonuç |
|---|---|---|---|---|---|
| `ogle2022idfAtlas` | 10.1016/j.diabres.2021.109083 | Diabetes Res Clin Pract 2022;183:109083 (IDF Atlas 10th ed) | <15 yaş **108.300** ✓ · <20 yaş **149.500** ✓ (2021 yeni tanı) | Crossref ✓ + Europe PMC abstract | `cite-ok` |
| `yesilkaya2016turkiyeIncidence` | 10.1111/dme.13063 | Diabetic Medicine 2017;34:405–410 | prevalans **0,75/1000** (%95 GA 0,74–0,76) ✓ · yaşa-standardize insidans **10,8/100.000** (%95 GA 10,1–11,5) ✓ | Crossref ✓ + tam metin (Anna's Archive) | `cite-ok` |
| `chen2023parentDepression` | 10.3389/fendo.2023.1095729 | Front Endocrinol 2023;14:1095729 (PMID 36936139) | ebeveyn geneli **%22,4** (GA 17,2–28,7) ✓ · anneler **%31,5** ✓ · küçük yaş grubu daha yüksek (%32,3 vs %16,0) ✓ | Crossref ✓ + Frontiers OA tam metin | `cite-ok` |

## Ek bulgu — §3 kıtasal konumlandırma kaynak-destekli

Giriş §3'teki "Türkiye'yi Asya'dan yüksek, Avrupa'dan düşük bir insidans kuşağında
konumlandırmaktadır" ifadesi, `yesilkaya2016turkiyeIncidence`'ın kendi sonuç
cümlesiyle birebir desteklenmektedir ("*the incidence … being higher than in Asia
but lower than in Europe*"). Kaynak zaten cümlenin öncesinde atıflı; ek atıf veya
yumuşatma gerekmedi.

## Not
- Bu üç künye `references/references.bib`'de mevcut; doğrulama yeni aday atıf
  üretmedi — dosya-içi değişiklik yok.
- KVKK: doğrulama sorgularına yalnız literatür terimi gönderildi.
- İlgili oturum: Giriş denetimi + `simonsohn2015specification` → `simonsohn2020specificationCurve`
  VoR taşıması (bkz. `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`).
