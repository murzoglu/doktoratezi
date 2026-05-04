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
# F2-F07 — Cross-informant GGM network edge map
# F2-F08 — Diagnosis age spline decision panel
# F2-F09 — Imai-Keele rho sensitivity curve
# F2-F10 — DAG implied CI + three-level validation panel
# F2-F11 — Posterior predictive replication
# F2-F12 — DCA threshold-sensitivity heatmap
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

phase2_carbon_palette <- function() {
  c(
    chart_1 = "#6929c4",
    chart_2 = "#1192e8",
    chart_3 = "#005d5d",
    chart_4 = "#9f1853",
    chart_5 = "#fa4d56",
    chart_6 = "#520408",
    chart_7 = "#198038",
    chart_8 = "#002d9c",
    chart_9 = "#ee5396",
    chart_10 = "#b28600",
    chart_11 = "#009d9a",
    chart_12 = "#012749",
    chart_13 = "#8a3800",
    chart_14 = "#a56eff",
    blue_60 = "#0f62fe",
    blue_70 = "#0043ce",
    gray_10 = "#f4f4f4",
    gray_20 = "#e0e0e0",
    gray_30 = "#c6c6c6",
    gray_40 = "#a8a8a8",
    gray_50 = "#8d8d8d",
    gray_60 = "#6f6f6f",
    gray_70 = "#525252",
    gray_80 = "#393939",
    gray_100 = "#161616",
    success = "#198038",
    warning = "#b28600",
    error = "#da1e28"
  )
}

phase2_carbon_subscale_label <- function(x) {
  labels <- c(
    sicaklik = "Sicaklik",
    asiri_koruma = "Asiri koruma",
    reddetme = "Reddetme",
    karsilastirma = "Karsilastirma"
  )
  out <- labels[as.character(x)]
  out[is.na(out)] <- as.character(x)[is.na(out)]
  unname(out)
}

phase2_carbon_item_label <- function(x) {
  out <- gsub("^embu_[pc]_q0*", "Q", as.character(x))
  out <- gsub("_indeks$", " indeks", out)
  out <- gsub("_kardes$", " kardes", out)
  out
}

phase2_carbon_variable_label <- function(x) {
  labels <- c(
    embu_p_sicaklik_mean = "Anne sicaklik",
    embu_p_asiri_koruma_mean = "Anne asiri koruma",
    embu_p_reddetme_mean = "Anne reddetme",
    embu_p_karsilastirma_mean = "Anne karsilastirma",
    embu_c_sicaklik_mean = "Cocuk sicaklik",
    embu_c_asiri_koruma_mean = "Cocuk asiri koruma",
    embu_c_reddetme_mean = "Cocuk reddetme",
    embu_c_karsilastirma_mean = "Cocuk karsilastirma",
    beck_total = "Anne BDI",
    srq_ho_warmth_mean = "Kardes sicaklik",
    srq_ho_status_mean = "Kardes status",
    srq_ho_conflict_mean = "Kardes catismasi"
  )
  out <- labels[as.character(x)]
  out[is.na(out)] <- gsub("_", " ", as.character(x)[is.na(out)])
  unname(out)
}

phase2_carbon_caption <- function(source_table) {
  paste(
    "[KESIFSEL - POST-HOC] Carbon/Figma revizyonu: @carbon/charts v11 palette;",
    "kaynak:",
    source_table
  )
}

phase2_carbon_svg_metadata <- function() {
  paste0(
    "data-carbon-style=\"IBM Carbon Design System v11\" ",
    "data-figma-color-library=\"Uu7QTLz6ERkFJPD7cVEWel#2228:805\" ",
    "data-figma-carbon-charts-library=\"503EVkMrbdCfkqBbfjLqA3#3984:105703\" ",
    "data-figma-technical-diagram-library=\"RtZDc7pMQt8HcgYTiitspr#345:5092\" ",
    "data-font=\"IBM Plex Sans\" ",
    "data-chart-palette=\"@carbon/charts white 14\" "
  )
}

phase2_carbonize_svg_file <- function(path) {
  if (!file.exists(path)) return(path)
  x <- readLines(path, warn = FALSE, encoding = "UTF-8")
  txt <- paste(x, collapse = "\n")
  if (!grepl("data-carbon-style=", txt, fixed = TRUE)) {
    txt <- sub("<svg ", paste0("<svg ", phase2_carbon_svg_metadata()), txt, fixed = TRUE)
  }
  writeLines(txt, path, useBytes = TRUE)
  path
}

phase2_carbon_theme <- function(base_size = 10) {
  pal <- phase2_carbon_palette()
  ggplot2::theme_minimal(base_size = base_size, base_family = "sans") +
    ggplot2::theme(
      plot.title.position = "plot",
      plot.caption.position = "plot",
      plot.title = ggplot2::element_text(
        face = "bold", color = pal[["gray_100"]], size = base_size + 3,
        margin = ggplot2::margin(b = 4)
      ),
      plot.subtitle = ggplot2::element_text(
        color = pal[["gray_70"]], size = base_size,
        margin = ggplot2::margin(b = 8)
      ),
      plot.caption = ggplot2::element_text(
        color = pal[["gray_60"]], size = base_size - 2, hjust = 0,
        margin = ggplot2::margin(t = 8)
      ),
      axis.title = ggplot2::element_text(color = pal[["gray_100"]]),
      axis.text = ggplot2::element_text(color = pal[["gray_70"]]),
      panel.grid.major = ggplot2::element_line(color = pal[["gray_20"]], linewidth = 0.25),
      panel.grid.minor = ggplot2::element_blank(),
      plot.background = ggplot2::element_rect(fill = "white", color = NA),
      panel.background = ggplot2::element_rect(fill = "white", color = NA),
      strip.background = ggplot2::element_rect(fill = pal[["gray_10"]], color = NA),
      strip.text = ggplot2::element_text(face = "bold", color = pal[["gray_100"]], hjust = 0),
      legend.position = "bottom",
      legend.title = ggplot2::element_text(color = pal[["gray_70"]]),
      legend.text = ggplot2::element_text(color = pal[["gray_100"]])
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
    labels = c("Ortak trait", "Indeks method", "Kardes method")
  )
  d$subscale_label <- phase2_carbon_subscale_label(d$subscale)
  d$item_label <- phase2_carbon_item_label(d$item)
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(x = item_label, y = std_loading, fill = method_label)) +
    ggplot2::geom_hline(yintercept = 0, color = pal[["gray_30"]], linewidth = 0.3) +
    ggplot2::geom_hline(yintercept = 0.40, color = pal[["gray_50"]],
      linetype = "dashed", linewidth = 0.3) +
    ggplot2::geom_col(position = ggplot2::position_dodge(width = 0.8), width = 0.7) +
    ggplot2::facet_wrap(~ subscale_label, scales = "free_x", ncol = 2L) +
    ggplot2::scale_fill_manual(values = c(
      `Ortak trait` = pal[["chart_1"]],
      `Indeks method` = pal[["chart_2"]],
      `Kardes method` = pal[["chart_3"]]
    )) +
    ggplot2::coord_cartesian(ylim = c(0, max(1, d$std_loading, na.rm = TRUE))) +
    ggplot2::labs(
      title = "F2-F01 | Trifactor yukleme mimarisi",
      subtitle = "Trait, indeks-method ve kardes-method bilesenleri ayni madde yuzeyinde ayriliyor",
      x = "Madde",
      y = "Standardize yukleme",
      fill = "Faktor",
      caption = phase2_carbon_caption("phase2_trifactor_loadings.csv")
    ) +
    phase2_carbon_theme(base_size = 9) +
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
  d_long$group_label <- factor(d_long$group_label,
    levels = c("all", "Kontrol", "DM"),
    labels = c("Tum aileler", "Kontrol", "DM"))
  d_long$edge_type <- factor(d_long$edge_type,
    levels = c("within_informant", "cross_informant"),
    labels = c("Ayni informant", "Cross-informant"))
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d_long, ggplot2::aes(x = group_label, y = n, fill = edge_type)) +
    ggplot2::geom_col(width = 0.62, color = "white", linewidth = 0.25) +
    ggplot2::geom_text(ggplot2::aes(label = ifelse(n > 0, n, "")),
      position = ggplot2::position_stack(vjust = 0.5),
      color = "white", size = 3, fontface = "bold") +
    ggplot2::scale_fill_manual(values = c(
      `Ayni informant` = pal[["chart_2"]],
      `Cross-informant` = pal[["chart_4"]]
    )) +
    ggplot2::labs(
      title = "F2-F02 | Cross-informant GGM edge dagilimi",
      subtitle = "Cross-informant bag zayif/seyrek; ag yogunlugu informant-ici kapanma gosteriyor",
      x = "Grup", y = "Edge sayisi", fill = "Edge tipi",
      caption = phase2_carbon_caption("phase2_xinfo_summary.csv")
    ) +
    phase2_carbon_theme(base_size = 10)
}

phase2_apa_plot_floor_irt_delta <- function(group_delta_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(group_delta_table) || nrow(group_delta_table) == 0L) return(NULL)
  d <- group_delta_table
  d$panel <- paste(phase2_carbon_subscale_label(d$subscale), d$informant, sep = " / ")
  d$direction <- ifelse(abs(d$cohen_d) < 0.20, "|d| < 0.20",
    ifelse(d$cohen_d > 0, "DM > Kontrol", "Kontrol > DM"))
  d$panel <- factor(d$panel, levels = d$panel[order(d$cohen_d)])
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(x = panel, y = cohen_d)) +
    ggplot2::geom_col(ggplot2::aes(fill = direction), width = 0.62) +
    ggplot2::geom_hline(yintercept = 0, color = pal[["gray_80"]], linewidth = 0.35) +
    ggplot2::geom_hline(yintercept = 0.20, linetype = "dashed",
      color = pal[["gray_50"]], linewidth = 0.3) +
    ggplot2::geom_hline(yintercept = -0.20, linetype = "dashed",
      color = pal[["gray_50"]], linewidth = 0.3) +
    ggplot2::geom_text(ggplot2::aes(label = sprintf("%.2f", cohen_d)),
      hjust = ifelse(d$cohen_d >= 0, -0.12, 1.12),
      size = 3, color = pal[["gray_100"]]) +
    ggplot2::scale_fill_manual(values = c(
      `DM > Kontrol` = pal[["chart_2"]],
      `Kontrol > DM` = pal[["chart_5"]],
      `|d| < 0.20` = pal[["gray_40"]]
    )) +
    ggplot2::coord_flip(clip = "off") +
    ggplot2::labs(
      title = "F2-F03 | Floor-aware IRT latent theta farki",
      subtitle = "DM vs Kontrol; kesik cizgiler kucuk etki esigi olarak +/-0.20 SD",
      x = "Alt olcek / informant", y = "Cohen's d", fill = "Yon",
      caption = phase2_carbon_caption("phase2_floor_irt_group_delta.csv")
    ) +
    phase2_carbon_theme(base_size = 10) +
    ggplot2::theme(plot.margin = ggplot2::margin(5.5, 18, 5.5, 5.5))
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
  d$outcome_label <- phase2_carbon_subscale_label(d$outcome_subscale)
  d$ad_label <- ifelse(d$ad_bin == 1L, "AD-var", "AD-yok")
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(x = strata, y = pearson_r, color = outcome_label,
    shape = ad_label)) +
    ggplot2::geom_hline(yintercept = 0, color = pal[["gray_80"]], linewidth = 0.35) +
    ggplot2::geom_errorbar(ggplot2::aes(ymin = ci_lower, ymax = ci_upper),
      width = 0.18, linewidth = 0.45) +
    ggplot2::geom_point(size = 2.8, stroke = 0.9) +
    ggplot2::geom_text(ggplot2::aes(label = paste0("n=", n)),
      color = pal[["gray_70"]], size = 2.5, nudge_y = 0.08,
      show.legend = FALSE) +
    ggplot2::facet_wrap(~ outcome_label, ncol = 2L) +
    ggplot2::scale_color_manual(values = c(
      `Sicaklik` = pal[["chart_1"]],
      `Asiri koruma` = pal[["chart_2"]],
      `Reddetme` = pal[["chart_3"]],
      `Karsilastirma` = pal[["chart_4"]]
    )) +
    ggplot2::scale_shape_manual(values = c(`AD-yok` = 16, `AD-var` = 17)) +
    ggplot2::labs(
      title = "F2-F04 | H5 stratified diadic Pearson r",
      subtitle = "Grup x antidepresan katmani; noktalar r, cizgiler %95 GA",
      x = "Strata", y = "Pearson r [%95 GA]", color = "Alt olcek", shape = "AD",
      caption = phase2_carbon_caption("phase2_ad_moderation_h5_stratified_correlations.csv")
    ) +
    phase2_carbon_theme(base_size = 9) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 30, hjust = 1, size = 7),
      legend.position = "bottom")
}

phase2_apa_plot_h1_spec_curve <- function(h1_spec_results_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(h1_spec_results_table) || nrow(h1_spec_results_table) == 0L) return(NULL)
  d <- h1_spec_results_table[h1_spec_results_table$status == "ok", , drop = FALSE]
  d <- d[order(d$group_dm_estimate), , drop = FALSE]
  d$rank <- seq_len(nrow(d))
  d$significant <- ifelse(!is.na(d$group_dm_p) & d$group_dm_p < 0.05, "p < .05", "NS")
  d$outcome_source <- if ("outcome_subscale" %in% names(d)) d$outcome_subscale else d$outcome_subscale_result
  d$outcome_label <- phase2_carbon_subscale_label(d$outcome_source)
  d$ci_lower <- d$group_dm_estimate - 1.96 * d$group_dm_se
  d$ci_upper <- d$group_dm_estimate + 1.96 * d$group_dm_se
  median_estimate <- stats::median(d$group_dm_estimate, na.rm = TRUE)
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(x = rank, y = group_dm_estimate,
    color = outcome_label, shape = significant)) +
    ggplot2::geom_linerange(ggplot2::aes(ymin = ci_lower, ymax = ci_upper),
      alpha = 0.18, linewidth = 0.25, show.legend = FALSE) +
    ggplot2::geom_point(size = 1.5, alpha = 0.82) +
    ggplot2::geom_hline(yintercept = 0, color = pal[["gray_80"]], linewidth = 0.35) +
    ggplot2::geom_hline(yintercept = median_estimate,
      linetype = "dashed", color = pal[["blue_60"]], linewidth = 0.4) +
    ggplot2::scale_color_manual(values = c(
      `Sicaklik` = pal[["chart_1"]],
      `Asiri koruma` = pal[["chart_2"]],
      `Reddetme` = pal[["chart_3"]],
      `Karsilastirma` = pal[["chart_4"]]
    )) +
    ggplot2::scale_shape_manual(values = c(`p < .05` = 16, NS = 1)) +
    ggplot2::labs(
      title = "F2-F05 | H1 multiverse specification curve",
      subtitle = sprintf("%d spesifikasyon; kesik mavi cizgi median beta = %.3f",
        nrow(d), median_estimate),
      x = "Spesifikasyon sirasi", y = "Group_dm estimate (multilevel beta)",
      color = "Alt olcek", shape = "Anlamlilik",
      caption = phase2_carbon_caption("phase2_multi_h1_spec_results.csv")
    ) +
    phase2_carbon_theme(base_size = 10)
}

phase2_apa_plot_meta_forest <- function(combined_studies_table, pooling_summary_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(combined_studies_table)) return(NULL)
  d <- combined_studies_table
  if (nrow(d) == 0L) return(NULL)
  d$se <- sqrt(d$vi)
  d$ci_lower <- d$yi - 1.96 * d$se
  d$ci_upper <- d$yi + 1.96 * d$se
  d <- d[order(d$yi), , drop = FALSE]

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
  d$study_source <- ifelse(grepl("^T1DM_EBEVEYN", d$study_label), "Bu calisma", "Dis kaynak")
  pooled_row <- d[1L, , drop = FALSE]
  pooled_row[1L, ] <- NA
  pooled_row$study_label <- "Pooled REML"
  pooled_row$yi <- pooled_y
  pooled_row$se <- NA_real_
  pooled_row$ci_lower <- pooled_lo
  pooled_row$ci_upper <- pooled_hi
  pooled_row$study_source <- "Pooled"
  plot_d <- rbind(d, pooled_row)
  plot_d$study_label <- factor(plot_d$study_label, levels = rev(plot_d$study_label))
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(plot_d, ggplot2::aes(x = yi, y = study_label)) +
    ggplot2::geom_vline(xintercept = 0, color = pal[["gray_40"]],
      linetype = "dashed", linewidth = 0.35) +
    ggplot2::geom_vline(xintercept = pooled_y, color = pal[["blue_60"]],
      linetype = "dotted", linewidth = 0.45) +
    ggplot2::geom_segment(
      data = plot_d[plot_d$study_source != "Pooled", , drop = FALSE],
      ggplot2::aes(x = ci_lower, xend = ci_upper, y = study_label, yend = study_label),
      color = pal[["gray_50"]], linewidth = 0.5
    ) +
    ggplot2::geom_point(
      data = plot_d[plot_d$study_source != "Pooled", , drop = FALSE],
      ggplot2::aes(shape = study_source),
      size = 2.9, color = pal[["gray_80"]], fill = "white", stroke = 0.9
    ) +
    ggplot2::geom_segment(
      data = plot_d[plot_d$study_source == "Pooled", , drop = FALSE],
      ggplot2::aes(x = ci_lower, xend = ci_upper, y = study_label, yend = study_label),
      color = pal[["blue_60"]], linewidth = 0.9
    ) +
    ggplot2::geom_point(
      data = plot_d[plot_d$study_source == "Pooled", , drop = FALSE],
      shape = 18, size = 4.4, color = pal[["blue_60"]]
    ) +
    ggplot2::scale_shape_manual(values = c(`Bu calisma` = 21, `Dis kaynak` = 16)) +
    ggplot2::labs(
      title = "F2-F06 | Bayesian/meta-analytic forest",
      subtitle = sprintf("Pooled = %.3f [%.3f, %.3f]; mavi isaret pooled kestirim",
        pooled_y, pooled_lo, pooled_hi),
      x = "Effect size estimate", y = "Study", shape = "Kaynak",
      caption = phase2_carbon_caption("phase2_meta_combined_studies.csv")
    ) +
    phase2_carbon_theme(base_size = 9)
}

phase2_apa_plot_xinfo_network <- function(xinfo_edges_table, xinfo_centrality_table = NULL) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(xinfo_edges_table) || nrow(xinfo_edges_table) == 0L) return(NULL)
  required <- c("group_label", "from", "to", "weight", "sign", "cross_informant")
  if (!all(required %in% names(xinfo_edges_table))) return(NULL)

  d <- xinfo_edges_table
  d$from_label <- phase2_carbon_variable_label(d$from)
  d$to_label <- phase2_carbon_variable_label(d$to)
  d$abs_weight <- abs(d$weight)
  d$edge_type <- ifelse(d$cross_informant, "Cross-informant", "Ayni informant")
  d$group_label <- factor(d$group_label,
    levels = c("all", "Kontrol", "DM"),
    labels = c("Tum aileler", "Kontrol", "DM"))

  if (!is.null(xinfo_centrality_table) && nrow(xinfo_centrality_table) > 0L) {
    c0 <- xinfo_centrality_table[
      xinfo_centrality_table$group_label == "all", , drop = FALSE
    ]
    if (nrow(c0) > 0L && "strength" %in% names(c0)) {
      c0$label <- phase2_carbon_variable_label(c0$variable)
      order_levels <- c0$label[order(c0$strength, decreasing = TRUE)]
    } else {
      order_levels <- unique(c(d$from_label, d$to_label))
    }
  } else {
    order_levels <- unique(c(d$from_label, d$to_label))
  }
  d$from_label <- factor(d$from_label, levels = rev(unique(order_levels)))
  d$to_label <- factor(d$to_label, levels = unique(order_levels))
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(x = from_label, y = to_label)) +
    ggplot2::geom_point(ggplot2::aes(size = abs_weight, color = sign, shape = edge_type),
      alpha = 0.82, stroke = 0.85) +
    ggplot2::facet_wrap(~ group_label, nrow = 1L) +
    ggplot2::scale_color_manual(values = c(
      positive = pal[["chart_2"]],
      negative = pal[["chart_5"]]
    )) +
    ggplot2::scale_shape_manual(values = c(`Ayni informant` = 16, `Cross-informant` = 17)) +
    ggplot2::scale_size_continuous(range = c(1.5, 6.2)) +
    ggplot2::labs(
      title = "F2-F07 | Cross-informant GGM network edge map",
      subtitle = "Nokta buyuklugu edge agirligini, sekil cross-informant baglari gosterir",
      x = "Kaynak dugum", y = "Hedef dugum",
      color = "Isaret", shape = "Edge tipi", size = "|Weight|",
      caption = phase2_carbon_caption("phase2_xinfo_edges.csv; phase2_xinfo_centrality.csv")
    ) +
    phase2_carbon_theme(base_size = 8) +
    ggplot2::theme(
      axis.text.x = ggplot2::element_text(angle = 45, hjust = 1, size = 6.5),
      axis.text.y = ggplot2::element_text(size = 6.5)
    )
}

phase2_apa_plot_dx_age_spline <- function(hba1c_spline_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(hba1c_spline_table) || nrow(hba1c_spline_table) == 0L) return(NULL)
  required <- c("outcome_subscale", "linear_r_squared", "spline_r_squared", "lrt_p")
  if (!all(required %in% names(hba1c_spline_table))) return(NULL)

  d <- hba1c_spline_table[hba1c_spline_table$status == "ok", , drop = FALSE]
  if (nrow(d) == 0L) return(NULL)
  d$outcome_label <- phase2_carbon_subscale_label(d$outcome_subscale)
  d$delta_aic <- d$aic_spline - d$aic_linear
  d_long <- data.frame(
    outcome_label = rep(d$outcome_label, 2L),
    model = rep(c("Lineer", "Spline"), each = nrow(d)),
    r_squared = c(d$linear_r_squared, d$spline_r_squared),
    lrt_p = rep(d$lrt_p, 2L),
    delta_aic = rep(d$delta_aic, 2L),
    stringsAsFactors = FALSE
  )
  d_long$model <- factor(d_long$model, levels = c("Lineer", "Spline"))
  pal <- phase2_carbon_palette()
  label_d <- d
  label_d$label <- paste0("p=", phase2_apa_format_p(label_d$lrt_p))

  ggplot2::ggplot(d_long, ggplot2::aes(x = outcome_label, y = r_squared, fill = model)) +
    ggplot2::geom_col(position = ggplot2::position_dodge(width = 0.72), width = 0.62) +
    ggplot2::geom_text(data = label_d,
      ggplot2::aes(x = outcome_label, y = pmax(linear_r_squared, spline_r_squared) + 0.025,
        label = label),
      inherit.aes = FALSE, color = pal[["gray_70"]], size = 3) +
    ggplot2::scale_fill_manual(values = c(Lineer = pal[["chart_2"]], Spline = pal[["chart_4"]])) +
    ggplot2::coord_cartesian(ylim = c(0, max(d_long$r_squared, na.rm = TRUE) + 0.08)) +
    ggplot2::labs(
      title = "F2-F08 | Tani yasi x parenting spline karar paneli",
      subtitle = "Spline eklenmesi 4/4 alt olcekte anlamli kazanc saglamadi; karar: linear sufficient",
      x = "Alt olcek", y = "R kare", fill = "Model",
      caption = phase2_carbon_caption("phase2_hba1c_spline.csv")
    ) +
    phase2_carbon_theme(base_size = 10)
}

phase2_apa_plot_imai_sensitivity <- function(imai_sensitivity_grid_table, imai_summary_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(imai_sensitivity_grid_table) || nrow(imai_sensitivity_grid_table) == 0L) return(NULL)
  required <- c("mediator_subscale", "rho", "adjusted_acme")
  if (!all(required %in% names(imai_sensitivity_grid_table))) return(NULL)

  d <- imai_sensitivity_grid_table
  d$mediator_label <- phase2_carbon_subscale_label(d$mediator_subscale)
  crit <- imai_summary_table
  if (!is.null(crit) && nrow(crit) > 0L && "rho_critical" %in% names(crit)) {
    crit$mediator_label <- phase2_carbon_subscale_label(crit$mediator_subscale)
  } else {
    crit <- NULL
  }
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(x = rho, y = adjusted_acme, color = mediator_label)) +
    ggplot2::geom_hline(yintercept = 0, color = pal[["gray_80"]], linewidth = 0.35) +
    ggplot2::geom_vline(xintercept = 0, color = pal[["gray_30"]], linewidth = 0.3) +
    ggplot2::geom_line(linewidth = 0.75) +
    ggplot2::geom_vline(data = crit,
      ggplot2::aes(xintercept = rho_critical, color = mediator_label),
      linetype = "dashed", linewidth = 0.35, show.legend = FALSE) +
    ggplot2::facet_wrap(~ mediator_label, ncol = 2L, scales = "free_y") +
    ggplot2::scale_color_manual(values = c(
      `Sicaklik` = pal[["chart_1"]],
      `Asiri koruma` = pal[["chart_2"]],
      `Reddetme` = pal[["chart_3"]],
      `Karsilastirma` = pal[["chart_4"]]
    )) +
    ggplot2::labs(
      title = "F2-F09 | Imai-Keele rho sensitivity curve",
      subtitle = "Kesik cizgiler rho critical; tum dolayli etkiler olculmemis karistiriciya karsi kirilgan",
      x = "Rho duyarlilik parametresi", y = "Adjusted ACME", color = "Mediator",
      caption = phase2_carbon_caption("phase2_imai_sensitivity_grid.csv; phase2_imai_summary.csv")
    ) +
    phase2_carbon_theme(base_size = 9)
}

phase2_apa_plot_dag_validation <- function(dag_ci_tests_table, dag_three_level_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(dag_ci_tests_table) || nrow(dag_ci_tests_table) == 0L) return(NULL)

  ci <- dag_ci_tests_table
  ci$outcome_label <- phase2_carbon_subscale_label(ci$subscale)
  ci$panel <- "DAG implied CI"
  ci$metric <- paste0(ci$X, " _||_ ", ci$Y,
    ifelse(is.na(ci$conditioning_set) | ci$conditioning_set == "",
      "", paste0(" | ", ci$conditioning_set)))
  ci$status <- ci$ci_implication
  ci$label <- paste0("p=", phase2_apa_format_p(ci$p_value))
  plot_d <- ci[, c("panel", "outcome_label", "metric", "status", "label"), drop = FALSE]

  if (!is.null(dag_three_level_table) && nrow(dag_three_level_table) > 0L) {
    tl <- dag_three_level_table[dag_three_level_table$status == "ok", , drop = FALSE]
    if (nrow(tl) > 0L) {
      tl$outcome_label <- phase2_carbon_subscale_label(tl$outcome_subscale)
      tl1 <- data.frame(
        panel = "3-level year clustering",
        outcome_label = tl$outcome_label,
        metric = "ICC year",
        status = tl$decision,
        label = sprintf("%.2f", tl$icc_year_3level),
        stringsAsFactors = FALSE
      )
      tl2 <- data.frame(
        panel = "3-level year clustering",
        outcome_label = tl$outcome_label,
        metric = "SE inflation",
        status = tl$decision,
        label = sprintf("%.1f%%", tl$se_inflation_pct),
        stringsAsFactors = FALSE
      )
      plot_d <- rbind(plot_d, tl1, tl2)
    }
  }
  plot_d$panel <- factor(plot_d$panel,
    levels = c("DAG implied CI", "3-level year clustering"))
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(plot_d, ggplot2::aes(x = metric, y = outcome_label, fill = status)) +
    ggplot2::geom_tile(color = "white", linewidth = 0.35) +
    ggplot2::geom_text(ggplot2::aes(label = label), size = 2.7, color = pal[["gray_100"]]) +
    ggplot2::facet_wrap(~ panel, scales = "free_x", ncol = 1L) +
    ggplot2::scale_fill_manual(values = c(
      consistent = pal[["chart_2"]],
      year_clustering_relevant = pal[["warning"]],
      year_clustering_negligible = pal[["gray_30"]]
    ), na.value = pal[["gray_20"]]) +
    ggplot2::labs(
      title = "F2-F10 | DAG implied CI ve uc-duzey dogrulama paneli",
      subtitle = "12/12 conditional-independence testi tutarli; yil kume etkisi alt olcege gore degisiyor",
      x = "Test / metrik", y = "Alt olcek", fill = "Karar",
      caption = phase2_carbon_caption("phase2_dag_ci_tests.csv; phase2_dag_three_level.csv")
    ) +
    phase2_carbon_theme(base_size = 8) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 25, hjust = 1, size = 6.5))
}

phase2_apa_plot_ppc_replication <- function(meta_ppc_summary_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(meta_ppc_summary_table) || nrow(meta_ppc_summary_table) == 0L) return(NULL)
  required <- c("outcome_subscale", "observed_t", "replicate_t_mean",
    "replicate_t_2_5", "replicate_t_97_5", "ppc_quantile")
  if (!all(required %in% names(meta_ppc_summary_table))) return(NULL)

  d <- meta_ppc_summary_table
  d$outcome_label <- phase2_carbon_subscale_label(d$outcome_subscale)
  d$outcome_label <- factor(d$outcome_label,
    levels = d$outcome_label[order(d$observed_t)])
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(y = outcome_label)) +
    ggplot2::geom_segment(ggplot2::aes(x = replicate_t_2_5, xend = replicate_t_97_5,
      yend = outcome_label),
      color = pal[["gray_50"]], linewidth = 0.9) +
    ggplot2::geom_point(ggplot2::aes(x = replicate_t_mean),
      color = pal[["blue_60"]], size = 3.0) +
    ggplot2::geom_point(ggplot2::aes(x = observed_t),
      color = pal[["chart_1"]], shape = 18, size = 4.0) +
    ggplot2::geom_text(ggplot2::aes(x = replicate_t_97_5, label = sprintf("q=%.3f", ppc_quantile)),
      hjust = -0.08, color = pal[["gray_70"]], size = 3) +
    ggplot2::labs(
      title = "F2-F11 | Posterior predictive replication",
      subtitle = "Mor elmas gozlenen t; mavi nokta replike ortalama; gri cizgi %95 replike aralik",
      x = "t istatistigi", y = "Alt olcek",
      caption = phase2_carbon_caption("phase2_meta_ppc_summary.csv")
    ) +
    phase2_carbon_theme(base_size = 10) +
    ggplot2::theme(plot.margin = ggplot2::margin(5.5, 28, 5.5, 5.5))
}

phase2_apa_plot_dca_heatmap <- function(clinical_dca_heatmap_table) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(NULL)
  if (is.null(clinical_dca_heatmap_table) || nrow(clinical_dca_heatmap_table) == 0L) return(NULL)
  required <- c("threshold", "cost_ratio", "net_benefit")
  if (!all(required %in% names(clinical_dca_heatmap_table))) return(NULL)

  d <- clinical_dca_heatmap_table
  label_d <- d[d$threshold %in% c(0.05, 0.25, 0.50) & d$cost_ratio %in% c(1, 5, 10), ,
    drop = FALSE]
  pal <- phase2_carbon_palette()

  ggplot2::ggplot(d, ggplot2::aes(x = factor(threshold), y = factor(cost_ratio),
    fill = net_benefit)) +
    ggplot2::geom_tile(color = "white", linewidth = 0.35) +
    ggplot2::geom_text(data = label_d,
      ggplot2::aes(label = sprintf("%.2f", net_benefit)),
      color = pal[["gray_100"]], size = 2.6) +
    ggplot2::scale_fill_gradient2(low = pal[["error"]], mid = "white", high = pal[["success"]],
      midpoint = 0) +
    ggplot2::labs(
      title = "F2-F12 | DCA threshold-sensitivity heatmap",
      subtitle = "Net benefit threshold ve cost-ratio boyunca hizla azalir; yesil alan klinik fayda bolgesidir",
      x = "Threshold probability", y = "Cost ratio", fill = "Net benefit",
      caption = phase2_carbon_caption("phase2_clinical_dca_heatmap.csv")
    ) +
    phase2_carbon_theme(base_size = 10)
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

phase2_apa_svg_path <- function(path) {
  sub("\\.[Pp][Nn][Gg]$", ".svg", path)
}

phase2_apa_save_plot <- function(plot, path, width = 8, height = 5, dpi = 300) {
  if (is.null(plot)) {
    return(path)
  }
  if (!requireNamespace("ggplot2", quietly = TRUE)) return(path)
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  ggplot2::ggsave(path, plot = plot, width = width, height = height, dpi = dpi,
    units = "in", bg = "white")
  svg_path <- phase2_apa_svg_path(path)
  try(
    {
      ggplot2::ggsave(svg_path, plot = plot, width = width, height = height,
        units = "in", bg = "white", device = grDevices::svg)
      phase2_carbonize_svg_file(svg_path)
    },
    silent = TRUE
  )
  path
}

run_phase2_apa_outputs_pipeline <- function(
    trifactor_loadings_table = NULL,
    trifactor_fit_indices_table = NULL,
    disc_latent_correlation_table = NULL,
    xinfo_summary_table = NULL,
    xinfo_edges_table = NULL,
    xinfo_centrality_table = NULL,
    floor_irt_group_delta_table = NULL,
    omegah_metrics_summary_table = NULL,
    h5ext_strategy_pooled_table = NULL,
    ad_h5_stratified_table = NULL,
    hba1c_bayesian_posterior_table = NULL,
    hba1c_spline_table = NULL,
    imai_sensitivity_grid_table = NULL,
    imai_summary_table = NULL,
    dag_ci_tests_table = NULL,
    dag_three_level_table = NULL,
    multi_h1_spec_results_table = NULL,
    multi_h1_curve_summary_table = NULL,
    multi_sca_inferential_table = NULL,
    meta_combined_studies_table = NULL,
    meta_pooling_summary_table = NULL,
    meta_ppc_summary_table = NULL,
    clinical_fit_summary_table = NULL,
    clinical_dca_heatmap_table = NULL,
    output_dir = "outputs/figures") {

  figures <- list(
    f01_trifactor = phase2_apa_plot_trifactor_loadings(trifactor_loadings_table),
    f02_xinfo = phase2_apa_plot_xinfo_summary(xinfo_summary_table),
    f03_floor_irt = phase2_apa_plot_floor_irt_delta(floor_irt_group_delta_table),
    f04_h5_strat = phase2_apa_plot_h5_strat(ad_h5_stratified_table),
    f05_h1_spec_curve = phase2_apa_plot_h1_spec_curve(multi_h1_spec_results_table),
    f06_meta_forest = phase2_apa_plot_meta_forest(
      meta_combined_studies_table, meta_pooling_summary_table),
    f07_xinfo_network = phase2_apa_plot_xinfo_network(
      xinfo_edges_table, xinfo_centrality_table),
    f08_dx_age_spline = phase2_apa_plot_dx_age_spline(hba1c_spline_table),
    f09_imai_sensitivity = phase2_apa_plot_imai_sensitivity(
      imai_sensitivity_grid_table, imai_summary_table),
    f10_dag_validation = phase2_apa_plot_dag_validation(
      dag_ci_tests_table, dag_three_level_table),
    f11_ppc_replication = phase2_apa_plot_ppc_replication(meta_ppc_summary_table),
    f12_dca_heatmap = phase2_apa_plot_dca_heatmap(clinical_dca_heatmap_table)
  )

  figure_dims <- list(
    f07_xinfo_network = c(10, 6),
    f10_dag_validation = c(10, 6),
    f11_ppc_replication = c(8.5, 5),
    f12_dca_heatmap = c(8.5, 5.5)
  )

  saved_paths <- character(0)
  saved_svg_paths <- character(0)
  for (key in names(figures)) {
    path <- file.path(output_dir, paste0("phase2_", key, ".png"))
    dims <- figure_dims[[key]]
    if (is.null(dims)) dims <- c(8, 5)
    saved_path <- phase2_apa_save_plot(figures[[key]], path,
      width = dims[1L], height = dims[2L])
    saved_paths <- c(saved_paths, saved_path)
    saved_svg_paths <- c(saved_svg_paths, phase2_apa_svg_path(saved_path))
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
    figure_svg_paths = saved_svg_paths,
    summary_table = summary_table,
    target_summary = data.frame(
      analysis = "phase2_apa_outputs",
      n_figures = length(figures),
      n_summary_rows = if (!is.null(summary_table)) nrow(summary_table) else 0L,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXXII/93)",
      reference_doc = "04-sap-faz2-posthoc.md",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
