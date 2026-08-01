# T1DM Niteliksel Çalışma Bağlamı

Güncelleme: 2026-08-01

Bu dizin, `doktoratezi` üst reposunun nitel araştırma alt-ağacıdır. Git,
bağımlılık ve çalışma kökü üst repodan yönetilir; tarihsel taşıma ayrıntıları
`MIGRATION_TO_DOKTORATEZI_2026-07-09.md` içindedir ve güncel çalışma kuralı değildir.

## Amaç ve Sınır

- Tasarım: nitel tanımlayıcı/fenomenolojik duyarlılık, çoklu-bilgi-kaynağı aile
  yaklaşımı, Braun ve Clarke refleksif tematik analiz ve COREQ-uyumlu raporlama.
- Bu kol, karma tezin nitel kanıt, yöntem, audit trail ve seçilmiş anonim alıntı
  denetimi katmanıdır. Nicel analiz, Quarto üretimi ve tez yazım operasyonu üst
  repoda yürütülür.
- Ham görüşme, demografi, onam/protokol içeriği ve aile düzeyi ayrıntılar
  korunmuş alandadır. Bunlar dış araca, memory'ye veya rapor çıktısına aktarılmaz.

## Güncel Mimari

| Katman | Sorumluluk |
|---|---|
| `00_context/` | Operasyon rehberi, tracker ve çalışma kararları |
| `01_raw_data/` | Korumalı ham/idari araştırma materyali |
| `02_processed/` | Korumalı işlenmiş metin ve temiz yazım kaynağı |
| `03_analysis/` | Codebook, yöntem, tema ve uzlaştırma belgeleri |
| `06_manuscript_outputs/` | Kanonik nitel sonuç QMD'si ve tez aktarım Markdown'ı |
| `07_reports/`, `99_ai_use_log/` | Türetilmiş denetim ve kullanım kayıtları |
| `99_archive/` | Superseded, fakat tarihsel olarak korunacak sürümler |
| `dm_niteliksel_toolkit/`, `scripts/`, `tests/` | Yerel güvenli denetim araçları |
| `reliability/`, `governance/`, `plugins/` | AI-reliability ve politika katmanı |

## Kanonik Aktif Kaynaklar

1. Nitel sonuç kaynak belgesi:
   `06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`.
2. Tez aktarım Markdown'ı:
   `06_manuscript_outputs/qualitative_canonical_results_for_doktoratezi.md`.
3. Aktif codebook:
   `03_analysis/codebook/codebook_v3.md`.
4. Tema mimarisi:
   `03_analysis/codebook/theme_architecture_v3.md`.
5. V2→v3 karar farkları:
   `03_analysis/reconciliation_v2_to_v3.md`.
6. Çalışma durumu:
   `00_context/TRACKER.md`; yol haritası:
   `00_context/ROADMAP_v1.md`.

V1/v2 codebook'lar `99_archive/2026-07-29_pre_new_canon/` altında tarihsel
başvuru içindir; aktif analiz veya tez aktarımında kullanılmaz.

## Çalışma Komutları

```bash
cd "$(git rev-parse --show-toplevel)/niteliksel"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
./dmnitel ai-context
./dmnitel route-tool --query "<soru>"
```

`pyproject.toml`, `dmnitel` yerel komutunun paket manifestidir. AI-reliability
bağımlılıkları `reliability/requirements.txt` içinde pinlenir; root R ortamı
`renv.lock` ile yönetilir.

## Tarihsel Kayıt Politikası

- Tarihsel belgeler, kararın ne zaman ve neden değiştiğini göstermek için korunur.
- Yeni operasyonel komut, kanon veya yol bilgisi yalnız bu belge, `CLAUDE.md`,
  `AGENTS.md` ve ilgili aktif README/manifestlerde güncellenir.
- Tarihsel plan/raporlar geçmişteki yol veya sürüm ifadelerini taşıyabilir; bunlar
  güncel çalışma talimatı sayılmaz.
