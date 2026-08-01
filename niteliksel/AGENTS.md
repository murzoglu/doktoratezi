# AGENTS.md - T1DM Niteliksel Ajan Rehberi

> **Migrasyon notu (2026-07-09):** Bu dosyanın canonical kopyası artık
> `/workspaces/T1DM-Tez/niteliksel` altındadır.
> Eski `/workspaces/T1DM-Tez/niteliksel` repo yolu tarihsel kaynak
> olarak korunur; yeni nitel işlemler bu alt-ağaçtan yürütülmelidir.

Bu depo Tip 1 Diyabet karma doktora projesinin niteliksel koludur. Yazılım uygulaması değil;
anne, T1DM'li çocuk ve sağlıklı kardeş triadlarına ait nitel araştırma korpusu, analiz belgeleri,
tez/makale taslakları ve yerel belge-denetim araçlarından oluşur.

## Öncelik Sırası

1. Önce `CLAUDE.md`, sonra `00_context/TRACKER.md`, `00_context/REPO_CONTEXT.md` ve
   `00_context/CODEX_PLAYBOOK.md` oku; Codex işlemlerinde playbook'u ana operasyonel kaynak kabul et.
2. Niteliksel işlerde ana gate `niteliksel-arastirma-rehberi-t1dm` mantığıdır: RTA, COREQ/SRQR,
   JARS-Qual, KVKK, refleksivite, audit trail ve triadik anne-cocuk-kardes yorum çerçevesi.
3. Tez yazımı, format, bölüm sırası, özet/summary, tablo/şekil veya kaynakça işi varsa nicel kök
   `/workspaces/T1DM-Tez/tez-yazim` giriş noktasını ve
   `/workspaces/T1DM-Tez/docs/tez-kilavuz` resmi kaynaklarını üst kural kabul et.
   Bundan böyle tez yazımının ana operasyon merkezi nicel köktür; bu
   kol (niteliksel/) yalnız nitel kolun ilişkili tez kesimleri için kaynak/denetim katmanı olarak açılır.
4. Nicel R pipeline, H1-H5, EMBU/Beck/KIA analizleri veya karma tez joint display gerekiyorsa
   nicel kök `/workspaces/T1DM-Tez`, `tez-yazim` ve `t1dm-tez-rehberi` ile koordine et.
5. Dış literatür, citation audit, tam metin, YÖK tez, OSF/PsyArXiv veya KOL gereksiniminde
   Evidentia v1.7.0 `medical-research` v8.5.0 native-first hattını kullan; web/OSINT
   fallback yoktur, yapısal kaynakta bulunamayan veri gap olarak yazılır. Anna's
   Library/annas-reader copyright-gated tam metin fallback katmanıdır. Ham katılımcı
   verisini connector'a gönderme.
6. Manüskript adli denetimi, bölüm sertifikasyonu ve Türkçe bilimsel yazım/imla işlerinde
   `sci-audit@cureonics-marketplace` v0.2.0 kullan; doktoratezi
   `tez-yazim/04_kalite-kontrol` Kapı 4/5 kuralları üstündür. Eski repo-local
   `tr_sciaudit.py` veya `.venv-tr-sciaudit` scaffold'u kurma. Sci-audit
   KVKK/ham veri/quote-parity denetimi değildir; bu invaryantlar `dmnitel`,
   `t1dm-qual-ai-audit` ve `doktoratezi-ai-audit` katmanında kalır.
7. Araç seçimi belirsizse önce `./dmnitel route-tool --query "<soru>"`; kapsamı sabitlemek için
   `./dmnitel ai-context` çalıştır.
8. Genetik, varyant, protein, pathway, farmakoloji, klinik çalışma, omics/public dataset veya
   mekanistik T1DM biyolojisi varsa `life-science-research` plugin router'ını koşullu kullan.
9. Bağlam yönetimi, Anamnesis/context ve bellek araçları yalnız anonim/türetilmiş proje karar
   bağlamı için kullanılır; ham transcript, demografi satırı, `.env` veya credential taşınmaz.
10. Zotero, yalnız kaynak kütüphanesi, citation key, `references.bib`, BibTeX/RIS veya lokal
   full-text index işleri için kullanılır. Headless search/export için `scripts/util/zotero_env_bridge.py`
   `.env` içindeki `ZOTERO_API_KEY` değerini okur; anahtarı asla yazdırma. Zotero import/write
   işlemleri açık onay gerektirir.
11. Teze girecek her dış referans DOI/PMID/ID, Anna's veya eşdeğer tam metin kanıtı, Zotero item
    key, BibTeX citation key ve claim/pasaj notuyla ledger'a bağlanır; referanslı bölüm kapanışı
    nitel ve nicel AI-reliability kontrolleri birlikte geçmeden tamam sayılmaz.
12. Diğer MCP'ler görev kapılıdır:
    `yoktez-mcp`/`yok-akademik` Türkiye tez ve akademik bağlam için,
    `eric-mcp` eğitim/okul literatürü için, `mevzuat`/`mevzuat-bilgisi` resmi
    mevzuat doğrulaması için, klinik terminoloji/regülasyon MCP'leri yalnız
    terminoloji ve kaynak doğrulaması için, teknik MCP'ler ise yalnız render,
    GitHub veya platform işleri için açılır.

## Gizlilik ve Veri Sınırı

- `01_raw_data/`, `02_processed/transcripts/`, `.remember/` ve aile/rol düzeyinde hassas içerik
  özel nitelikli sağlık + çocuk verisidir.
- Ham görüşme, birleşik transcript, demografi satırı, onam/protokol kişisel içeriği ve aile düzeyi
  hassas ayrıntı memory'ye veya harici MCP/RAG'e aktarılmaz.
- Raporlama yalnız anonim aile/rol kodu ve araştırmacı tarafından seçilmiş, temizlenmiş alıntı ile yapılır.
- `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md` aktif yazım kaynağıdır; uzun
  ham alıntı dökme, sadece hedefli bölüm düzenleme yap.

## Araç Yüzeyi

- Yerel toolkit: `dm_niteliksel_toolkit` ve `./dmnitel`.
- Tez yazım merkezi: `/workspaces/T1DM-Tez/tez-yazim/README.md`.
- Nitel kol rolü: kanonik nitel sonuç raporunun, RTA/COREQ/audit trail
  kanıtlarının ve anonim alıntı kontrollerinin gerektiği bölümlerde koşullu
  destek; genel tez yazım operasyonu bu kolda (niteliksel/) sürdürülmez.
- Agent/tool bridge: `./dmnitel ai-context`, `./dmnitel route-tool --query "<soru>"`,
  Anamnesis/context gate ve
  `./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md`.
- Test: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests`.
- MCP roster kontrolü: `python3 .codex/tools/codex_mcp_roster_redacted.py`.
- Görev kapılı MCP sınıfları: Anamnesis/memory/qdrant/sequentialthinking,
  Evidentia/PubMed/OpenAlex/Anna's, YÖK/ERIC, mevzuat, klinik
  terminoloji/regülasyon, render/browser/GitHub ve platform/design.
- Zotero Web API durum kontrolü: `python3 scripts/util/zotero_env_bridge.py status --json`.
- Zotero Desktop local API durum kontrolü: `python3 ~/.codex/plugins/cache/openai-curated-remote/zotero/0.1.2/skills/zotero/scripts/zotero.py status --json`.
- Ham `codex mcp list` kullanma; stdio argümanlarında token yazdırabilir.
- Harici Evidentia/Anna's/Anamnesis/Zotero/Codex/MCP kullanımı sonrası
  `./dmnitel log-ai-use ... --external-api-used yes`
  ile LLM kullanım günlüğüne kayıt düş.

## Kod ve Belge Değişikliği

- Toolkit kodu değişirse önce `tests/` altındaki en dar unittest'i, sonra tüm discover komutunu çalıştır.
- Tez/metodoloji belgesi değişirse `00_context/TRACKER.md` fazı ve ilgili audit trail bağı güncel mi kontrol et.
- `git add .` kullanma; dosyaları adıyla stage et.
