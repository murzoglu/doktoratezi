# NSCLC Kapsam Beyanı (Konstitüsyonel)

> Bu belge `NSCLC/` alt-ağacının **değiştirilemez sınırlarını** tanımlar. Bu
> alt-ağaçta çalışan her ajan/insan, işe başlamadan önce bu beyanı okur ve
> sınırların hiçbirini ihlal etmez. Sınırlar, kök doktora tezi (T1DM &
> Ebeveynlik Tutumu) ile bu çalışmayı **tam olarak yalıtmak** için vardır.

---

## 1. Konu ve tür sınırı

- **Konu:** Yalnızca **akciğer kanseri tedavisi** (öncelik: küçük hücreli dışı
  akciğer kanseri — NSCLC). Başka hastalık/alan **kapsam dışıdır**.
- **Tür:** Bu bir **sistematik derleme (systematic review, SR) / kanıt sentezi**
  sürecidir — birincil klinik çalışma **değildir**.
- **Bağlam taşınmaz:** T1DM / EMBU / Beck / KİA / ebeveynlik tutumu bağlamı bu
  alt-ağaca **hiçbir biçimde taşınmaz**; kavram, veri, ölçek veya metin ödünç
  alınmaz.

## 2. Dizin sınırı

- Tüm çalışma **yalnızca `NSCLC/` alt-ağacında** yürütülür.
- Kök tez artefaktları **okunmaz ve değiştirilmez**:
  `../data/`, `../outputs/`, `../_targets.R`, `../_targets/`, `../chapters/`,
  `../R/`, `../scripts/`, `../references/`, `../thesis.qmd`, `../tez-yazim/`,
  `../niteliksel/` ve kök `*.lock` / veri-haritası dosyaları.
- SR hattının kanonik dizin haritası:

  | Dizin | Faz | İçerik |
  |-------|-----|--------|
  | `00_context/` | — | Kapsam beyanı (bu belge) |
  | `01_protocol/` | F1 | Önceden-kayıtlı protokol (PICOTS, dahil/hariç) |
  | `02_search/` | F2 | Arama logu + kayıtlar (records.csv) |
  | `03_screening/` | F3 | Tarama logu + PRISMA akış sayıları |
  | `04_extraction/` | F4 | Çıkarım tablosu; `fulltext/` git-dışı (telif) |
  | `05_appraisal/` | F5 | Yanlılık riski (RoB 2 / ROBINS-I / QUADAS-2) |
  | `06_synthesis/` | F6 | Kanıt sentezi (± meta) + GRADE |
  | `07_manuscript/` | F8 | Manüskript taslağı |
  | `08_reports/` | F7/F8 | sci-audit + galileo + sertifika |
  | `09_ai_use_log/` | — | Yapay zekâ kullanım kütüğü |
  | `playbook/` | — | İş rehberi + referanslar + şablonlar |

## 3. Süreç sınırı

- Süreç **PRISMA 2020 uyumlu sekiz fazdır** (F1 Protokol → F2 Arama → F3 Tarama
  → F4 Çıkarım → F5 RoB → F6 Sentez → F7 Denetim → F8 Rapor). Ayrıntı:
  [`../playbook/NSCLC_PLAYBOOK.md`](../playbook/NSCLC_PLAYBOOK.md).
- Hiçbir faz sessizce atlanmaz; atlanırsa gerekçe rapora yazılır.
- Dört-katman araç doktrini (evidentia · minerva · sci-audit · aijudge/galileo)
  SR fazlarına eşlenmiştir.

## 4. Veri, telif ve gizlilik sınırı

- **Ham/hasta-düzeyinde veri YOKTUR.** Bu bir kanıt sentezidir: yalnızca
  **yayınlanmış literatürden künye + çalışma-düzeyi çıkarılmış özet veri**
  (HR / OS / PFS / ORR + %95 GA + tasarım) izlenir.
- **IPD-meta-analizi kapsam dışıdır** (hasta-düzeyi veri gerektirir).
- **Telif:** dahil edilen çalışmaların tam metni `04_extraction/fulltext/`
  altında **git-dışıdır**; toptan verbatim çoğaltma yasaktır (hedefli çıkarım).
- Credential / secret dosyaları git-dışıdır (`.gitignore`).

## 5. Bütünlük sınırı (no-fabrication)

- **Uydurma yasak:** NCT/PMID/DOI, endpoint, HR, örneklem veya çalışma
  **uydurulamaz**. Çözülemeyen kaynak/sayı `unverified` olarak işaretlenir.
- **Kaynak-tekilliği:** her sayı üretilmiş artefakttan (`04_extraction/*.csv`,
  `06_synthesis/*_meta.csv`) okunur; metne gömülü literal taşınmaz.
- **Önceden-kayıt:** sentez/alt-grup kararları protokolde tanımlıdır; post-hoc
  kararlar açıkça işaretlenir (HARKing karşıtı).
- **Kapı doktrini:** HARD kapı **yalnız deterministik** sci-audit'ten gelir;
  LLM-judge (galileo) yalnızca SOFT-block / advisory üretir.
- **Türkçe biçim:** ondalık ayırıcı virgüldür; APA 7 + PRISMA 2020 uyumu.

## 6. Onay gerektiren durumlar

Aşağıdakiler **açık kullanıcı onayı olmadan yapılmaz**:

- Kapsamı akciğer kanseri dışına genişletmek.
- `NSCLC/` dışına (özellikle kök tez artefaktlarına) yazmak.
- Ham/hasta-düzeyi veri toplamak veya IPD-meta yürütmek.
- HARD kapıyı LLM-judge çıktısına dayandırmak.
- Commit / push / PR açmak.

---

*Bu beyan konstitüsyoneldir: playbook, referanslar, şablonlar ve tüm faz
çıktıları bu sınırlara tabidir. Çelişki halinde bu belge üstündür.*
