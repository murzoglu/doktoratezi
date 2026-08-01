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
    beck_total = "Beck toplam",
    sicaklik = "Sıcaklık",
    asiri_koruma = "Aşırı koruma",
    reddetme = "Reddetme",
    karsilastirma = "Karşılaştırma"
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
    cocuk_sayisi_z = "Çocuk sayısı (z)",
    ses_latent = "Latent SES",
    age_gap = "Kardeş yaş farkı",
    cocuk_sayisi = "Çocuk sayısı",
    anne_yas = "Anne yaşı",
    anne_yas_z = "Anne yaşı (z)",
    mean_aile_egitim = "Aile eğitimi (ortalama)",
    material_index = "Maddi olanak indeksi",
    ses_composite_eq = "SES bileşik (eşit ağırlık)",
    ses_hollingshead = "SES (Hollingshead)",
    beck_dep = "Beck depresyon",
    beck_total = "Beck toplam",
    dm_yili = "DM süresi (yıl)",
    tani_yasi = "Tanı yaşı"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

# P1-15: Ingilizce/snake_case durum-karar etiketlerini Turkce'ye cevirir.
# Haritada olmayan degerler oldugu gibi birakilir (regresyon guvenligi).
apa_status_label <- function(x) {
  map <- c(
    ok = "Tamam",
    fit_ok = "Uyum sağlandı",
    fit_failed = "Uyum sağlanamadı",
    converged = "Yakınsadı",
    pass = "Geçti",
    fail = "Geçemedi",
    ppc_consistent = "Öngörücü denetim tutarlı",
    ppc_inconsistent = "Öngörücü denetim tutarsız",
    consistent = "Tutarlı",
    inconsistent = "Tutarsız",
    Equivalent = "Eşdeğer",
    equivalent = "Eşdeğer",
    not_equivalent = "Eşdeğer değil",
    undetermined = "Belirsiz",
    nonsignificant = "Anlamlı değil",
    significant = "Anlamlı",
    insufficient = "Yetersiz",
    insufficient_data = "Veri yetersiz",
    singular = "Tekil (kimliklenemedi)",
    unavailable = "Uygulanamadı",
    linear = "Doğrusal",
    nonlinear = "Doğrusal değil",
    selected = "Seçilen",
    flag = "İşaretli",
    suspicious = "Şüpheli",
    beklenen = "Beklenen",
    fitted = "Tahmin edildi",
    iyi_denge = "İyi denge",
    kotu_denge = "Zayıf denge",
    dengesiz = "Dengesiz",
    dengeli = "Dengeli",
    sinirda = "Sınırda",
    ciddi_dengesizlik = "Ciddi dengesizlik",
    primary_adjustment_ok = "Birincil ayarlama uygun",
    linear_sufficient = "Doğrusal yeterli",
    nonlinear_preferred = "Doğrusal olmayan tercih edilir",
    boundary_solution = "Sınır çözümü",
    primary_mi_or_fiml = "Birincil: MI/FIML",
    dm_only_high_missing_sensitivity = "Yalnız DM: yüksek eksik (duyarlılık)",
    dm_only_sensitivity_where_matrix = "Yalnız DM: matris duyarlılığı",
    structural_only = "Yalnız yapısal"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  # Bayes faktoru sinif etiketlerini cevir (or. "Very strong H1").
  out <- gsub("Very strong", "Çok güçlü", out, fixed = TRUE)
  out <- gsub("Strong", "Güçlü", out, fixed = TRUE)
  out <- gsub("Moderate", "Orta", out, fixed = TRUE)
  out <- gsub("Anecdotal", "Zayıf", out, fixed = TRUE)
  out <- gsub("Extreme", "Aşırı güçlü", out, fixed = TRUE)
  out <- gsub("Indeterminate", "Belirsiz", out, fixed = TRUE)
  out <- gsub(" H1", " H1 lehine", out, fixed = TRUE)
  out <- gsub(" H0", " H0 lehine", out, fixed = TRUE)
  out
}

# Kovaryat/eksik-veri/blok gibi teknik degisken adlarini Turkce etikete cevirir.
# Haritada olmayan degerler oldugu gibi birakilir (regresyon guvenligi).
apa_var_label <- function(x) {
  map <- c(
    age_gap = "Kardeş yaş farkı",
    age_gap_z = "Kardeş yaş farkı (z)",
    ses_latent = "Latent SES",
    ses_latent_z = "Latent SES (z)",
    cocuk_sayisi = "Çocuk sayısı",
    cocuk_sayisi_z = "Çocuk sayısı (z)",
    anne_yas = "Anne yaşı",
    anne_yas_z = "Anne yaşı (z)",
    aile_isei08 = "Aile ISEI-08 (mesleki indeks)",
    beck_total = "Beck toplam",
    dm_yili = "DM süresi (yıl)",
    material_index = "Maddi olanak indeksi",
    mean_aile_egitim = "Aile eğitimi (ortalama)",
    tani_yasi = "Tanı yaşı",
    beck = "Beck",
    ses = "SES",
    clinical_dm_only = "Klinik (yalnız DM)",
    continuous = "Sürekli",
    binary = "İkili",
    categorical = "Kategorik",
    level = "Düzey"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

# Tablo 1 kategorik degisken duzey kodlarini (0/1/2 ... veya factor etiketi)
# okunur Turkce etikete cevirir. Kaynak: docs/protokol/KANONIK_DEMOGRAFIK_VE_TIBBI_BILGILER.md
# (egitim 0-5, calisma 0/1, ev sahipligi 0/1, araba 0/1) + R/01 same_sex factor etiketi.
apa_table1_level_label <- function(variable, level) {
  variable <- as.character(variable)
  level <- as.character(level)
  # Degisken bazli duzey sozlukleri
  egitim <- c(
    "0" = "Okuma bilmiyor", "1" = "İlkokul", "2" = "Ortaokul",
    "3" = "Lise", "4" = "Üniversite", "5" = "Lisansüstü"
  )
  calisma <- c("0" = "Hayır", "1" = "Evet")
  ev <- c("0" = "Kendi mülkü", "1" = "Kiralık")
  araba <- c("0" = "Yok", "1" = "Var")
  same_sex <- c(
    "Farkli" = "Farklı cinsiyet", "Ayni" = "Aynı cinsiyet",
    "0" = "Farklı cinsiyet", "1" = "Aynı cinsiyet"
  )
  dict_for <- function(v) {
    switch(v,
      egitim_durumu = egitim,
      es_egitim_durumu = egitim,
      calisma_durumu = calisma,
      es_calisma_durumu = calisma,
      ev_sahipligi = ev,
      arabaniz_var_mi = araba,
      same_sex = same_sex,
      NULL
    )
  }
  vapply(seq_along(level), function(i) {
    dict <- dict_for(variable[[i]])
    lv <- level[[i]]
    if (is.null(dict) || !(lv %in% names(dict))) return(lv)
    unname(dict[[lv]])
  }, character(1L))
}

# lavaan uyum indeksi anahtarlarini (cfi.scaled, rmsea, srmr, chisq, df, pvalue ...)
# okunur Turkce/istatistik etiketine cevirir. Olcekli (.scaled) varyantlar ayni
# etikete eslenir; alt-not olarak olcekli oldugu tablo dipnotunda belirtilir.
apa_fit_measure_label <- function(x) {
  map <- c(
    cfi = "CFI", "cfi.scaled" = "CFI",
    tli = "TLI", "tli.scaled" = "TLI",
    rmsea = "RMSEA", "rmsea.scaled" = "RMSEA",
    srmr = "SRMR",
    chisq = "\u03c7\u00b2", "chisq.scaled" = "\u03c7\u00b2",
    df = "sd", "df.scaled" = "sd",
    pvalue = "\u03c7\u00b2 p", "pvalue.scaled" = "\u03c7\u00b2 p"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

# Yeniden siniflandirma metrik kodlarini (NRI_event, IDI_total ...) Turkce etikete cevirir.
apa_reclassification_label <- function(x) {
  map <- c(
    NRI_event = "NRI (olaylı)", NRI_nonevent = "NRI (olaysız)", NRI_total = "NRI (toplam)",
    IDI_event = "IDI (olaylı)", IDI_nonevent = "IDI (olaysız)", IDI_total = "IDI (toplam)"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

# Antidepresan/duyarlilik strata ve senaryo adlarini Turkce'ye cevirir.
apa_stratum_label <- function(x) {
  map <- c(
    all_adjusted_for_antidepressant = "Tümü (antidepresan ayarlı)",
    no_antidepressant = "Antidepresan yok",
    antidepressant_only = "Yalnız antidepresan",
    short_dm = "Kısa DM süresi",
    good_control = "İyi metabolik kontrol",
    negctrl_random = "Negatif kontrol (rastgele)",
    negctrl_aile_no = "Negatif kontrol (aile no)"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

# LCA sinif karsilastirma etiketlerini Turkce'ye cevirir (2_vs_reference vb.).
apa_class_contrast_label <- function(x) {
  out <- as.character(x)
  out <- gsub("_vs_reference", ". sınıf vs. referans", out)
  out <- gsub("_vs_", ". sınıf vs. ", out)
  out
}

# Grup etiketlerini Turkce'ye cevirir (havuzlanmis = pooled vb.).
apa_group_label <- function(x) {
  map <- c(
    Pooled = "Havuzlanmış", pooled = "Havuzlanmış",
    all = "Havuzlanmış", DM = "DM", Kontrol = "Kontrol", Control = "Kontrol"
  )
  out <- as.character(x)
  idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]])
  out
}

# n=NA gibi eksik sayilari okunur bir tire ile gosterir.
apa_fmt_n <- function(x) {
  out <- suppressWarnings(as.integer(x))
  ifelse(is.na(out), "—", as.character(out))
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
  df <- df[seq_len(min(nrow(df), 40L)), , drop = FALSE]
  level_txt <- apa_table1_level_label(df$variable, df$level)
  label <- ifelse(df$row_type == "level" & nzchar(df$level), paste0(df$label, ": ", level_txt), df$label)
  out <- data.frame(
    Degisken = label,
    Toplam = df$overall,
    DM = df$DM,
    Kontrol = df$Kontrol,
    SMD = apa_fmt_num(df$abs_smd, 2L),
    q = ifelse(is.na(df$q_value_fmt), "", df$q_value_fmt),
    Denge = ifelse(is.na(df$balance_flag) | !nzchar(df$balance_flag), "",
                   apa_status_label(df$balance_flag)),
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 1. Örneklem özellikleri", "Sürekli değişkenler ortalama (SS); medyan [ÇAA], kategorik değişkenler n (%) olarak verilmiştir. Denge sütunu yalnız SMD hesaplanan satırlarda doldurulur. q sütunu, grup farkı testinin (sürekli: Wilcoxon; kategorik: Fisher kesin testi) yanlış keşif oranı (FDR) düzeltmesiyle elde edilen değeridir. Aile mesleki statüsü ISEI-08 baskınlık (dominance) kuralıyla eş (baba) mesleğinden türetildiğinden 'Eş ISEI-08' ile aile düzeyi ISEI-08 sayısal olarak özdeştir; tekrarı önlemek için yalnız eş göstergesi listelenmiştir.")
}

apa_table_covariate_balance <- function(propensity_balance_before_after_table) {
  df <- propensity_balance_before_after_table
  df <- df[order(df$abs_smd_before, decreasing = TRUE), , drop = FALSE]
  out <- data.frame(
    Degisken = apa_var_label(df$variable),
    Tip = apa_var_label(df$variable_type),
    SMD_once = apa_fmt_num(df$abs_smd_before, 3L),
    SMD_IPTW = apa_fmt_num(df$abs_smd_iptw, 3L),
    SMD_matching = apa_fmt_num(df$abs_smd_matched, 3L),
    IPTW_karar = apa_status_label(df$balance_flag_iptw),
    Oneri = apa_status_label(df$recommendation),
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
    Degisken = apa_var_label(df$variable),
    Blok = apa_var_label(df$block),
    Analitik_payda = df$analytic_denominator,
    Analitik_eksik = df$analytic_missing_n,
    Analitik_eksik_yuzde = apa_fmt_num(df$analytic_missing_pct, 1L),
    Yapisal_eksik = df$structural_missing_n,
    Strateji = apa_status_label(df$strategy),
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
    Bilesen = apa_term_label(s$component),
    n = apa_fmt_n(s$non_missing_n),
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
      Bilesen = paste0("DFA uyum: ", apa_fit_measure_label(fit$measure)),
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
    n = apa_fmt_n(apa_col(df, c("n"), NA)),
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
    Kanit = apa_status_label(b$bf_class),
    Rhat_max = apa_fmt_num(d$max_rhat[d_match], 3L),
    Divergent = d$n_divergent[d_match],
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 7. H1 Bayesian dual reporting", "ROPE yüzdesi yüzde birimiyle verilmiştir; BF10 sınıfları ön-kayıtlı dual reporting kararlarına dayanır.")
}

apa_table_h1_period2023 <- function(h1_primary_period2023_group_main_effect_table) {
  df <- h1_primary_period2023_group_main_effect_table
  out <- data.frame(
    Sonuc = apa_outcome_label(apa_col(df, c("outcome"), "")),
    Tahmin = apa_fmt_num(apa_col(df, c("estimate")), 3L),
    GA95 = apa_fmt_ci(apa_col(df, c("ci_low")), apa_col(df, c("ci_high")), 3L),
    p = apa_fmt_p(apa_col(df, c("p_value"))),
    q_FDR = apa_fmt_p(apa_col(df, c("p_fdr_across_h1_group"))),
    stringsAsFactors = FALSE
  )
  apa_table_info(
    apa_nonempty(out),
    "Tablo 6c. H1 dönem duyarlılığı: 2023 ortak-takvim alt örnekleminde birincil grup ana etkisi",
    "Birincil H1 estimandı (dört düzeyli rol; indeks+kardeş eşit-ağırlıklı DM eksi Kontrol emmeans kontrastı; çocuk yaşı, cinsiyet, latent SES, kardeş yaş farkı ve aile çocuk sayısı ayarlı; aile rastgele kesişimli) yalnız 2023 alt örnekleminde (n = 40 kontrol, 108 DM indeks aile) yeniden kestirilmiştir. q sütunu dört alt ölçek üzerinde BH-FDR düzeltmesidir. Bu, dönem/merkez kırılganlığının birincil estimandla doğrudan replikasyonudur."
  )
}

apa_table_h1_group_main_effect <- function(h1_primary_group_main_effect_table) {
  df <- h1_primary_group_main_effect_table
  out <- data.frame(
    Sonuc = apa_outcome_label(apa_col(df, c("outcome"), "")),
    Tahmin = apa_fmt_num(apa_col(df, c("estimate")), 3L),
    GA95 = apa_fmt_ci(apa_col(df, c("ci_low")), apa_col(df, c("ci_high")), 3L),
    p = apa_fmt_p(apa_col(df, c("p_value"))),
    q_FDR = apa_fmt_p(apa_col(df, c("p_fdr_across_h1_group"))),
    stringsAsFactors = FALSE
  )
  apa_table_info(
    apa_nonempty(out),
    "Tablo 6b. H1 doğrulayıcı grup ana etkisi (EMBU-C alt ölçekleri)",
    "Doğrulayıcı estimand: DM eksi Kontrol grup ana etkisi; indeks ve kardeş rolleri eşit ağırlıkla ortalanmıştır. Katsayı ham 1-4 ölçek puanı birimindedir. q sütunu dört alt ölçek üzerinde Benjamini-Hochberg (BH-FDR) düzeltmesidir. Rol-özgül hücre kontrastları (Tablo 6) betimsel ayrıştırmadır ve bu doğrulayıcı aileye girmez."
  )
}

apa_table_h1_within_group_contrast <- function(h1_primary_within_group_role_contrast_table) {
  df <- h1_primary_within_group_role_contrast_table
  if (is.null(df) || nrow(df) == 0L) {
    return(apa_table_info(
      data.frame(
        Sonuc = character(0), Kontrast = character(0), Tahmin = character(0),
        GA95 = character(0), p = character(0), q_FDR = character(0),
        stringsAsFactors = FALSE
      ),
      "Tablo 6d. H1 grup-içi rol kontrastı (aile içi indeks eksi kardeş)",
      "Keşifsel/post-hoc estimand raporlanmadı."
    ))
  }
  contrast_label <- function(x) {
    x <- as.character(x)
    x[x == "DM_indeks_eksi_kardes"] <- "DM: indeks eksi kardeş"
    x[x == "Kontrol_indeks_eksi_kardes"] <- "Kontrol: indeks eksi kardeş"
    x
  }
  out <- data.frame(
    Sonuc = apa_outcome_label(apa_col(df, c("outcome"), "")),
    Kontrast = contrast_label(apa_col(df, c("contrast"), "")),
    Tahmin = apa_fmt_num(apa_col(df, c("estimate")), 3L),
    GA95 = apa_fmt_ci(apa_col(df, c("ci_low")), apa_col(df, c("ci_high")), 3L),
    p = apa_fmt_p(apa_col(df, c("p_value"))),
    q_FDR = apa_fmt_p(apa_col(df, c("p_fdr_within_family"))),
    stringsAsFactors = FALSE
  )
  apa_table_info(
    apa_nonempty(out),
    "Tablo 6d. H1 grup-içi rol kontrastı (aile içi indeks eksi kardeş)",
    "Keşifsel/post-hoc estimand: kontrol grubu dışlanarak DM ailesi içinde indeks çocuk ile sağlıklı kardeşinin farkı; ve simetrik olarak kontrol ailesi içinde indeks eksi kardeş farkı. Aynı çok-düzeyli modelin dört düzeyli rol faktöründen emmeans özel kontrastı ile kestirilmiştir; aile rastgele kesişimi eşli (paired) aile-içi bağımlılığı modeller. Katsayı ham 1-4 ölçek puanı birimindedir. q sütunu sekiz kontrast (iki grup × dört alt ölçek) üzerinde Benjamini-Hochberg (BH-FDR) düzeltmesidir; keşifsel katman olduğundan doğrulayıcı q iddiası taşımaz."
  )
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
    n = apa_fmt_n(p$n),
    stringsAsFactors = FALSE
  )
  i_out <- data.frame(
    Model = "IPTW + HC3",
    Sonuc = apa_outcome_label(i$outcome),
    Beta = apa_fmt_num(i$std_beta, 3L),
    GA95 = apa_fmt_ci(i$std_beta_ci_low, i$std_beta_ci_high, 3L),
    p = apa_fmt_p(i$p_value),
    p_FDR = apa_fmt_p(i$p_fdr_across_h3_iptw),
    n = apa_fmt_n(i$n),
    stringsAsFactors = FALSE
  )
  out <- rbind(p_out, i_out)
  apa_table_info(out, "Tablo 10. H3 anne öz-rapor grup etkileri", "β standardize etkiyi gösterir; IPTW modeli stabilize trimlenmiş ağırlık ve HC3 SE kullanır.")
}

apa_table_h3_sensitivity <- function(h3_antidepressant_stratified_group_effects_table, bayes_h3_posterior_table, robust_tost_equivalence_table) {
  h <- h3_antidepressant_stratified_group_effects_table
  h <- h[h$term == "group_fDM", , drop = FALSE]
  h_out <- data.frame(
    Katman = apa_stratum_label(h$stratum),
    Sonuc = apa_outcome_label(h$outcome),
    Deger = apa_fmt_num(h$std_beta, 3L),
    Aralik = apa_fmt_ci(h$std_beta_ci_low, h$std_beta_ci_high, 3L),
    p = apa_fmt_p(h$p_value),
    Karar = apa_status_label(h$status),
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
    Karar = apa_status_label(b$bf_class),
    Kaynak = "Bayesçi çift raporlama",
    stringsAsFactors = FALSE
  )
  t <- robust_tost_equivalence_table
  t_out <- data.frame(
    Katman = "TOST",
    Sonuc = apa_outcome_label(t$outcome),
    Deger = paste0("SESOI=", apa_fmt_num(t$sesoi, 2L)),
    Aralik = ifelse(is.na(t$observed_d), "d = —",
                    paste0("d = ", apa_fmt_num(t$observed_d, 2L))),
    p = apa_fmt_p(t$tost_p),
    Karar = apa_status_label(t$decision),
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
    Parametre = apa_fit_measure_label(fit_keep$measure),
    Terim = "Uyum",
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

apa_table_h4_multigroup_invariance <- function(h4_multigroup_fit_measures_table,
                                               h4_multigroup_comparison_table) {
  fm <- h4_multigroup_fit_measures_table
  cmp <- h4_multigroup_comparison_table
  if (is.null(cmp) || !is.data.frame(cmp) || nrow(cmp) == 0L) {
    return(apa_table_info(
      data.frame(Not = "H4 çok-grup değişmezlik modeli yakınsamadı veya çalıştırılmadı; ayrıntı için H4 durum tablosuna bakınız.", stringsAsFactors = FALSE),
      "Tablo 12b. H4 çok-grup ölçüm değişmezliği (DM vs Kontrol)",
      "Bkz. H4 çok-grup durum tablosu."
    ))
  }
  mv <- function(mt, measure) {
    if (is.null(fm) || !is.data.frame(fm) || nrow(fm) == 0L) return(NA_real_)
    r <- fm[fm$model_type == mt & fm$measure == measure, , drop = FALSE]
    if (nrow(r) == 0L) NA_real_ else r$value[[1L]]
  }
  lab <- c(
    multigroup_configural = "Yapılandırmasal (configural)",
    multigroup_metric_loadings = "Metrik (yük)",
    multigroup_scalar_thresholds = "Kesişim (scalar)"
  )
  karar <- c(
    acceptable_change = "Kabul edilebilir değişim",
    possible_noninvariance = "Olası değişmezlik ihlali"
  )
  out <- data.frame(
    Duzey = ifelse(cmp$model_type %in% names(lab), unname(lab[cmp$model_type]), cmp$model_type),
    ChiSq = apa_fmt_num(vapply(cmp$model_type, mv, numeric(1L), measure = "chisq.scaled"), 1L),
    sd = apa_fmt_num(vapply(cmp$model_type, mv, numeric(1L), measure = "df.scaled"), 0L),
    CFI = apa_fmt_num(cmp$cfi_scaled, 3L),
    TLI = apa_fmt_num(vapply(cmp$model_type, mv, numeric(1L), measure = "tli.scaled"), 3L),
    RMSEA = apa_fmt_num(cmp$rmsea_scaled, 3L),
    SRMR = apa_fmt_num(cmp$srmr, 3L),
    dCFI = apa_fmt_num(cmp$delta_cfi_scaled, 3L),
    dRMSEA = apa_fmt_num(cmp$delta_rmsea_scaled, 3L),
    Karar = ifelse(is.na(cmp$invariance_flag), "—",
                   ifelse(cmp$invariance_flag %in% names(karar), unname(karar[cmp$invariance_flag]), cmp$invariance_flag)),
    stringsAsFactors = FALSE
  )
  apa_table_info(
    apa_nonempty(out),
    "Tablo 12b. H4 çok-grup ölçüm değişmezliği (DM vs Kontrol)",
    "Daraltılmış 13 EMBU-P + 6 Beck maddelik set üzerinde WLSMV çok-grup taraması; her iki gruba aynı kategori-birleştirme uygulanmıştır. ΔCFI ve ΔRMSEA bir önceki düzeye göredir; karar kuralı ΔCFI ≤ -0,010 veya ΔRMSEA ≥ 0,015 ise olası değişmezlik ihlalidir. En katı (kesişim/scalar) düzey grup-boş sıralı kategoriler nedeniyle yalnız birleştirmeli duyarlılık olarak değerlendirilmiştir."
  )
}

apa_table_h5_concordance <- function(h5_icc_bland_altman_table, h5_dyadic_cfa_latent_corr_table, h5_k_coefficient_table, h5_inconsistency_patterns_table, h5_rsa_parameters_table = NULL, h5_common_fate_regressions_table = NULL) {
  icc <- h5_icc_bland_altman_table[h5_icc_bland_altman_table$dyad == "anne_idx", , drop = FALSE]
  icc <- icc[seq_len(min(nrow(icc), 12L)), , drop = FALSE]
  icc_out <- data.frame(
    Strateji = "ICC + Bland-Altman",
    Olcek = apa_outcome_label(paste0("embu_p_", icc$subscale, "_mean")),
    Grup = apa_group_label(icc$group),
    Deger = paste0("ICC=", apa_fmt_num(icc$icc, 2L)),
    Aralik = apa_fmt_ci(icc$icc_ci_lo, icc$icc_ci_hi, 2L),
    Not = paste0("LoA ", apa_fmt_ci(icc$loa_lo, icc$loa_hi, 2L)),
    stringsAsFactors = FALSE
  )
  cfa <- h5_dyadic_cfa_latent_corr_table
  cfa_out <- data.frame(
    Strateji = "Olsen-Kenny latent CFA",
    Olcek = "Reddetme latent konkordans",
    Grup = apa_group_label(cfa$group),
    Deger = paste0("r=", apa_fmt_num(cfa$true_concordance, 2L)),
    Aralik = "",
    Not = "",
    stringsAsFactors = FALSE
  )
  k <- h5_k_coefficient_table
  k_out <- data.frame(
    Strateji = "Kenny k-katsayısı",
    Olcek = apa_outcome_label(paste0("embu_p_", k$subscale, "_mean")),
    Grup = "Havuzlanmış",
    Deger = paste0("k=", apa_fmt_num(k$k, 2L)),
    Aralik = apa_fmt_ci(k$k_ci_lo, k$k_ci_hi, 2L),
    # P1-1: k guven araligi sifiri kapsadiginda (karara elverissiz genislik)
    # "Uyum saglandi" yaniltici; tahmin edildigini ama GA'nin karar vermeye
    # elverissiz oldugunu belirt.
    Not = ifelse(!is.na(k$k_ci_lo) & !is.na(k$k_ci_hi) & k$k_ci_lo <= 0 & k$k_ci_hi >= 0,
                 "Tahmin edildi; GA karara elverişsiz", apa_status_label(k$status)),
    stringsAsFactors = FALSE
  )
  inc <- h5_inconsistency_patterns_table
  inc_out <- data.frame(
    Strateji = "Klinik tutarsızlık",
    Olcek = inc$description,
    Grup = apa_group_label(inc$group),
    Deger = paste0(apa_fmt_num(100 * inc$prop_flagged, 1L), "%"),
    Aralik = paste0(inc$n_flagged, "/", inc$n),
    Not = paste0("eşik=", inc$threshold),
    stringsAsFactors = FALSE
  )

  # Strateji 2 (Edwards-Parry yanit yuzeyi): tutarsizlik ekseni a4 parametresi
  # alt olcek x grup bazinda ozetlenir (Denetim #18: tabloda eksikti). Tek grup
  # uyum skoru uretmedigi icin a4 (est, p) betimsel olarak raporlanir.
  rsa_out <- NULL
  if (!is.null(h5_rsa_parameters_table) && nrow(h5_rsa_parameters_table) > 0L) {
    r <- h5_rsa_parameters_table[h5_rsa_parameters_table$param == "a4:=b3-b4+b5", , drop = FALSE]
    if (nrow(r) > 0L) {
      rsa_out <- data.frame(
        Strateji = "Yanıt yüzeyi (a4)",
        Olcek = apa_outcome_label(paste0("embu_c_", r$subscale, "_mean")),
        Grup = apa_group_label(r$group),
        Deger = apa_fmt_num(r$est, 2L),
        Aralik = apa_fmt_ci(r$ci.lower, r$ci.upper, 2L),
        Not = apa_fmt_p(r$pvalue),
        stringsAsFactors = FALSE
      )
    }
  }

  # Strateji 3 (ortak yazgi modeli): ortak ebeveynlik latentinin DM etkisi
  # alt olcek bazinda (Denetim #18: tabloda eksikti). Yakinsamayan alt olcekler
  # kaynak tabloda yer almadigi icin otomatik dislanir.
  cf_out <- NULL
  if (!is.null(h5_common_fate_regressions_table) && nrow(h5_common_fate_regressions_table) > 0L) {
    cf <- h5_common_fate_regressions_table[grepl("group|grup|DM", h5_common_fate_regressions_table$rhs, ignore.case = TRUE), , drop = FALSE]
    if (nrow(cf) > 0L) {
      cf_out <- data.frame(
        Strateji = "Ortak yazgı (DM etkisi)",
        Olcek = apa_outcome_label(paste0("embu_c_", cf$subscale, "_mean")),
        Grup = "Havuzlanmış",
        Deger = apa_fmt_num(cf$est, 2L),
        Aralik = "—",
        Not = ifelse(is.na(cf$pvalue), "—", apa_fmt_p(cf$pvalue)),
        stringsAsFactors = FALSE
      )
    }
  }

  out <- rbind(icc_out, rsa_out, cf_out, cfa_out, k_out, inc_out)
  apa_table_info(out, "Tablo 13. H5 diadik tutarlılık stratejileri", "Beş stratejinin özet metrikleri aynı tabloda birleştirilmiştir. Strateji 2 (yanıt yüzeyi) tutarsızlık ekseni a4, Strateji 3 (ortak yazgı) ortak latentin DM etkisiyle özetlenir; her ikisi de tek gruplu yön oyu üretmez. ICC, iki yönlü rastgele etkiler, mutlak uyum, tek ölçüm tanımıyla hesaplanmıştır (ICC(A,1)/ICC(2,1)).")
}

apa_mediation_param_label <- function(x) {
  map <- c(
    a = "a (X→M)", b = "b (M→Y)", cprime = "c′ (doğrudan)",
    indirect = "Dolaylı (a×b)", a1 = "a1", a3 = "a3",
    cond_indirect_kontrol = "Koşullu dolaylı (kontrol)",
    cond_indirect_dm = "Koşullu dolaylı (DM)",
    index_mod_mediation = "Aracılı moderasyon indeksi"
  )
  out <- as.character(x); idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]]); out
}

apa_table_mediation <- function(mediation_simple_effect_table, mediation_multilevel_effect_table, mediation_conditional_effect_table) {
  s <- mediation_simple_effect_table
  s$Model <- "Tek aracılı"
  m <- mediation_multilevel_effect_table
  m$Model <- "Çok düzeyli aracılık"
  cnd <- mediation_conditional_effect_table
  cnd$Model <- "Koşullu süreç"
  df <- rbind(s, m, cnd)
  df <- df[df$parameter %in% c("a", "b", "cprime", "indirect", "a1", "a3", "cond_indirect_kontrol", "cond_indirect_dm", "index_mod_mediation"), , drop = FALSE]
  out <- data.frame(
    Model = df$Model,
    Parametre = apa_mediation_param_label(df$parameter),
    Tahmin = apa_fmt_num(df$estimate, 4L),
    GA95 = apa_fmt_ci(df$ci_lo, df$ci_hi, 4L),
    p = apa_fmt_p(df$p_value),
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 14. Aracılık ve koşullu süreç sonuçları", "Dolaylı etkiler bootstrap/SEM tabanlı güven aralıkları ile sunulur.")
}

apa_table_lpa_bifactor <- function(lpa_fit_table, bifactor_s1_fit_table,
                                   lca_fit_table = NULL,
                                   lca_modal_regression_table = NULL,
                                   flexmix_fit_table = NULL) {
  lpa <- lpa_fit_table
  # Parsimoni-duyarli secim: kesin en dusuk BIC yerine, en dusuk BIC'ten ΔBIC<=2
  # (Raftery 1995: "bare mention" esigi) icinde kalan en az profilli model secilir.
  # ONCEKI HATA: strict min(BIC) 4-profili isaretliyordu, oysa metin 3-profili
  # (ΔBIC=2) parsimoni gerekcesiyle raporluyor -> tablo<->metin celiskisi
  # (denetim P0-7). Bu kural metindeki karari makinede yeniden uretir.
  .bic_min <- min(lpa$BIC, na.rm = TRUE)
  .parsim_ok <- which(lpa$BIC - .bic_min <= 2 + 1e-9)
  .sel_idx <- .parsim_ok[which.min(lpa$Classes[.parsim_ok])]
  lpa_out <- data.frame(
    Bolum = "LPA",
    Model = paste0(lpa$Classes, " profil"),
    BIC = apa_fmt_num(lpa$BIC, 1L),
    Entropy = apa_fmt_num(lpa$Entropy, 2L),
    BLRT_p = apa_fmt_p(lpa$BLRT_p),
    Karar = ifelse(seq_len(nrow(lpa)) == .sel_idx, "Seçilen (parsimoni; ΔBIC\u22642)", ""),
    stringsAsFactors = FALSE
  )
  if (is.data.frame(lca_fit_table) && nrow(lca_fit_table) > 0L) {
    lca <- lca_fit_table[lca_fit_table$status == "ok", , drop = FALSE]
    if (nrow(lca) > 0L) {
      lca_out <- data.frame(
        Bolum = "LCA",
        Model = paste0(lca$nclass, " sınıf"),
        BIC = apa_fmt_num(lca$bic, 1L),
        Entropy = apa_fmt_num(lca$entropy, 2L),
        BLRT_p = "",
        Karar = ifelse(lca$bic == min(lca$bic, na.rm = TRUE), "Seçilen (duyarlılık)", ""),
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
        Model = apa_class_contrast_label(group_row$class_contrast[1]),
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
      Model = paste0(flexmix_fit_table$k[1], " bileşen"),
      BIC = apa_fmt_num(flexmix_fit_table$bic[1], 1L),
      Entropy = "",
      BLRT_p = "",
      Karar = apa_status_label(flexmix_fit_table$status[1]),
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
  apa_table_info(lpa_out, "Tablo 15. LPA, LCA, mixture regression ve Bifactor S-1 model seçim tanıları", "LPA/LCA seçiminde BIC ana karar metriğidir; LCA kategorik gösterge duyarlılık çözümlemesi olarak yorumlanır.")
}

apa_table_network <- function(network_centrality_table, network_nct_table,
                              network_stability_table = NULL) {
  c <- network_centrality_table
  # Denetim P0-3: onceki surum grup filtresi olmadan tum satirlari (all + DM +
  # Kontrol) strength'e gore sirilayip ilk 10'u aliyordu; ayni degisken birden
  # fazla grup degeriyle cikip strength ile expected influence tek "Merkeziyet"
  # kategorisinde birlesiyordu. Duzeltme: yalniz havuzlanmis (group == "all")
  # deger raporlanir ve iki merkeziyet olcutu ayri etiketlenir.
  if ("group_label" %in% names(c)) {
    c <- c[c$group_label == "all", , drop = FALSE]
  } else if ("group" %in% names(c)) {
    c <- c[c$group == "all", , drop = FALSE]
  }
  c <- c[order(c$strength, decreasing = TRUE), , drop = FALSE]
  c <- c[seq_len(min(nrow(c), 6L)), , drop = FALSE]
  cent <- data.frame(
    Bolum = "Merkeziyet (havuzlanmış)",
    Degisken = apa_outcome_label(c$variable),
    Olcut = "Strength",
    Deger = apa_fmt_num(c$strength, 2L),
    Ek = paste0("EI=", apa_fmt_num(c$expected_influence, 2L)),
    p = "",
    stringsAsFactors = FALSE
  )
  nct <- network_nct_table
  nct_out <- data.frame(
    Bolum = "NCT",
    Degisken = c("Network invariance", "Global strength"),
    Olcut = c("M", "S"),
    Deger = apa_fmt_num(c(nct$M_invariance, nct$global_strength_invariance), 3L),
    Ek = paste0("perm=", nct$permutations),
    p = apa_fmt_p(c(nct$M_invariance_pvalue, nct$global_strength_pvalue)),
    stringsAsFactors = FALSE
  )
  out <- rbind(cent, nct_out)
  if (!is.null(network_stability_table) && is.data.frame(network_stability_table) &&
      nrow(network_stability_table) > 0L) {
    st <- network_stability_table
    stab_out <- data.frame(
      Bolum = "Kararlılık (CS)",
      Degisken = c("Strength", "Expected influence"),
      Olcut = "CS(0.7)",
      Deger = apa_fmt_num(c(st$cs_strength[1], st$cs_expected_influence[1]), 2L),
      Ek = paste0("boot=", st$n_boots[1]),
      p = "",
      stringsAsFactors = FALSE
    )
    out <- rbind(out, stab_out)
  }
  apa_table_info(out, "Tablo 16. Network merkeziyet, NCT ve kararlılık", "Merkeziyet satırları havuzlanmış (birleşik) örneklemdendir; Değer = standardize strength, Ek = expected influence (EI). NCT satırlarında M = network invariance test istatistiği, S = global strength farkı. Kararlılık satırlarında CS(0.7) = %70 korelasyon eşiğinde case-dropping bootstrap kararlılık katsayısı (≥0,25 minimum, ≥0,50 tercih; Epskamp ve ark., 2018). Network bulguları koşullu bağımlılık olarak yorumlanır; nedensel yön vermez.")
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
    Ek = paste0("optimizm-düzeltilmiş = ", apa_fmt_num(perf$auc_corrected, 2L)),
    stringsAsFactors = FALSE
  )
  # P1-13: Kalibrasyon intercept/slope (apparent + optimizm-duzeltilmis + %95 GA).
  # Denetim #22: optimizm-duzeltilmis egim/sabit %95 GA'lari metinde vardi ama
  # tabloda yoktu; kaynak tablodaki *_corr_lo/*_corr_hi kolonlari Ek hucresine eklendi.
  cal_src <- rbind(
    data.frame(Model = "Temel", clinical_base_performance[, c("cal_intercept_apparent", "cal_intercept_corrected", "cal_intercept_corr_lo", "cal_intercept_corr_hi", "cal_slope_apparent", "cal_slope_corrected", "cal_slope_corr_lo", "cal_slope_corr_hi")], check.names = FALSE),
    data.frame(Model = "Geniş", clinical_full_performance[, c("cal_intercept_apparent", "cal_intercept_corrected", "cal_intercept_corr_lo", "cal_intercept_corr_hi", "cal_slope_apparent", "cal_slope_corrected", "cal_slope_corr_lo", "cal_slope_corr_hi")], check.names = FALSE)
  )
  cal_out <- rbind(
    data.frame(
      Bolum = "Kalibrasyon",
      Metrik = paste0(cal_src$Model, " kalibrasyon eğimi (slope)"),
      Deger = apa_fmt_num(cal_src$cal_slope_apparent, 2L),
      Ek = paste0("optimizm-düzeltilmiş = ", apa_fmt_num(cal_src$cal_slope_corrected, 2L),
                  " ", apa_fmt_ci(cal_src$cal_slope_corr_lo, cal_src$cal_slope_corr_hi, 2L)),
      stringsAsFactors = FALSE
    ),
    data.frame(
      Bolum = "Kalibrasyon",
      Metrik = paste0(cal_src$Model, " kalibrasyon sabiti (intercept)"),
      Deger = apa_fmt_num(cal_src$cal_intercept_apparent, 2L),
      Ek = paste0("optimizm-düzeltilmiş = ", apa_fmt_num(cal_src$cal_intercept_corrected, 2L),
                  " ", apa_fmt_ci(cal_src$cal_intercept_corr_lo, cal_src$cal_intercept_corr_hi, 2L)),
      stringsAsFactors = FALSE
    )
  )
  # B4b denetimi: NRI/IDI guven araligi/p olmadan raporlanamayacagindan tablodan
  # cikarilmistir; ayrim gucu-kalibrasyon-DCA uclusu korunur. Hesaplama
  # (clinical_nri_idi) pipeline'da kalir ama tabloya yazilmaz. clinical_nri_idi_table
  # argumani geriye-uyum icin imzada tutulur.
  invisible(clinical_nri_idi_table)
  apa_table_info(rbind(perf_out, cal_out), "Tablo 17. Eşzamanlı klinik sınıflandırma (tarama) modeli performansı", "Kesitsel eşzamanlı sınıflandırma; ileriye dönük yordama değildir. Dış validasyon yoktur; performans internal validation (Harrell/Efron bootstrap optimizm düzeltmesi) düzeyinde raporlanır. İdeal kalibrasyon: slope=1, intercept=0.")
}

apa_dm_metric_label <- function(x) {
  map <- c(
    n_dm_total = "DM toplam (n)",
    n_with_dm_yili = "DM süresi bilinen (n)",
    n_with_tani_yasi = "Tanı yaşı bilinen (n)",
    median_dm_yili = "DM süresi (medyan, yıl)",
    median_tani_yasi = "Tanı yaşı (medyan, yıl)"
  )
  out <- as.character(x); idx <- out %in% names(map)
  out[idx] <- unname(map[out[idx]]); out
}

apa_table_dm_clinical <- function(dm_n_summary_table, dm_duration_spline_table, dm_strata_tests_table) {
  .dm_val_fmt <- function(metric, value) {
    v <- suppressWarnings(as.numeric(value))
    is_count <- grepl("^n_|_n$|^n$", metric)
    ifelse(is.na(v), as.character(value),
           ifelse(is_count, as.character(as.integer(round(v))),
                  formatC(v, format = "f", digits = 1L)))
  }
  n_out <- data.frame(
    Analiz = "DM klinik payda",
    Sonuc = apa_dm_metric_label(dm_n_summary_table$metric),
    Deger = .dm_val_fmt(dm_n_summary_table$metric, dm_n_summary_table$value),
    p = "",
    Karar = "",
    stringsAsFactors = FALSE
  )
  s <- dm_duration_spline_table
  s_out <- data.frame(
    Analiz = "DM süresi spline",
    Sonuc = apa_outcome_label(s$outcome),
    Deger = paste0("doğrusal R²=", apa_fmt_num(s$linear_r2, 2L), "; spline R²=", apa_fmt_num(s$spline_r2, 2L)),
    p = apa_fmt_p(s$lrt_p),
    Karar = apa_status_label(s$interpretation),
    stringsAsFactors = FALSE
  )
  st <- dm_strata_tests_table
  st_out <- data.frame(
    Analiz = "Tanı yaşı strata",
    Sonuc = apa_outcome_label(st$outcome),
    Deger = paste0("F=", apa_fmt_num(st$F_value, 2L), "; eta_p=", apa_fmt_num(st$eta_partial, 3L)),
    p = apa_fmt_p(st$p_value),
    Karar = apa_status_label(st$status),
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(n_out, s_out, st_out), "Tablo 18. DM klinik alt-analizleri", "Yalnız DM alt grubunda yürütüldüğü için keşifsel yorumlanır; imputasyon yapılmamıştır.")
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
    Karar = apa_status_label(t$decision),
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
    Karar = apa_status_label(s$status),
    stringsAsFactors = FALSE
  )
  n <- robust_negative_control_table
  n_out <- data.frame(
    Analiz = "Negatif kontrol",
    Sonuc = paste(apa_stratum_label(n$predictor), "→", apa_outcome_label(n$outcome)),
    Deger = paste0("β=", apa_fmt_num(n$estimate, 3L)),
    p = apa_fmt_p(n$p_value),
    Karar = ifelse(n$suspicious, "İşaretli", "Beklenen"),
    stringsAsFactors = FALSE
  )
  f <- robust_falsification_table
  f_out <- data.frame(
    Analiz = "Falsifikasyon",
    Sonuc = paste(apa_stratum_label(f$scenario), apa_outcome_label(f$outcome), sep = ": "),
    Deger = paste0("attenuation=", apa_fmt_num(f$attenuation_pct, 1L), "%"),
    p = apa_fmt_p(f$falsi_p),
    Karar = apa_status_label(f$status),
    stringsAsFactors = FALSE
  )
  apa_table_info(rbind(s_out, n_out, f_out), "Tablo 20. Ölçülmemiş karıştırıcı ve falsifikasyon duyarlılığı", "RVq ve E-value değerleri nedensel dil sınırı için kullanılır. Falsifikasyon satırlarında zayıflama (attenuation) = 100 × (1 − β_altörneklem/β_tam); birincil H3 grup etkileri sıfıra yakın olduğundan bu oran kararsızdır (%100'ü aşan değer işaret dönüşünü, negatif değer büyümeyi gösterir). Falsifikasyon yorumu yüzde büyüklüğüne değil, grup etkisinin her iki senaryoda da anlamsız kalmasına (p > 0,10) dayanır.")
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
    Kanit = apa_status_label(p$bf_class),
    Rhat_max = apa_fmt_num(d$max_rhat[idx], 3L),
    ESS_min_oran = apa_fmt_num(d$min_ess_ratio[idx], 2L),
    Divergent = d$n_divergent[idx],
    stringsAsFactors = FALSE
  )
  if (!is.null(bayes_loo_waic_table) && is.data.frame(bayes_loo_waic_table) && nrow(bayes_loo_waic_table) > 0L) {
    loo <- data.frame(
      Hipotez = "Model uyum tanısı (LOO/WAIC)",
      Sonuc = apa_outcome_label(apa_col(bayes_loo_waic_table, c("model", "analysis", "outcome"), "")),
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
  apa_table_info(out, "Tablo 21. Bayesian dual reporting ve MCMC tanıları", "ESS_min_oran, minimum etkin örneklem büyüklüğü oranıdır (min neff/N; yakınsama tanısı) ve ROPE oranından farklıdır. Rhat ve divergent transition tanıları tüm modellerde raporlanır. LOO/WAIC değerleri her sonuç için tek modelin mutlak öngörücü uyumudur; sonuçlar farklı ölçek/olasılık taşıdığından satırlar arası kıyaslanamaz ve model seçimi amacı taşımaz.")
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
    h1_primary_group_main_effect_table,
    h1_primary_within_group_role_contrast_table = NULL,
    h1_primary_period2023_group_main_effect_table = NULL,
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
    h4_multigroup_fit_measures_table = NULL,
    h4_multigroup_comparison_table = NULL,
    h5_icc_bland_altman_table,
    h5_dyadic_cfa_latent_corr_table,
    h5_k_coefficient_table,
    h5_inconsistency_patterns_table,
    h5_rsa_parameters_table,
    h5_common_fate_regressions_table,
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
    network_stability_table = NULL,
    clinical_base_performance,
    clinical_full_performance,
    clinical_nri_idi_table,
    dm_n_summary_table,
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
    t06_h1_primary = apa_table_effects(h1_primary_fixed_effects_table, "Tablo 6. H1 multilevel ANCOVA sabit etkileri", "Referans kategori Kontrol indeks çocuktur. Rol-özgül katsayılar grup ana etkisinin keşifsel/betimsel ayrıştırmasıdır ve yalnız güven aralıklarıyla raporlanır; doğrulayıcı FDR ailesi (dört EMBU-C alt ölçeğinin grup ana etkisi) ayrı bir tabloda BH-FDR düzeltmeli q değerleriyle verilmiştir (Tablo 6b). Bu nedenle buradaki p sütunu düzeltilmemiş (ham) değerlerdir; doğrulayıcı q iddiası bu tablodan yapılmaz.", term_filter = c("role_fKontrol_Kardes", "role_fDM_Hasta_Indeks", "role_fDM_Hasta_Kardes")),
    t06b_h1_group_main_effect = apa_table_h1_group_main_effect(h1_primary_group_main_effect_table),
    t06c_h1_period2023 = apa_table_h1_period2023(h1_primary_period2023_group_main_effect_table),
    t06d_h1_within_group_contrast = apa_table_h1_within_group_contrast(h1_primary_within_group_role_contrast_table),
    t07_h1_bayesian = apa_table_h1_bayes(bayes_h1_posterior_table, bayes_h1_diagnostics_table),
    t08_h2_family_mean = apa_table_h2_family(h2_family_mean_welch_tests_table),
    t09_h2_apim = apa_table_effects(h2_apim_fixed_effects_table, "Tablo 9. H2 APIM sabit etkileri", "APIM-benzeri karma model aile içi bağımlılığı dikkate alır.", term_filter = c("group_fDM", "family_role_fsibling", "group_fDM:family_role_fsibling")),
    t10_h3_primary_iptw = apa_table_h3_integrated(h3_primary_group_effects_table, h3_iptw_group_effects_table),
    t11_h3_sensitivity = apa_table_h3_sensitivity(h3_antidepressant_stratified_group_effects_table, bayes_h3_posterior_table, robust_tost_equivalence_table),
    t12_h4_sem = apa_table_h4_sem(h4_latent_sem_fit_measures_table, h4_latent_sem_structural_paths_table),
    t12b_h4_multigroup_invariance = apa_table_h4_multigroup_invariance(h4_multigroup_fit_measures_table, h4_multigroup_comparison_table),
    t13_h5_concordance = apa_table_h5_concordance(h5_icc_bland_altman_table, h5_dyadic_cfa_latent_corr_table, h5_k_coefficient_table, h5_inconsistency_patterns_table, h5_rsa_parameters_table, h5_common_fate_regressions_table),
    t14_mediation = apa_table_mediation(mediation_simple_effect_table, mediation_multilevel_effect_table, mediation_conditional_effect_table),
    t15_lpa_bifactor = apa_table_lpa_bifactor(
      lpa_fit_table,
      bifactor_s1_fit_table,
      lca_fit_table,
      lca_modal_regression_table,
      flexmix_fit_table
    ),
    t16_network = apa_table_network(network_centrality_table, network_nct_table, network_stability_table),
    t17_clinical = apa_table_clinical(clinical_base_performance, clinical_full_performance, clinical_nri_idi_table),
    t18_dm_clinical = apa_table_dm_clinical(dm_n_summary_table, dm_duration_spline_table, dm_strata_tests_table),
    t19_robustness = apa_table_robustness(robust_multiverse_summary_table, robust_tost_equivalence_table),
    t20_sensitivity = apa_table_sensitivity(robust_sensemakr_evalue_table, robust_negative_control_table, robust_falsification_table),
    t21_bayesian_global = apa_table_bayesian_global(bayes_h1_posterior_table, bayes_h3_posterior_table, bayes_h1_diagnostics_table, bayes_h3_diagnostics_table, bayes_loo_waic_table),
    t22_result_synthesis = apa_table_result_synthesis(bayes_h1_posterior_table, bayes_h3_posterior_table)
  )
}

apa_table_result_synthesis <- function(bayes_h1_posterior_table = NULL,
                                       bayes_h3_posterior_table = NULL) {
  # H1 BF10 tek dogruluk kaynagi bayes_h1_posterior_table'dir; elle literal
  # yazilmaz (denetim P0-1: onceki "8.12" degeri kanonik model ciktisi olan
  # 10.55'ten kopmustu). Kaynak yoksa metinsel yer tutucuya duser.
  .bf_h1 <- tryCatch({
    b <- bayes_h1_posterior_table
    v <- as.numeric(b$bf10[grepl("reddetme", b$outcome)][1])
    if (is.finite(v)) sprintf("%.2f", v) else "NA"
  }, error = function(e) "NA")
  # H3 BF10 araligi da kanonik H3 posterior tablosundan hesaplanir; elle literal
  # yazilmaz (denetim #27: onceki "0.17-0.25" ust sinir kanonik 0.23'ten kopmustu).
  .bf_h3 <- tryCatch({
    h <- bayes_h3_posterior_table
    v <- as.numeric(h$bf10)
    v <- v[is.finite(v)]
    if (length(v)) sprintf("%.2f-%.2f", min(v), max(v)) else "NA"
  }, error = function(e) "NA")
  out <- data.frame(
    Hipotez = c("H1", "H2", "H3", "H4", "H5", "Sağlamlık (multiverse/TOST)", "Bayesçi çift raporlama"),
    Ana_bulgu = c(
      "EMBU-C reddetme ve aşırı koruma DM'de yüksek (doğrulayıcı grup ana etkisi q<.005 + Bayes BF>6); sıcaklık freq-marjinal/Bayes H0, karşılaştırma null",
      "KİA/SRQ grup farkı kanıtı yetersiz",
      "EMBU-P anne öz-raporda Bayesçi H0 desteği; TOST ±0,30'da 2/4 eşdeğer, 2/4 belirsiz (±0,20/±0,25'te tamamı belirsiz)",
      "Sınırlı global uyumlu SEM'de model-koşullu anne-bildirimli eş-değişimler",
      "Anne-çocuk diadik tutarlılığı zayıf",
      "Multiverse %p<.05 = 0; TOST kısmi eşdeğerlik",
      paste0("H1 reddetme BF10=", .bf_h1, "; H3 BF10=", .bf_h3)
    ),
    Yorum_siniri = c(
      "Çocuk-bildirimli olumlu bulgu; bilgi-vericiye özgü; dönem/merkez kırılganlığı (2023 alt-örnekleminde zayıflar)",
      "Negatif/belirsiz bulgu",
      "Öz-rapor kanalında görünürlük sınırı; mutlak yokluk değil",
      "Nedensel/yordayıcı yorum yok; ilişkisel",
      "Yenilik katkısı; bootstrap CI geniş",
      "Nedensel dayanıklılık zayıf-orta",
      "Çift raporlama bulgularla uyumlu"
    ),
    stringsAsFactors = FALSE
  )
  apa_table_info(out, "Tablo 22. Genel bulgu sentezi", "Tablo yorum sınırını açıkça belirtir; nedensel dil kullanılmaz.")
}

save_apa_table_csv <- function(table, path) {
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)
  if (is.null(table) || (is.data.frame(table) && nrow(table) == 0L)) {
    table <- data.frame(note = "empty result; see status table", stringsAsFactors = FALSE)
  }
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
