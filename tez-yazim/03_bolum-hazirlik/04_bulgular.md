# BULGULAR — Kapsamlı Bölüm Talimatnamesi

> **Kanonik kural otoritesi:** Bölüm içerik kuralı →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §3.6 (tarafsız,
> **yorumsuz**, amaç/hipotez sırasında; aynı bulgu hem tablo hem şekil değil);
> nitel bulgu biçimi → §7; istatistik yazım → §8 + §1.4; tablo/şekil → §1.7/§1.6.
> Bu talimatname kural tanımlamaz. Klasör haritası: `03_bolum-hazirlik/README.md`.

## 1. Bölüm İşlevi

`BULGULAR`, amaç ve hipotezlerle uyumlu sırada, tüm verileri **açık, düzenli,
tarafsız ve yorumsuz** sunar. Yorum, literatür karşılaştırması ve karma
bütünleştirme dili **kesinlikle** `TARTIŞMA ve SONUÇ`a bırakılır. Bu bölüm karma
tezin nicel (H1–H5) ve nitel (4 makro tema) kollarının bulgularını **ayrı kanıt
türü** olarak sunar ve joint display'e köprü hazırlar.

## 2. Yazım Sınırları (ihlal edilemez)

- **Yorum yok:** "bu ilişkili olabilir", "beklendiği gibi", "önemli biçimde
  düşündürmektedir" gibi yorum/çıkarım cümleleri bu bölümde yasaktır.
- **Ham veri/quote yok:** satır düzeyi veri, aile-düzeyi ayrıntı, ham transcript
  girmez. Nitel alıntı yalnız **araştırmacı onaylı anonim** (aile no + rol
  etiketi) veya **quote ID** ile (marmara §7).
- **Sayı kanıtı:** her sayısal bulgu kaynağı repo aggregate çıktısına
  (`outputs/tables`, `outputs/models`, CSR) izlenebilir olmalı; metne uydurma
  sayı yazılmaz (Stop kapısı: kaynaksız sayı bloklar).
- **Tez = 4 makro tema** (journal = 6 tema — karıştırma).

## 3. Önerilen Akış (sıra amaç/hipotezle uyumlu)

1. **Örneklem ve tanımlayıcılar** — grup (DM/kontrol), rol dağılımı, temel
   demografik/klinik betimleyiciler (aggregate; ortalama **ve** medyan uygun
   yerde). Kaynak: CSR, `outputs/tables`.
2. **Ölçek ve veri kalitesi** — güvenirlik (α/ω), eksik veri örüntüsü, madde/
   ölçek betimleyicileri (yorumsuz).
3. **H1–H5 birincil nicel bulgular** — hipotez sırasında; her biri: nokta tahmini
   + %95 GA (veya Bayesian credible interval) + anlamlılık; etki büyüklüğü
   raporlanır, **yorum yok**.
   - H1 çocuk algısı · H2 kardeş ilişkisi (APIM) · H3 anne öz-rapor ·
     H4 Beck→EMBU-P SEM · **H5 diadik tutarlılık** (ICC/Bland-Altman/RSA/CFM/
     k-coef) — birincil yenilik; bulgu burada, yorumu Tartışma'da.
4. **Faz II / post-hoc bulgular** — **ayrı `[KEŞİFSEL]` etiketiyle**; birincil
   hipotez sonucu gibi yazılmaz.
5. **Nitel bulgular** — 4 makro tema, alt tema, örüntü ve **triadik rol
   karşılaştırması** (anne / T1DM'li çocuk / sağlıklı kardeş ayrı). Tema =
   "central organizing concept", katılımcı sözünün başlığı değil.
6. **Joint display köprüsü** — nicel bulgu ↔ nitel tema yan yana; ilişki türü
   (uyum / tamamlayıcılık / ayrışma / açıklayıcı genişleme) **etiketli**; ama
   *yorum* yapılmadan (yorumun tam açılımı Tartışma'da).

## 4. Nicel bulgu yazım kuralları (marmara §8)

- Tanımlayıcılarda ölçek, birim, payda ve **eksik veri notu** açık.
- `p` değeri: `p=0,038` / `p<0,001`; ondalık **virgül**; ondalık öncesi sıfır
  (`0,14`); ortalama/yüzde 1 basamak, test/oran 2 basamak (marmara §12).
- Önce metinde özet, ayrıntı tablo/şekille; **aynı bulgu hem tablo hem şekil
  olarak sunulmaz**; program çıktılarının tamamı eklenmez.
- Tablo başlığı **üstte**, şekil başlığı **altta**; kısaltma/simge/test/p
  dipnotta (marmara §1.7/§1.6). İskelet: `02_sablonlar/tablo-sekil-sablonlari.md`.
- Aile-içi bağımlılık nedeniyle multilevel/clustered sonuç sunulurken ICC
  bağlamı korunur (yöntemi §GEREÇ'te; burada yalnız bulgu).

## 5. Nitel bulgu yazım kuralları (marmara §7)

- Tema/alt tema/örüntü/rol karşılaştırması olarak; **ham alıntı dökümü yok**.
- Triadik yorumda üç konum ayrı kanıt; "aynı olayın üç konumdan görünümü".
- Nitel tema **nicel etki büyüklüğü/nedensel mekanizma gibi sunulmaz**; sıklık
  sayımı temanın kanıtı değildir (information power mantığı).
- Anonim alıntı bütünlüğü `./dmnitel check-quotes` ile denetlenir (nitel repoda);
  ham transcript açılmaz.

## 6. Joint display köprüsü (Faz 6 hazırlığı)

Bu bölüm joint display satırlarının **bulgu** kısmını hazırlar; alan tanımı ve
ilişki sözlüğü `05_entegrasyon/nitel-nicel-joint-display-plan.md`'dedir. Satır:
araştırma odağı/hipotez → nicel bulgu (yön + belirsizlik) → nitel tema/örüntü →
ilişki türü etiketi → (yorum sınırı Tartışma'ya bırakılır). H5 için nicel uyum
*ne kadar/hangi boyut*, nitel tema *neden/nasıl* — bu ayrım joint display'de
görünür kılınır.

## 7. Nitel bulgular için güvenli kaynak

`docs/niteliksel/qualitative_canonical_results_report.md` nicel repoya taşınmış
**güvenli, de-identified** entegrasyon kaynağıdır; nitel kolu temsil eden
varsayılan aktarımdır. Ham transcript veya nitel repo geniş taraması **default
değildir**; gerekirse yalnız tema/kod/COREQ/audit-trail düzeyi.

## 8. Anti-pattern'ler (bu bölümde yapma)

- Bulgu cümlesine yorum/çıkarım karıştırmak (→ Tartışma).
- Aynı veriyi hem tablo hem şekil olarak tekrarlamak.
- Post-hoc bulguyu birincil hipotez sonucu gibi yazmak.
- Nitel temayı sıklık sayımı/etki büyüklüğü gibi sunmak; 4↔6 tema karıştırmak.
- Kaynağı repo çıktısına izlenemeyen sayı yazmak.
- Ham quote/aile demografisi taşımak.

## 9. Kanıt eşlemesi (repo)

| Bulgu türü | Repo kaynağı | Sınır |
|---|---|---|
| Tanımlayıcı/psikometri | `outputs/tables`, CSR | Aggregate; yorum yok. |
| H1–H5 sonuç | `outputs/models`, `outputs/tables`, SAP | Nokta+GA+etki; yorum yok. |
| Faz II/post-hoc | `docs/analiz_planlari/04-sap-faz2-posthoc.md` | `[KEŞİFSEL]` etiketli. |
| Nitel tema/triad | `docs/niteliksel/qualitative_canonical_results_report.md` | De-identified; anonim quote. |
| Joint display | `05_entegrasyon/nitel-nicel-joint-display-plan.md` | Kanıt türü etiketli. |

## 10. Kapanış kapıları

- [ ] Tüm yorum cümleleri Tartışma'ya taşındı; bölüm yorumsuz.
- [ ] Aynı bulgu hem tablo hem şekil olarak tekrarlanmadı.
- [ ] `p`/ondalık marmara §8/§1.4 biçiminde; her sayı repo çıktısına izlenebilir.
- [ ] Post-hoc `[KEŞİFSEL]`; birincil hipotezden ayrı.
- [ ] Nitel quote anonim + araştırmacı onaylı; `check-quotes` geçti; ham veri yok.
- [ ] Tez 4 makro tema; journal 6 tema ile karışmadı.
- [ ] Format §12 + `sci-audit` axis G/A–F blocker'sız.
- [ ] Kapı 0–5 sertifikasyonu + açık onay.
