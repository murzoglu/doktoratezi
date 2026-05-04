reporting_status_levels <- function() {
  c("planned", "drafted", "implemented", "verified", "not_applicable")
}

reporting_priority_levels <- function() {
  c("required", "recommended", "contextual")
}

reporting_framework_registry <- function() {
  data.frame(
    framework = c("STROBE", "CONSORT-Mixed", "JARS-Mixed"),
    scope = c(
      "Observational case-control reporting",
      "Mixed-methods participant and integration flow",
      "APA quantitative, qualitative, and mixed-methods reporting"
    ),
    primary_artifact = c(
      "thesis methods/results/discussion tables",
      "participant flow figure and integration timing note",
      "manuscript-style reporting checklist"
    ),
    stringsAsFactors = FALSE
  )
}

reporting_standards_checklist <- function() {
  data.frame(
    framework = c(
      rep("STROBE", 12),
      rep("CONSORT-Mixed", 7),
      rep("JARS-Mixed", 8)
    ),
    item = c(
      "STROBE-01",
      "STROBE-02",
      "STROBE-03",
      "STROBE-04",
      "STROBE-05",
      "STROBE-06",
      "STROBE-07",
      "STROBE-08",
      "STROBE-09",
      "STROBE-10",
      "STROBE-11",
      "STROBE-12",
      "CONSORT-MIXED-01",
      "CONSORT-MIXED-02",
      "CONSORT-MIXED-03",
      "CONSORT-MIXED-04",
      "CONSORT-MIXED-05",
      "CONSORT-MIXED-06",
      "CONSORT-MIXED-07",
      "JARS-MIXED-01",
      "JARS-MIXED-02",
      "JARS-MIXED-03",
      "JARS-MIXED-04",
      "JARS-MIXED-05",
      "JARS-MIXED-06",
      "JARS-MIXED-07",
      "JARS-MIXED-08"
    ),
    domain = c(
      "Title and abstract",
      "Background and objectives",
      "Study design and setting",
      "Participants and eligibility",
      "Variables and measurement",
      "Bias and confounding",
      "Study size",
      "Statistical methods",
      "Participant flow",
      "Descriptive and outcome data",
      "Main results and sensitivity analyses",
      "Limitations and generalisability",
      "Eligibility flow",
      "Recruitment and refusal accounting",
      "Exclusions and missing phases",
      "Quantitative sample",
      "Qualitative subset",
      "Integration timing",
      "Joint display plan",
      "Mixed-methods design statement",
      "Participant and sampling description",
      "Quantitative measures",
      "Qualitative data collection",
      "Integration rationale",
      "Researcher reflexivity",
      "Ethics and data protection",
      "Transparency and reproducibility"
    ),
    requirement = c(
      "Identify the observational case-control design in the thesis front matter and abstract.",
      "State clinical-developmental rationale and preregistered H1-H5 objectives.",
      "Describe retrospective secondary-data design, setting, dates, and family structure.",
      "Report eligibility criteria, recruitment source, group definitions, and sibling pairing.",
      "Define outcomes, exposures, predictors, confounders, and instrument scoring boundaries.",
      "Describe selection bias, family clustering, missingness, and confounding controls.",
      "Report fixed available sample and any analyzable-set changes after canonical lock.",
      "Report estimators, confidence intervals, family clustering, missing-data handling, and sensitivity analyses.",
      "Report numbers through eligibility, inclusion, exclusions, and analysis sets.",
      "Report demographics, clinical descriptors, scale distributions, and missingness.",
      "Report adjusted estimates with effect sizes, confidence intervals, and sensitivity results.",
      "Discuss bias, measurement limitations, external validity, and preregistration deviations.",
      "Show invited, eligible, included, excluded, and analyzed families.",
      "Separate refusal, incomplete, and unavailable records when information exists.",
      "Document quantitative and qualitative phase attrition separately.",
      "Show family-level and child-level quantitative denominators.",
      "Define qualitative subset selection and any non-participation.",
      "State whether qualitative interpretation follows or informs quantitative results.",
      "Plan a joint display linking H1-H5 quantitative findings to qualitative interpretation.",
      "Name the mixed-methods structure and justify secondary-data status.",
      "Describe family sampling, sibling structure, and participant roles.",
      "Document EMBU, BDI, SRQ/KIA and demographic/tibbi instruments with scoring decisions.",
      "Describe interview/transcript availability, anonymisation, and quotation rules if used.",
      "Explain how quantitative and qualitative strands are integrated in inference.",
      "State analyst role, prior clinical context, and bias-control procedure where applicable.",
      "Report ethics approval, consent boundary, OSF boundary, and row-level data access limits.",
      "Link OSF registrations, SAP, reproducibility runbook, lock file, and audit outputs."
    ),
    thesis_location = c(
      "Title page; abstract",
      "chapters/01_giris.qmd; chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd; chapters/04_tartisma.qmd",
      "chapters/02_yontem.qmd; chapters/03_bulgular.qmd",
      "chapters/02_yontem.qmd",
      "chapters/03_bulgular.qmd",
      "chapters/03_bulgular.qmd",
      "chapters/03_bulgular.qmd",
      "chapters/04_tartisma.qmd",
      "outputs/figures/consort_mixed_flow.*",
      "chapters/03_bulgular.qmd",
      "chapters/03_bulgular.qmd",
      "chapters/03_bulgular.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd; chapters/04_tartisma.qmd",
      "chapters/03_bulgular.qmd; chapters/04_tartisma.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd",
      "chapters/04_tartisma.qmd",
      "chapters/04_tartisma.qmd",
      "chapters/02_yontem.qmd",
      "chapters/02_yontem.qmd; docs/analiz_planlari"
    ),
    artifact = c(
      "thesis.qmd",
      "docs/analiz_planlari/03-sap-ana-plan.md",
      "docs/analiz_planlari/03-sap-ana-plan.md",
      "docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md",
      "docs/protokol/KANONIK_*.md",
      "docs/analiz_planlari/02-sapma-tablosu.md",
      "data/processed/FINAL_REFERENCE__CANONICAL_ANALYSIS_BASE.lock",
      "docs/analiz_planlari/03-sap-ana-plan.md",
      "outputs/figures/consort_mixed_flow.*",
      "outputs/tables/table1_descriptives.*",
      "outputs/tables/hypothesis_results.*",
      "docs/analiz_planlari/02-sapma-tablosu.md",
      "outputs/figures/consort_mixed_flow.*",
      "outputs/tables/participant_flow.*",
      "outputs/tables/participant_flow.*",
      "outputs/tables/participant_flow.*",
      "docs/analiz_planlari/03-sap-ana-plan.md",
      "docs/analiz_planlari/03-sap-ana-plan.md",
      "outputs/tables/joint_display.*",
      "docs/analiz_planlari/03-sap-ana-plan.md",
      "docs/protokol/FINAL_REFERENCE_VERI_HARITASI.md",
      "docs/protokol/KANONIK_*.md",
      "docs/analiz_planlari/17-etik-veri-yonetimi-plani.md",
      "outputs/tables/joint_display.*",
      "chapters/04_tartisma.qmd",
      "docs/analiz_planlari/17-etik-veri-yonetimi-plani.md",
      "docs/analiz_planlari/19-reproduktivite-runbook.md"
    ),
    status = c(
      "planned",
      "drafted",
      "drafted",
      "drafted",
      "drafted",
      "drafted",
      "verified",
      "drafted",
      "planned",
      "planned",
      "planned",
      "planned",
      "planned",
      "planned",
      "planned",
      "planned",
      "drafted",
      "drafted",
      "planned",
      "drafted",
      "drafted",
      "drafted",
      "drafted",
      "planned",
      "planned",
      "drafted",
      "drafted"
    ),
    priority = c(
      rep("required", 12),
      rep("required", 7),
      "required",
      "required",
      "required",
      "required",
      "required",
      "recommended",
      "required",
      "required"
    ),
    stringsAsFactors = FALSE
  )
}

validate_reporting_standards_checklist <- function(checklist) {
  required_columns <- c(
    "framework",
    "item",
    "domain",
    "requirement",
    "thesis_location",
    "artifact",
    "status",
    "priority"
  )
  missing_columns <- setdiff(required_columns, names(checklist))
  if (length(missing_columns) > 0L) {
    stop(
      sprintf("Reporting checklist is missing column(s): %s", paste(missing_columns, collapse = ", ")),
      call. = FALSE
    )
  }

  missing_frameworks <- setdiff(
    reporting_framework_registry()$framework,
    unique(checklist$framework)
  )
  if (length(missing_frameworks) > 0L) {
    stop(
      sprintf("Reporting checklist is missing framework(s): %s", paste(missing_frameworks, collapse = ", ")),
      call. = FALSE
    )
  }

  invalid_status <- setdiff(unique(checklist$status), reporting_status_levels())
  if (length(invalid_status) > 0L) {
    stop(
      sprintf("Invalid reporting status value(s): %s", paste(invalid_status, collapse = ", ")),
      call. = FALSE
    )
  }

  invalid_priority <- setdiff(unique(checklist$priority), reporting_priority_levels())
  if (length(invalid_priority) > 0L) {
    stop(
      sprintf("Invalid reporting priority value(s): %s", paste(invalid_priority, collapse = ", ")),
      call. = FALSE
    )
  }

  duplicate_keys <- duplicated(paste(checklist$framework, checklist$item, sep = "::"))
  if (any(duplicate_keys)) {
    stop("Reporting checklist contains duplicate framework-item keys", call. = FALSE)
  }

  empty_required_values <- vapply(
    required_columns,
    function(column) any(is.na(checklist[[column]]) | !nzchar(trimws(checklist[[column]]))),
    logical(1)
  )
  if (any(empty_required_values)) {
    stop(
      sprintf("Reporting checklist has empty value(s) in: %s", paste(names(empty_required_values)[empty_required_values], collapse = ", ")),
      call. = FALSE
    )
  }

  invisible(TRUE)
}

summarize_reporting_standards <- function(checklist = reporting_standards_checklist()) {
  validate_reporting_standards_checklist(checklist)
  summary <- stats::aggregate(
    item ~ framework + status,
    data = checklist,
    FUN = length
  )
  names(summary)[names(summary) == "item"] <- "n"
  summary[order(summary$framework, summary$status), , drop = FALSE]
}

reporting_standards_findings <- function(checklist = reporting_standards_checklist()) {
  validate_reporting_standards_checklist(checklist)
  open <- checklist[
    checklist$priority == "required" &
      !(checklist$status %in% c("implemented", "verified", "not_applicable")),
    ,
    drop = FALSE
  ]

  if (nrow(open) == 0L) {
    return(data.frame(
      framework = character(),
      item = character(),
      severity = character(),
      status = character(),
      finding = character(),
      stringsAsFactors = FALSE
    ))
  }

  data.frame(
    framework = open$framework,
    item = open$item,
    severity = "review",
    status = open$status,
    finding = "Required reporting item is not yet implemented or verified in the manuscript.",
    stringsAsFactors = FALSE
  )
}
