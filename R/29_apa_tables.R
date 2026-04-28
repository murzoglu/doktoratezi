# KISIM XIII / 40 — APA tablo üretimi

apa_fmt_num <- function(x, digits = 2L) {
  out <- rep("", length(x))
  ok <- !is.na(x) & is.finite(x)
  out[ok] <- formatC(x[ok], format = "f", digits = digits)
  out
}

apa_fmt_p <- function(p) {
  out <- rep("", length(p))
  ok <- !is.na(p) & is.finite(p)
  out[ok] <- ifelse(p[ok] < 0.001, "<.001", sub("^0", "", formatC(p[ok], format = "f", digits = 3L)))
  out
}

apa_fmt_ci <- function(lo, hi, digits = 2L) {
  sprintf("[%s, %s]", apa_fmt_num(lo, digits), apa_fmt_num(hi, digits))
}

apa_first_col <- function(df, candidates) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0L) {
    return(NA_character_)
  }
  hit[[1L]]
}

apa_col <- function(df, candidates, default = NA) {
  col <- apa_first_col(df, candidates)
  if (is.na(col)) {
    return(rep(default, nrow(df)))
  }
  df[[col]]
}

apa_outcome_label <- function(x) {
  map <- c(
    embu_c_sicaklik_mean = "EMBU-C Sıcaklık",
    embu_c_asiri_koruma_mean = "EMBU-C Aşırı koruma",
    embu_c_reddetme_mean = "EMBU-C Reddetme",
    embu_c_karsilastirma_mean = "EMBU-C Karşılaştırma",
    embu_p_sicaklik_mean = "EMBU-P Sıcaklık",
    embu_p_asiri_koruma_mean = "EMBU-P Aşırı koruma",
    embu_p_reddetme_mean = "EMBU-P Reddetme",
    embu_p_karsilastirma_mean = "EMBU-P Karşılaştırma",
    srq_ho_warmth_mean = "KİA Sıcaklık",
    srq_ho_status_mean = "KİA Statü",
    srq_ho_conflict_mean = "KİA Çatışma",
    srq_ho_rivalry_mean = "KİA Rekabet",
    beck_total = "Beck toplam"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

apa_term_label <- function(x) {
  map <- c(
    "(Intercept)" = "Sabit",
    role_fKontrol_Kardes = "Kontrol kardeş",
    role_fDM_Hasta_Indeks = "DM indeks çocuk",
    role_fDM_Hasta_Kardes = "DM kardeş",
    group_fDM = "DM grubu",
    family_role_fsibling = "Kardeş rolü",
    "group_fDM:family_role_fsibling" = "DM × kardeş rolü",
    cocuk_yas_z = "Çocuk yaşı (z)",
    age_gap_z = "Kardeş yaş farkı (z)",
    ses_latent_z = "Latent SES (z)",
    cocuk_sayisi_z = "Çocuk sayısı (z)"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

apa_nonempty <- function(df, note = "Raporlanabilir satır yok") {
  if (is.null(df) || !is.data.frame(df) || nrow(df) == 0L) {
    return(data.frame(Not = note, stringsAsFactors = FALSE))
  }
  df
}

apa_bind_rows_fill <- function(...) {
  dfs <- list(...)
  dfs <- dfs[vapply(dfs, is.data.frame, logical(1))]
  if (length(dfs) == 0L) {
    return(data.frame())
  }
  cols <- unique(unlist(lapply(dfs, names), use.names = FALSE))
  aligned <- lapply(dfs, function(df) {
    missing <- setdiff(cols, names(df))
    for (col in missing) {
      df[[col]] <- NA
    }
    df[, cols, drop = FALSE]
  })
  do.call(rbind, aligned)
}

apa_table_info <- function(df, title, note) {
  attr(df, "title") <- title
  attr(df, "note") <- note
  df
}

apa_table_sample_characteristics <- function(table1_family_summary_table) {
  keep <- table1_family_summary_table$row_type %in% c("continuous", "level", "binary")
  df <- table1_family_summary_table[keep, , drop = FALSE]
  df <- df[seq_len(min(nrow(df), 28L)), , drop = FALSE]
  label <- ifelse(df$row_type == "level" & nzchar(df$level), paste0(df$label, ": ", df$level), df$label)
  out <- data.frame(
    Degisken = label,
    Toplam = df$overall,
    DM = df$DM,
    Kontrol = df$Kontrol,
    SMD = apa_fmt_num(df$abs_smd, 2L),
    q = df$q_value_fmt,
    Denge = df$balance_flag,
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 1. Örneklem özellikleri", "Sürekli değişkenler ortalama (SS); medyan [ÇAA], kategorik değişkenler n (%) olarak verilmiştir.")
}

apa_table_covariate_balance <- function(propensity_balance_before_after_table) {
  df <- propensity_balance_before_after_table
  df <- df[order(df$abs_smd_before, decreasing = TRUE), , drop = FALSE]
  out <- data.frame(
    Degisken = df$variable,
    Tip = df$variable_type,
    SMD_once = apa_fmt_num(df$abs_smd_before, 3L),
    SMD_IPTW = apa_fmt_num(df$abs_smd_iptw, 3L),
    SMD_matching = apa_fmt_num(df$abs_smd_matched, 3L),
    IPTW_karar = df$balance_flag_iptw,
    Oneri = df$recommendation,
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 2. Kovaryat dengesi", "SMD mutlak değeri verilmiştir; <0.10 iyi denge olarak yorumlanır.")
}

apa_table_missing_data <- function(missing_variable_summary_table) {
  df <- missing_variable_summary_table
  df <- df[order(df$analytic_missing_pct, decreasing = TRUE), , drop = FALSE]
  df <- df[df$analytic_missing_n > 0 | df$structural_missing_n > 0, , drop = FALSE]
  df <- df[seq_len(min(nrow(df), 18L)), , drop = FALSE]
  out <- data.frame(
    Degisken = df$variable,
    Blok = df$block,
    Analitik_payda = df$analytic_denominator,
    Analitik_eksik = df$analytic_missing_n,
    Analitik_eksik_yuzde = apa_fmt_num(df$analytic_missing_pct, 1L),
    Yapisal_eksik = df$structural_missing_n,
    Strateji = df$strategy,
    stringsAsFactors = FALSE
  )
  apa_table_info(apa_nonempty(out, "Analitik eksikliği olan değişken yok"), "Tablo 3. Eksik veri özeti", "Yapısal eksiklikler analitik paydadan ayrıştırılmıştır.")
}

apa_table_propensity_model <- function(propensity_model_summary_table, propensity_weight_summary_table, propensity_overlap_summary_table) {
  model <- propensity_model_summary_table
  out_model <- data.frame(
    Bolum = "Logit PS modeli",
    Terim = apa_term_label(model$term),
    Tahmin = apa_fmt_num(model$estimate, 3L),
    OR_GA95 = paste0(apa_fmt_num(model$odds_ratio, 2L), " ", apa_fmt_ci(model$or_ci_low, model$or_ci_high, 2L)),
    p = apa_fmt_p(model$p_value),
    Not = "",
    stringsAsFactors = FALSE
  )
  w <- propensity_weight_summary_table
  out_weight <- data.frame(
    Bolum = "Ağırlık / ortak destek",
    Terim = paste("Grup", w$group),
    Tahmin = paste0("PS medyan=", apa_fmt_num(w$ps_median, 3L)),
    OR_GA95 = paste0("IPTW max=", apa_fmt_num(w$iptw_max, 2L)),
    p = "",
    Not = paste0("Trimlenen n=", w$trimmed_n),
    stringsAsFactors = FALSE
  )
  ov <- propensity_overlap_summary_table
  out_overlap <- data.frame(
    Bolum = "Ağırlık / ortak destek",
    Terim = "Ortak destek dışı",
    Tahmin = as.character(ov$outside_common_support_n),
    OR_GA95 = paste0("[", apa_fmt_num(ov$common_support_low, 3L), ", ", apa_fmt_num(ov$common_support_high, 3L), "]"),
    p = "",
    Not = "Propensity skoru aralığı",
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(out_model, out_weight, out_overlap), "Tablo 4. Propensity score modeli ve ortak destek", "PS modeli total-effect ayarlama hattı için kullanılmıştır.")
}

apa_table_ses_composite <- function(ses_component_summary_table, ses_cfa_fit_measures_table) {
  s <- ses_component_summary_table
  s <- s[s$component %in% c("mean_aile_egitim", "aile_isei08", "material_index", "ses_composite_eq", "ses_hollingshead", "ses_latent"), , drop = FALSE]
  out <- data.frame(
    Bilesen = s$component,
    n = s$non_missing_n,
    Eksik = s$missing_n,
    Ortalama = apa_fmt_num(s$mean, 2L),
    SS = apa_fmt_num(s$sd, 2L),
    Min = apa_fmt_num(s$min, 2L),
    Maks = apa_fmt_num(s$max, 2L),
    stringsAsFactors = FALSE
  )
  fit <- ses_cfa_fit_measures_table
  if (is.data.frame(fit) && nrow(fit) > 0L) {
    fit_row <- data.frame(
      Bilesen = paste0("CFA fit: ", fit$measure),
      n = "",
      Eksik = "",
      Ortalama = apa_fmt_num(fit$value, 3L),
      SS = "",
      Min = "",
      Maks = "",
      stringsAsFactors = FALSE
    )
    out <- rbind(out, fit_row)
  }
  apa_table_info(out, "Tablo 5. SES kompozit bileşenleri", "Latent SES eğitim, mesleki statü ve materyal bileşenleriyle izlenmiştir.")
}

apa_table_effects <- function(df, title, note, term_filter = NULL, p_col = NULL) {
  if (!is.null(term_filter) && "term" %in% names(df)) {
    df <- df[df$term %in% term_filter, , drop = FALSE]
  }
  p_name <- if (is.null(p_col)) apa_first_col(df, c("p_fdr_across_h1", "p_fdr_across_h2", "p_fdr_across_h3_primary", "p_fdr_across_h3_iptw", "p_value", "pvalue")) else p_col
  est <- apa_col(df, c("std_beta", "estimate", "std.all", "est"))
  lo <- apa_col(df, c("std_beta_ci_low", "ci_low", "ci.lower", "ci_lo"))
  hi <- apa_col(df, c("std_beta_ci_high", "ci_high", "ci.upper", "ci_hi"))
  out <- data.frame(
    Sonuc = apa_outcome_label(apa_col(df, c("outcome", "lhs"), "")),
    Terim = apa_term_label(apa_col(df, c("term", "rhs", "parameter"), "")),
    Tahmin = apa_fmt_num(est, 3L),
    GA95 = apa_fmt_ci(lo, hi, 3L),
    p = apa_fmt_p(if (!is.na(p_name)) df[[p_name]] else rep(NA_real_, nrow(df))),
    n = apa_col(df, c("n"), ""),
    stringsAsFactors = FALSE
  )
  apa_table_info(apa_nonempty(out), title, note)
}

apa_table_h1_bayes <- function(bayes_h1_posterior_table, bayes_h1_diagnostics_table) {
  b <- bayes_h1_posterior_table
  d <- bayes_h1_diagnostics_table
  d_match <- match(b$outcome, d$outcome)
  out <- data.frame(
    Sonuc = apa_outcome_label(b$outcome),
    Posterior_ortalama = apa_fmt_num(b$estimate, 3L),
    CrI95 = apa_fmt_ci(b$ci_lo, b$ci_hi, 3L),
    pd = apa_fmt_num(b$pd, 3L),
    ROPE_yuzde = apa_fmt_num(100 * b$rope_pct, 1L),
    BF10 = apa_fmt_num(b$bf10, 2L),
    Kanit = b$bf_class,
    Rhat_max = apa_fmt_num(d$max_rhat[d_match], 3L),
    Divergent = d$n_divergent[d_match],
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 7. H1 Bayesian dual reporting", "ROPE yüzdesi yüzde birimiyle verilmiştir; BF10 sınıfları ön-kayıtlı dual reporting kararlarına dayanır.")
}

apa_table_h2_family <- function(h2_family_mean_welch_tests_table) {
  df <- h2_family_mean_welch_tests_table
  out <- data.frame(
    Sonuc = apa_outcome_label(df$outcome),
    DM_ort = apa_fmt_num(df$mean_dm, 2L),
    Kontrol_ort = apa_fmt_num(df$mean_control, 2L),
    Fark_GA95 = paste0(apa_fmt_num(df$mean_difference_dm_minus_control, 3L), " ", apa_fmt_ci(df$mean_difference_ci_low, df$mean_difference_ci_high, 3L)),
    Hedges_g_GA95 = paste0(apa_fmt_num(df$hedges_g, 2L), " ", apa_fmt_ci(df$hedges_g_ci_low, df$hedges_g_ci_high, 2L)),
    p_FDR = apa_fmt_p(df$p_fdr_across_h2),
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 8. H2 aile-ortalama Welch testleri", "Etki büyüklüğü Hedges g olarak verilmiştir.")
}

apa_table_h3_integrated <- function(h3_primary_group_effects_table, h3_iptw_group_effects_table) {
  p <- h3_primary_group_effects_table
  i <- h3_iptw_group_effects_table
  p_out <- data.frame(
    Model = "Birincil ANCOVA",
    Sonuc = apa_outcome_label(p$outcome),
    Beta = apa_fmt_num(p$std_beta, 3L),
    GA95 = apa_fmt_ci(p$std_beta_ci_low, p$std_beta_ci_high, 3L),
    p = apa_fmt_p(p$p_value),
    p_FDR = apa_fmt_p(p$p_fdr_across_h3_primary),
    n = p$n,
    stringsAsFactors = FALSE
  )
  i_out <- data.frame(
    Model = "IPTW + HC3",
    Sonuc = apa_outcome_label(i$outcome),
    Beta = apa_fmt_num(i$std_beta, 3L),
    GA95 = apa_fmt_ci(i$std_beta_ci_low, i$std_beta_ci_high, 3L),
    p = apa_fmt_p(i$p_value),
    p_FDR = apa_fmt_p(i$p_fdr_across_h3_iptw),
    n = i$n,
    stringsAsFactors = FALSE
  )
  out <- rbind(p_out, i_out)
  apa_table_info(out, "Tablo 10. H3 anne öz-rapor grup etkileri", "β standardize etkiyi gösterir; IPTW modeli stabilize trimlenmiş ağırlık ve HC3 SE kullanır.")
}

apa_table_h3_sensitivity <- function(h3_antidepressant_stratified_group_effects_table, bayes_h3_posterior_table, robust_tost_equivalence_table) {
  h <- h3_antidepressant_stratified_group_effects_table
  h <- h[h$term == "group_fDM", , drop = FALSE]
  h_out <- data.frame(
    Katman = h$stratum,
    Sonuc = apa_outcome_label(h$outcome),
    Deger = apa_fmt_num(h$std_beta, 3L),
    Aralik = apa_fmt_ci(h$std_beta_ci_low, h$std_beta_ci_high, 3L),
    p = apa_fmt_p(h$p_value),
    Karar = h$status,
    Kaynak = "Antidepresan strata",
    stringsAsFactors = FALSE
  )
  b <- bayes_h3_posterior_table
  b_out <- data.frame(
    Katman = "Bayesian",
    Sonuc = apa_outcome_label(b$outcome),
    Deger = paste0("BF10=", apa_fmt_num(b$bf10, 2L)),
    Aralik = apa_fmt_ci(b$ci_lo, b$ci_hi, 3L),
    p = "",
    Karar = b$bf_class,
    Kaynak = "Bayesian dual reporting",
    stringsAsFactors = FALSE
  )
  t <- robust_tost_equivalence_table
  t_out <- data.frame(
    Katman = "TOST",
    Sonuc = apa_outcome_label(t$outcome),
    Deger = paste0("SESOI=", apa_fmt_num(t$sesoi, 2L)),
    Aralik = paste0("d=", apa_fmt_num(t$observed_d, 2L)),
    p = apa_fmt_p(t$tost_p),
    Karar = t$decision,
    Kaynak = "Eşdeğerlik testi",
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(h_out, b_out, t_out), "Tablo 11. H3 duyarlılık ve dual reporting", "Antidepresan strata, Bayesian kanıt ve TOST eşdeğerlik aynı tabloda sunulur.")
}

apa_table_h4_sem <- function(h4_latent_sem_fit_measures_table, h4_latent_sem_structural_paths_table) {
  paths <- apa_table_effects(
    h4_latent_sem_structural_paths_table,
    "",
    "",
    term_filter = NULL,
    p_col = "p_fdr_across_h4"
  )
  paths$Bolum <- "Yapısal yol"
  names(paths)[names(paths) == "Sonuc"] <- "Parametre"
  fit <- h4_latent_sem_fit_measures_table
  fit_keep <- fit[fit$measure %in% c("cfi.scaled", "tli.scaled", "rmsea.scaled", "srmr", "chisq.scaled", "df.scaled"), , drop = FALSE]
  fit_out <- data.frame(
    Parametre = fit_keep$measure,
    Terim = "Fit",
    Tahmin = apa_fmt_num(fit_keep$value, 3L),
    GA95 = "",
    p = "",
    n = "",
    Bolum = "Model uyumu",
    stringsAsFactors = FALSE
  )
  out <- rbind(paths[, names(fit_out), drop = FALSE], fit_out)
  apa_table_info(out, "Tablo 12. H4 Beck → EMBU-P latent SEM", "Yapısal yollar standardize katsayı ve FDR p-değeri ile raporlanır.")
}

apa_table_h5_concordance <- function(h5_icc_bland_altman_table, h5_dyadic_cfa_latent_corr_table, h5_k_coefficient_table, h5_inconsistency_patterns_table) {
  icc <- h5_icc_bland_altman_table[h5_icc_bland_altman_table$dyad == "anne_idx", , drop = FALSE]
  icc <- icc[seq_len(min(nrow(icc), 12L)), , drop = FALSE]
  icc_out <- data.frame(
    Strateji = "ICC + Bland-Altman",
    Olcek = apa_outcome_label(paste0("embu_p_", icc$subscale, "_mean")),
    Grup = icc$group,
    Deger = paste0("ICC=", apa_fmt_num(icc$icc, 2L)),
    Aralik = apa_fmt_ci(icc$icc_ci_lo, icc$icc_ci_hi, 2L),
    Not = paste0("LoA ", apa_fmt_ci(icc$loa_lo, icc$loa_hi, 2L)),
    stringsAsFactors = FALSE
  )
  cfa <- h5_dyadic_cfa_latent_corr_table
  cfa_out <- data.frame(
    Strateji = "Olsen-Kenny latent CFA",
    Olcek = "Reddetme latent konkordans",
    Grup = cfa$group,
    Deger = paste0("r=", apa_fmt_num(cfa$true_concordance, 2L)),
    Aralik = "",
    Not = "",
    stringsAsFactors = FALSE
  )
  k <- h5_k_coefficient_table
  k_out <- data.frame(
    Strateji = "Kenny k-katsayısı",
    Olcek = apa_outcome_label(paste0("embu_p_", k$subscale, "_mean")),
    Grup = "Pooled",
    Deger = paste0("k=", apa_fmt_num(k$k, 2L)),
    Aralik = apa_fmt_ci(k$k_ci_lo, k$k_ci_hi, 2L),
    Not = k$status,
    stringsAsFactors = FALSE
  )
  inc <- h5_inconsistency_patterns_table
  inc_out <- data.frame(
    Strateji = "Klinik tutarsızlık",
    Olcek = inc$description,
    Grup = inc$group,
    Deger = paste0(apa_fmt_num(100 * inc$prop_flagged, 1L), "%"),
    Aralik = paste0(inc$n_flagged, "/", inc$n),
    Not = paste0("eşik=", inc$threshold),
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(icc_out, cfa_out, k_out, inc_out), "Tablo 13. H5 diadik tutarlılık stratejileri", "Beş stratejinin özet metrikleri aynı tabloda birleştirilmiştir.")
}

apa_table_mediation <- function(mediation_simple_effect_table, mediation_multilevel_effect_table, mediation_conditional_effect_table) {
  s <- mediation_simple_effect_table
  s$Model <- "Tek mediator"
  m <- mediation_multilevel_effect_table
  m$Model <- "Multilevel mediation"
  cnd <- mediation_conditional_effect_table
  cnd$Model <- "Conditional process"
  df <- rbind(s, m, cnd)
  df <- df[df$parameter %in% c("a", "b", "cprime", "indirect", "a1", "a3", "cond_indirect_kontrol", "cond_indirect_dm", "index_mod_mediation"), , drop = FALSE]
  out <- data.frame(
    Model = df$Model,
    Parametre = df$parameter,
    Tahmin = apa_fmt_num(df$estimate, 4L),
    GA95 = apa_fmt_ci(df$ci_lo, df$ci_hi, 4L),
    p = apa_fmt_p(df$p_value),
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 14. Mediation ve conditional process sonuçları", "Indirect etkiler bootstrap/SEM tabanlı güven aralıkları ile sunulur.")
}

apa_table_lpa_bifactor <- function(lpa_fit_table, bifactor_s1_fit_table,
                                   lca_fit_table = NULL,
                                   lca_modal_regression_table = NULL,
                                   flexmix_fit_table = NULL) {
  lpa <- lpa_fit_table
  lpa_out <- data.frame(
    Bolum = "LPA",
    Model = paste0(lpa$Classes, " profil"),
    BIC = apa_fmt_num(lpa$BIC, 1L),
    Entropy = apa_fmt_num(lpa$Entropy, 2L),
    BLRT_p = apa_fmt_p(lpa$BLRT_p),
    Karar = ifelse(lpa$BIC == min(lpa$BIC, na.rm = TRUE), "Seçilen", ""),
    stringsAsFactors = FALSE
  )
  if (is.data.frame(lca_fit_table) && nrow(lca_fit_table) > 0L) {
    lca <- lca_fit_table[lca_fit_table$status == "ok", , drop = FALSE]
    if (nrow(lca) > 0L) {
      lca_out <- data.frame(
        Bolum = "LCA",
        Model = paste0(lca$nclass, " sinif"),
        BIC = apa_fmt_num(lca$bic, 1L),
        Entropy = apa_fmt_num(lca$entropy, 2L),
        BLRT_p = "",
        Karar = ifelse(lca$bic == min(lca$bic, na.rm = TRUE), "Seçilen sensitivity", ""),
        stringsAsFactors = FALSE
      )
      lpa_out <- rbind(lpa_out, lca_out)
    }
  }
  if (is.data.frame(lca_modal_regression_table) && nrow(lca_modal_regression_table) > 0L) {
    group_row <- lca_modal_regression_table[lca_modal_regression_table$term == "group_fDM", , drop = FALSE]
    if (nrow(group_row) > 0L) {
      modal_out <- data.frame(
        Bolum = "LCA modal regresyon",
        Model = group_row$class_contrast[1],
        BIC = paste0("OR=", apa_fmt_num(group_row$odds_ratio[1], 2L),
                     " ", apa_fmt_ci(group_row$or_low[1], group_row$or_high[1], 2L)),
        Entropy = "",
        BLRT_p = apa_fmt_p(group_row$p_value[1]),
        Karar = "Grup sınıf üyeliği",
        stringsAsFactors = FALSE
      )
      lpa_out <- rbind(lpa_out, modal_out)
    }
  }
  if (is.data.frame(flexmix_fit_table) && nrow(flexmix_fit_table) > 0L) {
    flex_out <- data.frame(
      Bolum = "Flexmix",
      Model = paste0(flexmix_fit_table$k[1], " bilesen"),
      BIC = apa_fmt_num(flexmix_fit_table$bic[1], 1L),
      Entropy = "",
      BLRT_p = "",
      Karar = flexmix_fit_table$status[1],
      stringsAsFactors = FALSE
    )
    lpa_out <- rbind(lpa_out, flex_out)
  }
  b <- bifactor_s1_fit_table
  if (is.data.frame(b) && nrow(b) > 0L) {
    measure_col <- apa_first_col(b, c("measure", "fit_measure", "metric", "index"))
    measure <- if (is.na(measure_col)) as.character(seq_len(nrow(b))) else b[[measure_col]]
    value_col <- apa_first_col(b, c("value", "fit", "estimate", "value_num"))
    value <- if (is.na(value_col)) rep(NA_real_, nrow(b)) else b[[value_col]]
    b_out <- data.frame(
      Bolum = "Bifactor S-1",
      Model = measure,
      BIC = apa_fmt_num(value, 3L),
      Entropy = "",
      BLRT_p = "",
      Karar = "Keşifsel uyum",
      stringsAsFactors = FALSE
    )
    lpa_out <- rbind(lpa_out, b_out)
  }
  apa_table_info(lpa_out, "Tablo 15. LPA, LCA, mixture regression ve Bifactor S-1 model seçim tanıları", "LPA/LCA seçiminde BIC ana karar metriğidir; LCA kategorik gösterge sensitivity olarak yorumlanır.")
}

apa_table_network <- function(network_centrality_table, network_nct_table) {
  c <- network_centrality_table
  c <- c[order(c$strength, decreasing = TRUE), , drop = FALSE]
  c <- c[seq_len(min(nrow(c), 10L)), , drop = FALSE]
  cent <- data.frame(
    Bolum = "Merkeziyet",
    Degisken = apa_outcome_label(c$variable),
    Deger = apa_fmt_num(c$strength, 2L),
    Ek = paste0("EI=", apa_fmt_num(c$expected_influence, 2L)),
    p = "",
    stringsAsFactors = FALSE
  )
  nct <- network_nct_table
  nct_out <- data.frame(
    Bolum = "NCT",
    Degisken = c("Network invariance", "Global strength"),
    Deger = apa_fmt_num(c(nct$M_invariance, nct$global_strength_invariance), 3L),
    Ek = paste0("perm=", nct$permutations),
    p = apa_fmt_p(c(nct$M_invariance_pvalue, nct$global_strength_pvalue)),
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(cent, nct_out), "Tablo 16. Network merkeziyet ve NCT", "Network bulguları koşullu bağımlılık olarak yorumlanır; nedensel yön vermez.")
}

apa_table_clinical <- function(clinical_base_performance, clinical_full_performance, clinical_nri_idi_table) {
  perf <- rbind(
    data.frame(Model = "Temel", clinical_base_performance[, c("n", "n_events", "auc", "auc_ci_lo", "auc_ci_hi", "auc_corrected")], check.names = FALSE),
    data.frame(Model = "Geniş", clinical_full_performance[, c("n", "n_events", "auc", "auc_ci_lo", "auc_ci_hi", "auc_corrected")], check.names = FALSE)
  )
  perf_out <- data.frame(
    Bolum = "Performans",
    Metrik = paste0(perf$Model, " AUC"),
    Deger = paste0(apa_fmt_num(perf$auc, 2L), " ", apa_fmt_ci(perf$auc_ci_lo, perf$auc_ci_hi, 2L)),
    Ek = paste0("optimism-corrected=", apa_fmt_num(perf$auc_corrected, 2L)),
    stringsAsFactors = FALSE
  )
  nri <- clinical_nri_idi_table
  nri_out <- data.frame(
    Bolum = "Yeniden sınıflandırma",
    Metrik = nri$metric,
    Deger = apa_fmt_num(nri$value, 3L),
    Ek = "",
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(perf_out, nri_out), "Tablo 17. Klinik risk skoru performansı", "Dış validasyon yoktur; skor internal validation düzeyinde raporlanır.")
}

apa_table_dm_clinical <- function(dm_n_summary_table, dm_hba1c_interaction_table, dm_duration_spline_table, dm_strata_tests_table) {
  n_out <- data.frame(
    Analiz = "DM klinik payda",
    Sonuc = dm_n_summary_table$metric,
    Deger = as.character(dm_n_summary_table$value),
    p = "",
    Karar = "",
    stringsAsFactors = FALSE
  )
  h <- dm_hba1c_interaction_table
  h_out <- data.frame(
    Analiz = "HbA1c × ebeveynlik",
    Sonuc = apa_outcome_label(h$outcome),
    Deger = paste0("β=", apa_fmt_num(h$estimate, 3L), "; R2=", apa_fmt_num(h$r_squared, 2L)),
    p = apa_fmt_p(h$p_value),
    Karar = h$status,
    stringsAsFactors = FALSE
  )
  s <- dm_duration_spline_table
  s_out <- data.frame(
    Analiz = "DM süresi spline",
    Sonuc = apa_outcome_label(s$outcome),
    Deger = paste0("linear R2=", apa_fmt_num(s$linear_r2, 2L), "; spline R2=", apa_fmt_num(s$spline_r2, 2L)),
    p = apa_fmt_p(s$lrt_p),
    Karar = s$interpretation,
    stringsAsFactors = FALSE
  )
  st <- dm_strata_tests_table
  st_out <- data.frame(
    Analiz = "Tanı yaşı strata",
    Sonuc = apa_outcome_label(st$outcome),
    Deger = paste0("F=", apa_fmt_num(st$F_value, 2L), "; eta_p=", apa_fmt_num(st$eta_partial, 3L)),
    p = apa_fmt_p(st$p_value),
    Karar = st$status,
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(n_out, h_out, s_out, st_out), "Tablo 18. DM klinik alt-analizleri", "HbA1c n=39 olduğu için keşifsel yorumlanır; imputasyon yapılmamıştır.")
}

apa_table_robustness <- function(robust_multiverse_summary_table, robust_tost_equivalence_table) {
  m <- robust_multiverse_summary_table
  m_out <- data.frame(
    Analiz = "Multiverse",
    Sonuc = apa_outcome_label(m$outcome),
    Deger = paste0("median d=", apa_fmt_num(m$median_d, 2L), " ", apa_fmt_ci(m$d_q05, m$d_q95, 2L)),
    Ek = paste0("%p<.05=", apa_fmt_num(100 * m$pct_p_lt_05, 1L)),
    Karar = "Spesifikasyon eğrisi",
    stringsAsFactors = FALSE
  )
  t <- robust_tost_equivalence_table
  t_out <- data.frame(
    Analiz = "TOST",
    Sonuc = apa_outcome_label(t$outcome),
    Deger = paste0("SESOI=", apa_fmt_num(t$sesoi, 2L)),
    Ek = paste0("p=", apa_fmt_p(t$tost_p)),
    Karar = t$decision,
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(m_out, t_out), "Tablo 19. Robustluk: multiverse ve TOST", "SESOI ±0.30 SMD olarak tanımlanmıştır.")
}

apa_table_sensitivity <- function(robust_sensemakr_evalue_table, robust_negative_control_table, robust_falsification_table) {
  s <- robust_sensemakr_evalue_table
  s_out <- data.frame(
    Analiz = "Sensemakr / E-value",
    Sonuc = apa_outcome_label(s$outcome),
    Deger = paste0("RVq=", apa_fmt_num(s$RV_q, 3L), "; E=", apa_fmt_num(s$evalue_point, 2L)),
    p = apa_fmt_p(s$p_value),
    Karar = s$status,
    stringsAsFactors = FALSE
  )
  n <- robust_negative_control_table
  n_out <- data.frame(
    Analiz = "Negative control",
    Sonuc = paste(n$predictor, "→", apa_outcome_label(n$outcome)),
    Deger = paste0("β=", apa_fmt_num(n$estimate, 3L)),
    p = apa_fmt_p(n$p_value),
    Karar = ifelse(n$suspicious, "flag", "beklenen"),
    stringsAsFactors = FALSE
  )
  f <- robust_falsification_table
  f_out <- data.frame(
    Analiz = "Falsification",
    Sonuc = paste(f$scenario, apa_outcome_label(f$outcome), sep = ": "),
    Deger = paste0("attenuation=", apa_fmt_num(f$attenuation_pct, 1L), "%"),
    p = apa_fmt_p(f$falsi_p),
    Karar = f$status,
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(s_out, n_out, f_out), "Tablo 20. Ölçülmemiş karıştırıcı ve falsifikasyon duyarlılığı", "RVq ve E-value değerleri nedensel dil sınırı için kullanılır.")
}

apa_table_bayesian_global <- function(bayes_h1_posterior_table, bayes_h3_posterior_table, bayes_h1_diagnostics_table, bayes_h3_diagnostics_table, bayes_loo_waic_table = NULL) {
  p <- apa_bind_rows_fill(
    data.frame(Hipotez = "H1", bayes_h1_posterior_table, check.names = FALSE),
    data.frame(Hipotez = "H3", bayes_h3_posterior_table, check.names = FALSE)
  )
  d <- apa_bind_rows_fill(
    data.frame(Hipotez = "H1", bayes_h1_diagnostics_table, check.names = FALSE),
    data.frame(Hipotez = "H3", bayes_h3_diagnostics_table, check.names = FALSE)
  )
  key <- paste(p$Hipotez, p$outcome)
  d_key <- paste(d$Hipotez, d$outcome)
  idx <- match(key, d_key)
  out <- data.frame(
    Hipotez = p$Hipotez,
    Sonuc = apa_outcome_label(p$outcome),
    Ortalama = apa_fmt_num(p$estimate, 3L),
    CrI95 = apa_fmt_ci(p$ci_lo, p$ci_hi, 3L),
    BF10 = apa_fmt_num(p$bf10, 2L),
    Kanit = p$bf_class,
    Rhat_max = apa_fmt_num(d$max_rhat[idx], 3L),
    ESS_min_oran = apa_fmt_num(d$min_ess_ratio[idx], 2L),
    Divergent = d$n_divergent[idx],
    stringsAsFactors = FALSE
  )
  if (!is.null(bayes_loo_waic_table) && is.data.frame(bayes_loo_waic_table) && nrow(bayes_loo_waic_table) > 0L) {
    loo <- data.frame(
      Hipotez = "Model karşılaştırma",
      Sonuc = apa_col(bayes_loo_waic_table, c("model", "analysis", "outcome"), ""),
      Ortalama = "",
      CrI95 = "",
      BF10 = "",
      Kanit = paste0(
        "LOO=", apa_fmt_num(apa_col(bayes_loo_waic_table, c("looic", "loo_ic", "elpd_loo"), NA_real_), 1L),
        "; WAIC=", apa_fmt_num(apa_col(bayes_loo_waic_table, c("waic", "waic_value"), NA_real_), 1L)
      ),
      Rhat_max = "",
      ESS_min_oran = "",
      Divergent = "",
      stringsAsFactors = FALSE
    )
    out <- rbind(out, loo)
  }
  apa_table_info(out, "Tablo 21. Bayesian dual reporting ve MCMC tanıları", "Rhat ve divergent transition tanıları tüm modellerde raporlanır.")
}

apa_build_table_bundle <- function(
    table1_family_summary_table,
    propensity_balance_before_after_table,
    missing_variable_summary_table,
    propensity_model_summary_table,
    propensity_weight_summary_table,
    propensity_overlap_summary_table,
    ses_component_summary_table,
    ses_cfa_fit_measures_table,
    h1_primary_fixed_effects_table,
    h1_primary_anova_table,
    bayes_h1_posterior_table,
    bayes_h1_diagnostics_table,
    h2_family_mean_welch_tests_table,
    h2_apim_fixed_effects_table,
    h3_primary_group_effects_table,
    h3_iptw_group_effects_table,
    h3_antidepressant_stratified_group_effects_table,
    bayes_h3_posterior_table,
    bayes_h3_diagnostics_table,
    robust_tost_equivalence_table,
    h4_latent_sem_fit_measures_table,
    h4_latent_sem_structural_paths_table,
    h5_icc_bland_altman_table,
    h5_dyadic_cfa_latent_corr_table,
    h5_k_coefficient_table,
    h5_inconsistency_patterns_table,
    mediation_simple_effect_table,
    mediation_multilevel_effect_table,
    mediation_conditional_effect_table,
    lpa_fit_table,
    lca_fit_table,
    lca_modal_regression_table,
    flexmix_fit_table,
    bifactor_s1_fit_table,
    network_centrality_table,
    network_nct_table,
    clinical_base_performance,
    clinical_full_performance,
    clinical_nri_idi_table,
    dm_n_summary_table,
    dm_hba1c_interaction_table,
    dm_duration_spline_table,
    dm_strata_tests_table,
    robust_multiverse_summary_table,
    robust_sensemakr_evalue_table,
    robust_negative_control_table,
    robust_falsification_table,
    bayes_loo_waic_table = NULL) {
  list(
    t01_sample_characteristics = apa_table_sample_characteristics(table1_family_summary_table),
    t02_covariate_balance = apa_table_covariate_balance(propensity_balance_before_after_table),
    t03_missing_data = apa_table_missing_data(missing_variable_summary_table),
    t04_propensity_model = apa_table_propensity_model(propensity_model_summary_table, propensity_weight_summary_table, propensity_overlap_summary_table),
    t05_ses_composite = apa_table_ses_composite(ses_component_summary_table, ses_cfa_fit_measures_table),
    t06_h1_primary = apa_table_effects(h1_primary_fixed_effects_table, "Tablo 6. H1 multilevel ANCOVA sabit etkileri", "Referans kategori Kontrol indeks çocuktur.", term_filter = c("role_fKontrol_Kardes", "role_fDM_Hasta_Indeks", "role_fDM_Hasta_Kardes")),
    t07_h1_bayesian = apa_table_h1_bayes(bayes_h1_posterior_table, bayes_h1_diagnostics_table),
    t08_h2_family_mean = apa_table_h2_family(h2_family_mean_welch_tests_table),
    t09_h2_apim = apa_table_effects(h2_apim_fixed_effects_table, "Tablo 9. H2 APIM sabit etkileri", "APIM-benzeri karma model aile içi bağımlılığı dikkate alır.", term_filter = c("group_fDM", "family_role_fsibling", "group_fDM:family_role_fsibling")),
    t10_h3_primary_iptw = apa_table_h3_integrated(h3_primary_group_effects_table, h3_iptw_group_effects_table),
    t11_h3_sensitivity = apa_table_h3_sensitivity(h3_antidepressant_stratified_group_effects_table, bayes_h3_posterior_table, robust_tost_equivalence_table),
    t12_h4_sem = apa_table_h4_sem(h4_latent_sem_fit_measures_table, h4_latent_sem_structural_paths_table),
    t13_h5_concordance = apa_table_h5_concordance(h5_icc_bland_altman_table, h5_dyadic_cfa_latent_corr_table, h5_k_coefficient_table, h5_inconsistency_patterns_table),
    t14_mediation = apa_table_mediation(mediation_simple_effect_table, mediation_multilevel_effect_table, mediation_conditional_effect_table),
    t15_lpa_bifactor = apa_table_lpa_bifactor(
      lpa_fit_table,
      bifactor_s1_fit_table,
      lca_fit_table,
      lca_modal_regression_table,
      flexmix_fit_table
    ),
    t16_network = apa_table_network(network_centrality_table, network_nct_table),
    t17_clinical = apa_table_clinical(clinical_base_performance, clinical_full_performance, clinical_nri_idi_table),
    t18_dm_clinical = apa_table_dm_clinical(dm_n_summary_table, dm_hba1c_interaction_table, dm_duration_spline_table, dm_strata_tests_table),
    t19_robustness = apa_table_robustness(robust_multiverse_summary_table, robust_tost_equivalence_table),
    t20_sensitivity = apa_table_sensitivity(robust_sensemakr_evalue_table, robust_negative_control_table, robust_falsification_table),
    t21_bayesian_global = apa_table_bayesian_global(bayes_h1_posterior_table, bayes_h3_posterior_table, bayes_h1_diagnostics_table, bayes_h3_diagnostics_table, bayes_loo_waic_table),
    t22_result_synthesis = apa_table_result_synthesis()
  )
}

apa_table_result_synthesis <- function() {
  out <- data.frame(
    Hipotez = c("H1", "H2", "H3", "H4", "H5", "KISIM XI", "KISIM XII"),
    Ana_bulgu = c(
      "EMBU-C reddetme DM grubunda yüksek",
      "KİA/SRQ grup farkı kanıtı yetersiz",
      "EMBU-P anne öz-raporda grup farkı yok",
      "Beck depresyonu EMBU-P latent yollarını yordar",
      "Anne-çocuk diadik tutarlılığı zayıf",
      "Multiverse %p<.05 = 0; TOST kısmi eşdeğerlik",
      "H1 reddetme BF10=8.12; H3 BF10=0.17-0.25"
    ),
    Yorum_siniri = c(
      "Multi-informant olumlu bulgu",
      "Negatif/indeterminate bulgu",
      "Üç-katmanlı H0 kanıtı",
      "Assosiyatif SEM; nedensel dil yok",
      "Yenilik katkısı; bootstrap CI geniş",
      "Nedensel dayanıklılık zayıf-orta",
      "Dual reporting bulgularla uyumlu"
    ),
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 22. Genel bulgu sentezi", "Tablo yorum sınırını açıkça belirtir; nedensel dil kullanılmaz.")
}

save_apa_table_csv <- function(table, path) {
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  utils::write.csv(table, path, row.names = FALSE, fileEncoding = "UTF-8")
  normalizePath(path, winslash = "/", mustWork = TRUE)
}

save_apa_table_bundle <- function(bundle, directory = "outputs/tables") {
  if (!is.list(bundle) || length(bundle) == 0L) {
    stop("APA table bundle must be a non-empty named list", call. = FALSE)
  }
  ids <- names(bundle)
  if (any(!nzchar(ids)) || anyDuplicated(ids)) {
    stop("APA table bundle must have unique non-empty names", call. = FALSE)
  }
  paths <- file.path(directory, paste0("apa_", ids, ".csv"))
  names(paths) <- ids
  for (id in ids) {
    save_apa_table_csv(bundle[[id]], paths[[id]])
  }
  out <- normalizePath(paths, winslash = "/", mustWork = TRUE)
  names(out) <- ids
  out
}

apa_table_manifest <- function(paths, bundle) {
  if (is.null(names(paths))) {
    names(paths) <- tools::file_path_sans_ext(basename(paths))
  }
  rows <- lapply(names(paths), function(id) {
    bundle_id <- id
    if (is.null(bundle[[bundle_id]]) && startsWith(bundle_id, "apa_")) {
      bundle_id <- sub("^apa_", "", bundle_id)
    }
    table <- bundle[[bundle_id]]
    path <- paths[[id]]
    title <- attr(table, "title", exact = TRUE)
    note <- attr(table, "note", exact = TRUE)
    if (is.null(title) || length(title) == 0L) {
      title <- bundle_id
    }
    if (is.null(note) || length(note) == 0L) {
      note <- ""
    }
    data.frame(
      table_id = bundle_id,
      title = title,
      note = note,
      path = normalizePath(path, winslash = "/", mustWork = FALSE),
      exists = file.exists(path),
      bytes = if (file.exists(path)) file.info(path)$size else NA_real_,
      rows = if (is.data.frame(table)) nrow(table) else NA_integer_,
      cols = if (is.data.frame(table)) ncol(table) else NA_integer_,
      stringsAsFactors = FALSE
    )
  })
  out <- do.call(rbind, rows)
  rownames(out) <- NULL
  out
}
