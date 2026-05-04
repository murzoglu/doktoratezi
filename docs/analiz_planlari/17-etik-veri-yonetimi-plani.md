# Etik ve Veri Yönetimi Planı

**Çalışma:** T1DM-EBEVEYN doktora tezi  
**Etik kurul:** Marmara Üniversitesi Tıp Fakültesi Klinik Araştırmalar Etik Kurulu, 06.01.2023, Protokol Kodu 09.2023.201  
**Kanonik veri kilidi:** `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` (2026-04-26)  
**OSF proje:** <https://osf.io/vqrt5/>  
**Son güncelleme:** 2026-04-27

## 1. Yönetim İlkesi

Bu planın amacı, çocuk katılımcı içeren hassas klinik-psikososyal bir tez veri setinde veri minimizasyonu, erişim kontrolü, kimlik gizliliği, reprodüktiblik ve açık bilim gerekliliklerini birlikte yürütmektir.

Ana karar: satır-düzeyi veri açık paylaşılmaz. Açık paket yalnızca analiz planı, kod, kanonik dokümantasyon, veri kilidi metadata'sı, aggregate raporlar ve controlled-access notlarını içerir.

## 2. Veri Sınıflandırması

| Düzey | Sınıf | İçerik | Depo/Git | OSF |
|---|---|---|---|---|
| L0 | Açık metadata | SAP, protokol özeti, kanonik form dokümantasyonu, analiz kodu, aggregate raporlar | Commit edilebilir | Yüklenebilir |
| L1 | De-identified analiz verisi | `FINAL_REFERENCE__analysis_base_family.csv`, `FINAL_REFERENCE__analysis_base_long.csv` | Commit edilmez; `data/processed/*` git dışı | Controlled access; public yüklenmez |
| L2 | Kaynak/ara veri | `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/` | Commit edilmez | Yüklenmez |
| L3 | Kimlik/credential | `.env`, servis hesabı JSON, token, anahtar, onamda kimlik bilgisi | Commit edilmez | Yüklenmez |

## 3. Erişim Matrisi

| Aktör | Erişim | Sınır |
|---|---|---|
| PI | L0-L4 | Ham ve kimlikli veri için tam sorumluluk |
| Tez danışmanı | L0-L2, gerekli olduğunda L3/L4 kontrollü | Paylaşım yalnız çalışma amacıyla |
| İstatistik/analiz desteği | L0-L1 | Row-level veri controlled-access; credential yok |
| TİK/jüri | L0 ve gerektiğinde L1 read-only | Kimlikli veri yok |
| Yayın okuyucuları | L0 aggregate | Satır-düzeyi veri yok |

## 4. Zorunlu Teknik Kontroller

Her analiz fazı öncesinde aşağıdaki komutlar çalıştırılır:

```bash
Rscript scripts/R/07_verify_reproducibility.R
Rscript tests/test_data_governance.R
Rscript scripts/R/08_ethics_data_governance_audit.R
```

`08_ethics_data_governance_audit.R` iki denetim yapar:

1. Kanonik CSV başlıklarında doğrudan tanımlayıcı kolon var mı?
2. Git tarafından görülebilen dosya yollarında ham veri, processed row-level veri, `.env`, credential veya benzeri kritik içerik var mı?

Denetim çıktısı `outputs/tables/ethics_data_governance_audit.csv` altında üretilir ve git dışıdır.

## 5. PII/PHI Kolon Politikası

**Kritik bulgu sayılan doğrudan tanımlayıcılar:**

- ad, soyad, isim
- telefon, e-posta
- TC kimlik, hasta no, protokol no, dosya no, MRN
- açık adres, sokak, mahalle, posta kodu

**Review bulgusu sayılan dolaylı tanımlayıcılar:**

- doğum tarihi
- tanı tarihi
- anket tarihi
- il/ilçe/semt gibi coğrafi alanlar

Kritik bulgu denetimi başarısız kılar. Review bulguları, analiz gerekliliği ve veri minimizasyonu açısından ayrıca gözden geçirilir.

## 6. OSF ve Açık Bilim Sınırı

OSF iki katmanlıdır:

- Layer 1 reflective registration: <https://osf.io/d524q/>
- Layer 2 secondary data preregistration: <https://osf.io/pytfe/>

OSF'e yüklenmeyenler:

- ham veri
- kimlikli veri
- temizlenmiş ara veri
- satır-düzeyi processed CSV
- credential ve `.env`

OSF'e yüklenebilenler:

- SAP
- analiz kodu
- kanonik form ve veri haritası dokümantasyonu
- veri kilidi metadata'sı
- aggregate/anonim raporlar
- controlled-access veri notu

## 7. Sapma ve Olay Yönetimi

Ön-kayıttan yöntemsel sapmalar `docs/analiz_planlari/02-sapma-tablosu.md` içinde izlenir.

Veri güvenliği olayı şüphesinde:

1. İlgili dosya veya paylaşım kanalı durdurulur.
2. Etkilenen veri sınıfı L0-L4 olarak belirlenir.
3. PI ve tez danışmanı aynı gün bilgilendirilir.
4. Gerekirse KAEK ve kurum veri koruma birimi için olay notu hazırlanır.
5. Kök neden ve düzeltici/önleyici faaliyet bu plana eklenir.

## 8. Commit Öncesi Kontrol Listesi

- `git status --short` içinde `data/raw/`, `data/cleaned/`, `data/identified/`, `data/backup/`, `data/processed/*.csv`, `.env`, `*.json`, `_targets/`, `outputs/` görünmüyor.
- `Rscript scripts/R/08_ethics_data_governance_audit.R` kritik bulgu vermiyor.
- OSF/public paketlerde satır-düzeyi veri yok.
- Sapma varsa deviation table güncel.
