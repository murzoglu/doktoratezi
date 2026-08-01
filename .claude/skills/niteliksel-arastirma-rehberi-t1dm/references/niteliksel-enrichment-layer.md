# Niteliksel Araştırma Metodolojisi Layer (0.5.Q)

**Optional enrichment module** — evidentia dış-literatür koşumu niteliksel metodoloji bağlamına
girdiğinde yüklenir. Zorunlu değildir; evidentia'nın çekirdek narratif derin-lit / PRISMA hattı bu
katman olmadan da çalışır. Çıktı → açıkça etiketlenmiş **enrichment appendix** (çekirdek rapora
karışmaz). **In-repo proje katmanı:** evidentia plugin-cache'i salt-okunurdur; bu katman
`niteliksel-arastirma-rehberi-t1dm` skill'i + `.claude/evidentia.local.md` (`default_modules`)
üzerinden devreye girer — cache auto-ingest iddia edilmez.

**Triggers (full):** niteliksel, nitel araştırma, qualitative, refleksif tematik analiz, RTA,
reflexive thematic analysis, Braun-Clarke, tematik analiz, kodlama güvenirliği, coding reliability,
COREQ, SRQR, JARS-Qual, GRAMMS, trustworthiness, credibility, dependability, confirmability,
transferability, bilgi gücü, information power, saturation, doygunluk, member checking, üye
kontrolü, negatif vaka, negative case, reflexivity, positionality, multi-informant, triadic,
grounded theory, IPA, framework analysis, phenomenology, thick description, qualitative rigor.

---

## 1. Otorite kaynak katmanları (Tier 1 — metodoloji)
- **RTA / TA aile:** Braun & Clarke (2006, 2019, 2021, 2022), Byrne (2022); reflexive vs.
  coding-reliability vs. codebook TA ayrımı — bir dış kaynağın hangi TA ailesine ait olduğu
  değerlendirilir (paradigma karışması sık hatadır).
- **Örneklem yeterliliği:** Malterud, Siersma & Guassora (2016) bilgi gücü; doygunluk eleştirisi
  (Braun & Clarke 2021). Dış kaynak "saturation" iddia ediyorsa TA ailesiyle tutarlılığı sorgulanır.
- **Güvenilirlik:** Lincoln & Guba (1985); Tracy (2010) "big-tent" kriterleri; Nowell et al. (2017).
- **Raporlama:** Tong et al. (2007) COREQ; O'Brien et al. (2014) SRQR; Levitt et al. (2018)
  JARS-Qual; O'Cathain et al. (2008) GRAMMS (karma).

## 2. Terapötik/klinik bağlam katmanı (Tier 2)
- Pediatrik kronik hastalık + aile yükü + multi-informant discrepancy literatürü (T1DM ebeveynlik,
  kardeş deneyimi, maternal caregiving). Bu, niteliksel bulguların **konumlandırılması** içindir;
  metodoloji katmanıyla karıştırılmaz.

## 3. Kanıt madenciliği (evidentia hattı)
- Narratif derin-lit modu varsayılan (SR değil): D0-D6 kaskadı; **minerva** D2 discovery + D4
  full-text rungu (bağlıysa); PubMed/EPMC, OpenAlex, Semantic Scholar, YÖK Akademik/YÖK Tez
  (Türkçe niteliksel tez katmanı), annas-reader copyright-gated tam metin.
- Konferans/gri literatür yalnız bağlam (Tier 6); bir claim'i asla tek başına dayamaz.

## 4. Değerlendirme kontrol listesi (niteliksel-özgü)
Bir dış niteliksel kaynağı değerlendirirken:
- **Paradigma-yöntem uyumu** (RTA'ya kappa iliştirilmiş mi? saturation yanlış mı kullanılmış?).
- **Tema = analitik iddia mı, konu-özeti mi?** (domain-summary temaları zayıf.)
- **Refleksivite + positionality** raporlanmış mı?
- **Trustworthiness** dört ölçütün dayanağı var mı?
- **Raporlama standardı** (COREQ/SRQR/JARS) karşılanmış mı?
- **Transfer riski:** popülasyon/bağlam bizim T1DM triadik bağlamımıza uyar mı?

## 5. Output → enrichment appendix (niteliksel-metodoloji yerleşim notu), asla çekirdek SR bölümü
Enrichment appendix'e: (a) dış kaynağın TA-ailesi + paradigma sınıflaması, (b) trustworthiness/
raporlama-standardı uyum notu, (c) bizim triadik RTA bağlamımıza transfer edilebilirlik yargısı,
(d) çelişki/gap kaydı. Bu katman **kendi verimizin** kodlama/tema/yorum kararını üretmez — o karar
`rta-ve-analiz.md` + araştırmacıdadır; bu katman yalnız **dış metodoloji literatürünü** çerçeveler.

- **Referans Bütünlük Şiarı (RBŞ — konstitüsyonel; `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` §4.1):** Bir referanstan zenginleştirme/analiz yaparken makalenin **bir parçasını değil tamamını geniş bağlamda semantik kavra**, bu bağlamı **rafine ederek** revize et; **hem kaynağın hem tez metninin somut bilimsel iddialarını çarpıtma** (cherry-pick / düzleştirme / abartma yok; kaynak kendi kapsam+koşuluyla aktarılır).

## Çapraz referanslar
- evidentia köprüsü → `literatur-kanit-evidentia.md`
- Analiz/değerlendirme/raporlama → `rta-ve-analiz.md`, `gecerlik-ve-degerlendirme.md`, `raporlama-coreq-jars.md`
