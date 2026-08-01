# Zotero Organizasyon Şeması — T1DM Thesis (9ZFDHMZA)

> **Amaç:** Tez kaynaklarını Zotero `T1DM Thesis` koleksiyonu (key `9ZFDHMZA`) altında bölüm/tema alt-koleksiyonları + etiket taksonomisiyle düzenlemek. **Scope kilidi:** tüm op'lar yalnız `9ZFDHMZA` (ve alt-koleksiyonları); aşağıdaki "dokunulmaz koleksiyonlar" **asla** değiştirilmez/enumerate edilmez.
> **Yetki:** Kullanıcı Zotero yazma için per-işlem açık onay zorunluluğunu kaldırdı (standing yetki). Kod-düzeyi `_assert_in_scope`/`_assert_item_in_scope` scope-dışı yazmayı reddeder; `dry_run` önizleme opsiyoneldir; API anahtarı yazdırılmaz (KVKK: yalnız literatür-meta).
> **Kaynak doktrini:** bkz. `docs/superpowers/specs/2026-07-11-zotero-reference-management-upgrade-design.md` §5.5; araç: `scripts/util/bib_hygiene.py desired-scheme` (çevrimdışı eşleme) + `scripts/mcp/zotero_refs_bridge.py` (çevrimiçi, gitignored).

## 1. Mevcut durum (2026-07-11, salt-okunur envanter)

| Ölçüm | Değer |
|---|---|
| `9ZFDHMZA` üst-düzey künye (canlı) | **72** |
| Mevcut alt-koleksiyon | **0** |
| `references/references.bib` künye | **126** |
| Kapsam farkı | ~54 bib künyesi Zotero `9ZFDHMZA`'da **değil** (çoğu YÖK tez / elle eklenen kaynak; canlı reorg yalnız 72 Zotero item'ını kapsar) |

**Önemli:** Canlı organizasyon yalnız Zotero'daki 72 item'ı düzenleyebilir. bib'deki 126 künye `references.bib`'in tam kümesidir; bibkey ↔ Zotero item eşlemesi DOI üzerinden yapılır ve yalnız Zotero'da bulunan item'lar taşınır. Kalan bib künyeleri (YÖK tez vb.) `bib_hygiene` denetiminde izlenir ama Zotero reorg'una girmez.

## 2. Dokunulmaz koleksiyonlar (SCOPE-LOCK — asla değiştirilmez)

Bu kütüphane karışık kişisel kütüphanedir; aşağıdaki koleksiyonlar **farklı projelere** aittir (Kistik Fibrozis / CF-Aşı çalışmaları) ve tez araçları tarafından **hiçbir koşulda** okunmaz/yazılmaz:

`Cystic Fibrosis` (4TRKZXFM · XX9Y6HCD · Z6AERMV3) · `missing_articles` (C8HN84YN) · `full_trial_report_references` (YGT9ILKT) · `2020-2025 CF Vaccination Literature (NEW)` (ZZ3WAMZB) · `CF-Vaccination-PubMed-2022-2025` (EICMK4ZS) · `Imported from Archive` (EBCAP4E4) · `pubmed-cysticfibr-set` (GKWGVBAZ) · `2023-2025 Literature Search (358 articles)` (GIAU37DU) · `Cystic Fibrosis and Vaccines` (29JEWM2U).

`_assert_in_scope` (koleksiyon hedefi 9ZFDHMZA/alt-koleksiyon değilse) ve `_assert_item_in_scope` (item 9ZFDHMZA kapsamında değilse) bu koleksiyonlara yazmayı kod düzeyinde **reddeder** — smoke test `4TRKZXFM` (Cystic Fibrosis) üzerinde red doğrulanmıştır.

## 3. Alt-koleksiyon şeması (9ZFDHMZA altında)

`bib_hygiene desired-scheme` çıktısının 126 künye üzerindeki dağılımı (BAŞLIK-taramalı zenginleştirilmiş eşleme):

| Alt-koleksiyon | bib künye (126) | Not |
|---|---|---|
| **T1DM Psikososyal** | 28 | ISPAD/T1D/diyabet/glisemik/psikososyal/distress |
| **EMBU / Ebeveynlik Tutumu** | 15 | embu/parenting/parental/rearing/ebeveyn |
| **Ölçek Geçerlik / COSMIN** | 13 | cosmin/psychometric/validation/reliability/ölçek |
| **Maternal Depresyon / Beck** | 12 | maternal/depress/beck/bdi/anxiety |
| **Türkiye / YÖK Tez** | 9 | tez tipi + yoktez key |
| **Kardeş Uyumu** | 6 | sibling/kardeş (başlıktan) |
| **KİA / Yaşam Kalitesi** | 1 | quality of life/qol/well-being |
| **Genel** | 42 | eşleşmeyen (catch-all) |

**İyileştirme uygulandı:** Eşleme artık key+keywords **+ başlık** tarıyor; "Genel" 78→42 düştü (**84/126 = %67 özgül sınıflama**). Son-eşleşen token kazanır (genel diyabet token'larını özgül temalar ezer). Kalan 42 "Genel", çoğunlukla yöntem/istatistik/genel-referans künyeleridir; daha da azaltmak istenirse `references.bib`'e `keywords` eklenebilir. Sınırlılık: eşleme heuristiktir (başlık substring); tek doğru sınıf garanti etmez.

## 4. Etiket taksonomisi

`t1dm` (taban) · `embu` · `sibling` · `maternal-depression` · `measurement` · `turkiye` · `staged` (tez metnine henüz girmemiş) · `cited` (chapters'ta atıflı). `cited`/`staged`, `bib_hygiene reconcile` çıktısından türetilebilir (atıflı=cited, orphan=staged).

## 5. Eşleme kuralı (çevrimdışı, deterministik)

`scripts/util/bib_hygiene.py::_TAG_TO_SUBCOLLECTION` + `desired_scheme()`: her künye için `key.lower() + " " + keywords.lower()` içinde token aranır; tez tipi (`mastersthesis`/`phdthesis`) veya `yoktez` → daima "Türkiye / YÖK Tez"; eşleşme yoksa "Genel", etiket yoksa `["t1dm"]`. Çıktı: `key → {subcollection, tags}` (ağsız, tekrarlanabilir).

## 6. Uygulama prosedürü (çevrimdışı türet → çevrimiçi uygula)

1. **Çevrimdışı:** `python3 scripts/util/bib_hygiene.py desired-scheme > desired.json` (istenen-durum eşlemesi).
2. **Eşleme:** Zotero `9ZFDHMZA` item'ları DOI ile bib künyelerine bağlanır (yalnız Zotero'da bulunan 72 item).
3. **Dry-run:** `zotero-refs` MCP `dry_run=true` ile op listesi (oluşturulacak alt-koleksiyonlar + item→alt-koleksiyon + etiketler) önizlenir; özet gösterilir.
4. **Uygula (standing yetki):** alt-koleksiyonlar `9ZFDHMZA` altında oluşturulur; item'lar ≤20/parti eklenir/etiketlenir. Her yazma `_assert_in_scope`/`_assert_item_in_scope` scope-lock'undan geçer; scope-dışı hedef reddedilir. Anahtar basılmaz.

## 7. Geri alma

Alt-koleksiyon oluşturma ve item-koleksiyon ilişkisi Zotero'da geri alınabilir (koleksiyon silme item'ı silmez; item yalnız koleksiyondan çıkar). Etiketler item'dan kaldırılabilir. Reorg yalnız `9ZFDHMZA` topolojisini değiştirir; item içeriği/başka koleksiyon üyelikleri korunur.
