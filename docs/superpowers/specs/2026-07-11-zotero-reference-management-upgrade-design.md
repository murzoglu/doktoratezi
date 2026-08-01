# Zotero + Referans Yönetimi — Bütünsel Yükseltme — Tasarım

> **Tarih:** 2026-07-11 · **Durum:** onaylandı (kullanıcı: "hepsi — bütünsel yükseltme" + "araç + onaylı canlı uygulama" + tasarım "uygun") · **Değişiklik (2026-07-11):** kullanıcı Zotero yazma için **per-işlem açık onay zorunluluğunu kaldırdı** (standing yetki, kütüphane sahibi); 9ZFDHMZA scope-lock + KVKK + anahtar-basılmaz + opsiyonel `dry_run` KORUNUR. · **Kapsam:** referans-yönetim yeteneği kurulumu; tez bölüm metni yazımı DEĞİL.
> **Bağlayıcı üst kaynak:** `tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md`; künye biçimi → `tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` §4 (AMA-11); kapı sırası → `.claude/commands/referans-kapisi.md` + `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md`; KVKK/kol-ayrımı → CONVENTIONS k.9/k.15 + [[plugin-tooling-integration]].

## 1. Amaç
Tez yazım sürecinin referans katmanını üç eksende yükseltmek: (a) **çevrimdışı bib hijyeni** — atıf↔künye↔ledger mutabakatı, AMA-11 alan-tamlığı, DOI/PMID sağlığı, yakın-duplikat; (b) **Zotero↔repo akışı** — mevcut Web API köprüsünü sohbet-içi MCP araçlarına bağlamak ve iki-kopya drift'ini kesmek; (c) **canlı Zotero organizasyonu** — tez kaynaklarını `T1DM Thesis` koleksiyonu altında bölüm/tema alt-koleksiyon + etiket şemasına oturtmak. Sistem kazanımı: render-kıran atıf hatalarını erkenden yakalayan, künye biçimini AMA-11'e karşı doğrulayan, elle-ledger sürtünmesini azaltan tekrarlanabilir bir referans-yönetim hattı.

## 2. Locked kararlar
- **Kapsam:** dört parça birden (hijyen denetçisi + MCP wiring + CSL regresyon testi + canlı organizasyon) — tek tutarlı yükseltme.
- **Canlı kütüphane:** araç + canlı uygulama; kullanıcı **per-yazma onay zorunluluğunu kaldırdı** (standing yetki) → yazma op'ları durup sormadan uygulanır. **Değişmez güvenceler:** yazma yalnız `9ZFDHMZA`-scoped (kod-düzeyi hard invariant; scope-dışı yazma reddedilir), KVKK lit-meta, anahtar yazdırılmaz, opsiyonel `dry_run` önizleme; önce `status` bağlantı doğrulaması.
- **Paketleme:** Yaklaşım A — ayrık çevrimdışı saf modül + mevcut köprünün MCP sarmalayıcısı (all-in-one köprü ve minimal-galileo alternatifleri reddedildi).
- **Scope kilidi:** tüm canlı Zotero op'ları **yalnız `9ZFDHMZA` (T1DM Thesis)** koleksiyonuna; Cystic Fibrosis / CF-Vaccination ve diğer proje koleksiyonlarına **asla** dokunulmaz, enumerate edilmez.

## 3. Gözlemlenen mevcut durum (grounding)
- **Köprü:** `scripts/util/zotero_env_bridge.py` (~42 KB, bağımlılıksız, 12 alt-komut: status/groups/collections/search/export-bibtex/cite/children/upload-file/delete-item/set-citation-key/import-doi). `.env → ZOTERO_API_KEY`. Yalnız CLI (MCP değil). İkinci kopya: `niteliksel/scripts/util/zotero_env_bridge.py`.
- **references.bib:** 126 künye (114 makale, 6 mastersthesis, 3 phdthesis, 3 book); **tekrar anahtar yok**; semantik `authorYYYYetiket` şeması; PMID/PMCID yaygın; ~4 makale DOI'siz; **75 anahtar** `chapters/*.qmd`'de atıfta (≈51 tanımlı-atıfsız — staged/orphan belirsiz).
- **CSL:** aktif `references/marmara-ama11.csl` (`_quarto.yml`); legacy `apa.csl` korunuyor. Elle `references/_csl_test/` smoke var, otomatik test yok.
- **Yönetişim:** `/referans-kapisi` 6-adım + `referans-denetim-ledgeri.md` (70 KB kanonik ledger) + marmara-tez-formati §4 (AMA-11). `galileo_bib_dedup` galileo köprüsünde mevcut (embedding yakın-duplikat).
- **Canlı Zotero (salt-okunur doğrulandı):** userID 17265855 (`mahirkurt`), kullanıcı+grup yazma erişimi. 12 koleksiyon; tez içeriği tek koleksiyonda: **`T1DM Thesis` = 9ZFDHMZA**; kalanı çoğunlukla farklı proje (Cystic Fibrosis / CF-Vaccination). Tam envanter Faz 0'da köprü komutlarıyla çıkarılır.

## 4. Mimari — üç düzlem
- **Çevrimdışı düzlem (tracked, saf, testli):** `scripts/util/bib_hygiene.py` — yalnız `references.bib` + `chapters/*.qmd` + `referans-denetim-ledgeri.md` okur; **ağ yok, deterministik.**
- **Çevrimiçi düzlem (gitignored anahtar; standing-yetkili yazma, scope-lock'lu):** mevcut `zotero_env_bridge.py` + yeni gitignored `scripts/mcp/zotero_refs_bridge.py` → gitignored `.mcp.json`'da `zotero-refs`. Zotero'ya **yalnız 9ZFDHMZA-scoped**.
- **Semantik düzlem (mevcut):** `galileo_bib_dedup` — hijyen modülünün opsiyonel zenginleştirmesi; yoksa bağımlılıksız Jaccard fallback.

Sınır ilkesi: çevrimdışı saf mantık ↔ çevrimiçi anahtarlı op'lar kesin ayrık; çevrimdışı katman ağ/anahtar görmez, tek başına test edilir.

## 5. Bileşenler

### 5.1 `scripts/util/bib_hygiene.py` — çevrimdışı denetçi (TRACKED)
Bağımlılıksız Python; alt-komutlar:
- `reconcile` — 3-yönlü fark: (a) chapters'ta atıflı ∧ bib'de yok → **HARD/ERROR** (render kırar); (b) bib'de var ∧ hiç atıfsız → **INFO** (orphan/staged); (c) ledger ↔ bib ↔ chapters tutarlılık farkı.
- `fields` — AMA-11 alan-tamlığı, künye tipine göre zorunlu alan seti: makale = author,title,journal,year,volume,issue,pages,doi; mastersthesis/phdthesis = author,title,school,year,type; book/incollection = author|editor,title,publisher,address,year (+ chapter için editor,pages,edition). Eksik zorunlu alan → **WARN**.
- `ids` — DOI/PMID varlık + regex geçerlik + yinelenen DOI tespiti.
- `dedup` — galileo `galileo_bib_dedup` varsa embedding yakın-duplikat; yoksa başlık+yazar Jaccard fallback (bağımlılıksız).
- **Çıktı:** `--json` makine-okunur + varsayılan Türkçe rapor; gate için anlamlı exit-code. `--out` ile tracked snapshot: `tez-yazim/04_kalite-kontrol/raporlar/bib-hijyen-raporu.md` (yalnız açık lit-meta → güvenli/tracked).
- **Girdi kaynakları salt-okunur:** dosyaları yazmaz (rapor hariç); `references.bib`'i değiştirmez; künye **silmez/otomatik düzeltmez** — yalnız raporlar.

### 5.2 Zotero MCP wiring (GITIGNORED)
- Yeni `scripts/mcp/zotero_refs_bridge.py` (minerva_evidence_bridge deseni; stdio JSON-RPC MCP) mevcut köprü fonksiyonlarını araç olarak sunar; `.mcp.json`'da `zotero-refs` sunucusu (`.mcp.json` zaten gitignored).
- **Salt-okunur araçlar (her zaman):** `zotero_status`, `zotero_search`, `zotero_export_bibtex`, `zotero_collection_items` (9ZFDHMZA-scoped), `zotero_reconcile_bib` (bib_hygiene reconcile'ı çağırır).
- **Yazma araçları (standing yetki — per-çağrı onay YOK):** `zotero_add_to_collection`, `zotero_set_tag`, `zotero_import_doi` — durup sormadan uygulanır. **Kod-düzeyi hard invariant:** hedef koleksiyon `9ZFDHMZA` (veya alt-koleksiyonu) değilse yazma **reddedilir**; opsiyonel `dry_run=true` uygulamadan önizler.
- KVKK: yalnız literatür-meta; anahtar yazdırılmaz; CF/diğer koleksiyonlar enumerate/modify edilmez.

### 5.3 İki-kopya köprü → parity guard (fiziksel merge DEĞİL)
- `scripts/util/zotero_env_bridge.py` (nicel) ve `niteliksel/scripts/util/zotero_env_bridge.py` (nitel) **KVKK kol-ayrımı** gereği fiziksel ayrı kalır (her kol self-contained; kollar arası import yasak).
- `tests/test_zotero_bridge_parity.py` iki dosyanın **bayt-özdeş** (veya yalnız belgeli başlık farkı) olduğunu doğrular → sessiz davranış-drift'ini keser. Bu, coupling'siz tekilleştirmedir.

### 5.4 CSL render regresyon testi (TRACKED)
- `tests/test_marmara_csl_render.py` → `pandoc --citeproc` ile `references/_csl_test/test-refs.bib` + `references/marmara-ama11.csl` render eder; test.qmd'deki gömülü **BEKLENEN KAYNAKÇA** bloğunu çıkarır, normalize-karşılaştırır.
- Guard'lar: et-al `ve ark.`, `ve` bağlacı, `https://doi.org/` DOI biçimi, alfabetik sıra, italik/kalın yokluğu, metin-içi (Yazar ve ark., YYYY) biçimi. Quarto yerine pandoc → hızlı, hafif, freeze bağımsız.

### 5.5 Canlı Zotero organizasyonu (9ZFDHMZA-scoped)
- **Şema dokümanı** `tez-yazim/06_kritik-kaynaklar/zotero-organizasyon-semasi.md`: `T1DM Thesis` altına alt-koleksiyonlar (tez temasına göre; örn. EMBU/ebeveynlik tutumu · T1DM psikososyal · kardeş uyumu · maternal depresyon/Beck · KİA/ölçek-geçerlik/COSMIN · yöntem/istatistik · Türkiye/YÖK tez) + etiket taksonomisi (`t1dm`, `embu`, `sibling`, `maternal-depression`, `measurement`, `turkiye`, `staged`, `cited`). Şema, bib anahtarlarının semantik etiketleriyle eşlenir.
- **Uygulama (düzlem-ayrık):** (1) *çevrimdışı* — `bib_hygiene desired-scheme` bib anahtarlarının semantik etiketlerinden **istenen-durum eşlemesi** (key → alt-koleksiyon + etiketler) üretir (ağsız, deterministik, tracked çıktı); (2) *çevrimiçi* — `zotero_refs_bridge` istenen-durum eşlemesi ile canlı 9ZFDHMZA envanterini karşılaştırıp op listesi (`sync-plan`) çıkarır ve köprü yazma araçlarıyla **durup sormadan** uygular (standing yetki; `dry_run` ile önce önizlenebilir). Faz 0'da 9ZFDHMZA envanteri (bridge komutları) çıkarılır; scope-lock gereği **CF koleksiyonlarına dokunulmaz.** İstenen-şema türetimi çevrimdışı, canlı fark+yazma çevrimiçi kalır — §4 düzlem sınırı korunur.

## 6. Gate kompozisyonu — three-tier (mevcutla tutarlı)
| Katman | Tetik | Etki |
|--------|-------|------|
| **HARD** | chapters'ta atıflı ∧ bib'de tanımsız anahtar (render kırar); (mevcut sci-audit HARD'ları değişmez) | Bölüm `blocked`; düzeltmeden geçilmez |
| **SOFT-block** | atıflı künyede eksik zorunlu AMA-11 alanı; atıflı makalede DOI eksik; galileo-onaylı yakın-duplikat | En fazla `provisional`; düzeltme veya ledger'a yazılan açık override |
| **Advisory** | orphan (tanımlı-atıfsız); staged künye; küçük biçim notları | Rapor; blok yok |

Eşik/tanımlar `bib_hygiene`'de; sertifikasyon Kapı'sına `bolum-finalizasyon-sertifikasyon-playbook.md` üzerinden bağlanır (galileo three-tier deseniyle aynı).

## 7. Veri akışı (örnek — bölüm finali)
Bölüm finali → `bib_hygiene reconcile` (chapters↔bib↔ledger) → `fields`+`ids`+`dedup` → three-tier sınıflama → HARD varsa blok; SOFT liste + advisory rapor → `/referans-kapisi` ledger mutabakatı (Zotero item/BibTeX key) → gerekiyorsa `sync-plan` ile canlı Zotero düzeni (standing-yetkili, scope-lock'lu, `dry_run` önizlemeli) → sertifikasyon Kapısı. **KVKK: yalnız künye-meta + manuskript; ham katılımcı verisi ASLA.**

## 8. Yönetişim kablolaması (TRACKED)
- `.claude/commands/referans-kapisi.md` + `referans-denetim-ledgeri.md`: "otomatik ön-mutabakat `bib_hygiene reconcile`" ön-adımı (kapı sırası korunur).
- `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`: bib-hijyen girdisi (cited-undefined=HARD; diğerleri SOFT/advisory).
- `CONVENTIONS.md` (+ `plugins/doktoratezi-ai-audit/.../CONVENTIONS.md` ikizi) k.9: Zotero MCP wiring + `bib_hygiene` notu.
- `.claude/skills/t1dm-tez-rehberi/references/literatur-kanit-evidentia.md` + `manuskript-denetimi-sciaudit.md` + `SKILL.md`: yeni araçlara işaret.
- `.gitignore`: `scripts/mcp/zotero_refs_bridge.py` ignore (`.mcp.json` zaten ignore); `bib_hygiene.py` + parity/CSL testleri + şema dokümanı + rapor **tracked**.

## 9. Test / kabul kriterleri
- [ ] **bib_hygiene reconcile:** bilinen atıflı-tanımsız anahtar (fixture) HARD verir; tanımlı-atıfsız INFO; ledger farkı raporlanır.
- [ ] **fields:** DOI'siz/eksik-alan künye (fixture) WARN; tam künye temiz geçer.
- [ ] **ids:** bozuk DOI regex yakalanır; yinelenen DOI raporlanır.
- [ ] **dedup:** bilinen yakın-dup çift (fixture) yakalanır (galileo varsa embedding, yoksa Jaccard).
- [ ] **parity:** iki köprü kopyası bayt-özdeş; kasıtlı fark testi kırar.
- [ ] **CSL render:** `_csl_test` render'ı beklenen AMA-11 bloğuyla eşleşir; et-al/`ve`/DOI/sıra guard'ları geçer.
- [ ] **MCP smoke:** `zotero-refs` salt-okunur araçları (status/collection_items 9ZFDHMZA) yanıt verir; yazma araçları onaysız çalışır AMA scope-dışı (9ZFDHMZA olmayan) hedefte **reddedilir** (scope-lock); `dry_run=true` uygulamadan önizler.
- [ ] **KVKK guard:** çevrimdışı modül ağ çağrısı yapmaz; çevrimiçi çağrılar 9ZFDHMZA-scoped; CF koleksiyonu enumerate/modify edilmez; anahtar basılmaz.
- [ ] **Canlı organizasyon:** şema dokümanı + `sync-plan` op'ları üretir; canlı uygulama standing-yetkili (per-yazma onay yok), scope-lock'lu, `dry_run` önizlemeli.

## 10. Kapsam dışı / kısıtlar
- Bölüm metni yeniden yazılmaz; orphan künye otomatik silinmez (yalnız rapor).
- CF/diğer proje koleksiyonları ve tez-dışı kütüphane içeriği dokunulmaz.
- sci-audit/evidentia/galileo plugin iç dosyaları, `permissions.deny`, `.env`, ham veri katmanları dokunulmaz.
- Commit: repo kuralı #14 — yalnız açık istekle; gitignored altyapı (MCP köprüsü, `.mcp.json`, anahtar) commit edilmez.

## 11. Reddedilen alternatifler
- **Her şeyi köprüye ekle (B):** köprü 60 KB+, çevrimiçi/çevrimdışı karışır, test zor, iki-kopya sorunu büyür → ayrışma kötüleşir.
- **Minimal galileo-dedup + elle gate (C):** asıl render-kıran cited↔defined kontrolü yok; organizasyon/CSL/MCP karşılanmaz → "hepsi" hedefinin altında.
- **İki köprüyü fiziksel merge / kollar arası import:** KVKK kol-ayrımını bozar → parity-test tercih edildi.
- **Zotero desktop full-text helper'a bağlanmak:** koddaki yol Codex'e ait, bu Claude Code ortamında yok → yalnız Web API köprüsü hedeflenir.
