# Kanıt ve Gizlilik Kontrol Listesi

> **Kanonik kural otoritesi:** Bu, **Kapı 0** (kapsam/gizlilik) + **Kapı 1/2**
> (kanıt) operasyonel checklist'idir. Veri sınırı kanonik otoritesi →
> `00_kaynak-kurallari/talimatname-claude-code.md` §2; kanıt kaydı →
> `02_kanit-haritalari/referans-denetim-ledgeri.md`; korumalı yol listesi →
> `06_kritik-kaynaklar/kritik-dosya-manifesti.tsv`. Master süreç:
> `bolum-finalizasyon-sertifikasyon-playbook.md` Kapı 0–2. Klasör haritası:
> `04_kalite-kontrol/README.md`.

## Kanıt

- [ ] Her repo içi iddia dosya yoluna bağlandı.
- [ ] İlgili bölüm için `tez-yazim/06_kritik-kaynaklar/README.md` ve
  `kritik-dosya-manifesti.tsv` üzerinden kaynak sınıfı seçildi.
- [ ] Sayısal iddialar testlenmiş aggregate çıktı veya analiz planı ile uyumlu.
- [ ] Dış literatür iddiaları primary/official kaynakla doğrulandı.
- [ ] Güncel/değişken dış bilgiler canlı kontrol edildi.
- [ ] Faz II/post-hoc sonuçlar ayrı etiketlendi.
- [ ] Nitel ve nicel kanıt türleri açık ayrıldı.
- [ ] Bölüm için `bolum-finalizasyon-sertifikasyon-playbook.md` Kapı 0-5
  sertifika raporuna işlendi.
- [ ] Sertifika raporunda uygulama onayı yoksa bölüm final kabul edilmedi.

## Gizlilik

- [ ] Kritik kaynak manifestindeki `korumalı` ve `kontrollü` kaynaklar
  yalnız yol/hash/aggregate düzeyinde kullanıldı.
- [ ] `data/raw/`, `data/identified/`, `data/cleaned/`, `data/backup/`,
  `data/processed/*`, `_targets/`, `outputs/*` satır düzeyi içerik vermedi.
- [ ] Nitel `01_raw_data/`, `02_processed/transcripts/`, `01_deidentified/`,
  `00_raw_locked/`, `.remember/` içeriği yazıma taşınmadı.
- [ ] Aile düzeyi hassas ayrıntı veya demografi satırı yok.
- [ ] `.env`, credential, token veya API anahtarı yazdırılmadı.
- [ ] Harici MCP'ye yalnız anonim/türetilmiş bilgi gönderildi.
