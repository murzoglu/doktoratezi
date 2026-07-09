# VERİ-BÜTÜNLÜK DENETİMİ — Kanonik Analiz Bazı

> ✅ **ÇÖZÜLDÜ (2026-07-08).** Bu denetimde saptanan tüm final-tutarsızlıkları (B1/B2/B8/F2, 11 aile)
> PI form-teyitli değerlerle **düzeltildi**; kanonik kilit **rev 2** olarak yenilendi (38 hücre,
> satır/kolon değişmedi); düzeltme sonrası tutarsızlık **0**; tam pipeline yeniden koşuldu.
> B5 (es_dogum) kurtarıldı (supplement, 240/241). Detay: `09-tutarsizlik-worklist.md` (UYGULANDI),
> `CORRECTIONS__pi_verified_ledger.csv`, sapma tablosu #3. **⚠️ §110 maruziyet: dışlama kalktı →
> n=115'ten n=120'ye; CSR §16.7 buna göre güncellenmeli (re-run çıktısından).**

**Tarih:** 2026-07-08 · **Denetçi kapsam:** `FINAL_REFERENCE__analysis_base_{family,long}.csv`
(family 241×288, long 482×203; kilit SHA-256 doğrulı) · **Yöntem:** salt-okunur agregat/mantık
sorguları (satır-düzeyi PII dökülmez); tüm sayılar bağımsız hesapla doğrulandı.
**Amaç:** Ham/kanonik veride mantıksal tutarsızlıkları ayıklamak, sınıflamak ve **şu ana dek
yapılan analizlere etkisini** kod-footprint'iyle tespit etmek.
**⚠️ Kilit ilkesi:** Kanonik `FINAL_REFERENCE__*` DEĞİŞMEZ. Bu rapor tutarsızlıkları *tespit ve
sınıflar*; "giderme" ya analitik mantık-maskesi (kilit dokunulmaz) ya da kontrollü kaynak-düzeltme +
yeniden-türetme + yeniden-kilit (kanonik-değiştiren, PI onaylı) olarak §5'te ayrıştırılır.

---

## 1. BULGU ENVANTERİ (sınıflı)

| # | Bulgu | n | Sınıf | Kök-neden (olası) |
|---|---|---|---|---|
| B1 | `dm_yili > cocuk_yas` (tanı doğumdan önce — imkansız) | **5 DM** | 2 SUBSTANTİF (+3,3 / +1,3 yıl) · 3 YUVARLAMA (≤0,7) | `dm_tani_tarihi` entegrasyonu (3 kayıt sonradan tamamlandı) |
| B2 | `cocuk_sayisi = 1` ama kardeş var + `sira > cocuk_sayisi` | **2** (aile 119, 174) | GENUINE HATA (tek kök) | `cocuk_sayisi` eksik-kayıt (≥2 olmalı) |
| B3 | İndeks `sirasi == kardeş sirasi` (aynı doğum sırası) | **7** | 4 İKİZ/aynı-yaş (MEŞRU) · **3 farklı-yaş (HATA)** | ikiz kodlaması vs veri-giriş default |
| B4 | Kardeş tanı-anı yaşı `< 0` | 1 | **MEŞRU KATEGORİ** (tanıdan sonra doğan kardeş) | hata değil; R/55 §111 ayrı kategori |
| B5 | `es_dogum_tarihi` **%100 boş** (241/241 NA); `es_yas` yok | 241 | PROVENANS-BOŞLUĞU | baba yaşı kanonik baza taşınmamış |

**Ham→final provenans farkları (kullanıcı raporu, denetim-dışı doğrulama gerektirir):** raw-final
tarih farkı 19 ailede; 3 `dm_tani_tarihi` entegrasyonla tamamlandı; 2 eski-yıl kaydı temizlendi;
HbA1c ham dosyada yok → klinik-kayıt entegrasyonuyla eklendi (→ B6/seçilim); 1 PII kolonu ham'da,
çıktıya alınmadı.

| B6 | HbA1c MNAR seçilim (klinik-temas göstergesiyle seçilmiş alt-örneklem) | 39/120 | GEÇERLİK-TEHDİDİ | ayrı: `07-...faz4` §134, Fisher OR=4,56 |

---

## 2. TEMİZ DOĞRULANAN YÜZEYLER *(savunma için — sorun YOK)*

- **Kimlik/yapı:** `aile_no` tekil (241); grup 120 DM / 121 Kontrol; long tam 2 satır/aile. ✓
- **Likert aralıkları:** EMBU-P/C ∈ [1,4]; Beck ∈ [0,3]; SRQ ∈ [1,5] — **aralık ihlali YOK.** ✓
- **HbA1c değer aralığı:** [5,8–15,1] — klinik olarak makul. ✓
- **Komorbidite tutarlılığı:** `anne_hastalik_kategori_sayisi == Σ(14 flag)` **tüm ailelerde**. ✓
- **Yaş makullüğü:** anne−çocuk yaş farkı hepsinde ≥15 (imkansız-genç-anne YOK); yaşlar makul
  aralıkta (çocuk 7–17, anne 27–52, kardeş 7–17). ✓
- **Yapısal eksiklik doğru:** Kontrol'de `dm_yili`/`hba1c` DOLU olan **yok** (0); DM'de `dm_yili`
  NA olan yok. Yapısal-missing tasarım gereği temiz. ✓

**Yorum:** Tutarsızlıklar **dar ve lokalize** (B1–B3 toplam ~9 aile-kayıt); ölçek verisi,
komorbidite matrisi ve yapısal-missing tümüyle temiz. Bu, veri-yönetiminin genelde sağlam,
sorunun yalnız **birkaç tarih/sayı/sıra girişinde** olduğunu gösterir.

---

## 3. ANALİTİK ETKİ — Kod-Footprint İzlemesi

### 3.1 Doğrulayıcı H1–H5: **ETKİLENMEDİ (bir istisnayla)**
H1–H5 çekirdek yordayıcıları `group_f`/`role_f`/EMBU/SRQ/Beck/SES/`age_gap`'tir. `dm_yili` (B1)
ve doğum-sırası (B3) **hiçbir confirmatory modele girmez** → H1–H5 estimand'ları güvende.
**Tek istisna (B2):** `cocuk_sayisi` H1/H3'te `cocuk_sayisi_z` **kovaryatı**dır; 2 ailede yanlış
(=1). Etki: 2/241 kovaryat kontaminasyonu → sonuç yönünü değiştirmez (kovaryat, estimand değil),
ama temizlik için maskelenmeli.

### 3.2 Keşifsel/DM-klinik: **kısmen etkilendi**
| Modül (CSR) | `dm_yili`/sıra kullanımı | Maske? | Etki |
|---|---|---|---|
| R/55 (§16.7 maruziyet) | `dm_yili/cocuk_yas` oranı | ✅ **MASKELİ** (dm_yili>cocuk_yas dışlanır, `n_dislanan` raporlanır; §110.1) | Korunmuş |
| R/27 (§12.5 DM alt-analiz) | `dm_yili_z` kovaryat | ❌ **MASKESİZ** | 5/120 kontaminasyon (biri negatif `tani_yasi`) |
| R/40 (§12.5.1/§16.7 HbA1c) | `dm_yili_z`, `tani_yasi_z` | ❌ **MASKESİZ** | 5/120 + HbA1c MNAR (B6) çift-tehdit |
| R/54 (§108 doğum sırası/sibship) | `sirasi`, `cocuk_sayisi` | ❌ maskesiz | B2 (2) + B3-hata (3) kontaminasyon |
| R/12/R/21/R/31/R/04 | `dm_yili` (NMAR/rapor/türetim) | — | düşük öncelik (kovaryat/taşıma) |

`R/01_io.R` yalnız **hash-doğrulaması** yapar (dosya bütünlüğü); **mantık-doğrulaması yoktur**
(`stopifnot(dm_yili<=cocuk_yas)` yok) → B1 `tani_yasi = cocuk_yas − dm_yili`'yi global olarak
**negatif** üretir ve maskesiz modüllere sızar.

### 3.3 HbA1c hattı: **çift-tehdit**
B1 (maskesiz `dm_yili`) + B6 (MNAR seçilim). CSR §12.5.1/§16.7 HbA1c bulguları **iki** düzeltme
gerektirir: mantık-maskesi + seçilim-uyarısı (bkz. `07-...faz4` §134).

---

## 4. ÖZET: Etkinin Ağırlığı
- **Tez ana iddiaları (H1–H5): güvende** — yalnız 2-aile `cocuk_sayisi` kovaryat teması, ihmal
  edilebilir.
- **Etkilenen: keşifsel DM-klinik + sibship + HbA1c** (zaten `[KEŞİFSEL·İKİNCİL]`, düşük güç).
- **Ölçek/psikometri/komorbidite/yapısal-missing: temiz.**
- **§125 (Faz IV) infizibl** — `es_dogum_tarihi` %100 boş (B5).

---

## 5. GİDERME SEÇENEKLERİ *(kilit-farkında; PI kararı)*

**Seçenek A — Belgeli mantık-maskesi / veri-kalite katmanı (ÖNERİLEN).**
Yeni saf fonksiyon `data_quality_flags()` (R/55 maskesinin genellenmişi): (i) B1 `dm_yili>cocuk_yas`
(5), (ii) B2 `cocuk_sayisi` tutarsız (2), (iii) B3 ikiz-olmayan aynı-sıra (3) bayrakları. R/27,
R/40, R/54 bu bayrakla dışlama/duyarlılık uygular; birim testi + `outputs/tables/data_quality_*.csv`.
**Kilit DEĞİŞMEZ.** Yalnız etkilenen keşifsel modüller yeniden koşar; H1–H5 yeniden-koşum GEREKMEZ.
Sapma tipi: **Tip 2** (analitik işleme). — *En orantılı; standart pratik (kilitli veri elle
düzeltilmez, maskelenir/belgelenir).*

**Seçenek B — Kaynak-düzeltme + yeniden-türetme + yeniden-kilit (AĞIR).**
~5–7 genuine hücreyi (B1'in +3,3/+1,3'ü; B2'nin 2 `cocuk_sayisi`'si; B3'ün 3 sırası) **ham
kaynakta** düzelt, yeniden türet, **yeni SHA ile yeniden kilitle**, **TÜM pipeline'ı (H1–H5 dahil)
yeniden koş**, CSR'ı yeniden denetle. Sapma tipi **Tip 3**, OSF amendment. — *Orantısız:
confirmatory'yi yalnız 2-aile kovaryat etkiler; pristine veri PI tercihiyse yapılır.*

**Seçenek C — Hibrit.** Şimdi maske (A) ile analizleri koru; genuine hücreleri bir sonraki
planlı veri-sürümü için `08-...denetimi` kayıt-defterinde biriktir; toplu re-lock ileride.

**B5 (baba yaşı) ve B6 (HbA1c seçilim) hiçbir maskeyle çözülmez** — B5 provenans-boşluğu (kabul
edilir sınır), B6 seçilim-uyarısı olarak raporlanır.

---

## 6. KARAR BEKLEYEN SORULAR
1. Giderme yolu: **A / B / C**?
2. B3 aynı-sıra 7 aile: 4 ikiz teyidi için demografi-kaynağına (ham) tek-seferlik bakış yapılsın mı,
   yoksa "yaş-farkı<1 → ikiz varsay" heuristiği yeterli mi?
3. CSR-düzeyi düzeltmeler (`07-...faz4` §1.8: §12.5 seçilim-uyarısı, §18.1 batch-confound, §15.5 AD
   yorumu, §18.4 MNAR) bu turda uygulansın mı, yoksa maske/karar sonrası mı?

---

## 7. KAYNAK FORENSİK VE KURTARMA *(ham dosya `Birleşik Veri - Doktora Tezi - NİHAİ.csv`, 482×157)*

**Yöntem:** Ham kaynak (yedeklendi: scratchpad) final ile `cocuk_no` üzerinden birleştirildi
(241/241 eşleşme); PII kolonu [3] `Çocuk Adı Soyadı` **hiç okunmadı**. Aritmetik doğrulandı:
kaynaktan yeniden hesaplanan `anne_yas` finalle **222/241 birebir** eşleşti (medyan mutlak fark 0
yıl); sapan **19 aile = ham→final tarih düzeltmeleri** (kullanıcı raporuyla tutarlı).

### 7.1 Her bulgunun kaynağı — kaynak-hatası mı, türetme-kaybı mı?

| # | Forensik sonuç | Düzeltilebilir mi? |
|---|---|---|
| **B1** (5) | **GENUINE KAYNAK HATASI** — kaynakta DM Tanı Tarihi, Çocuk Doğum Tarihi'nden ÖNCE: gün farkları **−6, −260, −501, −627, −1211** (cocuk_no 2025-1/2004-1/1003-1/1007-1/2000-1). Yuvarlama değil, tarih giriş hatası. | ❌ Hangi tarihin yanlış olduğu **orijinal formsuz bilinemez** → **uydurulamaz**; maske + PI form-teyidi. |
| **B2** (2) | **GENUINE KAYNAK HATASI** — aile 1003, 1219: kaynak `Çocuk Sayısı=1` ama **2 katılımcı satırı** var (≥2 çocuk kesin). | ⚠️ "1" kesin yanlış; gerçek toplam (2? 3?) belirsiz → değer uydurulamaz; maske + PI teyidi. |
| **B3** (3) | **GENUINE KAYNAK HATASI** — aile 403/904/1216: iki kardeşin `Katılımcı Çocuk Sırası` aynı (2,2 / 1,1 / 1,1) hâlbuki farklı yaşta. | ❌ Doğru sıra bilinemez (Çocuk No eki −3/−4 ipucu olabilir ama teyitsiz) → maske + PI teyidi. |
| **B4** (1) | MEŞRU (tanıdan sonra doğan kardeş). | — hata değil. |
| **B5** (241) | **TÜRETME KAYBI** — Eş Doğum Tarihi kaynakta **480/482 dolu**; final derivation düşürmüş. | ✅ **KURTARILDI** → §7.2. |

### 7.2 B5 kurtarma + yeni bulgu B7

`data/processed/SUPPLEMENT__es_yas_recovered.csv` **üretildi** (kilit dokunulmadı; yalnız
`aile_no, cocuk_no, es_yas, es_dogum_available, ebeveyn_yas_farki`; **isim/ham-tarih içermez**).
Kapsam: **es_yas 240/241** aile; ebeveyn yaş farkı medyan −3,6 yıl (baba tipik olarak daha yaşlı;
203/240 anne<baba — makul).

> **⚠️ B7 (yeni):** Kurtarılan `es_yas` aralığı **13–56,5** → **13 imkansız baba yaşı** → kaynak
> Eş Doğum Tarihi'nde ≥1 giriş hatası. `es_yas` kullanılmadan önce **plausibilite-maskesi**
> gerekir (ör. es_yas < 16 veya > ~70 dışla). Ayrıca 19 aile (§7 başı) ham↔final tarih-sapması
> taşır → o ailelerde es_yas *düzeltme-öncesi* tarihe dayanabilir.

**Sonuç:** Tek temiz düzeltme B5 kurtarmasıdır (supplement, tahmin yok, kilit dokunulmadı).
B1/B2/B3 **genuine kaynak hatalarıdır ve orijinal veri-toplama kaydı olmadan güvenle
düzeltilemez** — bilimsel bütünlük gereği değer uydurulmaz; C-hibrit maske + PI form-teyidi.
