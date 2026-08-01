# Denetim Kanonik Dosya Haritası

Bu belge, istatistik doğruluk ve tutarlılık denetimi öncesinde hangi dosyaların kanonik kaynak,
hangi dosyaların türetilmiş/yerel artefakt olduğunu sabitler.

## Kanonik kaynaklar

| Katman | Kanonik dosya |
|---|---|
| Proje talimatı | `AGENTS.md`, `CLAUDE.md` |
| Tez yazım kritik kaynak manifesti | `tez-yazim/06_kritik-kaynaklar/README.md`, `tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv` |
| Veri kilidi | `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` |
| Veri sözleşmesi | `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` |
| Ölçek formları | `docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md`, `docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md`, `docs/protokol/KANONIK_BECK_DEPRESYON_ENVANTERI.md`, `docs/protokol/KANONIK_KARDES_ILISKILERI_ANKETI.md`, `docs/protokol/KANONIK_DEMOGRAFIK_VE_TIBBI_BILGILER.md` |
| Analiz planı | `docs/analiz_planlari/03-sap-ana-plan.md`, `docs/analiz_planlari/04-sap-faz2-posthoc.md`, `docs/analiz_planlari/05-osf-layer3-faz2-amendment.md` |
| Final CSR | `docs/CLINICAL-STUDY-REPORT-FINAL.md` |
| Nitel sonuç raporu | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` |
| Nitel sonuç raporu Markdown kopyası | `niteliksel/qualitative_canonical_results_report.md` |
| Ham klinik veri sınırı | `data/raw/Raw Data - Final.csv` yalnız korumalı reprodüksiyon kaynağıdır; yazımda satır düzeyi kullanılmaz. |
| Pipeline | `_targets.R`, `R/`, `scripts/R/`, `tests/` |
| İstatistik audit | `R/50_statistical_audit.R`, `scripts/R/51_statistical_audit.R`, `tests/test_statistical_audit.R` |
| Derin audit planı | `docs/analiz_planlari/51-istatistik-audit-derin-denetim-plani.md` |
| Dış kanıt köprüsü | `.claude/skills/t1dm-tez-rehberi/SKILL.md`, `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` |

## Türetilmiş veya yerel artefaktlar

| Desen | Karar |
|---|---|
| `outputs/`, `_targets/`, `_freeze/` | Türetilmiş analiz/render çıktısı; git dışı |
| `data/processed/FINAL_REFERENCE__*.csv` | Kontrollü erişimli analiz verisi; hash ile doğrulanır, git dışı |
| `CSR-FINAL-render.qmd`, `CSR-FINAL-render_cache/`, `CSR-FINAL-render_files/` | `scripts/build_csr_render_qmd.py` ve Quarto tarafından yeniden üretilebilir render artefaktları; git dışı |
| `*.bak-precorrection.md` | Geçici düzeltme yedeği; kanonik karar kaynağı değil, git dışı |
| `.env`, credential JSON, `.claude/*.local.*` | Kullanıcı-local/gizli dosyalar; git dışı |

## Denetim düzeni

1. Kanonik veri `validate_and_load()` ile lock/hash/satır-sütun kontrolünden geçmeden analiz nesnesi sayılmaz.
2. İstatistik audit çıktılarını yalnız `outputs/tables/statistical_audit_*.csv` altında üret.
3. Audit raporunda ham satır, `.env`, credential, doğrudan kimlikleyici veya tam CSV dump paylaşma.
4. `critical` audit bulgusu varsa final rapora "geçti" deme; önce kaynak fonksiyon veya kanonik sözleşme ile doğrula.
5. `review` bulgularını `kabul edildi`, `düzeltilecek` veya `opsiyonel skip` olarak sınıflandır.
6. En derin yürütme için `docs/analiz_planlari/51-istatistik-audit-derin-denetim-plani.md` planını izle; merkezi audit sonucunu `targets`, modül runner'ları, CSR/tez mapping ve Evidentia kanıt zinciriyle birlikte kapat.
