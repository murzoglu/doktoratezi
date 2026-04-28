# KISIM XIII / 41 — Tez bölüm-artefakt eşlemesi

thesis_chapter_mapping <- function() {
  data.frame(
    chapter = c("01_giris", "02_yontem", "03_bulgular", "04_tartisma", "05_sonuc"),
    path = file.path("chapters", c("01_giris.qmd", "02_yontem.qmd", "03_bulgular.qmd", "04_tartisma.qmd", "05_sonuc.qmd")),
    role = c(
      "Kuramsal gerekçe ve hipotez çerçevesi",
      "Açık bilim, veri katmanı ve analiz protokolü",
      "H1-H5 + KISIM VI-XII bulgu, figür ve APA tabloları",
      "Literatür sentezi, sınırlılıklar ve klinik yorum sınırı",
      "Ana sonuç ve gelecek faz önerileri"
    ),
    required_artifact = c(
      "Hipotez metni",
      "Yöntem protokolü",
      "24 figür + 22 APA tablo",
      "Tartışma/sınırlılık metni",
      "Sonuç metni"
    ),
    stringsAsFactors = FALSE
  )
}

thesis_mapping_checks <- function(chapter_mapping, figure_manifest, table_manifest,
                                  thesis_html = "outputs/quarto/thesis.html") {
  chapter_exists <- file.exists(chapter_mapping$path)
  html_exists <- file.exists(thesis_html)
  html <- if (html_exists) paste(readLines(thesis_html, warn = FALSE, encoding = "UTF-8"), collapse = "\n") else ""

  figure_ids <- c(
    "fig-strobe-flow", "fig-causal-dag", "fig-smd-love", "fig-propensity-overlap",
    "fig-ses-correlation", "fig-h1-forest", "fig-h1-three-way-emm", "fig-h2-apim-path",
    "fig-h3-stratified-forest", "fig-h4-sem-path", "fig-h5-bland-altman", "fig-h5-rsa-surface",
    "fig-mediation-effects", "fig-lpa-fit-indices", "fig-network-graph", "fig-network-nct",
    "fig-clinical-roc", "fig-clinical-dca", "fig-clinical-calibration", "fig-clinical-cart-rf",
    "fig-specification-curve", "fig-sensemakr-contour", "fig-bayesian-forest", "fig-bayesian-diagnostics"
  )
  table_ids <- c(
    "tbl-apa-sample-characteristics", "tbl-apa-covariate-balance", "tbl-apa-missing-data",
    "tbl-apa-propensity-model", "tbl-apa-ses-composite", "tbl-apa-h1-primary",
    "tbl-apa-h1-bayesian", "tbl-apa-h2-family-mean", "tbl-apa-h2-apim",
    "tbl-apa-h3-primary-iptw", "tbl-apa-h3-sensitivity", "tbl-apa-h4-sem",
    "tbl-apa-h5-concordance", "tbl-apa-mediation", "tbl-apa-lpa-bifactor",
    "tbl-apa-network", "tbl-apa-clinical", "tbl-apa-dm-clinical",
    "tbl-apa-robustness", "tbl-apa-sensitivity", "tbl-apa-bayesian-global",
    "tbl-apa-result-synthesis"
  )

  checks <- data.frame(
    check_id = c(
      "chapters_exist",
      "figure_manifest_complete",
      "table_manifest_complete",
      "html_render_exists",
      "html_contains_figure_refs",
      "html_contains_table_refs"
    ),
    expected = c(
      nrow(chapter_mapping),
      24L,
      22L,
      1L,
      length(figure_ids),
      length(table_ids)
    ),
    observed = c(
      sum(chapter_exists),
      nrow(figure_manifest),
      nrow(table_manifest),
      as.integer(html_exists),
      sum(vapply(figure_ids, grepl, logical(1), x = html, fixed = TRUE)),
      sum(vapply(table_ids, grepl, logical(1), x = html, fixed = TRUE))
    ),
    stringsAsFactors = FALSE
  )
  checks$status <- ifelse(checks$expected == checks$observed, "verified", "review")
  checks
}

thesis_mapping_manifest <- function(chapter_mapping, checks) {
  data.frame(
    metric = c("chapters", "verified_checks", "review_checks"),
    value = c(
      nrow(chapter_mapping),
      sum(checks$status == "verified"),
      sum(checks$status != "verified")
    ),
    stringsAsFactors = FALSE
  )
}
