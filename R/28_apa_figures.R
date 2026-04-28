# KISIM XIII / 40 — APA tablo + sekil uretimi
# Saf grafik nesnesi uretir; dosya yazma targets/runner katmaninda yapilir.

apa_subscale_labels <- function() {
  c(
    sicaklik = "Sıcaklık",
    asiri_koruma = "Aşırı koruma",
    reddetme = "Reddetme",
    karsilastirma = "Karşılaştırma",
    embu_c_sicaklik_mean = "EMBU-C Sıcaklık",
    embu_c_asiri_koruma_mean = "EMBU-C Aşırı koruma",
    embu_c_reddetme_mean = "EMBU-C Reddetme",
    embu_c_karsilastirma_mean = "EMBU-C Karşılaştırma",
    embu_p_sicaklik_mean = "EMBU-P Sıcaklık",
    embu_p_asiri_koruma_mean = "EMBU-P Aşırı koruma",
    embu_p_reddetme_mean = "EMBU-P Reddetme",
    embu_p_karsilastirma_mean = "EMBU-P Karşılaştırma",
    srq_ho_warmth_mean = "Kardeş sıcaklığı",
    srq_ho_status_mean = "Kardeş statüsü",
    srq_ho_conflict_mean = "Kardeş çatışması",
    srq_ho_rivalry_mean = "Kardeş rekabeti"
  )
}

apa_label_outcome <- function(x) {
  labels <- apa_subscale_labels()
  out <- unname(labels[x])
  out[is.na(out)] <- x[is.na(out)]
  out
}

apa_h5_subscales <- function() {
  if (exists("h5_subscales", mode = "function")) {
    return(h5_subscales())
  }
  c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma")
}

apa_h5_dyad_specs <- function() {
  if (exists("h5_dyad_specs", mode = "function")) {
    return(h5_dyad_specs())
  }
  list(
    anne_idx = list(a = "embu_p_%s_mean", b = "embu_c_idx_%s_mean", label = "Anne x Indeks"),
    anne_sib = list(a = "embu_p_%s_mean", b = "embu_c_sib_%s_mean", label = "Anne x Kardes"),
    idx_sib = list(a = "embu_c_idx_%s_mean", b = "embu_c_sib_%s_mean", label = "Indeks x Kardes")
  )
}

apa_plot_theme <- function(base_size = 11) {
  ggplot2::theme_minimal(base_size = base_size, base_family = "sans") +
    ggplot2::theme(
      plot.title = ggplot2::element_text(face = "bold", size = base_size + 2),
      plot.subtitle = ggplot2::element_text(color = "grey30", size = base_size),
      plot.caption = ggplot2::element_text(color = "grey35", hjust = 0, size = base_size - 2),
      panel.grid.minor = ggplot2::element_blank(),
      legend.position = "bottom",
      strip.text = ggplot2::element_text(face = "bold"),
      axis.title = ggplot2::element_text(face = "bold")
    )
}

apa_require_plot_packages <- function() {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("Required package is not installed: ggplot2", call. = FALSE)
  }
  invisible(TRUE)
}

apa_h1_forest_data <- function(h1_primary_fixed_effects_table) {
  terms <- c("role_fKontrol_Kardes", "role_fDM_Hasta_Indeks", "role_fDM_Hasta_Kardes")
  rows <- h1_primary_fixed_effects_table[
    h1_primary_fixed_effects_table$term %in% terms,
    ,
    drop = FALSE
  ]
  if (nrow(rows) == 0L) {
    stop("H1 fixed-effects table does not contain role_f terms", call. = FALSE)
  }
  labels <- apa_subscale_labels()
  rows$outcome_label <- labels[rows$outcome]
  rows$outcome_label[is.na(rows$outcome_label)] <- rows$outcome[is.na(rows$outcome_label)]
  rows$contrast_label <- c(
    role_fKontrol_Kardes = "Kontrol kardeş",
    role_fDM_Hasta_Indeks = "DM indeks",
    role_fDM_Hasta_Kardes = "DM kardeş"
  )[rows$term]
  rows$outcome_label <- factor(
    rows$outcome_label,
    levels = rev(c("EMBU-C Sıcaklık", "EMBU-C Aşırı koruma", "EMBU-C Reddetme", "EMBU-C Karşılaştırma"))
  )
  rows$contrast_label <- factor(
    rows$contrast_label,
    levels = c("Kontrol kardeş", "DM indeks", "DM kardeş")
  )
  rows
}

apa_plot_h1_forest <- function(h1_primary_fixed_effects_table) {
  apa_require_plot_packages()
  forest <- apa_h1_forest_data(h1_primary_fixed_effects_table)
  ggplot2::ggplot(
    forest,
    ggplot2::aes(
      x = estimate,
      y = outcome_label,
      xmin = ci_low,
      xmax = ci_high,
      color = contrast_label
    )
  ) +
    ggplot2::geom_vline(xintercept = 0, linetype = "dashed", color = "grey45", linewidth = 0.4) +
    ggplot2::geom_errorbar(
      ggplot2::aes(xmin = ci_low, xmax = ci_high),
      position = ggplot2::position_dodge(width = 0.55),
      width = 0.18,
      orientation = "y",
      linewidth = 0.55
    ) +
    ggplot2::geom_point(position = ggplot2::position_dodge(width = 0.55), size = 2.2) +
    ggplot2::scale_color_manual(
      values = c("Kontrol kardeş" = "#6f6f6f", "DM indeks" = "#0f62fe", "DM kardeş" = "#007d79"),
      name = "Referans: Kontrol indeks"
    ) +
    ggplot2::labs(
      title = "H1 çocuk algısı: multilevel ANCOVA rol/grup katsayıları",
      subtitle = "Nokta tahmini ve %95 GA; aile için random intercept modeli",
      x = "Katsayı (ölçek puanı farkı)",
      y = NULL,
      caption = "Not. Referans kategori Kontrol indeks çocuktur. Pozitif değer daha yüksek EMBU-C puanını gösterir."
    ) +
    apa_plot_theme()
}

apa_h4_path_data <- function(h4_latent_sem_structural_paths_table) {
  rows <- h4_latent_sem_structural_paths_table
  rows <- rows[rows$rhs == "beck_dep" & rows$op == "~", , drop = FALSE]
  if (nrow(rows) == 0L) {
    stop("H4 structural path table does not contain beck_dep regression paths", call. = FALSE)
  }
  labels <- c(
    sicaklik = "Sıcaklık",
    asiri_koruma = "Aşırı koruma",
    reddetme = "Reddetme",
    karsilastirma = "Karşılaştırma"
  )
  rows$target_label <- labels[rows$lhs]
  rows$target_label[is.na(rows$target_label)] <- rows$lhs[is.na(rows$target_label)]
  rows$significant <- !is.na(rows$p_fdr_across_h4) & rows$p_fdr_across_h4 < 0.05
  rows$beta_label <- sprintf("β = %.2f%s", rows$std.all, ifelse(rows$significant, "*", ""))
  rows$y <- match(rows$lhs, c("sicaklik", "asiri_koruma", "reddetme", "karsilastirma"))
  rows$y <- max(rows$y, na.rm = TRUE) + 1 - rows$y
  rows
}

apa_plot_h4_sem_path <- function(h4_latent_sem_structural_paths_table) {
  apa_require_plot_packages()
  paths <- apa_h4_path_data(h4_latent_sem_structural_paths_table)
  beck_y <- mean(paths$y)
  paths$beck_y <- beck_y
  node_targets <- data.frame(
    x = 5,
    y = paths$y,
    label = paths$target_label,
    stringsAsFactors = FALSE
  )
  beck_node <- data.frame(x = 1, y = beck_y, label = "Beck\ndepresyon\nlatent", stringsAsFactors = FALSE)

  ggplot2::ggplot() +
    ggplot2::geom_curve(
      data = paths,
      ggplot2::aes(
        x = 1.65,
        y = beck_y,
        xend = 4.35,
        yend = y,
        linewidth = abs(std.all),
        color = std.all
      ),
      curvature = 0.08,
      arrow = grid::arrow(length = grid::unit(0.18, "cm"), type = "closed"),
      lineend = "round"
    ) +
    ggplot2::geom_label(
      data = paths,
      ggplot2::aes(x = 3.2, y = y + 0.18, label = beta_label, color = std.all),
      fill = "white",
      linewidth = 0,
      size = 3.2,
      fontface = "bold"
    ) +
    ggplot2::geom_label(
      data = beck_node,
      ggplot2::aes(x = x, y = y, label = label),
      fill = "#edf5ff",
      color = "#161616",
      linewidth = 0.35,
      size = 4.2,
      fontface = "bold",
      label.padding = grid::unit(0.22, "lines")
    ) +
    ggplot2::geom_label(
      data = node_targets,
      ggplot2::aes(x = x, y = y, label = label),
      fill = "#f4f4f4",
      color = "#161616",
      linewidth = 0.35,
      size = 3.9,
      label.padding = grid::unit(0.22, "lines")
    ) +
    ggplot2::scale_color_gradient2(
      low = "#da1e28",
      mid = "#8d8d8d",
      high = "#0f62fe",
      midpoint = 0,
      name = "Std. β"
    ) +
    ggplot2::scale_linewidth(range = c(0.5, 1.8), guide = "none") +
    ggplot2::coord_cartesian(xlim = c(0.3, 5.7), ylim = c(0.4, max(paths$y) + 0.6), clip = "off") +
    ggplot2::labs(
      title = "H4 Beck depresyonu → EMBU-P latent ebeveynlik yolları",
      subtitle = "WLSMV SEM; katsayılar standardize β, * FDR p < .05",
      x = NULL,
      y = NULL,
      caption = "Not. Aşırı koruma yolu FDR sonrası anlamlı değildir; diğer üç yol anlamlıdır."
    ) +
    apa_plot_theme() +
    ggplot2::theme(
      axis.text = ggplot2::element_blank(),
      axis.ticks = ggplot2::element_blank(),
      panel.grid = ggplot2::element_blank()
    )
}

apa_h5_bland_altman_data <- function(df_family_ses) {
  dyads <- apa_h5_dyad_specs()
  rows <- list()
  for (sub in apa_h5_subscales()) {
    for (dyad_name in names(dyads)) {
      spec <- dyads[[dyad_name]]
      col_a <- sprintf(spec$a, sub)
      col_b <- sprintf(spec$b, sub)
      pair <- df_family_ses[, c("aile_no", "group_f", col_a, col_b), drop = FALSE]
      names(pair) <- c("aile_no", "group_f", "a", "b")
      pair <- pair[stats::complete.cases(pair), , drop = FALSE]
      if (nrow(pair) == 0L) {
        next
      }
      pair$subscale <- sub
      pair$dyad <- dyad_name
      pair$dyad_label <- spec$label
      pair$mean_pair <- (pair$a + pair$b) / 2
      pair$diff_pair <- pair$a - pair$b
      rows[[length(rows) + 1L]] <- pair
    }
  }
  out <- do.call(rbind, rows)
  labels <- apa_subscale_labels()
  out$subscale_label <- labels[out$subscale]
  out$subscale_label[is.na(out$subscale_label)] <- out$subscale[is.na(out$subscale_label)]
  out$dyad_label <- factor(out$dyad_label, levels = c("Anne x Indeks", "Anne x Kardes", "Indeks x Kardes"))
  out$subscale_label <- factor(out$subscale_label, levels = c("Sıcaklık", "Aşırı koruma", "Reddetme", "Karşılaştırma"))
  out$group_f <- factor(as.character(out$group_f), levels = c("Kontrol", "DM"))
  out
}

apa_h5_bland_altman_summary <- function(ba_data) {
  split_key <- interaction(ba_data$subscale_label, ba_data$dyad_label, ba_data$group_f, drop = TRUE)
  rows <- lapply(split(ba_data, split_key), function(df) {
    mean_diff <- mean(df$diff_pair, na.rm = TRUE)
    sd_diff <- stats::sd(df$diff_pair, na.rm = TRUE)
    data.frame(
      subscale_label = df$subscale_label[[1L]],
      dyad_label = df$dyad_label[[1L]],
      group_f = df$group_f[[1L]],
      mean_diff = mean_diff,
      loa_lo = mean_diff - 1.96 * sd_diff,
      loa_hi = mean_diff + 1.96 * sd_diff,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, rows)
}

apa_plot_h5_bland_altman <- function(df_family_ses) {
  apa_require_plot_packages()
  ba <- apa_h5_bland_altman_data(df_family_ses)
  summary <- apa_h5_bland_altman_summary(ba)
  ggplot2::ggplot(ba, ggplot2::aes(x = mean_pair, y = diff_pair, color = group_f)) +
    ggplot2::geom_point(alpha = 0.42, size = 1.1) +
    ggplot2::geom_hline(
      data = summary,
      ggplot2::aes(yintercept = mean_diff, color = group_f),
      linewidth = 0.55
    ) +
    ggplot2::geom_hline(
      data = summary,
      ggplot2::aes(yintercept = loa_lo, color = group_f),
      linetype = "dashed",
      linewidth = 0.35
    ) +
    ggplot2::geom_hline(
      data = summary,
      ggplot2::aes(yintercept = loa_hi, color = group_f),
      linetype = "dashed",
      linewidth = 0.35
    ) +
    ggplot2::facet_grid(subscale_label ~ dyad_label) +
    ggplot2::scale_color_manual(values = c("Kontrol" = "#6f6f6f", "DM" = "#0f62fe"), name = "Grup") +
    ggplot2::labs(
      title = "H5 anne-çocuk-kardeş Bland-Altman tutarlılık haritası",
      subtitle = "Kesintisiz çizgi ortalama farkı, kesikli çizgiler 95% limits of agreement değerlerini gösterir",
      x = "Dyad ortalaması",
      y = "Fark skoru (ilk kaynak − ikinci kaynak)",
      caption = "Not. Üç dyad tipi dört EMBU alt ölçeği için aynı panelde verilmiştir."
    ) +
    apa_plot_theme(base_size = 10)
}

apa_h5_rsa_surface_data <- function(h5_rsa_parameters_table, df_family_ses, n_grid = 45L) {
  coeff_names <- c("Z~1", "Z~X", "Z~Y", "Z~X2", "Z~X_Y", "Z~Y2")
  rows <- list()
  labels <- apa_subscale_labels()
  for (sub in c("sicaklik", "reddetme")) {
    p_col <- sprintf("embu_p_%s_mean", sub)
    c_col <- sprintf("embu_c_idx_%s_mean", sub)
    for (grp in c("Pooled", "Kontrol", "DM")) {
      coefs <- h5_rsa_parameters_table[
        h5_rsa_parameters_table$subscale == sub &
          h5_rsa_parameters_table$group == grp &
          h5_rsa_parameters_table$param %in% coeff_names,
        c("param", "est"),
        drop = FALSE
      ]
      if (nrow(coefs) < length(coeff_names)) {
        next
      }
      coef_map <- stats::setNames(coefs$est, coefs$param)
      base_df <- if (grp == "Pooled") {
        df_family_ses
      } else {
        df_family_ses[as.character(df_family_ses$group_f) == grp, , drop = FALSE]
      }
      x_rng <- range(base_df[[p_col]], na.rm = TRUE)
      y_rng <- range(base_df[[c_col]], na.rm = TRUE)
      grid <- expand.grid(
        X = seq(x_rng[[1L]], x_rng[[2L]], length.out = n_grid),
        Y = seq(y_rng[[1L]], y_rng[[2L]], length.out = n_grid)
      )
      grid$Z_hat <- coef_map[["Z~1"]] +
        coef_map[["Z~X"]] * grid$X +
        coef_map[["Z~Y"]] * grid$Y +
        coef_map[["Z~X2"]] * grid$X^2 +
        coef_map[["Z~X_Y"]] * grid$X * grid$Y +
        coef_map[["Z~Y2"]] * grid$Y^2
      grid$subscale <- sub
      grid$subscale_label <- labels[sub]
      grid$group <- grp
      rows[[length(rows) + 1L]] <- grid
    }
  }
  out <- do.call(rbind, rows)
  out$group <- factor(out$group, levels = c("Pooled", "Kontrol", "DM"))
  out$subscale_label <- factor(out$subscale_label, levels = c("Sıcaklık", "Reddetme"))
  out
}

apa_plot_h5_rsa_surface <- function(h5_rsa_parameters_table, df_family_ses) {
  apa_require_plot_packages()
  surf <- apa_h5_rsa_surface_data(h5_rsa_parameters_table, df_family_ses)
  ggplot2::ggplot(surf, ggplot2::aes(x = X, y = Y, fill = Z_hat)) +
    ggplot2::geom_tile() +
    ggplot2::geom_contour(
      data = surf,
      ggplot2::aes(x = X, y = Y, z = Z_hat),
      inherit.aes = FALSE,
      color = "white",
      alpha = 0.55,
      linewidth = 0.25,
      bins = 7
    ) +
    ggplot2::geom_abline(slope = 1, intercept = 0, color = "grey10", linetype = "dotted", linewidth = 0.35) +
    ggplot2::facet_grid(subscale_label ~ group) +
    ggplot2::scale_fill_gradientn(
      colors = c("#edf5ff", "#78a9ff", "#0f62fe", "#001d6c"),
      name = "Tahmini\nBeck"
    ) +
    ggplot2::coord_equal(expand = FALSE) +
    ggplot2::labs(
      title = "H5 Response Surface Analysis: anne-çocuk algı uyumu ve Beck",
      subtitle = "Noktalı diyagonal anne ve indeks çocuk algısının eşit olduğu hattır",
      x = "Anne EMBU-P alt ölçek ortalaması",
      y = "İndeks çocuk EMBU-C alt ölçek ortalaması",
      caption = "Not. Yüzeyler RSA full polynomial katsayılarından türetilmiştir; keşifsel yorumlanmalıdır."
    ) +
    apa_plot_theme(base_size = 10)
}

apa_h2_apim_path_data <- function(h2_apim_fixed_effects_table) {
  terms <- c("group_fDM", "family_role_fsibling", "age_gap_z", "group_fDM:family_role_fsibling")
  rows <- h2_apim_fixed_effects_table[
    h2_apim_fixed_effects_table$term %in% terms &
      is.finite(h2_apim_fixed_effects_table$estimate),
    ,
    drop = FALSE
  ]
  if (nrow(rows) == 0L) {
    stop("H2 APIM fixed-effects table does not contain expected APIM terms", call. = FALSE)
  }
  term_labels <- c(
    group_fDM = "DM grup",
    family_role_fsibling = "Kardeş rolü",
    age_gap_z = "Yaş farkı",
    `group_fDM:family_role_fsibling` = "DM × kardeş rolü"
  )
  term_order <- names(term_labels)
  outcome_order <- c(
    "srq_ho_warmth_mean",
    "srq_ho_status_mean",
    "srq_ho_conflict_mean",
    "srq_ho_rivalry_mean"
  )
  rows$term_label <- unname(term_labels[rows$term])
  rows$outcome_label <- apa_label_outcome(rows$outcome)
  rows$term_y <- match(rows$term, rev(term_order))
  rows$outcome_y <- match(rows$outcome, rev(outcome_order))
  rows$edge_label <- sprintf("b = %.2f", rows$estimate)
  rows$significant <- if ("p_fdr_across_h2" %in% names(rows)) {
    !is.na(rows$p_fdr_across_h2) & rows$p_fdr_across_h2 < 0.05
  } else {
    !is.na(rows$p_value) & rows$p_value < 0.05
  }
  rows
}

apa_plot_h2_apim_path <- function(h2_apim_fixed_effects_table) {
  apa_require_plot_packages()
  paths <- apa_h2_apim_path_data(h2_apim_fixed_effects_table)
  predictor_nodes <- unique(paths[, c("term", "term_label", "term_y"), drop = FALSE])
  predictor_nodes <- predictor_nodes[order(predictor_nodes$term_y), , drop = FALSE]
  outcome_nodes <- unique(paths[, c("outcome", "outcome_label", "outcome_y"), drop = FALSE])
  outcome_nodes <- outcome_nodes[order(outcome_nodes$outcome_y), , drop = FALSE]
  label_rows <- paths[paths$term %in% c("group_fDM", "group_fDM:family_role_fsibling"), , drop = FALSE]

  ggplot2::ggplot() +
    ggplot2::geom_curve(
      data = paths,
      ggplot2::aes(
        x = 1.55,
        y = term_y,
        xend = 4.45,
        yend = outcome_y,
        color = estimate,
        linewidth = abs(estimate),
        alpha = significant
      ),
      curvature = 0.12,
      arrow = grid::arrow(length = grid::unit(0.12, "cm"), type = "closed"),
      lineend = "round"
    ) +
    ggplot2::geom_label(
      data = predictor_nodes,
      ggplot2::aes(x = 1, y = term_y, label = term_label),
      fill = "#edf5ff",
      color = "#161616",
      linewidth = 0.3,
      size = 3.3,
      label.padding = grid::unit(0.18, "lines")
    ) +
    ggplot2::geom_label(
      data = outcome_nodes,
      ggplot2::aes(x = 5, y = outcome_y, label = outcome_label),
      fill = "#f4f4f4",
      color = "#161616",
      linewidth = 0.3,
      size = 3.3,
      label.padding = grid::unit(0.18, "lines")
    ) +
    ggplot2::geom_text(
      data = label_rows,
      ggplot2::aes(x = 3, y = (term_y + outcome_y) / 2, label = edge_label, color = estimate),
      size = 2.8,
      fontface = "bold",
      check_overlap = TRUE
    ) +
    ggplot2::scale_color_gradient2(
      low = "#da1e28",
      mid = "#8d8d8d",
      high = "#0f62fe",
      midpoint = 0,
      name = "Katsayı"
    ) +
    ggplot2::scale_alpha_manual(values = c(`TRUE` = 0.95, `FALSE` = 0.35), guide = "none") +
    ggplot2::scale_linewidth(range = c(0.25, 1.4), guide = "none") +
    ggplot2::coord_cartesian(xlim = c(0.45, 5.55), ylim = c(0.45, 4.55), clip = "off") +
    ggplot2::labs(
      title = "H2 kardeş ilişkisi: APIM yol katsayıları",
      subtitle = "Ok kalınlığı katsayının mutlak büyüklüğünü, renk yönünü gösterir; sol blok APIM terimleri, sağ blok SRQ çıktılarıdır",
      x = NULL,
      y = NULL,
      caption = "Not. Yaş farkı kovaryatı modelde tutulmuştur. Etiketler DM ana etkisi ve DM × kardeş rolü etkileşimi için verilmiştir."
    ) +
    apa_plot_theme(base_size = 10) +
    ggplot2::theme(
      axis.text = ggplot2::element_blank(),
      axis.ticks = ggplot2::element_blank(),
      panel.grid = ggplot2::element_blank()
    )
}

apa_h3_stratified_forest_data <- function(h3_antidepressant_stratified_group_effects_table) {
  rows <- h3_antidepressant_stratified_group_effects_table
  rows <- rows[rows$term == "group_fDM" & rows$status == "fitted", , drop = FALSE]
  if (nrow(rows) == 0L) {
    stop("H3 stratified table does not contain fitted group_fDM rows", call. = FALSE)
  }
  rows$effect <- if ("std_beta" %in% names(rows) && any(is.finite(rows$std_beta))) rows$std_beta else rows$estimate
  rows$ci_low_effect <- if ("std_beta_ci_low" %in% names(rows) && any(is.finite(rows$std_beta_ci_low))) {
    rows$std_beta_ci_low
  } else rows$ci_low
  rows$ci_high_effect <- if ("std_beta_ci_high" %in% names(rows) && any(is.finite(rows$std_beta_ci_high))) {
    rows$std_beta_ci_high
  } else rows$ci_high
  rows$outcome_label <- apa_label_outcome(rows$outcome)
  rows$stratum_label <- c(
    all_adjusted_for_antidepressant = "Tüm örneklem\n(AD ayarlı)",
    no_antidepressant = "Antidepresan yok",
    antidepressant_only = "Antidepresan var"
  )[rows$stratum]
  rows$stratum_label[is.na(rows$stratum_label)] <- rows$stratum[is.na(rows$stratum_label)]
  rows$outcome_label <- factor(
    rows$outcome_label,
    levels = rev(c("EMBU-P Sıcaklık", "EMBU-P Aşırı koruma", "EMBU-P Reddetme", "EMBU-P Karşılaştırma"))
  )
  rows$stratum_label <- factor(
    rows$stratum_label,
    levels = c("Tüm örneklem\n(AD ayarlı)", "Antidepresan yok", "Antidepresan var")
  )
  rows
}

apa_plot_h3_stratified_forest <- function(h3_antidepressant_stratified_group_effects_table) {
  apa_require_plot_packages()
  forest <- apa_h3_stratified_forest_data(h3_antidepressant_stratified_group_effects_table)
  ggplot2::ggplot(
    forest,
    ggplot2::aes(
      x = effect,
      y = outcome_label,
      xmin = ci_low_effect,
      xmax = ci_high_effect,
      color = stratum_label
    )
  ) +
    ggplot2::geom_vline(xintercept = 0, linetype = "dashed", color = "grey45", linewidth = 0.4) +
    ggplot2::geom_errorbar(
      position = ggplot2::position_dodge(width = 0.58),
      width = 0.18,
      orientation = "y",
      linewidth = 0.55
    ) +
    ggplot2::geom_point(position = ggplot2::position_dodge(width = 0.58), size = 2.25) +
    ggplot2::scale_color_manual(
      values = c(
        "Tüm örneklem\n(AD ayarlı)" = "#0f62fe",
        "Antidepresan yok" = "#007d79",
        "Antidepresan var" = "#8a3ffc"
      ),
      name = "Katman"
    ) +
    ggplot2::labs(
      title = "H3 anne öz-raporu: antidepresan katmanlı DM etkisi",
      subtitle = "Standardize β ve %95 GA; tüm örneklem satırı antidepresan kullanımına göre ayarlıdır",
      x = "Standardize β (DM − Kontrol)",
      y = NULL,
      caption = "Not. Antidepresan var katmanı küçük n nedeniyle geniş güven aralığıyla yorumlanmalıdır."
    ) +
    apa_plot_theme()
}

apa_specification_curve_data <- function(robust_multiverse_spec_table) {
  rows <- robust_multiverse_spec_table
  rows <- rows[rows$status == "ok" & is.finite(rows$cohens_d), , drop = FALSE]
  if (nrow(rows) == 0L) {
    stop("Specification table has no valid ok rows with cohens_d", call. = FALSE)
  }
  rows$outcome_label <- apa_label_outcome(rows$outcome)
  rows$significant <- !is.na(rows$p_value) & rows$p_value < 0.05
  rows$spec_label <- paste(rows$controls, rows$model, rows$subset, sep = " / ")
  split_rows <- split(rows, rows$outcome_label)
  split_rows <- lapply(split_rows, function(df) {
    df <- df[order(df$cohens_d), , drop = FALSE]
    df$spec_index <- seq_len(nrow(df))
    df
  })
  out <- do.call(rbind, split_rows)
  out$outcome_label <- factor(out$outcome_label, levels = unique(out$outcome_label))
  out
}

apa_plot_specification_curve <- function(robust_multiverse_spec_table) {
  apa_require_plot_packages()
  curve <- apa_specification_curve_data(robust_multiverse_spec_table)
  ggplot2::ggplot(curve, ggplot2::aes(x = spec_index, y = cohens_d)) +
    ggplot2::geom_hline(yintercept = 0, linetype = "dashed", color = "grey45", linewidth = 0.35) +
    ggplot2::geom_line(color = "#6f6f6f", linewidth = 0.35) +
    ggplot2::geom_point(ggplot2::aes(color = significant), size = 1.8, alpha = 0.9) +
    ggplot2::facet_wrap(~ outcome_label, scales = "free_x", ncol = 2) +
    ggplot2::scale_color_manual(
      values = c(`FALSE` = "#0f62fe", `TRUE` = "#da1e28"),
      labels = c(`FALSE` = "p ≥ .05", `TRUE` = "p < .05"),
      name = "Nominal test"
    ) +
    ggplot2::labs(
      title = "Robustluk: specification curve analizi",
      subtitle = "Her panelde multiverse spesifikasyonları Cohen d büyüklüğüne göre sıralanmıştır",
      x = "Sıralı model spesifikasyonu",
      y = "Cohen d",
      caption = "Not. Sprint A figürü KISIM XI multiverse tablosundan türetilmiştir; p-değerleri nominaldir."
    ) +
    apa_plot_theme(base_size = 10)
}

apa_sensemakr_contour_data <- function(robust_sensemakr_evalue_table, n_grid = 80L) {
  rows <- robust_sensemakr_evalue_table
  rows <- rows[rows$status == "ok", , drop = FALSE]
  if (nrow(rows) == 0L) {
    stop("Sensemakr table has no ok rows", call. = FALSE)
  }
  max_axis <- max(c(rows$RV_q, rows$partial_r2_treatment), na.rm = TRUE) * 1.35
  max_axis <- max(max_axis, 0.10)
  grid <- expand.grid(
    r2_treatment = seq(0, max_axis, length.out = n_grid),
    r2_outcome = seq(0, max_axis, length.out = n_grid)
  )
  grid$joint_strength <- sqrt(grid$r2_treatment * grid$r2_outcome)
  rows$outcome_label <- apa_label_outcome(rows$outcome)
  list(grid = grid, points = rows, max_axis = max_axis)
}

apa_plot_sensemakr_contour <- function(robust_sensemakr_evalue_table) {
  apa_require_plot_packages()
  dat <- apa_sensemakr_contour_data(robust_sensemakr_evalue_table)
  ggplot2::ggplot(dat$grid, ggplot2::aes(x = r2_treatment, y = r2_outcome, z = joint_strength)) +
    ggplot2::geom_raster(ggplot2::aes(fill = joint_strength), alpha = 0.72, interpolate = TRUE) +
    ggplot2::geom_contour(color = "white", bins = 7, linewidth = 0.35, alpha = 0.8) +
    ggplot2::geom_point(
      data = dat$points,
      ggplot2::aes(
        x = partial_r2_treatment,
        y = RV_q,
        size = evalue_point,
        color = cohens_d
      ),
      inherit.aes = FALSE,
      alpha = 0.95
    ) +
    ggplot2::geom_text(
      data = dat$points,
      ggplot2::aes(
        x = partial_r2_treatment,
        y = RV_q,
        label = outcome_label
      ),
      inherit.aes = FALSE,
      nudge_x = dat$max_axis * 0.025,
      size = 2.8,
      hjust = 0,
      check_overlap = TRUE
    ) +
    ggplot2::scale_fill_gradientn(colors = c("#edf5ff", "#78a9ff", "#0f62fe", "#001d6c"), name = "Ortak\nR² gücü") +
    ggplot2::scale_color_gradient2(low = "#da1e28", mid = "#8d8d8d", high = "#0f62fe", midpoint = 0, name = "Cohen d") +
    ggplot2::scale_size(range = c(2.5, 5.5), name = "E-value") +
    ggplot2::coord_cartesian(xlim = c(0, dat$max_axis), ylim = c(0, dat$max_axis), clip = "off") +
    ggplot2::labs(
      title = "Sensemakr duyarlılık konturu",
      subtitle = "Noktalar tedavi kısmi R² ve RVq kesişimini; arka plan ortak karıştırıcı gücü konturlarını gösterir",
      x = "Karıştırıcı–tedavi ilişkisi (kısmi R² ölçeği)",
      y = "Karıştırıcı–sonuç ilişkisi / RVq",
      caption = "Not. Kontur görselleştirmesi sensemakr özet istatistiklerinden türetilmiş karar yüzeyidir."
    ) +
    apa_plot_theme(base_size = 10)
}

apa_manual_roc_curve <- function(observed, predicted, n_thresholds = 200L) {
  d <- data.frame(observed = observed, predicted = predicted)
  d <- d[stats::complete.cases(d), , drop = FALSE]
  if (!all(d$observed %in% c(0, 1))) {
    stop("ROC observed vector must be binary 0/1", call. = FALSE)
  }
  thresholds <- sort(
    unique(stats::quantile(d$predicted, probs = seq(0, 1, length.out = n_thresholds), na.rm = TRUE)),
    decreasing = TRUE
  )
  thresholds <- unique(c(Inf, thresholds, -Inf))
  n_pos <- sum(d$observed == 1L)
  n_neg <- sum(d$observed == 0L)
  rows <- lapply(thresholds, function(thr) {
    pred_pos <- d$predicted >= thr
    tp <- sum(pred_pos & d$observed == 1L)
    fp <- sum(pred_pos & d$observed == 0L)
    data.frame(
      threshold = thr,
      sensitivity = if (n_pos > 0) tp / n_pos else NA_real_,
      specificity = if (n_neg > 0) 1 - fp / n_neg else NA_real_,
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  out$fpr <- 1 - out$specificity
  out[order(out$fpr, out$sensitivity), , drop = FALSE]
}

apa_auc_trapezoid <- function(roc_data) {
  x <- roc_data$fpr
  y <- roc_data$sensitivity
  idx <- order(x)
  x <- x[idx]
  y <- y[idx]
  sum(diff(x) * (head(y, -1L) + tail(y, -1L)) / 2, na.rm = TRUE)
}

apa_clinical_roc_data <- function(df_family_ses) {
  if (!exists("clinical_prepare_frame", mode = "function") ||
      !exists("clinical_predictors_base", mode = "function") ||
      !exists("clinical_predictors_extended", mode = "function") ||
      !exists("clinical_outcome", mode = "function")) {
    stop("Clinical utility functions must be sourced before ROC figure generation", call. = FALSE)
  }
  prepared <- clinical_prepare_frame(df_family_ses)
  model_specs <- list(
    "Temel model" = clinical_predictors_base(),
    "Geniş model" = clinical_predictors_extended()
  )
  rows <- list()
  for (model_name in names(model_specs)) {
    predictors <- model_specs[[model_name]]
    cols <- c(clinical_outcome(), predictors)
    sub_df <- prepared[stats::complete.cases(prepared[, cols, drop = FALSE]), , drop = FALSE]
    fit <- stats::glm(
      stats::as.formula(sprintf("%s ~ %s", clinical_outcome(), paste(predictors, collapse = " + "))),
      data = sub_df,
      family = "binomial"
    )
    roc <- apa_manual_roc_curve(sub_df[[clinical_outcome()]], stats::predict(fit, type = "response"))
    roc$model <- model_name
    roc$auc <- apa_auc_trapezoid(roc)
    rows[[length(rows) + 1L]] <- roc
  }
  out <- do.call(rbind, rows)
  out$model <- factor(out$model, levels = names(model_specs))
  out
}

apa_plot_clinical_roc <- function(df_family_ses, clinical_base_performance, clinical_full_performance) {
  apa_require_plot_packages()
  roc <- apa_clinical_roc_data(df_family_ses)
  auc_labels <- data.frame(
    model = factor(c("Temel model", "Geniş model"), levels = c("Temel model", "Geniş model")),
    x = c(0.62, 0.62),
    y = c(0.20, 0.12),
    label = c(
      sprintf("Temel AUC = %.2f [%.2f, %.2f]", clinical_base_performance$auc, clinical_base_performance$auc_ci_lo, clinical_base_performance$auc_ci_hi),
      sprintf("Geniş AUC = %.2f [%.2f, %.2f]", clinical_full_performance$auc, clinical_full_performance$auc_ci_lo, clinical_full_performance$auc_ci_hi)
    ),
    stringsAsFactors = FALSE
  )
  ggplot2::ggplot(roc, ggplot2::aes(x = fpr, y = sensitivity, color = model)) +
    ggplot2::geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "grey55", linewidth = 0.35) +
    ggplot2::geom_line(linewidth = 0.9) +
    ggplot2::geom_label(
      data = auc_labels,
      ggplot2::aes(x = x, y = y, label = label, color = model),
      inherit.aes = FALSE,
      fill = "white",
      linewidth = 0,
      hjust = 0,
      size = 3.1
    ) +
    ggplot2::scale_color_manual(values = c("Temel model" = "#6f6f6f", "Geniş model" = "#0f62fe"), name = "Risk skoru") +
    ggplot2::coord_equal(xlim = c(0, 1), ylim = c(0, 1), expand = TRUE) +
    ggplot2::labs(
      title = "Klinik fayda: yüksek Beck riski için ROC eğrisi",
      subtitle = "Temel model demografi/SES; geniş model EMBU-P alt ölçeklerini ekler",
      x = "1 − Özgüllük",
      y = "Duyarlılık",
      caption = "Not. AUC güven aralıkları KISIM IX performans tablosundan, eğri koordinatları aynı model formüllerinden türetilmiştir."
    ) +
    apa_plot_theme()
}

apa_clinical_dca_data <- function(clinical_decision_curve_table, clinical_full_performance) {
  rows <- clinical_decision_curve_table
  if (nrow(rows) == 0L) {
    stop("Clinical decision curve table is empty", call. = FALSE)
  }
  prevalence <- clinical_full_performance$n_events / clinical_full_performance$n
  model <- data.frame(
    threshold = rows$threshold,
    net_benefit = rows$net_benefit,
    model = "Geniş risk skoru",
    stringsAsFactors = FALSE
  )
  treat_all <- data.frame(
    threshold = rows$threshold,
    net_benefit = prevalence - (1 - prevalence) * rows$threshold / (1 - rows$threshold),
    model = "Treat all",
    stringsAsFactors = FALSE
  )
  treat_none <- data.frame(
    threshold = rows$threshold,
    net_benefit = 0,
    model = "Treat none",
    stringsAsFactors = FALSE
  )
  out <- rbind(model, treat_all, treat_none)
  out$model <- factor(out$model, levels = c("Geniş risk skoru", "Treat all", "Treat none"))
  out
}

apa_plot_clinical_dca <- function(clinical_decision_curve_table, clinical_full_performance) {
  apa_require_plot_packages()
  dca <- apa_clinical_dca_data(clinical_decision_curve_table, clinical_full_performance)
  ggplot2::ggplot(dca, ggplot2::aes(x = threshold, y = net_benefit, color = model, linetype = model)) +
    ggplot2::geom_hline(yintercept = 0, color = "grey55", linewidth = 0.3) +
    ggplot2::geom_line(linewidth = 0.9) +
    ggplot2::scale_color_manual(values = c("Geniş risk skoru" = "#0f62fe", "Treat all" = "#6f6f6f", "Treat none" = "#a8a8a8"), name = NULL) +
    ggplot2::scale_linetype_manual(values = c("Geniş risk skoru" = "solid", "Treat all" = "dashed", "Treat none" = "dotted"), name = NULL) +
    ggplot2::labs(
      title = "Klinik fayda: decision curve analysis",
      subtitle = "Yüksek Beck riski için eşik olasılıklarına göre net benefit",
      x = "Eşik olasılığı",
      y = "Net benefit",
      caption = "Not. Treat all çizgisi örneklem olay prevalansından türetilmiştir; model eğrisi KISIM IX DCA target çıktısıdır."
    ) +
    apa_plot_theme()
}

apa_plot_clinical_calibration <- function(clinical_calibration_table) {
  apa_require_plot_packages()
  calibration <- clinical_calibration_table
  if (nrow(calibration) == 0L) {
    stop("Clinical calibration table is empty", call. = FALSE)
  }
  ggplot2::ggplot(calibration, ggplot2::aes(x = mean_predicted, y = mean_observed)) +
    ggplot2::geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "grey55", linewidth = 0.35) +
    ggplot2::geom_line(color = "#0f62fe", linewidth = 0.8) +
    ggplot2::geom_point(ggplot2::aes(size = n), color = "#0f62fe", alpha = 0.85) +
    ggplot2::scale_size(range = c(2.8, 6), name = "n") +
    ggplot2::coord_equal(xlim = c(0, 1), ylim = c(0, 1), expand = TRUE) +
    ggplot2::labs(
      title = "Klinik fayda: calibration plot",
      subtitle = "Geniş risk skoru için tahmin edilen ve gözlenen yüksek-risk oranları",
      x = "Ortalama tahmin edilen risk",
      y = "Gözlenen risk",
      caption = "Not. Nokta büyüklüğü kalibrasyon binindeki aile sayısını gösterir."
    ) +
    apa_plot_theme()
}

apa_plot_study_flow <- function(df_family_ses, table1_group_counts_table) {
  apa_require_plot_packages()
  n_families <- nrow(df_family_ses)
  n_rows <- n_families * 2L
  n_dm <- table1_group_counts_table$n[table1_group_counts_table$group == "DM"][[1L]]
  n_control <- table1_group_counts_table$n[table1_group_counts_table$group == "Kontrol"][[1L]]
  hba1c_n <- sum(!is.na(df_family_ses$hba1c))
  boxes <- data.frame(
    id = c("lock", "family", "group_dm", "group_control", "clinical"),
    x = c(2.5, 2.5, 1.35, 3.65, 2.5),
    y = c(4.7, 3.55, 2.35, 2.35, 1.15),
    label = c(
      "Kanonik veri kilidi\nLOCKED_CANONICAL_ANALYSIS_BASE",
      sprintf("Analitik aile tabanı\n%d aile · %d çocuk satırı", n_families, n_rows),
      sprintf("DM indeks aile\nn = %d", n_dm),
      sprintf("Kontrol indeks aile\nn = %d", n_control),
      sprintf("DM klinik alt-analiz\nHbA1c gözlenen n = %d", hba1c_n)
    ),
    fill = c("#edf5ff", "#f4f4f4", "#d0e2ff", "#e0e0e0", "#d9fbfb"),
    stringsAsFactors = FALSE
  )
  arrows <- data.frame(
    x = c(2.5, 2.5, 2.5, 1.35, 3.65),
    y = c(4.35, 3.20, 3.20, 2.00, 2.00),
    xend = c(2.5, 1.35, 3.65, 2.5, 2.5),
    yend = c(3.88, 2.72, 2.72, 1.48, 1.48)
  )
  ggplot2::ggplot() +
    ggplot2::geom_segment(
      data = arrows,
      ggplot2::aes(x = x, y = y, xend = xend, yend = yend),
      arrow = grid::arrow(length = grid::unit(0.14, "cm"), type = "closed"),
      color = "#6f6f6f",
      linewidth = 0.45
    ) +
    ggplot2::geom_label(
      data = boxes,
      ggplot2::aes(x = x, y = y, label = label, fill = fill),
      color = "#161616",
      linewidth = 0.35,
      size = 3.6,
      fontface = "bold",
      label.padding = grid::unit(0.22, "lines")
    ) +
    ggplot2::scale_fill_identity() +
    ggplot2::coord_cartesian(xlim = c(0.45, 4.55), ylim = c(0.6, 5.25), clip = "off") +
    ggplot2::labs(
      title = "Analitik örneklem akış diyagramı",
      subtitle = "Kanonik veri kilidinden aile-düzeyi analiz ve DM klinik alt-analiz katmanına akış",
      x = NULL,
      y = NULL,
      caption = "Not. Bu diyagram randomize çalışma CONSORT akışı değil, kilitlenmiş veri setinin analitik akış haritasıdır."
    ) +
    apa_plot_theme(base_size = 10) +
    ggplot2::theme(
      axis.text = ggplot2::element_blank(),
      axis.ticks = ggplot2::element_blank(),
      panel.grid = ggplot2::element_blank()
    )
}

apa_plot_causal_dag <- function(causal_dag_nodes_table, causal_dag_edges_table) {
  apa_require_plot_packages()
  nodes <- causal_dag_nodes_table
  edges <- merge(causal_dag_edges_table, nodes[, c("node", "x", "y")], by.x = "from", by.y = "node", all.x = TRUE)
  edges <- merge(edges, nodes[, c("node", "x", "y")], by.x = "to", by.y = "node", all.x = TRUE, suffixes = c("", "_to"))
  role_colors <- c(
    confounder = "#d0e2ff",
    exposure = "#0f62fe",
    mediator = "#d9fbfb",
    mediator_or_sensitivity = "#fcf4d6",
    outcome = "#ffd7d9",
    downstream_outcome = "#e8daff",
    unobserved_exposure_cause = "#e0e0e0"
  )
  nodes$fill <- role_colors[nodes$role]
  nodes$fill[is.na(nodes$fill)] <- "#f4f4f4"
  ggplot2::ggplot() +
    ggplot2::geom_segment(
      data = edges,
      ggplot2::aes(x = x, y = y, xend = x_to, yend = y_to, linetype = edge_role),
      arrow = grid::arrow(length = grid::unit(0.12, "cm"), type = "closed"),
      color = "#525252",
      linewidth = 0.42
    ) +
    ggplot2::geom_label(
      data = nodes,
      ggplot2::aes(x = x, y = y, label = label, fill = fill),
      color = "#161616",
      linewidth = 0.35,
      size = 3.2,
      label.padding = grid::unit(0.18, "lines")
    ) +
    ggplot2::scale_fill_identity() +
    ggplot2::scale_linetype_manual(
      values = c(
        exposure_background = "dotted",
        backdoor_or_selection = "solid",
        exposure_to_mediator_or_outcome = "solid",
        mediator_path = "longdash",
        total_effect_path = "solid",
        downstream_path = "dashed"
      ),
      name = "Kenar rolü"
    ) +
    ggplot2::coord_cartesian(xlim = c(-0.8, 10.8), ylim = c(0.5, 4.45), clip = "off") +
    ggplot2::labs(
      title = "Causal DAG: total-effect ayarlama stratejisi",
      subtitle = "SES, kardeş yaş farkı ve aile büyüklüğü baseline/design karıştırıcıları olarak sabitlenmiştir",
      x = NULL,
      y = NULL,
      caption = "Not. Beck ve antidepresan kullanımı total-effect modellerinde ana ayarlama setine alınmaz; sensitivite katmanında izlenir."
    ) +
    apa_plot_theme(base_size = 10) +
    ggplot2::theme(
      axis.text = ggplot2::element_blank(),
      axis.ticks = ggplot2::element_blank(),
      panel.grid = ggplot2::element_blank()
    )
}

apa_plot_smd_love <- function(propensity_balance_before_after_table) {
  apa_require_plot_packages()
  balance <- propensity_balance_before_after_table
  long <- rbind(
    data.frame(variable = balance$variable, abs_smd = balance$abs_smd_before, stage = "Ağırlık öncesi"),
    data.frame(variable = balance$variable, abs_smd = balance$abs_smd_iptw, stage = "IPTW sonrası"),
    data.frame(variable = balance$variable, abs_smd = balance$abs_smd_matched, stage = "Matching sonrası")
  )
  long$label <- c(
    age_gap = "Kardeş yaş farkı",
    ses_latent = "Latent SES",
    cocuk_sayisi = "Çocuk sayısı"
  )[long$variable]
  long$label[is.na(long$label)] <- long$variable[is.na(long$label)]
  long$label <- factor(long$label, levels = rev(unique(long$label[order(match(long$variable, balance$variable))])))
  long$stage <- factor(long$stage, levels = c("Ağırlık öncesi", "IPTW sonrası", "Matching sonrası"))
  ggplot2::ggplot(long, ggplot2::aes(x = abs_smd, y = label, color = stage)) +
    ggplot2::geom_vline(xintercept = c(0.10, 0.25), linetype = c("dashed", "dotted"), color = c("#6f6f6f", "#a8a8a8"), linewidth = 0.35) +
    ggplot2::geom_line(ggplot2::aes(group = label), color = "#c6c6c6", linewidth = 0.4) +
    ggplot2::geom_point(size = 2.7) +
    ggplot2::scale_color_manual(values = c("Ağırlık öncesi" = "#da1e28", "IPTW sonrası" = "#24a148", "Matching sonrası" = "#0f62fe"), name = NULL) +
    ggplot2::labs(
      title = "Propensity dengeleme: SMD love plot",
      subtitle = "Birincil ayarlama setinde IPTW sonrası tüm |SMD| değerleri 0.01'in altındadır",
      x = "|Standardize mean difference|",
      y = NULL,
      caption = "Not. Kesikli çizgi 0.10 iyi denge eşiğini, noktalı çizgi 0.25 izleme eşiğini gösterir."
    ) +
    apa_plot_theme()
}

apa_plot_propensity_overlap <- function(df_family_propensity, propensity_overlap_summary_table) {
  apa_require_plot_packages()
  df <- df_family_propensity
  df <- df[!is.na(df$ps_value) & !is.na(df$group_f), , drop = FALSE]
  support <- propensity_overlap_summary_table[1, , drop = FALSE]
  ggplot2::ggplot(df, ggplot2::aes(x = ps_value, fill = group_f, color = group_f)) +
    ggplot2::annotate(
      "rect",
      xmin = support$common_support_low,
      xmax = support$common_support_high,
      ymin = -Inf,
      ymax = Inf,
      fill = "#edf5ff",
      alpha = 0.65
    ) +
    ggplot2::geom_density(alpha = 0.28, linewidth = 0.8) +
    ggplot2::geom_rug(alpha = 0.35, sides = "b") +
    ggplot2::scale_fill_manual(values = c("Kontrol" = "#6f6f6f", "DM" = "#0f62fe"), name = "Grup") +
    ggplot2::scale_color_manual(values = c("Kontrol" = "#525252", "DM" = "#0043ce"), name = "Grup") +
    ggplot2::labs(
      title = "Propensity score overlap",
      subtitle = sprintf("Ortak destek aralığı %.3f–%.3f; ortak destek dışında n = %d", support$common_support_low, support$common_support_high, support$outside_common_support_n),
      x = "Propensity score P(DM)",
      y = "Yoğunluk",
      caption = "Not. Mavi arka plan ortak destek aralığını gösterir; rug çizgileri aile-düzeyi gözlemlerdir."
    ) +
    apa_plot_theme()
}

apa_plot_ses_correlation <- function(ses_correlation_summary_table) {
  apa_require_plot_packages()
  corr <- ses_correlation_summary_table
  keep <- c("mean_aile_egitim", "aile_isei08", "material_index", "ses_composite_eq", "ses_hollingshead", "ses_latent")
  corr <- corr[corr$variable_1 %in% keep & corr$variable_2 %in% keep, , drop = FALSE]
  labels <- c(
    mean_aile_egitim = "Eğitim",
    aile_isei08 = "ISEI",
    material_index = "Materyal",
    ses_composite_eq = "Eşit ağırlık",
    ses_hollingshead = "Hollingshead",
    ses_latent = "Latent SES"
  )
  corr$variable_1_label <- labels[corr$variable_1]
  corr$variable_2_label <- labels[corr$variable_2]
  corr$variable_1_label <- factor(corr$variable_1_label, levels = rev(unname(labels[keep])))
  corr$variable_2_label <- factor(corr$variable_2_label, levels = unname(labels[keep]))
  ggplot2::ggplot(corr, ggplot2::aes(x = variable_2_label, y = variable_1_label, fill = r)) +
    ggplot2::geom_tile(color = "white", linewidth = 0.45) +
    ggplot2::geom_text(ggplot2::aes(label = sprintf("%.2f", r)), size = 3.1, color = "#161616") +
    ggplot2::scale_fill_gradient2(low = "#da1e28", mid = "#f4f4f4", high = "#0f62fe", midpoint = 0, limits = c(-1, 1), name = "r") +
    ggplot2::coord_equal() +
    ggplot2::labs(
      title = "SES kompozit doğrulama korelasyon matrisi",
      subtitle = "Latent SES eğitim ve mesleki statü bileşenleriyle yüksek, materyal bileşenle orta korelasyon göstermektedir",
      x = NULL,
      y = NULL,
      caption = "Not. Korelasyonlar aile-düzeyi kanonik analiz tabanından hesaplanmıştır."
    ) +
    apa_plot_theme(base_size = 10) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(angle = 35, hjust = 1))
}

apa_h1_three_way_emm_data <- function(h1_three_way_emmeans_grid_table) {
  rows <- h1_three_way_emmeans_grid_table
  rows <- rows[is.finite(rows$emmean), , drop = FALSE]
  if (nrow(rows) == 0L) {
    stop("H1 three-way EMM grid is empty", call. = FALSE)
  }
  rows$outcome_label <- apa_label_outcome(rows$outcome)
  rows$role_label <- c(
    Kontrol_Indeks = "Kontrol indeks",
    Kontrol_Kardes = "Kontrol kardeş",
    DM_Hasta_Indeks = "DM indeks",
    DM_Hasta_Kardes = "DM kardeş"
  )[as.character(rows$role_f)]
  rows$role_label[is.na(rows$role_label)] <- as.character(rows$role_f[is.na(rows$role_label)])
  rows$role_label <- factor(rows$role_label, levels = c("Kontrol indeks", "Kontrol kardeş", "DM indeks", "DM kardeş"))
  rows$cinsiyet_f <- factor(as.character(rows$cinsiyet_f), levels = c("Kiz", "Erkek"), labels = c("Kız", "Erkek"))
  rows$outcome_label <- factor(
    rows$outcome_label,
    levels = c("EMBU-C Sıcaklık", "EMBU-C Aşırı koruma", "EMBU-C Reddetme", "EMBU-C Karşılaştırma")
  )
  rows
}

apa_plot_h1_three_way_emm <- function(h1_three_way_emmeans_grid_table) {
  apa_require_plot_packages()
  emm <- apa_h1_three_way_emm_data(h1_three_way_emmeans_grid_table)
  ggplot2::ggplot(emm, ggplot2::aes(x = age_year, y = emmean, color = role_label, group = role_label)) +
    ggplot2::geom_ribbon(
      ggplot2::aes(ymin = lower.CL, ymax = upper.CL, fill = role_label),
      alpha = 0.10,
      color = NA
    ) +
    ggplot2::geom_line(linewidth = 0.75) +
    ggplot2::geom_point(size = 1.8) +
    ggplot2::facet_grid(outcome_label ~ cinsiyet_f) +
    ggplot2::scale_color_manual(
      values = c("Kontrol indeks" = "#6f6f6f", "Kontrol kardeş" = "#a8a8a8", "DM indeks" = "#0f62fe", "DM kardeş" = "#007d79"),
      name = "Rol"
    ) +
    ggplot2::scale_fill_manual(
      values = c("Kontrol indeks" = "#6f6f6f", "Kontrol kardeş" = "#a8a8a8", "DM indeks" = "#0f62fe", "DM kardeş" = "#007d79"),
      guide = "none"
    ) +
    ggplot2::labs(
      title = "H1 role × yaş × cinsiyet EMM paneli",
      subtitle = "8, 12 ve 16 yaş ankrajlarında estimated marginal mean ve %95 güven aralıkları",
      x = "Çocuk yaşı (yıl)",
      y = "EMBU-C tahmini ortalama",
      caption = "Not. Üçlü etkileşim testlerinin tamamı FDR sonrası anlamsızdır; panel görsel tanı amaçlıdır."
    ) +
    apa_plot_theme(base_size = 9)
}

apa_mediation_effects_data <- function(mediation_simple_effect_table,
                                       mediation_multilevel_effect_table,
                                       mediation_conditional_effect_table) {
  add_model <- function(df, model_label) {
    if (nrow(df) == 0L) return(data.frame())
    df$model_label <- model_label
    df
  }
  rows <- rbind(
    add_model(mediation_simple_effect_table, "Tek-mediator"),
    add_model(mediation_multilevel_effect_table, "Multilevel"),
    add_model(mediation_conditional_effect_table, "Conditional process")
  )
  keep <- c("a", "b", "cprime", "indirect", "cond_indirect_kontrol", "cond_indirect_dm", "index_mod_mediation")
  rows <- rows[rows$parameter %in% keep & is.finite(rows$estimate), , drop = FALSE]
  if (nrow(rows) == 0L) {
    stop("Mediation effect tables contain no plottable parameters", call. = FALSE)
  }
  labels <- c(
    a = "a: Beck → EMBU-P",
    b = "b: EMBU-P → EMBU-C",
    cprime = "c′: DM → EMBU-C",
    indirect = "a×b indirect",
    cond_indirect_kontrol = "Indirect Kontrol",
    cond_indirect_dm = "Indirect DM",
    index_mod_mediation = "IMM"
  )
  rows$parameter_label <- labels[rows$parameter]
  rows$parameter_label[is.na(rows$parameter_label)] <- rows$parameter[is.na(rows$parameter_label)]
  rows$model_label <- factor(rows$model_label, levels = c("Tek-mediator", "Multilevel", "Conditional process"))
  rows$parameter_label <- factor(rows$parameter_label, levels = rev(unique(rows$parameter_label)))
  rows$significant <- !is.na(rows$p_value) & rows$p_value < 0.05
  rows
}

apa_plot_mediation_effects <- function(mediation_simple_effect_table,
                                       mediation_multilevel_effect_table,
                                       mediation_conditional_effect_table) {
  apa_require_plot_packages()
  effects <- apa_mediation_effects_data(
    mediation_simple_effect_table,
    mediation_multilevel_effect_table,
    mediation_conditional_effect_table
  )
  ggplot2::ggplot(effects, ggplot2::aes(x = estimate, y = parameter_label, xmin = ci_lo, xmax = ci_hi, color = significant)) +
    ggplot2::geom_vline(xintercept = 0, linetype = "dashed", color = "grey45", linewidth = 0.35) +
    ggplot2::geom_errorbar(width = 0.16, orientation = "y", linewidth = 0.55) +
    ggplot2::geom_point(size = 2.3) +
    ggplot2::facet_wrap(~ model_label, scales = "free_y", ncol = 1) +
    ggplot2::scale_color_manual(values = c(`FALSE` = "#0f62fe", `TRUE` = "#da1e28"), labels = c(`FALSE` = "p ≥ .05", `TRUE` = "p < .05"), name = NULL) +
    ggplot2::labs(
      title = "KISIM VI mediation: yol ve indirect etki özeti",
      subtitle = "Nokta tahmini ve %95 güven aralığı; indirect etkiler sıfırı içerir",
      x = "Katsayı",
      y = NULL,
      caption = "Not. Bootstrap/FIML ayrıntıları yöntem bölümünde; conditional process Hayes Model 14 indeksini içerir."
    ) +
    apa_plot_theme(base_size = 10)
}

apa_lpa_fit_data <- function(lpa_fit_table) {
  rows <- lpa_fit_table
  if (nrow(rows) == 0L || !"Classes" %in% names(rows)) {
    stop("LPA fit table is empty or missing Classes", call. = FALSE)
  }
  bic <- data.frame(Classes = rows$Classes, metric = "BIC", value = rows$BIC)
  entropy <- data.frame(Classes = rows$Classes, metric = "Entropy", value = rows$Entropy)
  blrt <- data.frame(Classes = rows$Classes, metric = "BLRT p", value = rows$BLRT_p)
  out <- rbind(bic, entropy, blrt)
  out <- out[is.finite(out$value), , drop = FALSE]
  out$metric <- factor(out$metric, levels = c("BIC", "Entropy", "BLRT p"))
  out
}

apa_plot_lpa_fit <- function(lpa_fit_table) {
  apa_require_plot_packages()
  fit <- apa_lpa_fit_data(lpa_fit_table)
  best_bic <- lpa_fit_table$Classes[which.min(lpa_fit_table$BIC)]
  ggplot2::ggplot(fit, ggplot2::aes(x = Classes, y = value)) +
    ggplot2::geom_vline(xintercept = best_bic, color = "#0f62fe", linetype = "dashed", linewidth = 0.35) +
    ggplot2::geom_line(color = "#525252", linewidth = 0.65) +
    ggplot2::geom_point(color = "#0f62fe", size = 2.2) +
    ggplot2::facet_wrap(~ metric, scales = "free_y", ncol = 1) +
    ggplot2::scale_x_continuous(breaks = sort(unique(fit$Classes))) +
    ggplot2::labs(
      title = "KISIM VII LPA model seçim tanıları",
      subtitle = sprintf("Kesikli çizgi BIC minimum çözümü gösterir: %s profil", best_bic),
      x = "Profil sayısı",
      y = NULL,
      caption = "Not. Profil ortalama tabloları tidyLPA sınıf çıkarımı sınırı nedeniyle ayrı denetlenir; bu figür model seçim kanıtını gösterir."
    ) +
    apa_plot_theme(base_size = 10)
}

apa_network_node_labels <- function() {
  c(
    embu_p_sicaklik_mean = "P sıcaklık",
    embu_p_asiri_koruma_mean = "P aşırı kor.",
    embu_p_reddetme_mean = "P reddetme",
    embu_p_karsilastirma_mean = "P karşı.",
    srq_ho_warmth_mean = "SRQ sıcaklık",
    srq_ho_status_mean = "SRQ statü",
    srq_ho_conflict_mean = "SRQ çatışma",
    srq_ho_rivalry_mean = "SRQ rekabet",
    beck_total = "Beck"
  )
}

apa_network_layout_data <- function(network_edges_table, network_centrality_table) {
  edges <- network_edges_table[network_edges_table$group == "all", , drop = FALSE]
  cent <- network_centrality_table[network_centrality_table$group == "all", , drop = FALSE]
  if (nrow(edges) == 0L || nrow(cent) == 0L) {
    stop("Network edge/centrality tables must contain group == 'all'", call. = FALSE)
  }
  variables <- unique(c(cent$variable, edges$from, edges$to))
  angle <- seq(0, 2 * pi, length.out = length(variables) + 1L)[-length(variables) - 1L]
  nodes <- data.frame(
    variable = variables,
    x = cos(angle),
    y = sin(angle),
    stringsAsFactors = FALSE
  )
  nodes <- merge(nodes, cent[, c("variable", "strength", "expected_influence")], by = "variable", all.x = TRUE)
  labels <- apa_network_node_labels()
  nodes$label <- labels[nodes$variable]
  nodes$label[is.na(nodes$label)] <- nodes$variable[is.na(nodes$label)]
  edge_xy <- merge(edges, nodes[, c("variable", "x", "y")], by.x = "from", by.y = "variable", all.x = TRUE)
  edge_xy <- merge(edge_xy, nodes[, c("variable", "x", "y")], by.x = "to", by.y = "variable", all.x = TRUE, suffixes = c("", "_to"))
  list(nodes = nodes, edges = edge_xy)
}

apa_plot_network_graph <- function(network_edges_table, network_centrality_table) {
  apa_require_plot_packages()
  net <- apa_network_layout_data(network_edges_table, network_centrality_table)
  ggplot2::ggplot() +
    ggplot2::geom_segment(
      data = net$edges,
      ggplot2::aes(x = x, y = y, xend = x_to, yend = y_to, linewidth = abs(partial_cor), color = partial_cor),
      alpha = 0.78,
      lineend = "round"
    ) +
    ggplot2::geom_point(
      data = net$nodes,
      ggplot2::aes(x = x, y = y, size = strength, fill = expected_influence),
      shape = 21,
      color = "#161616",
      stroke = 0.35
    ) +
    ggplot2::geom_text(
      data = net$nodes,
      ggplot2::aes(x = x * 1.18, y = y * 1.18, label = label),
      size = 3.1,
      fontface = "bold"
    ) +
    ggplot2::scale_color_gradient2(low = "#da1e28", mid = "#c6c6c6", high = "#0f62fe", midpoint = 0, name = "Kısmi r") +
    ggplot2::scale_fill_gradient2(low = "#da1e28", mid = "#f4f4f4", high = "#0f62fe", midpoint = 0, name = "Expected\ninfluence") +
    ggplot2::scale_linewidth(range = c(0.25, 2.1), guide = "none") +
    ggplot2::scale_size(range = c(4, 9), name = "Strength") +
    ggplot2::coord_equal(xlim = c(-1.45, 1.45), ylim = c(-1.35, 1.35), clip = "off") +
    ggplot2::labs(
      title = "KISIM VIII GGM network haritası",
      subtitle = "EBIC-LASSO havuzlanmış ağ; kenar kalınlığı |partial r|, düğüm boyutu strength merkeziyetidir",
      x = NULL,
      y = NULL,
      caption = "Not. Network koşullu bağımlılık haritasıdır; nedensel yön olarak yorumlanmaz."
    ) +
    apa_plot_theme(base_size = 10) +
    ggplot2::theme(
      axis.text = ggplot2::element_blank(),
      axis.ticks = ggplot2::element_blank(),
      panel.grid = ggplot2::element_blank()
    )
}

apa_nct_data <- function(network_nct_table) {
  row <- network_nct_table[1, , drop = FALSE]
  data.frame(
    metric = c("Network invariance", "Global strength"),
    statistic = c(row$M_invariance, row$global_strength_invariance),
    p_value = c(row$M_invariance_pvalue, row$global_strength_pvalue),
    stringsAsFactors = FALSE
  )
}

apa_plot_network_nct <- function(network_nct_table) {
  apa_require_plot_packages()
  nct <- apa_nct_data(network_nct_table)
  nct$metric <- factor(nct$metric, levels = rev(nct$metric))
  ggplot2::ggplot(nct, ggplot2::aes(x = p_value, y = metric, fill = p_value < 0.05)) +
    ggplot2::geom_vline(xintercept = 0.05, linetype = "dashed", color = "#da1e28", linewidth = 0.35) +
    ggplot2::geom_col(width = 0.55) +
    ggplot2::geom_text(ggplot2::aes(label = sprintf("p = %.2f", p_value)), hjust = -0.08, size = 3.4) +
    ggplot2::scale_fill_manual(values = c(`FALSE` = "#0f62fe", `TRUE` = "#da1e28"), guide = "none") +
    ggplot2::coord_cartesian(xlim = c(0, 1)) +
    ggplot2::labs(
      title = "Network Comparison Test: DM × Kontrol",
      subtitle = "Ağ yapısı ve global strength farkı için permütasyon p-değerleri",
      x = "p-değeri",
      y = NULL,
      caption = "Not. p > .05 değerleri iki grup ağının anlamlı biçimde ayrışmadığını gösterir."
    ) +
    apa_plot_theme()
}

apa_clinical_cart_rf_data <- function(clinical_cart_cp_table, clinical_rf_importance_table) {
  cp <- data.frame(
    panel = "CART cross-validated error",
    label = paste0("split=", clinical_cart_cp_table$n_splits),
    value = clinical_cart_cp_table$xerror,
    lo = clinical_cart_cp_table$xerror - clinical_cart_cp_table$xstd,
    hi = clinical_cart_cp_table$xerror + clinical_cart_cp_table$xstd,
    stringsAsFactors = FALSE
  )
  rf <- clinical_rf_importance_table
  rf$variable_label <- apa_label_outcome(rf$variable)
  rf$variable_label <- c(
    group_dm = "DM grup",
    anne_yas_z = "Anne yaşı",
    ses_latent_z = "Latent SES",
    cocuk_sayisi_z = "Çocuk sayısı"
  )[rf$variable]
  rf$variable_label[is.na(rf$variable_label)] <- apa_label_outcome(rf$variable[is.na(rf$variable_label)])
  imp <- data.frame(
    panel = "Random forest importance",
    label = rf$variable_label,
    value = rf$mean_decrease_gini,
    lo = NA_real_,
    hi = NA_real_,
    stringsAsFactors = FALSE
  )
  out <- rbind(cp, imp)
  out$panel <- factor(out$panel, levels = c("CART cross-validated error", "Random forest importance"))
  out
}

apa_plot_clinical_cart_rf <- function(clinical_cart_cp_table, clinical_rf_importance_table) {
  apa_require_plot_packages()
  dat <- apa_clinical_cart_rf_data(clinical_cart_cp_table, clinical_rf_importance_table)
  ggplot2::ggplot(dat, ggplot2::aes(x = value, y = stats::reorder(label, value))) +
    ggplot2::geom_col(fill = "#0f62fe", alpha = 0.82, width = 0.62) +
    ggplot2::geom_errorbar(ggplot2::aes(xmin = lo, xmax = hi), width = 0.18, na.rm = TRUE, color = "#161616") +
    ggplot2::facet_wrap(~ panel, scales = "free", ncol = 1) +
    ggplot2::labs(
      title = "Klinik model tamamlayıcıları: CART ve Random Forest",
      subtitle = "CART xerror profili ve RF MeanDecreaseGini değişken önemi",
      x = NULL,
      y = NULL,
      caption = "Not. Bu figür karar ağacı yapısının metinsel yerine, karar ağacı/RF tanı metriklerini özetler."
    ) +
    apa_plot_theme(base_size = 10)
}

apa_bayesian_posterior_data <- function(bayes_h1_posterior_table, bayes_h3_posterior_table) {
  h1 <- bayes_h1_posterior_table
  h1$family <- "H1 çocuk algısı"
  h3 <- bayes_h3_posterior_table
  h3$family <- "H3 anne öz-rapor"
  rows <- rbind(h1[, intersect(names(h1), names(h3)), drop = FALSE], h3[, intersect(names(h1), names(h3)), drop = FALSE])
  rows$family <- c(rep("H1 çocuk algısı", nrow(h1)), rep("H3 anne öz-rapor", nrow(h3)))
  rows$outcome_label <- apa_label_outcome(rows$outcome)
  rows$outcome_label <- factor(rows$outcome_label, levels = rev(unique(rows$outcome_label)))
  rows
}

apa_plot_bayesian_forest <- function(bayes_h1_posterior_table, bayes_h3_posterior_table) {
  apa_require_plot_packages()
  post <- apa_bayesian_posterior_data(bayes_h1_posterior_table, bayes_h3_posterior_table)
  ggplot2::ggplot(post, ggplot2::aes(x = estimate, y = outcome_label, xmin = ci_lo, xmax = ci_hi, color = bf_class)) +
    ggplot2::annotate("rect", xmin = -0.10, xmax = 0.10, ymin = -Inf, ymax = Inf, fill = "#e0e0e0", alpha = 0.35) +
    ggplot2::geom_vline(xintercept = 0, linetype = "dashed", color = "grey45", linewidth = 0.35) +
    ggplot2::geom_errorbar(width = 0.16, orientation = "y", linewidth = 0.55) +
    ggplot2::geom_point(size = 2.5) +
    ggplot2::facet_wrap(~ family, scales = "free_y", ncol = 1) +
    ggplot2::scale_color_manual(values = c("Moderate H0" = "#6f6f6f", "Moderate H1" = "#0f62fe"), name = "BF sınıfı") +
    ggplot2::labs(
      title = "KISIM XII Bayesian forest: posterior etki ve BF sınıfı",
      subtitle = "Gri bant yaklaşık ROPE ±0.10 SD; H1 reddetme Moderate H1 olarak ayrışır",
      x = "Posterior ortalama etki",
      y = NULL,
      caption = "Not. Noktalar posterior ortalama, yatay çizgiler %95 güvenilir aralıktır."
    ) +
    apa_plot_theme()
}

apa_bayesian_diagnostics_data <- function(bayes_h1_diagnostics_table, bayes_h3_diagnostics_table) {
  h1 <- bayes_h1_diagnostics_table
  h1$family <- "H1"
  h3 <- bayes_h3_diagnostics_table
  h3$family <- "H3"
  rows <- rbind(h1, h3)
  rows$outcome_label <- apa_label_outcome(rows$outcome)
  rows
}

apa_plot_bayesian_diagnostics <- function(bayes_h1_diagnostics_table, bayes_h3_diagnostics_table) {
  apa_require_plot_packages()
  diag <- apa_bayesian_diagnostics_data(bayes_h1_diagnostics_table, bayes_h3_diagnostics_table)
  ggplot2::ggplot(diag, ggplot2::aes(x = max_rhat, y = min_ess_ratio, color = family, label = outcome_label)) +
    ggplot2::geom_vline(xintercept = 1.01, linetype = "dashed", color = "#da1e28", linewidth = 0.35) +
    ggplot2::geom_point(size = 3.0) +
    ggplot2::geom_text(nudge_y = 0.035, size = 2.9, check_overlap = TRUE) +
    ggplot2::scale_color_manual(values = c("H1" = "#0f62fe", "H3" = "#007d79"), name = NULL) +
    ggplot2::labs(
      title = "Bayesian MCMC tanı paneli",
      subtitle = "Maksimum R-hat ve minimum ESS oranı; divergent transition tüm modellerde 0",
      x = "Maksimum R-hat",
      y = "Minimum ESS oranı",
      caption = "Not. Kesikli çizgi R-hat = 1.01 eşiğini gösterir."
    ) +
    apa_plot_theme(base_size = 10)
}

save_apa_plot <- function(plot, path, width = 8, height = 5, dpi = 320) {
  apa_require_plot_packages()
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  ggplot2::ggsave(path, plot = plot, width = width, height = height, dpi = dpi, units = "in", bg = "white")
  normalizePath(path, winslash = "/", mustWork = TRUE)
}

apa_figure_manifest <- function(paths) {
  paths <- unlist(paths, use.names = TRUE)
  data.frame(
    figure_id = names(paths),
    path = unname(paths),
    exists = file.exists(unname(paths)),
    bytes = ifelse(file.exists(unname(paths)), file.info(unname(paths))$size, NA_real_),
    stringsAsFactors = FALSE
  )
}
