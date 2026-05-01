source("R/34_cross_informant_network.R")

set.seed(20260503L)

# 1) Node specs
specs <- xinfo_node_specs()
stopifnot(nrow(specs) == 12L)
stopifnot(all(c("anne", "cocuk_indeks") %in% specs$informant))
stopifnot(sum(specs$informant == "anne") == 5L)        # 4 EMBU-P + Beck
stopifnot(sum(specs$informant == "cocuk_indeks") == 7L) # 4 EMBU-C + 3 SRQ

# 2) Synthetic fixture: kismi-korele dugumler (EBIC-LASSO en az birkac edge bulsun)
n_families <- 120L
shared_factor <- stats::rnorm(n_families)        # ortak latent
shared_indeks <- stats::rnorm(n_families)        # cocuk-spesifik
shared_anne <- stats::rnorm(n_families)          # anne-spesifik

mk_corr_var <- function(loading_shared, loading_specific, specific_factor, n) {
  loading_shared * shared_factor +
    loading_specific * specific_factor +
    sqrt(1 - loading_shared^2 - loading_specific^2) * stats::rnorm(n)
}

family_df <- data.frame(
  aile_no = seq_len(n_families),
  group_f = factor(rep(c("Kontrol", "DM"), each = n_families / 2L), levels = c("Kontrol", "DM")),
  embu_p_sicaklik_mean = mk_corr_var(0.6, 0.4, shared_anne, n_families),
  embu_p_asiri_koruma_mean = mk_corr_var(0.5, 0.5, shared_anne, n_families),
  embu_p_reddetme_mean = mk_corr_var(0.5, 0.5, shared_anne, n_families),
  embu_p_karsilastirma_mean = mk_corr_var(0.4, 0.6, shared_anne, n_families),
  beck_total = mk_corr_var(0.5, 0.4, shared_anne, n_families),
  stringsAsFactors = FALSE
)

long_df <- data.frame(
  aile_no = rep(seq_len(n_families), each = 2L),
  family_role_f = factor(rep(c("Indeks", "Kardes"), n_families), levels = c("Indeks", "Kardes")),
  stringsAsFactors = FALSE
)
ix_indeks <- which(long_df$family_role_f == "Indeks")
ix_kardes <- which(long_df$family_role_f == "Kardes")
add_long_var <- function(df, col, n_indeks, n_kardes, ix_i, ix_k,
                         loading_shared, loading_specific, specific_factor) {
  values <- numeric(nrow(df))
  values[ix_i] <- mk_corr_var(loading_shared, loading_specific, specific_factor, n_indeks)
  values[ix_k] <- stats::rnorm(n_kardes)
  df[[col]] <- values
  df
}
for (col in c(
  "embu_c_sicaklik_mean", "embu_c_asiri_koruma_mean",
  "embu_c_reddetme_mean", "embu_c_karsilastirma_mean",
  "srq_ho_warmth_mean", "srq_ho_status_mean", "srq_ho_conflict_mean"
)) {
  long_df <- add_long_var(
    long_df, col,
    length(ix_indeks), length(ix_kardes),
    ix_indeks, ix_kardes,
    loading_shared = 0.5, loading_specific = 0.4, specific_factor = shared_indeks
  )
}

# 3) Prepare data: paired wide
paired <- xinfo_prepare_data(family_df, long_df)
stopifnot(nrow(paired) == n_families)
stopifnot("group_f" %in% names(paired))

# Coverage
cov <- xinfo_coverage(paired, specs$variable, group_label = "all")
stopifnot(cov$n_rows == n_families)
stopifnot(cov$n_variables == 12L)

# 4) Pipeline (group split disabled for speed)
if (requireNamespace("qgraph", quietly = TRUE)) {
  result <- run_cross_informant_network_pipeline(
    family_df, long_df,
    group_split = FALSE
  )
  stopifnot(nrow(result$nodes) == 12L)
  stopifnot(nrow(result$status) >= 1L)
  if (any(result$status$status == "ok")) {
    stopifnot(!is.null(result$centrality))
    stopifnot(all(c("strength", "expected_influence") %in% names(result$centrality)))
    # Edges ve summary EBIC-LASSO sonucunda bos olabilir; eger varsa schema kontrolu
    if (!is.null(result$edges) && nrow(result$edges) > 0L) {
      stopifnot(all(c("from", "to", "from_informant", "to_informant",
                      "cross_informant", "weight") %in% names(result$edges)))
    }
    if (!is.null(result$cross_informant_summary)) {
      stopifnot("cross_informant_share" %in% names(result$cross_informant_summary))
    }
  } else {
    cat(sprintf(
      "[xinfo test] GGM not estimated: %s\n",
      paste(result$status$status, collapse = ", ")
    ))
  }

  # Group split (3 grup: all + Kontrol + DM)
  result_grouped <- run_cross_informant_network_pipeline(
    family_df, long_df,
    group_split = TRUE
  )
  stopifnot(nrow(result_grouped$status) == 3L)
  stopifnot(all(c("all", "Kontrol", "DM") %in% result_grouped$status$group_label))
} else {
  cat("[xinfo test] qgraph unavailable, skipping\n")
}

# 5) Edges-table empty edge-case
stopifnot(nrow(xinfo_edges_table(list(status = "qgraph_unavailable"))) == 0L)
stopifnot(nrow(xinfo_centrality_table(list(status = "qgraph_unavailable"))) == 0L)

cat("PASS: tests/test_cross_informant_network.R\n")
