source("R/10_derived_scores.R")

stopifnot(identical(lengths(embu_subscale_map()), c(
  sicaklik = 9L,
  asiri_koruma = 7L,
  reddetme = 8L,
  karsilastirma = 5L
)))

srq_fo <- srq_first_order_map()
srq_ho <- srq_higher_order_map(srq_fo)
stopifnot(length(srq_fo) == 16L)
stopifnot(identical(unname(lengths(srq_fo)), rep(3L, 16L)))
stopifnot(identical(lengths(srq_ho), c(warmth = 21L, status = 12L, conflict = 9L, rivalry = 6L)))

embu_fixture <- as.data.frame(as.list(stats::setNames(
  rep(1, 29),
  embu_score_item_columns("embu_p")
)))
embu_fixture$embu_p_q25 <- 4
embu_scored <- derive_embu_scores(embu_fixture, "embu_p", "embu_p")
stopifnot(identical(unname(embu_scored$embu_p_sicaklik_sum_complete), 9))
stopifnot(identical(unname(embu_scored$embu_p_asiri_koruma_sum_complete), 10))
stopifnot(identical(unname(embu_scored$embu_p_asiri_koruma_valid_n), 7))
stopifnot(isTRUE(all.equal(unname(embu_scored$embu_p_asiri_koruma_mean), 10 / 7)))

embu_missing <- embu_fixture
embu_missing$embu_p_q04 <- NA_real_
embu_missing_scored <- derive_embu_scores(embu_missing, "embu_p", "embu_p", min_present_pct = 0.50)
stopifnot(is.na(embu_missing_scored$embu_p_asiri_koruma_sum_complete))
stopifnot(isTRUE(all.equal(unname(embu_missing_scored$embu_p_asiri_koruma_mean), 9 / 6)))

embu_low_present <- embu_fixture
for (column in embu_score_item_columns("embu_p", c(4, 8, 14, 15))) {
  embu_low_present[[column]] <- NA_real_
}
embu_low_present_scored <- derive_embu_scores(embu_low_present, "embu_p", "embu_p", min_present_pct = 0.50)
stopifnot(is.na(embu_low_present_scored$embu_p_asiri_koruma_mean))

srq_fixture <- as.data.frame(as.list(stats::setNames(
  as.numeric(1:48),
  srq_score_item_columns("srq")
)))
srq_scored <- derive_srq_scores(srq_fixture, "srq", "srq")
stopifnot(identical(unname(srq_scored$srq_fo_intimacy_sum_complete), 1 + 17 + 33))
stopifnot(identical(unname(srq_scored$srq_fo_intimacy_mean), 17))
stopifnot(isTRUE(all.equal(
  unname(srq_scored$srq_ho_warmth_mean),
  mean(unlist(srq_fo[c(
    "intimacy",
    "prosocial",
    "companionship",
    "similarity",
    "admiration_by_sib",
    "admiration_of_sib",
    "affection"
  )], use.names = FALSE))
)))

beck_fixture <- as.data.frame(as.list(stats::setNames(rep(1, 21), beck_score_item_columns("beck"))))
beck_scored <- derive_beck_scores(beck_fixture)
stopifnot(identical(unname(beck_scored$beck_total), 21))
stopifnot(identical(as.character(beck_scored$beck_severity), "Orta"))
stopifnot(identical(as.character(beck_scored$beck_clinical), "Klinik_duzey"))

beck_missing <- beck_fixture
beck_missing$beck_3 <- NA_real_
beck_missing_scored <- derive_beck_scores(beck_missing)
stopifnot(is.na(beck_missing_scored$beck_total))
stopifnot(identical(unname(beck_missing_scored$beck_valid_n), 20))

range_fixture <- as.data.frame(as.list(stats::setNames(
  rep(3, 48),
  srq_score_item_columns("srq")
)))
range_ok <- score_range_block(range_fixture, srq_score_item_columns("srq"), 1, 5, "test", "SRQ", "srq")
stopifnot(isTRUE(assert_no_score_range_violations(range_ok)))

range_bad_fixture <- range_fixture
range_bad_fixture$srq_1 <- 9
range_bad <- score_range_block(range_bad_fixture, srq_score_item_columns("srq"), 1, 5, "test", "SRQ", "srq")
stopifnot(range_bad$n_out_of_range == 1L)
stopifnot(inherits(try(assert_no_score_range_violations(range_bad), silent = TRUE), "try-error"))

dictionary <- derived_score_dictionary()
stopifnot(nrow(dictionary) == 78L)
stopifnot(any(dictionary$score_prefix == "srq_fo" & dictionary$subscale == "intimacy"))
stopifnot(any(dictionary$score_prefix == "srq_ho" & dictionary$subscale == "warmth"))
stopifnot(any(dictionary$score_prefix == "beck" & dictionary$subscale == "total"))

score_columns <- score_columns_from_dictionary(dictionary)
stopifnot("beck_total" %in% score_columns)
stopifnot("srq_ho_warmth_mean" %in% score_columns)
