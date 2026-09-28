# KISIM XIII / 41 — Tez bölüm-artefakt eşlemesi

thesis_chapter_mapping <- function() {
  data.frame(
    chapter = c("01_giris_ve_amac", "02_genel_bilgiler", "03_gerec_ve_yontem", "04_bulgular", "05_tartisma_ve_sonuc"),
    path = file.path("chapters", c("01_giris_ve_amac.qmd", "02_genel_bilgiler.qmd", "03_gerec_ve_yontem.qmd", "04_bulgular.qmd", "05_tartisma_ve_sonuc.qmd")),
    role = c(
      "Kuramsal gerekçe ve hipotez çerçevesi",
      "Kavramsal ve klinik arka plan",
      "Açık bilim, veri katmanı ve analiz protokolü",
      "Word-onaylı H1-H5, seçilmiş keşifsel bulgular ve karma sentez",
      "Tartışma, sınırlılıklar, sonuç ve gelecek faz önerileri"
    ),
    required_artifact = c(
      "Hipotez metni",
      "Genel bilgiler metni",
      "Yöntem protokolü",
      "7 seçilmiş şekil + 6 kaynak-okumalı sayısal tablo + 2 sentez tablosu",
      "Tartışma/sınırlılık/sonuç metni"
    ),
    stringsAsFactors = FALSE
  )
}

thesis_mapping_checks <- function(chapter_mapping, figure_manifest, table_manifest,
                                  thesis_html = "outputs/quarto/thesis.html") {
  chapter_exists <- file.exists(chapter_mapping$path)
  html_exists <- file.exists(thesis_html)
  html <- if (html_exists) paste(readLines(thesis_html, warn = FALSE, encoding = "UTF-8"), collapse = "\n") else ""

  html_figure_ids <- c(
    "fig-strobe-flow", "fig-causal-dag", "fig-h1-forest",
    "fig-h5-bland-altman", "fig-h5-rsa-surface", "fig-network-graph",
    "fig-clinical-roc"
  )
  table_ids <- c(
    "tbl-apa-sample-characteristics", "tbl-apa-h1-group",
    "tbl-apa-h2-family-mean", "tbl-apa-h2-apim", "tbl-apa-h3-primary-iptw",
    "tbl-apa-h4-sem", "tbl-nitel-tema-ayrisma", "tbl-apa-result-synthesis"
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
      26L,
      1L,
      length(html_figure_ids),
      length(table_ids)
    ),
    observed = c(
      sum(chapter_exists),
      nrow(figure_manifest),
      nrow(table_manifest),
      as.integer(html_exists),
      sum(vapply(html_figure_ids, grepl, logical(1), x = html, fixed = TRUE)),
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
