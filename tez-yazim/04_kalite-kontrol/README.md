# 04_kalite-kontrol — Kalite Kontrol / Sertifikasyon Katmanı

Bu klasör tez yazımının **kalite kontrol katmanı**dır: bir `chapters/*.qmd`
bölümünün final kabul edilmeden önce geçmesi gereken **Kapı 0–5** sertifikasyon
sürecinin **tek kanonik yeri**. Tek-otorite ilkesi geçerlidir (bkz.
`00_kaynak-kurallari/README.md`).

> **Merkez otorite:** `bolum-finalizasyon-sertifikasyon-playbook.md` (Kapı 0–5,
> durumlar, artefakt, AI-reliability katman sınırı, bloklayıcı sözlüğü, nihai
> karar). Diğer dosyalar ya bir **Kapı'nın operasyonel checklist'i**, ya
> **doldurulacak sertifika iskeleti**, ya **makine raporu**, ya **doldurulmuş
> sertifika** (audit trail) olarak buna bağlıdır ve kural yeniden tanımlamaz.

## Tek-Otorite Haritası

| Dosya | Otorite alanı | Diğer dosyalarla ilişki |
|---|---|---|
| `bolum-finalizasyon-sertifikasyon-playbook.md` | **Master sertifikasyon** (kanonik): Kapı 0–5 süreci, sertifikasyon durumları, artefakt, AI-reliability katman sınırı, nihai karar kuralı. | Bölüm kapanışının tek otoritesi. Checklistler ve sertifika iskeleti buna bağlı. |
| `tez-kontrol-checklisti.md` | **Kapsamlı kontrol checklisti** (8 eksen · 26 madde, A bölüm-düzeyi + B tez-düzeyi + kapsama matrisi). Her madde bir araca/mekanizmaya bağlı; otomasyon `scripts/util/tez_checklist_verify.py`. | Operasyonel checklistleri (format/kanıt-gizlilik/ai-mcp/Türkçe) **birleştiren** insan-okunur yansıma; kural tanımlamaz, ID'ler script kaydına birebir eşleşir (`--audit-doc`). |
| `bolum-finalizasyon-sertifikasi-sablonu.md` | **Sertifika iskeleti** (fill-in): Kapı 0–5 doldurulabilir form. | Playbook'un doldurulacak hâli; `sertifikalar/<bölüm>-sertifika-YYYY-MM-DD.md`'ye kopyalanır. |
| `format-kontrol-listesi.md` | **Kapı 3** format operasyonel checklist. | marmara §12'nin bölüm-kapanışı operasyonel örneği; kural marmara'da. |
| `kanit-ve-gizlilik-kontrol-listesi.md` | **Kapı 0/1/2** kanıt + gizlilik operasyonel checklist. | Veri sınırı → talimatname §2; kanıt → `02` ledger. |
| `ai-mcp-kullanim-kontrol-listesi.md` | **Kapı 5** + araç kullanımı operasyonel checklist. | Araç otoritesi → `01_mimari/yetkinlik-ve-arac-mimarisi.md`; süreç → talimatname. |
| `turkce-bilimsel-yazim-denetimi.md` | **Kapı 4** sci-audit axis G (kanonik kullanım) — **denetim tarafı**. | Türkçe imla/yazım denetiminin tek yeri (plugin bundled). |
| `insan-turkcesi-retorik-playbook.md` | **Kapı 4** insan-Türkçesi retorik üretimi — **üretim tarafı**. | Denetçinin yakaladığı yapaylığı baştan önler; register otoritesi marmara §1–§5. |

## Alt klasörler ve tarihli kanıt

| Yol | İçerik | Not |
|---|---|---|
| `raporlar/` | Makine-okunur sci-audit çıktıları (axis G + axes A–F). | `raporlar/README.md`. |
| `sertifikalar/` | Doldurulmuş, tarihli bölüm sertifikaları. | **Audit trail — silinmez**, yalnız eklenir. `sertifikalar/README.md`. |
| `yazim-oncesi-preflight-2026-06-30.md` | Tarihli başlangıç preflight kanıtı. | Audit trail — dokunulmaz. |

## Kapı → checklist → kanonik kural haritası

| Kapı | Ne denetler | Operasyonel checklist | Kanonik kural otoritesi |
|---|---|---|---|
| Kapı 0 | Kapsam ve hassasiyet/gizlilik sınırı | `kanit-ve-gizlilik-kontrol-listesi.md` (Gizlilik) | `talimatname-claude-code.md` §2 + `06_kritik-kaynaklar` manifesti |
| Kapı 1 | Derin literatür ve künye evreni | `kanit-ve-gizlilik-kontrol-listesi.md` (Kanıt) | `01_mimari/evidentia-entegrasyon-cercevesi.md` §1–5 |
| Kapı 2 | Tam metin, Zotero ve bağlam | (playbook Kapı 2) | `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md` + `02` ledger |
| Kapı 3 | Bölüm metni, kılavuz ve iç tutarlılık | `format-kontrol-listesi.md` | `marmara-tez-formati-talimatnamesi.md` §12 (+ §1–§5, §8) |
| Kapı 4 | Türkçe imla, anlam akışı, mantık | `turkce-bilimsel-yazim-denetimi.md` | sci-audit **axis G** |
| Kapı 5 | AI-reliability, render, repo | `ai-mcp-kullanim-kontrol-listesi.md` | sci-audit **axes A–F** + repo ai-audit + `talimatname` §6 |

> **Birleşik otomasyon:** Yukarıdaki tüm kapıların otomatik-doğrulanabilir
> maddeleri `tez-kontrol-checklisti.md` altında 26 ID'ye bölünmüş ve
> `scripts/util/tez_checklist_verify.py` orkestratörüne bağlıdır. Tek komutla
> tam tez/bölüm denetimi: `python3 scripts/util/tez_checklist_verify.py
> [--fast|--section K3|--chapter <yol>]`. Belge↔script senkronu: `--audit-doc`.

## AI-Reliability katman sınırı (çakışmaz)

**Manüskript metni adli denetimi** (referans/claim/istatistik/halüsinasyon/
kılavuz/AI-şeffaflık/Türkçe imla) **yalnız `sci-audit`** axes A–G'dedir;
**KVKK/ham veri/quote-parity/kanonik kilit** **yalnız repo ai-audit**
plugin'lerindedir (`doktoratezi-ai-audit` + nitel `t1dm-qual-ai-audit`). İki
katman çakışmaz; tam açılım `bolum-finalizasyon-sertifikasyon-playbook.md`
"AI-Reliability Katman Sınırı" bölümündedir.

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman → (2) resmi `docs/tez-kilavuz/` → (3)
`00_kaynak-kurallari` kanonik kural (biçim/süreç) → (4) bu klasördeki playbook
→ (5) operasyonel checklist. Bir bölüm yalnız sertifikada **Kapı 0–5 PASS +
`certified-final` + açık uygulama onayı** ile final kabul edilir; aksi halde en
fazla `provisional-pass` / `blocked`.

## Duplikasyon önleme kuralı

Operasyonel checklistler **kural tanımlamaz**; ilgili kanonik otoriteye (marmara
§12, talimatname §2, yetkinlik matrisi, sci-audit axis G) pointer verir. Yeni
bir kapı kuralı önce playbook'a; yeni bir biçim kuralı önce marmara §12'ye
yazılır (bkz. 2026-07-06 rafinasyonu: üç operasyonel checklist Kapı ve kanonik
otoriteye bağlandı; `format-kontrol-listesi` marmara §12'nin operasyonel örneği
olarak işaretlendi; repo-local `tr_sciaudit` kopyası silinip sci-audit axis G
tek otorite yapıldı).
