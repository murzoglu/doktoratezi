# Tez Yazım Operasyon Merkezi

Bu klasör doktora tezinin yazım sürecinde resmi Marmara Üniversitesi tez kılavuzu,
repo içi analiz kanıtları ve iki-repo karma yöntem entegrasyonunu tek hatta bağlayan
operasyon katmanıdır. `thesis.qmd` ve `chapters/` gerçek üretim dosyalarıdır; bu
klasör karar, şablon, kontrol listesi ve yazım hazırlık alanıdır.

## Ana Çalışma Merkezi Kararı

Bundan sonraki tez yazım süreci bu repo içinde yürütülür. Ana çalışma
dizini `/mnt/thunderbolt/workspaces/doktoratezi`, ana operasyon alanı
`tez-yazim/`, üretim dosyaları ise `thesis.qmd` ve `chapters/*.qmd`
dosyalarıdır. Nitel repo, kanonik nitel sonuç raporunun temsil etmediği
veya ek denetim gerektiren yöntem, bulgular, joint display, tartışma ve
ekler kesimlerinde koşullu kaynak/denetim katmanı olarak açılır.

Kanonik nitel sonuç raporu bu tez yazım sürecinde nitel repoyu temsil eden
varsayılan aktarım kaynağıdır. Ham transcript, demografi satırı veya geniş
nitel repo yeniden taraması varsayılan iş akışı değildir.

## Resmi Kaynak Önceliği

1. Birincil biçim ve şablon kaynağı:
   `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf`
2. Birincil kapak, ön bölüm ve bölüm sırası kaynağı:
   `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`
3. Repo içi yöntem, analiz ve veri yönetişimi kaynakları:
   `AGENTS.md`, `CLAUDE.md`, `_targets.R`, `docs/protokol/`,
   `docs/analiz_planlari/`, `docs/niteliksel/` ve `chapters/`.

Bu kaynaklar çakışırsa resmi `docs/tez-kilavuz` dosyaları yazım biçimi,
bölüm sırası, başlıklandırma, sayı/kaynakça kuralları ve ön bölüm şablonlarında
üstün kabul edilir. Analiz, veri yapısı ve hipotez kararlarında ise repo içi
kanıt ve testlenmiş pipeline kaynakları üstün kabul edilir.

Resmi kılavuzdan **eksiksiz** çıkarılmış kanonik biçim otoritesi:
`00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`. Tüm yazım
süreçlerinde bu talimatnameye **zorunlu uyum** sağlanır; `format-kontrati.md`
onun kısa operasyonel özetidir. Dış literatür/citation Evidentia hattı:
`01_mimari/evidentia-entegrasyon-cercevesi.md`. Nitel kol çıktı çerçevesi:
`05_entegrasyon/nitel-cikti-cercevesi.md`.

## Klasör Haritası

| Klasör | Amaç |
|---|---|
| `00_kaynak-kurallari/` | Resmi kılavuzdan çıkarılmış format, kaynakça ve şablon sözleşmesi. Tek-otorite haritası: `00_kaynak-kurallari/README.md`. |
| `01_mimari/` | Yürütme planı, araç/yetkinlik mimarisi, dış-kanıt hattı ve iki-repo yazım modeli. Tek-otorite haritası: `01_mimari/README.md`. |
| `02_kanit-haritalari/` | Referans denetim ledger'ı ve bölüm bazlı iddia↔kaynak kanıt haritaları. Tek-otorite haritası: `02_kanit-haritalari/README.md`. |
| `02_sablonlar/` | Bölüm, özet, tablo, şekil ve ön bölüm yazım şablonları (iskelet). Tek-otorite haritası: `02_sablonlar/README.md`. |
| `03_bolum-hazirlik/` | Her resmi Marmara bölümü için bu teze özgü kapsamlı yürütme talimatnameleri. Tek-otorite haritası: `03_bolum-hazirlik/README.md`. |
| `04_kalite-kontrol/` | Format, kanıt, atıf, AI/MCP, gizlilik ve bölüm finalizasyon sertifikasyon kapıları (Kapı 0–5). Tek-otorite haritası: `04_kalite-kontrol/README.md`. |
| `05_entegrasyon/` | Nitel-nicel joint display ve karma yorum planı. Tek-otorite haritası: `05_entegrasyon/README.md`. |
| `06_kritik-kaynaklar/` | Klinik/nitel rapor, protokol, ham/kilitli veri, ölçek-form ve kalite kapısı manifesti. Tek-otorite haritası: `06_kritik-kaynaklar/README.md`. |

## Varsayılan Yazım Sırası

1. `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` (kanonik biçim
   otoritesi) ve özeti `00_kaynak-kurallari/format-kontrati.md` ile biçim
   kurallarını sabitle.
2. `06_kritik-kaynaklar/README.md` ve
   `06_kritik-kaynaklar/kritik-dosya-manifesti.tsv` ile kullanılacak klinik,
   nitel, protokol, veri ve ölçek/form kaynaklarını seç.
3. `01_mimari/yetkinlik-ve-arac-mimarisi.md` ile kullanılacak local tool,
   MCP, plugin ve doğrulama kapısını seç.
4. İlgili bölüm için `03_bolum-hazirlik/` briefini aç.
5. Metin üretmeden önce repo kanıtını dosya yolu ile eşleştir.
6. Dış literatür gerekiyorsa Evidentia paketini birincil geniş kanıt motoru
   olarak kullan; PubMed/OpenAlex/Paper Search, OpenAthens publisher
   full-text, Anna's fallback, Zotero ve çift AI-reliability kapılarını
   sırayla kapat; ham veri gönderme.
7. YÖK/ERIC, mevzuat, klinik terminoloji/regülasyon, render/browser/GitHub ve
   platform/design MCP'lerini yalnız görev sinyali varsa aç.
8. Nitel repo yetkinliklerini yalnız nitel kolun tezde ilişkili kesimleri için
   kullan; kanonik nitel sonuç raporu varsayılan temsil kaynağıdır.
9. Üretilen içeriği `chapters/` dosyalarına taşımadan önce
   `04_kalite-kontrol/` listeleriyle kontrol et.
10. Bölüm finalize edilmeden önce
   `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
   eksiksiz uygulanır ve
   `04_kalite-kontrol/sertifikalar/<bolum>-sertifika-YYYY-MM-DD.md`
   raporu oluşturulur. Sertifika ve açık uygulama onayı yoksa bölüm yalnız
   taslak veya `provisional-pass` kabul edilir.

## MCP Görev Kapıları

Aşağıdaki tablo özet kapılardır; **tam araç/MCP/skill/plugin seçim matrisinin**
tek kanonik otoritesi `01_mimari/yetkinlik-ve-arac-mimarisi.md`'dir.

| Kapı | MCP'ler | Kullanım sınırı |
|---|---|---|
| Bağlam | `anamnesis`, `memory`, `qdrant`, `sequentialthinking` | Anonim/türetilmiş karar bağlamı; raw veri yok. |
| Literatür/full-text | Evidentia, PubMed, OpenAlex, Paper Search, OpenAthens, Anna's | Full-text ve ledger kapanmadan citation yok. |
| Türkiye akademik | `yoktez-mcp`, `yok-akademik`, `eric-mcp` | YÖK/okul/eğitim bağlamı; uzun metin kopyalanmaz. |
| Mevzuat | `mevzuat`, `mevzuat-bilgisi` | Resmi madde/kaynak doğrulaması; hukuki tavsiye yok. |
| Klinik terminoloji | `openfda`, `med-terminologies`, `nlm-rxnorm`, `nih-clinicaltables`, `iuphar-gtopdb`, `drugddx`, `titck-cache` | Tez terminolojisi ve kaynak doğrulaması; hasta düzeyi öneri yok. |
| Teknik teslim | `playwright`, `chrome-devtools`, `brave-search`, `github`, `filesystem` | Render/screenshot/GitHub; credential ve raw veri yok. |
| Platform/design | `firebase`, `supabase`, `cloudflare-api`, `figma`, OpenAI API key flow | Tez yazımı default'u değil; açık teknik görevle. |

## Yazım İlkeleri

- Tez dili Türkçedir; resmi kılavuza göre sade, açık ve çoğunlukla edilgen
  üçüncü tekil anlatım tercih edilir.
- Resmi bölüm sırası korunur: `ÖZET`, `SUMMARY`, `GİRİŞ ve AMAÇ`,
  `GENEL BİLGİLER`, `GEREÇ ve YÖNTEM`, `BULGULAR`,
  `TARTIŞMA ve SONUÇ`, `KAYNAKLAR`, `ÖZGEÇMİŞ`,
  `BİLİMSEL FAALİYETLER`, `EKLER`.
- Sayısal yazımda ondalık ayırıcı virgüldür: `62,4`, `p=0,038`,
  `p<0,001`.
- Kaynak listesi Enstitü kılavuzundaki AMA-11 tabanlı özel formata göre
  alfabetik sıralanır; metin içi atıflar kılavuzdaki yazar-yıl örüntüsüne
  uygun tutulur.
- Nitel bulgular nicel etki tahmini gibi yazılmaz; nicel sonuçlar da nitel
  tema için nedensel kanıt gibi sunulmaz.
- Ham görüşme, aile düzeyi hassas ayrıntı, satır düzeyi veri, `.env` ve
  credential içerikleri bu klasöre alınmaz.

## Doğrulama Komutları

Bölüm finalizasyonu için ana kapı:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
test -f tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md
test -f tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasi-sablonu.md
```

Bu playbook uygulanmadan hiçbir `chapters/*.qmd` bölümü final sayılmaz.

Dar tez-yazım/tool değişikliği için:

```bash
./dmnitel cross-repo-status --output 07_reports/cross_repo_thesis_bridge_status.md
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

Nicel repo AI/tool değişikliği için:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
```

Referans içeren bölüm kapanışı için:

```bash
cd /mnt/thunderbolt/workspaces/T1DM\ Niteliksel
PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py

cd /mnt/thunderbolt/workspaces/doktoratezi
PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py
```

Quarto çıktısı etkilenirse:

```bash
cd /mnt/thunderbolt/workspaces/doktoratezi
quarto check
quarto render thesis.qmd
```
