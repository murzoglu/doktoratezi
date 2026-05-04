# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXI/54
# Floor-Aware IRT — Reddetme Madde Kumesi
#
# Standard graded response model (Samejima 1969) ile floor-aware empirical-hist
# GRM (Wang & Wu 2011 Tobit IRT motivasyonu) karsilastirmasi. Mokken
# nonparametric IRT opsiyonel; bulunmazsa mirt::mirt(dentype="empiricalhist")
# ile floor-aware tahmin yapilir.
#
# Skill referanslari: references/psikometri-pipeline.md
# Veri: df_family_scored (anne EMBU-P) ve df_long_scored (cocuk EMBU-C)

floor_irt_subscale_map <- function() {
  if (exists("embu_subscale_map", mode = "function")) {
    return(embu_subscale_map())
  }
  list(
    sicaklik = c(1, 3, 6, 7, 13, 17, 20, 24, 26),
    asiri_koruma = c(4, 8, 14, 15, 19, 23, 25),
    reddetme = c(5, 9, 10, 12, 16, 21, 22, 28),
    karsilastirma = c(2, 11, 18, 27, 29)
  )
}

floor_irt_anne_columns <- function(items) {
  paste0("embu_p_q", sprintf("%02d", items))
}

floor_irt_cocuk_columns <- function(items) {
  paste0("embu_c_q", sprintf("%02d", items))
}

floor_irt_normalize_role <- function(role_value) {
  txt <- as.character(role_value)
  txt <- tolower(iconv(txt, to = "ASCII//TRANSLIT", sub = ""))
  ifelse(grepl("indeks|index", txt), "indeks",
    ifelse(grepl("kardes|sibling", txt), "kardes", NA_character_)
  )
}

floor_irt_floor_threshold_default <- function() 1L

floor_irt_floor_summary <- function(item_data, threshold = floor_irt_floor_threshold_default()) {
  out <- lapply(seq_along(item_data), function(i) {
    col <- item_data[[i]]
    valid <- col[!is.na(col)]
    n_valid <- length(valid)
    n_floor <- sum(valid <= threshold)
    data.frame(
      item = names(item_data)[i],
      n_valid = n_valid,
      n_floor = n_floor,
      floor_share = if (n_valid > 0L) n_floor / n_valid else NA_real_,
      stringsAsFactors = FALSE
    )
  })
  do.call(rbind, out)
}

floor_irt_extract_items <- function(df, columns) {
  if (length(columns) == 0L) {
    stop("floor_irt_extract_items: zero columns supplied", call. = FALSE)
  }
  missing_cols <- setdiff(columns, names(df))
  if (length(missing_cols) > 0L) {
    stop(sprintf(
      "floor_irt_extract_items missing columns: %s",
      paste(missing_cols, collapse = ", ")
    ), call. = FALSE)
  }
  out <- df[, columns, drop = FALSE]
  for (col in columns) {
    out[[col]] <- suppressWarnings(as.integer(as.character(out[[col]])))
  }
  out
}

floor_irt_fit_grm <- function(item_data,
                              dentype = c("Gaussian", "empiricalhist"),
                              technical = list(NCYCLES = 2000)) {
  if (!requireNamespace("mirt", quietly = TRUE)) {
    return(list(status = "mirt_unavailable", dentype = dentype[[1L]]))
  }
  dentype <- match.arg(dentype)
  fit <- tryCatch(
    suppressMessages(mirt::mirt(
      data = as.data.frame(item_data),
      model = 1,
      itemtype = "graded",
      method = "EM",
      dentype = dentype,
      technical = technical,
      verbose = FALSE
    )),
    error = function(e) e
  )
  if (inherits(fit, "error")) {
    return(list(status = "fit_error", dentype = dentype, error_message = conditionMessage(fit)))
  }
  list(status = "ok", dentype = dentype, fit = fit)
}

floor_irt_item_parameters <- function(grm_result, subscale_label, informant_label) {
  if (!is.list(grm_result) || !identical(grm_result$status, "ok")) {
    return(NULL)
  }
  if (!requireNamespace("mirt", quietly = TRUE)) {
    return(NULL)
  }
  coefs <- mirt::coef(grm_result$fit, IRTpars = TRUE, simplify = TRUE)$items
  df <- as.data.frame(coefs)
  df$item <- rownames(coefs)
  df$subscale <- subscale_label
  df$informant <- informant_label
  df$dentype <- grm_result$dentype
  rownames(df) <- NULL
  df[, c("subscale", "informant", "dentype", "item",
    setdiff(names(df), c("subscale", "informant", "dentype", "item"))), drop = FALSE]
}

floor_irt_score_thetas <- function(grm_result) {
  if (!is.list(grm_result) || !identical(grm_result$status, "ok")) {
    return(NULL)
  }
  if (!requireNamespace("mirt", quietly = TRUE)) {
    return(NULL)
  }
  thetas <- as.numeric(mirt::fscores(grm_result$fit, method = "EAP", verbose = FALSE)[, 1L])
  thetas
}

floor_irt_compare_thetas <- function(theta_standard, theta_floor_aware,
                                     subscale_label, informant_label) {
  if (is.null(theta_standard) || is.null(theta_floor_aware)) {
    return(data.frame(
      subscale = subscale_label,
      informant = informant_label,
      n = 0L,
      pearson_r = NA_real_,
      mean_abs_delta = NA_real_,
      sd_delta = NA_real_,
      stringsAsFactors = FALSE
    ))
  }
  ok <- !is.na(theta_standard) & !is.na(theta_floor_aware)
  if (sum(ok) < 5L) {
    return(data.frame(
      subscale = subscale_label,
      informant = informant_label,
      n = sum(ok),
      pearson_r = NA_real_,
      mean_abs_delta = NA_real_,
      sd_delta = NA_real_,
      stringsAsFactors = FALSE
    ))
  }
  data.frame(
    subscale = subscale_label,
    informant = informant_label,
    n = sum(ok),
    pearson_r = stats::cor(theta_standard[ok], theta_floor_aware[ok]),
    mean_abs_delta = mean(abs(theta_standard[ok] - theta_floor_aware[ok])),
    sd_delta = stats::sd(theta_standard[ok] - theta_floor_aware[ok]),
    stringsAsFactors = FALSE
  )
}

floor_irt_group_delta <- function(theta_floor_aware, group_dm,
                                  subscale_label, informant_label) {
  if (is.null(theta_floor_aware) || is.null(group_dm)) {
    return(data.frame(
      subscale = subscale_label,
      informant = informant_label,
      n_kontrol = 0L,
      n_dm = 0L,
      mean_kontrol = NA_real_,
      mean_dm = NA_real_,
      cohen_d = NA_real_,
      stringsAsFactors = FALSE
    ))
  }
  ok <- !is.na(theta_floor_aware) & !is.na(group_dm)
  th <- theta_floor_aware[ok]
  gd <- as.integer(group_dm[ok])
  m_k <- mean(th[gd == 0L], na.rm = TRUE)
  m_d <- mean(th[gd == 1L], na.rm = TRUE)
  s_pooled <- stats::sd(th, na.rm = TRUE)
  d <- if (!is.na(s_pooled) && s_pooled > 0) (m_d - m_k) / s_pooled else NA_real_
  data.frame(
    subscale = subscale_label,
    informant = informant_label,
    n_kontrol = sum(gd == 0L),
    n_dm = sum(gd == 1L),
    mean_kontrol = m_k,
    mean_dm = m_d,
    cohen_d = d,
    stringsAsFactors = FALSE
  )
}

floor_irt_run_subscale <- function(item_data, subscale_label, informant_label,
                                   group_dm = NULL,
                                   floor_threshold = floor_irt_floor_threshold_default()) {
  floor_summary <- floor_irt_floor_summary(item_data, threshold = floor_threshold)
  floor_summary$subscale <- subscale_label
  floor_summary$informant <- informant_label

  std <- floor_irt_fit_grm(item_data, dentype = "Gaussian")
  flr <- floor_irt_fit_grm(item_data, dentype = "empiricalhist")

  status_rows <- data.frame(
    subscale = rep(subscale_label, 2L),
    informant = rep(informant_label, 2L),
    model = c("standard_grm", "floor_aware_grm"),
    status = c(std$status, flr$status),
    error_message = c(std$error_message %||% NA_character_, flr$error_message %||% NA_character_),
    stringsAsFactors = FALSE
  )

  std_params <- floor_irt_item_parameters(std, subscale_label, informant_label)
  if (!is.null(std_params)) std_params$model <- "standard_grm"
  flr_params <- floor_irt_item_parameters(flr, subscale_label, informant_label)
  if (!is.null(flr_params)) flr_params$model <- "floor_aware_grm"

  th_std <- floor_irt_score_thetas(std)
  th_flr <- floor_irt_score_thetas(flr)
  comparison <- floor_irt_compare_thetas(th_std, th_flr, subscale_label, informant_label)
  group_delta <- floor_irt_group_delta(th_flr, group_dm, subscale_label, informant_label)

  list(
    floor_summary = floor_summary[, c("subscale", "informant", "item", "n_valid", "n_floor", "floor_share")],
    status = status_rows,
    item_parameters = rbind(std_params, flr_params),
    theta_comparison = comparison,
    group_delta = group_delta
  )
}

floor_irt_run_informant <- function(df, columns_fn, subscale_label, items, informant_label,
                                    group_dm = NULL,
                                    floor_threshold = floor_irt_floor_threshold_default()) {
  cols <- columns_fn(items)
  item_data <- floor_irt_extract_items(df, cols)
  floor_irt_run_subscale(
    item_data = item_data,
    subscale_label = subscale_label,
    informant_label = informant_label,
    group_dm = group_dm,
    floor_threshold = floor_threshold
  )
}

run_floor_aware_irt_pipeline <- function(df_family_scored, df_long_scored,
                                         subscales = NULL,
                                         informants = c("anne", "indeks"),
                                         floor_threshold = floor_irt_floor_threshold_default()) {
  subscale_map <- floor_irt_subscale_map()
  if (is.null(subscales)) {
    subscales <- "reddetme" # Faz II odagi: floor effect en yuksek alt olcek
  }
  unknown <- setdiff(subscales, names(subscale_map))
  if (length(unknown) > 0L) {
    stop(sprintf("Unknown subscales: %s", paste(unknown, collapse = ", ")), call. = FALSE)
  }
  unknown_inf <- setdiff(informants, c("anne", "indeks"))
  if (length(unknown_inf) > 0L) {
    stop(sprintf("Unknown informants: %s", paste(unknown_inf, collapse = ", ")), call. = FALSE)
  }

  group_dm_family <- if ("group_dm" %in% names(df_family_scored)) {
    as.integer(df_family_scored$group_dm)
  } else if ("group_f" %in% names(df_family_scored)) {
    as.integer(df_family_scored$group_f) - 1L
  } else {
    NULL
  }

  if ("indeks" %in% informants) {
    long_indeks <- df_long_scored
    long_indeks$role_token <- floor_irt_normalize_role(long_indeks$family_role_f)
    long_indeks <- long_indeks[!is.na(long_indeks$role_token) & long_indeks$role_token == "indeks", , drop = FALSE]
    group_dm_indeks <- if ("group_dm" %in% names(long_indeks)) {
      as.integer(long_indeks$group_dm)
    } else if ("group_f" %in% names(long_indeks)) {
      as.integer(long_indeks$group_f) - 1L
    } else {
      NULL
    }
  } else {
    long_indeks <- NULL
    group_dm_indeks <- NULL
  }

  floor_rows <- list()
  status_rows <- list()
  param_rows <- list()
  comp_rows <- list()
  delta_rows <- list()

  for (sl in subscales) {
    items <- subscale_map[[sl]]
    if ("anne" %in% informants) {
      r <- floor_irt_run_informant(
        df_family_scored, floor_irt_anne_columns,
        sl, items, "anne",
        group_dm = group_dm_family,
        floor_threshold = floor_threshold
      )
      floor_rows[[paste(sl, "anne", sep = "_")]] <- r$floor_summary
      status_rows[[paste(sl, "anne", sep = "_")]] <- r$status
      if (!is.null(r$item_parameters)) param_rows[[paste(sl, "anne", sep = "_")]] <- r$item_parameters
      comp_rows[[paste(sl, "anne", sep = "_")]] <- r$theta_comparison
      delta_rows[[paste(sl, "anne", sep = "_")]] <- r$group_delta
    }
    if ("indeks" %in% informants) {
      r <- floor_irt_run_informant(
        long_indeks, floor_irt_cocuk_columns,
        sl, items, "indeks",
        group_dm = group_dm_indeks,
        floor_threshold = floor_threshold
      )
      floor_rows[[paste(sl, "indeks", sep = "_")]] <- r$floor_summary
      status_rows[[paste(sl, "indeks", sep = "_")]] <- r$status
      if (!is.null(r$item_parameters)) param_rows[[paste(sl, "indeks", sep = "_")]] <- r$item_parameters
      comp_rows[[paste(sl, "indeks", sep = "_")]] <- r$theta_comparison
      delta_rows[[paste(sl, "indeks", sep = "_")]] <- r$group_delta
    }
  }

  bind <- function(rows) if (length(rows) > 0L) do.call(rbind, rows) else NULL
  list(
    floor_summary = bind(floor_rows),
    status = bind(status_rows),
    item_parameters = bind(param_rows),
    theta_comparison = bind(comp_rows),
    group_delta = bind(delta_rows),
    target_summary = data.frame(
      analysis = "floor_aware_irt_phase2",
      subscales = paste(subscales, collapse = ","),
      informants = paste(informants, collapse = ","),
      floor_threshold = floor_threshold,
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXI/54)",
      reference_doc = "04-sap-faz2-posthoc.md",
      stringsAsFactors = FALSE
    )
  )
}

# NULL coalesce
if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
