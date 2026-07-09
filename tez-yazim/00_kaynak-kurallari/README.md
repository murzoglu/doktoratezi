# 00_kaynak-kurallari — Kaynak Kuralları Katmanı

Bu klasör tez yazımının **kaynak-otorite katmanı**dır: her biçim, süreç ve
kaynak-erişim kararının **tek kanonik yeri**. Tek-otorite ilkesi geçerlidir —
bir kural yalnız bir dosyada tanımlanır; diğer dosyalar onu **yeniden yazmaz,
işaret eder**. Duplikasyon bu klasörde policy ihlalidir.

## Tek-Otorite Haritası

| Dosya | Otorite alanı | Diğer dosyalarla ilişki |
|---|---|---|
| `marmara-tez-formati-talimatnamesi.md` | **Biçim** (kanonik, eksiksiz): sayfa düzeni, başlık, sayısal yazım, tablo/şekil, atıf, AMA-11 kaynakça, bölüm sırası, ön bölümler. | Tüm biçim detayının tek kaynağı. Diğerleri buraya işaret eder. |
| `talimatname-claude-code.md` | **Süreç** (bağlayıcı): oturum ritüeli, rota, KVKK sınırı, araç/MCP kapıları, referans kapısı, doğrulama paketi, sci-audit katman sınırı. | Süreç/rota otoritesi. Biçim kararını `marmara-...`e devreder. |
| `tam-metin-erisim-kaskadi.md` | **Tam metin erişimi** (kanonik): T0–T3 kaskadı, OpenAthens/Anna's/PMC, Zotero kapanışı, ledger durumları, yasaklar. | Full-text kaskadının tek kaynağı. Evidentia çerçevesi (`01_mimari/evidentia-entegrasyon-cercevesi.md`) buraya işaret eder. |
| `format-kontrati.md` | **Operasyonel hızlı kontrat**: bağlayıcı kararların bir-ekranlık özeti (tablo). | Özet + pointer; detay `marmara-...`dedir. Kural yeniden yazmaz. |
| `kilavuz-kaynak-ledgeri.md` | **Kaynak izlenebilirliği**: kanonik talimatname bölümü → resmi kılavuz dosyası/kesimi eşlemesi. | Provenance haritası; kural metni tutmaz. |

## Kanonik biçim/süreç otoritesi dışı çerçeveler (bağlı omurga)

| Konu | Çerçeve dosyası | Skill |
|---|---|---|
| Dış literatür / citation / benchmark / prior | `01_mimari/evidentia-entegrasyon-cercevesi.md` | `t1dm-tez-rehberi` |
| Nitel kol çıktısı (RTA/COREQ/quote/KVKK) | `05_entegrasyon/nitel-cikti-cercevesi.md` | `niteliksel-arastirma-rehberi-t1dm` |
| AI-reliability (manüskript adli) + Türkçe imla | — (sci-audit plugin) | `sci-audit@cureonics-marketplace` axes A–G |

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman açık talimatı → (2) resmi
`docs/tez-kilavuz/` (PDF + DOCX) → (3) bu klasördeki kanonik otorite dosyası →
(4) repo içi eski notlar. Analiz/veri/hipotez kararında repo kanıtı
(`_targets.R`, testler, protokol) üstündür; bu klasör yalnız **biçim, süreç ve
kaynak-erişim** otoritesidir.

## Duplikasyon önleme kuralı

Yeni bir kural eklenirken: önce yukarıdaki haritadan **hangi dosyanın otoritesi**
olduğu belirlenir; kural yalnız oraya yazılır; gerekiyorsa diğer dosyalara
**pointer** eklenir. Aynı kuralın iki dosyada tam metniyle bulunması rafine
edilir (bkz. 2026-07-06 rafinasyonu: `kilavuz-kaynak-ledgeri` provenance'a
indirgendi, full-text kaskadı tek otoriteye toplandı).
