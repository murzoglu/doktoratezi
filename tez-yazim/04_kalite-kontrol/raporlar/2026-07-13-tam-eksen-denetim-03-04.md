# Tam-Eksen Bilimsel Bütünlük Denetimi — Gereç ve Yöntem (03) + Bulgular (04)

**Tarih:** 2026-07-13
**Kapsam:** `chapters/03_gerec_ve_yontem.qmd` + `chapters/04_bulgular.qmd`
**Sıkılık:** certification (sertifikasyon kapısı)
**Eksenler:** sci-audit A–G (yedi eksen)
**Bağlam:** Faz-2 kapanış kapısı (03↔04 açıklayıcılık + anlam akışı + uyum mükemmelleştirme sonrası doğrulama)

---

## Yönetici Özeti

| Eksen | 03 | 04 | Sonuç |
|---|---|---|---|
| **A** — Atıf bütünlüğü | 0 kırık | 0 kırık | ✅ 39 benzersiz @key, tamamı `references.bib`'te tanımlı; Faz-2'de yeni atıf eklenmedi |
| **B** — İddia temellendirme | temiz | temiz | ✅ Sayısal iddialar CSR §9–16'ya, nitel ankrajlar kanonik nitel dosyaya izlenir (Faz-1 Görev-13 izlenebilirlik geçişi) |
| **C** — İstatistik forensik | 0/0/0 | 0/0/0 | ✅ statcheck/GRIM/GRIMMER/SPRITE/CI/yüzde/alt-grup tutarsızlık yok |
| **D** — Halüsinasyon | temiz | temiz | ✅ Varlık (ölçek/yöntem/kurum) reel; Faz-2'de yeni varlık girmedi |
| **E** — Kılavuz uyumu | JARS-Quant + COREQ (yöntem yanı) güçlü | JARS-Quant (bulgu) + COREQ (raporlama) | ⚠️ Bkz. §E — düzeltilenler + tasarım-gereği sapmalar |
| **F** — YZ şeffaflığı | tam beyan + ai_use_log | — | ✅ Kapsam + araştırmacı sorumluluğu + KVKK sınırı + insan gözden geçirme |
| **G** — Türkçe bilimsel yazım | blocker **0** | blocker **0** | ✅ Ondalık virgül, madde işaretçi, kip disiplini; kalan major'lar okunabilirlik nüdjü + tanımlı özel-ad yanlış-pozitifi |

**Blocker (her iki bölüm, tüm eksenler): 0.**

---

## Eksen ayrıntıları

### A — Atıf bütünlüğü
- İki bölümdeki 39 benzersiz `@citekey`'in tamamı `references/references.bib`'te tanımlı (0 tanımsız/halüsine anahtar).
- Faz-2 düzenlemeleri yalnız prose yeniden ifade + yönlendirme cümlesi ekledi; **yeni atıf eklenmedi** → dış re-doğrulama gerektiren yeni citation-riski yok. Mevcut yöntem atıfları (Austin, Cicchetti, Hu-Bentler, Lakens, De Los Reyes, Braun-Clarke, Malterud, Rhemtulla, Li vb.) yerleşik metodolojik kaynaklardır ve `/referans-kapisi` disiplinine tabidir.

### B — İddia temellendirme
- Bulgular'daki sayısal iddialar `docs/CLINICAL-STUDY-REPORT-FINAL.qmd §9–16`'ya, nitel ankrajlar `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd`'ye izlenir (Faz-1 Görev-13 çift-yönlü izlenebilirlik geçişi; iki düzeltme sonrası sıfır fabrikasyon: R̂ "≤1,012"; DM-kardeş reddetme β "0,13").
- Faz-2 yeni sayı üretmedi; eklenen tek sayısal öğe **241 aile** (zaten §4.1'de mevcut, izlenebilir).

### C — İstatistik forensik
- Deterministik tarama iki bölümde 0/0/0. Türkçe ondalık-virgül biçimi statcheck'in `t(df)=…,p=…` makine-okur kalıbını sınırlar; "bulgu yok", tutarsızlık yokluğu anlamındadır, tam-tarama garantisi değildir (araç caveat'i korunur).

### D — Halüsinasyon
- Adlandırılmış varlıklar (s-EMBU, KİA/SRQ, Beck, WLSMV, APIM, Olsen-Kenny, EBIC-LASSO, Marmara Üniversitesi vb.) reel ve kanonik kaynakta mevcut. Faz-2 yeni varlık girmedi → artık risk taban çizgisiyle aynı.

### E — Kılavuz uyumu (JARS-Quant + COREQ)

**Düzeltilen gerçek boşluklar (izlenebilir, fabrikasyonsuz):**

| # | Bulgu | Eksen | Aksiyon |
|---|---|---|---|
| 1 | Ağ analizi n = 238 (DM 117) ↔ çalışma DM 120 görünürde tutarsız | JARS R15 | 04: "dokuz ağ değişkeninde tam veri gerektiren EBIC-LASSO nedeniyle üç DM ailesi liste-bazlı dışlanmıştır" açıklaması eklendi (CSR §3465/3471 ile tutarlı) |
| 2 | H2 aile-düzeyi N metin içinde belirtilmemiş | JARS R3 | 04: "(241 ailenin kardeş-çifti ortalaması)" eklendi |
| 3 | Nitel örneklem gerekçesi (bilgi gücü) 4.6.x'te yok | COREQ C3 | 04: 4.6.1'e "bilgi gücü çerçevesiyle Gereç ve Yöntem'de gerekçelendirilmiştir" yönlendirmesi (öğe ch03'te tam mevcut — Marmara §3.6: yöntem ch03'te) |
| 4 | OSF kayıt tanımlayıcısı "bulunamaz" | JARS J-22/J-23 | 03: "kayıt tanımlayıcısı (OSF proje kimliği ve rezerve DOI) savunma sonrası açık paketle yayımlanacaktır" zamanlama netliği eklendi (CSR §7329 ile tutarlı) |

**Tasarım-gereği / fabrike edilemez (aksiyon alınmadı — gerekçeli):**

- **COREQ item 32 (verbatim alıntı)** — Ajan "blocker" işaretledi. **Reddedildi:** Kanonik nitel kaynağın **kendisi** yalnız quote-ID ankrajı kullanır (verbatim çocuk-görüşme metni KVKK çocuk-sağlığı sınırı gereği raporlanmaz; `quotes_used.csv` metin kolonu içermez). 04 kaynağına sadıktır ve "ham görüşme metni raporlanmamıştır" diye **açıkça beyan eder** → açıklanmış, etik-gerekçeli sapma. Alıntı eklemek KVKK ihlali + kanonik-dışı fabrikasyon olurdu.
- **H4 SEM χ²(df)** — Kaynakta yok (χ²(15)=40,81 aslında DM Olsen-Kenny reddetme modeline aittir, 04 zaten doğru raporlar). Eklemek fabrikasyon olurdu → atlandı.
- **H2 boyut-düzeyi g + GA nokta tahminleri** — Şekil 11.2 boyut-düzeyi g + %95 GA taşır (Marmara: "aynı bulgu hem tablo hem şekil değil"); metindeki d < 0,20 bandı + şekil yeterli.
- **H5 ICC güven aralıkları** — Psikometri/ICC tablosunda mevcut (CSR §1865: "tüm ICC değerleri %95 GA eşliğinde"); metin nokta değeri verir, tablo GA taşır.
- **Power girdisi etki büyüklükleri (J-6)**, **KİA Türkçe psikometrisi (J-8)** — kaynak değer olmadan eklenemez; minör, şeffaflık notu.

**Verdict E:** JARS-Quant + COREQ (yöntem yanı) güçlü uyum; sıfır blocker, sıfır gerçek "missing" (her öğe ya mevcut ya açıklanmış sınırlılık). Kalan minörler kaynak-değeri gerektiren şeffaflık eklemeleri.

### F — YZ şeffaflığı
- 03'te tam beyan (satır 201): büyük dil modeli araçları yalnız yazım/düzenleme/tutarlılık ön-denetimi; kodlama/tema/yorum kararları araştırmacıda; ham döküm/demografi/takma-ad haritası aktarılmadı; çıktılar insan gözden geçirmesinden geçti. `niteliksel/99_ai_use_log/ai_use_log.csv` mevcut (69 satır).

### G — Türkçe bilimsel yazım
- **Blocker 0** (İngilizce ondalık-nokta p-değeri yok; ondalık virgül tutarlı).
- 03 major: 21 sentence-long + 9 sentence-too-long + 5 repeated-word + 5 paragraph-long (okunabilirlik nüdjü) + 2 english-term-leak (**yanlış-pozitif**: FMSF/OSF tanımlı özel-adları) + 4 decimal-dot (**yanlış-pozitif**: sürüm 3.01 / tarih 06.01·09.2023).
- 04 major: 6 sentence-long + 3 sentence-too-long + 3 decimal-dot (kimlik/tarih) + 1 paragraph.
- Faz-2 eklemeleri sonrası blocker sabit 0.

---

## Sonuç

İki bölüm de **certification kapısını yedi eksende blocker'sız geçer.** Dört gerçek, kaynağa-izlenebilir uyum boşluğu düzeltildi; kalan işaretlemeler ya tasarım-gereği (KVKK verbatim sınırı) ya kaynak-değeri gerektiren minör şeffaflık eklemeleri ya da okunabilirlik nüdjü / araç yanlış-pozitifidir. 03↔04 uyumu (yöntem adları, hipotez çerçevesi, ondalık biçim, H5 beş-strateji/≥3-strateji kuralı, örneklem N'leri, SRQ boyut adları) hizalıdır.
