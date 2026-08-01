# F2 Arama Logu — BP27 Türkiye atezolizumab (NSCLC) kanıt doğrulaması

**Tarih:** 2026-07-24 · **Mod:** hedefli kanıt-doğrulama (belgedeki `problem.md`
iddialarının bağımsız teyidi + en geniş kapsamda genişletme). **Kapsam:** yalnız
akciğer kanseri (NSCLC) tedavi kanıtı + Türkiye ruhsat/geri-ödeme/epidemiyoloji
bağlamı. Yalnız yayınlanmış literatür + resmî/otorite kaynak; hasta-düzeyi veri yok.

> **Not (SR ↔ bu koşum):** Bu, tam PRISMA F1–F8 sistematik derlemesi DEĞİL; bir
> ticari/pazar-erişim belgesinin (`problem.md`) iddialarını bağımsız doğrulayan
> **geniş-kapsam kanıt-doğrulama** koşumudur (F2 arama + F4 hedefli çıkarım'a
> denk). Formal SR için F1 PROSPERO protokolü + F3 tarama + F5 RoB + F6 GRADE +
> F7 tam HARD-gate/sci-audit/galileo ayrı adımlardır (bkz. playbook).

## Bağlanan connector'lar (bu koşum)

| Katman | Connector | Durum | Rol |
|--------|-----------|:-----:|-----|
| L1/L2 kanıt | pubmed-epmc (E-utilities, keyless) | ✅ canlı | birincil arama + tam-metin |
| L1 kanıt | openalex, semantic-scholar (keyless) | ✅ canlı | genişletme + çapraz |
| L5 bağlam epi | globocan (IARC GLOBOCAN 2022, keyless) | ✅ canlı | Türkiye akciğer kanseri yükü |
| L5 bağlam epi | who-gho (keyless) | ⚠️ boş | akciğer-özgü indikatör dönmedi |
| L5 bağlam ruhsat | titck-cache (keyless) | ✅ canlı | TECENTRIQ/IMFINZI kayıt + KÜB + geri-ödeme |
| L5 bağlam mevzuat | mevzuat-bilgisi (keyless) | ⚠️ kısmi | SGK SUT tam-metni indekslenmiyor |
| — | anamnesis/openathens/annas/yok-akademik | ❌ 401 | anahtar yok (bu oturum) |

## Yürütme mimarisi

7 bağımsız kanıt ekseni; 5'i paralel literatür alt-ajanına, 2'si (epidemiyoloji +
pazar matematiği) doğrudan koordinatöre. Her ajan: gerçek PMID/DOI zorunlu, uydurma
yasak, çözülemeyen `unverified`, her sayı lokatörlü.

## Eksen bazında arama + isabet

| Eksen | Konu | Ana sorgular / araçlar | Ana isabetler (PMID/DOI) |
|-------|------|------------------------|--------------------------|
| 1 | 1L IO tedavi süresi (DoT/rwToT/RMST) | pubmed+openalex: pembrolizumab/atezolizumab 1L NSCLC time-on-treatment, restricted mean | Velcheti 2022 (35205788); Liu/Burke 2021 (33911121); Velcheti/Burke 2022 (36755804); IMpower110 (32997907); KEYNOTE-024/189/407 5-yıl (33872070/36809080/36735893) |
| 2 | Kötü PS (ECOG 2/3) ICI | pubmed: ICI + ECOG 2/3/4 NSCLC outcomes/toxicity | Ahmed 2020 (32089478); Katsura 2019 (31258716); Meyers 2023 (37090101); PePS2 (32199466); CheckMate 171 (32028209)/153 (31121324); PICASO (40382877) |
| 3 | 2L atezolizumab (OAK/TAIL) | pubmed+EPMC tam-metin: atezolizumab previously-treated DoT/PFS/OS/tail | OAK (27979383); TAIL (33737339)+final (36450379); POPLAR (26970723) |
| 4 | Evre III KRT+durvalumab progresyon/wash-out | pubmed: PACIFIC/PACIFIC-R + durvalumab early recurrence 6-month | PACIFIC (28885881); Spigel 5-yıl (35108059); PACIFIC-R (36307040); Park 2025 (40386716); Aslan 2025 (40662350) |
| 5 | Türkiye ruhsat/SUT | titck-cache (TECENTRIQ/IMFINZI KÜB + geri-ödeme) + WebFetch KÜB PDF + mevzuat | TİTCK IMFINZI 500mg KÜB (onay 19/01/2026, kubkt::d7c6f4051efe); TECENTRIQ kayıt master::8699505763460 (GERİ ÖDEMELİ) |
| 6 | Türkiye epidemiyoloji | globocan gco_query (Türkiye=792, akciğer=15) + pubmed Cangır/STONE | GLOBOCAN 2022 Türkiye akciğer: ins. 41.032 / mort. 38.505 / 5-yıl prev. 54.335; Cangır 2022 (36192076); STONE (UHOD, MEDLINE-indeksli değil) |
| 7 | Pazar-payı matematiği + dinamik model | analitik (belgenin kendi sayıları); literatür değil | — (aritmetik + yöntem doğrulaması) |

## Erişilemeyen / sınır

- **who-gho:** akciğer-kanseri-özgü mortalite indikatörü sorgusu boş döndü →
  GLOBOCAN birincil epi kaynağı olarak kullanıldı (küresel yetkili).
- **SGK SUT birincil metni:** mevzuat-bilgisi tam-metin araması `atezolizumab` için
  0 isabet; SGK SUT tebliği bu araçlarda güvenilir indekslenmiyor → atezolizumab 2L
  geri-ödeme *koşul metni* medikaynak.com (üretici portalı, SUT'u yeniden ifade
  eden) üzerinden; durvalumab koşulları resmî TİTCK KÜB'ünden (birincil).
- **IMpower110 5,3 ay DoT:** NEJM tam-metni kapalı → hakemli ikincil kaynaktan
  (Velcheti 2022) kısmen doğrulandı.
- **STONE (UHOD):** MEDLINE/PMC-indeksli değil → PubMed/EPMC ile bağımsız
  doğrulanamadı; belgenin kendi kapsamlı çekinceleri geçerli.
