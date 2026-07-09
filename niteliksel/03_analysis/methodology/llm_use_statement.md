# LLM Kullanım Beyanı (Yazım Yardımcısı Kapsamı)

**Sürüm:** v1 (2026-05-04)
**Paket:** A.8 (Faz A — Kalite Pekiştirme)
**Skill referansı:** `niteliksel-arastirma-rehberi-t1dm/assets/llm-kullanim-beyani-tr.md` + `references/06-llm-destekli-kodlama.md`
**Hedef:** (i) Tezin Yöntem bölümüne entegre edilecek özet beyan, (ii) Tez Beyanı bölümünde (Marmara şablonu 3.1.3) yer alacak ifade, (iii) Pediatric Diabetes manuscript için Acknowledgments / Methods notu

---

## 1. Açık Beyan (Tezde ve Manuscript'te Yer Alacak)

### TÜRKÇE — Tez Yöntem bölümü için kısa beyan (~120 kelime)

> **Yazım sürecinde büyük dil modeli (LLM) kullanımı.** Bu çalışmanın yazım sürecinde, niteliksel verilerin **kodlama, tema geliştirme veya yorumlama aşamalarında değil**, yalnızca metin yazım yardımcısı olarak Anthropic Claude (claude-opus-4-7) modeli kullanılmıştır. LLM'in kullanım kapsamı: (a) cümle akıcılığı ve metin organizasyonu önerileri, (b) eşanlamlı/alternatif ifade önerileri, (c) yapısal şablon (örn. tablo başlıkları) önerileri ile sınırlıdır. Ham görüşme verisi (transkriptler), saha notları, anonimleştirilmemiş demografik bilgi veya katılımcıya ait herhangi bir doğrudan tanımlayıcı **LLM'e gönderilmemiştir**; bu kapsam KVKK uyumluluğunu sağlamak için sınırlandırılmıştır. LLM tarafından üretilen tüm öneriler birinci araştırmacı (OM) tarafından gözden geçirilmiş, kabul edilen önerilerin nihai biçimleri yazıya alınmıştır. Atıf bütünlüğü için LLM'in önerdiği tüm bibliyografik referanslar manuel olarak doğrulanmıştır.

### ENGLISH — Manuscript / methods supplement (~110 words)

> **Use of large language model (LLM) in writing.** During the writing of this manuscript, Anthropic Claude (claude-opus-4-7) was used as a language assistant — **not** for qualitative coding, theme generation, or interpretation. Its use was limited to (a) sentence-flow and organisational suggestions, (b) alternative phrasings, and (c) structural templates (e.g. table headings). Raw interview transcripts, field notes, non-anonymised demographic information and any direct participant identifiers were **never submitted to the LLM**, in line with KVKK and ethical-review constraints. All LLM suggestions were reviewed by the principal researcher (OM); only those manually accepted entered the final text. To preserve citation integrity, every reference proposed by the LLM was manually verified against original sources.

### Tez Beyanı (Marmara şablonu 3.1.3) için ek cümle

> "Bu tezin yazım sürecinde, niteliksel verilerin analizinde değil yalnızca metin yazım yardımcısı olarak büyük dil modeli (Anthropic Claude) kullanılmıştır; analizin akademik içerik aitliği yazara aittir; LLM kullanımının kapsamı ve sınırları Yöntem bölümünde ayrıntılı olarak raporlanmıştır."

---

## 2. Genişletilmiş Açıklama (Yöntem bölümü ek-paragrafı veya Ek belge)

### 2.1 Kullanılan model ve sürümler

| Tarih aralığı | Model | Sürüm | Erişim |
|---|---|---|---|
| {2026-XX-XX – devam eden} | Anthropic Claude | claude-opus-4-7 (Claude Code arayüzü; 1M context penceresi) | Kurum-içi araştırmacı oturumu |
| {Önceki dönemde varsa} | {ÖNCEKI MODEL — boş bırakılabilir} | {SÜRÜM} | {ERİŞİM} |

### 2.2 Kapsam — LLM neyi yaptı, neyi yapmadı

**LLM'in YAPTIĞI işler:**
- Metin akıcılığı + organizasyon önerileri (paragraf yapısı, geçiş cümleleri)
- Eşanlamlı/alternatif ifade önerileri (Türkçe akademik kayıt)
- Yapısal şablonlar (tablo başlıkları, başlıklandırma hiyerarşisi)
- Yöntem bölümünün epistemolojik tutarlılık açısından gözden geçirilmesi (örn. A.1 paketinde "doygunluk → bilgi gücü" reframe önerisi)
- COREQ + JARS-Qual + Marmara tez şablonu kontrol listeleri ile metin uyumluluk kontrolü
- Atıf önerileri (sonradan manuel doğrulama gerekli)

**LLM'in YAPMADIĞI işler:**
- Ham görüşme transkripti analizi
- Kodlama (codebook v1 → v2 dahil hiçbir kodlama LLM tarafından yapılmadı; yalnızca codebook **yapısal organizasyonu** önerildi)
- Tema geliştirme veya tema isimlendirmesi (6 journal tema + 4 thesis makro tema OM tarafından önceden geliştirildi)
- Niteliksel veri yorumlama (alıntıların anlam çözümlemesi)
- Saha notları üzerinde herhangi bir işlem
- Demografik veri analizi
- Katılımcıya ait herhangi bir doğrudan tanımlayıcının işlenmesi

### 2.3 KVKK uyumluluk

LLM'e gönderilen materyaller:
- Yazım taslakları (Yöntem bölümü cümleleri, atıf taslakları, methodology dokümanları)
- Tez yapısı şablonları (başlıklar, alt-başlıklar)
- Çalışma sabitleri (sayılar: 7 aile, 21 katılımcı; tasarım: triadik; saha: Marmara Üniv. — bunlar zaten kamu bilgisi olacak tez içeriği)

LLM'e ASLA gönderilmeyen materyaller:
- Ham veya anonimleştirilmemiş transkriptler
- Saha notları (orijinal hâli)
- Demografik form içeriği
- Pseudonym haritası
- Aile-bazlı detaylı bilgi (çocuk yaşı + DM tanı yaşı + il kombinasyonu)
- Katılımcı isimleri, doğum tarihleri, adres, telefon
- Aile bireylerine ait fotoğraf, video, ses örneği

**Veri saklama (Anthropic):** Kullanılan API/arayüz, Anthropic'in standart veri saklama politikalarına tâbidir (yaklaşık 30 gün geri-bildirim için saklama; eğitim verisi olarak kullanılmadığı bildirilir). Kurumsal güvenli LLM erişimi için **Zero Data Retention (ZDR)** kontratı gelecekte düşünülebilir; bu dosya KVKK ihlali oluşturmaz çünkü zaten ham veri gönderilmemiştir.

### 2.4 Halüsinasyon ve Atıf Doğrulama Protokolü

Niteliksel araştırmada LLM tarafından üretilen atıfların **halüsine** olma riski belgelenmiş bir sorundur (bibliyografik kaynaklar uydurulabilir, DOI'lar yanlış olabilir, sayfalar hatalı çıkabilir). Bu çalışma için aşağıdaki doğrulama protokolü uygulanmıştır:

1. **Atıf doğrulama:** LLM tarafından önerilen her atıf (yazar, yıl, dergi, cilt, sayı, sayfa, DOI), bağımsız bir veritabanı (PubMed, Google Scholar, doğrudan dergi sayfası) üzerinde **kaynağa gidilerek** doğrulanmıştır
2. **Tıbbi/psikolojik tanımlar:** LLM tarafından özetlenen kuramsal kavramlar (örn. "biographical disruption", "biographical reconstruction") orijinal kaynak metinleri ile karşılaştırılmıştır
3. **Methodolojik özetler:** LLM tarafından özetlenen metodolojik çerçeveler (örn. Malterud bilgi gücü, Braun-Clarke RTA fazları), orijinal makaleye gidilerek doğrulanmıştır
4. **Türkçe kayıt:** LLM'in ürettiği Türkçe metinde, akademik kayıt + dilbilgisi açısından OM tarafından son okumadan geçirilmiştir; gereksiz İngilizce calque'ler düzeltilmiştir

**Şu ana kadar tespit edilen halüsinasyon olayları:** A.5 audit trail'a kaydedilecek (varsa).

### 2.5 OSF Prompt Zinciri Arşivi (D.1 paketi ile birlikte)

Tez sonrası açılacak niteliksel kol OSF projesinde, "supplementary materials" altında **prompt zinciri arşivi** yer alabilir:

```
osf.io/{niteliksel-proje}/
├── supplementary/
│   ├── llm_use_statement.md (bu belge)
│   ├── prompt_log/
│   │   ├── 2026-05-04_A1_information_power.md
│   │   ├── 2026-05-04_A6_codebook_v2.md
│   │   ├── 2026-XX-XX_*.md
│   │   └── README.md
│   └── verification_log/
│       └── citation_verification_2026-XX.csv
```

**Prompt log içeriği** (her dosya için):
- Tarih + saat
- Çalışma görevi (Faz A.X paketi)
- Gönderilen prompt (metin)
- Gönderilen materyal türü (yazım taslağı / yapı önerisi / atıf sorgusu)
- Önerilen çıktı (özet)
- OM kararı (kabul / kısmi kabul / red)
- Eklenen doğrulama (varsa atıf check, kaynak teyidi)

**Karar:** Tez teslim öncesi prompt log'unun OSF'ta hangi düzeyde paylaşılacağı (tam log / özet log / paylaşım yok) D.1 paketinde değerlendirilecek.

### 2.6 Etik Konum: Yazım Yardımcısı Olarak LLM

Bu çalışmanın **akademik içerik aitliği** birinci araştırmacı (OM) ve eş-araştırmacıya (BA) aittir. LLM, metnin **dilsel ve organizasyonel** boyutunda yardımcı bir araçtır; tez ve manuscript üretiminde "yazar" sıfatı taşımaz. Bu yaklaşım:

- **APA 7. baskı (2020) yönergesi** ile uyumludur (LLM yazar değil; methods/acknowledgments'ta beyan edilir)
- **COPE (Committee on Publication Ethics) 2023 ilkeleri** ile uyumludur
- **Anthropic Acceptable Use Policy** ile uyumludur

---

## 3. Mevcut Onam Formu ile Uyumluluk

A.7 KVKK DMP'sinde Bölüm 6 kontrol listesinde belirtildiği gibi, **mevcut onam formunda LLM kullanımına ilişkin açık ifade yer almayabilir** (çünkü onam formu 2023-02 tarihli; LLM kullanımı 2026'da başlamıştır).

**Bu durumun değerlendirmesi:**

- LLM'e ham veri gönderilmediği için **onam formu kapsamına uygun** (katılımcı verisi sızdırılmamıştır)
- Yine de "araştırma süreci yazımında AI yardımcısı kullanımı" şeklinde bir madde, **gelecekte yapılacak çalışmalarda** onam formuna eklenmesi önerilir
- Mevcut çalışmada bu kullanım, **yöntem şeffaflığı** prensibi gereği tezde + manuscript'te açıkça raporlanmaktadır (yukarıda § 1)
- KAEK'a **bilgilendirme bildirimi** (amendment değil, bilgi notu) gönderilebilir; bu karar A.5 audit trail'a kaydedilecek

---

## 4. Sürüm Geçmişi

- **v1 (2026-05-04):** İlk LLM kullanım beyanı. A.8 paketi.

İlerideki LLM kullanımı (yeni model sürümü, kapsam değişikliği) bu belgede güncellenir + audit trail'a kaydedilir.

---

## 5. Atıflar

```bibtex
American Psychological Association. (2024). APA Style and AI: Frequently Asked
  Questions. Retrieved from https://apastyle.apa.org/

Committee on Publication Ethics (COPE). (2023). Authorship and AI tools:
  COPE position statement. https://publicationethics.org/cope-position-statements

Hosseini, M., Resnik, D. B., & Holmes, K. (2023). The ethics of disclosing the
  use of artificial intelligence tools in writing scholarly manuscripts.
  Research Ethics, 19(4), 449–465.
```

---

## 6. Bağlantılı Paketler

- **A.7** (KVKK DMP): Bölüm 3 erişim kontrolü ve Bölüm 6 onam formu uyumluluğu — bu beyan ile koordineli.
- **A.5** (audit trail): LLM-ile-üretilmiş metin halüsinasyon tespit logu, atıf doğrulama logu burada tutulacak.
- **A.10** (jüri savunma): Olası soru — "AI ile mi yazdınız tezi?" Yanıt çekirdeği A.10'a entegre edilecek (kısaca: "yazım yardımcısı, analiz değil; ham veri gönderilmedi; APA/COPE ilkeleri ile uyumlu").
- **B.3** (Yöntem genişletme): § 1 ve § 2 arası özet, Yöntem'in Etik Hususlar veya yeni bir "Çalışmada Kullanılan Araçlar" alt-bölümüne eklenecek.
- **D.1** (OSF kayıt): § 2.5 prompt log arşivi tezin OSF projesinde yer alacak (paylaşım düzeyi karar verilecek).
- **D.2** (manuscript): Pediatric Diabetes manuscript'te Acknowledgments / Methods altına § 1 İngilizce versiyonu eklenecek.
