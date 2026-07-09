# 01_mimari — Mimari Katmanı

Bu klasör tez yazımının **mimari katmanı**dır: yürütme planı, araç/yetkinlik
seçimi, dış-kanıt hattı ve iki-repo yazım modelinin **tek kanonik yeri**.
Tek-otorite ilkesi geçerlidir — bir karar yalnız bir dosyada tanımlanır; diğer
dosyalar onu **yeniden yazmaz, işaret eder**. Duplikasyon bu klasörde policy
ihlalidir (bkz. `00_kaynak-kurallari/README.md`).

Ayrım: **`00_kaynak-kurallari`** *ne yazılacağının* kaynak-otorite katmanı
(biçim, süreç, tam-metin erişimi); **`01_mimari`** *nasıl yürütüleceğinin*
mimari katmanı (plan, araç, dış-kanıt, iki-repo). Kural çakışmasında biçim/süreç
kararı daima 00'a devredilir.

## Tek-Otorite Haritası

| Dosya | Otorite alanı | Diğer dosyalarla ilişki |
|---|---|---|
| `tez-yazim-ana-plani.md` | **Uçtan uca yürütme planı** (kanonik): Faz 0–10 sırası, dosya/sorumluluk haritası, iş paketleri, gap register, self-review. | Yürütme sırasının tek kaynağı. Araç/oturum/referans detayını aşağıdaki otoritelere **devreder**, tekrar etmez. |
| `yetkinlik-ve-arac-mimarisi.md` | **Araç/yetkinlik mimarisi** (kanonik): L0–L4 kaynak katmanları, tool gate, MCP/skill/plugin seçim matrisi, çıkış kriterleri. | Tüm tool/MCP/skill/plugin seçiminin tek kaynağı. Oturum ritüelini `00`'a devreder. |
| `evidentia-entegrasyon-cercevesi.md` | **Dış-kanıt mimarisi** (kanonik): evidentia D0–D6 kaskadı, psikososyal kapsam kapısı, giriş noktaları, kanıt paketi. | Dış literatür/citation hattının tek kaynağı (`t1dm-tez-rehberi` çerçevesi). Tam-metin ve ledger'ı `00`/`02`'ye devreder. |
| `iki-repo-entegrasyon-plani.md` | **İki-repo entegrasyon modeli** (kanonik): resmi bölüm ↔ nicel/nitel kaynak eşlemesi, repo-düzeyi gizlilik sınırı. | Cross-repo yazım modelinin tek kaynağı. Joint display alanlarını `05`'e devreder. |

## Mimari katmanı dışı bağlı omurga (devredilen otoriteler)

| Konu | Kanonik otorite | Katman |
|---|---|---|
| Biçim: sayfa/başlık/sayısal yazım, tablo-şekil, atıf, AMA-11, bölüm sırası | `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` | 00 |
| Süreç: oturum ritüeli, veri sınırı (KVKK), referans kapısı sırası, sertifikasyon, doğrulama paketi | `00_kaynak-kurallari/talimatname-claude-code.md` | 00 |
| Tam metin erişimi: T0–T3 kaskadı, OpenAthens/Anna's/PMC, Zotero kapanışı | `00_kaynak-kurallari/tam-metin-erisim-kaskadi.md` | 00 |
| Referans denetim ledger: satır şeması + durum makinesi (candidate → cite-ok) | `02_kanit-haritalari/referans-denetim-ledgeri.md` | 02 |
| Joint display alanları/ilkesi + nitel kol çıktı çerçevesi | `05_entegrasyon/nitel-nicel-joint-display-plan.md` + `05_entegrasyon/nitel-cikti-cercevesi.md` | 05 |
| Bölüm finalizasyon sertifikasyonu (Kapı 0–5) | `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | 04 |
| AI-reliability (manüskript adli denetim + Türkçe imla) | `sci-audit@cureonics-marketplace` axes A–G | plugin |

## Okuma sırası (yazım oturumu)

1. **Oturum ritüeli** → `00_kaynak-kurallari/talimatname-claude-code.md` §1 (`/tez-oturum`).
2. **Yürütme fazı** → `tez-yazim-ana-plani.md` (bölümün hangi faza düştüğü).
3. **Araç/MCP seçimi** → `yetkinlik-ve-arac-mimarisi.md` (tool gate + matris).
4. **Dış literatür gerekiyorsa** → `evidentia-entegrasyon-cercevesi.md`.
5. **Karma/iki-repo kesim ise** → `iki-repo-entegrasyon-plani.md` + `05_entegrasyon/`.

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman açık talimatı → (2) resmi `docs/tez-kilavuz/`
→ (3) `00_kaynak-kurallari` kanonik otorite (biçim/süreç) → (4) bu klasördeki
mimari otorite → (5) repo içi eski notlar. Analiz/veri/hipotez kararında repo
kanıtı (`_targets.R`, testler, protokol, CSR) üstündür; bu klasör yürütme,
araç ve entegrasyon **mimarisi** otoritesidir, biçim/analiz otoritesi değildir.

## Duplikasyon önleme kuralı

Yeni bir mimari karar eklenirken: önce yukarıdaki haritadan **hangi dosyanın
otoritesi** olduğu belirlenir; karar yalnız oraya yazılır; gerekiyorsa diğer
dosyalara **pointer** eklenir. Aynı içeriğin (araç matrisi, oturum ritüeli,
referans kapısı, ledger şeması) iki dosyada tam metniyle bulunması rafine
edilir (bkz. 2026-07-06 rafinasyonu: `tez-yazim-ana-plani.md` §2 araç/oturum/
referans detayı pointer'a indirildi; araç matrisi tek otoriteye —
`yetkinlik-ve-arac-mimarisi.md` — toplandı).
