# ÖNERİ: Kanonik Terim Sözlüğü + Otomatik Denetim Tasarımı

Durum: **tasarım önerisi** — hiçbir dosyayı değiştirmez, kod yazmaz. Uygulama
kararı ve kapsam onayı kullanıcıya aittir.
Oluşturma tarihi: 2026-07-29
Bağlam: `docs/tez-kilavuz/TERIM_TUTARLILIK_TARAMASI.md` taraması, tek seferlik
düzeltmenin yeterli olmadığını, tutarlılığın **sürdürülebilir** bir mekanizma
gerektirdiğini gösterdi.

---

## 1. Problem: Neden tek seferlik düzeltme yetmez?

- Tez canlı bir belge; her yeni pasaj yeni varyant sokabilir (`aşırı koruma` →
  yanlışlıkla `aşırı koruyuculuk`).
- Mevcut denetim (`tr_corpus_audit`) yalnız **kısaltma-drift** ve **yakın-duplikat**
  yakalar; **eşanlamlı/varyant terim** (gizil↔latent, reddetme↔reddedicilik)
  yakalamaz.
- `00b_kisaltmalar.qmd` yalnız *kısaltmaları* tutar; *tercih edilen tam terim*
  ve *yasak varyantları* tutmaz.
- Sonuç: tutarlılık şu an **insan dikkatine** bağlı → kaçınılmaz drift.

## 2. Mevcut altyapı (üzerine inşa edilecek)

| Bileşen | Ne yapıyor | Eksik |
|---|---|---|
| `chapters/00b_kisaltmalar.qmd` | Kısaltma→açıklama tablosu | Eşanlamlı/tercih-terim yok |
| `scripts/util/tr_corpus_audit.py` | Kısaltma-drift + yakın-duplikat + geçiş | Varyant-terim denetimi yok |
| `scripts/util/tez_checklist_verify.py` | 8-eksen orkestratör (K4 dil ekseni) | Terim-sözlüğü kapısı yok |
| `TERIM_TUTARLILIK_TARAMASI.md` | Tespit raporu (statik) | Otomatik zorlama yok |

**Tasarım ilkesi:** yeni bir paralel sistem KURMA; mevcut üçlüyü (00b tarzı
sözlük + tr_corpus_audit tarzı denetim + checklist kapısı) genişlet.

---

## 3. Önerilen Çözüm — Üç Katmanlı

### Katman 1 — Kanonik Terim Sözlüğü (veri)
Tek bir makine-okunur kaynak: **`docs/tez-kilavuz/terim-sozlugu.yaml`** (veya .md
tablo). Her giriş:

```yaml
- kanonik: "gizil değişken"
  ingilizce: "latent variable"       # ilk-geçiş parantezi için
  yasak_varyantlar: ["latent değişken", "örtük değişken", "gizli değişken"]
  kapsam: "istatistik"                # bağlam etiketi
  istisna_notu: "'gizli' confounder anlamında MUAF (bkz. sensemakr)"
  oncelik: "A"

- kanonik: "aşırı koruma"
  yasak_varyantlar: ["aşırı koruyuculuk"]
  kapsam: "embu-alt-olcek"
  istisna_notu: "Dirik'ten söz ederken 'aşırı koruyuculuk' serbest; genel kuram serbest"
  oncelik: "A"

- kanonik: "reddetme"
  yasak_varyantlar: ["reddedicilik"]
  kapsam: "embu-alt-olcek"
  istisna_notu: "Dirik terimi olarak serbest"
  oncelik: "A"
```

Neden YAML: istisna/kapsam/öncelik gibi çok-alanlı meta taşır; hem denetim scripti
hem insan okur. (Alternatif: 00b tarzı markdown tablo — daha basit ama meta-fakir.)

### Katman 2 — Denetim Scripti (zorlama)
**`scripts/util/terim_tutarlilik_audit.py`** — sözlüğü okur, `chapters/*.qmd`
tarar, her *yasak varyant* için:
- konum (dosya:satır) + bağlam satırı,
- kanonik karşılık önerisi,
- istisna kuralı otomatik uygulanır (ör. İngilizce özet `00c`, ilk-geçiş
  parantezi `(*latent*)`, kod-bloğu, alıntı → MUAF),
- çıktı: `HARD` (yasak varyant, muafiyet dışı) / `INFO` (muaf).

Mevcut `tr_corpus_audit.py`'nin `strip_fenced`, `tokenize_tr`, muafiyet
desenleri **yeniden kullanılır** (kopyalanmaz). Exit≠0 → FAIL.

### Katman 3 — Checklist Kapısı (entegrasyon)
`tez_checklist_verify.py`'ye yeni madde: **`K4-TERM-01`** (Türkçe/Akış ekseni
altında). Terim-audit'i alt-süreçle çağırır; herhangi HARD bulgu = teslim engeli.
Böylece her kapanış turunda otomatik çalışır.

---

## 4. İş Akışı (uygulandıktan sonra)

```
Yazar yeni pasaj ekler
        ↓
tez_checklist_verify.py çalışır
        ↓
K4-TERM-01 → terim_tutarlilik_audit.py
        ↓
"latent değişken" bulundu (04_bulgular.qmd:812, muaf değil)
        ↓
FAIL: → "gizil değişken" kullan   [teslim engellendi]
```

Sözlük büyüdükçe (her yeni terim kararı bir giriş) tutarlılık **kümülatif**
korunur; drift kaynakta yakalanır.

---

## 5. Uygulama Fazları (önerilen sıra)

| Faz | İş | Çıktı | Risk |
|---|---|---|---|
| **F1** | Sözlüğü oluştur (yalnız A-grubu 7 terim ile başla) | `terim-sozlugu.yaml` | Düşük (yalnız veri) |
| **F2** | Denetim scriptini yaz + testini ekle | `terim_tutarlilik_audit.py` + `tests/` | Orta (muafiyet mantığı) |
| **F3** | Mevcut A-grubu ihlallerini düzelt (script rehberliğinde) | temiz `chapters/*.qmd` | Orta (bağlam kontrolü) |
| **F4** | Checklist kapısını bağla (K4-TERM-01) | orkestratör güncel | Düşük |
| **F5** | B/C gruplarını sözlüğe ekle (kademeli) | genişleyen sözlük | Düşük |

Her fazda değişmezlik kuralı: sayı/istatistik/atıf/yön korunur; yalnız terim-dili.

---

## 6. Alternatifler (ve neden önerilmedi)

| Alternatif | Artı | Eksi | Karar |
|---|---|---|---|
| Yalnız `TERIM_TUTARLILIK_TARAMASI.md` (statik rapor) | Basit | Zorlama yok, drift devam eder | Yetersiz |
| `00b_kisaltmalar.qmd`'yi genişlet | Mevcut dosya | Kısaltma-odaklı; tam-terim/istisna taşıyamaz | Kısmi |
| Global bul-değiştir (sözlüksüz) | Hızlı | İstisnaları ezer (gizli-confounder!), tehlikeli | Reddedildi |
| Harici araç (LanguageTool vb.) | Hazır | Türkçe-domain terimlerini bilmez, repo'ya yabancı | Reddedildi |
| **3-katmanlı (bu öneri)** | Zorlayıcı, istisna-farkında, mevcut altyapıya oturur | Script yazımı gerektirir | **Önerilen** |

---

## 7. Minimum Uygulanabilir Adım (isterseniz hemen)

En küçük değerli parça: **F1 + F3 (yalnız A-grubu)** — sözlüğü A1-A7 ile kur,
mevcut ihlalleri düzelt. Denetim scripti (F2/F4) sonraya bırakılabilir; ama
o olmadan drift geri döner. Tam değer için F1→F4 önerilir.

## 8. İlgili belgeler
- Tespit raporu: `docs/tez-kilavuz/TERIM_TUTARLILIK_TARAMASI.md`
- Gizil-terim standardı (A1): `docs/tez-kilavuz/ONERI_gizil-latent-ortuk-terim-standardi.md`
- Kanonik EMBU adları (A2-A4): `docs/protokol/KANONIK_KISALTILMIS_EMBU_*.md`
- Mevcut denetim motoru: `scripts/util/tr_corpus_audit.py`
- Orkestratör: `scripts/util/tez_checklist_verify.py`
