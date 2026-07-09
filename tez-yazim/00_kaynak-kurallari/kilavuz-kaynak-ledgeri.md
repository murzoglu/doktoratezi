# Kılavuz Kaynak Ledgeri (Provenance)

Bu ledger `docs/tez-kilavuz` altındaki iki resmi dosyanın hangi kesiminin
kanonik biçim talimatnamesinin hangi bölümüne kaynaklık ettiğini izlenebilir
kılar. **Kural metni burada tekrarlanmaz** (duplikasyon önleme, tek-otorite
ilkesi — `README.md`); kural detayının tek kanonik yeri
`marmara-tez-formati-talimatnamesi.md`'dir. Bu dosya yalnız **provenance
haritası**dır.

## Kaynak Dosyalar

| Kaynak | Kapsam |
|---|---|
| `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf` | Genel biçim, sayfa düzeni, başlık, tablo/şekil, özet, bölüm içeriği, kaynakça (AMA-11), ekler. |
| `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx` | Kapak, beyan, içindekiler, listeler, özet/summary alanları, ana bölüm sırası, başlık numaralandırma, özgeçmiş, faaliyet şablonu. |

## Provenance Haritası (kanonik talimatname bölümü → resmi kaynak kesimi)

| `marmara-tez-formati-talimatnamesi.md` bölümü | Resmi kaynak kesimi |
|---|---|
| 1.1 Sayfa tasarımı | Klavuz PDF §1.1 |
| 1.2 Yazı, satır, paragraf, maddeleme | Klavuz PDF §1.2 |
| 1.3 Başlıklar (14/12 punto, kapitalizasyon, numaralandırma) | Klavuz PDF §1.3 + Şablon DOCX başlık düzeni |
| 1.4 Anlatım ve sayısal yazım (ondalık virgül, `p`) | Klavuz PDF §1.4 |
| 1.5 Kısaltmalar | Klavuz PDF §1.5 |
| 1.6 Şekiller | Klavuz PDF §1.6 |
| 1.7 Tablolar | Klavuz PDF §1.7 |
| 1.8 Metin içinde kaynak gösterme | Klavuz PDF §1.8 |
| 1.9 Sayfa numaralandırması | Klavuz PDF §1.9 |
| 2 Ön bölümler (kapak, beyan, teşekkür, içindekiler, kısaltmalar, şekiller, tablolar) | Klavuz PDF §2.1–2.7 + Şablon DOCX ön bölümler |
| 3.1 Başlık | Klavuz PDF §3.1 |
| 3.2 Özet / Summary | Klavuz PDF §3.2 + Şablon DOCX özet/summary alanları |
| 3.3–3.7 Giriş, Genel Bilgiler, Gereç-Yöntem, Bulgular, Tartışma-Sonuç | Klavuz PDF §3.3–3.7 |
| 3.8 Özgeçmiş / 3.9 Bilimsel Faaliyetler / 3.10 Ekler | Klavuz PDF §3.9–3.11 + Şablon DOCX |
| 4 Kaynakça (AMA-11 + örnek künyeler) | Klavuz PDF §3.8 (Tablo 1 örnekleri dahil) |
| 5 Resmi bölüm sırası (18 madde) | Şablon DOCX içindekiler sırası |
| 11 Override notu (APA→AMA-11, nokta→virgül) | Klavuz PDF §1.4 + §3.8 (repo eski notlarına karşı) |

## Kullanım

Bir biçim kuralının **kaynağını** doğrulamak için: kanonik talimatnamedeki
ilgili bölümü aç, yukarıdaki haritadan resmi kaynak kesimini bul, gerekirse
`docs/tez-kilavuz` dosyasından teyit et. Kural **değişikliği** yalnız resmi
kılavuz güncellenirse yapılır ve önce `marmara-tez-formati-talimatnamesi.md`'ye,
sonra bu haritaya işlenir.
