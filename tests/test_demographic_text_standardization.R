source("R/05_demographic_text_standardization.R")

fixture <- data.frame(
  aile_no = c(42, 77, 65, 2007),
  cocuk_no = c("42-1", "77-1", "65-1", "2007-1"),
  es_calisma_durumu = c(0, 1, 1, 1),
  es_calistigi_is = c("avukat", NA, "muhendis", "Emekli"),
  calisma_durumu = c(1, 1, 0, 0),
  calistigi_is = c("ogretmen", NA, NA, "isci"),
  kronik_hastalik_durumu = c(0, 0, 1, 0),
  hastalik_engel = c(NA, NA, NA, "Tiroid"),
  esiniz_kronik_hastalik_durumu = c(0, 1, 1, 0),
  es_hastalik_engel = c(NA, "Astim, Tip 2 DM", NA, NA),
  stringsAsFactors = FALSE
)

standardized_result <- standardize_demographic_final_family(fixture)
standardized_family <- standardized_result$family
audit <- standardized_result$audit

stopifnot(!any(demographic_free_text_columns() %in% names(standardized_family)))
stopifnot(all(occupation_standard_columns() %in% names(standardized_family)))
stopifnot(all(disease_category_names("anne") %in% names(standardized_family)))
stopifnot(all(disease_category_names("es") %in% names(standardized_family)))

row42 <- standardized_family[standardized_family$aile_no == 42, ]
stopifnot(identical(row42$es_calisma_durumu, 1))
stopifnot(identical(row42$es_isco08_4digit, "2611"))
stopifnot(!is.na(row42$aile_isei08))

row77 <- standardized_family[standardized_family$aile_no == 77, ]
stopifnot(identical(row77$es_meslek_kodlama_durumu, "missing_text"))
stopifnot(is.na(row77$es_isco08_4digit))

row2007_occupation <- standardized_family[standardized_family$aile_no == 2007, ]
stopifnot(identical(row2007_occupation$es_meslek_kodlama_durumu,
                    "retired_not_working"))
stopifnot(identical(row2007_occupation$es_calisma_durumu, 0))
stopifnot(identical(row2007_occupation$es_emekli, 1L))
stopifnot(is.na(row2007_occupation$es_isco08_4digit))
stopifnot(is.na(row2007_occupation$aile_isei08))

row2007 <- standardized_family[standardized_family$aile_no == 2007, ]
stopifnot(identical(row2007$kronik_hastalik_durumu, 1))
stopifnot(identical(row2007$anne_hastalik_endokrin, 1L))
stopifnot(identical(row2007$anne_hastalik_kategori_sayisi, 1L))
stopifnot(identical(row2007$anne_hastalik_kodlama_durumu,
                    "final_flag_corrected"))

row65 <- standardized_family[standardized_family$aile_no == 65, ]
stopifnot(identical(row65$anne_hastalik_kodlama_durumu, "missing_text"))
stopifnot(is.na(row65$anne_hastalik_endokrin))
stopifnot(identical(row65$es_hastalik_kodlama_durumu, "missing_text"))
stopifnot(is.na(row65$es_hastalik_endokrin))

row77_spouse <- standardized_family[standardized_family$aile_no == 77, ]
stopifnot(identical(row77_spouse$es_hastalik_endokrin, 1L))
stopifnot(identical(row77_spouse$es_hastalik_solunum, 1L))
stopifnot(identical(row77_spouse$es_hastalik_kategori_sayisi, 2L))

fmf_sleep_apnea <- draft_code_chronic_condition("Fmf, Uyku Apnesi", 1)
stopifnot(identical(fmf_sleep_apnea$hastalik_solunum, 1L))
stopifnot(identical(fmf_sleep_apnea$hastalik_otoimmun, 1L))
stopifnot(identical(fmf_sleep_apnea$hastalik_diger, 0L))

type1 <- draft_code_chronic_condition("Tip1", 1)
stopifnot(identical(type1$hastalik_endokrin, 1L))
stopifnot(identical(type1$hastalik_diger, 0L))

myasthenia <- draft_code_chronic_condition("Mystania Gravis", 1)
stopifnot(identical(myasthenia$hastalik_sinir, 1L))
stopifnot(identical(myasthenia$hastalik_diger, 0L))

stomach_cancer <- draft_code_chronic_condition("mide ca", 1)
stopifnot(identical(stomach_cancer$hastalik_neoplazm, 1L))
stopifnot(identical(stomach_cancer$hastalik_diger, 1L))

long_fixture <- rbind(fixture, fixture)
long_fixture$cocuk_no <- c("42-1", "77-1", "65-1", "2007-1",
                           "42-2", "77-2", "65-2", "2007-2")
standardized_long <- merge_demographic_standardization_into_long(
  long_fixture,
  standardized_family
)

stopifnot(!any(demographic_free_text_columns() %in% names(standardized_long)))
stopifnot(all(occupation_standard_columns() %in% names(standardized_long)))
stopifnot(identical(
  unique(standardized_long$es_isco08_4digit[standardized_long$aile_no == 42]),
  "2611"
))

stopifnot(nrow(audit) == nrow(fixture) * 3)
stopifnot(all(c("raw_text", "coding_status", "standardized_code") %in% names(audit)))

validate_demographic_standardized_final(standardized_family, standardized_long)

family_path <- "data/processed/FINAL_REFERENCE__analysis_base_family.csv"
long_path <- "data/processed/FINAL_REFERENCE__analysis_base_long.csv"
if (file.exists(family_path) && file.exists(long_path)) {
  if (requireNamespace("readr", quietly = TRUE)) {
    final_family <- readr::read_csv(family_path, show_col_types = FALSE, progress = FALSE)
    final_long <- readr::read_csv(long_path, show_col_types = FALSE, progress = FALSE)
    validate_demographic_standardized_final(final_family, final_long)

    stopifnot(identical(
      final_family$es_calisma_durumu[final_family$aile_no == 42],
      1
    ))
    stopifnot(!is.na(final_family$es_isco08_4digit[final_family$aile_no == 42]))
    stopifnot(identical(
      final_family$kronik_hastalik_durumu[final_family$aile_no == 2007],
      1
    ))
    stopifnot(identical(
      final_family$anne_hastalik_endokrin[final_family$aile_no == 2007],
      1
    ))
    stopifnot(!"needs_manual_review" %in% final_family$es_meslek_kodlama_durumu)
    stopifnot(identical(
      final_family$es_meslek_kodlama_durumu[final_family$aile_no == 1015],
      "retired_not_working"
    ))
    stopifnot(identical(
      final_family$es_calisma_durumu[final_family$aile_no == 1015],
      0
    ))
    stopifnot(identical(
      final_family$es_emekli[final_family$aile_no == 1015],
      1
    ))
    stopifnot("hba1c" %in% names(final_family))
    stopifnot("hba1c" %in% names(final_long))
    stopifnot(sum(!is.na(final_family$hba1c)) == 39)
    stopifnot(sum(!is.na(final_long$hba1c)) == 39)
    stopifnot(sum(final_family$role != "DM_Hasta_Indeks" &
                    !is.na(final_family$hba1c)) == 0)
    stopifnot(sum(final_long$role != "DM_Hasta_Indeks" &
                    !is.na(final_long$hba1c)) == 0)
    stopifnot(all(
      final_family$hba1c[!is.na(final_family$hba1c)] >= 4.5 &
        final_family$hba1c[!is.na(final_family$hba1c)] <= 18
    ))
  }
}

cat("Demographic text standardization tests passed\n")
