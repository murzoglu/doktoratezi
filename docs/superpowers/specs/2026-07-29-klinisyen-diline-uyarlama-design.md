# Tasarım Belgesi — `klinisyen-diline-uyarlama` (skill + command)

**Tarih:** 2026-07-29
**Durum:** Onaylandı (brainstorming tasarım kapısı) — inşa writing-skills TDD ile.
**Sahip:** Nicel tez kolu, T1DM & Ebeveynlik Tutumu.

---

## 1. Amaç (telos)

Sunulan pasajı/bölümü, **Sosyal Pediatri klinisyen jürisinin** ilk okuyuşta anlayacağı
**register ve kurguya** uyarlayan otör-düzeyi yeniden-üsluplama kapısı. Hedef kitle:
çocuk sağlığı ve hastalıkları / sosyal pediatri öğretim üyeleri — **klinisyen kökenli;
psikometri, davranış bilimleri ve alana özgü ileri istatistiksel metodolojilerde derin
altyapısı yok.** Mevcut anlatım bu grup için karmaşık ve kafa karıştırıcı.

Yetkinlik: pasajı **sade, çok iyi anlaşılır, izah edici, akıcı**, **sebep-sonuç
ilişkilerini net kuran**, az-altyapılı okura dahi mesaj veren bir dile **reformüle ederek
yazar** — ve bunu yaparken tez kapsamındaki **tüm hesaplama, sayı, bulgu, atıf ve kanonik
hususu titizlikle korur.**

**Ayırt edici çizgi:** zenginleştirme değil **erişilebilirlik**; vektör aşağı
(sadeleştirme), yukarı (derinleştirme) değil.

## 2. Kapsam ve sınırlar

- **Girdi:** kullanıcının işaret ettiği pasaj/bölüm; argüman boşsa `ide_selection`.
- **Çıktı:** tez metninin fiilen revize edilmiş hali — **doğrudan yazılmaz**; öneri →
  denetim kapısı → açık onay → Edit.
- **Çalışma bölgesi:** herhangi bir bölümün **nesri**. Bulgular'da da çalışır, ama sayısal
  yoğunluk ve dondurulmuş sıra nedeniyle en sıkı güvence katmanıyla (§5, §6).
- **DOKUNULMAZ:** sayı/istatistik (g, β, SE, p, %GA, ICC, AUC, ω, CFI, RMSEA, BF, N,
  yüzde …), bulgu içeriği / yönü / anlamlılığı / büyüklüğü, `@tbl-*` · `@fig-*` · `[@key]`
  token'ları, `[KEŞİFSEL]`/`[POST-HOC]` etiketleri, çekince ve sınırlılık ifadeleri,
  yöntem beyanı.
- **EKLENMEZ (kaynakta yoksa):** etki-büyüklüğü etiketi ("küçük/orta/güçlü", "klinik
  açıdan anlamlı"), nedensellik dili, informant/aktör özgüllüğü. (Referans Bütünlük Şiarı
  + house kırmızı bayrakları.)
- **ATIF EKLEMEZ:** mevcut atıflar korunur; yeni literatür getirmez (o `anlatim-zenginligi`
  işidir). Bu yönüyle kardeşlerden daha basit.

## 3. Kardeş sınırı (çakışma önleme)

| Yetkinlik | Ne yapar | Metni düzenler mi | Vektör |
|---|---|---|---|
| `data-narrative` | Ayrı açıklama üretir | Hayır | Öğretme |
| `anlatim-zenginligi` | Nesri zenginleştirir + yeni atıflı literatür | Evet (kapı+onay) | Derinleştirme ↑ |
| **`klinisyen-diline-uyarlama`** | Tanımlı kitleye register uyarlar, atıf eklemez | Evet (kapı+onay) | **Sadeleştirme ↓** |
| `veri-gosterimi-zenginligi` | Figür/tablo/altyazı sunum katmanı | Evet (kapı+onay) | Sunum |

**Aynı bölgede eşgüdüm:** ikisi de istenirse sıra **önce zenginleştir (anlatim), sonra son
okunabilirlik geçişi olarak klinisyen-diline-uyarla.** SKILL.md'de Devir/scope-guard bloğu +
`tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md`'ye bir satır işaret.

## 4. Dosya mimarisi (data-narrative modeli)

```
.claude/skills/klinisyen-diline-uyarlama/
  SKILL.md                              # bağlayıcı metodoloji
  references/
    hedef-kitle-personasi.md           # klinisyen jüri: ne bilir / ne çevrilmeli (+klinik karşılık)
    yeniden-uslup-yontemi.md           # teknik + yerel yeniden sıralama kuralları + gerekçe şablonu
    kaynak-dogrulama.md                # yeniden yazmadan önce kaynak/token/numeric-trace doğrulama
    ornek-yeniden-uslup.md             # tek mükemmel öncesi/sonrası örnek (sayılar korunmuş)
.claude/commands/klinisyen-diline-uyarlama.md   # ince sarmalayıcı (otomatik bağlam + skill bağlayıcı)
tez-yazim/04_kalite-kontrol/klinisyen-diline-uyarlama-journal.md   # journal (şablonla)
```

## 5. Hedef-kitle personası (referansın çekirdeği)

`hedef-kitle-personasi.md`, klinisyen jürinin bilgi profilini iki sütuna oturtur:

- **Bilir (çeviri gerekmez, klinik zeminde konuş):** prevalans/insidans, ortalama±SS,
  p-değeri sezgisi, duyarlılık/özgüllük, OR/RR, güven aralığı sezgisi, tanı ölçütü mantığı.
- **Çevrilmeli (klinik karşılıkla + parantezde özgün ad):** başlangıç tohum listesi —
  SEM/CFA, Cronbach ω/α, RMSEA/CFI, IPTW/eğilim skoru, ICC/çok düzeyli model, Bayes
  faktörü/ROPE, LPA/LCA/bifaktör, IRT/GRM, ölçüm değişmezliği, APIM/diyadik uyum,
  multiverse, E-değeri, TOST/eşdeğerlik. Her satır: **klinik karşılık cümlesi** (ör.
  "eğilim skoruyla ağırlıklandırma ≈ gözlemsel veride 'sanki randomize etmiş gibi' grup
  dengeleme"). Tam tablo referans dosyasında; büyüklük eşikleri için `data-narrative`'in
  `buyukluk-esikleri.md`'sine köprü.

## 6. Yeniden üsluplama yöntemi (görünmez iskelet)

`yeniden-uslup-yontemi.md`:
1. **Klinik çerçeve önce** — pasajı klinisyenin bildiği zemine oturt.
2. **Açık sebep-sonuç** — "çünkü/dolayısıyla/bu nedenle" ile mekanizmayı görünür kıl.
3. **Jargon çevirisi** — her metodolojik terim ilk geçişte klinik karşılığı + parantezde
   özgün ad (personadan).
4. **Cümle bölme** — uzun/iç-içe cümleleri kısa, izlenebilir adımlara.
5. **Yerel yeniden sıralama** (Seçenek B) — gerektiğinde klinik-anlam → istatistik-dayanak
   sırası; §7 kapısına tabi.
6. **Ölçek uyumu** — basit pasaj hafif dokunuş; ağır metodoloji pasajı tam yeniden kurma.
7. **Detay kaybı yok** — çekince, alt-ölçek ayrımı, keşifsel etiket akıcılık uğruna asla
   atılmaz.

## 7. Yerel yeniden sıralama kapısı (Seçenek B'nin bedeli)

Bir öğe/bulgu-sırası yeniden dizildiğinde:
- (a) diff'te **↔ yeniden sıralama** işareti,
- (b) **klinik-pedagojik gerekçe** (şablon: "Klinisyen okur için X önce Y sonra daha
  anlaşılır çünkü …"),
- (c) **ayrı onay** — yeniden sıralamalar onay özetinde ayrı listelenir, kullanıcı açıkça
  onaylar.
- **Güvence:** bulgu *kümesi* değişmez; her bulgunun sayısı/yönü/anlamlılığı/atfı sabit;
  çapraz-referanslar (`@tbl`/`@fig`, "yukarıda/aşağıda", ileri-geri atıf, özet/summary)
  yeniden doğrulanır; **Bulgular'da** ise `csr_numeric_trace_audit` yeniden koşar
  (yüksek-risk eşsiz = 0). Yeniden sıralama **yereldir**; argüman mantığını veya atıf
  zincirini kıran sınırları aşamaz.

## 8. Denetim kapısı (house anayasası devralınır — uygulamadan ÖNCE)

| Kademe | Araç | Rol |
|---|---|---|
| **HARD** | `sci-audit:check-turkish --strictness certification` | Türkçe imla + ondalık virgül (nokta-`p` = blocker) |
| **HARD** | `sci-audit:verify-citations` · `check-stats` | Atıf bütünlüğü · istatistik tutarlılığı |
| **HARD** | `csr_numeric_trace_audit.py` (yalnız Bulgular yeniden sıralaması) | Yazılı bulgu ↔ CSV izi; yüksek-risk eşsiz = 0 |
| **SOFT-block** | `galileo_judge` (`text`, `section_type`, `evidence`=orijinal pasaj+artefakt) | **Bu skill'in ana kontrolü:** sadeleştirme iddiayı çarpıttı mı — faithfulness/groundedness/overclaim/hallucination |
| **advisory** | `galileo_coherence` · `galileo_reference_prose` | Akış/tekrar · atıf nesri |

Kademe anlamı `.claude/galileo.local.md`. HARD override yok; SOFT-block `certified-final`'ı
durdurur (insan-override'lı); advisory bloklamaz. Doğrudan yazmaz; öneri → kapı → onay →
Edit; denetim onaydan önce, ertelenmez. **KVKK:** gateway'e yalnız literatür/aggregate terim.

## 9. Journal tasarımı

`tez-yazim/04_kalite-kontrol/klinisyen-diline-uyarlama-journal.md`:
- **Kullanım ritüeli** (skill + command'a gömülü, zorunlu): *seans başı* → journal'ı oku,
  durum panosu + backlog'dan sıradakini seç; *seans sonu* → seans günlüğü gir, panoyu +
  backlog'u güncelle.
- **Durum panosu:** Bölüm/Pasaj | Durum (bekliyor / işlendi-onay bekliyor / uygulandı /
  certified) | Son dokunuş | Not.
- **Backlog (yapılacaklar):** öncelikli; her madde: pasaj + anlaşılırlık sorunu +
  **tez-geneli takip** (terim tutarlılığı, forward-ref).
- **Seans günlükleri (ters-kronolojik):** tarih · işlenen pasaj (dosya:satır) · ne yapıldı ·
  yeniden sıralama + gerekçe · kapı sonucu (+galileo skorları) · **tez-geneli bağlam
  etkileri** · açık takipler.

## 10. Tez-geneli bağlam etkisi davranışı

Her uyarlama bir **"tez-geneli bağlam etkisi" notu** üretir: terim tutarlılığı dalgalanması
(burada sadeleşen terim başka bölümlerde aynı karşılıkla anılmalı → backlog'a), çapraz-
referanslar, özet/summary/kısaltmalar yansıması, pasajın başka yerde tekrarı. Not hem onay
özetine hem journal girdisine girer. (Kullanıcının 3. gereksinimi.)

## 11. Yürütme sırası (sabit)

1. Bağlamı sabitle — dosya adı tahmin etme; `grep` ile gerçek dosya:satır; sayı/atıf/token
   envanteri; numeric-trace bağla. t1dm-tez-rehberi **Faz 0** kapsam + **Faz 0.5** tedbir.
2. **Journal'ı oku** (seans başı ritüeli).
3. Persona kalibrasyonu — pasajdaki çevrilecek metodolojik yükü işaretle.
4. Yeniden üsluplama (§6) + gerekirse yerel yeniden sıralama (§7).
5. Bağlam-etkisi notu (§10).
6. Denetle (§8) — uygulamadan ÖNCE.
7. Onaya sun: diff (eski→yeni), yeniden-sıralama + gerekçe listesi, kapı özeti, bağlam-etkisi
   notu, backlog güncellemesi.
8. Onay sonrası: Edit → (Bulgular reorder ise tam `tar_make` + numeric-trace) → **journal
   güncelle** (seans günlüğü + pano + backlog) → kapanışta `sci-audit:audit … --lang tr` +
   bölüm kapanıyorsa `/tez-dogrulama`.

## 12. İnşa planı (writing-skills TDD — Iron Law: önce başarısız test)

- **RED:** skill'siz bir subagent'a gerçek zor bir metodoloji pasajını (ör. IPTW ANCOVA veya
  WLSMV ordinal SEM cümlesi) "klinisyen jüriye sadeleştir" dedir; başarısızlığı **birebir**
  belgele. Beklenen başarısızlıklar: çekince düşürme, "anlamlı/güçlü/klinik anlamlı" etiketi
  ekleme, sayı/yön kayması, korelasyonu nedene çevirme, ya da hâlâ jargon-yüklü çıktı.
- **GREEN:** o spesifik başarısızlıklara karşı SKILL.md + references yaz; skill'li tekrar
  koş, uyum doğrula.
- **REFACTOR:** yeni rasyonalizasyonları yakala, rationalization tablosu + red-flags listesi
  ile kapat; bulletproof olana dek tekrar.
- **Form eşleşmesi (writing-skills "Match the Form to the Failure"):** *disiplin* parçası
  (DOKUNULMAZ kanıt, çekince düşürme yok) → yasak + rationalization tablosu + red-flags;
  *şekillendirme* parçası (klinisyen-net çıktının biçimi) → pozitif reçete. Şekillendirme
  ifadeleri no-guidance kontrolüne karşı mikro-test edilir (5+ tekrar, elle okunur).
- **Deployment:** command wrapper + journal şablonu; commit.

## 13. Kabul kriterleri

- Skill'siz baseline pasajda gözlenen ≥1 kanıt-mutasyonu/çekince-düşürme başarısızlığı,
  skill'li koşumda **tekrarlamaz.**
- Skill'li çıktı: tüm sayı/atıf/token birebir korunur (diff ile doğrulanır); klinisyen-net
  register; sebep-sonuç açık.
- HARD kapı temiz; SOFT-block eşik üstü; yeniden sıralama varsa gerekçe + ayrı onay + (Bulgular)
  numeric-trace temiz.
- Journal ritüeli skill + command'da zorunlu; bağlam-etkisi notu her uyarlamada üretilir.

## 14. Varsayımlar / açık noktalar

- Spec dosyası `docs/superpowers/specs/` altında (brainstorming varsayılanı); repo'da bu
  dizin yeni açılıyor.
- Persona çeviri tablosu **başlangıç tohumuyla** açılır; kullanım sırasında büyür (backlog'a
  eklenerek).
- Codex ikizi (`.codex/`) kapsam dışı — bu yetkinlik denetim politikası değil yazım
  yardımcısı; hook/politika değişikliği içermez.

## 15. Mimari revizyonu — Gemini-core (2026-07-29, kullanıcı onaylı)

Kullanıcı direktifi: yeniden-üsluplamanın **özünü Gemini 3.5 Flash** yapsın (portkey-galileo
gateway, `GALILEO_GEMINI_API_KEY`), **Claude çıktıyı değerlendirsin** ve amaca uygunsa sunsun.

- **Rol dağılımı:** Gemini = üretici (taslak); Claude = değerlendirici (DOKUNULMAZ + F1–F5 +
  klinisyen-anlaşılırlık) + orkestratör; bağımsız GPT-5.4 `galileo_judge` = ikinci-model kapı.
  **Üretici ≠ denetleyici** ilkesi korunur (Claude-dışı üretici bilinçli tercih).
- **Köprü:** `scripts/eval/gemini_reformulate.py` (stdlib-only, **gitignored**, `.env`
  sözleşmesi galileo_bridge ile paylaşık: `GALILEO_GATEWAY` + `GALILEO_GEMINI_API_KEY` +
  `GALILEO_GEMINI_MODEL`; sır basmaz/commit edilmez). `/chat/completions` OpenAI-uyumlu,
  çok-auth fallback + `--probe`.
- **Akış değişikliği:** §11 sırası → Adım 0 (Claude doğrula + DOKUNULMAZ envanter + journal +
  kalibrasyon) → Adım 1 (Gemini üret; erişilemezse bildir, sessiz Claude-fallback YOK) → Adım 2
  (Claude değerlendir: sayı/token diff + F1–F5; kabul/yeniden-yönlendir 2–3 tur/düzelt/reddet) →
  kapı → onay → Edit → journal.
- **Model seçimi:** üretici için Claude-dışı **Pro-sınıfı** önerilir (jüri-kalite; fidelity +
  Türkçe akıcılık); Flash hızlı varsayılan. Model `.env` tek satır — kod değişikliği yok;
  entegrasyon açılınca 2–3 model `galileo_judge` ile A/B ölçülür.
- **Açık bloker (2026-07-29):** virtual-key `gemini-3.5-flash`'a sabit; `@org-gcp-general-
  multius` entegrasyonu bu modele izin vermiyor (HTTP 412; istek-gövde modeli yok sayılıyor).
  Gateway/auth/köprü doğrulandı. Panoda model allowlist açılınca canlı üretim çalışır; skill +
  command + references + journal buna göre yazıldı (model-agnostik).
- **KVKK:** gateway'e yalnız manuskript pasajı + literatür terimi; ham/katılımcı/aile-düzeyi veri
  ASLA. Anahtar düz-metin sohbete girdi → kullanıcıya rotasyon önerildi.
