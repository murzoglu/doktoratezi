# Evidentia Entegrasyon Çerçevesi

Sürüm: 1.0 · 2026-07-06 · Kapsam: Tez yazımında **tüm dış literatür / tam metin
/ citation / benchmark / prior** işlerinin Evidentia üzerinden yürütülmesi.

Bu belge Evidentia plugin'ini **`t1dm-tez-rehberi` skill'inin sağladığı çerçeve
dahilinde** yapılandırır. Amaç, ham MCP connector'larını tek tek çağırmak değil;
skill'in köprü protokolü + repo-router + kanıt kaskadı ile **tek entegre dış-
kanıt hattı** kurmaktır. Dış literatür işinde ham connector'a doğrudan gidilmez.

---

## 0. Otorite zinciri (hangi belge neyi belirler)

Bu dosya **dış-kanıt (literatür/citation/tam-metin) mimarisinin** tek kanonik
yeridir; klasör tek-otorite haritası: `01_mimari/README.md`.

| Katman | Belge | Ne belirler |
|---|---|---|
| Skill çerçevesi | `t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` | İç-veri ↔ dış-kanıt görev ayrımı, giriş noktaları, tez-artefaktı besleme haritası, prior-HARKing kuralı, uydurma-referans yasağı. **Birincil çerçeve.** |
| Repo-router | `.claude/evidentia.local.md` | Bu kurulumun **tek doğruluk kaynağı**: `known_connected` bağlı connector listesi + narratif-derin-lit modu + tam-metin kaskadı + proje-scoped enrichment modülü. **Repo-özel yapılandırma.** |
| Süreç talimatnamesi | `00_kaynak-kurallari/talimatname-claude-code.md` (Bölüm 4–5) | Araç kapıları, tam metin kaskadı, zorunlu referans kapısı sırası. |
| Referans ledgeri | `02_kanit-haritalari/referans-denetim-ledgeri.md` | Her künyenin durum makinesi (candidate → cite-ok). |
| Biçim | `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` (Bölüm 4) | Künyenin nihai AMA-11 biçimi. |

**Kural:** Evidentia, `t1dm-tez-rehberi` ana kapısını bypass etmez. Önce skill
kapsam/OSF/PII/artefakt kararı verir; sonra Evidentia dış-kanıt, bağlam yönetimi
ve tam-metin çıkarımı için çağrılır. Nitel kolda köprü ikizi:
`.claude/skills/niteliksel-arastirma-rehberi-t1dm/references/literatur-kanit-evidentia.md`.

---

## 1. Görev ayrımı — Evidentia ne zaman?

Her literatür-kokulu soruda önce ayrım yapılır:

- **İç-veri analizi** (kendi 482-satır verimiz, H1–H5, EMBU/Beck/KİA, targets) →
  Evidentia'ya gitmez; `t1dm-tez-rehberi` iç-veri kapsamında kalır.
- **Dış literatür kanıtı** (dünyadan gelen kanıt) → Evidentia kaskadına delege
  edilir. Kapsam:
  - Giriş / Tartışma literatürü,
  - benchmark doğrulama (Pinquart vb. etki büyüklüğü referansları),
  - Bayesian confirmatory prior'ın **literatür temeli** (yalnız ön-kayıt anında;
    Bölüm 6),
  - psikometrik karşılaştırma (tarihsel α/ω, faktör yapısı),
  - T1DM epidemiyoloji (insidans/prevalans arka plan),
  - `references.bib` doğrulama / citation audit,
  - KOL / hakem / jüri haritası,
  - kritik makaleden sayısal endpoint (tam metin),
  - Türkiye tez boşluğu (YÖK), okul/eğitim bağlamı (ERIC, koşullu).

---

## 2. Kapsam kapısı — psikososyal repo-router

Bu tez **gelişimsel/psikososyal** (ebeveynlik tutumu, depresyon, kardeş
ilişkisi); diyabet medikal çapadır. `evidentia.local.md` repo-router'ı önce
soru tipini belirler, sonra havuzu açar.

**Varsayılan aktif çekirdek** (bu Claude Code kurulumunda bağlı — kaynak
`.claude/evidentia.local.md` `known_connected`; maksimum derinlikte çalışır):
`pubmed-epmc`, `openalex`, `semantic-scholar`, `anamnesis`, `evidentia-kb`,
`annas-reader`, `openathens`, `yok-akademik`, `minerva-evidence`.
`paper-search`, `psyarxiv-osf`, `yoktez-mcp` bu kurulumda **bulunmaz** (bkz.
`literatur-kanit-evidentia.md` §1.1); işlevleri OpenAlex/EPMC `AFF:"Turkey"` +
Semantic Scholar ile karşılanır, karşılanamazsa `gap_log`'a "connector yok" yazılır.

**Koşullu katmanlar** (yalnız açık tetikleyici sinyalle kaskada eklenir; sinyal
yoksa çağrılmaz ve preflight gürültüsü sayılmaz): `clinical-trials`,
`yok-akademik` (KOL), `openfda`/ICD-11/FAERS, `pophive` (yalnız ABD),
`titck-cache`, `mevzuat`/`mevzuat-bilgisi`, terminoloji (`med-terminologies`/
`nlm-rxnorm`/`nih-clinicaltables`/`iuphar-gtopdb`), `eric-mcp`, `drugddx`.

Soruyu **psikososyal İngilizce terimlerle** çerçevele ("type 1 diabetes
parenting overprotection child adjustment"); molekül/ATC dili yalnız soru
gerçekten gerektiriyorsa.

---

## 3. Kanıt kaskadı (D0–D6) ve giriş noktaları

Repo `evidence_mode: maximum_depth_uncapped`, `default_cascade: D0-D6`. Ciddi
literatür görevlerinde skill köprüsündeki kaskad varsayılan çalışır:

geniş bibliyografik tarama → semantik/citation genişletme → metodolojik rerank
→ hedefli tam-metin çıkarımı → claim-level semantik hakemlik → tez artefaktına
entegrasyon.

**Giriş noktaları** (Claude Code yüzeyi — slash komut):

| Giriş | Ne zaman |
|---|---|
| `/evidentia "<soru>"` | Tek konu / benchmark / odaklı tarama |
| `/evidentia-synthesize "<konu>" [DOI'ler]` | Çok-belge derin sentez (graph-RAG) |
| `/evidentia-fulltext <DOI>` | Kritik makaleden sayısal endpoint |
| `/evidentia-kol "<alan>"` | Jüri / hakem / ortak-yazar / alan otoritesi |
| `evidence-synthesizer` (alt-ajan) | Ağır fan-out (Giriş'in tamamı) — bağlam ekonomisi |
| `academic-archival-distiller` (alt-ajan) | TR psikoloji/gelişim tezleri (YÖK), arşiv |

**Bağlam ekonomisi:** Geniş fan-out'ta ana bağlamı doldurmak yerine distiller
alt-ajanları kullan (`medical-distiller`, `academic-archival-distiller`,
`evidentia:evidence-synthesizer`). Uzun tam metinler `anamnesis`
`ingest_document` ile RAG substratına indekslenir; ham tam metin bağlama
dökülmez.

---

## 4. Tam metin kaskadı

Tam metin erişiminin **tek kanonik otoritesi**
`00_kaynak-kurallari/tam-metin-erisim-kaskadi.md`'dir (T0 preflight → T1
OpenAthens/Millet Kütüphanesi → T1.5 Minerva (Roche korpus) → T2 Anna's →
T3 OA/diğer → Zotero kapanışı →
ledger durumları → yasaklar). Burada tekrarlanmaz; Evidentia D4 aşaması o
kaskadı çalıştırır.

Özet: kurumsal (OpenAthens) → Minerva (Roche korpus) → Anna's → PMC/OA → istisna;
OA + kurumsal + Minerva + Anna's tüketilmeden `full-text-exception` yazılamaz;
credential/`.env` (Minerva `${GRAVITEE_*}` dahil) asla tool-
çağrısına yazılmaz (bkz. memory: Wiley → OpenAthens+Playwright); hiçbir katılımcı
verisi/transkript tam metin araçlarına gönderilmez.

---

## 5. Zorunlu referans kapısı (citation'dan önce)

`/referans-kapisi "<künye>"` sırası sabittir — kapı kapanmadan referans metne
girmez:

**bağlam → bibliyografik kimlik (DOI/PMID/PMCID/OpenAlex/YÖK) → tam metin
kanıtı → Zotero mutabakatı (item key + BibTeX key; ikisi farklıdır) →
claim/pasaj notu → ledger kaydı + iki-kol AI-reliability**.

- Ledger: `02_kanit-haritalari/referans-denetim-ledgeri.md`.
- Durumlar: `candidate → full-text-ok / full-text-exception → zotero-ok →
  reliability-ok → cite-ok`.
- Zotero'ya yazma/import **açık onay** ister; `.env ZOTERO_API_KEY` yazdırılmaz;
  Web API için `scripts/util/zotero_env_bridge.py`.
- **Manüskript adli denetimi:** `sci-audit` plugin **axis A** (referans
  bütünlüğü — DOI/PMID metadata + retraction) ve **axis B** (claim grounding —
  atfın kaynağı gerçekten destekleyip desteklemediği, yasal OA tam metinle)
  referans kapısını metin düzeyinde tamamlar. Uydurma/yanlış-atıf/geri-çekilmiş
  künye burada yakalanır.
- **Repo/veri invaryantı:** `doktoratezi-ai-audit` (bu repo) + `t1dm-qual-ai-audit`
  (nitel kol (niteliksel/)) — KVKK/ham veri/quote-parity; referans içeren her bölüm
  kapanışında birlikte koşulur. Bu katman `sci-audit` metin adli denetimiyle
  **çakışmaz** (sınır: `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`).

---

## 6. Açık bilim kuralları (üç bağlayıcı)

1. **KAPSAM KAPISI** — Evidentia önce repo-router'ı uygular; varsayılan aktif
   akademik/RAG/tam-metin çekirdeği derin, koşullu connector'lar yalnız sinyalle.
2. **PRIOR / HARKing TUZAĞI** — Confirmatory (H1–H4) prior'lar **veriyi görmeden,
   ön-kayıt anında** (OSF `pytfe`) sabitlenir. Evidentia ile **veriyi gördükten
   sonra** prior güçlendirmek HARKing'tir; sonradan getirilen kanıt yalnız
   `[KEŞİFSEL]` duyarlılık veya Tartışma yorumudur. Tartışma literatürü serbest.
3. **UYDURMA REFERANS YASAĞI** — `references.bib`'e giren her künye
   Evidentia-doğrulamalı gerçek **PMID/DOI/NCT/YÖK-ID**'ye iz sürer.
   Doğrulanamayan eklenmez ("VERİ BULUNAMADI"). Literatür iddiası hafızadan
   uydurulmaz.

Dönen kanıt **tedbir denetiminden** geçer (tek meta-analiz mutlak değildir; etki
büyüklüğü + %95 GA; yayın yanlılığı; popülasyon transferi; korelasyon ≠
nedensellik), sonra AMA-11'e çevrilip `references.bib` ve ilgili `.qmd`'ye işlenir.

---

## 7. Kanıt paketi (her dış-kanıt koşumunun kapanışı)

Her koşum tam izlenebilir `evidence_packet` ile kapanır:
`soru`, `preflight`, `router_decision`, `coverage_set`, `depth_decision`,
`kullanılan_connectorlar`, `source_ids` (PMID/DOI/NCT/YÖK-ID/OpenAlex-ID/
PsyArXiv-ID/OSF-registration-ID), `canonical_artifacts`, `candidate_sources`,
`fulltext_extracts`, `claim_ledger`, `semantic_adjudication`, `validation_gates`,
`tez_artefakti`, `bibtex_durumu`, `gap_log`.

Her harici Evidentia/MCP kullanımı, tez içeriğini etkilediyse oturum bitmeden
`./dmnitel log-ai-use … --external-api-used yes` (nitel kolda (niteliksel/)) veya
`/ai-kayit` ile LLM beyanına işlenir; `--data-type` daima "anonim/türetilmiş".

---

## 8. KVKK sınırı (bu çerçeveye de uygulanır)

Ham hasta/aile verisi, transkript, satır-düzeyi veri, demografi ve kimlikleyici
**hiçbir Evidentia connector'ına, RAG substratına (anamnesis/qdrant/evidentia-kb)
veya memory'ye** gönderilmez. Yalnız yayın metni (dış literatür) ve anonim/
türetilmiş karar bağlamı persist edilir. Nitel kol (niteliksel/) çıktılarından yalnız
de-identified tema/codebook/COREQ/audit-trail ve araştırmacı onaylı anonim
alıntılar karma sentezde kullanılır.
