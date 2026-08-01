# Klinisyen-Uyarlama Register Standardı (v2 — 2026-07-30)

Kullanıcı geri bildirimiyle (¶139 üzerine: "çok uzun cümleler, çok fazla parantez tanımı, çizge gibi
anlamsız kelimeler") kilitlenen, D1–D6-A'ya geriye dönük + tüm ileri dalgalara uygulanan register
standardı. Bu standart, "yalnız cümle böl, her şeyi aynen koru" hafif-dokunuşunun üstüne **derin klinik
yeniden-kurma** katmanını ekler. **Sayı/atıf/çekince/etiket her hâlde mutlak korunur (DOKUNULMAZ).**

## İlke 1 — Opak Türkçe coinage sadeleştirmesi (kapsam: kullanıcı onayı)
Klinisyene geçmeyen Türkçe karşılıklar sade karşılıkla değiştirilir. **Onaylı kapsam:**
| ESKİ (opak) | YENİ (sade) |
|---|---|
| çizge / nedensel yönlü çizge | **nedensel diyagram** (ilk geçiş: *Directed Acyclic Graph*, DAG; kısaltmalar listesi Türkçe genişletmeyi taşır) |
| kestirimci | **kestirim yöntemi** |
| yordam | **işlem / yöntem** |
| kovaryat | **KALIR** (çekirdek terim; ilk geçişte klinik karşılık "ayarlama değişkeni (kovaryat)" verilebilir; tez-geneli tutarlılık için değiştirilmez) |

ch03'te terim tek-biçim olmalı (çizge → tüm 3 geçiş: ¶139, ¶123 R-listesi, ¶177 hizalanır).

## İlke 2 — Ağır glossa → Quarto dipnotu (`^[...]`)
İtalik-İngilizce özgün ad + uzun tanım içeren ağır parantez-glossaları gövdeden **dipnota** taşınır.
**RBŞ kilidi:** Dipnot YALNIZ kaynağın metinde ZATEN var olan glossa'sını **birebir** taşır; asla yeni
tanım/özellik uydurmaz. Kaynakta yalnız terim adı varsa (tanım yoksa) dipnot açılmaz — terim gövdede
kalır. Sayı/atıf/çapraz-referans/çekince parantezleri (ör. `(SMD ≈ 0,21; …)`, `(bkz. @fig-…)`,
`(IPTW)`) **gövdede kalır**, dipnota taşınmaz.

## İlke 3 — Uzun cümle bölme (≥ ~45 kelime hedefi)
İç-içe, çok yüklemli uzun cümleler kısa bildirim cümlelerine bölünür. Governing fiil tekrarı gerekirse
kaynağın fiiliyle yapılır (eşanlamlı geçiş yok — F4). Yeni bağlaç/gerekçe eklenmez (F2).

## Emsal (¶139 nedensel çıkarım çerçevesi)
- "nedensel yönlü çizge" → "nedensel diyagram (*Directed Acyclic Graph*, DAG)"; gövdede çizge = 0.
- 3 ağır glossa dipnota: `*backdoor set*`, `*point-identified*`, `*propensity score*` (üçü de kaynağın
  birebir tanımı). `*selection node*` (kaynakta tanım yok → gövdede kalır), `*doubly robust*`
  (kaynağın inline betimi gövdede kalır).
- Uzun zincirler bölündü. `verify_authored_spans` PASS (20 span); DOKUNULMAZ tam.

## Doğrulama hattı (her rev alt-birim için)
1. `verify_authored_spans` — DOKUNULMAZ span'leri (dipnottaki italik terimler dahil) korundu mu.
2. 4-mercek adversaryal (sadakat-RBŞ · eklenen-iddia · Marmara-register · DOKUNULMAZ-tamlık).
3. grep-teyit: gövdede opak-coinage = 0; dipnot sayısı = beklenen; ana dosya git-temiz.
4. Onay-taslak sun → onay → Edit (`03_..._new.qmd`; ana dosya dokunulmaz).
