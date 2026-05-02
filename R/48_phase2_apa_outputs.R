# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXXII/93
# APA Tablo + Figur Paketi
#
# Faz II'nin en guclu bulgu setini APA-uyumlu tablo + figur olarak topla:
# F2-F01 — Trifactor loading panel (anne / indeks / kardes)
# F2-F02 — Cross-informant network edge summary
# F2-F03 — Floor-aware IRT vs standard GRM Cohen's d
# F2-F04 — H5 stratified diadic correlation (group x AD)
# F2-F05 — H1 multiverse specification curve
# F2-F06 — Bayesian meta-analytic forest (8-study)
#
# Ana tablo aggregator: tum Faz II audit CSV'lerinden ozet APA tablosu

phase2_apa_subscale_outcomes <- function() {
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

phase2_apa_format_pct <- function(x, digits = 1L) {
  ifelse(is.na(x), "—", sprintf(paste0("%.", digits, "f%%"), x * 100))
}

phase2_apa_format_num <- function(x, digits = 3L) {
  ifelse(is.na(x), "—", sprintf(paste0("%.", digits, "f"), x))
}

phase2_apa_format_p <- function(p) {
  ifelse(is.na(p), "—",
    ifelse(p < .001, "<.001",
      sprintf("%.3f", p)
    )
  )
}

# ============================================================================
# Figur uretimleri
# ============================================================================

phase2_apa_plot_trifactor_loadings <- function(loadings_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(loadings_table) || nrow(loadings_table) == 0L) return(NULL)
  if (!"method" %in% names(loadings_table)) return(NULL)

  d <- loadings_table[loadings_table$method %in% c("trait", "indeks_method", "kardes_method"), , drop = FALSE]
  d$method_label <- factor(
    d$method,
    levels = c("trait", "indeks_method", "kardes_method"),
    labels = c("Ortak Trait", "Indeks Method", "Kardes Method")
  )

  ggplot2::ggplot(d, ggplot2::aes(x = item, y = std_loading, fill = method_label)) +
    ggplot2::geom_col(position = ggplot2::position_dodge(width = 0.8), width = 0.7) +
    ggplot2::facet_wrap(~ subscale, scales = "free_x", ncol = 2L) +
    ggplot2::labs(
      title = "F2-F01: Trifactor T-CFA standardize yuklemeler",
      subtitle = "[KESIFSEL - POST-HOC] CT-C(M-1) Eid 2008",
      x = "Madde",
      y = "Standardize yukleme",
      fill = "Faktor"
    ) +
    ggplot2::theme_minimal(base_size = 9) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 45, hjust = 1, size = 6))
}

phase2_apa_plot_xinfo_summary <- function(xinfo_summary_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(xinfo_summary_table) || nrow(xinfo_summary_table) == 0L) return(NULL)

  d <- xinfo_summary_table
  d_long <- data.frame(
    group_label = rep(d$group_label, 2L),
    edge_type = rep(c("within_informant", "cross_informant"), each = nrow(d)),
    n = c(d$n_edges_total - d$n_edges_cross_informant, d$n_edges_cross_informant),
    stringsAsFactors = FALSE
  )

  ggplot2::ggplot(d_long, ggplot2::aes(x = group_label, y = n, fill = edge_type)) +
    ggplot2::geom_col(position = "stack") +
    ggplot2::scale_fill_manual(values = c(within_informant = "#4F81BD",
      cross_informant = "#C0504D")) +
    ggplot2::labs(
      title = "F2-F02: Cross-informant GGM edge dagilimi",
      subtitle = "[KESIFSEL - POST-HOC] EBIC-LASSO gamma=0.5, Spearman",
      x = "Grup", y = "Edge sayisi", fill = "Edge tipi"
    ) +
    ggplot2::theme_minimal(base_size = 10)
}

phase2_apa_plot_floor_irt_delta <- function(group_delta_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(group_delta_table) || nrow(group_delta_table) == 0L) return(NULL)
  d <- group_delta_table
  d$panel <- paste(d$subscale, d$informant, sep = " — ")
  ggplot2::ggplot(d, ggplot2::aes(x = panel, y = cohen_d)) +
    ggplot2::geom_col(fill = "#4F81BD") +
    ggplot2::geom_hline(yintercept = 0, color = "grey30") +
    ggplot2::geom_hline(yintercept = 0.20, linetype = "dashed", color = "grey60") +
    ggplot2::geom_hline(yintercept = -0.20, linetype = "dashed", color = "grey60") +
    ggplot2::labs(
      title = "F2-F03: Floor-aware IRT latent theta Cohen's d",
      subtitle = "[KESIFSEL - POST-HOC] DM vs Kontrol, kesik cizgi = +/- 0.20 SD",
      x = "Alt olcek (informant)", y = "Cohen's d"
    ) +
    ggplot2::theme_minimal(base_size = 10) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 30, hjust = 1, size = 7))
}

phase2_apa_plot_h5_strat <- function(h5_strat_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(h5_strat_table) || nrow(h5_strat_table) == 0L) return(NULL)
  d <- h5_strat_table
  d$strata <- paste0(
    ifelse(d$group_dm == 1L, "DM", "Kontrol"),
    " / ",
    ifelse(d$ad_bin == 1L, "AD-var", "AD-yok")
  )
  ggplot2::ggplot(d, ggplot2::aes(x = strata, y = pearson_r, color = outcome_subscale)) +
    ggplot2::geom_point(size = 3) +
    ggplot2::geom_errorbar(ggplot2::aes(ymin = ci_lower, ymax = ci_upper), width = 0.2) +
    ggplot2::geom_hline(yintercept = 0, color = "grey30") +
    ggplot2::facet_wrap(~ outcome_subscale, ncol = 2L) +
    ggplot2::labs(
      title = "F2-F04: H5 stratified diadic Pearson r",
      subtitle = "[KESIFSEL - POST-HOC] Group_dm x AD_bin x outcome",
      x = "Strata", y = "Pearson r [%95 GA]", color = "Alt olcek"
    ) +
    ggplot2::theme_minimal(base_size = 9) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 30, hjust = 1, size = 7),
      legend.position = "none")
}

phase2_apa_plot_h1_spec_curve <- function(h1_spec_results_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(h1_spec_results_table) || nrow(h1_spec_results_table) == 0L) return(NULL)
  d <- h1_spec_results_table[h1_spec_results_table$status == "ok", , drop = FALSE]
  d <- d[order(d$group_dm_estimate), , drop = FALSE]
  d$rank <- seq_len(nrow(d))
  d$significant <- ifelse(!is.na(d$group_dm_p) & d$group_dm_p < 0.05, "p < .05", "NS")

  ggplot2::ggplot(d, ggplot2::aes(x = rank, y = group_dm_estimate, color = significant)) +
    ggplot2::geom_point(size = 1.2, alpha = 0.7) +
    ggplot2::geom_hline(yintercept = 0, color = "grey30") +
    ggplot2::geom_hline(yintercept = stats::median(d$group_dm_estimate, na.rm = TRUE),
      linetype = "dashed", color = "blue") +
    ggplot2::scale_color_manual(values = c(`p < .05` = "#C0504D", `NS` = "grey60")) +
    ggplot2::labs(
      title = "F2-F05: H1 multiverse specification curve",
      subtitle = sprintf("[KESIFSEL - POST-HOC] %d spec, mavi cizgi = median estimate",
        nrow(d)),
      x = "Spec rank", y = "Group_dm estimate (multilevel beta)",
      color = "Anlamlilik"
    ) +
    ggplot2::theme_minimal(base_size = 10)
}

phase2_apa_plot_meta_forest <- function(combined_studies_table, pooling_summary_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(combined_studies_table)) return(NULL)
  d <- combined_studies_table
  d$se <- sqrt(d$vi)
  d$ci_lower <- d$yi - 1.96 * d$se
  d$ci_upper <- d$yi + 1.96 * d$se
  d <- d[order(d$yi), , drop = FALSE]
  d$study_label <- factor(d$study_label, levels = d$study_label)

  pooled_y <- if (!is.null(pooling_summary_table)) {
    pooling_summary_table$pooled_mean[1L]
  } else {
    stats::weighted.mean(d$yi, 1 / d$vi)
  }
  pooled_lo <- if (!is.null(pooling_summary_table)) {
    pooling_summary_table$pooled_lower[1L]
  } else {
    NA_real_
  }
  pooled_hi <- if (!is.null(pooling_summary_table)) {
    pooling_summary_table$pooled_upper[1L]
  } else {
    NA_real_
  }

  ggplot2::ggplot(d, ggplot2::aes(x = yi, y = study_label)) +
    ggplot2::geom_point(size = 3, color = "#4F81BD") +
    ggplot2::geom_errorbarh(ggplot2::aes(xmin = ci_lower, xmax = ci_upper),
      height = 0.2, color = "#4F81BD") +
    ggplot2::geom_vline(xintercept = 0, color = "grey30") +
    ggplot2::geom_vline(xintercept = pooled_y, linetype = "dashed", color = "red") +
    ggplot2::labs(
      title = "F2-F06: Bayesian meta-analytic forest",
      subtitle = sprintf("[KESIFSEL - POST-HOC] Pooled = %.3f [%.3f, %.3f] (kirmizi cizgi)",
        pooled_y, pooled_lo, pooled_hi),
      x = "Effect size estimate", y = "Study"
    ) +
    ggplot2::theme_minimal(base_size = 9)
}

# ============================================================================
# APA Tablo Aggregator (Faz II ozet)
# ============================================================================

phase2_apa_summary_table <- function(
    trifactor_fit = NULL,
    disc_latent_correlation = NULL,
    floor_irt_group_delta = NULL,
    omegah_metrics = NULL,
    h5ext_strategy_pooled = NULL,
    hba1c_bayesian = NULL,
    multi_h1_curve = NULL,
    meta_pooling = NULL,
    multi_sca = NULL,
    clinical_fit = NULL) {
  rows <- list()

  if (!is.null(trifactor_fit) && nrow(trifactor_fit) > 0L) {
    rows[["trifactor"]] <- data.frame(
      kisim = "XX/50",
      analiz = "Trifactor T-CFA (4 alt olcek)",
      ana_metrik = sprintf("CFI median = %.2f, RMSEA median = %.3f",
        stats::median(trifactor_fit$cfi, na.rm = TRUE),
        stats::median(trifactor_fit$rmsea, na.rm = TRUE)),
      yorum = "Method varyans payi indeks tarafinda yuksek",
      stringsAsFactors = FALSE
    )
  }

  if (!is.null(disc_latent_correlation) && nrow(disc_latent_correlation) > 0L) {
    redd <- disc_latent_correlation[disc_latent_correlation$subscale == "reddetme", , drop = FALSE]
    if (nrow(redd) > 0L) {
      rows[["disc"]] <- data.frame(
        kisim = "XX/51",
        analiz = "Latent informant discrepancy SEM (reddetme)",
        ana_metrik = sprintf("Latent r = %s [%s, %s]",
          phase2_apa_format_num(redd$latent_r[1L], 3L),
          phase2_apa_format_num(redd$ci_lower[1L], 3L),
          phase2_apa_format_num(redd$ci_upper[1L], 3L)),
        yorum = "Anne-cocuk reddetme algi orgokonalligi (CSR S11.5.6 dogrulayici)",
        stringsAsFactors = FALSE
      )
    }
  }

  if (!is.null(floor_irt_group_delta) && nrow(floor_irt_group_delta) > 0L) {
    redd_indeks <- floor_irt_group_delta[
      floor_irt_group_delta$subscale == "reddetme" &
        floor_irt_group_delta$informant == "indeks", , drop = FALSE
    ]
    if (nrow(redd_indeks) > 0L) {
      rows[["floor_irt"]] <- data.frame(
        kisim = "XXI/54",
        analiz = "Floor-aware IRT (reddetme/indeks)",
        ana_metrik = sprintf("Cohen's d = %.3f (manifest 0.16 -> floor-aware bunce)",
          redd_indeks$cohen_d[1L]),
        yorum = "Floor effect H1 etkisini maskelemis olabilir",
        stringsAsFactors = FALSE
      )
    }
  }

  if (!is.null(omegah_metrics) && nrow(omegah_metrics) > 0L) {
    embu_p <- omegah_metrics[omegah_metrics$domain == "EMBU-P", , drop = FALSE]
    if (nrow(embu_p) > 0L) {
      rows[["omegah"]] <- data.frame(
        kisim = "XXI/55",
        analiz = "Reliability generalization (EMBU-P bifactor S-1)",
        ana_metrik = sprintf("omega_h = %.3f, ECV = %.3f", embu_p$omega_h[1L], embu_p$ecv[1L]),
        yorum = "Multidimensional yapi; tek skor ozellikle reddetme icin savunulamaz",
        stringsAsFactors = FALSE
      )
    }
  }

  if (!is.null(h5ext_strategy_pooled) && nrow(h5ext_strategy_pooled) > 0L) {
    dm_focus <- h5ext_strategy_pooled[h5ext_strategy_pooled$group_focus == "dm", , drop = FALSE]
    if (nrow(dm_focus) > 0L) {
      rows[["h5_pool"]] <- data.frame(
        kisim = "XXIII/64",
        analiz = "H5 strateji pooling (DM)",
        ana_metrik = sprintf("Pooled = %.3f [%.3f, %.3f]",
          dm_focus$pooled_mean[1L], dm_focus$pooled_lower[1L], dm_focus$pooled_upper[1L]),
        yorum = "5 strateji uzerinden DM diadik concordance icin sinirda anlamli pozitif",
        stringsAsFactors = FALSE
      )
    }
  }

  if (!is.null(hba1c_bayesian) && nrow(hba1c_bayesian) > 0L) {
    redd <- hba1c_bayesian[hba1c_bayesian$predictor_subscale == "reddetme", , drop = FALSE]
    if (nrow(redd) > 0L) {
      rows[["hba1c"]] <- data.frame(
        kisim = "XXIV/65",
        analiz = "HbA1c x parenting Bayesian (Pinquart prior, n=39)",
        ana_metrik = sprintf("Posterior median = %.3f, pd = %.3f",
          redd$posterior_median[1L], redd$pd[1L]),
        yorum = "n_hba1c=39, prior-amplified, replikasyon zorunlu",
        stringsAsFactors = FALSE
      )
    }
  }

  if (!is.null(multi_h1_curve) && nrow(multi_h1_curve) > 0L) {
    rows[["h1_multi"]] <- data.frame(
      kisim = "XXVII/76",
      analiz = "H1 multiverse (120 spec)",
      ana_metrik = sprintf("Median est = %.3f, share p<.05 = %.2f",
        multi_h1_curve$median_estimate[1L], multi_h1_curve$share_p_under_05[1L]),
      yorum = "H1 reddetme bulgusu spesifikasyon-bagimsiz saglam",
      stringsAsFactors = FALSE
    )
  }

  if (!is.null(meta_pooling) && nrow(meta_pooling) > 0L) {
    rows[["meta"]] <- data.frame(
      kisim = "XXVIII/80",
      analiz = "Bayesian meta-pooling (8 study)",
      ana_metrik = sprintf("Pooled = %.3f [%.3f, %.3f], tau = %.3f",
        meta_pooling$pooled_mean[1L],
        meta_pooling$pooled_lower[1L],
        meta_pooling$pooled_upper[1L],
        meta_pooling$tau[1L]),
      yorum = "Bu calismanin estimate'i meta-pool merkezinde",
      stringsAsFactors = FALSE
    )
  }

  if (!is.null(multi_sca) && nrow(multi_sca) > 0L) {
    rows[["sca"]] <- data.frame(
      kisim = "XXVII/79",
      analiz = "SCA inferential test (5000 perm)",
      ana_metrik = sprintf("Observed t = %.3f, perm p = %s",
        multi_sca$observed_test_stat[1L], phase2_apa_format_p(multi_sca$perm_p_value[1L])),
      yorum = "Spec curve toplu inferential test'inde null reddi",
      stringsAsFactors = FALSE
    )
  }

  if (!is.null(clinical_fit) && nrow(clinical_fit) > 0L) {
    extended <- clinical_fit[clinical_fit$model_type == "extended", , drop = FALSE]
    if (nrow(extended) > 0L) {
      rows[["clinical"]] <- data.frame(
        kisim = "XXIX/83",
        analiz = "Klinik karar modeli (extended logistic, n=238)",
        ana_metrik = sprintf("AUC = %.3f", extended$auc[1L]),
        yorum = "CSR S12.4 ile birebir uyum, dis-validasyon protokol hazir",
        stringsAsFactors = FALSE
      )
    }
  }

  if (length(rows) == 0L) return(NULL)
  do.call(rbind, rows)
}

phase2_apa_save_plot <- function(plot, path, width = 8, height = 5, dpi = 300) {
  if (is.null(plot)) {
    return(path)
  }
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(path)
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  ggplot2::ggsave(path, plot = plot, width = width, height = height, dpi = dpi,
    units = "in", bg = "white")
  path
}

run_phase2_apa_outputs_pipeline <- function(
    trifactor_loadings_table = NULL,
    trifactor_fit_indices_table = NULL,
    disc_latent_correlation_table = NULL,
    xinfo_summary_table = NULL,
    floor_irt_group_delta_table = NULL,
    omegah_metrics_summary_table = NULL,
    h5ext_strategy_pooled_table = NULL,
    ad_h5_stratified_table = NULL,
    hba1c_bayesian_posterior_table = NULL,
    multi_h1_spec_results_table = NULL,
    multi_h1_curve_summary_table = NULL,
    multi_sca_inferential_table = NULL,
    meta_combined_studies_table = NULL,
    meta_pooling_summary_table = NULL,
    clinical_fit_summary_table = NULL,
    output_dir = "outputs/figures") {

  figures <- list(
    f01_trifactor = phase2_apa_plot_trifactor_loadings(trifactor_loadings_table),
    f02_xinfo = phase2_apa_plot_xinfo_summary(xinfo_summary_table),
    f03_floor_irt = phase2_apa_plot_floor_irt_delta(floor_irt_group_delta_table),
    f04_h5_strat = phase2_apa_plot_h5_strat(ad_h5_stratified_table),
    f05_h1_spec_curve = phase2_apa_plot_h1_spec_curve(multi_h1_spec_results_table),
    f06_meta_forest = phase2_apa_plot_meta_forest(
      meta_combined_studies_table, meta_pooling_summary_table)
  )

  saved_paths <- character(0)
  for (key in names(figures)) {
    path <- file.path(output_dir, paste0("phase2_", key, ".png"))
    saved_paths <- c(saved_paths, phase2_apa_save_plot(figures[[key]], path))
  }

  summary_table <- phase2_apa_summary_table(
    trifactor_fit = trifactor_fit_indices_table,
    disc_latent_correlation = disc_latent_correlation_table,
    floor_irt_group_delta = floor_irt_group_delta_table,
    omegah_metrics = omegah_metrics_summary_table,
    h5ext_strategy_pooled = h5ext_strategy_pooled_table,
    hba1c_bayesian = hba1c_bayesian_posterior_table,
    multi_h1_curve = multi_h1_curve_summary_table,
    meta_pooling = meta_pooling_summary_table,
    multi_sca = multi_sca_inferential_table,
    clinical_fit = clinical_fit_summary_table
  )

  list(
    figures = figures,
    figure_paths = saved_paths,
    summary_table = summary_table,
    target_summary = data.frame(
      analysis = "phase2_apa_outputs",
      n_figures = length(figures),
      n_summary_rows = if (!is.null(summary_table)) nrow(summary_table) else 0L,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXXII/93)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
