# Kaynak Doğrulama Kalıpları

Bir öğeyi açıklamadan önce kaynağını teyit etmek için kullanılan komut kalıpları.
Amaç: hiçbir açıklama hafızadan/tahminden değil, **gerçek içerik + gerçek sayı**dan.

## İçindekiler
- [1. Numara → kanonik etiket eşleme](#1-numara--kanonik-etiket-eslemesi)
- [2. Öğenin içeriğini ve caption'ı okuma](#2-ogenin-icerigini-ve-captioni-okuma)
- [3. Üreten kaynağı bulma (R modülü / CSV / metin)](#3-ureten-kaynagi-bulma)
- [4. Gerçek sayıları teyit etme](#4-gercek-sayilari-teyit-etme)
- [5. researcher alt-ajanı ne zaman](#5-researcher-alt-ajani-ne-zaman)

---

## 1. Numara → kanonik etiketleşme

Bu tezde tablolar `@tbl-apa-...`, şekiller `@fig-...` semantik etiketiyle tanımlıdır.
Kullanıcının söylediği **"Tablo 4.4" / "Şekil 3.2"** gibi numaralar render sırasına
göre **otomatik** atanır; kaynakta bu numara yazmaz. Eşleme için ilgili bölümdeki
`#| label:` sırasını say — N'inci etiket = <bölüm>.N.

```bash
# Tablolar (04_bulgular = 4.N): sıra numarası → etiket
grep -nE "^#\| label: tbl-" chapters/04_bulgular.qmd | nl -ba | \
  awk '{print "4."$1"  →  "$0}'

# Şekiller (03 = 3.N): ![...](...){#fig-...} veya #| label: fig-
grep -nE "\{#fig-|^#\| label: fig-" chapters/03_gerec_ve_yontem.qmd | nl -ba | \
  awk '{print "3."$1"  →  "$0}'
```

Not: Ön bölümler (00a-00c) ve ekler (07) ayrı numara uzayına sahip olabilir; hangi
`.qmd` dosyasının hangi bölüm numarasına denk geldiğini `thesis.qmd` include sırası
belirler. Şüphede `grep -n "include" thesis.qmd` ile sırayı doğrula.

## 2. Öğenin içeriğini ve caption'ı okuma

```bash
# Etiket bulunduktan sonra caption + üreten çağrı (label satırından 3-5 satır)
sed -n '552,557p' chapters/04_bulgular.qmd

# Öğeye atıfta bulunan tüm açıklayıcı metin (bağlamı toplar)
grep -nE "@tbl-apa-propensity-model|eğilim skoru|IPTW|ortak destek" \
  chapters/04_bulgular.qmd
```

## 3. Üreten kaynağı bulma

Caption'ın altındaki `apa_render_table("tXX_...")` / `#| label` çağrısındaki anahtar
adı, üreten R modülüne ve CSV artefaktına götürür.

```bash
# APA tablo/şekil üreten fonksiyon ve targets hedefi
grep -rnE "t04_propensity_model|propensity_model" R/ scripts/R/ _targets.R

# İlgili CSV artefaktı (outputs gitignored; ad kalıbını R modülünden oku)
grep -rnE "write.*propensity|psychval_|outputs/tables" R/15_propensity_score.R
```

Kaynak-tekilliği (AGENTS.md): sayılar R fonksiyonlarına gömülü olamaz; model/CSV
artefaktından okunur. Bir sayının nereden geldiğinden emin değilsen üreten modülü
izle, literal arama yapma.

## 4. Gerçek sayıları teyit etme

Aktaracağın her değeri metinde/CSV'de gör. Metinde geçen sayıları çek:

```bash
# Bir bölgedeki tüm sayısal değerler (ondalık-virgül dahil)
sed -n '494,510p' chapters/04_bulgular.qmd | grep -oE "[0-9]+,[0-9]+|%[0-9]+"

# Belirli bir istatistiğin geçtiği yer (α, ω, SMD, β, OR, r, p, CFI, RMSEA)
grep -nE "α = 0,|ω = 0,|SMD|CFI|RMSEA|ΔCFI" chapters/04_bulgular.qmd
```

Kural: metin ile tablo/CSV **aynı** değeri göstermeli. Çelişki görürsen açıklama
yazma; çelişkiyi kullanıcıya bildir (bu bir sayısal-bütünlük bulgusudur).

## 5. researcher alt-ajanı ne zaman

Tek `grep`/`sed` ile toplanamayacak, çok dosyaya yayılmış veya "sürecin tamamı"
türü sorularda `researcher` alt-ajanını kullan (ör. "ölçek validasyon sürecini
izah et" → yöntem + bulgular + R modülleri + Ek 7 birlikte). Görev tanımında:
- Hangi dosyaları taramasını istediğini,
- Sayısal değerleri **aynen** aktarmasını,
- Her bulguyu dosya:satır/modül adıyla belirtmesini iste.

researcher çıktısını yine de kilit sayılar için `grep`/`sed` ile spot-doğrula;
alt-ajan özeti tek doğrulama katmanı olmasın.
