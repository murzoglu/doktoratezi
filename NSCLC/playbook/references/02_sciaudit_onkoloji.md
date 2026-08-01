# L3 — sci-audit: SR Adli Denetimi (NSCLC, PRISMA-merkezli)

> Kapsam: yalnız akciğer kanseri tedavi **sistematik derleme** manüskriptleri;
> yalnız `NSCLC/` alt-ağacı. Ana playbook:
> [`../NSCLC_PLAYBOOK.md`](../NSCLC_PLAYBOOK.md) §3.

sci-audit, **yedi-eksen adli denetim** disiplinini bir sistematik derlemeye uyarlar.
SR'de raporlama-kılavuzu ekseni (E) **PRISMA 2020 + RoB + GRADE** üçlüsü etrafında
merkezîleşir. Denetim, üç katmanın en üstündeki **HARD kapıdır**: `error`/`blocker`
teslimi durdurur.

---

## 0. Üç katman sınırı (çakışmaz)

| Katman | Rol | SR'de | Zorlama |
|--------|-----|-------|---------|
| **HARD (sci-audit)** | Deterministik; teslim engeli | PRISMA madde eksiği, akış tutarsızlığı, kaynaksız havuzlanmış etki, TR `p` yazımı | `scripts/run_hard_gate.py` (Python, LLM'siz) + eksen denetimi |
| **SOFT (galileo)** | Eşik-tabanlı, insan-override'lı | Groundedness/overclaim/HARKing | `galileo_*` tool'ları (bkz. aijudge referansı §1) |
| **advisory** | Critical friend | Anlatı, tekrar, üslup | judge advisory |

**HARD kapı asla LLM-judge'dan gelmez;** deterministik Python scriptleri +
kural-tabanlı eksen kontrolüyle üretilir.

---

## 1. Yedi eksen — SR uyarlaması

| Eksen | Ne denetler (SR) | Blocker örneği |
|-------|------------------|----------------|
| **A — Referans bütünlüğü** | Dahil edilen her çalışmanın DOI/PMID/NCT çözülür; künye eşleşir; **geri-çekilme** | Uydurma/geri-çekilmiş dahil çalışma |
| **B — Claim grounding** | Her tekil bulgu `extraction.csv`+lokatöre; her havuzlanmış etki `meta.csv`'ye bağlı; adversaryel refuter | "OS yararı" ama çıkarımda yalnız PFS |
| **C — İstatistik tutarlılığı** | Havuzlanmış HR↔GA↔p; **I²/τ² heterojenite**; forest ↔ SoF; alt-grup ↔ genel; olay/örneklem; **Türkçe ondalık virgül** | Forest'ta HR 0,72 ama özette 0,62 (sürüklenme) |
| **D — Halüsinasyon** | Uydurma çalışma/ajan/gen; imkânsız etki (HR≤0, I²>%100); NCT/ORCID checksum; `entity-verifier` | Var olmayan RCT dahil listesinde |
| **E — Raporlama kılavuzu** | **PRISMA 2020 (27 madde + akış)** + **RoB** (RoB2/ROBINS-I) + **GRADE** (SoF) | Akış diyagramı sayıları tutmuyor; RoB tablosu yok |
| **F — AI-şeffaflık** | ICMJE/COPE AI-kullanım beyanı; placeholder; LLM-giveaway | "[insert pooled HR]" kalıntısı |
| **G — Türkçe imla/yazım** | Ondalık virgül + `p` (**blocker**); onkoloji + SR kısaltmaları (PRISMA/RoB/GRADE/I²); nedensellik dili | `p = 0.03` (nokta) TR metinde blocker |

**No-fabrication invaryantı:** her eksen kapsamını beyan eder; çözülemeyen kaynak/
sayı `unverified`, asla "geçti".

---

## 2. Axis E — SR raporlama kılavuzu haritası

| Bileşen | Kılavuz | Kritik maddeler (NSCLC SR) |
|---------|---------|----------------------------|
| **Derlemenin kendisi** | **PRISMA 2020** (27 madde) | Protokol/kayıt, uygunluk, bilgi kaynakları, arama dizesi, seçim süreci, veri öğeleri, RoB yöntemi, etki ölçüsü, sentez yöntemi, kesinlik |
| **Akış** | **PRISMA akış diyagramı** | identified→screened→eligible→included sayıları iç-tutarlı |
| **Ağ meta-analizi (varsa)** | **PRISMA-NMA** | Ağ geometrisi, tutarlılık (inconsistency), sıralama |
| **Yanlılık riski** | **RoB 2** (RCT) / **ROBINS-I** (gözlemsel) / QUADAS-2 (tanısal) | Alan-alan yargı + gerekçe |
| **Kanıt kesinliği** | **GRADE** (SoF tablosu) | İndirme/artırma faktörleri + kesinlik düzeyi gerekçesi |
| **Protokol** | **PRISMA-P** | PROSPERO kayıt ID mevcut mu; kayıt sonrası her sapma tarih+gerekçe ile raporlandı mı (kayıt tarihine karşı) |

`guideline-mapper` her PRISMA maddesini **present / missing / partial** + alıntı ile
işaretler.

---

## 3. Adım adım tam denetim protokolü (atlanmaz)

0. **Deterministik ön-kapı (HARD, LLM'siz):** `scripts/run_hard_gate.py` koşulur —
   PRISMA-akış aritmetiği (`prisma_flow_check`), çıkarım yön-mantığı
   (`extraction_direction_check`), kaynak-tekilliği (`source_singularity_check`),
   Türkçe `p` imlası (`turkish_p_check`). Herhangi bulgu = blocker; LLM eksenlerine
   geçilmez.
1. **Kapsam:** dosya `07_manuscript/<konu>.md`; tip = sistematik derleme → `--type prisma`.
2. **Axis A:** dahil çalışmaların künyesi çözülür; geri-çekilme kontrol. Uydurma → blocker.
3. **Axis B:** her tekil bulgu `04_extraction/<konu>_extraction.csv`+lokatöre; her
   havuzlanmış etki `06_synthesis/<konu>_meta.csv`'ye bağlanır; `claim-refuter`
   kaynağın desteğini test eder. RBŞ ihlali (cherry-pick) burada + galileo overclaim'de.
4. **Axis C:** havuzlanmış HR↔GA↔p; I²/τ²; forest↔SoF yeniden-ifade tutarlılığı;
   alt-grup↔genel; imkânsız değer. Türkçe ondalık virgül.
5. **Axis D:** aşırı-kesinlik dili; atıfsız çalışma/ajan; bozuk NCT/ORCID;
   `entity-verifier` ilaç/gen/histoloji doğrulaması.
6. **Axis E:** `guideline-mapper` → PRISMA 27 madde + akış + RoB + GRADE (§2).
7. **Axis F:** AI-kullanım beyanı; placeholder; LLM-giveaway.
8. **Axis G:** Türkçe imla; **İngilizce ondalık-nokta `p` blocker**; SR kısaltmaları.
   İngilizce özet ayrı `--lang en`.
9. **Birleştir:** `08_reports/<konu>_sci-audit.md`.
10. **Kabul:** `error`/`blocker` yok; `warning`/`major` düzeltilmiş/gerekçeli;
    harici araç kullanıldıysa AI-use log yazılmış.

---

## 4. SR-özel istatistik kontrol listesi (Axis C derinleştirme)

- **Havuzlama modeli:** rastgele vs sabit etki gerekçesi; küçük-çalışma etkisi.
- **Heterojenite:** I² ∈ [0,%100]; τ²; yüksek heterojenitede havuzlama uygunluğu
  sorgulanır (→ narratif/alt-grup).
- **Etki yönü:** havuzlanmış HR<1 koruyucu; GA 1'i içeriyorsa "anlamlı" denemez.
- **Yeniden-ifade:** havuzlanmış etki özet/forest/SoF'ta **aynı** (sürüklenme kapısı).
- **Yayın yanlılığı:** ≥10 çalışmada funnel/Egger; az çalışmada yorum sınırı.
- **Alt-grup/meta-regresyon:** önceden-planlı mı (protokol); post-hoc işaretli mi (G-HARKING).
- **GRADE tutarlılığı:** kesinlik düzeyi indirme faktörleriyle (RoB/tutarsızlık/
  dolaylılık/kesinsizlik/yayın-yanlılığı) gerekçeli mi.

---

## 5. Manüskript artefaktlarına besleme

| sci-audit bulgusu | Beslenen artefakt |
|-------------------|-------------------|
| Axis A referans düzeltmesi | `04_extraction/` + taslak atıf |
| Axis B kaynaksız etki | `06_synthesis/<konu>_meta.csv` / `extraction.csv` |
| Axis C istatistik/heterojenite | Taslak forest/SoF + metin (yeniden-ifade tutarlılığı) |
| Axis E eksik PRISMA madde | Taslak ilgili bölüm + `08_reports/` akış |
| Tüm eksenler | `08_reports/<konu>_sci-audit.md` → `<konu>_certificate.md` |
