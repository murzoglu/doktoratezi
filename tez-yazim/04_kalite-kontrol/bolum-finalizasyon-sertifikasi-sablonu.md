# Bölüm Finalizasyon Sertifikası

Durum: `draft | certification-running | blocked | provisional-pass | certified-final`

## Bölüm Kimliği

| Alan | Değer |
|---|---|
| Bölüm kodu |  |
| Bölüm başlığı |  |
| Üretim dosyası | `chapters/...qmd` |
| Hazırlık briefi | `tez-yazim/03_bolum-hazirlik/...md` |
| Sertifikasyon tarihi | YYYY-MM-DD |
| Sertifikasyonu uygulayan |  |
| Uygulama onayı | `bekliyor | verildi | reddedildi` |
| Onay veren |  |

## Kapı 0: Kapsam ve Gizlilik

- [ ] Bölüm dosyası ve hazırlık briefi okundu.
- [ ] `docs/tez-kilavuz` ve `format-kontrati.md` okundu.
- [ ] Kritik kaynak manifesti okundu.
- [ ] Ham veri, ham transcript, satır düzeyi veri, `.env`, token veya
      credential rapora taşınmadı.

Kanıt:

```text
Komutlar / dosyalar / notlar:
```

## Kapı 1: Derin Literatür ve Künye Evreni

| Veri tabanı / araç | Sorgu veya kapsam | Sonuç | Gap |
|---|---|---|---|
| Evidentia D0-D6 |  |  |  |
| PubMed/EPMC |  |  |  |
| OpenAlex |  |  |  |
| Semantic Scholar |  |  |  |
| Paper Search |  |  |  |
| PsyArXiv/OSF |  |  |  |
| YÖK Tez |  |  |  |
| ERIC |  |  |  |
| Koşullu diğer MCP |  |  |  |

Künye özeti:

| Citation key | DOI/PMID/ID | Çalışma tipi | Dahil/dışla | Gerekçe |
|---|---|---|---|---|

Semantik değerlendirme:

```text
Popülasyon, ölçüm, yöntem kalitesi, aktarılabilirlik, çelişki ve bölümde kullanım notu:
```

Kapı 1 kararı: `PASS | FAIL`

## Kapı 2: Full-Text, Zotero ve Anamnesis

| Citation key | Full-text route | Zotero item | Attachment/note | BibTeX key | Ledger durumu |
|---|---|---|---|---|---|

Anamnesis/context veya semantik full-text inceleme notu:

```text
Kullanılan corpus/index, hedefli çıkarımlar, claim lokatörleri ve telif/gizlilik notu:
```

Kapı 2 kararı: `PASS | FAIL`

## Kapı 3: Bölüm Metni ve Resmi Kılavuz Uyumu

- [ ] Resmi bölüm başlığı doğru.
- [ ] Bölüm işlevi doğru.
- [ ] H1-H5, nitel amaçlar, Faz II/post-hoc ve karma yöntem dili ayrıldı.
- [ ] Her repo-içi iddia güvenli kanıta bağlı.
- [ ] Her dış claim ledger satırına bağlı.
- [ ] Citation key'ler `references.bib` içinde var.
- [ ] Tablo/şekil/kısaltma/cross-reference uyumu kontrol edildi.

Kapı 3 kararı: `PASS | FAIL`

## Kapı 4: Türkçe İmla, Akış ve Mantık

- [ ] Türkçe imla ve noktalama kontrol edildi.
- [ ] Terimler ve kısaltmalar tutarlı.
- [ ] Paragraf akışı bütünlüklü.
- [ ] Gereksiz tekrar ve bölüm dışı içerik yok.
- [ ] Nedensellik/genelleme/klinik öneri sınırları doğru.
- [ ] Ondalık virgül ve `p` yazımı uyumlu (G5 blocker'sız).
- [ ] `sci-audit` axis G (`/sci-audit:check-turkish`) Kapı 4 denetimi çalıştırıldı.
- [ ] sci-audit axis G raporunda `error` (blocker) yok; `warning` (major) bulguları düzeltildi veya gerekçeli kabul edildi.

Edit notları:

```text
```

Kapı 4 kararı: `PASS | FAIL`

## Kapı 5: AI-Reliability ve Teknik Doğrulama

Manüskript adli denetimi (sci-audit — axes A–F; imla G Kapı 4'te):

| Komut | Sonuç |
|---|---|
| `/sci-audit:audit chapters/<bolum>.qmd --lang tr --type <kılavuz>` |  |
| `/sci-audit:audit-report --out raporlar/<bolum>-sci-audit.md` |  |

Repo/veri invaryantı (KVKK/ham veri/quote-parity — sci-audit DIŞI):

| Komut | Sonuç |
|---|---|
| `./dmnitel ai-context` |  |
| `./dmnitel route-tool --query "<bolum> sertifikasyon kaynak ve araç kapıları"` |  |
| `t1dm-qual-ai-audit` |  |
| `doktoratezi-ai-audit` |  |
| `python3 scripts/util/zotero_env_bridge.py status --json` |  |
| `git diff --check -- ...` |  |
| `quarto check` |  |
| `quarto render thesis.qmd` | `not-run | pass | fail` |
| Koşullu R/nitel/promptfoo kontrolleri |  |

AI-use log:

```text
Gerekli değil / eklendi: <log notu>
```

Kapı 5 kararı: `PASS | FAIL`

## Bloklayıcılar ve Çözüm

| Bloklayıcı | Durum | Çözüm |
|---|---|---|

## Nihai Sertifika Kararı

| Alan | Değer |
|---|---|
| Kapı 0 | `PASS | FAIL` |
| Kapı 1 | `PASS | FAIL` |
| Kapı 2 | `PASS | FAIL` |
| Kapı 3 | `PASS | FAIL` |
| Kapı 4 | `PASS | FAIL` |
| Kapı 5 | `PASS | FAIL` |
| Nihai durum | `blocked | provisional-pass | certified-final` |

Final notu:

```text
```
