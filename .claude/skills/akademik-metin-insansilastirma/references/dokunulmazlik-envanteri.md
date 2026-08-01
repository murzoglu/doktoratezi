# DOKUNULMAZLIK ENVANTERİ — neyin özü değişemez?

Bu kapının tek kırmızı çizgisi: **üslup değişir, öz değişmez.** "Öz" iki katmandır.
Sözel katman mekanik doğrulanır; anlamsal katmanın denetçisi ajandır.

---

## A. Sözel öz — 12 sınıf (mekanik: `humanize_invariant_guard.py`)

| # | Sınıf | Kapsam | Örnek | Kademe |
| --- | --- | --- | --- | --- |
| 1 | `sayi` | tüm çıplak sayılar (yıl, N, ondalık) | `0,38` · `241` · `2014` | HARD (düşme **ve** ekleme) |
| 2 | `birimli_sayi` | sayı + birim bitişikliği | `%12,4` · `7,8 yıl` · `42 mg/dL` | HARD (düşme + ekleme) |
| 3 | `istatistik` | sembol + operatör + değer | `p<0,001` · `β=0,29` · `ICC=0,41` | HARD (düşme + ekleme) |
| 4 | `aralik` | güven aralığı / aralık gösterimi | `%95 GA [0,12; 0,45]` | HARD (düşme + ekleme) |
| 5 | `atif` | atıf anahtarı | `@rohner2005` | HARD (düşme + ekleme) |
| 6 | `capraz_ref` | Quarto çapraz-referans | `@tbl-apa-h1` · `@fig-h1-forest` | HARD (düşme + ekleme) |
| 7 | `bolum_ref` | bölüm göndermesi | `§4.2.1` | HARD (düşme) |
| 8 | `etiket` | kanıt-düzeyi etiketi | `[KEŞİFSEL]` · `[POST-HOC]` | HARD (düşme) |
| 9 | `cekince` | sınırlılık/temkin imleci | "kesitsel", "nedensellik çıkarılamaz", "dikkatle yorumlan" | HARD (**düşme**) |
| 10 | `olumsuzluk` | olumsuzlama imleci | "bulunmamıştır", "anlamlı değildir" | HARD (**düşme**) |
| 11 | `kesinlik` | mutlaklık/nedensellik yükseltmesi | "kesinlikle", "kanıtlamaktadır", "neden olmaktadır" | HARD (**ekleme**) |
| 12 | `yz_beyani` | yapay zeka kullanım beyanı imleci | "büyük dil modeli", "yapay zeka desteği" | HARD (düşme) |

Ek olarak `atif_blok` (atıf bloğunun tümü: sıra, lokator, "bkz.") ve `yon`
(artış/azalış/pozitif/negatif/anlamlı) **SOFT** izlenir: yeniden ifade sırasında
meşru biçimde değişebilir, ama **her SOFT satırı gerekçelendirilir.**

### Neden ekleme de ihlaldir?

Düşen bir sayı veri kaybıdır; **eklenen** bir sayı/atıf uydurmadır (halüsinasyon).
İnsansılaştırma "daha somut görünsün" diye asla yeni değer, yeni yıl, yeni kaynak
üretmez. `0,38` → `0,4` yuvarlaması da mutasyondur: guard bunu bir düşme + bir
uydurma olarak raporlar.

### Ondalık ayraç özün parçasıdır

`0,38` → `0.38` biçimsel bir tercih değildir; Marmara sözleşmesi ondalık **virgül**
kullanır ve `tr_corpus_audit` nokta-`p`'yi blocker sayar. Guard bu kaymayı mutasyon
olarak yakalar.

### Çıkarma komutu

```bash
python3 scripts/eval/humanize_invariant_guard.py inventory chapters/<bolum>.qmd
python3 scripts/eval/humanize_invariant_guard.py inventory /tmp/pasaj.md --json   # makine
```

---

## B. Anlamsal öz — ajan kontrol listesi (mekanik yakalayamaz)

Guard PASS verse bile aşağıdakilerin **hepsi** doğrulanmadan onaya sunma. Her madde,
gerçek denetimlerde yakalanmış bir çarpıtma sınıfına karşılık gelir.

### 1. Yön ve karşılaştırma

- Hangi grup hangi gruba göre yüksek/düşük? Yeniden yazımda **kıyas ekseni** korundu mu?
- "DM grubunda kontrol grubuna göre daha yüksek" ≠ "kontrol grubunda daha düşük"
  cümlesi başka bir referans noktası kurabilir; kaynak neyi öne alıyorsa o kalır.

### 2. Kapsam ve koşul

- "… yaş ve cinsiyet kontrol edildiğinde", "yalnızca kız çocuklarında", "ergen alt
  örnekleminde" gibi koşul öbekleri cümleden **koparılamaz**.
- Koşullu bir bulgu koşulsuz cümleye dönüşürse kapsam genişlemiştir = ihlal.

### 3. Kesinlik derecesi (modality)

- Kaynaktaki kip aynen taşınır: "saptanmıştır" / "düşündürmektedir" / "olabilir" /
  "işaret etmektedir" birbirinin yerine kullanılamaz.
- Yukarı yükseltme (overclaim) HARD; aşağı indirme (underclaim) da ihlaldir —
  bulgunun gücünü düşürmek de bulguyu değiştirmektir.

### 4. Nedensellik derecesi

- İlişkisel ifade nedensel ifadeye çevrilemez: "ilişkilidir" → "neden olmaktadır"
  yasak. `csr_causal_label_audit.py` bunun repo-düzeyi bekçisidir.
- Ters yön de yasak: nedensel çerçeve kurulan (ör. IPTW/PS) bir bulgunun nedensellik
  dili gerekçesiz sulandırılamaz.

### 5. Atfetme (kim söylüyor?)

- "Rohner'e göre …" ile "Bu çalışmada …" karışamaz. Literatür iddiası bu çalışmanın
  bulgusu gibi, bu çalışmanın bulgusu literatür gibi sunulamaz.
- Bir cümlede birden çok kaynak varsa hangi iddianın hangi kaynağa ait olduğu
  korunur (atıfların cümle içi konumu anlam taşır).

### 6. Örneklem ve birim

- N, alt örneklem, analiz birimi (aile / çocuk / gözlem) korunur. "241 aile" →
  "241 katılımcı" bir sayı korunmuş gibi görünür ama **birim mutasyonudur**
  (guard `sayi` sınıfında geçer, seni yakalamaz — bu maddeyi elle kontrol et).

### 7. Zaman ve tasarım

- "Kesitsel", "izlem", "başlangıç ölçümü" gibi tasarım imleçleri korunur; zaman
  kipi bulgunun yorumunu belirler.

### 8. Sıra ve öncelik

- Bulgu sırası bir yorum taşır (birincil → ikincil). Yeniden sıralama meşru olabilir,
  ama **yereldir ve gerekçelidir**; birincil bulgu ikincilin arkasına atılamaz.

### 9. Tablo/şekil sözleşmesi

- "@tbl-x'te sunulmuştur" ifadesi taşınıyorsa değerin o tabloda **gerçekten var
  olduğu** doğrulanır. Metinden düşürülen bir değer tabloda yoksa veri kaybıdır.

### 10. Çekincenin yeri

- Çekince cümlesi korunmakla kalmaz, **bağlandığı bulgunun yanında** kalır.
  Sınırlılığı paragraf sonundan bölüm sonuna sürüklemek, bulguyu çekincesiz okutur.

---

## C. Hızlı öz-denetim soruları (onaya sunmadan önce)

1. Aday metni tek başına okuyan biri, kaynak metni okuyan biriyle **aynı** bilimsel
   sonuca mı varır?
2. Kaynakta olmayan hangi bilgi eklendi? (Yanıt "hiçbiri" olmalı.)
3. Kaynakta olan hangi bilgi kayboldu? (Yanıt "hiçbiri" olmalı.)
4. Hangi cümlede kesinlik derecesi değişti? (Yanıt "hiçbirinde" olmalı.)
5. Bir hakem "bu cümle kaynağı çarpıtıyor" derse hangi cümleyi gösterir?
   O cümleyi şimdi düzelt.
