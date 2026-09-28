# Gereç ve Yöntem İçin Eklere Aktarım Önerisi

**Durum:** Karar ve yerleştirme notu. Bu belge, metin veya analiz çıktısı taşımamaktadır.

**Kapsam:** Danışman inceleme Word taslağındaki Özet ve Gereç-Yöntem anlatımı ile mevcut `chapters/07_ekler.qmd` kapsamı karşılaştırılmıştır. Amaç, ana metni ileri istatistik ayrıntısıyla yormadan yöntemin bilimsel olarak denetlenebilir kalmasını sağlamaktır.

## Genel Karar

Yeni bir ek numarası açılması önerilmemektedir. İleri yöntemlerin ayrıntılı tablosu, parametresi, tanı grafiği ve alternatif model sonucu zaten Ek 3, Ek 5, Ek 6, Ek 7, Ek 8 ve Ek 9 içinde yer almaktadır. Ana metinde her yöntemin **neden kullanıldığı**, **hangi soruyu yanıtladığı** ve **sonucun nasıl yorumlandığı** kısa biçimde kalmalıdır. Sayısal ayrıntılar ve teknik tanılar doğru mevcut eke yönlendirilmelidir.

Bu not yalnız öneridir. QMD kaynakları, tez ekleri veya analiz artefaktları bu belge oluşturulurken değiştirilmemiştir.

## Önerilen Yerleştirme Matrisi

| Ana metin alanı | Eke aktarılabilecek ayrıntı | Mevcut ek hedefi | Ana metinde kalması gereken | Karar |
|---|---|---|---|---|
| 5.7 Ölçme araçlarının psikometrik değerlendirmesi | Madde dağılımları, alfa/omega tabloları, faktör yükleri, uyum indeksleri, kategori doluluğu, değişmezlik yakınsama tanıları ve çoklu evren ayrıntıları | Ek 3 ve Ek 7 | Psikometrik değerlendirmenin amacı; yedi değerlendirme ekseni; karar eşiklerinin kısa anlamı | Zaten eklerde kapsamlı biçimde yer alıyor |
| H5 anne-çocuk uyumu | Yanıt yüzeyi katsayı formülleri, Bland-Altman ve diadik model tanıları, alternatif uyum ölçütlerinin tam tabloları | Ek 4 ve Ek 8.6 | Uyumun tek bir katsayıyla sınırlı olmadığı ve her yöntemin hangi uyum boyutunu değerlendirdiği | Ek yönlendirmesi güçlendirilmeli |
| 5.8.5 Duyarlılık ve sağlamlık çözümlemeleri | Çoklu evren spesifikasyon dizisi, TOST duyarlılık bantları, E-değeri/falsifikasyon tabloları, merkez-dönem alt örneklem sonuçları | Ek 5, Ek 8.8-8.9 ve Ek 9.1-9.2 | Ana bulgunun alternatif makul varsayımlara ne ölçüde dayandığı; TOST ve E-değerinin kısa amacı | Zaten eklerde yer alıyor |
| 5.8.6 Bayesçi paralel analiz | Önsel merkez/genişlik seçenekleri, posterior tabloları, ROPE yüzdeleri, MCMC yakınsama ve tanı grafikleri | Ek 6 ve Ek 9.3 | Bayesçi analizin fark yokluğuna ilişkin doğrudan kanıtı neden tamamladığı; BF10 ve ROPE'un kısa anlamı | Zaten eklerde yer alıyor |
| 5.8.7 IRT ve trifaktör çözümlemeleri | Madde düzeyi bilgi eğrileri, taban etkisine duyarlı kestirimler ve trifaktör yükleme yapısı | Ek 8.7 | Bu çözümlemelerin birincil manifest puan modellerinin yerine geçmediği | Zaten eklerde yer alıyor |
| 5.8.7 klinik ayırt etme çözümlemeleri | ROC, iç doğrulama, kalibrasyon ve karar eğrisi ayrıntıları | Ek 8.8 | Çözümlemenin tanı koyma amacı taşımadığı ve yalnız keşifsel klinik yarar bilgisi verdiği | Zaten eklerde yer alıyor |
| 5.8.7 latent profil ve ağ çözümlemeleri | Model sayısı ölçütleri, profil üyelikleri, ağ kararlılığı ve merkezilik tanıları | Henüz ayrılmış, okunabilir bir ek alt başlığı yok | Bu çözümlemelerin keşifsel niteliği | Ancak kanonik çıktı ve son anlatım onaylanırsa Ek 8 altında yeni alt başlık açılmalı; aksi halde ayrıntı eklenmemeli |

## Ana Metinde Kalacak Bilgiler

- BH-FDR ve Holm düzeltmelerinin yanlış pozitif bulgu riskini azaltma amacı.
- FIML, çoklu atama, WLSMV, DAG ve IPTW'nin hangi veri veya karşılaştırma sorununu ele aldığına ilişkin birer kısa açıklama.
- H1-H5 modellerinin araştırma sorusuyla bağlantısı.
- TOST, E-değeri, ROPE ve BF10'un yalnız karar için gerekli yalın anlamı.
- Kesitsel tasarım, merkez-dönem örtüşmesi ve ölçülmemiş karıştırıcılara ilişkin yorum sınırları.

Bu unsurlar eklerde bırakılırsa, temel istatistik bilgisi olan hekim okuyucu yöntemin nedenini takip edemez. Bu nedenle yalnız teknik ayrıntı eklenmeli; yöntem gerekçesi ve yorum sınırı ana metinden çıkarılmamalıdır.

## Eklere Aktarılmaması Gerekenler

- Birincil hipotezlerin sonuçları, yönü, belirsizliği ve klinik yorumu.
- Ana model seçiminin gerekçesi ve tasarıma bağlı sınırlılıklar.
- Ham veri, satır düzeyinde çıktı, kimliklendirici, erişim anahtarı, dosya yolu veya çalışma ortamı ayrıntısı.
- SHA-256 denetiminin komutları, kilit dosyası içeriği, paket manifestleri ve çalışma günlüğü. Ana metindeki kısa bütünlük açıklaması yeterlidir; teknik kayıtlar tez ekinden çok repo içi yeniden üretilebilirlik belgelerinde kalmalıdır.

## QMD Entegrasyonunda Önerilen Çapraz Atıflar

Word taslağındaki anlatım QMD kaynaklarına işlendiğinde aşağıdaki kısa yönlendirmeler yeterlidir:

- Psikometrik ayrıntılar için: `Ek 3 ve Ek 7`.
- Duyarlılık, çoklu evren, TOST ve ölçülmemiş karıştırıcı ayrıntıları için: `Ek 5, Ek 8.8-8.9 ve Ek 9.1-9.2`.
- Bayesçi önsel ve yakınsama ayrıntıları için: `Ek 6 ve Ek 9.3`.
- IRT, trifaktör ve klinik ayırt etme çözümlemeleri için: `Ek 8.7-8.8`.

Bu atıflar, ana metindeki genel ifadeyi “ilgili eklerde sunulmuştur” düzeyinde bırakmak yerine okuyucuyu doğrudan denetlenebilir içeriğe yönlendirir.

## Uygulama Sınırı

Bu not, mevcut eklerin kapsamının yeterli olduğunu ve şu anda yeni bir ek veya yeni bir sayısal analiz gerekmediğini gösterir. Latent profil ve ağ çözümlemeleri için ek açılması, yalnız ilgili kanonik çıktıların varlığı, sonuç metniyle uyumu ve tezde kalmasına yönelik nihai karar doğrulandıktan sonra değerlendirilmelidir.
