# Karma Sentez Kanonik — Joint-Display ve Çapraz-Kol Meta-Çıkarım Belgesi

**Belge statüsü:** Kanonik  
**Otorite kodu:** `05_entegrasyon/karma-sentez-kanonik`  
**Oluşturma:** 2026-07-11  
**Kaynak ledger:** `tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv`  
**Tüketiciler:** Task 5 (yönetişim/README) bu belgeye işaret eder; Task 6 (04/05 bölüm taslakları) §4 köprü cümlelerini enjeksiyon kaynağı olarak kullanır.

---

## §0 Otorite Zinciri ve Kanonik Girdi Beyanı

### §0.1 Otorite zinciri

```
tez-yazim/05_entegrasyon/README.md            (entegrasyon katmanı meta-otorite)
        ↓ işaret eder
tez-yazim/05_entegrasyon/karma-sentez-kanonik.md   (BU BELGE — joint-display + meta-çıkarım)
        ↓ türetilmiştir
tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv   (joint-display §1 veri kaynağı, 6 satır)
```

Bu belge, `05_entegrasyon/README.md` otorite hiyerarşisi içinde **kanonik joint-display + çapraz-kol meta-çıkarım belgesidir**. Bölüm taslakları ve yönetişim dosyaları buraya işaret eder; buradan türetmeden bağımsız karma sentez üretemez.

### §0.2 KVKK sınırı

Bu belge ham görüşme metni, doğrudan alıntı, kimlikleyici bilgi veya aile-düzeyi geri-tanımlanabilir satır içermez. Tüm içerik yalnızca aşağıdaki iki kanonik manuskript dosyası ve kanıt ledgerinden türetilmiştir.

### §0.3 Kanonik girdi beyanı

| Kaynak kol | Tam yol | İçerik türü |
|---|---|---|
| Nicel kanonik kaynak | `docs/CLINICAL-STUDY-REPORT-FINAL.qmd` | H1–H5 karar kutuları + hipotez özeti |
| Nitel kanonik kaynak | `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` | 4 makro tema + çapraz bilimsel neticeler |
| Kanıt ledgeri | `tez-yazim/05_entegrasyon/karma-kanit-ledgeri.tsv` | 6 satır, ankraj-provenanslı ham kaynak |

Bu belgede yer alan hiçbir nicel değer veya nitel ifade yukarıdaki kaynaklara `dosya#ankraj` yoluyla bağlanamıyorsa kullanılamaz. Ekleme yapmadan önce ledger veya kaynak dosya güncellenmelidir.

---

## §1 Joint-Display (Yorumsuz — Bulgular Hazır)

*Bu tablo doğrudan `karma-kanit-ledgeri.tsv` 6 satırından türetilmiştir. Her hücre `dosya#ankraj` provenanslıdır. Yorum ve gerekçe §2–§3'tedir; bu tabloya yorum eklenmez.*

| Odak | Nicel verdikt (kaynak) | Nitel örüntü (kaynak) | İlişki türü | Yorum sınırı |
|---|---|---|---|---|
| **H1 — Çocuk algısı (EMBU-C)** | DM çocuklarının kontrol çocuklarına kıyasla reddetme algısını küçük ama tutarlı biçimde daha yüksek bildirdiği [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar`] | Normalleşme dili yükün yokluğu anlamına gelmez; çoğu zaman yükü sürdürülebilir kılma stratejisidir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-3`] | Açıklayıcı genişleme | Nedensellik yok; nitel deneyimsel bağlam nicel reddetme algısının mekanizması değil |
| **H2 — Kardeş ilişkisi (KİA/SRQ)** | Dört SRQ boyutunda aynı yönde belirgin bir DM × Kontrol farkı üretmemiştir [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar`] | Ebeveyn ilgisinin yeniden dağılımını kendi gündelik yaşamında taşımaktadır [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-1`] | Açıklayıcı genişleme | Nedensellik yok; nicel fark yokluğu nitel sessiz yükü silmez; farklı düzeyler ölçülüyor |
| **H3 — Anne öz-rapor (EMBU-P)** | Anne öz-bildirimi düzleminde DM × Kontrol farkı bulunmadığını tutarlı biçimde desteklemektedir [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar`] | Bakımın normalleştirilmiş ve ahlaki sorumluluk olarak içselleştirilmiş biçimidir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2`] | Açıklayıcı genişleme | Nedensellik yok; sınırlı nicel fark nitel içselleştirme süreciyle yorumlanır |
| **H4 — Beck → EMBU-P (SEM)** | Anne depresif belirti yükü dört EMBU-P alt ölçeğinden üçünde anlamlı yapısal yollar üretmiştir [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar`] | Suçluluk yalnız geçmişe değil gelecekteki bakım sorumluluğuna da bağlanır [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2`] | Uyum | Kesitsel SEM; nedensel risk aktarımı yorumu yok; nitel psikolojik yük klinik yorum alanı |
| **H5 — Diadik tutarlılık** | Ön-kayıtlı triangülasyon şartı karşılanmayan, tek-strateji/tek-alt-ölçek bir sinyal [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h5-karar`] | Aynı olayın farklı sorumluluk, risk ve adalet çerçeveleriyle anlamlandırıldığını gösterir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4`] | Açıklayıcı genişleme | Nedensellik yok; algı uyumsuzluğu ölçüm hatası değil, bağlamsal rol-temelli deneyim farkı |
| **Meta — Triadik informant asimetrisi** | Genel bir ebeveynlik farkından çok bilgi-veren düzeyinde ayrışma olarak yorumlanmaktadır [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#sec-genel-hipotez-ozet`] | Triadik farklılık bilimsel sonuçtur, hata değildir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#sec-capraz`] | Tamamlayıcılık | Nicel örüntü + nitel anlam birbirini tamamlar; H düzeyinde ayrı bağlamsal okuma gerekli |

---

## §2 İlişki-Türü Gerekçelendirmesi

### §2.1 H1 — Açıklayıcı genişleme

Nicel reddetme bulgusu, DM grubunda çocuk algısının kontrol grubuna kıyasla yüksek olduğunu ortaya koyar [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h1-karar`]. Keşifsel grup-içi rol kontrastı bu bulguyu bir adım daha yerleştirir: kontrol dışlanıp aile içinde bakıldığında indeks çocuk ile sağlıklı kardeş arasında hiçbir EMBU-C boyutunda fark yoktur (dört boyut, q > 0,76); yani nicel sinyal hastalığı taşıyan çocuğu kardeşinden ayırmaz, aile/grup düzeyinde yerleşir. Bu durum nitel kolla tamamlayıcılığı netleştirir: nicel ölçüm kardeşi indeks çocuktan istatistiksel olarak ayırt edemezken, nitel Tema 1 kardeşin sessiz yükünü görünür kılar — iki kol farklı düzeyleri ölçer. Nitel Tema 3 ise DM tanılı çocuğun hastalığı hem normalleştirmeye hem yük olarak taşımaya devam ettiğini gösterir; "normalleşme" söylemi yükün işleniş biçimini açıklar, varlığını ortadan kaldırmaz [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-3`]. İki kol ayrı düzlemleri ölçer: nicel ölçek puanı reddetme algısının büyüklüğünü, nitel anlatı bu algının çocuk tarafından nasıl çerçevelendiğini verir. Nitel bulgu nicel algı ölçümünün nedenini değil, o algının deneyimsel bağlamını genişletir. İlişki türü açıklayıcı genişlemedir.

### §2.2 H2 — Açıklayıcı genişleme (Tema 1 + Tema 4 ikili bağ)

Nicel H2, dört SRQ alt ölçeğinde fark için kanıt yetersizliği verir [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar`]. Bu bulgu, kardeşin etkilenmediğini değil, grup düzeyi ölçümlerinin net ayrışma üretemediğini gösterir.

Niteliksel dosya H2'yi **iki ayrı Tema ile** ilişkilendirir:

- **Tema 1** (ledger birincil ankrajı): Kardeşin sessiz yükü — gönüllü feragat, bakım rutinlerine gömülü adalet gerilimi, ebeveyn ilgisinin yeniden dağılımını kendi yaşamında taşıma [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-1`]
- **Tema 4** (ek bağ): Triadik okumada kardeşin "kısıtlanma/gözetmenlik/adalet" dili; H5 diadik tutarlılık için nitel köprü olarak da işaretlenmiştir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4`]

Ledger Tema 1'i birincil ankraj olarak tutar çünkü Tema 1 doğrudan kardeş deneyimini betimler. Tema 4, triadik karşılaştırma düzleminde H2 için bağlamsal derinlik ekler: kardeşin nicel ölçümlerde görünmeyen yükünün aile sisteminin rol dağılımında kökenlendiğini gösterir. İlişki türü açıklayıcı genişlemedir: nitel bulgular fark yokluğunun bağlamsal okumasını (sessiz yük) ve aile sistemindeki kökenini (triadik rol) sağlar; grup farkını ne doğrular ne çürütür.

### §2.3 H3 — Açıklayıcı genişleme

Nicel H3, anne öz-bildiriminde üç-katmanlı negatif kanıt zinciriyle güçlü H₀ desteği verir [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar`]. Nitel Tema 2, anneliğin tıbbi bakım koordinatörlüğüne kaymasını ve bu rolün "normal ebeveynlik" olarak içselleştirilmesini betimler [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2`]. Sınırlı öz-bildirim farkının açıklayıcı bağlamı nicel kol tarafından üretilemez; nitel bulgu "yük yokluğu" değil "yükün ölçüm düzlemine girme biçimini kısıtlayan içselleştirme süreci" için bağlam sağlar. İlişki türü açıklayıcı genişlemedir.

### §2.4 H4 — Uyum

Nicel H4, Beck depresif belirti yükünün EMBU-P alt ölçeklerinden üçüyle anlamlı yapısal yol ilişkisi gösterdiğini ortaya koyar [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar`]. Nitel Tema 2, annenin suçluluk ve kaybetme korkusu örüntüsünün hem geçmişe hem geleceğe yönelik bakım sorumluluğuna bağlandığını gösterir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2`]. İki kol birbirini destekler: nicel yapısal yol klinik ölçüm düzleminde ilişkiyi tespit eder, nitel bulgu aynı psikolojik yük alanında anne anlatısının içeriğini betimler. Nitel bulgu nedensel mekanizma kanıtı değil, klinik yorum alanı sağlar. İlişki türü uyumdur.

### §2.5 H5 — Açıklayıcı genişleme

Nicel H5, baskın manifest kanıtın (ICC) dört boyutun tamamında Kontrol > DM yönünde seyrettiğini ve yalnızca tek alt ölçekte/tek stratejide zayıf model uyumu altında DM > Kontrol sinyali bulunduğunu gösterir; ön-kayıtlı triangülasyon şartı karşılanmamıştır [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h5-karar`]. Nitel Tema 4, aynı aile olayının anne, hasta çocuk ve sağlıklı kardeş tarafından farklı sorumluluk, risk ve adalet çerçeveleriyle anlamlandırıldığını betimler [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4`]. Nicel kol düşük uyumun *ne kadar* olduğunu ölçer; nitel kol bu ayrışmanın *neden* yapısal olarak bekleneceğini açıklar (rol-temelli deneyim). İlişki türü açıklayıcı genişlemedir.

### §2.6 Meta — Tamamlayıcılık

Genel hipotez özeti, H1 reddetme farkının anne öz-bildiriminde değil çocuk algısında belirmesini "bilgi-veren düzeyinde ayrışma" olarak konumlandırır [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#sec-genel-hipotez-ozet`]. Nitel çapraz neticeler, triadik farklılığın metodolojik gürültü değil bilimsel sonuç olduğunu teyit eder [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#sec-capraz`]. İki kol birbirini silmez: nicel veri hangi düzlemde ne yoğunlukta ayrışma bulunduğunu ölçer, nitel bulgu farklı informantların aynı aile gerçekliğini farklı perspektiflerle deneyimlemesinin kaçınılmaz olduğunu gösterir. İlişki türü tamamlayıcılıktır: her iki kol da ayrı kanıt türü üretir ve birlikte karma tezin bütünleşik bulgusunu oluşturur.

---

## §3 Çapraz-Kol Meta-Çıkarımlar

*Her meta-çıkarım tek kolun tek başına üretemeyeceği bir sonuçtur. Tüm nicel değerler ankraj-provenanslıdır.*

### Meta-1: H5 triangülasyon başarısızlığı + Tema 4 triadik farklılık → Algı ayrışması ölçüm hatası değil, rol-temelli deneyim farkıdır

Nicel H5, ön-kayıtlı "en az üç strateji uyumlu" triangülasyon şartının karşılanmadığını ve baskın manifest kanıtın (ICC, havuzlanmış anne-indeks aralığı 0,00–0,11 [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h5-karar`]) dört alt ölçekte Kontrol > DM yönünde seyrettiğini gösterir. Tek başına alındığında bu bulgu, düşük anne-çocuk algı uyumunu *ölçüm sınırlılığı* ya da *rastgele varyasyon* olarak yorumlamaya açık bırakır.

Nitel Tema 4, aynı aile olayının anne (düzen/güvenlik), hasta çocuk (beden/özerklik/sosyal görünürlük) ve sağlıklı kardeş (kısıtlanma/gözetmenlik/adalet) tarafından yapısal olarak farklı çerçevelerle deneyimlendiğini betimler [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4`].

**İki kol birlikte şunu üretir:** Düşük anne-çocuk algı uyumu, ölçüm hatasına indirgenmemesi gereken, aile içi rol farklılaşmasının nicel yansımasıdır. Nicel kol *büyüklüğü* ölçer (kaynak `#h5-karar`); nitel kol *neden ve nasıl* (rol-temelli çerçeveleme farkı) bağlamını sağlar (kaynak `#tema-4`). Bu sonuç hiçbir kol tek başına üretemez.

### Meta-2: H2 nicel fark yokluğu + Tema 1 sessiz yük → Standart kardeş ilişkisi ölçümleri T1DM bağlamındaki yük biçimini tümüyle yakalamayabilir

Nicel H2, dört SRQ alt ölçeğinde fark için kanıt yetersizliğini gösterir; Welch d değerleri < 0,20, FDR-düzeltilmiş p değerleri > 0,35 düzeyinde kalmıştır [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar`]. Bu sonuç tek başına değerlendirildiğinde, T1DM tanısının sağlıklı kardeş için ek yük yaratmadığı çıkarımına zemin oluşturabilir.

Nitel Tema 1, kardeş yükünün gönüllü feragat, sessiz uyum, bakım rutinlerine gömülü adalet gerilimi ve erken sorumluluk biçimlerinde tezahür ettiğini gösterir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-1`]. Bu yük biçimleri, kardeş ilişki kalitesi toplam puanına doğrudan yansımayabilir.

**İki kol birlikte şunu üretir:** Grup puanları düzeyindeki fark yokluğu, kardeşin etkilenmediği anlamına gelmez; T1DM bağlamında kardeş yükünün standart ilişki ölçümlerinin ötesine geçen biçimler aldığını yalnızca nitel kol görünür kılmaktadır. Bu bütünleşik okuma karma tez dışında ulaşılamaz.

### Meta-3: H3 nicel eşdeğerlik + Tema 2 içselleştirme → Ölçek farkı yokluğu psikolojik yük yokluğunu kanıtlamaz

Nicel H3, anne öz-bildiriminde güçlü H₀ desteği gösterir: BF₁₀ = 0,17–0,25 aralığı, aşırı koruma ve karşılaştırma alt ölçeklerinde TOST "Eşdeğer" kararı [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar`]. Tek başına bu bulgu, DM annelerinin psikolojik olarak kontrol anneleriyle eşdeğer olduğu çıkarımına zemin açabilir.

Nitel Tema 2, tıbbi bakım koordinatörlüğünün "normal annelik" olarak içselleştirilmesini ve bu rolün ölçek yanıtlarına sistematik biçimde yansımayabileceğini betimler [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2`].

**İki kol birlikte şunu üretir:** Nicel eşdeğerlik, annelerin bakım deneyiminin eşdeğer olduğunu değil, psikolojik yükün içselleştirme aracılığıyla öz-bildirim düzeyinde görünür olmayabileceğini düşündürür. Bu yorum yalnızca nitel bulgularla birlikte yapılabilir; nitel kol olmadan nicel H3 "yük yokluğu" olarak yorumlanmaya müsaittir.

### Meta-4: Triadik informant asimetrisi (H1 + meta-triad) → Çalışmanın birincil katkısı genel ebeveynlik farkı değil, informant düzeyi ayrışma haritalamasıdır

Nicel genel hipotez özeti, H1 reddetme sinyalinin anne öz-bildiriminde değil çocuk algısında belirmesini "bilgi-veren düzeyinde ayrışma" olarak yorumlar; bu örüntü, genel bir ebeveynlik tutumu farkından çok ölçüm düzlemi özgüllüğünün bir sonucudur [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#sec-genel-hipotez-ozet`].

Nitel çapraz neticeler, triadik farklılığın analitik gürültü değil bilimsel sonuç olduğunu teyit eder [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#sec-capraz`]. Hem nicel hem nitel kol, aynı aile gerçekliğinin farklı informantlar tarafından farklı deneyimlendiğini ayrı kanıt türleriyle gösterir.

**İki kol birlikte şunu üretir:** Bu karma çalışmanın birincil katkısı tek bir "T1DM ebeveynlik farkı" tanımlaması değil; *hangi informant*, *hangi boyut* ve *hangi deneyim düzleminde* ayrışmanın gerçekleştiğinin haritalanmasıdır. Bu harita, multi-informant nicel tasarım ile triadik nitel tasarımın birlikte kurulmasıyla üretilmiştir.

---

## §4 Tartışma Köprü Cümleleri (05'e Enjeksiyon Taslakları)

*Bu paragraflar üretim bölümü `chapters/05_tartisma_ve_sonuc.qmd`'ye enjeksiyon için hazırlanmıştır (yürütme talimatnamesi: `tez-yazim/03_bolum-hazirlik/05_tartisma-ve-sonuc.md`). Her paragraf ankraj-provenanslıdır. Kol-aşırı nedensel dil kullanılmamıştır.*

### §4.1 H5 + Tema 4 köprüsü

Diadik tutarlılık analizinde nicel kol, ön-kayıtlı triangülasyon şartını karşılamayan tek-strateji bir sinyalle karşılaşmış; baskın manifest kanıt, anne ↔ indeks çocuk algı uyumunun dört EMBU-P/EMBU-C alt ölçeğinin tamamında Kontrol grubuna kıyasla DM grubunda daha düşük seyrettiğini göstermiştir [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h5-karar`]. Bu örüntü nitel bulgularla birlikte okunduğunda, sınırlı anne-çocuk algı uyumunun ölçüm sınırlılığından çok rol-temelli bir deneyim farkını yansıtabileceği düşünülebilir: Tema 4 triadik okuma, aynı aile olayının anne, hasta çocuk ve sağlıklı kardeş tarafından farklı sorumluluk, risk ve adalet çerçeveleriyle anlamlandırıldığını göstermektedir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-4`]. Bu bağlamda diadik uyumsuzluğu yalnızca ölçüm hatasına indirgeme yerine, klinik değerlendirmede çoklu-informant perspektifinin zorunluluğuna işaret eden bir bulgu olarak konumlandırmak karma tezin metodolojik katkısını güçlendirecektir.

### §4.2 H2 + Tema 1 köprüsü

Kardeş ilişkisi analizinde nicel kol, dört SRQ alt ölçeğinde belirgin bir DM × Kontrol grup farkı üretmemiş; bu durum aktif eşdeğerlik kanıtı olmaksızın "kanıt yetersizliği" olarak raporlanmıştır [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h2-karar`]. Bununla birlikte, grup puanları düzeyinde görünmeyen bu örüntü, sağlıklı kardeşin T1DM tanısından etkilenmediğini göstermemektedir. Nitel kol, kardeşin ebeveyn ilgisinin yeniden dağılımını, sessiz feragati ve adalet gerilimini gündelik yaşamında taşıdığını ortaya koymaktadır [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-1`]. Bu iki bulgu birlikte, standart kardeş ilişkisi ölçümlerinin T1DM bağlamındaki yük biçimlerini tümüyle yakalayamayabileceğine dikkat çekmekte; klinik değerlendirmede kardeşin deneyiminin özgün bir perspektif olarak ele alınması gereğini desteklemektedir.

### §4.3 H3 + Tema 2 köprüsü

Anne öz-bildiriminde güçlü H₀ desteği içeren nicel bulgu [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h3-karar`], DM annelerinin EMBU-P ölçeğinden elde edilen puan profilinin kontrol anneleriyle eşdeğer olduğunu göstermektedir. Bu sonuç nitel bulgularla birlikte değerlendirildiğinde, sınırlı öz-bildirim farkının psikolojik yük yokluğunun değil; anneliğin tıbbi bakım koordinatörlüğüne kaymasının ve bu rolün ahlaki zorunluluk olarak içselleştirilmesinin ölçeğe doğrudan yansımayabileceğinin bağlamsal kanıtı olarak okunabilir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2`]. Bu yorum karma kanıt türü karıştırılmadan, "nitel bağlam nicel yorumu daraltır" disipliniyle kullanılmalıdır.

### §4.4 H4 + Tema 2 köprüsü

Anne depresif belirti yükü ile üç EMBU-P alt ölçeği arasındaki nicel yapısal yol bulgusu [`docs/CLINICAL-STUDY-REPORT-FINAL.qmd#h4-karar`], nitel Tema 2'nin betimsel içeriğiyle anlamlı biçimde örtüşmektedir: anne anlatılarında suçluluk, kaybetme korkusu ve sürekli tetikte olma örüntüsünün hem geçmişe hem geleceğe yönelik bakım sorumluluğuna bağlandığı görülmektedir [`niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd#tema-2`]. Nicel kol bu ilişkinin mertebe ve yönünü (kesitsel SEM yapısal yollar) ölçer; nitel kol ise aynı deneyim alanında annenin anlatısal çerçevesini betimler. Bu uyum, psikolojik yükün hem klinik ölçüm hem de yaşantı düzleminde tutarlı bir örüntü oluşturduğunu düşündürmektedir; nedensel aktarım yorumu kesitsel tasarım nedeniyle yapılmamaktadır.

---

## §5 Karma-Özel Sınırlılık: Paralel Örneklem Farkı

Bu karma çalışmanın iki kolu birbirinden bağımsız, paralel örneklemlere dayanmaktadır:

| Kol | Örneklem | Kaynak |
|---|---|---|
| Nicel kol | 241 aile (482 katılımcı; 241 aile × 2) | `CLAUDE.md` domain notu: "Veri yapısı: 482 satır = 241 aile × 2 katılımcı" |
| Nitel kol | 7 aile (21 görüşme; 7 aile × 3 bilgi verici) | `niteliksel/CLAUDE.md`: "7 aile × 3 = 21 görüşme" |

**İki kol aynı bireyleri örneklememiştir.** Eşzamanlı paralel karma yöntem tasarımı izlenmektedir. Bu durum üç sınır doğurur:

**Sınır 1 — Birleştirme yorum düzeyindedir, istatistiksel düzeyde değil.** Nitel bulgular nicel istatistikleri doğrulamak için değil, nicel bulguların bağlamsal anlamını derinleştirmek için kullanılır. "İki kol birbirini doğrular" ifadesi metodolojik olarak hatalıdır; yerine "birbirini tamamlar" veya "bağlamsal açıklama sağlar" ifadeleri kullanılmalıdır.

**Sınır 2 — Örneklem asimetrisi yorumu sınırlar.** 241 aileli nicel bulguların genel örüntüsünü 7 aileli nitel bulgularla açıklamak, nitel örneklemde temsil edilmeyen alt grupları görmezden gelme riski taşır. Bu sınır tartışma bölümünde şeffaf biçimde raporlanmalıdır.

**Sınır 3 — Aktarılabilirlik analitik genelleme gerektirir.** Nitel bulgular 7 aile T1DM deneyimini betimler; bu bağlamın 241 aileli nicel örneklemin tümüne aktarılması analitik genelleme yoluyla, istatistiksel genelleme yoluyla değil, mümkündür.

Bu sınırlılıklar karma yöntem entegrasyonunun değerini ortadan kaldırmaz; ancak iki kolun bulguları birleştirilirken "tamamlayıcı kanıt" retoriğinin "tek bütünleşik kanıt" retoriklerine dönüşmemesini zorunlu kılar.

---

*Belge sonu. Revizyon için: ledger güncellenmeli, ardından bu belge § bazında güncellenmelidir. Yeni ankraj eklemeden önce `dosya#ankraj` kaynakta var mı kontrol edilmelidir.*
