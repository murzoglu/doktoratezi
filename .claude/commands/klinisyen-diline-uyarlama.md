---
description: Bir tez pasajını Sosyal Pediatri klinisyen jürisine sade/akıcı/sebep-sonuç-açık dile yeniden üslupla — üretim portkey-galileo gateway modeli (.env; şu an GPT-5.5), değerlendirme Claude; sayı/bulgu/atıf DOKUNULMAZ; kapı+onay+journal
argument-hint: "[uyarlanacak pasaj — ör. chapters/03_gerec_ve_yontem.qmd konumu / seçili metin / @tbl-* çevresi]"
allowed-tools: Bash(grep *), Bash(sed *), Bash(nl *), Bash(head *), Bash(awk *), Bash(python3 scripts/eval/constrained_rewrite.py*), Bash(python3 scripts/eval/gemini_reformulate.py*), Bash(python3 scripts/util/tr_corpus_audit.py*), Bash(python3 scripts/util/bib_hygiene.py*), Bash(python3 scripts/util/claim_certification.py*), Bash(python3 scripts/util/csr_causal_label_audit.py*), Bash(python3 scripts/util/csr_numeric_trace_audit.py*), Read
---

<!--
ONA-UYUM NOTU (bu komut hem Claude Code hem Ona'da kullanilir)
==============================================================
Ona (Gitpod) ortaminda calisma modeli Claude Code'dan farklidir; komut ayni
metodolojiyi izler ama arac katmani su sekilde eslesir:

1. SLASH-INVOKE: Ona'da `.claude/commands/*.md` dosyalari `/komut` olarak
   dogrudan cagrilmaz; skill'ler ACIKLAMA-ESLESMESI ile otomatik tetiklenir
   (bkz. skills.md). "klinisyen diline uyarla / juriye sadelestir" gibi bir
   istek `.claude/skills/klinisyen-diline-uyarlama/SKILL.md`'yi otomatik acar.
   Bu komut dosyasi Ona'da ek REFERANS/checklist islevi gorur.

2. sci-audit HARD KAPISI -> ONA-YEREL IKAME. `sci-audit` bir Claude Code
   plugin'idir (sci-audit@cureonics-marketplace) ve Ona'da MEVCUT DEGILDIR.
   Ayni HARD guvenceyi Adim 5'te repo-yerel araclarla saglа:
     - sci-audit:check-turkish --strictness certification
         -> python3 scripts/util/tr_corpus_audit.py all --fail-on blocker
            (+ ondalik-virgul/nokta-p kapisi: python3 scripts/util/tez_checklist_verify.py --fast)
     - sci-audit:verify-citations
         -> python3 scripts/util/bib_hygiene.py all
     - sci-audit:check-stats
         -> python3 scripts/util/claim_certification.py
            (+ python3 scripts/util/csr_causal_label_audit.py)
   HARD anlami korunur: herhangi blocker/FAIL = duzelt-ve-tekrar; onay yok.

3. galileo SOFT-block -> Ona MCP. `galileo_judge`/`galileo_coherence`/
   `galileo_reference_prose` tool'lari `.ona/mcp-config.json`'daki galileo-audit
   MCP sunucusundan gelir (Ona `.ona/mcp-config.json` okur; `.mcp.json` degil).
   MCP baglanmadiysa CLI fallback: printf '<json>' | python3 scripts/eval/galileo_bridge.py.

4. GATEWAY/HARNESS Ona'da degismeden calisir (probe ok; .env kimligi).
-->


## Otomatik toplanan bağlam

### Journal — durum panosu + backlog (SEANS BAŞI ritüeli: oku, sıradakini seç)
!`head -70 tez-yazim/04_kalite-kontrol/klinisyen-diline-uyarlama-journal.md 2>/dev/null || echo "(journal yok — ilk seans; şablon oluşturulacak)"`

### Gemini gateway erişilebilirliği (sır basmaz — yalnız durum)
!`python3 scripts/eval/gemini_reformulate.py --probe 2>/dev/null || echo "(probe çalıştırılamadı)"`

### Skill tanımı (bağlayıcı metodoloji)
!`head -40 .claude/skills/klinisyen-diline-uyarlama/SKILL.md`

## Görev

Şu pasajı klinisyen jüriye uyarla: **$ARGUMENTS** — argüman boşsa editör seçimini
(`ide_selection`) kullan; o da yoksa netleştir.

`klinisyen-diline-uyarlama` skill'i (`.claude/skills/klinisyen-diline-uyarlama/SKILL.md`) bu
işte **bağlayıcıdır**. Skill'i ve beş referansını oku (`references/kaynak-dogrulama.md`,
`hedef-kitle-personasi.md`, `yeniden-uslup-yontemi.md`, `gemini-prompt-sablonu.md`,
`ornek-yeniden-uslup.md`), sonra sırasıyla:

1. **Adım 0 — Claude doğrular (atlanamaz).** Pasajın gerçek dosya:satırını `grep` ile bul
   (dosya adı tahmin etme). DOKUNULMAZ envanteri çıkar (sayı/token/atıf/çekince). Sayıları
   artefakttan teyit et. Journal'ı oku. Kitleyi kalibre et.
2. **Adım 1 — harness üretir.** Envanteri spec'e sınıfla (paragraf başına `spans`=atomik
   sayı/token/etiket, `caveats`=**tam-cümle** çekince + tam-yüklemli kapsam öbeği, `note`,
   `glossary`=yabancı model) → `python3 scripts/eval/constrained_rewrite.py < spec.json`. Harness
   maskeler → üretir (portkey-galileo) → **verify/retry** → splice. Register (`default_system`)
   klinik hekim: sayı KALIR, formül→teknik ek, klinik-önce ("poliklinikte" DEME), İSTATİSTİK-META/
   dump/note-echo yasak. Gateway erişilemezse bildir, sessizce Claude'a düşme.
3. **Adım 2 — Claude değerlendirir.** `verify.ok` sayı/atıf/token/çekinceyi mekanik garanti eder;
   sen **bağlaç nesrini** denetle: F1 abartı/kapsam · F2 eklenen iddia/gloss · F3 pasif 3. tekil ·
   F4 terim (partner→eş yok) · İSTATİSTİK-META (p/GA tanımı/filler yok) · register (poliklinik yok,
   ondalık virgül) · **dikiş** (run-on, büyük-harf maske önü, nokta düşmesi) · note-echo. Kabul /
   spec düzelt+yeniden koş / 1–4 kelime elle onar / reddet.
4. **Tez-geneli bağlam etkisi notu** üret (terim tutarlılığı, çapraz-ref, özet/summary,
   tekrar). Backlog'a takip ekle.
5. **Denetle — UYGULAMADAN ÖNCE** (üç kademe): `sci-audit:check-turkish --strictness
   certification` + `verify-citations` + `check-stats` (HARD) — **Ona'da sci-audit yoksa yerel
   ikame** (bkz. üstteki ONA-UYUM NOTU §2): `tr_corpus_audit.py all --fail-on blocker` +
   `bib_hygiene.py all` + `claim_certification.py`; Bulgular yeniden sıralaması varsa
   `csr_numeric_trace_audit.py` (HARD); `galileo_judge` aday metin üzerinde (SOFT-block, evidence
   = orijinal pasaj + artefakt; Ona'da galileo-audit MCP veya `galileo_bridge.py` CLI fallback);
   `galileo_coherence`/`reference_prose` (advisory). Herhangi HARD/blocker = düzelt-ve-tekrar.
6. **Onaya sun:** diff (eski→yeni), Gemini modeli + tur sayısı + çıkan F# bulguları,
   yeniden-sıralama + gerekçe listesi, kapı özeti (+galileo skorları), bağlam-etkisi notu, backlog
   güncellemesi. **Açık kullanıcı onayı olmadan Edit/commit yok.**
7. **Onay sonrası:** Edit → (Bulgular reorder ise tam `tar_make` + numeric-trace) → **journal
   güncelle** (seans günlüğü + pano + backlog) → kapanışta `sci-audit:audit
   chapters/<bolum>.qmd --lang tr` + bölüm kapanıyorsa `/tez-dogrulama`.

**Bağlayıcı:** kanıt DOKUNULMAZ (sayı/yön/anlamlılık/atıf/token/çekince) — Gemini eklese/
değiştirse de reddedilir; kaynak = artefakt, üretici değil; dosyaya doğrudan yazma; denetimi
onaydan sonraya erteleme; KVKK (gateway'e yalnız manuskript/literatür terimi).
