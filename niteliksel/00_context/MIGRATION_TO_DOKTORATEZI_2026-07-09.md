# Nitel Repo Migrasyon Kaydı

**Tarih:** 2026-07-09
**Kaynak:** `/mnt/thunderbolt/workspaces/T1DM Niteliksel`
**Hedef:** `/mnt/thunderbolt/workspaces/doktoratezi/niteliksel`
**Durum:** Güvenli kopyalama tamamlandı; kaynak repo silinmedi.

## Kapsam

Nitel çalışma ağacındaki proje içeriği, tek-repo çalışma modeli için `doktoratezi`
reposu altına taşındı. Aktarım yerel dosya sistemi içinde yapıldı; harici servis
veya MCP/RAG'e ham veri gönderilmedi.

## Uygulanan Kural

Kopyalama komutu mantığı:

```bash
rsync -a \
  --exclude='.git/' \
  --exclude='.env' \
  --exclude='.env.*' \
  '/mnt/thunderbolt/workspaces/T1DM Niteliksel/' \
  '/mnt/thunderbolt/workspaces/doktoratezi/niteliksel/'
```

Taşınmayan öğeler:

- `.git/`: nested git deposu oluşturulmaması için.
- `.env` ve `.env.*`: credential/secret dosyaları çoğaltılmaması için.

## Gizlilik Sınırı

Hedef alt-ağaçtaki `.gitignore`, hassas nitel araştırma alanlarını commit dışı
tutar:

- `01_raw_data/interviews_docx/`
- `01_raw_data/demographics/`
- `02_processed/transcripts/`
- `.remember/`

Bu klasörler yerel dosya olarak mevcuttur; ham katılımcı metni, demografi satırı
veya aile düzeyi hassas ayrıntılar harici araca gönderilmemelidir.

## Uygulama Sonrası Uyarlamalar

Üst repo altında çalışırken `git rev-parse --show-toplevel` artık
`/mnt/thunderbolt/workspaces/doktoratezi` döndürdüğü için taşınan nitel test
ve hook katmanında alt-kök bulma mantığı düzeltildi:

- `plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py`
- `.codex/hooks/session_start.py`
- `.claude/hooks/_common.py`
- `tests/test_cross_repo_status.py`

`./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md`
yeniden çalıştırıldı ve yeni qualitative root bilgisi hedef alt-ağaçta üretildi.

## Doğrulama

```text
İlk rsync kopyalama sonrası dry-run --checksum: fark yok
Root konuma taşıma ve alt-kök uyarlaması sonrası kaynakla beklenen farklar: path notları, hook/test root çözümleme ve cross-repo status raporu
test ! -d niteliksel/.git: PASS
test ! -e niteliksel/.env: PASS
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests: Ran 93 tests, OK
```

## Kalan Karar

Kaynak repo henüz silinmedi veya arşivlenmedi. Kaynak klasörü silme, arşivleme,
read-only yapma veya Git geçmişiyle birleştirme ayrı onay gerektirir.
