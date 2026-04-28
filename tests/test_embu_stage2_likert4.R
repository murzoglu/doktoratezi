source("R/03_embu_stage2_likert4.R")

make_stage1_fixture <- function() {
  embu_p <- as.data.frame(matrix(c(
    1, 2, 3, 4, 5, 6,
    6, 5, 4, 3, 2, 1
  ), nrow = 6, ncol = 2))
  names(embu_p) <- c("embu_p_q01", "embu_p_q02")

  embu_c <- as.data.frame(matrix(c(
    1, 1, 2, 3, 4, 4,
    1, 2, 3, 4, 5, 6
  ), nrow = 6, ncol = 2))
  names(embu_c) <- c("embu_c_q01", "embu_c_q02")

  remaining_p <- as.data.frame(matrix(2, nrow = 6, ncol = 27))
  names(remaining_p) <- paste0("embu_p_q", sprintf("%02d", 3:29))
  remaining_c <- as.data.frame(matrix(2, nrow = 6, ncol = 27))
  names(remaining_c) <- paste0("embu_c_q", sprintf("%02d", 3:29))

  data.frame(
    source_row_number = 1:6,
    aile_no = c(1, 1, 2, 2, 3, 3),
    embu_p,
    remaining_p,
    embu_c,
    remaining_c,
    embu_p_likert_version = "6pt",
    embu_c_likert_version = c("4pt", "4pt", "4pt", "6pt", "6pt", "6pt"),
    stringsAsFactors = FALSE,
    check.names = FALSE
  )
}

result <- convert_embu_likert4(make_stage1_fixture())
converted <- result$data
sensitivity <- result$sensitivity_data

p_cols <- paste0("embu_p_q", sprintf("%02d", 1:29))
c_cols <- paste0("embu_c_q", sprintf("%02d", 1:29))

stopifnot(all(p_cols %in% names(converted)))
stopifnot(all(c_cols %in% names(converted)))
stopifnot(all(unlist(converted[p_cols]) %in% 1:4))
stopifnot(all(unlist(converted[c_cols]) %in% 1:4))
stopifnot(identical(converted$embu_p_likert_version_original, rep("6pt", 6)))
stopifnot(identical(converted$embu_c_likert_version_original,
                    c("4pt", "4pt", "4pt", "6pt", "6pt", "6pt")))
stopifnot(identical(unique(converted$embu_p_likert_version), "4pt"))
stopifnot(identical(unique(converted$embu_c_likert_version), "4pt"))

stopifnot(identical(converted$embu_c_q01[1:3], c(1, 1, 2)))
stopifnot(all(converted$embu_c_q01[4:6] %in% 1:4))
stopifnot(all(converted$embu_p_q01 %in% 1:4))

stopifnot(all(c("form", "item", "value_6pt", "value_4pt_eq",
                "value_4pt_rounded", "method") %in% names(result$tables$item)))
stopifnot(nrow(result$tables$item) == 29 * 6)
stopifnot(nrow(result$tables$pooled) == 6)

pooled_ref <- c(rep(1, 3066), rep(2, 2227), rep(3, 1501), rep(4, 2014))
pooled_measured <- c(rep(1, 1459), rep(2, 572), rep(3, 708),
                     rep(4, 585), rep(5, 678), rep(6, 1160))
boundary_lookup <- build_empirical_equip_lookup(
  pooled_ref,
  pooled_measured,
  reference_percentile = "upper_boundary"
)
midpoint_lookup <- build_empirical_equip_lookup(
  pooled_ref,
  pooled_measured,
  reference_percentile = "midpoint"
)

stopifnot(identical(boundary_lookup$value_4pt_rounded, c(1L, 1L, 1L, 2L, 3L, 4L)))
stopifnot(identical(midpoint_lookup$value_4pt_rounded, c(1L, 2L, 2L, 3L, 3L, 4L)))
stopifnot(identical(unique(result$tables$pooled_sensitivity$reference_percentile),
                    "midpoint"))
stopifnot(identical(sensitivity$embu_p_conversion_method,
                    rep("pooled_embu_c_midpoint_equip_percentile_rounded", nrow(sensitivity))))
stopifnot(identical(sensitivity$embu_c_conversion_method,
                    converted$embu_c_conversion_method))
stopifnot(!identical(sensitivity[p_cols], converted[p_cols]))

cat("EMBU stage 2 Likert conversion tests passed\n")
