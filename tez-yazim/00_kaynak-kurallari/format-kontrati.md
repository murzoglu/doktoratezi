# Format Kontratı

Bu dosya tez yazımında ajanların, local scriptlerin ve insan düzenlemesinin
uyması gereken pratik kontrattır. Kaynak otoritesi:
`docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf` ve
`docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`.

> **Kanonik biçim otoritesi:**
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`. Bu kontrat onun
> **kısa operasyonel özeti**dir; herhangi bir biçim ayrıntısı çakışırsa kanonik
> talimatname esastır ve tüm yazım süreçlerinde ona **zorunlu uyum** sağlanır.

## Belge Kontratı

| Alan | Karar |
|---|---|
| Dil | Türkçe; Summary İngilizce. |
| Anlatım | Sade, açık, akademik, çoğunlukla edilgen üçüncü tekil. |
| Font | Times New Roman, 12 punto. |
| Satır aralığı | Ana metin 1,5. |
| Paragraf | Girintisiz, paragraflar arası 6 nk. |
| Kenar boşlukları | Sol/sağ 2,5 cm; üst/alt 2 cm. |
| Sayılar | Ondalık virgül. |
| Kaynak listesi | Enstitü AMA-11 özel formatı, alfabetik. |
| Metin içi atıf | Kılavuz yazar-yıl örüntüsü. |
| Bölüm sırası | Şablon DOCX'teki resmi sıra (kanonik §5). |
| İmla/sayısal denetim | `sci-audit` axis G (`/sci-audit:check-turkish`); ondalık-nokta `p` blocker. |
| Finalizasyon | Bölüm sertifikası ve açık uygulama onayı yoksa final statüsü verilmez. |

Her satırın detayı kanonik talimatnamededir (Font/satır/paragraf §1.2, sayılar
§1.4, kaynakça §4, atıf §1.8, bölüm sırası §5).

## Finalizasyon Kontratı

- Her `chapters/*.qmd` bölümü final kabul edilmeden önce
  `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`
  eksiksiz uygulanır.
- Sertifika raporu
  `tez-yazim/04_kalite-kontrol/sertifikalar/<bolum-kodu>-sertifika-YYYY-MM-DD.md`
  yolunda saklanır.
- Sertifika beş ana kapıyı birlikte kapatır: derin literatür/künye evreni,
  full-text/Zotero/Anamnesis, resmi bölüm/kılavuz uyumu, Türkçe imla-akış ve
  AI-reliability/teknik doğrulama.
- Herhangi bir kapı `FAIL` ise bölüm `blocked` kalır.
- Tüm teknik kapılar geçse bile kullanıcı/danışman uygulama onayı yoksa durum
  en fazla `provisional-pass` olur.

## Kanıt ve Yazım Kontratı (detay = kanonik otorite)

Aşağıdaki bağlayıcı kararların **tam metni** ilgili kanonik otoritededir; burada
yalnız kapı olarak listelenir (duplikasyon önleme, `README.md`):

| Kontrat | Bağlayıcı kapı | Kanonik detay |
|---|---|---|
| Bölüm başlığı | Ana başlık büyük harf; `GİRİŞ ve AMAÇ` / `TARTIŞMA ve SONUÇ` alt başlıksız; şablon bağlaç biçimi. | `marmara-tez-formati-talimatnamesi.md` §1.3 |
| İstatistik yazım | Bulgular yorumsuz; `p=0,038`/`p<0,001`; tablo≠şekil tekrarı; post-hoc `[KEŞİFSEL]`. | Kanonik §8 |
| Nitel bulgular | Tema/alt tema/rol; ham alıntı yok (anonim/quote ID); triadik ayrı kanıt; tema ≠ etki büyüklüğü. | Kanonik §7 + `05_entegrasyon/nitel-cikti-cercevesi.md` |
| Karma yöntem | Önce kendi kanıt türü; joint display doğrulama değil; uyum/tamamlayıcılık/ayrışma/genişleme etiketi. | Kanonik §6 + `05_entegrasyon/nitel-cikti-cercevesi.md` |
| Dış referans izi | DOI/PMID/ID + full-text route + Zotero item/attachment + BibTeX + claim notu. | `02_kanit-haritalari/referans-denetim-ledgeri.md` + `tam-metin-erisim-kaskadi.md` |
