# GEREÇ ve YÖNTEM — Kapsamlı Bölüm Talimatnamesi

> **Kanonik kural otoritesi:** Bölüm içerik kuralı →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §3.5
> (tekrarlanabilirlik düzeyi, alt başlık, etik kurul tarih-sayı); karma
> bölüm-kaynak-kapı haritası → §6; nitel biçim → §7; istatistik yazım (biçim) →
> §8 + §1.4; başlık/atıf → §1.3/§1.8. Bu talimatname kural **tanımlamaz**;
> yürütme stratejisini verir. Klasör haritası: `03_bolum-hazirlik/README.md`.

## 1. Bölüm İşlevi

`GEREÇ ve YÖNTEM`, çalışmanın **bağımsız bir ekip tarafından tekrarlanabilmesi**
için gereken tüm tasarım, örneklem, ölçüm ve analiz kararlarını verir. Bu tez
**karma yöntem** olduğu için bölüm iki kolu (nicel + nitel) ayrı ama **tek karma
tasarım çatısı** altında sunar. Bu bölümde **hiçbir bulgu, sonuç veya yorum**
yer almaz; yalnız *ne yapıldığı* anlatılır. Bulgular → `04_bulgular.md`; yorum →
`05_tartisma-ve-sonuc.md`.

## 2. Yazım Sınırları (ihlal edilemez)

- Satır düzeyi veri, aile-düzeyi demografi, ham nitel transcript, PII, imzalı
  onam metni **yazıya taşınmaz** (`talimatname-claude-code.md` §2). Örneklem
  aggregate düzeyde anlatılır.
- Kanonik analiz bazına yalnız **varlık/hash kontratı** olarak atıf yapılır
  (`data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock`); satır içeriği
  gösterilmez.
- Görünür tez metninde araç/MCP/connector/DSL/telemetri **yer almaz**; bunlar
  yalnız hazırlık ve sertifika kayıtlarında tutulur.
- Etik kurul **tarih ve sayı** bu bölümde verilir; onay belgesi **Ekler**dedir
  (marmara §3.5, §3.10). Tarih/sayı, `06_kritik-kaynaklar` etik kaynağı ile
  bire bir tutarlı olmalıdır — uydurulmaz.
- Faz II/post-hoc yöntemler burada **birincil analiz gibi** yazılmaz; keşifsel
  olduğu belirtilir.

## 3. Alt Başlık Omurgası

Bölüm alt başlıklarla yapılandırılır (marmara §3.5 alt başlığa izin verir). Her
alt başlık bir konu cümlesiyle açılır, sonrakine geçişle bağlanır.

### 3A. Nicel kol alt başlıkları

| Alt başlık | Yazım işlevi | Repo kanıt kaynağı | Kaçınılacak taşma |
|---|---|---|---|
| Araştırma tasarımı | Olgu-kontrol, çok-bilgi-kaynaklı, aile düzeyinde nesteli karma tasarım; nicel-nitel zamanlama ve öncelik. | `docs/CLINICAL-STUDY-REPORT-FINAL.md`, `docs/analiz_planlari/03-sap-ana-plan.md` | Sonuç yönü/etki iması. |
| Çalışmanın yeri ve tarihi | Veri toplama yeri, dönemi (marmara §3.5 zorunlu alanı). | Protokol | — |
| Evren ve örneklem | 241 aile × 2 katılımcı = 482 satır (DM indeks=120, kontrol=121); dahil/dışlama; güç/örneklem gerekçesi. | `docs/protokol/`, `_targets.R` | Aile-düzeyi demografi satırı. |
| Örnekleme yöntemi | Nasıl seçildiği, eşleştirme/karşılaştırma mantığı. | Protokol | — |
| Değişkenler ve tanımları | Faktör + sürekli değişkenler, kanonik isimler ve ölçüm biçimi. | `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` | Ham değer örneği. |
| Veri toplama araçları | EMBU-P/C (29 madde, 4'lü Likert), Beck (21 madde), KİA/SRQ, demografik-tıbbi form; kim doldurdu, nasıl. | `docs/protokol/KANONIK_*` ölçek dosyaları | Ölçek maddelerinin tam dökümü (telif). |
| Veri yönetimi ve kanonik baz | Hash-kilitli kanonik CSV, `validate_and_load()`, `targets` orkestrasyonu; tekrarlanabilirlik altyapısı (renv). | `_targets.R`, `R/01_io.R`, `.lock` | Satır içeriği. |
| İstatistiksel analiz | Her hipotez için yöntem (aşağıda §4). Anlamlılık, çoklu karşılaştırma stratejisi, yazılım/paket. | `docs/analiz_planlari/`, `tests/` | Bulgu/etki büyüklüğü değeri. |
| Eksik veri | DM-spesifik zamanlama değişkenleri için tasarım sınırı, FIML/MI (m, maxit) ve NMAR duyarlılığı çerçevesi. | `docs/analiz_planlari/`, `R/` | Sonuç. |
| Nedensel çıkarım sınırı | DAG-temelli kovaryat seti, propensity/IPTW, sensemakr — *tasarım* olarak; nedensellik iddiası kurulmaz. | SAP | Nedensel sonuç. |
| Etik onay | Etik kurul tarih + sayı; üç katmanlı onam/assent; KVKK veri yönetim planı özeti. | Etik kaynak + `06_kritik-kaynaklar` | Katılımcı kimliği. |

### 3B. Nitel kol alt başlıkları

| Alt başlık | Yazım işlevi | Kaynak | Kaçınılacak taşma |
|---|---|---|---|
| Nitel desen ve paradigma | Refleksif Tematik Analiz (Braun-Clarke); konstrüktivist epistemoloji + kritik realist ontoloji; RTA seçim gerekçesi (IPA/GT değil). | Kanonik nitel rapor + nitel kol methodology pack | — |
| Katılımcı yapısı ve bilgi gücü | 7 aile × 3 = 21 görüşme; triad (anne + T1DM'li çocuk + sağlıklı kardeş); **information power (Malterud)** — "saturasyon" terimi kullanılmaz. | Kanonik nitel rapor | Aile kodu/kimlik detayı. |
| Veri toplama | Yarı-yapılandırılmış görüşme + çocuk-uyumlu protokol; ayrı görüşme (dyadic conjoint değil); alan notu. | Nitel methodology pack | Ham transcript. |
| Analiz süreci | RTA 6 faz (tanışıklık → kod → tema üretimi → gözden geçirme → tanımlama → yazım); codebook v2 (23 kod × tema); IRR tartışması (Gwet AC1/Krippendorff α opsiyonel, uzlaşma süreci dokümante). | Kanonik nitel rapor, audit trail | Ham kod/aile eşlemesi. |
| Raporlama uyumu | COREQ (32), SRQR (21), JARS-Qual — hangisi nasıl karşılandı. | COREQ tamamlanmış dosya | — |
| Refleksivite ve audit trail | Positionality (OM/BA), refleksif günlük, karar audit trail; süreç olarak refleksivite. | positionality, audit trail | — |
| AI/LLM kullanım beyanı | LLM'in yalnız pilot/denetim katmanı olduğu, birincil analizin insan olduğu; prompt zinciri arşivi. | LLM beyanı dosyası | — |

## 4. Nicel istatistiksel analiz — hipotez bazlı yazım

Her hipotez için yöntem *tasarım düzeyinde* yazılır; **sonuç verilmez**. Yöntem
detayı ve kanonik isimler için `docs/analiz_planlari/` ve `t1dm-tez-rehberi`
skill referansları esastır (bu talimatname yöntem *seçimini* tekrar tanımlamaz).

- **H1** çocuk algısı (EMBU-C) → multilevel + IRT GRM + Bayesian preflight.
- **H2** kardeş ilişkisi (KİA) → APIM + distinguishable dyad CFA.
- **H3** anne öz-rapor (EMBU-P) → ANCOVA + IPTW duyarlılığı.
- **H4** Beck → EMBU-P latent SEM → WLSMV ordinal + multigroup invariance.
- **H5** diadik tutarlılık (anne ↔ çocuk uyumu) → ICC + Bland-Altman + RSA +
  Common Fate + k-coefficient. **Tezin birincil yenilik katkısıdır**; yöntem
  burada, "neden/nasıl" nitel açıklaması karma yorumda (Tartışma).
- Aile-içi bağımlılık nedeniyle her primer model **multilevel veya aile-clustered
  SE** içerir; bu tasarım gerekçesi (ICC) açık yazılır.

## 5. Nitel yöntem — yazım disiplini (marmara §7 + nitel çerçeve)

- Nitel bölüm nicel dilinden bağımsız yazılır: RTA "anlamlandırma eylemi"dir;
  IRR pozitivist zorunluluk gibi sunulmaz (jüri isterse uzlaşma stratejisi
  dokümante edilir). Detay: `05_entegrasyon/nitel-cikti-cercevesi.md`.
- **Tez = 4 makro tema** (journal = 6 tema — karıştırma). Bu bölüm yalnız
  *yöntemi* verir; temaların içeriği `04_bulgular.md`'dedir.
- Triadik tasarımda anne / T1DM'li çocuk / sağlıklı kardeş **ayrı bilgi
  kaynağı** olarak konumlanır; informant farkı "hata" değil rol/bağlam farkıdır.

## 6. Karma yöntem entegrasyonu

- Tasarım tipi açıkça adlandırılır (ör. yakınsak/açıklayıcı-sıralı karma);
  nicel-nitel **öncelik ve zamanlama** belirtilir. GRAMMS/MMAT raporlama
  çerçevesine atıf yapılır.
- Joint display'in **yöntemi** burada tanımlanır (alanlar → `05_entegrasyon/
  nitel-nicel-joint-display-plan.md`); joint display bir *doğrulama* aracı değil,
  yan yana koyma + kanıt türü etiketleme aracıdır.
- H5 dyadic concordance karma yeniliğin çekirdeğidir: nicel uyum *hangi
  boyutlarda*, nitel kol *neden/nasıl* sorusunu yanıtlar (bu ayrım yazılır).

## 7. Etik ve açık bilim

- Etik kurul **tarih + sayı** (Ekler'de belge); üç katmanlı onam: (1) anne kendi
  katılımı, (2) anne çocuk için ebeveyn rızası, (3) çocuk **assent** (gelişimsel
  uygunluk). KVKK özel nitelikli sağlık + çocuk verisi yönetimi özetlenir.
- OSF ön-kayıtları: `osf.io/pytfe` (H1–H5 confirmatory), `osf.io/d524q`
  (psikometrik validation); nitel ön-kayıt stratejisi. Ön-kayıttan sapma varsa
  sapma tablosuna (`docs/analiz_planlari/` altında; sapma oluştuğunda üretilir/
  güncellenir) işlenir ve confirmatory ↔ keşifsel ayrımı korunur (HARKing yasağı).

## 8. Anti-pattern'ler (bu bölümde yapma)

- Yöntem içine bulgu/etki büyüklüğü sızdırmak.
- Ham veri, ölçek maddesi tam dökümü, transcript veya aile demografi satırı.
- Post-hoc/Faz II'yi birincil analiz gibi yazmak (`[KEŞİFSEL]` etiketi düşer).
- Nitel yöntemi "küçük-n nicel" gibi sunmak; "saturasyon" demek.
- Etik kurul tarih/sayısını yaklaşık/uydurma yazmak.
- Araç/MCP/connector jargonunu görünür metne koymak.

## 9. Kanıt eşlemesi (repo)

| Tez bileşeni | Repo kaynağı | Kullanım sınırı |
|---|---|---|
| Tasarım/örneklem/analiz | `docs/CLINICAL-STUDY-REPORT-FINAL.md`, `docs/analiz_planlari/03-sap-ana-plan.md`, `04-sap-faz2-posthoc.md` | Aggregate/tasarım; sonuç yok. |
| Değişken sözleşmesi | `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` | Tanım; ham değer yok. |
| Ölçekler | `docs/protokol/KANONIK_*` | Ne ölçtüğü; madde dökümü yok. |
| Pipeline/tekrarlanabilirlik | `_targets.R`, `R/01_io.R`, `tests/` | Altyapı; çıktı değeri yok. |
| Nitel yöntem | `niteliksel/qualitative_canonical_results_report.md` + nitel kol methodology pack | De-identified; ham veri yok. |
| Kritik kaynak/etik | `06_kritik-kaynaklar/kritik-dosya-manifesti.tsv` | Erişim/doğrulama kuralına uygun seçim. |

## 10. Kapanış kapıları

- [ ] Tekrarlanabilirlik düzeyi sağlandı; bağımsız ekip çalışmayı kurabilir.
- [ ] Satır düzeyi veri/transcript/PII yazıya taşınmadı.
- [ ] Etik kurul tarih/sayı Ekler ile bire bir tutarlı.
- [ ] Nicel + nitel yöntem ayrı ama karma tasarım altında bağlı.
- [ ] Faz II/post-hoc `[KEŞİFSEL]` olarak ayrıldı; HARKing yok.
- [ ] Sayısal biçim: ondalık virgül, `p` yazımı (marmara §8/§1.4).
- [ ] Format §12 checklist + `sci-audit` axis G/A–F blocker'sız.
- [ ] Referanslı kısımda iki-kol AI-reliability (`talimatname` §6) + ledger `cite-ok`.
- [ ] Kapı 0–5 sertifikasyonu (`04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`) + açık onay.
