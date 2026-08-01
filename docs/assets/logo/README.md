# Marmara Üniversitesi logosu (tez kapağı)

| Dosya | Rol |
|---|---|
| `marmara-universitesi-logo.png` | Tez dış/iç kapağında kullanılan mavi Marmara Üniversitesi arma logosu (Marmara Tez Yazım Kılavuzu 2025 §2.1: “kapağın üst orta bölümünde 2×2 cm boyutlarında Marmara Üniversitesi logosu mavi renkli olarak bulunmalıdır”). |

## Kaynak ve üretim

Logo, resmi tez şablonunun (`docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx`)
kapak sayfasına gömülü görselinden (`word/media/image1.png`, 378×378 px)
çıkarılmıştır. Şablonun kapak paragrafı bu görseli kendi kırpma kutusuyla
kullanır:

```xml
<a:srcRect l="26722" t="9909" r="26810" b="43732"/>
```

Yani gömülü PNG hem armayı hem altındaki “MARMARA ÜNİVERSİTESİ” yazısını
içerir; şablon `srcRect` ile yalnız yuvarlak armayı gösterir. Depodaki varlık
aynı kırpma uygulanıp kare tuvale ortalanarak ve 472×472 px'e (2 cm @ 600 dpi)
yükseltilerek üretilmiştir; böylece kapakta ek kırpma parametresi gerekmez.

Yeniden üretim (repo kökünden):

```bash
python3 - <<'PY'
from PIL import Image
import zipfile, io
z = zipfile.ZipFile("docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx")
im = Image.open(io.BytesIO(z.read('word/media/image1.png'))).convert('RGBA')
W, H = im.size
l, t, r, b = 26722/100000, 9909/100000, 26810/100000, 43732/100000
crop = im.crop((round(l*W), round(t*H), round(W - r*W), round(H - b*H)))
side = max(crop.size)
canvas = Image.new('RGBA', (side, side), (255, 255, 255, 0))
canvas.paste(crop, ((side-crop.size[0])//2, (side-crop.size[1])//2), crop)
canvas.resize((472, 472), Image.LANCZOS).save(
    'docs/assets/logo/marmara-universitesi-logo.png', dpi=(600, 600))
PY
```

## Kullanım

`chapters/00_kapak.qmd` her iki render kolunda da bu dosyaya başvurur:

- PDF: `\includegraphics[width=2cm,height=2cm]{docs/assets/logo/marmara-universitesi-logo.png}`
- DOCX: `![](../docs/assets/logo/marmara-universitesi-logo.png){width=2cm height=2cm}`

Ölçü **2×2 cm'de sabittir**; §2.1 boyut kuralı gereği değiştirilmemelidir.
