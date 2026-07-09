# Kritik Kaynaklar

Bu klasör tez yazımında kullanılacak hayati kaynak dosyalarının çalışma haritasıdır.
Dosyaların kendisini buraya kopyalamaz; klinik/nitel sonuç raporlarını, protokolü,
ham ve kilitli verileri, ölçek/form dokümanlarını ve kalite kapılarını tek
izlenebilir listede bağlar.

> **Otorite:** Bu dosya **kritik kaynak/veri manifestinin** tek kanonik yeridir
> (hangi repo/klinik/nitel/ölçek dosyası, hangi erişim sınırıyla, hangi bölümde).
> Devredilen otoriteler: biçim/kaynakça →
> `00_kaynak-kurallari/marmara-tez-formati-talimatnamesi.md`; referans kapısı
> sırası → `00_kaynak-kurallari/talimatname-claude-code.md` §4 +
> `01_mimari/evidentia-entegrasyon-cercevesi.md` §5; veri sınırı (KVKK) →
> `talimatname-claude-code.md` §2; bölüm kapanışı (Kapı 0–5) →
> `04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md`;
> makine-okunur manifest → `kritik-dosya-manifesti.tsv`.

## Kullanım Kuralı

1. Her bölüm yazım oturumunda önce bu dosya ve `kritik-dosya-manifesti.tsv` okunur.
2. Ham veri, kimliklenebilir veri, transcript veya satır düzeyi CSV içeriği bu
   klasöre kopyalanmaz ve harici MCP/RAG araçlarına gönderilmez.
3. Yazımda kullanılacak sayısal iddia önce CSR, SAP, veri haritası ve ilgili test
   kanıtıyla; nitel iddia önce kanonik nitel rapor, COREQ/audit trail ve gerekirse
   nitel repo reliability raporuyla kapatılır.
4. Dış literatür eklenecekse Evidentia -> OpenAthens/full-text ->
   Anna's fallback -> PMC/OA/repository -> Zotero -> referans ledgeri ->
   çift AI-reliability sırası tamamlanmadan citation metne giremez.

## Birincil Kaynak Haritası

| Kaynak sınıfı | Birincil dosya | Yazımda kullanım | Erişim |
|---|---|---|---|
| Resmi tez kılavuzu | `docs/tez-kilavuz/TEZ YAZIM KLAVUZU-2025.pdf` | Format, bölüm sırası, tablo/şekil, kaynakça. | Açık repo içi |
| Resmi tez şablonu | `docs/tez-kilavuz/TEZ ŞABLONLARI-2026-2RV.docx` | Kapak, ön bölümler, bölüm yerleşimi. | Açık repo içi |
| Güncel klinik çalışma sonuç raporu | `docs/CLINICAL-STUDY-REPORT-FINAL.md` | Nicel bulgular, örneklem, yöntem, klinik yorum sınırı. | Repo içi kanonik |
| Nitel çalışma sonuç raporu | `docs/niteliksel/qualitative_canonical_results_report.md` | Nitel kolun tezde varsayılan temsil kaynağı. | Repo içi türetilmiş |
| Klinik çalışma protokolü | `docs/protokol/KLINIK_CALISMA_PROTOKOLU.md` | Etik, tasarım, örneklem, ölçüm araçları, veri toplama. | Repo içi kanonik |
| Veri sözleşmesi | `docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md` | Final CSV şeması, structural NA, ölçüm blokları. | Repo içi kanonik |
| Ham klinik veri | `data/raw/Raw Data - Final.csv` | Yalnız doğrulama ve reprodüksiyon; yazıma satır içeriği taşınmaz. | Korumalı |
| Kanonik analiz kilidi | `data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock` | Hash, satır/sütun ve final analiz baz doğrulaması. | Kontrollü |
| Long analiz bazı | `data/processed/FINAL_REFERENCE__analysis_base_long.csv` | Analiz girdisi; aggregate çıktılar üzerinden yazılır. | Kontrollü |
| Family analiz bazı | `data/processed/FINAL_REFERENCE__analysis_base_family.csv` | Aile düzeyi analiz girdisi; aggregate çıktılar üzerinden yazılır. | Kontrollü |
| EMBU-P formu | `docs/protokol/KANONIK_KISALTILMIS_EMBU_EBEVEYN.md` | Anne/ebeveyn bildirimi ölçek tanımı ve puanlama. | Repo içi kanonik |
| EMBU-C formu | `docs/protokol/KANONIK_KISALTILMIS_EMBU_COCUK.md` | Çocuk bildirimi ölçek tanımı ve puanlama. | Repo içi kanonik |
| Beck formu | `docs/protokol/KANONIK_BECK_DEPRESYON_ENVANTERI.md` | Anne depresif belirti ölçümü. | Repo içi kanonik |
| KİA/SRQ formu | `docs/protokol/KANONIK_KARDES_ILISKILERI_ANKETI.md` | Kardeş ilişkileri ölçümü. | Repo içi kanonik |
| Demografik ve tıbbi form | `docs/protokol/KANONIK_DEMOGRAFIK_VE_TIBBI_BILGILER.md` | Kovaryatlar, klinik/demografik alanlar, kodlar. | Repo içi kanonik |
| SES formu | `docs/protokol/SOSYOEKONOMIK-STATU-DEGERLENDIRME.md` | SES/meslek/ev-olanakları alanları ve kod kararları. | Repo içi kanonik |

## Nitel Repo Koşullu Kaynakları

Nitel repo artık genel yazım merkezi değildir. Aşağıdaki kaynaklar yalnız nitel
yöntem, bulgular, joint display, tartışma veya ekler kesiminde gerekli olursa
açılır.

| Kaynak | Yol | Kullanım sınırı |
|---|---|---|
| Kanonik nitel sonuç raporu kaynağı | `/mnt/thunderbolt/workspaces/T1DM Niteliksel/06_manuscript_outputs/qualitative_canonical_results_for_doktoratezi.md` | Doktoratezi kopyasıyla hash eşleşmesi korunur. |
| Nitel rapor AI reliability | `/mnt/thunderbolt/workspaces/T1DM Niteliksel/07_reports/ai_reliability_qualitative_canonical_results_report.md` | Quote-ID, code-ID ve copy parity düzeyi; ham alıntı yok. |
| Codebook | `/mnt/thunderbolt/workspaces/T1DM Niteliksel/03_analysis/codebook/codebook_v2.md` | Tema/kod tanımı; gerektiğinde `codebook_v3.csv` ile kontrol. |
| COREQ ve yöntem paketi | `/mnt/thunderbolt/workspaces/T1DM Niteliksel/03_analysis/methodology/` | RTA, COREQ, audit trail, positionality ve LLM beyanı. |
| Ham nitel görüşmeler | `/mnt/thunderbolt/workspaces/T1DM Niteliksel/01_raw_data/interviews_docx/` | Korumalı; yazımda doğrudan açılmaz, kopyalanmaz, dış araca gönderilmez. |
| Görüşme rehberi | `/mnt/thunderbolt/workspaces/T1DM Niteliksel/01_raw_data/interview_guides/qualitative_interview_questions.docx` | Yöntem bölümünde araç tanımı için hedefli kullanılır; ham içerik/katılımcı yanıtı taşınmaz, dış araca gönderilmez. |

## Zorunlu Kapanış Kapıları

| Kapanış | Komut / belge | Beklenen sonuç |
|---|---|---|
| Klinik veri kilidi | `Rscript tests/test_reproducibility_lock.R`; `Rscript tests/test_final_reference_loading.R` | Kanonik CSV lock/hash/shape geçer. |
| Nicel AI reliability | `PYTHONDONTWRITEBYTECODE=1 python3 plugins/doktoratezi-ai-audit/skills/doktoratezi-ai-audit/scripts/test_repo_ai_reliability.py` | Nicel guardrail ve raw-data sınırı geçer. |
| Nitel AI reliability | `PYTHONDONTWRITEBYTECODE=1 python3 plugins/t1dm-qual-ai-audit/skills/t1dm-qual-ai-audit/scripts/test_repo_ai_reliability.py` | Nitel gizlilik ve kanonik rapor sınırı geçer. |
| Referans ledgeri | `tez-yazim/02_kanit-haritalari/referans-denetim-ledgeri.md` | DOI/PMID/ID, full-text route, Zotero item/attachment key ve claim notu tamamlanır. |
| Format kontrolü | `tez-yazim/04_kalite-kontrol/format-kontrol-listesi.md` | Resmi Marmara biçim kuralları kapanır. |
| Bölüm sertifikasyonu | `tez-yazim/04_kalite-kontrol/bolum-finalizasyon-sertifikasyon-playbook.md` | Kapı 0-5 PASS, sertifika raporu ve uygulama onayı olmadan final yok. |

## Güncelleme Kuralı

Bu klasördeki manifest yeni dosya taşınması veya kanonik kaynak değişiminde
güncellenir. Raw veri içeriği, aile/katılımcı satırları, transcript metinleri,
`.env` ve credential değerleri bu klasörde hiçbir zaman saklanmaz.

## Öncelik zinciri

Çakışmada: (1) kullanıcı/danışman → (2) resmi `docs/tez-kilavuz/` → (3)
`00_kaynak-kurallari` kanonik kural → (4) bu manifest → (5) eski notlar.
Analiz/veri/hipotez kararında repo kanıtı (`_targets.R`, testler, protokol, CSR)
üstündür.

## Duplikasyon önleme kuralı

Bu dosya kaynak/erişim **eşlemesi**dir; referans kapısı sırası, tam-metin
kaskadı, format ve bölüm kapanış kapıları burada **tam metniyle tekrarlanmaz** —
yukarıdaki kanonik otoritelere pointer verilir. Yeni kaynak eklenince önce
`kritik-dosya-manifesti.tsv`, sonra bu harita güncellenir.
