# Tam Metin Erişim Kaskadı

Bu belge, tez yazımında dış kaynakların tam metin erişimini Evidentia kanıt
sürecine bağlayan operasyon kuralıdır. Amaç tam metni bulmak değil, her
citation adayını bibliyografik kimlik, yasal/kurumsal erişim, Zotero kaydı,
BibTeX anahtarı ve claim-level ledger iziyle kapatmaktır.

## Temel İlke

Tam metin erişimi Evidentia D4 aşamasının parçasıdır. Dış kaynak şu sıra
tamamlanmadan tez metnine final citation olarak girmez:

1. Evidentia ile DOI/PMID/PMCID/OpenAlex/YÖK kimliği doğrulanır.
2. OpenAthens veya eşdeğer kurumsal yayıncı erişimi denenir.
3. Kurumsal erişim başarısızsa Anna's Library/annas-reader denenir.
4. Anna başarısızsa PubMed Central, Europe PMC, yayıncı OA sayfası, kurumsal
   repository, author accepted manuscript, interlibrary loan veya yazar talebi
   gibi diğer kanıtlı rotalara geçilir.
5. Erişilen tam metin Zotero'ya item, full-text URL, dosya attachment veya
   erişim notu olarak bağlanır.
6. `references/references.bib` ve
   `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` aynı kayıtla
   mutabıklaştırılır.

## T0 Preflight

Her tam metin oturumunda:

- `.claude/evidentia.local.md` ve `t1dm-tez-rehberi` dış kanıt köprüsü okunur.
- `python3 scripts/util/zotero_env_bridge.py status --json` ile Zotero Web API
  yetkileri doğrulanır.
- OpenAthens için yalnız ortam değişkenlerinin varlığı doğrulanır:
  `OPENATHENS_USERNAME`, `OPENATHENS_PASSWORD`, `OPENATHENS_INSTITUTION`,
  `OPENATHENS_LOGIN_URL`, `MILLET_KUTUPHANESI_DATABASES_URL`.
- Credential değerleri, `.env` içeriği, ham veri ve transcript hiçbir çıktıya,
  ledger'a veya harici araca yazılmaz.

## T1 OpenAthens / Kurumsal Yayıncı Kapısı

OpenAthens, bu repo için claim-critical tam metinde ilk erişim kapısıdır.

1. Kaynak Evidentia ile doğrulanır: DOI/PMID, yayıncı, dergi, yıl, sayfa ve
   çalışma tipi.
2. Millet Kütüphanesi veritabanı listesi veya yayıncı OpenAthens redirector
   rotası kullanılır.
3. Playwright yalnız oturum açma, resmi yayıncı sayfası ve görünür tam metin
   doğrulaması için kullanılır.
4. Başarılı sayılan kanıtlar:
   - resmi yayıncı HTML tam metni,
   - resmi yayıncı PDF'i,
   - kurumsal platformdaki lisanslı full text,
   - Zotero'ya eklenen URL, snapshot veya dosya attachment.
5. Yayıncı PDF endpoint'i bot/Cloudflare/oturum sınırına takılırsa, resmi HTML
   tam metin görüldüyse `full-text-ok` kabul edilebilir; Zotero notunda dosyanın
   yayıncı PDF'i değil HTML snapshot olduğu açık yazılır.
6. **Wiley Online Library (Cloudflare):** `onlinelibrary.wiley.com` kaynakları
   Cloudflare bot doğrulamasıyla korunur; doğrudan Playwright navigasyonu
   "Just a moment... / Performing security verification" duvarına takılır. Bu
   yayıncı için tam metin **OpenAthens / Millet Kütüphanesi kurumsal oturumu
   Playwright ile** açılır (`my.openathens.net` veya proxy); Cloudflare
   kimliklendirilmiş oturum/IP ile geçilir. **OpenAthens parolası ve hiçbir
   credential/`.env` değeri tool-çağrısına veya çıktıya yazılmaz** (Playwright
   `browser_fill_form` value alanı dahil). Otomatik oturum güvenle kurulamazsa
   kullanıcının interaktif tarayıcı oturumu kullanılır veya OA eşdeğeri (ör.
   PMC) tercih edilir. Örnek engel: DOI `10.1111/jep.14190` (J Eval Clin Pract).

## T2 Anna's Library / annas-reader Kapısı

OpenAthens işe yaramazsa veya ilgili yayıncı kurum erişiminde yoksa Anna
ikinci ana kapıdır.

1. DOI/PMID/başlık ile arama yapılır.
2. Crossref/yayıncı metadata uyumu kontrol edilir.
3. `read_article`, `get_document_info` veya `search_in_document` ile hedefli
   claim doğrulanır.
4. Yanlış fuzzy match, metadata uyuşmazlığı veya tam metin 404 ise kaynak
   `full-text-ok` sayılmaz; fallback rotasına geçilir.
5. Telifli metin uzun alıntılanmaz, tam metin bağlama dökülmez, yalnız claim
   için gerekli bölüm/sayfa/tablo lokatörü ve kısa çıkarım ledger'a yazılır.

## T3 Açık Erişim ve Diğer Rotalar

OpenAthens ve Anna başarısızsa sırasıyla:

1. PubMed/EPMC: PMCID, `isOpenAccess`, Europe PMC full text.
2. OpenAlex/Unpaywall: `oa_status`, repository full text, license.
3. Paper Search/Semantic Scholar: PDF linkleri yalnız kaynak/provenance
   doğrulanırsa kullanılır.
4. Yayıncı sayfası: HTML/PDF, supplementary material, accepted manuscript.
5. Kurumsal repository veya author accepted manuscript.
6. ResearchGate/yazar talebi veya kütüphane kaynak sağlama yolu.

Bu rotalardan hiçbiri claim-critical tam metin sağlamazsa kaynak
`full-text-exception` kalır ve final citation olarak kullanılmaz.

## Zotero Kapanış Kapısı

Zotero kapanışı kullanıcı onayıyla yapılır. Bu oturum için onay verilmişse
repo-local köprü kullanılır:

```bash
python3 scripts/util/zotero_env_bridge.py import-doi <DOI> \
  --bibtex-key <citation_key> \
  --fulltext-url '<publisher_or_openathens_url>' \
  --fulltext-url-title '<route title>' \
  --attachment-file <local_fulltext_or_snapshot.pdf> \
  --attachment-title '<attachment title>' \
  --note '<short provenance note>' \
  --json
```

Kapanışta şu alanlar raporlanır:

- Zotero item key,
- Zotero child attachment key,
- Zotero note key,
- BibTeX citation key,
- `references/references.bib` ekleme durumu,
- ledger durum güncellemesi.

Zotero Desktop local API çalışıyorsa attachment/full-text index kontrolü ek
kanıt olarak kullanılabilir; Web API yeterliyse Desktop zorunlu değildir.

## Ledger Durumları

- `candidate`: kimlik doğrulandı, tam metin henüz açık değil.
- `full-text-ok`: OpenAthens, Anna, PMC/OA veya eşdeğer resmi tam metin kapısı
  başarıyla geçti.
- `zotero-ok`: Zotero item key, full-text URL/attachment veya note ve BibTeX
  key ledger ile mutabık.
- `full-text-exception`: tam metne erişilemedi; final citation için bekletilir
  veya kaynak dışlanır.
- `cite-ok`: full-text, Zotero/BibTeX ve iki AI-reliability kapısı geçti.

## Yasaklar

- `.env`, credential, token, oturum cookie veya ham veri çıktısı yazmak.
- Ham klinik CSV, ham transkript veya satır-düzeyi veriyi tam metin araçlarına
  göndermek.
- Telifli tam metni uzun pasajlar halinde çoğaltmak.
- Tam metni görülmeyen kaynaktan sayısal endpoint veya yöntem ayrıntısı
  uydurmak.
- SciSpace, ResearchGate veya genel web PDF aynasını OpenAthens/Anna/PMC/OA
  provenance olmadan tek başına `full-text-ok` saymak.
