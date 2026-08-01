---
description: 'Seçili tez metninin ANLATIMINI + referans doğruluk/kapsam/tutarlılığını zenginleştirir (sayı/istatistik/bulgu ve yapı DOKUNULMAZ); repo-yerel sci-audit ikamesi + galileo-audit MCP kapısından geçirip onaya sunar (dosyaya doğrudan yazmaz)'
mode: agent
---

# /anlatim-zenginligi — Anlatım Zenginleştirme Kapısı (Copilot ikizi)

Zenginleştirilecek metin: **${input:hedef:seçili metin veya chapters/<bolum>.qmd konumu}** — boşsa editör seçimini kullan.

Bu prompt, Claude komutu [.claude/commands/anlatim-zenginligi.md](../../.claude/commands/anlatim-zenginligi.md)
ve eşgüdüm playbook'u [tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md](../../tez-yazim/04_kalite-kontrol/bulgular-zenginlestirme-esgudum-playbook.md)
ile **aynı doktrinin** Copilot/VS Code ikizidir; ikisi bu işte **bağlayıcıdır**. `sci-audit` plugin'i
`~/.claude/plugins/marketplaces/cureonics-marketplace/plugins/sci-audit` altında **kuruludur**: Copilot'ta
slash komutları (`/sci-audit:*`) yoktur, ama skilleri (`turkish-sci-style`, `citation-forensics`,
`claim-grounding`, `stats-forensics`) otomatik tetiklenir ve scriptleri doğrudan çalıştırılır.

## DOKUNULMAZ kanıt bölgesi vs. düzenlenebilir anlatım/referans bölgesi

Bu araç YALNIZ **etkili bilimsel anlatım** + **referans doğruluk/kapsam/tutarlılığı** üzerinde
çalışır. Sayı/istatistik (g, β, SE, p, %GA, ICC, AUC, N, yüzde …), bulgunun içeriği/yönü/
anlamlılığı/büyüklüğü, bulgu sırası ve `@tbl-*`/`@fig-*`/`[@key]` token'ları **aynen korunur** —
yeniden yorumlanmaz, yuvarlanmaz, güçlendirilmez. Kaynakta olmayan özgüllük (informant "anneden",
"klinik açıdan anlamlı", "sağlam/dayanıklı", nedensellik) **eklenmez.** Zenginleştirme = terim izahı
+ okuyucu bağlamı + **ayrı ve atıflı** literatür karşılaştırması; bu çalışmanın yeni bir bulgusu
gibi sunulmaz.

## Yürütme (sıra sabittir)

1. **Bağlamı sabitle — DOSYA ADI TAHMİN ETME.** Seçili ifadeyi `grep -rn "<parça>" chapters/`
   ile ara; pasajın gerçek dosya + satırını bul. Sayısal iddiaların kaynak-tekilliğini artefakttan
   doğrula (gömülü literal yok). `t1dm-tez-rehberi` skill'i Faz 0 kapsam + Faz 0.5 tedbir kapısı.
2. **Literatür zenginleştirme (Minerva + anamnesis).** `minerva-evidence` MCP: `minerva_literature_search`
   (Türkçe sorgu = `mode:semantic`; İngilizce = hybrid) + `minerva_literature_fulltext_by_doi`.
   Kaynağı **bütün-makale** olarak kavra (amaç/yöntem/örneklem/ana-iddia/koşul), tek cümleden değil
   (cherry-pick = çarpıtma). **KVKK: gateway'e yalnız literatür terimi; katılımcı/ham/aile-düzeyi veri asla.**
3. **Türkçe revize et — yalnız anlatım/referans bölgesi.** Marmara sözleşmesi
   ([tez-yazim/00_kaynak-kurallari/](../../tez-yazim/00_kaynak-kurallari/)): pasif 3. tekil; **ondalık virgül**
   (`0,38`, `p<0,001`); terim ilk geçişte tam ad + parantezde kısaltma. `[@key]`/`@tbl-*`/`@fig-*` ve
   tüm sayı/yön/anlamlılık/sıra **aynen**.
4. **Yeni atıf = ADAY (uydurma YASAK).** `references.bib`'de olmayan kaynak gerekiyorsa ayrı "öneri"
   bloğunda listele; revizyondan ÖNCE [referans-kapisi.prompt.md](referans-kapisi.prompt.md) ile `cite-ok` yap.
5. **Denetle — UYGULAMADAN ÖNCE (araçları karıştırma).** Aday revizyonu önizleme parçasına yaz, kapıları koştur:

   | Kademe | Copilot ortamı aracı | Rol |
   |---|---|---|
   | **HARD** | `turkish-sci-style` skill · `python3 ~/.claude/plugins/marketplaces/cureonics-marketplace/plugins/sci-audit/skills/turkish-sci-style/scripts/tr_sciaudit.py <dosya> --strictness certification` | Axis G: Türkçe imla + okunabilirlik |
   | **HARD** | `python3 scripts/util/tr_corpus_audit.py all --fail-on blocker` + `python3 scripts/util/tez_checklist_verify.py --fast` | Repo-yerel ondalık-virgül kapısı (nokta-`p` = blocker) |
   | **HARD** | `citation-forensics` skill (pubmed/openalex/semantic-scholar MCP) + `python3 scripts/util/bib_hygiene.py all` | Axis A referans bütünlüğü |
   | **HARD** | `stats-forensics` + `claim-grounding` skilleri + `python3 scripts/util/claim_certification.py` + `python3 scripts/util/csr_causal_label_audit.py` | Axis B/C istatistik + iddia temellendirme |
   | **SOFT-block** | `galileo-audit` MCP `galileo_judge` (`text`,`section_type`,`evidence`) | Revize metnin faithfulness/groundedness/citation_support |
   | **SOFT-block** | `galileo-audit` MCP `galileo_claim_source_match` (`claim`,`source_text`) | Yeni/güçlendirilen iddia ↔ kaynak temellendirmesi |
   | **advisory** | `galileo-audit` MCP `galileo_coherence` · `galileo_reference_prose` | Akış/tekrar · atıf yoğunluğu |

   HARD = override yok, herhangi blocker/FAIL → düzelt-ve-tekrar. SOFT-block eşikleri
   [.claude/galileo.local.md](../../.claude/galileo.local.md) (groundedness/faithfulness < 0,60; nicel iddia `unsupported`).
6. **Onaya sun.** (a) diff (eski→yeni), (b) kapı özeti (HARD/SOFT/advisory + galileo skorları),
   (c) aday atıflar + kapı durumu. **Açık kullanıcı onayı olmadan Edit/commit yok.**
