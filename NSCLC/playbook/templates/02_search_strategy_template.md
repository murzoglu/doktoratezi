# Arama Stratejisi & Kaydı — <KONU> (NSCLC)

> Tekrarlanabilirlik zorunlu: her veritabanı için **tam dize + filtre + tarih +
> isabet sayısı**. G-REPRO kapısı bunu denetler.

## Arama kavram blokları (PICOTS'tan)
- **Popülasyon bloğu:** (ör. "non-small cell lung"[tiab] OR NSCLC OR "lung
  adenocarcinoma" … + MeSH)
- **Müdahale bloğu:** (ör. ajan adları + sınıf terimleri + RxNorm eşanlamlıları)
- **Sonuç/Tasarım bloğu:** (ör. survival, "progression-free" … / RCT filtresi)

## Veritabanı koşumları

| Veritabanı | Tam arama dizesi | Filtreler | Tarih | İsabet (n) |
|------------|------------------|-----------|-------|------------|
| PubMed/MEDLINE | | | | |
| Embase (EPMC) | | | | |
| Cochrane CENTRAL | | | | |
| ClinicalTrials.gov | | (durum/faz) | | |
| Kılavuz (NCCN/ESMO/ASCO) | | | | |

## Ek yöntemler
- İleri/geri atıf taraması (snowballing): (dahil edilen çalışmalar üzerinden)
- Gri literatür / konferans özetleri: (kaynak + tarih)

## Toplama
- Toplam ham kayıt (n): 
- Tekilleştirme sonrası (n): → `03_screening/`
- Ham dışa-aktarımlar `02_search/raw_exports/` (git-dışı); özet `<konu>_records.csv`.
