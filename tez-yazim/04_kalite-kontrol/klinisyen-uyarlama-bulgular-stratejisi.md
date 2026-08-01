# Bulgular (ch04) Klinisyen-Uyarlama Stratejisi — 4 Katmanlı Sunum + Hibrit De-dup (2026-07-30)

Bulgular bölümü DOKUNULMAZ kısıtı (hiçbir sayı silinemez) ile klinisyen-yükü (istatistik/sayı
bombardımanı) arasında en gergin bölümdür. Kullanıcı onaylı Bulgular-özel yaklaşım. Register v2'nin
([[klinisyen-uyarlama-register-standardi.md]]) üstüne bu katman eklenir.

## 4 Katmanlı sunum
| Katman | İçerik | Sayı |
|---|---|---|
| **1. Manşet** | Her hipotez/analiz biriminin başında **bold klinik çıkarım** (1–3 cümle, yön + küçük/orta/güçlü). Zaten "**Özetle:**" blokları varsa korunur/standartlaştırılır. | ~0 |
| **2. Kanıt-anahtarı** | Manşeti taşıyan TEK kilit istatistik dizisi inline (etki büyüklüğü + %95 GA + p/BF). | minimum |
| **3. Tablo** | Tüm sayı-gridleri (alt-ölçek×grup matrisleri, çok-katsayı dökümleri) tabloda — tek yer. | tam |
| **4. Dipnot/teknik** | Formüller (Z=…, a4=…), kestirim-yöntemi mekaniği, model-uyum minutiae, yöntem-parametreleri → dipnot. | gizli |

## Hibrit de-duplikasyon kuralı (KULLANICI ONAYI: "Hibrit")
- **Birincil H1–H5:** headline doğrulayıcı istatistik (etki + %95 GA + p/BF) **NESİRDE KALIR** (jüri beklentisi).
- **Keşifsel/ikincil katmanlar (LPA, ağ, klinik-fayda, ileri-psikometrik, artık-ilişki, gelişimsel-diadik) + birincil içindeki büyük sub-gridler:** tabloda birebir bulunan sayı-gridleri nesirden çıkarılır; nesir **yön + "ayrıntı @tbl-…"** taşır.
- **KAYIPSIZLIK GÜVENCESİ:** bir sayı nesirden ancak (a) ilgili tablo/şekil o gridi kapsıyorsa (tbl-cap + nesrin kendi "@tbl-…" çapraz-referansıyla doğrulanır) çıkarılır; aksi hâlde nesirde kalır. Sayı kaybolmaz (tabloda + CSV izinde durur).
- **Formül/mekanik** her hâlde dipnota (silinmez, taşınır).

## Doğrulama hattı (her dalga)
1. `verify_authored_spans` — nesirde KALAN DOKUNULMAZ (headline sayı/atıf/çekince/etiket) korundu mu.
2. 4-mercek adversaryal — özellikle **DOKUNULMAZ-tamlık merceği de-dup'ta**: (a) kaldırılan grid gerçekten tabloda mı, (b) kalan headline sayılar birebir mi, (c) çekince/yön çarpıtılmadı mı.
3. Dalga sonu / bölüm sonu: `csr_numeric_trace_audit.py` (ch04) → yüksek-risk eşsiz = 0 (kalan nesir sayıları CSV-izli); `check-turkish` + `verify-citations`.

## Kapsam dışı (değişmez)
R chunk kodu, tablo/şekil üretimi, tüm istatistik DEĞERLERİ (yalnız yeri değişebilir: nesir→tablo/dipnot),
`[KEŞİFSEL]/[POST-HOC]` etiketleri, nedensellik-yok çekinceleri, ön-kayıt/triangülasyon ifadeleri.

## Klinik-çerçeve kaynağı: DETAYLI-IZAHAT-BIRLESIK.md (2026-07-30, kullanıcı işareti)
`DETAYLI-IZAHAT-BIRLESIK.md` (2842 satır) her tablo/şekli klinisyen diliyle açıklar; alt-başlıkları:
"### Bu tablo hangi soruna çözüm?" (klinik çerçeve/manşet), "### Tablo ne söylüyor? / İşe yaradı mı? —
Kanıt + büyüklük okuryazarlığı", "### Bir cümleyle" (manşet-cümle). Tablo/şekil açıklamalarını (caption +
tabloyu tanıtan nesir) ve **manşet (katman 1)** ile **kanıt-anahtarı (katman 2)** yazarken bu belge
**klinik-çerçeve/ifade kaynağı** olarak kullanılır.
**RBŞ kilidi:** İzahat yalnız *nasıl anlatılacağına* yardımcıdır; DOKUNULMAZ substans (sayı/yön/anlamlılık/
çekince) TEZDEN gelir. İzahat bir yardımcı belgedir, otorite değil — kendi drift'i olabileceğinden her
alınan çerçeve tez metni/CSV karşısında doğrulanır; izahat'tan tezde olmayan iddia/sayı AKTARILMAZ.

---
## v3 — "Klinik-Önce, İki-Bloklu Bulgu" (2026-07-30, kullanıcı: hibrit hâlâ karmaşık)
Hibrit (sayı anlatıya dokunmuş) klinisyene hâlâ ağır geldiğinden, radikal sadeleştirme: her bulgu
birimi (H1–H5, keşifsel katman) **iki görsel-ayrı bloğa** ayrılır.

**Blok 1 — "Klinik bulgu." (anlatı):** düz Türkçe; yön + büyüklük **kelimeyle** ("küçük ama tutarlı",
"fark yok"), klinik anlam, sade çekince. **Gövdede sayı ~sıfır.** Klinisyenin bulguyu anlamak için
okuyacağı TEK blok. Mevcut "**Özetle:**" blokları bunun çekirdeğidir; yorum-noktaları (aile düzeyi,
güvenilir/değil, null) buraya sayısız absorbe edilir.

**Blok 2 — "*Kanıt* —" (demarke istatistik satırı):** tek kompakt satır; headline istatistik
(etki + %95 GA + p/BF) + yöntem-künyesi (model, n, ayarlanan kovaryatlar, düzeltme) + "@tbl-…"/"@fig-…"
işaretleri. Görsel olarak ayrık (italik "*Kanıt —*" öncülü); akışta değil, isteyen okur.

**Yer kuralı:** headline istatistik *Kanıt* satırında; grid + rol-özgül/ikincil katsayılar TABLODA
(nesir yalnız işaret); formül/mekanik DİPNOTTA. Klinik anlam + çekince ANLATIDA (sayısız).
**DOKUNULMAZ korunur** — sayı silinmez, yalnız yeri: anlatı→Kanıt-satırı/tablo/dipnot (kayıpsız, tabloda doğrulı).
**Kapsam:** ch04 birincil H1–H5 + keşifsel bu modele TAŞINIR (mevcut hibrit üzerine). Doğrulama hattı aynı
(verify_authored_spans + 4-mercek + kapanış csr_numeric_trace). Nitel Tema1–4 anlatısı zaten bu ruhta →
katılımcı alıntıları DOKUNULMAZ; yalnız gerekiyorsa manşet netliği.
