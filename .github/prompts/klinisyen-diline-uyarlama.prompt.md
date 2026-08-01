---
description: 'Bir tez pasajını Sosyal Pediatri klinisyen jürisine sade/akıcı/sebep-sonuç-açık dile yeniden üsluplar — üretim portkey-galileo gateway modeli (.env), değerlendirme ayrı; sayı/bulgu/atıf DOKUNULMAZ; kapı + açık onay + journal zorunlu'
mode: agent
---

# /klinisyen-diline-uyarlama — Klinisyen Dili Uyarlama Kapısı (Copilot ikizi)

Uyarlanacak pasaj: **${input:pasaj:uyarlanacak pasaj — ör. chapters/03_gerec_ve_yontem.qmd konumu / seçili metin / @tbl-* çevresi}** — boşsa editör seçimini kullan; o da yoksa netleştir.

> **Copilot uyum notu.** Bu komut Claude Code, Ona ve Copilot'ta aynı metodolojiyi
> izler; yalnız araç katmanı eşlemesi değişir:
>
> 1. **sci-audit HARD kapısı.** `sci-audit` skilleri kuruluysa doğrudan kullanılır.
>    Kurulu değilse aynı HARD güvence repo-yerel araçlarla sağlanır:
>    - `sci-audit:check-turkish --strictness certification`
>      → `python3 scripts/util/tr_corpus_audit.py all --fail-on blocker`
>        (+ ondalık-virgül/nokta-p kapısı: `python3 scripts/util/tez_checklist_verify.py --fast`)
>    - `sci-audit:verify-citations` → `python3 scripts/util/bib_hygiene.py all`
>    - `sci-audit:check-stats` → `python3 scripts/util/claim_certification.py`
>      (+ `python3 scripts/util/csr_causal_label_audit.py`)
>
>    HARD anlamı korunur: herhangi blocker/FAIL = düzelt-ve-tekrar; onay yok.
> 2. **galileo SOFT-block.** `galileo_judge` / `galileo_coherence` /
>    `galileo_reference_prose` araçları `galileo-audit` MCP sunucusundan gelir
>    (Copilot CLI `.mcp.json`, VS Code Chat `.vscode/mcp.json` okur). MCP
>    bağlanmadıysa CLI fallback: `printf '<json>' | python3 scripts/eval/galileo_bridge.py`.
> 3. **Gateway/harness** değişmeden çalışır (probe ok; `.env` kimliği).

## Otomatik toplanan bağlam

Önce şu komutları terminalde çalıştırıp çıktılarını bağlama al:

```bash
# Journal — durum panosu + backlog (SEANS BAŞI ritüeli: oku, sıradakini seç)
head -70 tez-yazim/04_kalite-kontrol/klinisyen-diline-uyarlama-journal.md 2>/dev/null \
  || echo "(journal yok — ilk seans; şablon oluşturulacak)"

# Gateway erişilebilirliği (sır basmaz — yalnız durum)
python3 scripts/eval/gemini_reformulate.py --probe 2>/dev/null || echo "(probe çalıştırılamadı)"

# Skill tanımı (bağlayıcı metodoloji)
head -40 .claude/skills/klinisyen-diline-uyarlama/SKILL.md
```

## Görev

`klinisyen-diline-uyarlama` skill'i
(`.claude/skills/klinisyen-diline-uyarlama/SKILL.md`) bu işte **bağlayıcıdır**.
Skill'i ve beş referansını oku (`references/kaynak-dogrulama.md`,
`hedef-kitle-personasi.md`, `yeniden-uslup-yontemi.md`, `gemini-prompt-sablonu.md`,
`ornek-yeniden-uslup.md`), sonra sırasıyla:

1. **Adım 0 — doğrula (atlanamaz).** Pasajın gerçek dosya:satırını `grep` ile bul
   (dosya adı tahmin etme). DOKUNULMAZ envanteri çıkar (sayı/token/atıf/çekince).
   Sayıları artefakttan teyit et. Journal'ı oku. Kitleyi kalibre et.
2. **Adım 1 — harness üretir.** Envanteri spec'e sınıfla (paragraf başına
   `spans`=atomik sayı/token/etiket, `caveats`=**tam-cümle** çekince + tam-yüklemli
   kapsam öbeği, `note`, `glossary`=yabancı model) →
   `python3 scripts/eval/constrained_rewrite.py < spec.json`. Harness maskeler →
   üretir (portkey-galileo) → **verify/retry** → splice. Register (`default_system`)
   klinik hekim: sayı KALIR, formül→teknik ek, klinik-önce ("poliklinikte" DEME),
   İSTATİSTİK-META/dump/note-echo yasak. Gateway erişilemezse bildir, sessizce yerel
   üretime düşme.
3. **Adım 2 — değerlendir.** `verify.ok` sayı/atıf/token/çekinceyi mekanik garanti
   eder; sen **bağlaç nesrini** denetle: F1 abartı/kapsam · F2 eklenen iddia/gloss ·
   F3 pasif 3. tekil · F4 terim (partner→eş yok) · İSTATİSTİK-META (p/GA tanımı/filler
   yok) · register (poliklinik yok, ondalık virgül) · **dikiş** (run-on, büyük-harf
   maske önü, nokta düşmesi) · note-echo. Kabul / spec düzelt+yeniden koş / 1–4 kelime
   elle onar / reddet.
4. **Tez-geneli bağlam etkisi notu** üret (terim tutarlılığı, çapraz-ref, özet/summary,
   tekrar). Backlog'a takip ekle.
5. **Denetle — UYGULAMADAN ÖNCE** (üç kademe): `check-turkish --strictness certification`
   + `verify-citations` + `check-stats` (HARD) — sci-audit yoksa yukarıdaki **yerel
   ikame**; Bulgular yeniden sıralaması varsa `csr_numeric_trace_audit.py` (HARD);
   `galileo_judge` aday metin üzerinde (SOFT-block, evidence = orijinal pasaj +
   artefakt); `galileo_coherence`/`reference_prose` (advisory). Herhangi HARD/blocker =
   düzelt-ve-tekrar.
6. **Onaya sun:** diff (eski→yeni), üretici model + tur sayısı + çıkan F# bulguları,
   yeniden-sıralama + gerekçe listesi, kapı özeti (+galileo skorları), bağlam-etkisi
   notu, backlog güncellemesi. **Açık kullanıcı onayı olmadan düzenleme/commit yok.**
7. **Onay sonrası:** düzenle → (Bulgular reorder ise tam `tar_make` + numeric-trace) →
   **journal güncelle** (seans günlüğü + pano + backlog) → kapanışta
   `sci-audit:audit chapters/<bolum>.qmd --lang tr` + bölüm kapanıyorsa `/tez-dogrulama`.

**Bağlayıcı:** kanıt DOKUNULMAZ (sayı/yön/anlamlılık/atıf/token/çekince) — üretici model
eklese/değiştirse de reddedilir; kaynak = artefakt, üretici değil; dosyaya doğrudan yazma;
denetimi onaydan sonraya erteleme; KVKK (gateway'e yalnız manuskript/literatür terimi,
asla katılımcı/ham veri).
