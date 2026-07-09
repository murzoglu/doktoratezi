# TARTIŞMA ve SONUÇ — Kapsamlı Bölüm Talimatnamesi

> **Kanonik kural otoritesi:** Bölüm içerik kuralı →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §3.7 (yorum
> bölümüdür, literatür özeti değil; hipotez desteği açık; **bulgu/istatistik
> tekrarı yok**; sonunda Sonuç + öneriler); **alt başlık kullanılmaz** →
> §1.3/§5. Bu talimatname kural tanımlamaz. Klasör haritası:
> `03_bolum-hazirlik/README.md`.

## 1. Bölüm İşlevi

`TARTIŞMA ve SONUÇ` **yorum bölümü**dür: bulguları literatürle karşılaştırır,
benzer/farklı yönleri muhtemel nedenleriyle tartışır, **hipotezlerin
desteklenip desteklenmediğini** açıkça belirtir ve karma (nicel+nitel) kanıtı
bütünleştirir. Bulguların *sunumu* değil *anlamı* buradadır. Resmi şablon bu
bölümde **alt başlık kullanılmamasını** ister — akış paragraf düzeyinde kurulur
(onaylı taslak notu yoksa alt başlık açılmaz).

## 2. Yazım Sınırları (ihlal edilemez)

- **Bulgu tekrarı yok:** tablo/şekle atıf yeterli; istatistik test sonucu
  yeniden yazılmaz (marmara §3.7).
- **`GİRİŞ`/`GENEL BİLGİLER` tekrarı yok:** arka plan bilgisi burada yeniden
  anlatılmaz; yorum eklenir.
- **Nedensellik sınırı:** olgu-kontrol + kesitsel ilişkisel tasarım nedensel
  sonuç vermez; "ilişkili/öngörüyor" dili korunur, "neden oluyor" yazılmaz.
- **Kanıt türü ayrımı:** nitel tema nicel etki kanıtı, nicel sonuç nitel temanın
  nedensel/mekanistik kanıtı yapılmaz (marmara §6).
- **Öneriler** yalnız çalışma amacı ve bulgularıyla **doğrudan** bağlantılı.

## 3. Önerilen İç Akış (paragraf omurgası, alt başlıksız)

1. **Ana bulguların kısa sentezi** — birkaç cümlede en önemli çıktılar (tekrar
   değil, çerçeveleme).
2. **H1–H4 bulgularının literatürle karşılaştırması** — her hipotez için
   destek/kısmi destek/desteklenmeme açık; benzer/farklı çalışmalar, olası
   nedenler; etki büyüklüğü **tedbir denetimi** ile (tek meta-analiz mutlak
   değil; GA; yayın yanlılığı; popülasyon transferi; korelasyon ≠ nedensellik).
3. **H5 diadik tutarlılık — karma yeniliğin yorumu** — nicel uyum *hangi
   boyutlarda/ne kadar*; nitel triadik kol *neden/nasıl*. Bu tezin birincil
   katkısı burada bütünleştirilir.
4. **Nitel temaların yorumu** — 4 makro tema literatür ve nicel örüntülerle;
   negatif/aykırı vaka (deviant case) ve refleksif okuma dahil.
5. **Karma bütünleştirme** — joint display üzerinden **uyum / tamamlayıcılık /
   ayrışma / açıklayıcı genişleme** alanları açık adlandırılır; ayrışma bir
   "hata" değil teorik katkı olarak okunur (ör. EMBU skoru ↔ görüşme ambivalansı).
6. **Güçlü yönler** — karma tasarım, triad, çok-bilgi-kaynaklı yapı, açık bilim,
   tekrarlanabilirlik.
7. **Sınırlılıklar** — kesitsel/nedensellik, örneklem (nicel 241 aile; nitel 7
   aile — aktarılabilirlik, genellenebilirlik değil), öz-bildirim/sosyal
   istenirlik, ölçek sınırları, informant yanlılığı, tek-merkez/kültürel bağlam.
8. **Sonuç** — varılan sonuçlar açık/kısa; amacın ne ölçüde gerçekleştiği.
9. **Öneriler** — klinik/aile, araştırma ve (varsa) politika; amaç-bulgu ile
   sınırlı; aşırı genelleme yok.

## 4. Karma yorum disiplini

- Her karma cümlede **hangi kanıt türünün ne dediği** ayrılır; joint display
  etiketi (uyum/tamamlayıcılık/ayrışma/genişleme) yoruma taşınır.
- H5'te "nicel *ne*, nitel *neden/nasıl*" çerçevesi korunur — nitel, nicel uyumu
  *açıklar*, *kanıtlamaz*.
- Nitel aktarılabilirlik (thick description) ile nicel genellenebilirlik ayrı
  kavramlar olarak yazılır.

## 5. Tedbir denetimi (her çıkarım öncesi)

Yorum yazmadan önce asgari kontrol (detay `t1dm-tez-rehberi`
`references/tedbir-ve-hatalar.md`): ortalama+medyan birlikte mi; aykırı değer/
Simpson altgrup denetimi; çoklu karşılaştırma; korelasyon→nedensellik kayması
yok; ondalık kesinlik gerçekçi; confirmatory ↔ `[KEŞİFSEL]` ayrımı korunuyor.

## 6. Anti-pattern'ler (bu bölümde yapma)

- Bulguyu/istatistik sonucunu yeniden dökmek; Giriş/Genel Bilgiler'i tekrarlamak.
- Nedensel dil ("neden olur", "yol açar") kurmak.
- Nitel temayı nicel kanıt, nicel sonucu nitel mekanizma kanıtı yapmak.
- Post-hoc/keşifsel bulguyu doğrulanmış sonuç gibi yorumlamak.
- Öneriyi bulgu kapsamının ötesine genişletmek; alt başlık açmak (onaysız).

## 7. Kanıt eşlemesi (repo + dış)

| Yorum bileşeni | Kaynak | Sınır |
|---|---|---|
| Hipotez sonucu | CSR, `outputs/models`, SAP | Bulgu tekrarı değil, yorum. |
| Literatür karşılaştırması | Evidentia hattı + ledger `cite-ok` | Tam metin + çift AI-reliability kapalı. |
| Nitel tema yorumu | `docs/niteliksel/qualitative_canonical_results_report.md` | De-identified; negatif vaka dahil. |
| Karma bütünleştirme | `05_entegrasyon/nitel-nicel-joint-display-plan.md` | Kanıt türü etiketli. |
| Sınırlılık/tedbir | `t1dm-tez-rehberi` tedbir referansı | Nedensellik/genelleme sınırı. |

## 8. Kapanış kapıları

- [ ] Ayrıntılı bulgu/istatistik tekrarı yok; yalnız yorum.
- [ ] Her hipotez için destek durumu açık yazıldı.
- [ ] Nedensellik sınırı ve kanıt türü ayrımı korundu.
- [ ] Karma bütünleştirme joint display etiketiyle yapıldı; ayrışma teorik
      okundu, hata sayılmadı.
- [ ] Öneriler amaç-bulgu ile sınırlı; alt başlık yok (onaysız).
- [ ] Dış referanslar ledger `cite-ok` + çift AI-reliability (`talimatname` §6).
- [ ] Format §12 + `sci-audit` axis G/A–F blocker'sız.
- [ ] Kapı 0–5 sertifikasyonu + açık onay.
