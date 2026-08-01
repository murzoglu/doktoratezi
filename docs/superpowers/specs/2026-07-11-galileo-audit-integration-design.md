# galileo-audit — Bağımsız Değerlendirme Katmanı (sci-audit yanında) — Tasarım

> **Tarih:** 2026-07-11 · **Durum:** onaylandı (kullanıcı: tasarım + "belli eşiklerde soft block ekle") · **Kapsam:** yetenek kurulumu (denetim katmanı), tez metni yazımı değil.
> **Bağlayıcı üst kaynak:** `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md`; KVKK sınırı için [[plugin-tooling-integration]] + Minerva deseni.

## 1. Amaç
Tez yazım sistemine, sci-audit'in (Claude-native denetim) **yanında** bağımsız bir değerlendirme katmanı eklemek: **GPT-5.4 judge** (model-çeşitliliği ile ikinci-görüş), **gemini-embedding-2 semantik-tutarlılık** (tez-içi çelişki/tekrar/dup) ve **Galileo eval-harness** (regresyon takibi). Sistem-düzeyi kazanım: tek-model korelasyonlu hatalarını kıran, farklı-sağlayıcı bağımsız denetim.

## 2. Locked kararlar
- **Deployment:** Roche-kapalı (Azure OpenAI GPT-5.4 + Vertex gemini in-tenant); veri Roche tenant'ında kalır → tez **manuskript** metni gidebilir, ham katılımcı verisi ASLA (Minerva ile aynı sınır).
- **Kapsam:** A (judge) + B (semantik) + C (harness) — hepsi.
- **Kompozisyon:** three-tier gate (HARD sci-audit / SOFT Galileo / advisory).

## 3. Mimari ilke
Minerva ↔ evidentia neyse, **galileo-audit ↔ sci-audit** odur (evidentia §1.5/§1.6 *extension* deseni, denetim tarafında). sci-audit plugin'i **düzenlenmez**. Repo katmanına gitignored köprü eklenir; t1dm-tez-rehberi **Faz 3.6**'da sci-audit'ten sonra advisory/soft-block pass olarak çağrılır. 3-katman sınırı korunur: evidentia getirir → t1dm-tez-rehberi üretir → **sci-audit (Claude) + galileo-audit (GPT-5.4/gemini) denetler**.

## 4. Bileşenler

### Köprü
`scripts/eval/galileo_bridge.py` — bağımlılıksız (tercihen), `${GALILEO_*}` env'den runtime kimlik (`GALILEO_API_KEY`, `GALILEO_CONSOLE_URL`, `GALILEO_JUDGE_MODEL`=gpt-5.4, `GALILEO_TEXT_EMBEDDING_MODEL`=gemini-embedding-2, `GALILEO_PROJECT`?); **değer basılmaz/commit edilmez**. İki giriş noktası: (a) proje `.mcp.json`'da MCP `galileo-audit` sunucusu (on-demand araçlar A+B), (b) `scripts/eval/thesis_eval_run.py` batch-runner import eder (C).

### A — Judge (GPT-5.4)
- `galileo_judge(text, section_type, evidence?)` → per-boyut skor: `faithfulness`, `groundedness` (verilen kanıta karşı), `citation_support`, `marmara_compliance`, `hallucination_risk` + gerekçe + işaretli span'lar.
- Faz 3.6'da sci-audit 7-eksenden sonra bağımsız ikinci-görüş.

### B — Semantik (gemini-embedding-2)
- `galileo_consistency(texts[])` → bölümler-arası çelişki/tekrar çiftleri (cosine + judge-onay), her çift {sim, tip: contradiction|redundancy}.
- `galileo_bib_dedup(bib_entries[])` → references.bib yakın-duplikat (aynı makale farklı key).
- `galileo_claim_source_match(claim, source_text)` → claim↔kaynak semantik groundedness skoru.

### C — Harness
- `galileo_eval_run(dataset, metrics)` → Galileo experiment loglar.
- `scripts/eval/thesis_eval_run.py` → bölüm finalizasyonunda (paragraf + kanıt) dataset kurup skorları dashboard'a gönderir; regresyon takibi.

### Config
`.claude/galileo.local.md` (YENİ, **gitignored**, evidentia.local.md muadili): `enabled`, model adları (env'e köprü), soft-block eşikleri, `project`. Eşikler buradan ayarlanır.

## 5. Kompozisyon — three-tier gate

| Katman | Tetik | Etki |
|--------|-------|------|
| **HARD (sci-audit, değişmez)** | ondalık-nokta `p`; uydurma/retraction künye; GRIM-imkansız istatistik | Bölüm `blocked`; düzeltmeden geçilmez |
| **SOFT-block (Galileo, YENİ)** | `groundedness<0,60` VEYA `faithfulness<0,60`; nicel iddia `citation_support=unsupported`; bölümler-arası çelişki `sim≥0,85 + judge-onaylı`; büyük Claude↔GPT bütünlük çelişkisi (GPT major-fabrication flag'i Claude'un geçtiği yerde, veya tersi) | Bölüm en fazla `provisional-pass`; `certified-final` yalnız düzeltme VEYA sertifika-defterine yazılan **açık insan override gerekçesi** ile |
| **Advisory (yalnız rapor)** | bib yakın-duplikat; tekrar (çelişki değil); üslup/register judge notları; küçük skor düşüşleri | Rapor; blok yok |

Eşikler `.claude/galileo.local.md`'de configurable (defaults yukarıda). Soft-block, `bolum-finalizasyon-sertifikasyon-playbook.md` Kapı 0–5'e ek bir girdi olur (override defter kaydı: `tez-yazim/04_kalite-kontrol/sertifikalar/`).

## 6. Veri akışı (örnek)
Bölüm finali → sci-audit 7-eksen (Claude; HARD blocker'lar) → **galileo-audit pass**: `galileo_judge` (paragraf+kanıt) + `galileo_consistency` (bu bölüm vs önceki bölümler) + `galileo_claim_source_match` (nicel iddialar) → three-tier sınıflama → advisory rapor + soft-block listesi → insan adjudike/override → `thesis_eval_run` regresyon logu. **KVKK: yalnız manuskript + literatür + references.bib gider.**

## 7. Governance / KVKK
- Roche-kapalı routing; Galileo'ya **yalnız manuskript metni + getirilen literatür + references.bib**; ham katılımcı/aile-düzeyi/transkript/kimlikleyici **ASLA**.
- Köprü + `.mcp.json` galileo girişi **gitignored** (iç altyapı; `.mcp.json` zaten `.gitignore`'da).
- `.claude/settings.json permissions.deny` / `.env` **dokunulmaz**; env değerleri yalnız `os.environ`'dan, basılmaz.

## 8. Phase 0 — API kontrat keşfi (Minerva dersi)
⚠️ Minerva canlı doğrulandı; **Galileo API'si henüz doğrulanmadı**. İlk adım Phase 0: Galileo SDK sürümü/auth şeması + minik judge çağrısı + minik embedding çağrısı → Roche-kapalı routing doğrulaması (Minerva GraphQL keşfi gibi). Araçlar Galileo'nun **gerçek** yüzeyine bağlanır; bir işlem temiz desteklenmiyorsa (ör. standalone embedding, custom-rubric scorer) uyarlanır ve dürüstçe not edilir. Plan Phase 0 ile başlar; kontrat bilinmeden A/B/C araç imzaları kesinleşmez.

## 9. Repo-katmanı dokümantasyon/kablolama (TRACKED)
- `.claude/skills/t1dm-tez-rehberi/references/manuskript-denetimi-sciaudit.md` → §"Galileo Bağımsız Judge + Semantik Katman" (Minerva §1.2 muadili; env-adları, KVKK, three-tier).
- `SKILL.md` Faz 3.6 → galileo-audit advisory/soft-block adımı.
- `CONVENTIONS.md` (+ audit ikizi) → denetim-katmanı extension notu (Minerva notu gibi).
- `.gitignore` → `scripts/eval/galileo_bridge.py` + `.claude/galileo.local.md` ignore; **spec TRACKED** (galileo-adlı, ignore yok).
- `bolum-finalizasyon-sertifikasyon-playbook.md` → soft-block girdisi + override defter kaydı.

## 10. Test / kabul kriterleri
- [ ] **Phase 0:** auth handshake + minik judge + minik embedding çağrısı Roche-kapalı routing'de başarılı; env değeri sızmıyor.
- [ ] **A judge:** örnek paragraf (+kanıt) → 5-boyut skor + gerekçe döner; kanıtsız uydurma paragrafta groundedness düşer (negatif kontrol).
- [ ] **B semantik:** iki çelişen bölüm → contradiction çifti; references.bib → bilinen dup yakalanır; claim↔kaynak eşleme skoru makul.
- [ ] **C harness:** `thesis_eval_run` bir experiment loglar.
- [ ] **Three-tier:** eşik-altı groundedness soft-block üretir; bib-dup advisory kalır; sci-audit HARD blocker'ları değişmez.
- [ ] **KVKK guard:** invocation contract yalnız manuskript/literatür geçirir; ham-veri alanı gitmez (sözleşme + test).
- [ ] **Config:** `.claude/galileo.local.md` parse + git-ignore doğrulanır.

## 11. Kapsam dışı / kısıtlar
- Bu tur **yeteneği kurar**; bölüm metnini yeniden yazmaz.
- Dokunulmaz: sci-audit/evidentia plugin iç dosyaları, `permissions.deny`, `.env`, ham veri katmanları.
- Commit: repo kuralı #14 — yalnız açık istekle.
- Phase 0 kontratı A/B/C imzalarını değiştirebilir; spec, kontrat-agnostik yazılmıştır.

## 12. Reddedilen alternatifler
- **sci-audit plugin'ini forklamak** → upstream drift; yanına ekle (Minerva dersi).
- **Galileo'yu hard-gate yapmak** → dış-judge tek başına otoriter değil; three-tier (soft-block + override) seçildi.
- **Yerel-model judge** → Roche-kapalı GPT-5.4 zaten farklı-sağlayıcı model-çeşitliliği veriyor; gereksiz ikinci yerel model.
- **evidentia tarafına bağlamak** → Galileo kanıt getirmez, denetler; sci-audit katmanına aittir.
