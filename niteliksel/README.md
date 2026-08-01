# T1DM Niteliksel

> **Migrasyon notu (2026-07-09):** Bu nitel kol artık tek-repo çalışma modeli için
> `/workspaces/T1DM-Tez/niteliksel` altında yönetilir.
> Eski bağımsız kaynak repo korunmuştur; yeni işler için canonical konum bu
> klasördür. `.git/` ve `.env*` dosyaları taşınmamıştır.

## DM Niteliksel Toolkit

Bu kol (niteliksel/), T1DM niteliksel tez çalışmasının analiz ve raporlama süreçlerini desteklemek üzere
`dm_niteliksel_toolkit` adlı yerel bir yardımcı araç içerir. Araç; kod kitabı denetimi, triadik
matris üretimi, COREQ uyum kontrolü, alıntı bütünlüğü, negatif vaka taraması, AI kullanım günlüğü
ve repo-özel Evidentia/life-science-research/Zotero/t1dm-tez yönlendirmesi için tasarlanmıştır.

Araç nitel analizi otomatikleştirmez. Tema geliştirme, yorumlama ve nihai bulgu üretimi araştırmacı
sorumluluğundadır.

Varsayılan modda harici AI veya bulut API çağrısı yapılmaz. Ham veya kimliklenebilir katılımcı
verileri hiçbir harici sisteme gönderilmemelidir.

### Bridge Kullanımı

```bash
./dmnitel ai-context
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
./dmnitel route-tool --query "COREQ ve alıntı bütünlüğü denetimi"
./dmnitel route-tool --query "RTA bilgi gücü için PubMed tam metin taraması"
./dmnitel route-tool --query "HLA genetik mekanizma ve references.bib Zotero eşitleme"
./dmnitel route-tool --query "H5 joint display için nicel-nitel sentez"
```

`ai-context`, ajanlara güvenli çalışma yüzeyini verir: yerel `dmnitel` komutları, Evidentia MCP
çekirdeği, koşullu Life Science Research ve Zotero plugin katmanları, nicel kök yolu,
güvenli repo kanıtları ve korunmuş veri sınırları. `route-tool`, her soru için önce yerel nitel
araçları mı, Evidentia dış-kanıt kaskadını mı, Life Science Research biyomedikal veri katmanını mı,
Zotero kaynakça katmanını mı, yoksa paired `doktoratezi` + `t1dm-tez-rehberi` akışını mı
kullanacağını seçer.

`cross-repo-status`, nitel koldaki ve nicel kökteki güvenli kaynakları tek karma tez yazım haritasında
birleştirir; ham transcript, demografi veya nicel satır düzeyi veri okumaz.

Zotero Web API durum kontrolü (`ZOTERO_API_KEY` `.env`den okunur, anahtar yazdırılmaz):

```bash
python3 scripts/util/zotero_env_bridge.py status --json
python3 scripts/util/zotero_env_bridge.py search "type 1 diabetes family" --json --with-bibtex-keys
python3 scripts/util/zotero_env_bridge.py export-bibtex --out references/references.bib
```

Zotero import/write işlemleri açık araştırmacı onayı gerektirir; BibTeX export, search ve status
read-only kullanım kabul edilir.

Zotero Desktop local API yalnız Zotero uygulamasındaki lokal full-text index, attachment path veya
connector import gibi işler gerektiğinde kullanılır:

```bash
python3 ~/.codex/plugins/cache/openai-curated-remote/zotero/0.1.2/skills/zotero/scripts/zotero.py status --json
```

### Kısa Kullanım

```bash
./dmnitel init
./dmnitel ai-context --output 07_reports/t1dm_ai_tool_bridge.md
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
./dmnitel lint-codebook 02_codebook/codebook.csv
./dmnitel build-triadic-matrix --coded-data 01_deidentified/coded_segments.csv --output 04_triadic_matrices/triadic_matrix.csv
./dmnitel check-quotes --source 01_deidentified/transcripts/ --quotes 06_manuscript_outputs/quotes_used.csv
./dmnitel audit-coreq --methods 06_manuscript_outputs/methods.md --results 06_manuscript_outputs/results.md
./dmnitel log-ai-use --tool "evidentia" --model "mcp-cascade" --purpose "literatür doğrulama" --data-type "anonim/türetilmiş" --output-summary "PMID/DOI doğrulandı" --external-api-used yes
```

Paket kurulu kullanım için `pyproject.toml` içinde `dmnitel` console script tanımlıdır.
