# Yetkinlik ve Araç Mimarisi

Bu mimari tüm Codex, plugin, skill ve MCP seçimlerini resmi tez kılavuzu
merkezli yazım hattına bağlar.

> **Otorite zinciri:** Bu dosya **araç/yetkinlik mimarisinin tek kanonik
> yeri**dir (L0–L4 kaynak katmanı, tool gate, MCP/skill/plugin matrisi, çıkış
> kriterleri). `tez-yazim-ana-plani.md` §2 ve kök `README.md` MCP tablosu buraya
> **işaret eder**, matrisi tekrarlamaz. Devredilen otoriteler: oturum ritüeli →
> `00_kaynak-kurallari/talimatname-claude-code.md` §1; biçim →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`; dış-kanıt kaskadı →
> `01_mimari/evidentia-entegrasyon-cercevesi.md`; tam metin →
> `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md`; referans ledger →
> `02_kanit-haritalari/referans-denetim-ledgeri.md`. Klasör haritası:
> `01_mimari/README.md`.

## Kaynak Öncelik Katmanları

| Katman | Kaynak | Ne için kullanılır |
| --- | --- | --- |
| L0 Resmi kılavuz | `docs/tez-kilavuz/` + kanonik özet `tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` | Format, bölüm sırası, kaynakça, özet, tablo/şekil, ön bölüm. Tüm yazımda zorunlu uyum. |
| L1 Nicel kök | `_targets.R`, `R/`, `tests/`, `docs/protokol/`, `docs/analiz_planlari/`, `chapters/`, `tez-yazim/06_kritik-kaynaklar/` | Veri kontratı, H1-H5, EMBU/Beck/KİA, aggregate sonuçlar, kritik dosya manifesti. |
| L2 Nitel kol | `niteliksel/` güvenli türetilmiş çıktıları | RTA, COREQ, audit trail, tema, triadik matris, seçilmiş anonim alıntı. |
| L3 Dış kanıt | Anamnesis/context, Evidentia/PubMed/OpenAlex/Paper Search, OpenAthens/kurumsal yayıncı erişimi, Minerva (Roche kurumsal korpus), Anna's Library, Zotero, YÖK/ERIC, mevzuat, klinik terminoloji/regülasyon ve teknik delivery MCP kapıları | Bağlam yönetimi, literatür, tam metin, kaynakça mutabakatı, akademik/kurumsal doğrulama, mevzuat ve render/teknik kontrol. |
| L4 Teknik doğrulama | Unit test, iki-kol AI-reliability, promptfoo, Quarto | Tool/agent davranışı, referans güvenilirliği, format ve üretilebilirlik. |

## Varsayılan Tool Gate

1. Yerel repo kuralları: `AGENTS.md`, `CLAUDE.md`, `CONVENTIONS.md`,
   `tez-yazim/README.md`.
2. Tez yazım veya format işi: `tez-yazim/00_kaynak-kurallari/` ve resmi
   `docs/tez-kilavuz` dosyaları.
3. Kritik kaynak seçimi: `tez-yazim/06_kritik-kaynaklar/README.md` ve
   `tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv` dosyaları.
4. Tez yazımı bu repo içinde devam eder; nitel kol yalnız nitel kolun
   ilişkili yöntem, bulgular, joint display, tartışma veya ekler kesiminde
   koşullu kaynak/denetim katmanı olarak açılır.
5. Karma/nitel-nicel denetim gerekiyorsa nitel kolda
   `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md`.
6. Tool seçimi belirsizse nitel kolda `./dmnitel route-tool --query "<soru>"`.
7. Her bölüm başlangıcında bağlam yönetimi: `./dmnitel ai-context`;
   Anamnesis/context araçları yalnız anonim/türetilmiş proje karar bağlamında
   kullanılır.
8. Literatür veya dış claim gerekiyorsa Evidentia MCP çekirdeği en geniş
   kapsamlı kanıt motoru olarak kullanılır; PubMed/OpenAlex/Paper Search,
   OpenAthens kurumsal yayıncı erişimi, Anna's full-text, Zotero ve referans
   ledger kapanışı bu hattı tamamlar. Yapılandırma ve kaskad:
   `01_mimari/evidentia-entegrasyon-cercevesi.md` (t1dm-tez-rehberi çerçevesi).
   Nitel kol çıktısı gerekiyorsa `05_entegrasyon/nitel-cikti-cercevesi.md`
   (niteliksel-arastirma-rehberi-t1dm çerçevesi).
9. Dış referans citation olmadan önce tam metin kaskadı çalışır: önce
   OpenAthens/yayıncı, sonra Minerva (Roche kurumsal korpus, annas öncesi lisanslı
   bant), başarısızsa Anna's Library, ardından PMC/OA/repository ve diğer kanıtlı
   rotalar. Tam metin yoksa ledger'a açık istisna yazılmadan referans kullanılmaz.
   Deterministik yardımcı `scripts/mcp/fulltext_cascade.py` üç tam-metin kaynağını
   (OpenAthens/Minerva/annas) tek koşumda dener. Kanonik:
   `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md`.
10. Kaynakça, citation key veya BibTeX gerekiyorsa Zotero bridge; Zotero item
   key ile BibTeX citation key ayrı tutulur.
11. Referans içeren her bölüm kapanışında nitel ve nicel AI-reliability
    kontrolleri birlikte çalışır.
12. Biyomedikal entity, pathway, farmakoloji veya klinik çalışma gerekiyorsa
    `life-science-research:research-router-skill`.
13. YÖK tezleri, Türkiye akademik bağlamı veya okul/eğitim literatürü gerekiyorsa
   `yoktez-mcp`, `yok-akademik` ve `eric-mcp` görev kapılı kullanılır.
14. KVKK, etik kurul, sağlık mevzuatı veya resmi metin gerekiyorsa `mevzuat`
   ve `mevzuat-bilgisi` yalnız madde/kaynak doğrulaması için kullanılır.
15. İlaç, ATC/RxNorm, ICD/SNOMED, FDA/TITCK veya klinik terminoloji gerekiyorsa
   `openfda`, `med-terminologies`, `nlm-rxnorm`, `nih-clinicaltables`,
   `iuphar-gtopdb`, `drugddx` ve `titck-cache` kaynak doğrulaması için açılır.
16. Render, HTML/PDF, screenshot, GitHub veya platform/tasarım işleri varsa
   `playwright`, `chrome-devtools`, `brave-search`, `github`, `filesystem`,
   `firebase`, `supabase`, `cloudflare-api`, `figma` ve OpenAI API key kapıları
   yalnız açık teknik görevle kullanılır.

## Kullanılacak Yetkinlikler

| Yetkinlik | Kullanım | Sınır |
| --- | --- | --- |
| `t1dm-tez-rehberi` | Tez metni, nicel analiz, Quarto, H1-H5 ve raporlama. | Resmi `docs/tez-kilavuz` format kuralları üstündür. |
| `t1dm-qual-ai-audit` | Nitel kol gizlilik, RTA/COREQ, cross-repo koordinasyon. | Ham transcript veya aile düzeyi hassas veri göndermez. |
| `doktoratezi-ai-audit` | Nicel kök AI reliability, hook, claim grounding, raw-data guard. | İstatistiksel doğruluğu tek başına sertifikalamaz. |
| Anamnesis/context tools | Bölüm oturumu bağlamı, karar geçmişi ve tez çalışma belleği. | Ham transcript, satır düzeyi veri, `.env` veya credential taşımaz. |
| Evidentia MCP | Dış literatür, citation audit, YÖK/OSF/KOL. | Tam metin denetimini OpenAthens/Anna's/Zotero/PMC ile tamamlamadan citation önermez. |
| OpenAthens / Millet Kütüphanesi | Kurumsal yayıncı HTML/PDF tam metin erişimi. | Credential yazdırılmaz; otomasyon yalnız hedefli kaynak için çalışır; lisanslı metin uzun çoğaltılmaz. |
| Minerva (minerva-evidence, Roche korpus) | DOI ile vectorstore tam metni + rominedb makale; OpenAthens sonrası, annas öncesi lisanslı tam-metin bandı. | Yerel stdio köprüsü (`${GRAVITEE_*}`); kimlik/anahtar yazdırılmaz; gateway'e yalnız DOI/başlık gider (KVKK); tam metin anamnesis'e ingest, teze verbatim toplu kopyalanmaz. |
| Anna's Library | DOI/MD5 üzerinden tam metin, OCR, sayfa ve pasaj doğrulaması. | OpenAthens ve Minerva başarısızsa veya yayıncı erişimi yoksa açılır (son çare); Crossref/metadata uyumsuzluğu varsa kaynak durdurulur; telifli metin uzun alıntılanmaz. |
| Zotero | `references.bib`, citation key, kaynakça export/sync, tam metin URL/file attachment ve erişim notu. | Import/write açık onay ister; `.env` anahtarı yazdırılmaz. |
| YÖK/ERIC | YÖK tez, Türkiye akademik bağlamı, okul/eğitim literatürü. | Uzun tam metin kopyalanmaz; yalnız hedefli özet ve citation kanıtı. |
| Mevzuat MCP'leri | KVKK, etik kurul, sağlık mevzuatı, yönetmelik ve tebliğ doğrulaması. | Hukuki tavsiye değil, resmi kaynak doğrulaması. |
| Klinik terminoloji/regülasyon MCP'leri | İlaç, ATC/RxNorm, ICD/SNOMED, FDA/TITCK ve klinik terminoloji. | Hasta düzeyi tedavi önerisi üretmez. |
| Teknik delivery MCP'leri | Quarto render, HTML/PDF, screenshot, GitHub ve dosya operasyonları. | Raw data ve credential dosyaları açılmaz; write işleri açık talimat ister. |
| Platform/design MCP'leri | Firebase, Supabase, Cloudflare, Figma ve API key kurulum işleri. | Tez yazımı için varsayılan değil; yalnız açık teknik görevle. |
| Quarto/R/targets | Tez üretimi, tablo/figür, analiz pipeline. | Veri satırı dökümü yapılmaz. |

## Oturum Başlangıcı

Kanonik oturum ritüeli `00_kaynak-kurallari/talimatname-claude-code.md` §1'dedir
(`/tez-oturum` çalıştırır). Bu bölüm yalnız **araç yüzeyi / kaynak varlık**
kontrolünü tanımlar. Tez yazımıyla ilgili her oturumda:

```bash
cd `git rev-parse --show-toplevel`
test -f tez-yazim/README.md
test -f tez-yazim/06_kritik-kaynaklar/README.md
test -f tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv
test -f docs/tez-kilavuz/'TEZ YAZIM KLAVUZU-2025.pdf'
test -f docs/tez-kilavuz/'TEZ ŞABLONLARI-2026-2RV.docx'
```

Karma yazım veya nitel entegrasyon varsa:

```bash
cd `git rev-parse --show-toplevel`/niteliksel
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
./dmnitel ai-context
```

Araç yüzeyi ve bağlam kapıları kontrolü:

```bash
cd `git rev-parse --show-toplevel`/niteliksel
python3 .codex/tools/codex_mcp_roster_redacted.py | rg '^(anamnesis|annas-reader|evidentia-kb|paper-search|pubmed-epmc|openalex|yoktez-mcp|yok-akademik|eric-mcp|mevzuat|mevzuat-bilgisi|openfda|med-terminologies|nlm-rxnorm|titck-cache|playwright|chrome-devtools|github)\b'
```

Bu kontrol yalnız redacted durum çıktısı üretir; token, `.env` veya ham veri
yazdırmaz.

### Copilot (VS Code) yüzeyi

Aynı yetkinlik matrisi Copilot oturumunda da geçerlidir; yalnız keşif yolları
farklıdır. Oturum başında:

| Katman | Claude Code / Codex | Copilot |
| --- | --- | --- |
| Talimat | `CLAUDE.md`, `AGENTS.md` | aynı + `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` |
| Slash komut | `.claude/commands/*.md` (9) | `.github/prompts/*.prompt.md` (9, birebir parite) |
| Skill | `.claude/skills/` | `.claude/skills/` + `.github/skills/` + `~/.agents/skills/` |
| MCP | `.mcp.json` (Claude), `.ona/mcp-config.json` (Ona) | **`.mcp.json`** (CLI) ve `.vscode/mcp.json` (Chat paneli) — ikisi eş tutulur |
| Zorlama | `.claude/settings.json` hooks + `permissions.deny` | `.github/hooks/hooks.json` (aynı beş hook, Claude sözdizimi) |

```bash
cd `git rev-parse --show-toplevel`
python3 -c "import json;a=json.load(open('.mcp.json'))['mcpServers'];b=json.load(open('.vscode/mcp.json'))['servers'];print('MCP paritesi:', 'TAM' if set(a)==set(b) else 'DRIFT ' + str(set(a)^set(b)))"
diff <(ls .claude/commands | sed 's/\.md$//' | sort) <(ls .github/prompts | sed 's/\.prompt\.md$//' | sort) && echo "slash komut paritesi: TAM"
python3 -c "import json;print('hook paritesi:', 'TAM' if set(json.load(open('.claude/settings.json'))['hooks'])==set(json.load(open('.github/hooks/hooks.json'))['hooks']) else 'DRIFT')"
```

Copilot'ta dikkat edilecek üç davranış farkı:

1. **Skill kaydı oturum başında dondurulur.** Yeni/değişmiş skill için
   `/skills reload` veya yeni oturum gerekir.
2. **Skill `description` bütçesi ~1024 karakterdir.** Aşan skill sessizce
   yüklenmez; bu yüzden tam tetikleyici listesi SKILL.md gövdesinin sonundaki
   "Ek: tam tetikleyici kapsamı (arşiv)" bölümünde tutulur.
3. **`permissions.deny` karşılığı yoktur.** Veri yönetişimi sınırı Copilot
   oturumunda talimat düzeyinde bağlayıcıdır ve `.github/hooks/` PreToolUse
   deny-list'i ile pekiştirilir. Hook yapılandırması oturum başında okunur;
   `.github/hooks/hooks.json` değişirse yeni oturum gerekir.

## Çıkış Kriterleri

- Üretilen metin resmi bölüm sırasına yerleşebiliyor.
- Her içerik iddiası repo kanıtı veya dış kaynakla izlenebiliyor.
- Klinik/nitel rapor, protokol, veri ve ölçek-form kaynakları kritik kaynak
  manifestindeki erişim ve doğrulama kuralına uygun seçilmiş.
- Dış kaynakların her biri `referans-denetim-ledgeri.md` içinde DOI/PMID/ID,
  OpenAthens/Minerva/Anna's Library/PMC/OA veya eşdeğer tam metin kanıtı, Zotero item
  key, attachment/note key, BibTeX key ve claim/pasaj notuyla izlenebiliyor.
- Referans içeren bölüm kapanışında nitel ve nicel AI-reliability kontrolleri
  birlikte geçmiş.
- Sayısal format ondalık virgül ve kılavuz `p` yazımına uygun.
- Kaynakça formatı Enstitü AMA-11 özel biçimine çevrilebilir.
- Nitel ve nicel kanıt türleri karıştırılmamış.
- Ham veri, transcript, `.env` veya credential içeriği taşınmamış.
