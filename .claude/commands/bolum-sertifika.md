---
description: Bölüm finalizasyon sertifikasyonu — Kapı 0-5 denetimi; certified-final yalnız açık kullanıcı onayıyla
argument-hint: "[bölüm adı, ör. 01_giris]"
---

**$ARGUMENTS** bölümü için finalizasyon sertifikasyon sürecini işlet.
Zorunlu playbook: `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
(önce onu oku ve kapı tanımlarını oradan uygula). Kapılar sırayla, atlanamaz:

1. **Kapı 0 — Kapsam/gizlilik**: bölümün kaynak seti `06_kritik-kaynaklar`
   manifestiyle eşleşiyor mu; korumalı veri sınırı ihlali var mı.
2. **Kapı 1 — Derin literatür**: bölümün iddia haritası; eksik/zayıf kanıtlı
   iddialar listesi.
3. **Kapı 2 — Full-text/Zotero/bağlam**: bölümdeki HER referans
   `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` içinde
   `cite-ok` (veya gerekçeli `full-text-exception`) mi.
4. **Kapı 3 — Metin/kılavuz uyumu**: resmi kılavuz + `format-kontrati.md`
   (başlık düzeni, ondalık virgül, tablo/şekil, AMA-11 kaynakça, edilgen dil).
5. **Kapı 4 — Türkçe imla/akış**: imla, terim tutarlılığı, paragraf akışı.
6. **Kapı 5 — AI-reliability/render**: `/tez-dogrulama` PASS + `quarto render`
   exit 0 + nitel kolda `t1dm-qual-ai-audit` (referanslı bölümde çift kapı).

**Semantik/judge katmanı (Şerit B — HARD değil, SOFT/advisory; embedding CANLI):**
Kapı 2'de `python3 scripts/util/thesis_semantic.py bib-dup`; Kapı 3'te `galileo_overclaim_judge` /
`galileo_harking_judge` (Tartışma/prior) + `galileo_convergence_judge` (karma joint-display) +
`python3 scripts/util/karma_ledger_check.py --semantic`; Kapı 4'te `python3 scripts/util/thesis_semantic.py
redundancy` + `galileo_coherence` / `galileo_coherence_judge`.

**Galileo assembly ZORUNLU (2026-07-22 — opt-in DEĞİL):** Bir içerik bölümü `certified-final`
olmadan önce Kapı 3/4 galileo dörtlüsü (`convergence` / `harking` / `overclaim` /
`coherence_judge`) o bölüm için (ve varsa her joint-display satırı için) çalıştırılmalıdır.
Tam-tez taraması: `python3 scripts/eval/run_full_thesis_judge.py --out
outputs/reports/galileo_full_thesis_judge.json` (checklist `K5-GAL-01` bu artefaktın tazeliğini
advisory raporlar). **Karar kuralı:** eşik-üstü bir galileo SOFT-block bulgusu, Gap Register'a
**yazılı gerekçe** (neden kabul edildiği / nasıl giderildiği) düşülmeden `certified-final`
YAZILAMAZ (gerekçesiz SOFT-block = en fazla `provisional-pass`). Gateway erişilemezse bu bir
SKIP'tir (uydurma yok) ve sertifikada açıkça not edilir. **HARD asla judge'dan gelmez** —
HARD yalnız sci-audit + hook + bib `--strict` + `tez_checklist_verify` deterministik-eşik.
Detay: `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` §galileo.

Karar kuralı:
- Tüm kapılar PASS **ve kullanıcı açık onay verdiyse** →
  `tez-yazim/04_kalite-kontrol/sertifikalar/<bölüm>-sertifika-<tarih>.md`
  dosyasına `Durum: certified-final` sertifikası yaz (mevcut GİRİŞ sertifikası
  formatını şablon al).
- Teknik kapılar geçse bile açık onay yoksa en fazla `provisional-pass` yazılır.
- Herhangi bir kapı FAIL ise `blocked` + Bloklayıcı Hata Sözlüğü'ne göre
  gerekçe ve düzeltme planı yazılır; Gap Register
  (`tez-yazim/01_mimari/tez-yazim-ana-plani.md`) güncellenir.
