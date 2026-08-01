---
description: Tez yazım oturumu ritüeli — resmi kaynak önceliğini, kritik kaynak seçimini ve bölüm rotasını sabitler
argument-hint: "[oturumun görevi / hedef bölüm]"
allowed-tools: Bash(head *), Bash(ls *), Bash(git status*), Read
---

## Otomatik toplanan bağlam

### Tez yazım merkezi (README başı)
!`head -60 tez-yazim/README.md`

### Kritik kaynak haritası (başı)
!`head -40 tez-yazim/06_kritik-kaynaklar/README.md`

### Bölüm brief dosyaları
!`ls -la tez-yazim/03_bolum-hazirlik/ tez-yazim/04_kalite-kontrol/sertifikalar/ 2>/dev/null`

### Çalışma ağacı durumu
!`git status --short | head -20`

## Görev

Bu tez yazım oturumunu aç: **$ARGUMENTS**

`tez-yazim/00_kaynak-kurallari/talimatname-claude-code.md` bu oturumda
bağlayıcıdır. Sırasıyla:

1. Görevin hangi tez bölümüne (ÖZET/SUMMARY, GİRİŞ ve AMAÇ, GENEL BİLGİLER,
   GEREÇ ve YÖNTEM, BULGULAR, TARTIŞMA ve SONUÇ, KAYNAKLAR, EKLER) veya hangi
   destek işine düştüğünü belirle ve açıkça bildir.
2. Kaynak önceliğini uygula: (1) `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf`
   + `TEZ ŞABLONLARI-2026-2RV.docx`, (2) kanonik biçim otoritesi
   `tez-yazim/00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md` ve özeti
   `tez-yazim/00_kaynak-kurallari/format-kontrati.md`, (3) repo kanıtı. Çakışmada
   biçim/bölüm sırası kararını resmi kılavuz + kanonik talimatname verir; tüm
   yazımda bu talimatnameye zorunlu uyum sağlanır. Dış literatür/citation için
   `tez-yazim/01_mimari/evidentia-entegrasyon-cercevesi.md`; nitel kol çıktısı
   için `tez-yazim/05_entegrasyon/nitel-cikti-cercevesi.md`.
3. Bölüm işiyse ilgili briefi aç: `tez-yazim/03_bolum-hazirlik/<bölüm>.md`;
   kanıt eşlemesi için `tez-yazim/06_kritik-kaynaklar/kritik-dosya-manifesti.tsv`.
4. Nitel kolun kanıtı gerekiyorsa kanonik kaynak
   `niteliksel/06_manuscript_outputs/qualitative_canonical_results_for_doktoratezi.md`'dir; ham transcript
   veya nitel kol geniş taraması default değildir.
5. Veri sınırını hatırla: `data/raw|identified|cleaned|backup` ve satır-düzeyi
   `data/processed`/`outputs` içeriği açılmaz; analiz targets pipeline'ı ve
   aggregate çıktılar üzerinden yürür.
6. Dış literatür gerekiyorsa her referans `/referans-kapisi` sürecinden geçer;
   bölüm kapanışında `/bolum-sertifika` ve `/tez-dogrulama` koşulur.
