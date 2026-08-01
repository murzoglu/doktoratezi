# Render Bağımlılıkları ve Bilinen Kısıtlar

**Tarih:** 2026-07-13
**Kapsam:** Quarto render hattı — tam tez (`thesis.qmd`) + bölüm-izole render + DOCX/PDF çıktı

---

## 1. Bölüm-izole render yol çözümü — ÇÖZÜLDÜ

**Belirti (eski):** `quarto render chapters/04_bulgular.qmd` tek başına koşturulduğunda
çalışma dizini bölüm klasörü olduğundan, kök-göreli `outputs/tables/apa_*.csv` ve
`docs/assets/figures/…` yolları çözülemiyor; `apa_read_table()` CSV'yi açamadığı için
render duruyordu. Tam üretim yolu `quarto render thesis.qmd` (çalışma dizini = proje
kökü) etkilenmiyordu; sorun yalnız bölüm-izole sertifikasyon render'ındaydı.

**Çözüm (iki katman):**
1. `_quarto.yml → project: execute-dir: project` — Quarto çalışma dizinini daima proje
   köküne sabitler; hem tam tez hem bölüm-izole render'da tablo + figür göreli yolları
   tutarlı çözülür.
2. `chapters/04_bulgular.qmd` `apa_read_table()` yardımcısı **root-aware** yapıldı:
   `_quarto.yml`'yi yukarı doğru arayarak proje kökünü cwd'den bağımsız çözer (etkileşimli
   / RStudio koşumu için ikinci güvence).

**Doğrulama:** root-resolver, cwd = `chapters/` iken proje kökünü (`T1DM-Tez`) doğru
buluyor; `quarto render chapters/04_bulgular.qmd` artık tablo + figür yollarını köke
göre çözer.

---

## 2. DOCX / PDF içinde SVG rasterizasyonu — ÇÖZÜLDÜ (build bağımlılığı: librsvg2-bin)

**Karar & uygulama (2026-07-13):** Seçenek (A) uygulandı — `librsvg2-bin` (rsvg-convert
2.58.0) bu render ortamına kuruldu ve doğrulandı (örnek SVG → PNG rasterizasyonu
başarılı). Quarto artık DOCX/PDF üretiminde SVG'leri otomatik rasterize eder.

> **Build bağımlılığı uyarısı:** apt paketleri depoda tutulmaz. `librsvg2-bin`, tezin
> DOCX/PDF'e render edildiği **her ortamda** kurulu olmalıdır:
> `sudo apt-get install -y librsvg2-bin`. HTML çıktısı bu bağımlılığa ihtiyaç duymaz.

### Arka plan (belirti ve alternatif)

**Belirti:** `quarto render thesis.qmd` HTML + DOCX üretir; ancak `rsvg-convert`
(librsvg) kurulu olmadığından 33+ SVG için rasterizasyon uyarısı verir. DOCX içine SVG
medya dosyaları gömülür (figürler tümüyle düşmez), fakat Word/PDF downstream dönüşüm
hattında uyumluluk riski kalır. HTML çıktısı SVG'yi doğal (native) render ettiğinden
etkilenmez.

**Ortam durumu (2026-07-13):** `rsvg-convert`, `inkscape`, `cairosvg` — hiçbiri kurulu
değil (70 SVG / 0 PNG eşlenik). Toplam SVG kaynağı: `docs/assets/figures/carbon/`.
SVG-yoğun bölge Bulgular'dır (figür kümeleri: `04_bulgular.qmd` 131–139, 373–375,
417–520, 605–607).

**İki seçenek (kullanıcı/ortam kararı — bu depoda uygulanmadı):**
- **(A) librsvg kur:** `sudo apt-get install -y librsvg2-bin` → Quarto DOCX/PDF üretiminde
  SVG'leri otomatik rasterize eder. En düşük repo değişikliği; nihai Word teslimi için
  önerilen yol.
- **(B) PNG/PDF eşlenik üret:** figürleri ön-render adımında PNG (veya PDF) olarak da
  üretip format-koşullu görsel yolu kullan (HTML→SVG, DOCX/PDF→PNG). Repo-içi ama daha
  fazla bakım yükü (70 dosya + koşullu include).

**Neden burada uygulanmadı:** sistem paketi kurulumu ve 70 raster dosyanın depoya
eklenmesi geri-alınması güç, ortam-düzeyi kararlardır; talimatname (rule 14: istenmedikçe
global kurulum yapılmaz) gereği kullanıcı onayına bırakılmıştır. Nihai Word/PDF teslimi
öncesi (A) veya (B) uygulanmalıdır.
