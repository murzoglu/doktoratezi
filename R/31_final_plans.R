# KISIM XIII/XV/XVI — yayin, risk ve zaman plani

final_publication_strategy <- function() {
  data.frame(
    manuscript_id = c("M1", "M2", "M3"),
    working_title = c(
      "Differential Parental Treatment Perceptions in Type 1 Diabetes Families: A Case-Control Multi-Informant Study from Turkey",
      "Maternal Mental Health Burden in Pediatric Type 1 Diabetes: Depressive Symptoms, Antidepressant Use, and Parenting Style",
      "Validation and Sensitivity Architecture for the Turkish Short-EMBU Parent and Child Forms in Family Research"
    ),
    primary_focus = c(
      "H1 + H5: çocuk algısı ve diadik tutarlılık",
      "H3 + H4 + KISIM VI: anne öz-rapor, Beck latent SEM ve mediation",
      "KISIM IV + XI + XII: psikometri, multiverse, TOST ve Bayesian dual reporting"
    ),
    target_journal_1 = c("Pediatric Diabetes", "Diabetic Medicine", "Methods in Psychology"),
    target_journal_2 = c("Journal of Pediatric Psychology", "Journal of Family Psychology", "Frontiers in Psychology - Quantitative Psychology"),
    core_tables = c(
      "apa_t06, apa_t07, apa_t13, apa_t22",
      "apa_t10, apa_t11, apa_t12, apa_t14, apa_t18",
      "psychval_*, apa_t05, apa_t19, apa_t20, apa_t21"
    ),
    core_figures = c(
      "h1_forest, h1_three_way_emm, h5_ba_grid, h5_rsa_surface",
      "h3_stratified_forest, h4_sem_path, mediation_effects, bayesian_forest",
      "ses_correlation_heatmap, specification_curve, sensemakr_contour, bayesian_diagnostics"
    ),
    readiness = c("tez-ready", "tez-ready", "methods-ready"),
    next_action = c(
      "Makale özetini 250 kelimeye indir ve H1/H5 odaklı Methods-Results iskeleti çıkar",
      "H3-H4-Mediation klinik yorum sınırını nedensel olmayan dil ile ayrılaştır",
      "Psikometrik validasyon raporunu journal formatına sıkıştır ve ek tablo setini seç"
    ),
    stringsAsFactors = FALSE
  )
}

final_publication_evidence_map <- function() {
  data.frame(
    manuscript_id = c("M1", "M1", "M1", "M2", "M2", "M2", "M3", "M3", "M3"),
    evidence_block = c("H1", "H5", "KISIM XII", "H3", "H4", "KISIM VI", "KISIM IV", "KISIM XI", "KISIM XII"),
    claim_boundary = c(
      "DM çocuklarında EMBU-C reddetme yükselmiştir",
      "Anne-cocuk tutarlılığı zayıf ve klinik tutarsızlık örüntüleri yüksektir",
      "H1 reddetme BF10=8.12 ile Bayesian destek alır",
      "Anne öz-raporda DM-Kontrol farkı yoktur",
      "Beck depresyonu EMBU-P latent yollarıyla ilişkilidir",
      "Mediation indirect etkileri sıfırı içerir",
      "Ölçek psikometri ve invariance bulguları ölçüm sınırlarını tanımlar",
      "Multiverse ve TOST H3 negatif bulguyu güçlendirir",
      "H3 BF10=0.17-0.25 ile H0 lehine kanıt verir"
    ),
    primary_artifact = c(
      "apa_t06_h1_primary.csv; h1_forest.png",
      "apa_t13_h5_concordance.csv; h5_ba_grid.png",
      "apa_t07_h1_bayesian.csv; bayesian_forest.png",
      "apa_t10_h3_primary_iptw.csv",
      "apa_t12_h4_sem.csv; h4_sem_path.png",
      "apa_t14_mediation.csv; mediation_effects.png",
      "psychval_*.csv",
      "apa_t19_robustness.csv; specification_curve.png",
      "apa_t21_bayesian_global.csv"
    ),
    interpretation_guardrail = c(
      "Multi-informant fark; nedensel dil yok",
      "Uyum zayıf; bootstrap aralıkları geniş",
      "Bayesian destek doğrulayıcı değil, tamamlayıcıdır",
      "Eşdeğerlik yalnız TOST equivalent alt ölçeklerde söylenir",
      "Kesitsel SEM assosiyatif yorumlanır",
      "Indirect etki yok; Beck-EMBU-P köprüsü ayrı yorumlanır",
      "Floor effect ve zayıf alpha açıkça raporlanır",
      "Specification setleri önceden tanımlı ailelerle sınırlıdır",
      "Prior ve ROPE sınırları açık raporlanır"
    ),
    stringsAsFactors = FALSE
  )
}

final_risk_matrix <- function() {
  data.frame(
    risk_id = sprintf("R%02d", 1:14),
    risk = c(
      "H1 grup farkı sıcaklık/aşırı korumada çıkmaz",
      "H2 APIM veya dyadic CFA convergence fail",
      "H3 EMBU-P reddetme zayıf psikometri",
      "H4 SEM identification veya sparse ordinal kategori sorunu",
      "H5 RSA convergence veya yüzey yorumu belirsizliği",
      "HbA1c tamamlanma oranı düşük",
      "renv veya sistem paket kilidi bozulur",
      "Antidepresan kullanımı karıştırıcı/yorum kaydırıcı rol oynar",
      "ISEI tek başına SES'i karşılamaz",
      "LPA/LCA tipoloji modeli kararsız kalır",
      "Network EBIC-LASSO sonuçları belirsizdir",
      "Klinik karar ağacı/RF overfit riski",
      "Bayesian Stan/brms compile veya sampling sorunu",
      "Quarto/papaja render problemi"
    ),
    probability = c("Orta", "Düşük", "Yüksek", "Düşük", "Orta", "Kesin", "Düşük", "Yüksek", "Orta", "Düşük", "Orta", "Yüksek", "Düşük", "Orta"),
    impact = c("Orta", "Orta", "Yüksek", "Yüksek", "Orta", "Yüksek", "Yüksek", "Yüksek", "Orta", "Orta", "Orta", "Yüksek", "Orta", "Orta"),
    mitigation = c(
      "TOST + Bayesian BF + multiverse savunması",
      "Family-mean Welch + moderation yedeği",
      "BSEM/latent yorum + multiverse + TOST + açık sınırlılık",
      "Reduced item multi-group screen + path analysis fallback",
      "ICC/Bland-Altman birincil; RSA keşifsel",
      "HbA1c keşifsel; dm_yili tam veriyle ana klinik süre göstergesi",
      "Docker + renv.lock + targets manifest",
      "Stratified sensitivity; total-effect model sınırı",
      "Latent SES + Hollingshead + materyal indeks triangülasyonu",
      "LPA continuous primary; LCA tertile sensitivity + modal-class regression",
      "NCT + merkeziyet + bootstrap/sensitivity dili",
      "Calibration + DCA + optimism correction + dış validasyon notu",
      "CSV/RDS smoke; divergent/Rhat/ESS tanıları",
      "HTML Quarto fallback; PDF ayrı export"
    ),
    trigger = c(
      "H1 FDR p>.05 ve BF10<3",
      "lavaan/lmer yakınsamaz",
      "alpha/omega ve floor effect sınır altı",
      "ordinal boş kategori veya nonidentification",
      "RSA model status ok değil",
      "HbA1c n<50",
      "renv::status() uyumsuz",
      "AD strata yön değiştirir",
      "SES SMD veya CFA zayıf",
      "entropy düşük veya BLRT kararsız",
      "NCT/edge kararsız",
      "AUC optimism veya calibration zayıf",
      "Rhat>1.01 veya divergent>0",
      "quarto render non-zero exit"
    ),
    status = c(
      "kapalı", "kapalı", "aktif-izlem", "kapalı", "kapalı", "aktif-izlem", "kapalı",
      "aktif-izlem", "kapalı", "kapalı", "kapalı", "aktif-izlem", "kapalı", "kapalı"
    ),
    stringsAsFactors = FALSE
  )
}

final_risk_summary <- function(risk_matrix) {
  data.frame(
    metric = c("total_risks", "active_monitoring", "closed_or_controlled", "deferred_boundary"),
    value = c(
      nrow(risk_matrix),
      sum(risk_matrix$status == "aktif-izlem"),
      sum(risk_matrix$status == "kapalı"),
      sum(risk_matrix$status == "deferred-sınır")
    ),
    stringsAsFactors = FALSE
  )
}

final_timeline_24_week <- function() {
  data.frame(
    week = c("1", "2", "3", "4", "5", "6", "7", "8", "9-10", "11-12", "13", "14", "15", "16", "17", "18", "19", "20-21", "22", "23", "24"),
    phase = c(
      "Setup + renv + Docker",
      "Veri yükleme + skor türetme",
      "Tablo 1 + SMD + DAG + propensity",
      "SES kompozit",
      "Eksik veri çoklu çerçeve",
      "H1 multilevel + 3-way + IRT",
      "H2 family-mean + APIM + dyadic CFA",
      "H3 main + stratified + IPTW",
      "H4 latent SEM + invariance + Bayesian preflight",
      "H5 ICC + Bland-Altman + RSA + CFM + dyadic CFA",
      "Mediation",
      "LPA anne tipoloji",
      "LCA/Bifactor S-1",
      "Network + NCT + Beck item network",
      "ROC + DCA + CART + RF + calibration",
      "DM klinik alt-analizler",
      "Multiverse + TOST + Sensemakr + negative control",
      "Bayesian H1/H3 + WAIC/LOO",
      "APA tablo + figür + tez eşleme",
      "Yayın hazırlığı + OSF/Zenodo",
      "Final QC + savunma hazırlığı"
    ),
    output = c(
      "renv.lock; Dockerfile",
      "Kanonik final reference lock",
      "Table1/SMD/DAG/PS tabloları",
      "ses_latent ve SES audit",
      "MI/FIML/NMAR plan tabloları",
      "H1 tabloları + figürler",
      "H2 tabloları + APIM figürü",
      "H3 tabloları + stratified forest",
      "H4 SEM tabloları + path figürü",
      "H5 beş strateji + BA/RSA figürleri",
      "Mediation tablo + figür",
      "LPA tablo + figür",
      "LCA sensitivity + modal regression + Bifactor S-1",
      "Network tabloları + figürler",
      "Clinical utility tabloları + ROC/DCA/calibration",
      "DM clinical tables",
      "Robustness/sensitivity tabloları + figürler",
      "Bayesian CSV/RDS + diagnostics",
      "24 figür + 22 tablo + thesis HTML",
      "3 makale planı + code/data package plan",
      "Risk kapanışı + savunma iskeleti"
    ),
    status = c(rep("verified", 19), "verified", "planned"),
    stringsAsFactors = FALSE
  )
}

final_timeline_summary <- function(timeline) {
  data.frame(
    metric = c("total_rows", "verified_rows", "planned_rows", "current_week"),
    value = c(nrow(timeline), sum(timeline$status == "verified"), sum(timeline$status == "planned"), 23L),
    stringsAsFactors = FALSE
  )
}

final_planning_bundle <- function() {
  publication <- final_publication_strategy()
  evidence <- final_publication_evidence_map()
  risks <- final_risk_matrix()
  timeline <- final_timeline_24_week()
  list(
    publication_strategy = publication,
    publication_evidence_map = evidence,
    risk_matrix = risks,
    risk_summary = final_risk_summary(risks),
    timeline_24_week = timeline,
    timeline_summary = final_timeline_summary(timeline)
  )
}

final_planning_manifest <- function(bundle) {
  data.frame(
    artifact = names(bundle),
    rows = vapply(bundle, nrow, integer(1)),
    cols = vapply(bundle, ncol, integer(1)),
    stringsAsFactors = FALSE
  )
}
