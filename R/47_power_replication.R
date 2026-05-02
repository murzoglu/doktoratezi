# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXX/87-89
# Power Analizleri (Mevcut Veri Tabanli)
#
# 87 — simr multilevel power simulation: simr yoksa manuel Monte Carlo
#      lme4 fit + p-value count. CSR n=241 ornekleminin guc karakterizasyonu
#      icin kullanilir.
#
# 88 — APIM sample size (Ackerman & Kenny 2016): pwr formulu + dyad
#      duzeltmesi. dyadic = 0.85 * independent (orta correlation 0.30).
#      Tezdeki H2 APIM bulgularinin guc-degerlendirmesi.
#
# 89 — Bayesian sample size determination (BSSD; Kruschke 2018):
#      ROPE = +/-0.10 SD; HDI %95 width target = 0.10. Manuel grid.
#      Mevcut n=241 ornekleminin BSSD eshiklerine gore degerlendirmesi.
#
# (Not: F2-90 cok-merkezli replikasyon protokolü yeni veri toplama
#  gerektirdigi icin Faz II'den cikarildi.)
#
# Skill referanslari: references/etki-buyuklugu-ve-guc.md

power_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

power_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

power_scale <- function(x) {
  m <- mean(x, na.rm = TRUE)
  s <- stats::sd(x, na.rm = TRUE)
  if (is.na(s) || s == 0) return(rep(NA_real_, length(x)))
  (x - m) / s
}

power_ensure_group_dm <- function(df) {
  if (!"group_dm" %in% names(df)) {
    if ("group_f" %in% names(df)) {
      df$group_dm <- as.integer(df$group_f) - 1L
    } else if ("grup" %in% names(df)) {
      df$group_dm <- as.integer(grepl("DM", as.character(df$grup), ignore.case = TRUE))
    }
  }
  df
}

# ============================================================================
# 87 — Multilevel Power Simulation (simr fallback: manuel MC)
# ============================================================================

power_simulate_multilevel <- function(n_aile_grid = c(100, 150, 200, 241, 300, 400),
                                       d_target = 0.20,
                                       icc_aile = 0.20,
                                       n_sim = 200L,
                                       alpha = 0.05,
                                       seed = 20260519L) {
  if (!requireNamespace("lme4", quietly = TRUE) ||
      !requireNamespace("lmerTest", quietly = TRUE)) {
    return(data.frame(
      n_aile = n_aile_grid,
      d_target = d_target,
      power = NA_real_,
      n_sim = n_sim,
      status = "lme4_unavailable",
      stringsAsFactors = FALSE
    ))
  }
  set.seed(seed)
  rows <- vector("list", length(n_aile_grid))
  for (i in seq_along(n_aile_grid)) {
    n_aile <- n_aile_grid[i]
    n_per_aile <- 2L  # indeks + kardes
    n_total <- n_aile * n_per_aile
    p_under_05 <- 0L
    fits_completed <- 0L
    for (k in seq_len(n_sim)) {
      group_dm <- rep(c(0L, 1L), length.out = n_aile)
      aile_no <- rep(seq_len(n_aile), each = n_per_aile)
      group_dm_long <- rep(group_dm, each = n_per_aile)
      # ICC = sigma_aile^2 / (sigma_aile^2 + sigma_resid^2)
      sigma_aile_sq <- icc_aile
      sigma_resid_sq <- 1 - icc_aile
      aile_re <- stats::rnorm(n_aile, 0, sqrt(sigma_aile_sq))
      y <- d_target * group_dm_long + aile_re[aile_no] +
        stats::rnorm(n_total, 0, sqrt(sigma_resid_sq))
      sim_data <- data.frame(y = y, group_dm = group_dm_long,
        aile_no = aile_no, stringsAsFactors = FALSE)
      fit <- tryCatch(
        suppressWarnings(suppressMessages(
          lmerTest::lmer(y ~ group_dm + (1 | aile_no), data = sim_data)
        )),
        error = function(e) NULL
      )
      if (is.null(fit)) next
      fits_completed <- fits_completed + 1L
      cs <- summary(fit)$coefficients
      if ("group_dm" %in% rownames(cs) &&
          cs["group_dm", "Pr(>|t|)"] < alpha) {
        p_under_05 <- p_under_05 + 1L
      }
    }
    power <- if (fits_completed > 0L) p_under_05 / fits_completed else NA_real_
    rows[[i]] <- data.frame(
      n_aile = n_aile,
      d_target = d_target,
      icc_aile = icc_aile,
      n_sim = n_sim,
      n_fits_completed = fits_completed,
      n_p_under_alpha = p_under_05,
      power = power,
      status = "ok",
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ============================================================================
# 88 — APIM Sample Size (Ackerman & Kenny 2016)
# ============================================================================

power_apim_sample_size <- function(rs = c(0.10, 0.20, 0.30, 0.40),
                                    powers = c(0.80, 0.90),
                                    alpha = 0.05,
                                    dyad_adjustment = 0.85) {
  if (!requireNamespace("pwr", quietly = TRUE)) {
    return(data.frame(r = rs[1], power = powers[1],
      n_independent = NA_real_, n_dyad = NA_real_,
      status = "pwr_unavailable", stringsAsFactors = FALSE))
  }
  rows <- list()
  for (r in rs) {
    for (pw in powers) {
      ind <- tryCatch(
        pwr::pwr.r.test(r = r, sig.level = alpha, power = pw),
        error = function(e) NULL
      )
      if (is.null(ind)) {
        rows[[length(rows) + 1L]] <- data.frame(
          r = r, power = pw, alpha = alpha,
          n_independent = NA_real_, n_dyad = NA_real_,
          dyad_adjustment = dyad_adjustment,
          status = "pwr_error", stringsAsFactors = FALSE
        )
        next
      }
      n_ind <- ceiling(ind$n)
      n_dyad <- ceiling(n_ind * dyad_adjustment)
      rows[[length(rows) + 1L]] <- data.frame(
        r = r, power = pw, alpha = alpha,
        n_independent = n_ind,
        n_dyad = n_dyad,
        dyad_adjustment = dyad_adjustment,
        status = "ok",
        stringsAsFactors = FALSE
      )
    }
  }
  do.call(rbind, rows)
}

# ============================================================================
# 89 — Bayesian Sample Size Determination (Kruschke 2018)
# ============================================================================

power_bayesian_ssd <- function(n_grid = c(100, 150, 200, 241, 300, 400, 500),
                                d_assumed = 0.16,
                                hdi_target_width = 0.20,
                                rope_half_width = 0.10,
                                n_sim = 100L,
                                seed = 20260519L) {
  set.seed(seed)
  rows <- list()
  for (n in n_grid) {
    hdi_widths <- numeric(n_sim)
    in_rope_decisions <- 0L
    for (k in seq_len(n_sim)) {
      group <- rep(c(0L, 1L), length.out = n)
      y <- d_assumed * group + stats::rnorm(n, 0, 1)
      # Posterior approximation: Normal with mean = OLS estimate, sd = SE
      fit <- stats::lm(y ~ group)
      cs <- summary(fit)$coefficients
      est <- cs["group", "Estimate"]
      se <- cs["group", "Std. Error"]
      hdi_lower <- est - 1.96 * se
      hdi_upper <- est + 1.96 * se
      hdi_widths[k] <- hdi_upper - hdi_lower
      # ROPE check
      if (hdi_lower > rope_half_width || hdi_upper < -rope_half_width) {
        in_rope_decisions <- in_rope_decisions + 1L
      }
    }
    rows[[length(rows) + 1L]] <- data.frame(
      n = n,
      d_assumed = d_assumed,
      hdi_target_width = hdi_target_width,
      rope_half_width = rope_half_width,
      n_sim = n_sim,
      mean_hdi_width = mean(hdi_widths),
      share_hdi_under_target = mean(hdi_widths < hdi_target_width),
      share_outside_rope = in_rope_decisions / n_sim,
      stringsAsFactors = FALSE
    )
  }
  do.call(rbind, rows)
}

# ============================================================================
# Pipeline
# ============================================================================

run_power_replication_pipeline <- function(
    n_aile_grid = c(100, 150, 200, 241, 300, 400),
    apim_rs = c(0.10, 0.20, 0.30, 0.40),
    apim_powers = c(0.80, 0.90),
    bssd_n_grid = c(100, 150, 200, 241, 300, 400, 500),
    multilevel_n_sim = 200L,
    bssd_n_sim = 100L,
    d_target = 0.20,
    icc_aile = 0.20,
    d_assumed_bayesian = 0.16) {

  multilevel_table <- power_simulate_multilevel(
    n_aile_grid = n_aile_grid,
    d_target = d_target,
    icc_aile = icc_aile,
    n_sim = multilevel_n_sim
  )

  apim_table <- power_apim_sample_size(
    rs = apim_rs,
    powers = apim_powers
  )

  bssd_table <- power_bayesian_ssd(
    n_grid = bssd_n_grid,
    d_assumed = d_assumed_bayesian,
    n_sim = bssd_n_sim
  )

  list(
    multilevel_power = multilevel_table,
    apim_sample_size = apim_table,
    bayesian_ssd = bssd_table,
    target_summary = data.frame(
      analysis = "power_phase2",
      n_aile_grid = paste(n_aile_grid, collapse = ","),
      multilevel_n_sim = multilevel_n_sim,
      bssd_n_sim = bssd_n_sim,
      simr_used = requireNamespace("simr", quietly = TRUE),
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXX/87-89)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
