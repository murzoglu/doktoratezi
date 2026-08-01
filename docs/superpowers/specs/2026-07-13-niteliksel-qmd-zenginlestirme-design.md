# Spec — Kanonik Niteliksel QMD Tam Zenginleştirme

**Tarih:** 2026-07-13
**Hedef dosya:** `niteliksel/06_manuscript_outputs/niteliksel_kanonik_sonuclar.qmd` (kanonik kaynak)
**Yönetişim:** `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` (bağlayıcı);
niteliksel otör-yetkinlik: `.claude/skills/niteliksel-arastirma-rehberi-t1dm`
**Yürütme modu:** Ultracode — Workflow-güdümlü fan-out, adversarial doğrulama.

## Amaç

Kullanıcının 4 parçalı talebi:
1. Bilimsel doğruluk ve tutarlılık denetimi.
2. Tam-metin uyumu + referans eksiksizliği + format uyumu (belirle ve iyileştir).
3. Yeni literatür araştırması + **tam metinlerden çıkarılan detaylarla** bulgu/tartışma derinleştirme.
4. Uygulanan (niteliksel) yöntemleri **bilgi kutuları** biçiminde anlaşılır tarif edip ilgili
   kesitlere yerleştir.

## Karar geçmişi (brainstorming)

- Task 4 mimarisi: **niteliksel kolun kendi yöntemleri** (RTA/COREQ/trustworthiness/bilgi gücü/
  triadik/negatif vaka) callout bilgi kutuları olarak — katman içi, doktrinle uyumlu.
- Kanoniklik: QMD kendi callout'unda (satır 27-32) tek kanonik kaynak; `.md` mekanik kopya.
- Kapsam: önce "C (bounded, lit ertele)" seçildi; kullanıcı **override etti** → tam literatür +
  tam-metin zenginleştirme geri kapsamda.

## Değişmez sınırlar

- **KVKK:** connector'lara yalnız literatür terimi; ham/aile/transcript/quote_text asla.
- **No-fabrication:** çözülemeyen kaynak/iddia = `gap`; uydurma atıf/DOI/destek-pasajı yasak.
  Her `[@key]` DOI + tam-metin ile doğrulanır; `references.bib` + Zotero **9ZFDHMZA** mutabık;
  `bib_hygiene all` HARD=0.
- **Telif:** CC-BY dışı içerikte verbatim toplu reprodüksiyon yok; çıkarım = damıtılmış bulgu +
  kısa destek pasajı (≤25 sözcük) + provenans.
- **Dokunulmaz:** kanonik sayılar, tema mimarisi (4 tez / 6 journal), codebook v2, ve
  "Kalan Araştırmacı Kararları" (5 kod quote ID, negatif vaka yayılımı, pilot durumu, final
  alıntı seçimi) — bunlar araştırmacıya ait; otonom kapatılmaz.
- Yalnız QMD düzenlenir; `.md` mekanik kopya sonda yeniden türetilir.
- Literatür modu: **narratif derin-lit** (PRISMA sistematik derleme DEĞİL).

## Faz akışı

| Faz | İş | Araç |
|---|---|---|
| F0 | Baseline denetim (sci-audit 7-eksen: A ref, B claim, D nedensel-dil, E COREQ, G Türkçe) | sci-audit (izole subagent) |
| F1 | Tema-bazlı derin-lit: arama → **tam-metin getir** → provenanslı enrichment bulgusu | Workflow → evidentia connectors |
| F2 | Her bulgu↔kaynak adversarial doğrulama (default desteksiz) + retraction | Workflow (F1 içinde) |
| F3 | Kapı + entegrasyon: bib_hygiene + Zotero 9ZFDHMZA + referans-kapısı → QMD derinleştirme | main-loop, gated |
| F4 | Yöntem bilgi kutuları (callout) | main-loop |
| F5 | Re-denetim + Galileo three-tier + bib_hygiene HARD=0 + .md senkron + sertifikasyon | sci-audit + Galileo |

## F1 literatür domain haritası

| Domain | Kapsam | QMD yerleşim |
|---|---|---|
| Tema 1 kardeş | Kronik hastalık kardeş yükü, parentifikasyon, adalet, T1DM kardeş | Tema 1 yorum + çapraz-netice 3 |
| Tema 2 anne | T1DM maternal bakım yükü, FoH, suçluluk, hipervijilans, diyabet distresi | Tema 2 yorum |
| Tema 3 çocuk | T1DM çocuk/ergen deneyim, normalleştirme, damgalanma, tedavi yükü, özerklik | Tema 3 yorum |
| Tema 4 triad | Multi-informant discrepancy, aile sistemleri, ebeveyn-çocuk uyum | Tema 4 yorum + çapraz-netice 6 |
| Çapraz aile | Aile yönetim tarzı (FMSF), adaptasyon/dayanıklılık, paylaşılan yönetim | Çapraz-netice 1-5 + karma entegrasyon |

## Deliverables

- Zenginleştirilmiş `niteliksel_kanonik_sonuclar.qmd` (derin tartışma + bilgi kutuları + gated atıflar).
- Güncel `references.bib` (yeni doğrulanmış atıflar) + Zotero 9ZFDHMZA mutabakat.
- Denetim izi: F0 baseline + F5 re-denetim raporları; gap listesi.
- `.md` mekanik kopya senkronu.

## Kapsam dışı

- Ham transcript / verbatim alıntı-transcript eşlemesi (araştırmacı sorumluluğu).
- Kanonik sayı/tema/codebook değişikliği.
- PRISMA sistematik derleme.
- Araştırmacıya ayrılmış kararların otonom kapatılması.

## Follow-up tamamlama (2026-07-13)

Kullanıcı talebiyle üç açık kalem tam kapsamlı kapatıldı:

- **G3 — bibkey normalize:** 4 anahtar author/yıl-uyumlu düzeltildi
  (`rahmani2022mothers`→`haghighiMoghadam2022mothers`, `vaghef2023loneliness`→
  `kobos2023loneliness`, `wilson2021lived`→`palmer2022kenya`,
  `elhabashy2024siblings`→`elhabashy2023siblings`); references.bib + QMD atıfları
  güncel; `bib_hygiene all` HARD=0.
- **G2 — Zotero 9ZFDHMZA import:** 26 kaynak `zotero_env_bridge import-doi` ile
  personal library "T1DM Thesis" (9ZFDHMZA) koleksiyonuna eklendi (find-or-create
  → duplikat yok; `--no-bib` → references.bib tekrar-append yok; her item'a
  references.bib anahtarıyla eşleşen Citation Key pinlendi). **26/26, 0 hata.**
- **G1 — Galileo three-tier advisory (bağımsız GPT-5.4 + gemini-embedding):**
  HARD boş; tek SOFT-BLOCK (groundedness 0.42) *evidence-korpusu-verilmemesi
  artefaktı* olarak ampirik teyit edildi — Tema-1 bloğu F1-doğrulanmış kaynak
  pasajlarıyla yeniden yargılandığında **groundedness 0.95, citation_support
  "supported", SOFT-BLOCK temizlendi**. faithfulness 0.84–0.96, hallucination_risk
  0.12–0.38; reference_prose PASS (63 atıf/47 anahtar); consistency 0 çelişki
  (redundancy = tek-konu tematik bütünlük). Advisory: marmara_compliance
  (İngilizce terim + köşeli atıf + register) tez-final entegrasyon fazına;
  heading_cascade `main_heading_not_upper` bu manuskript-çıktısına uygulanmaz
  (errors=0, doc-type mismatch).
