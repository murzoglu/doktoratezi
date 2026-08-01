# Yeniden üsluplama yöntemi (reçete) — harness register'ında gömülü, Claude denetler

Reçete, üretici modelin taslağının **biçimini bağlar** (varyansı çökertir) ve Claude'un
değerlendirme ölçütüdür. Artık `constrained_rewrite.py` `default_system` **klinik hekim
register'ında** kodludur (bkz. `gemini-prompt-sablonu.md`); aşağıdaki beş hamle o register'ın
insan-okunur açılımıdır. Yeniden yazılmış pasaj yalnız bu beş hamleden oluşur; altıncı bir şey
**eklemez**.

**Hekim = KDT altyapılı klinisyen** (bu skill'in kritik kalibrasyonu): sayı okur → **manşet
sayılar metinde KALIR**, ayrıntılı çok-hücreli **grid → tabloya** (@tbl; değerin tabloda varlığı
doğrulanır); matematiksel **formül + yöntem mekaniği** → teknik eke havale; p/%95 GA gibi bildiği
ölçütü **tanımlama** (İSTATİSTİK-META yasak); klinik "so-what" **önce**. Klinik-lead "klinik olarak
/ klinik açıdan / aile değerlendirmesinde" ile kurulur — **"poliklinikte" kullanılmaz**.

**Birincil akış: Claude YAZAR, harness DOĞRULAR.** Sade+Marmara+sadık nesri Claude kurar; sayı/
çekince/**verdikt VERBATIM** (parafraz yok — çarpıtma en çok verdiktte olur); `verify_authored_spans`
DOKUNULMAZ span'ları mekanik doğrular. Üretici model opsiyonel taslak (zorlanınca çarpıtır).
**Sade AMA Marmara:** kısa DÜZ bildirim cümlesi; retorik soru/eksiltili cümle/konuşma dili YOK.

## 1. Klinik çerçeve önce
Cümleyi/pasajı klinisyenin bildiği zemine oturt (persona). Metodolojik amacı klinik dille aç:
"grupların baştan benzer olup olmadığını görmek için…" gibi. Ama **kaynakta olmayan yeni bir
amaç/gerekçe uydurma** (F2).

## 2. Açık sebep-sonuç
Var olan mekanizmayı görünür kıl: "çünkü / bu nedenle / dolayısıyla / böylece". Zincirin
halkaları kaynakta zaten vardır; sen yalnız **bağlaçla görünür** yaparsın — yeni bir neden
**icat etmezsin**.

## 3. Jargon çevirisi
Her metodolojik terim **ilk geçişte**: klinik karşılık + parantezde özgün ad
("**eğilim skoru** (bir ailenin DM grubunda olma olasılığı)"). Karşılıklar
`hedef-kitle-personasi.md`'den; tabloda yoksa üret + backlog'a ekle. Metriğin **tanımını**
izah edebilirsin; ama **bu sonucun** büyüklük/yön etiketini kaynakta yoksa ekleyemezsin.

## 4. Cümle bölme
Uzun/iç-içe cümleyi klinisyenin izleyebileceği kısa adımlara böl. Bir cümlede tek ana fikir.
Bölerken hiçbir çekince/kapsam sözcüğünü (yalnız, neredeyse, sınırda, analizlerde dikkate
alınan) düşürme.

## 5. Yerel yeniden sıralama (yalnız gerektiğinde — kapıya tabi)
Klinisyen için akış daha iyi olacaksa blok içi sırayı değiştir (ör. önce klinik anlam → sonra
istatistik dayanak). Kurallar:
- **Yerel:** bir paragraf/blok içinde; bölümler/bulgular arası global karıştırma YOK.
- **Gerekçe zorunlu (şablon):** "Klinisyen okur için önce _[X]_ sonra _[Y]_ daha anlaşılır,
  çünkü _[klinik-pedagojik neden]_."
- **Ayrı onay:** onay özetinde yeniden sıralamalar ayrı listelenir.
- **Bütünlük:** bulgu kümesi + her bulgunun sayı/yön/anlamlılık/atfı sabit; çapraz-referanslar
  yeniden doğrulanır; Bulgular'da numeric-trace yeniden koşar.
- **Kırılırsa geri al:** argüman mantığını veya atıf zincirini bozuyorsa yeniden sıralama iptal.

## Ölçek uyumu
- **Basit pasaj** (tek terim, kısa cümle): hafif dokunuş — terim glossu + belki bir bölme.
- **Ağır metodoloji pasajı** (SEM/IPTW/Bayes yoğun): tam yeniden kurma — beş hamle + gerekirse
  yerel yeniden sıralama.

## "Detay kaybı yok" — akıcılık uğruna ASLA düşmez
- çekince / sınırlılık ("yalnız ayarlama-seti değişkenlerinde", "veri seyrek")
- kapsam niteleyicisi ("neredeyse", "sınırda", "kısmen")
- alt-ölçek / alt-grup ayrımı (reddetme vs aşırı-koruma; DM vs kontrol)
- `[KEŞİFSEL]` / `[POST-HOC]` etiketi ve keşifsel-doğrulayıcı ayrımı
- yön ve anlamlılık ifadesi ("anlamlı değildi" → asla "eğilim/kısmen"e yumuşatılmaz)

## Değişmeyen bölge (taşınır, dokunulmaz)
Sayı/istatistik · bulgunun içeriği/yönü/anlamlılığı/büyüklüğü · kaynağın kapsam+temkini ·
`@tbl-*`·`@fig-*`·`[@key]` · `[KEŞİFSEL]`/`[POST-HOC]` · yöntem beyanı · atıf zinciri.
