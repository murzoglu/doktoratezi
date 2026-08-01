# Bulgular Zenginleştirme Eşgüdüm Playbook'u

Sürüm: 1.0 · 2026-07-25

> **Konum:** Bu playbook, Bulgular (ch04) bölümünde birlikte çalışan iki kardeş
> kapının — `/anlatim-zenginligi` (nesir) ve `/veri-gosterimi-zenginligi`
> (veri-gösterim) — **eşgüdüm sırasını, sınır sözleşmesini ve devir
> protokolünü** tanımlar. Komut tanımları `.claude/commands/`'tadır; bu belge
> onları yeniden tanımlamaz, **birlikte nasıl işletileceğini** verir. Kanonik
> kural otoritesi `AGENTS.md` "Sayısal Bütünlük Kaideleri" ve
> `tez-yazim/00_kaynak-kurallari/`'dır.

## Neden iki ayrı kapı

Bulgular bölümünün kalitesi iki bağımsız eksende yaşar:

1. **Nesir kalitesi** — anlatım akışı, terim izahı, okuyucu bağlamı, atıflı
   literatür karşılaştırması. Sahibi: `/anlatim-zenginligi`.
2. **Veri-gösterim kalitesi** — R çıktısı ↔ metin mutabakatı, figür/tablo
   veri-tutarlılığı + estetik/Türkçe/tasarım, eksik ama yararlı yeni görsel,
   başlık/altyazı netliği, istatistik betim açıklığı. Sahibi:
   `/veri-gosterimi-zenginligi`.

İkisi tek komuta sıkıştırılırsa kapsam bulanır ve **kanıt-değeri koruması**
zayıflar. Ayrık tutmak, her kapının kendi DOKUNULMAZ bölgesini net savunmasını
sağlar.

## Sınır sözleşmesi (tek tabloda)

| Öğe | `/anlatim-zenginligi` | `/veri-gosterimi-zenginligi` |
|---|---|---|
| Düzenlediği bölge | Düzyazı anlatım + referans | Figür/tablo/R-çıktı + `tbl-cap`/`fig-cap` + betim cümlesi |
| Sayı/istatistik | **Dokunmaz** (aynen korur) | **Dokunmaz** (yalnız kaynağa hizalar; asla değiştirmez) |
| Figür/tablo | **Dokunmaz** | Sunum katmanını düzenler (etiket/renk/düzen/altyazı) |
| Bulgunun yönü/anlamlılığı | **Dokunmaz** | **Dokunmaz** |
| Yeni içerik | Atıflı literatür bağlamı (ayrı, `/referans-kapisi`'ndan) | Var olan artefakttan yeni görsel/tablo (yeni sayı YOK) |
| Betim cümlesi | Anlatım akışı + literatür konumlama | Metrik tanımı izahı + gösterim netliği (yorum YOK) |

**Ortak anayasa (ikisi de):** kanıt-değeri mutasyonu yasak; kaynak-tekilliği
(literal gömme yok); uydurma sayı/referans yok; sci-audit HARD atlanamaz;
ondalık virgül ve token'lar aynen; KVKK — dış gateway'e yalnız literatür/aggregate.

### Betim cümlesi çakışması — kim sahip?

Tek gri bölge, bir bulguyu betimleyen düzyazı cümlesidir; ikisi de dokunabilir.
Kural:
- **Cümlenin akışı, geçişi, literatür bağlamı** → `/anlatim-zenginligi`.
- **Cümlenin gösterdiği sayının doğruluğu, metrik tanımının izahı, figüre/tabloya
  gönderme netliği** → `/veri-gosterimi-zenginligi`.
- İkisi aynı cümleyi hedeflerse **veri-gösterimi önce** çalışır (sayı/gösterim
  doğru olmadan anlatım zenginleştirmenin anlamı yoktur), sonra anlatım.

## Eşgüdüm sırası (kanonik akış)

Bir Bulgular pasajı/alt-bölümü için önerilen sıra:

```
0. /tez-oturum "BULGULAR — <alt-bölüm>"        (bağlam + kaynak önceliği sabitle)
1. /veri-gosterimi-zenginligi <@tbl-*/@fig-*>  (önce gösterim doğru/tutarlı/net olsun)
      ├─ Eksen 1: R çıktısı ↔ metin mutabakatı (numeric-trace + literal-audit)
      ├─ Eksen 2: veri-tutarlılık + estetik/Türkçe + yeni görsel + altyazı
      └─ Eksen 3: istatistik betim netliği (yorumsuz)
      → onay → Edit → tar_make() + figür export
2. /anlatim-zenginligi <aynı pasaj>            (gösterim sabitken nesri zenginleştir)
      → onay → Edit
3. /bolum-sertifika chapters/04_bulgular.qmd   (Kapı 0–5; alt-bölüm veya bölüm kapanışı)
4. /tez-dogrulama                              (bölüm bütünü kapanıyorsa)
```

**Neden gösterim önce:** `/anlatim-zenginligi` sayıyı/figürü DOKUNULMAZ kabul
eder; bu nedenle gösterim katmanı (sayı-metin mutabakatı, altyazı, betim) önce
sabitlenmelidir. Aksi hâlde anlatım, sonradan düzeltilecek bir sayının etrafına
örülür ve yeniden iş doğar.

## Ortak kapı seti (ikisinin de geçtiği)

| Kademe | Araç | Anlatım | Veri-gösterim |
|---|---|---|---|
| HARD | `csr_numeric_trace_audit.py` (ch04, K5-NUM-03) | sayıya dokunmadığını doğrular | sayı↔CSV izini birincil sahiplenir |
| HARD | `r_generator_literal_audit.py` (K5-LIT-01) | — | R üretici literal = 0 |
| HARD | `targets_file_tracking_audit.py` (K5-TRK-01) | — | figür/tablo kaynağı file-izli |
| HARD | `/sci-audit:check-turkish --strictness certification` | nesir imla | altyazı/etiket imla |
| HARD | `/sci-audit:check-stats` | — | betim ↔ tablo tutarlılığı |
| SOFT | `galileo_judge` | nesir faithfulness/overclaim | altyazı/betim faithfulness/overclaim |
| advisory | `galileo_coherence` | paragraf akışı | figür↔metin↔tablo zinciri |

Master checklist ID eşlemesi:
`tez-yazim/04_kalite-kontrol/tez-kontrol-checklisti.md` (K3-FIG/TBL-01,
K5-NUM-03, K5-LIT-01, K5-TRK-01, K4-TRG-01). Otomasyon:
`scripts/util/tez_checklist_verify.py`.

## Devir kararları (hangi komut hangi işe)

| Görev | Doğru kapı |
|---|---|
| Metin bir tablo değerini yanlış aktarıyor | `/veri-gosterimi-zenginligi` (kaynağa hizala) |
| Bir figürün ekseni İngilizce/taşıyor | `/veri-gosterimi-zenginligi` (labs Türkçe/düzen) |
| Altyazı ne-gösterildiğini anlatmıyor | `/veri-gosterimi-zenginligi` (fig-cap/tbl-cap) |
| Bir bulgu görselleştirilmemiş ama artefaktta var | `/veri-gosterimi-zenginligi` (yeni görsel ADAY) |
| Metrik okuyucuya izah edilmeli (yorumsuz) | `/veri-gosterimi-zenginligi` (betim netliği) |
| Paragraf akışı kopuk / geçiş şablon | `/anlatim-zenginligi` |
| Bulguyu literatürle konumlama | `/anlatim-zenginligi` |
| Yeni atıf gerek | `/referans-kapisi` (7-adım) |
| Yeni sayı/analiz gerek | **İkisi de değil** — pipeline (`_targets.R` + R/) |

## Bağlayıcı (çiğnenmez)

- **Kanıt değeri ikisinde de DOKUNULMAZ.** Fark yalnız düzenlenen katmandır
  (nesir vs. gösterim); ne sayı, ne yön, ne anlamlılık değişir.
- **Gösterim önce, anlatım sonra.** Aynı pasajda ikisi çalışacaksa sıra sabittir.
- **Her iki kapı da onaydan önce denetlenir;** sci-audit HARD hiçbir durumda
  atlanmaz; onaysız Edit/commit yok.
- **Yeni görsel/tablo yalnız var olan artefakt değerinden** türetilir; yeni
  sayı/analiz üretmez; file-tracking'e bağlanır.
- **KVKK:** dış gateway'e yalnız literatür terimi + aggregate altyazı; ham/
  katılımcı/aile-düzeyi veri asla.
