---
description: 'Bir tablo/şekil/diyagram/grafik/istatistik sonucu/metin bölümünü "basitçe ama detay atlamadan, ders anlatır gibi" izah eder — kaynaktan doğrular, tipini tanır, değeri kaynaklı eşiğe oturtur; gerçek sayılar korunur, dosya değiştirilmez'
mode: agent
---

# /data-narrative — Veri Anlatısı Kapısı (Copilot ikizi)

İzah edilecek öğe: **${input:oge:açıklanacak öğe — ör. Tablo 4.13 / Şekil 3.2 / H1 sonucu / CFI 0,887 / eğilim skoru}** — boşsa editör seçimini kullan.

## Otomatik toplanan bağlam

Önce şu komutları terminalde çalıştırıp çıktılarını bağlama al:

```bash
# Bölüm tablo sırası (numara → kanonik etiket; 04_bulgular = 4.N)
grep -nE "^#\| label: tbl-" chapters/04_bulgular.qmd 2>/dev/null | nl -ba | awk '{print "4."$1"  →  "$0}'

# Bölüm şekil sırası (04_bulgular = Şekil 4.N; global render numarası farklı olabilir)
grep -nE "\{#fig-" chapters/04_bulgular.qmd 2>/dev/null | nl -ba | awk '{print "4."$1"  →  "$0}' | head -40

# Yöntem bölümü şekilleri (03 = Şekil 3.N)
grep -nE "\{#fig-" chapters/03_gerec_ve_yontem.qmd 2>/dev/null | nl -ba | awk '{print "3."$1"  →  "$0}' | head -20

# Skill tanımı (data-narrative metodolojisi)
head -40 .claude/skills/data-narrative/SKILL.md
```

## Görev

`data-narrative` skill'i (`.claude/skills/data-narrative/SKILL.md`) bu işte
**bağlayıcıdır**. Skill'i ve dört referansını oku
(`references/kaynak-dogrulama.md`, `references/gorsel-okuma-rehberi.md`,
`references/buyukluk-esikleri.md`, ve üslup için `references/ornek-tablo-4-4.md` +
`references/ornek-sekil-dag.md`), sonra sırasıyla:

1. **Kaynağı doğrula (ZORUNLU — atlanamaz).** Öğenin kanonik kimliğini bul (numara →
   `@tbl-apa-*`/`@fig-*` etiketi; render numaraları otomatiktir), içeriğini + caption'ı +
   üreten R modülünü/CSV'yi + çevre metnini `grep`/`sed` ile oku. Aktaracağın her sayıyı
   kaynaktan **birebir** teyit et; metin↔CSV çelişkisi görürsen açıklama yazma, çelişkiyi
   bildir. Öğe belirsizse tahmin etme; netleştir.

2. **Öğe tipini tanı → okuma hamlesini seç.** Öğe hangi aileye giriyor (orman grafiği,
   DAG, Bland–Altman, yanıt yüzeyi, ağ, ROC/DCA/kalibrasyon, spec-eğrisi, uyum-indeksi
   tablosu…)? O ailenin "önce şuna bak" hamlesini ve tipik yanılgısını
   `references/gorsel-okuma-rehberi.md`'den getir (aile listede yoksa genel yöntem).

3. **5-katman akışıyla anlat (görünmez iskelet):** (1) "Neden var?" → (2) analoji/
   somutlaştırma → (3) kademeli mekanizma + öğe-tipi okuma hamlesi (jargon daima
   parantezli) → (4) gerçek sayılarla kanıt; "iyi mi?" davet eden değeri
   **kaynaklı eşiğe** oturt (`references/buyukluk-esikleri.md`) → (5) tek-cümle
   blockquote kapanış. Katmanları numara vererek etiketleme.

4. **Ders anlatır gibi öğret:** yanlış okumayı önceden düzelt, zıtlıkla öğret, sayıyı
   günlük dile çevir (numeracy), değeri eşiğe yerleştir, "ee sonra?" köprüsüyle bir
   sonraki öğeye bağla. Uygun kavram-yanılgısı kapılarını (anlamlı≠büyük, anlamsız≠yok,
   ayarlanmış≠nedensel, iyi uyum≠doğru model, görünür≠optimizm-düzeltilmiş, keşifsel≠
   doğrulayıcı, eşik=gelenek) açıkça ele al.

5. **Zorunlu davranışlar:** dürüstlük kapısı (zayıf/başarısız/sınırlı yönleri gizleme,
   ⚠️/✓/❌); sayısal bütünlük (hiçbir sayı/yön/anlamlılık uydurulmaz-yuvarlanmaz-
   değiştirilmez; eşik de kaynağıyla verilir — `AGENTS.md` kaideleri); Türkçe + ilk-geçiş
   parantezli jargon; ölçeğe uyum (basit=kısa, karmaşık=tüm katmanlar); marketing dili
   yok.

6. **Kapanışta** ilgili komşu öğeleri (yandaki tablo, bağlı şekil, önceki/sonraki
   hipotez) aynı biçimde açma teklifini kısaca sun.

7. **Metni değiştirme.** Bu bir açıklama kapısıdır; tez dosyalarını düzenlemez, yeni
   analiz/sonuç üretmez. Yalnız var olanı ders anlatır gibi izah eder.

**Veri sınırı:** `data/raw|identified|cleaned|backup` ve satır-düzeyi
`data/processed`/`outputs` dosyaları okunmaz. Açıklama yalnız kanonik
tablo/şekil artefaktları ve `.qmd` metni üzerinden yapılır.
