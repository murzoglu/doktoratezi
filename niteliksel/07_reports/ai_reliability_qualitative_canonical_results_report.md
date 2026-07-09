# AI Reliability Kontrol Raporu: Niteliksel Kanonik Sonuç Raporu

**Tarih:** 2026-06-30
**Denetlenen kaynak:** `06_manuscript_outputs/qualitative_canonical_results_for_doktoratezi.md`
**Doktoratezi entegrasyon kopyası:** `/mnt/thunderbolt/workspaces/doktoratezi/niteliksel/qualitative_canonical_results_report.md`

AI destekli çıktılar yalnızca yardımcı, ön-denetim veya tutarlılık kontrolü olarak değerlendirilir. Kodlama, tema geliştirme ve yorumlama kararları araştırmacı sorumluluğundadır.

---

## Kapsam

Bu kontrol, niteliksel kanonik sonuç raporunun tez yazımında kullanılmadan önce AI reliability açısından güvenilirliğini değerlendirmek için yapıldı. Denetim şu eksenleri kapsadı:

- Kaynak rapor ile `doktoratezi` entegrasyon kopyasının bire bir eşitliği.
- Sayısal iddiaların yerel CSV/Markdown kaynaklarla tutarlılığı.
- Quote ID ve code ID referanslarının kaynak kayıtlarla eşleşmesi.
- COREQ, codebook, triadik matris ve quote integrity raporlarıyla çapraz tutarlılık.
- Nedensellik, otomatik tema üretimi, kesin hüküm dili ve AI kaynaklı aşırı yorum riski.
- Gizlilik sınırı: ham veri, doğrudan alıntı metni, `.env` içeriği veya kimlikleyici veri taşınmadı.

---

## Kritik Bulgular

- İlk kontrolde raporda eski test sayısı bulundu: `27 test geçti` ifadesi mevcut test paketiyle uyumsuzdu. Son doğrulamada unit test paketi 31 test geçti; kanonik rapor `31 test geçti` olarak güncellendi.
- Karma yöntem entegrasyonu bölümünde yer alan nedensellik riski taşıyabilecek ifade yumuşatıldı. Bulgular artık nicel sonuçların nedensel açıklaması gibi değil, deneyimsel bağlam ve yorumlayıcı açıklama zemini olarak konumlandırılıyor.

Bu iki düzeltmeden sonra özel AI reliability kontrolünde kritik bulgu veya uyarı kalmadı.

---

## Sayısal İddia Tutarlılığı

Rapor içindeki sayısal iddialar aşağıdaki kaynaklarla karşılaştırıldı:

| İddia | Kaynak | Durum |
|---|---|---|
| 7 aile triadı | `06_manuscript_outputs/quotes_used.csv` | Uyumlu |
| 21 katılımcı | `06_manuscript_outputs/quotes_used.csv` | Uyumlu |
| 116 seçilmiş anonim quote ID kaydı | `06_manuscript_outputs/quotes_used.csv` | Uyumlu |
| 116 araştırmacı-denetimli ön-kodlu segment | `01_deidentified/coded_segments.csv` | Uyumlu |
| 57 triadik matris satırı | `04_triadic_matrices/triadic_matrix_from_cleaned_thesis.csv` | Uyumlu |
| 23 kod | `03_analysis/codebook/codebook_v3.csv` | Uyumlu |
| 4 tez makro teması | `01_deidentified/coded_segments.csv` | Uyumlu |
| 6 journal tema yapısı | `03_analysis/codebook/codebook_v2.md` | Uyumlu |
| COREQ 32 madde | `03_analysis/methodology/coreq_32_completed.md` | Uyumlu |
| COREQ 30 complete, 2 partial, 0 missing | `03_analysis/methodology/coreq_32_completed.md` | Uyumlu |

---

## Quote ID ve Code ID Kontrolü

- Raporda geçen quote ID referansları `quotes_used.csv` içinde bulundu.
- Raporda geçen code ID referansları `codebook_v3.csv` içinde bulundu.
- Rapor doğrudan quote text taşımıyor; tez yazımında alıntı metinleri kaynak metinden bire bir alınmalıdır.
- `quote_integrity_report.md` kritik bulgu, uyarı veya öneri üretmedi.

Codebook linter, beş kodda gerçek quote ID yerine placeholder kaldığını uyarı olarak koruyor:

- `TANI_BILGI_ARAYISI`
- `GECE_TAKIP`
- `YARAR_BULMA_OLGUNLASMA`
- `SAGLIK_EKIBI_DESTEGI`
- `MANEVI_BASA_CIKMA`

Bu durum raporda açık kalan iş olarak belirtilmiştir; kaynak uydurma veya AI ile alıntı üretme yapılmamalıdır.

---

## Gizlilik ve Güvenlik Kontrolü

- Rapor içinde `.env` içeriği, ham transcript içeriği veya `quote_text_used` alanı taşınmadı.
- Denetim sırasında aktif IDE sekmesindeki `doktoratezi/.env` dosyası okunmadı ve değiştirilmedi.
- MCP roster kontrolü redaction ile çalıştırıldı; token ve secret değerleri maskeleme üzerinden raporlandı.
- Ham veri klasörlerine yazma veya dönüştürme yapılmadı.

---

## Çalıştırılan Reliability Gate'leri

| Kontrol | Komut | Sonuç |
|---|---|---|
| Repo AI reliability script | `PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py` | 55/55 geçti |
| Toolkit unit tests | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` | 31 test geçti |
| Promptfoo offline policy gate | `npx promptfoo@latest eval -c reliability/evals/promptfooconfig.yaml` | 4/4 geçti |
| MCP roster redaction | `python3 .codex/tools/codex_mcp_roster_redacted.py` | Secret değerleri redacted |
| Codebook lint | `./dmnitel lint-codebook 03_analysis/codebook/codebook_v3.csv` | Kritik bulgu yok; 5 placeholder quote ID uyarısı |
| Quote integrity | `./dmnitel check-quotes --source 02_processed/cleaned_text/thesis_qualitative_cleaned_current.md --quotes 06_manuscript_outputs/quotes_used.csv --output 07_reports/quote_integrity_report.md` | Kritik bulgu, uyarı veya öneri yok |

---

## Kalan Araştırmacı Kararı Gerektiren Noktalar

- Beş codebook kodu için gerçek ve güvenli quote ID atanmalıdır.
- COREQ Madde 16 ve Madde 31 kısmi durumdadır; pilot görüşme bilgisi ve küçük/farklı tema raporlaması final tez metninde netleştirilmelidir.
- Aile 201 düşük odak temsili, bilgi gücü ve asimetrik temsil açısından tartışmada dikkatle konumlandırılmalıdır.
- Doğrudan katılımcı alıntıları final tez/makale metnine eklenirken kaynak metinle bire bir kontrol edilmelidir.
- Rapor kanonik sonuç kaynağıdır; nihai tema, yorum ve bilimsel sonuç cümleleri araştırmacı denetimiyle yazılmalıdır.

---

## Sonuç

Mevcut denetim sonrası kanonik sonuç raporu AI reliability açısından tez entegrasyonu için kullanılabilir durumdadır. Bu karar, otomatik tema üretimi veya nihai yorum devri anlamına gelmez; rapor yalnız araştırmacı denetimli tez yazımı için kanonik ve kaynak-bağlı bir özet belge olarak kullanılmalıdır.
