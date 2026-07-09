# TALİMATNAME — Tez Yazım Süreci (Claude Code, Doktoratezi)

Sürüm: 1.0 · 2026-07-02 · Kapsam: doktoratezi reposundaki **tüm tez yazım,
bölüm, format, referans, render ve karma sentez oturumları**.

Bu belge bir öneri değil, **zorunlu uyulması gereken talimatnamedir**.
Nitel koldaki eş talimatname:
`/mnt/thunderbolt/workspaces/T1DM Niteliksel/00_context/TALIMATNAME_TEZ_YAZIM.md`.
Codex tarafında aynı süreci `CONVENTIONS.md` + `.codex/hooks/` zorlar. Tez
sürecinin araç envanteri:
`/mnt/thunderbolt/workspaces/T1DM Niteliksel/00_context/TOOL_ECOSYSTEM_MAP.md`.

## 0. Bağlayıcılık ve zorlama katmanları

| Katman | Mekanizma | Ne zorlar |
|---|---|---|
| Deterministik-dosya | `.claude/settings.json` → `permissions.deny` | `data/raw|identified|cleaned|backup/**` tam kapalı; `data/processed` ve `outputs` altında satır-düzeyi formatlar (csv/tsv/rds/parquet/xlsx) kapalı — `.lock` ve veri-haritası metadata dosyaları okunabilir; `_targets/**` kapalı; credential dosyaları kapalı |
| Deterministik-Bash | `.claude/hooks/pre_tool_use_policy.py` | Yıkıcı komutlar, `git add .`, ham `codex mcp list`, korumalı yolların shell/interpreter/kopya erişimi |
| Deterministik-prompt/çıktı | `user_prompt_submit.py` + `post_tool_use_review.py` | Sır kalıpları bloklanır/işaretlenir |
| Deterministik-kapanış | `stop_verify.py` | Kaynaksız sayısal iddia varsa tur kapanmaz; kaynak = URL/DOI/PMID/atıf yılı **veya repo dosya yolu** |
| Model-düzeyi | Bu talimatname + `CONVENTIONS.md` + `tez-yazim/` playbook seti | Rota disiplini, resmi kaynak önceliği, referans kapısı, sertifikasyon |

Politika değişikliği iki harness ağacına birlikte işlenir
(`.claude/hooks` ↔ `.codex/hooks`) ve `tests/test_claude_hooks.py` +
`plugins/doktoratezi-ai-audit/.../test_repo_ai_reliability.py` ile korunur.

## 1. Oturum ritüeli (her tez oturumunda zorunlu)

1. `/tez-oturum "<görev>"` çalıştır — tez-yazim README başı, kritik kaynak
   haritası, bölüm brief listesi ve git durumu otomatik gelir.
2. Görevin bölümünü/rotasını açıkça bildir; ilgili briefi
   (`tez-yazim/03_bolum-hazirlik/`) ve kanıt eşlemesini
   (`tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv`) aç.
3. Resmi kaynak önceliği: `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf` +
   `TEZ ŞABLONLARI-2026-2RV.docx` → kanonik biçim otoritesi
   `tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` (özeti
   `format-kontrati.md`) → repo kanıtı. Tüm yazımda kanonik talimatnameye zorunlu
   uyum sağlanır. Biçim/bölüm-sırası çakışmasını resmi kılavuz + kanonik
   talimatname çözer; analiz/veri çakışmasını repo kanıtı (`_targets.R`, testler,
   CSR) çözer.
4. Üretim eşlemesi: yazım `thesis.qmd` + `chapters/0X_*.qmd`'de yapılır;
   `tez-yazim/` operasyon katmanıdır, tez metni oraya yazılmaz.
5. Nitel kanıt gerekirse kanonik kaynak
   `docs/niteliksel/qualitative_canonical_results_report.md`; ham transcript ve
   nitel repo geniş taraması default değildir. Nitel metodoloji sorusu →
   `niteliksel-arastirma-rehberi-t1dm` skill; nicel pipeline sorusu →
   `t1dm-tez-rehberi` skill (`.claude/skills/t1dm-tez-rehberi/`).
6. Karma tez / joint display: nitel repoda `/capraz-repo` köprü raporu +
   `tez-yazim/05_entegrasyon/nitel-nicel-joint-display-plan.md`. Nitel kol çıktı
   çerçevesi (RTA/COREQ/quote-integrity/KVKK): `tez-yazim/05_entegrasyon/
   nitel-cikti-cercevesi.md`. Dış literatür/citation Evidentia hattı:
   `tez-yazim/01_mimari/evidentia-entegrasyon-cercevesi.md`.

## 2. Veri sınırı — ihlal edilemez

- Satır düzeyi içerik, aile-düzeyi detay, demografi satırı, PII **bağlama
  dökülmez, memory'ye yazılmaz, hiçbir harici MCP/RAG/connector'a gönderilmez**.
- Kanonik analiz bazına dokunmadan önce
  `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` ve
  `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` okunur (metadata; serbesttir).
- Veri işi targets pipeline'ı ve aggregate çıktılar üzerinden yürür; "ham
  CSV'den ilk N satırı göster" tarzı istekler şema/aggregate önerisiyle
  reddedilir (promptfoo golden-case sözleşmesi).
- `outputs/fulltext_cache/` telif-kapılıdır; içerik dışarı aktarılmaz.

## 3. Yazım kontratları (özet — tam metin `format-kontrati.md`)

- Türkçe, edilgen 3. tekil; Times New Roman 12 pt; 1,5 satır aralığı;
  ondalık **virgül** (`p<0,001`); AMA-11 alfabetik kaynakça.
- Resmi bölüm sırası: ÖZET, SUMMARY, GİRİŞ ve AMAÇ, GENEL BİLGİLER, GEREÇ ve
  YÖNTEM, BULGULAR, TARTIŞMA ve SONUÇ, KAYNAKLAR, ÖZGEÇMİŞ, BİLİMSEL
  FAALİYETLER, EKLER.
- Bulgular yorumsuz; post-hoc analiz birincil sonuç gibi yazılmaz; nitel tema
  nicel estimate gibi sunulmaz; ham alıntı dökümü yok — triadik kanıt
  (anne / T1DM'li çocuk / sağlıklı kardeş) ayrı ayrı etiketlenir.

## 4. Zorunlu referans kapısı

Her dış referans `/referans-kapisi` ile 6 kapıdan geçer: bağlam →
bibliyografik kimlik → tam metin → Zotero (item key ≠ BibTeX key) →
claim/pasaj → ledger + çift AI-reliability. Ledger:
`tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`. Kapı kapanmadan
referans `chapters/*.qmd` veya `references/references.bib`'e girmez.

## 5. Bölüm sertifikasyonu

Bölüm kapanışı `/bolum-sertifika` ile Kapı 0–5 üzerinden yürür
(`tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`).
`certified-final` yalnız tüm kapılar PASS **+ kullanıcının açık onayı** ile
yazılır; onay yoksa `provisional-pass`. FAIL → `blocked` + Gap Register kaydı.

## 6. Doğrulama paketi ve iş bitirme kriterleri

Kapanışta `/tez-dogrulama`:

```bash
# Manüskript adli denetimi + Türkçe imla (sci-audit — kanonik):
/sci-audit:audit chapters/<bolum>.qmd --lang tr --strictness certification
/sci-audit:check-turkish chapters/<bolum>.qmd --strictness certification

# Repo/veri invaryantı (KVKK/ham veri/quote-parity — sci-audit DIŞI):
Rscript tests/test_reproducibility_lock.R
Rscript tests/test_final_reference_loading.R
Rscript tests/test_data_governance.R
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
python3 -m py_compile .codex/hooks/*.py .claude/hooks/*.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/test_claude_hooks.py
# render kapanışı: quarto render (exit 0)
```

AI-reliability katman sınırı: **manüskript metni adli denetimi (referans/claim/
istatistik/halüsinasyon/kılavuz/AI-şeffaflık/Türkçe imla) yalnız `sci-audit`'te**;
**KVKK/ham veri/quote-parity/kanonik kilit yalnız repo ai-audit plugin'lerinde**.
İki katman çakışmaz (detay: `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`).

İş "tamam" sayılmaz, eğer: kaynaklar dosya yoluyla izlenebilir değilse; veri
sınırı ihlal edildiyse; gerekli test exit 0 değilse; referanslı bölümde çift
AI-reliability (bu repo + nitel repo) koşulmadıysa; harici MCP kullanımı nitel
repodaki `./dmnitel log-ai-use` günlüğüne yazılmadıysa; kullanıcı istemeden
stage/commit/push yapıldıysa.

## 7. Talimatname bakımı

Değişiklik önce burada, sonra nitel ikizde ve `CONVENTIONS.md`'de yapılır;
hook davranışı değişiyorsa iki hook ağacı + testler birlikte güncellenir.
Çelişki sırası: kullanıcının açık talimatı → bu talimatname → diğer repo notları.
