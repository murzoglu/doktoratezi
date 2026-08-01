# Spec — Kapsamlı Tez Kontrol Checklisti + Doğrulama Script'i

## Problem Tanımı

Repo, olgun bir kalite-kontrol katmanına sahip: `tez-yazim/04_kalite-kontrol/`
altında 6-kapı (Kapı 0–5) sertifikasyon playbook'u, sertifika şablonu ve eksen
bazlı alt-checklistler (`format-kontrol-listesi.md`, `kanit-ve-gizlilik-kontrol-listesi.md`,
`ai-mcp-kullanim-kontrol-listesi.md`, `turkce-bilimsel-yazim-denetimi.md`,
`render-bagimliliklari.md`) mevcut. Ayrıca `scripts/util/` altında çalışan
doğrulama araçları var (`bib_hygiene.py`, `karma_ledger_check.py`,
`claim_certification.py`, `csr_numeric_trace_audit.py`, `csr_causal_label_audit.py`,
`csr_block_review.py`, `tr_corpus_audit.py`) ve slash komutları
(`/tez-oturum`, `/bolum-sertifika`, `/referans-kapisi`, `/tez-literatur`,
`/tez-dogrulama`).

Ancak **tek, uçtan uca, tüm tezi kapsayan bir "master kontrol checklisti"
yok**. Mevcut checklistler eksen-parçalıdır ve her madde için (a) somut kontrol
mekanizması, (b) çalıştırılabilir komut/eşik ve (c) oto/manuel etiketi tek
yerde toplanmış değildir. Bunun sonucu:

1. **Dağınık doğrulama:** Bir bölümü veya tüm tezi teslim-öncesi kontrol etmek
   için hangi aracın hangi sırada koşacağı ve neyin PASS sayılacağı tek bir
   izlenebilir belgede yok.
2. **Otomasyon boşluğu:** Araçlar tek tek elle koşuluyor; hepsini sırayla koşup
   birleşik PASS/FAIL raporu üreten tek bir orkestratör script yok.
3. **Tez-düzeyi eksenler eksik:** Format bütünlüğü (Marmara §1), render/crossref
   bütünlüğü, targets pipeline tazeliği, PII/gizlilik sınırları, sayısal-iddia
   izlenebilirliği gibi eksenler bölüm-sertifikasında kısmen var ama tez-düzeyi
   toplu kapıda birleştirilmemiş.

## Kapsam

Kullanıcı kararları:
- **Kapsam:** İki katmanlı — hem **bölüm-düzeyi** (her `chapters/*.qmd` için
  tekrar koşulabilir) hem **tez-düzeyi** (kapanış/teslim öncesi bütün tez)
  checklist, tek belgede.
- **Mevcut sistemle ilişki:** Mevcut 6-kapı checklistlerini **genişlet** —
  eksik eksenleri var olan yapıya ekle, master checklist onları birleştirip
  bağlar (sıfırdan paralel sistem değil).
- **Madde mekanizması:** Her madde için **hem** çalıştırılabilir komut + beklenen
  çıktı + PASS eşiği **hem** Otomatik/Manuel etiketi + kanıt konumu.
- **Çıktı:** **Markdown master checklist + Python doğrulama script'i**
  (`scripts/util/` deseninde).
- **Dil:** Türkçe, çok kapsamlı.

### Script davranışı (kritik)
Doğrulama script'i **tüm otomatikleştirilebilir araçları sırayla koşar ve
birleşik rapor üretir**; hiçbir dosyayı değiştirmez (salt-okuma denetim).
Her madde için PASS/FAIL/SKIP + kısa kanıt satırı basar. Manuel maddeler
"MANUEL — elle kontrol gerekli" olarak işaretlenir (script bunları FAIL saymaz,
raporda ayrı listeler). Script bir özet exit kodu döndürür (0 = tüm otomatik
maddeler PASS; >0 = en az bir otomatik HARD fail) ki hem elde hem CI/pre-teslim
akışında kullanılabilsin.

### Kapsam dışı
- Mevcut chapter içeriğini düzeltmek/yeniden yazmak (checklist tespit eder,
  düzeltme ayrı iştir).
- Yeni bilimsel analiz veya pipeline hedefi eklemek.
- CI altyapısı (GitHub Actions vb.) kurmak — script CI-uyumlu yazılır ama
  workflow tanımı bu iş kapsamında değil.

## Gereksinimler

### R1 — Master checklist belgesi
- Yeni dosya: `tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md`.
- Türkçe, çok kapsamlı; iki ana bölüm: **(A) Bölüm-düzeyi kapı seti** ve
  **(B) Tez-düzeyi kapanış seti**.
- Belge, mevcut 6-kapı playbook'unu ve alt-checklistleri **kanonik otorite**
  olarak referanslar; onların yerine geçmez, üstlerinde birleştirici indeks olur.
- Her checklist maddesi standart bir satır/blok şemasıyla yazılır (bkz. R3).

### R2 — Eksen kapsamı (checklist neyi kontrol eder)
Master checklist en az şu eksenleri madde madde kapsar:
1. **Kapsam & Gizlilik (Kapı 0):** PII sınırları (`ad/soyad` düşürme, `data/raw|
   identified|cleaned|backup` git-dışı), credential/`.lock` erişimi,
   `.claude/settings.json` deny uyumu.
2. **Kanıt & Literatür (Kapı 1–2):** kaynaksız-sayı taraması, atıf künye
   bütünlüğü, ledger mutabakatı, full-text/Zotero izi.
3. **Bölüm metni & kılavuz uyumu (Kapı 3):** Marmara format kontratı §1 (kenar
   boşluk, satır aralığı, font, başlık düzeni, tablo/şekil başlık biçimi),
   bölüm sırası, başlık numaralandırma (çift-numara yok).
4. **Türkçe imla, akış, mantık (Kapı 4):** Türkçe bilimsel yazım denetimi,
   ondalık virgül, retorik/insan-Türkçesi kontrolleri.
5. **AI-reliability & teknik doğrulama (Kapı 5):** iki-kol hook derlemesi,
   render (quarto), crossref/atıf bütünlüğü, sayısal-iddia → CSV izi,
   nedensel-etiket denetimi.
6. **Pipeline & üretilebilirlik (tez-düzeyi):** `renv::status()` temiz,
   `targets::tar_make()` tazeliği (outdated hedef yok), üretilmiş
   tablo/şekil artefaktlarının varlığı.
7. **Render & çıktı bütünlüğü (tez-düzeyi):** `quarto render thesis.qmd`
   exit 0; HTML/PDF'te 0 çözülmemiş `?@`; 0 kırık atıf; şekil gömme; PDF
   Marmara format ölçüleri (A4, kenar boşluk, font).
8. **Ön/arka bölümler & teslim (tez-düzeyi):** özet/summary kelime sınırı +
   anahtar sözcükler, kısaltmalar, içindekiler/şekil/tablo listeleri, 00a resmi
   alanlar, 06 özgeçmiş, 07 ek yer-tutucuları, referans listesi.

### R3 — Madde şeması (her checklist maddesi için)
Her madde şu alanları içerir:
- **ID:** kısa benzersiz kod (ör. `K0-PII-01`).
- **Kontrol maddesi:** ne doğrulanıyor (Türkçe, tek cümle).
- **Mekanizma:** nasıl kontrol edilir (araç adı / gözle bakış yöntemi).
- **Komut:** çalıştırılabilir komut satırı (otomatik maddelerde) veya
  "MANUEL" (gözle kontrol maddelerinde).
- **PASS ölçütü:** beklenen çıktı / eşik (ör. "exit 0", "HARD=0",
  "0 çözülmemiş crossref").
- **Tür:** `OTOMATIK` | `MANUEL` | `YARI` (araç + gözle teyit).
- **Kanıt konumu:** çıktının/kanıtın nereye yazıldığı (rapor, sertifika, log).
- **Kapı/Kaynak:** hangi kapıya (0–5) ve hangi kanonik kural dosyasına bağlı.

### R4 — Doğrulama script'i
- Yeni dosya: `scripts/util/tez_checklist_verify.py` (mevcut util Python
  desenine uygun: `PYTHONDONTWRITEBYTECODE`, salt-okuma, satır-düzeyi veri
  sızdırmaz).
- Script, R2'deki **otomatikleştirilebilir** maddeleri sırayla koşar:
  mevcut araçları (`bib_hygiene.py`, `karma_ledger_check.py`,
  `claim_certification.py`, `csr_numeric_trace_audit.py`,
  `csr_causal_label_audit.py`, `tr_corpus_audit.py`) alt-süreç olarak çağırır;
  ek olarak render-crossref taraması, format ölçüm ve targets/renv durum
  kontrollerini kapsar (araç yoksa SKIP + neden).
- Her madde için satır: `MADDE-ID  DURUM(PASS/FAIL/SKIP/MANUEL)  kısa kanıt`.
- Sonda özet: toplam/PASS/FAIL/SKIP/MANUEL sayacı + genel sonuç.
- `--section <kod>` ile tek eksen; `--chapter <dosya>` ile bölüm-düzeyi alt-küme;
  argümansız tam tez-düzeyi koşum.
- Hiçbir dosyayı değiştirmez. Exit: 0 = otomatik maddelerin tümü PASS/SKIP;
  1 = en az bir otomatik HARD FAIL.
- Marmara format ölçümü (PDF varsa) ve render taraması ağır olabilir; bunlar
  `--fast` ile atlanabilir (SKIP olarak işaretlenir).

### R5 — Mevcut checklistleri genişletme
- `format-kontrol-listesi.md`, `kanit-ve-gizlilik-kontrol-listesi.md` ve
  `render-bagimliliklari.md` içinde master checklist'e ve script'e **çapraz
  bağlantı** eklenir (hangi madde script'in hangi kontrolüne karşılık geliyor).
- Yeni eksenler (pipeline tazeliği, PDF format ölçümü) uygun mevcut dosyaya
  veya master belgeye eklenir; içerik tekrarı yerine referans tercih edilir.
- `04_kalite-kontrol/README.md`, yeni master checklist ve script'i akış
  içinde konumlandıracak biçimde güncellenir.

### R6 — Araç-madde eşleme tablosu
- Master belgede, her mevcut aracın (`scripts/util/*.py`, slash komutlar)
  hangi checklist maddelerini kapsadığını gösteren bir **kapsama matrisi**
  bulunur. Böylece hangi maddenin otomatik, hangisinin manuel kaldığı ve
  otomasyon boşlukları görünür olur.

### R7 — Doğrulama (bu işin kendi kontrolü)
- `tez_checklist_verify.py` repo mevcut durumunda koşulur; hata vermeden
  (kod hatası anlamında) tamamlanır ve tutarlı bir rapor üretir.
- Script'in raporladığı otomatik maddeler, elle koşulan tekil araç sonuçlarıyla
  tutarlı olmalı (ör. `bib_hygiene` HARD sayısı script raporuyla aynı).
- Master checklist'teki her OTOMATIK madde, script'te karşılık gelen bir
  kontrole sahip (yetim madde yok); her script kontrolü belgede bir maddeye
  bağlı.

## Kabul Kriterleri

- [ ] `tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md` mevcut; Türkçe;
      bölüm-düzeyi (A) + tez-düzeyi (B) iki katman içeriyor.
- [ ] Belge R2'deki 8 eksenin tümünü madde madde kapsıyor.
- [ ] Her madde R3 şemasındaki alanları (ID, mekanizma, komut, PASS ölçütü,
      tür, kanıt konumu, kapı/kaynak) taşıyor.
- [ ] `scripts/util/tez_checklist_verify.py` mevcut; salt-okuma; argümansız
      tam koşum + `--section` + `--chapter` + `--fast` destekli.
- [ ] Script tüm otomatik araçları çağırıp birleşik PASS/FAIL/SKIP/MANUEL
      raporu ve özet exit kodu üretiyor; repo mevcut durumunda hatasız koşuyor.
- [ ] Script çıktısı tekil araç sonuçlarıyla tutarlı (ör. bib_hygiene HARD
      sayısı eşleşiyor).
- [ ] Master belgede araç→madde kapsama matrisi var; her OTOMATIK madde script
      kontrolüyle, her script kontrolü bir maddeyle eşleşiyor (yetim yok).
- [ ] Mevcut checklistler + `04_kalite-kontrol/README.md` yeni belge/script'e
      çapraz-bağlı; içerik tekrarı yerine referans kullanılmış.
- [ ] Değişiklikler tek toplu commit (Türkçe mesaj + `Co-authored-by: Ona
      <no-reply@ona.com>`); yalnız QC katmanı dosyaları + yeni script.

## Uygulama Adımları (sıralı)

1. **Envanter sabitleme:** `scripts/util/` araçlarının her birinin gerçek
   arayüzünü (argümanlar, exit kodları, çıktı biçimi) ve slash komutların
   koştuğu komutları çıkar. Her aracın hangi eksen(ler)i kapsadığını netleştir
   (R6 matrisinin ham verisi).
2. **Eksen → madde ayrıştırması:** R2'deki 8 ekseni somut, atomik maddelere
   böl; her maddeye R3 şemasını doldur (ID, mekanizma, komut, PASS eşiği, tür,
   kanıt konumu, kapı/kaynak). Otomatik vs manuel ayrımını burada sabitle.
3. **Master checklist yaz (R1):** `tez-kontrol-checklisti.md` oluştur; (A)
   bölüm-düzeyi + (B) tez-düzeyi katmanlar; her eksen için madde tablosu +
   R6 kapsama matrisi + kanonik otorite referansları.
4. **Doğrulama script'i yaz (R4):** `tez_checklist_verify.py` — mevcut araçları
   alt-süreç olarak çağıran orkestratör; render-crossref taraması, targets/renv
   durumu, (opsiyonel) PDF format ölçümü; `--section/--chapter/--fast`; birleşik
   rapor + özet exit kodu; salt-okuma.
5. **Script–belge senkronu:** Her OTOMATIK maddenin script'te karşılığı, her
   script kontrolünün belgede maddesi olduğunu doğrula (yetim madde/kontrol yok).
6. **Mevcut checklistleri genişlet (R5):** `format-kontrol-listesi.md`,
   `kanit-ve-gizlilik-kontrol-listesi.md`, `render-bagimliliklari.md` ve
   `README.md`'ye çapraz-bağlantı + yeni eksen referansları ekle.
7. **Script'i koş ve doğrula (R7):** `tez_checklist_verify.py` repo mevcut
   durumunda koştur; raporun tutarlı ve hatasız üretildiğini, exit kodunun
   beklendiği gibi olduğunu, tekil araç sonuçlarıyla eşleştiğini teyit et.
8. **Teslim:** QC dosyaları + yeni script'i tek toplu commit ile ver (Türkçe
   mesaj + co-author).

## Riskler / Notlar

- **Araç exit-kod tutarsızlığı:** Bazı araçlar (ör. `bib_hygiene`) mevcut repo
  durumunda HARD fail (exit 1) döndürüyor olabilir. Script bunu doğru şekilde
  FAIL raporlar; bu, script'in bozuk olduğu anlamına gelmez — checklist gerçek
  durumu yansıtır. Bu maddeler raporda net ayrılır.
- **Ağır kontroller:** Tam `tar_make()` ve PDF render dakikalar sürebilir;
  `--fast` ile bunlar SKIP edilebilir, böylece hızlı ön-kontrol mümkün olur.
- **Manuel maddeler kaçınılmaz:** Retorik akış, thick-description, jüri/kişisel
  alan doğruluğu gibi maddeler otomatikleştirilemez; belge bunları açıkça
  MANUEL işaretler ve script FAIL saymaz.
- **PII sınırı:** Script salt-okuma ve satır-düzeyi veri sızdırmaz; `data/raw|
  identified|cleaned|backup` içeriğini okumaz, yalnız varlık/gitignore durumunu
  denetler.
- **Kapsam disiplini:** Checklist tespit eder; bulunan içerik eksiklerini
  düzeltmek ayrı iştir (bu iş yalnız kontrol altyapısını kurar).
