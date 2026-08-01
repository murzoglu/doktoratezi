# İki-Kol Entegrasyon Planı

Bu plan `/workspaces/T1DM-Tez` nicel kök ile
`/workspaces/T1DM-Tez/niteliksel` nitel kolu tek tez yazım
sürecinde birleştirir.

> **Otorite zinciri:** Bu dosya **iki-kol entegrasyon modelinin (nicel kök ↔
> nitel kol) tek kanonik yeri**dir (resmi bölüm ↔ nicel/nitel kaynak eşlemesi, repo-düzeyi gizlilik
> sınırı). Devredilen otoriteler: joint display alan tanımları →
> `05_entegrasyon/nitel-nicel-joint-display-plan.md`; nitel kol çıktı çerçevesi →
> `05_entegrasyon/nitel-cikti-cercevesi.md`; biçim/süreç →
> `00_kaynak-kurallari/`; araç seçimi → `yetkinlik-ve-arac-mimarisi.md`.
> Klasör haritası: `01_mimari/README.md`.

## Entegrasyon Kaynakları

| Kaynak | Rol |
|---|---|
| `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` | Tek kanonik nitel sonuç raporu. |
| `niteliksel/qualitative_canonical_results_report.md` | Kanonik QMD'nin mekanik Markdown kopyası. |
| `T1DM Niteliksel/00_context/CODEX_PLAYBOOK.md` | Cross-repo tool ve gizlilik playbook'u. |
| `T1DM Niteliksel/07_reports/cross_repo_thesis_bridge_status.md` | Güncel cross-repo status raporu. |
| `docs/analiz_planlari/` | Nicel SAP, Faz II/post-hoc ve raporlama standartları. |
| `chapters/` | Quarto tez bölüm kaynakları. |

## Resmi Bölüm Eşlemesi

| Resmi bölüm | Nicel kaynak | Nitel kaynak | Yazım görevi |
|---|---|---|---|
| `GİRİŞ ve AMAÇ` | CSR, SAP, literatür matrisi | Triadik metodoloji literatürü, bilgi gücü notları | Bilimsel boşluk ve karma amaç. |
| `GENEL BİLGİLER` | T1DM, ebeveynlik, depresyon, KİA literatürü | Kardeş, aile sistemi, triadik çocuk deneyimi literatürü | Yorum yapmadan kavramsal zemin. |
| `GEREÇ ve YÖNTEM` | `_targets.R`, veri haritası, ölçek ve analiz planı | COREQ, RTA, audit trail, bilgi gücü, LLM use statement | Tekrarlanabilir nicel yöntem + şeffaf nitel yöntem. |
| `BULGULAR` | H1-H5 aggregate sonuçlar, tablo/figür | 4 makro tema, triadik matris, seçilmiş anonim alıntı | Yorumsuz bulgu sunumu ve joint display hazırlığı. |
| `TARTIŞMA ve SONUÇ` | Hipotez sonuçları ve Faz II sınırları | Negatif vaka, refleksivite, tema yorumu | Kanıt türlerini ayırarak karma yorum. |
| `EKLER` | Etik kurul, formlar, ölçekler, ek tablolar | COREQ, codebook/audit trail özetleri, LLM beyanı | Resmi sıraya göre ek dosyalar. |

## Joint Display İlkesi

Joint display **alan tanımları ve ilişki türü sözlüğü** tek kanonik yerdedir:
`05_entegrasyon/nitel-nicel-joint-display-plan.md` (nitel çıktı çerçevesi:
`05_entegrasyon/nitel-cikti-cercevesi.md`). Burada tekrarlanmaz.

İki-kol sınırı açısından bağlayıcı kural: her joint display satırı nicel
bulgu ile nitel tema/örüntüyü **ayrı kanıt türü** olarak taşır; ilişki yalnız
uyum / tamamlayıcılık / ayrışma / açıklayıcı genişleme etiketiyle adlandırılır;
nitel tema nicel mekanizma, nicel estimate nitel doğrulama gibi yazılmaz; aile
düzeyi ayrıntı ve ham alıntı satıra girmez (bkz. Gizlilik Sınırı).

## Gizlilik Sınırı

- Nitel upstream dosyadan ham quote dökümü çekilmez.
- Aile düzeyi ayrıntı joint display'e alınmaz.
- Nicel repo `data/processed/*` içeriği sadece lock/varlık kontratı olarak
  kontrol edilir; satır düzeyi veri yazıma taşınmaz.
- Harici MCP'lere yalnız anonim/türetilmiş bilgi ve literatür sorusu gönderilir.
