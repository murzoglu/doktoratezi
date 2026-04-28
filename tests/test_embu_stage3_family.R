source("R/04_embu_stage3_family.R")

default_dm_corrections <- stage3_default_dm_diagnosis_corrections()
stopifnot(identical(
  default_dm_corrections[default_dm_corrections$aile_no == 14, "dm_tani_tarihi"],
  "03.02.2012"
))

default_survey_corrections <- stage3_default_survey_date_corrections()
expected_survey_corrections <- c(
  `3` = "02.09.2023",
  `12` = "14.03.2023",
  `22` = "02.10.2023",
  `33` = "03.08.2023",
  `83` = "08.07.2025",
  `303` = "14.08.2024",
  `400` = "14.11.2024",
  `901` = "02.05.2025",
  `1001` = "15.06.2023",
  `1007` = "24.07.2025",
  `1101` = "06.09.2024",
  `1105` = "10.06.2025",
  `1110` = "11.07.2025",
  `1200` = "23.09.2025",
  `1218` = "25.12.2025",
  `1219` = "13.10.2025",
  `2027` = "07.08.2024",
  `2030` = "08.08.2025",
  `2034` = "10.08.2025",
  `2304` = "22.03.2023",
  `2306` = "03.09.2025"
)
for (family_id in names(expected_survey_corrections)) {
  stopifnot(identical(
    default_survey_corrections[
      default_survey_corrections$aile_no == as.numeric(family_id),
      "anket_tarihi"
    ],
    unname(expected_survey_corrections[family_id])
  ))
}
stopifnot(identical(
  default_survey_corrections[
    default_survey_corrections$aile_no == 1001,
    "anket_tarihi"
  ],
  "15.06.2023"
))
stopifnot(identical(
  default_survey_corrections[
    default_survey_corrections$aile_no == 33,
    "anket_tarihi"
  ],
  "03.08.2023"
))

default_child_birth_corrections <- stage3_default_child_birth_date_corrections()
expected_child_birth_corrections <- c(
  `607-4` = "09.07.2015",
  `1007-1` = "20.04.2018",
  `1200-3` = "17.09.2018",
  `1202-3` = "30.10.2008",
  `1219-4` = "13.09.2018",
  `1242-2` = "22.11.2008",
  `2027-2` = "07.10.2016",
  `2030-2` = "08.11.2009",
  `2034-2` = "06.10.2016",
  `2306-2` = "03.09.2012"
)
for (child_id in names(expected_child_birth_corrections)) {
  stopifnot(identical(
    default_child_birth_corrections[
      default_child_birth_corrections$cocuk_no == child_id,
      "katilimci_cocuk_dogum_tarihi"
    ],
    unname(expected_child_birth_corrections[child_id])
  ))
}
stopifnot(identical(
  default_child_birth_corrections[
    default_child_birth_corrections$cocuk_no == "607-4",
    "katilimci_cocuk_dogum_tarihi"
  ],
  "09.07.2015"
))
stopifnot(identical(
  default_child_birth_corrections[
    default_child_birth_corrections$cocuk_no == "1202-3",
    "katilimci_cocuk_dogum_tarihi"
  ],
  "30.10.2008"
))
stopifnot(identical(
  default_child_birth_corrections[
    default_child_birth_corrections$cocuk_no == "1242-2",
    "katilimci_cocuk_dogum_tarihi"
  ],
  "22.11.2008"
))

family_level_fixture <- data.frame(
  aile_no = c(1, 1),
  is_index = c(TRUE, FALSE),
  anket_tarihi = c("01.01.2024", "02.01.2024"),
  anne_dogum_tarihi = c("01.01.1984", "02.01.1984"),
  cocuk_sayisi = c("2", "#N/A"),
  ev_oda_sayisi = c("2", "#N/A"),
  hastalik_engel = c("astım", "?"),
  stringsAsFactors = FALSE
)
family_level_fixture <- normalize_stage3_literal_missing_values(family_level_fixture)
stopifnot(is.na(family_level_fixture$hastalik_engel[2]))
family_level_harmonized <- harmonize_stage3_family_level_fields(family_level_fixture)
stopifnot(identical(family_level_harmonized$anket_tarihi,
                    c("01.01.2024", "01.01.2024")))
stopifnot(identical(family_level_harmonized$anne_dogum_tarihi,
                    c("01.01.1984", "01.01.1984")))
stopifnot(identical(family_level_harmonized$cocuk_sayisi, c("2", "2")))
stopifnot(identical(family_level_harmonized$ev_oda_sayisi, c("2", "2")))
chronic_fixture <- data.frame(
  kronik_hastalik_durumu = c(0, 1, NA),
  esiniz_kronik_hastalik_durumu = c("1", "0", NA),
  stringsAsFactors = FALSE
)
chronic_standardized <- standardize_stage3_chronic_binary_codes(chronic_fixture)
stopifnot(identical(chronic_standardized$kronik_hastalik_durumu,
                    c(1L, 0L, NA_integer_)))
stopifnot(identical(chronic_standardized$esiniz_kronik_hastalik_durumu,
                    c(0L, 1L, NA_integer_)))

sibling_reference_fixture <- data.frame(
  aile_no = c(1, 1),
  katilimci_cocuk_dogum_tarihi = c("01.01.2010", "02.02.2012"),
  kardes_dogum_tarihi = c("wrong", "wrong"),
  katilimci_cocuk_cinsiyet = c(1, 0),
  kardes_cinsiyet = c(1, 1),
  stringsAsFactors = FALSE
)
sibling_reference_harmonized <- harmonize_stage3_sibling_reference_fields(
  sibling_reference_fixture
)
stopifnot(identical(
  sibling_reference_harmonized$kardes_dogum_tarihi,
  c("02.02.2012", "01.01.2010")
))
stopifnot(identical(sibling_reference_harmonized$kardes_cinsiyet, c(0, 1)))

final_reference_paths <- stage3_final_reference_paths()
stopifnot(all(grepl("FINAL_REFERENCE__", basename(final_reference_paths))))
stopifnot(identical(
  unname(final_reference_paths["long"]),
  "data/processed/FINAL_REFERENCE__analysis_base_long.csv"
))
stopifnot(identical(
  unname(final_reference_paths["family"]),
  "data/processed/FINAL_REFERENCE__analysis_base_family.csv"
))

make_stage2_fixture <- function() {
  embu_p <- as.data.frame(matrix(1:174, nrow = 6, ncol = 29))
  names(embu_p) <- paste0("embu_p_q", sprintf("%02d", 1:29))

  embu_c <- as.data.frame(matrix(201:374, nrow = 6, ncol = 29))
  names(embu_c) <- paste0("embu_c_q", sprintf("%02d", 1:29))

  beck <- data.frame(
    beck_1 = c(1, 1, 2, 2, 5, 1),
    beck_2 = c(2, 2, 3, 3, 15, 2),
    check.names = FALSE
  )
  names(beck) <- c("beck_1", "beck_2")

  kia <- data.frame(
    kia_1 = c(3, 6, 4, 5, 2, 1),
    kia_2 = c(1, 2, 6, 3, 4, 5),
    check.names = FALSE
  )

  data.frame(
    source_row_number = 1:6,
    sira_no = 101:106,
    aile_no = c(10, 10, 20, 20, 30, 30),
    katilimci_cocuk = c(1, 2, 3, 4, 1, 2),
    anket_tarihi = c("01.01.2024", "01.01.2024", "01.01.2024",
                     "01.01.2024", "01.01.2004", "01.01.2004"),
    anne_dogum_tarihi = c("01.01.1984", "01.01.1984", "01.01.1981",
                          "01.01.1981", "01.01.1980", "01.01.1980"),
    anne_antidepresan = c(0, 0, 1, 1, 0, 0),
    egitim_durumu = c(3, 3, 4, 4, 2, 2),
    calisma_durumu = c(1, 1, 2, 2, 1, 1),
    cocuk_no = c("10-1", "10-2", "20-3", "20-4", "30-1", "30-2"),
    katilimci_cocuk_dogum_tarihi = c(
      "01.01.2014", "01.01.2012", "01.01.2013",
      "01.01.2011", "01.01.1990", "01.01.2009"
    ),
    katilimci_cocuk_sirasi = c(1, 2, 1, 2, 1, 2),
    kardes_dogum_tarihi = c(
      "01.01.2012", "01.01.2014", "01.01.2011",
      "01.01.2013", "01.01.2009", "01.01.1990"
    ),
    katilimci_cocuk_cinsiyet = c(1, 2, 1, 2, 1, 2),
    dm_tani_tarihi = c("01.01.2020", NA, NA, NA, NA, NA),
    embu_p_likert_version = rep("4pt", 6),
    embu_c_likert_version = rep("4pt", 6),
    embu_p_likert_version_original = rep("6pt", 6),
    embu_c_likert_version_original = c("4pt", "4pt", "6pt", "6pt", "4pt", "4pt"),
    embu_p_conversion_method = rep("pooled_embu_c_equip_percentile_rounded", 6),
    embu_c_conversion_method = c(
      "none_original_4pt", "none_original_4pt",
      "item_embu_c_equip_percentile_rounded",
      "item_embu_c_equip_percentile_rounded",
      "none_original_4pt", "none_original_4pt"
    ),
    embu_p_outlier_n = c(0, 0, 1, 1, 0, 0),
    embu_c_outlier_n = c(0, 1, 0, 1, 0, 0),
    embu_outlier_n = c(0, 1, 1, 2, 0, 0),
    embu_c_family_mixed_likert = c(FALSE, FALSE, TRUE, TRUE, FALSE, FALSE),
    embu_likert_standardized = rep("4pt", 6),
    beck,
    embu_p,
    embu_c,
    kia,
    check.names = FALSE
  )
}

result <- prepare_embu_stage3_family(
  make_stage2_fixture(),
  index_authority_family_ids = c(10),
  dm_diagnosis_corrections = data.frame(
    aile_no = 30,
    dm_tani_tarihi = "03.02.2014",
    correction_source = "raw_data_lookup",
    stringsAsFactors = FALSE
  ),
  survey_date_corrections = data.frame(
    aile_no = 30,
    anket_tarihi = "01.01.2024",
    correction_source = "raw_data_lookup",
    stringsAsFactors = FALSE
  ),
  child_birth_date_corrections = data.frame(
    cocuk_no = "30-1",
    katilimci_cocuk_dogum_tarihi = "01.01.2010",
    correction_source = "raw_data_lookup",
    stringsAsFactors = FALSE
  )
)
long <- result$long
family <- result$family
index_authority <- result$index_authority
integrity <- result$integrity
outliers <- result$outliers
dm_missing <- result$dm_missing_diagnosis
dm_corrections <- result$dm_diagnosis_corrections
survey_corrections <- result$survey_date_corrections
child_birth_corrections <- result$child_birth_date_corrections

p_cols <- paste0("embu_p_q", sprintf("%02d", 1:29))
beck_cols <- c("beck_1", "beck_2")
srq_cols <- c("srq_1", "srq_2")

stopifnot(identical(long$is_index, c(TRUE, FALSE, TRUE, FALSE, TRUE, FALSE)))
stopifnot(identical(long$family_role,
                    c("index", "sibling", "index", "sibling", "index", "sibling")))
stopifnot(identical(long$role,
                    c("DM_Hasta_Indeks", "DM_Hasta_Kardes",
                      "Kontrol_Indeks", "Kontrol_Kardes",
                      "DM_Hasta_Indeks", "DM_Hasta_Kardes")))
stopifnot(identical(long$group, c("DM", "DM", "Kontrol", "Kontrol", "DM", "DM")))
stopifnot(all(is.na(unlist(long[!long$is_index, p_cols]))))
stopifnot(all(is.na(unlist(long[!long$is_index, beck_cols]))))
stopifnot(!any(is.na(unlist(long[long$is_index, p_cols]))))
stopifnot(is.na(long$beck_1[5]))
stopifnot(is.na(long$beck_2[5]))
stopifnot(!"kia_1" %in% names(long))
stopifnot(all(srq_cols %in% names(long)))
stopifnot(is.na(long$srq_1[2]))
stopifnot(is.na(long$srq_2[3]))
stopifnot(all(unlist(long[srq_cols]) %in% c(1:5, NA)))
stopifnot(abs(long$cocuk_yas[1] - 10) < 0.01)
stopifnot(abs(long$anne_yas[1] - 40) < 0.01)
stopifnot(abs(long$dm_yili[1] - 4) < 0.01)
stopifnot(is.na(long$dm_yili[2]))
stopifnot(identical(long$family_dm_inconsistent,
                    c(FALSE, FALSE, FALSE, FALSE, FALSE, FALSE)))
stopifnot(identical(long$dm_tani_tarihi[5], "03.02.2014"))
stopifnot(identical(long$anket_tarihi[5:6], c("01.01.2024", "01.01.2024")))
stopifnot(identical(long$katilimci_cocuk_dogum_tarihi[5], "01.01.2010"))
stopifnot(identical(long$kardes_dogum_tarihi[6], "01.01.2010"))
stopifnot(abs(long$dm_yili[5] - 9.91) < 0.01)
stopifnot(abs(long$cocuk_yas[5] - 14) < 0.01)

stopifnot(nrow(family) == 3)
stopifnot(identical(family$aile_no, c(10, 20, 30)))
stopifnot(identical(family$group, c("DM", "Kontrol", "DM")))
stopifnot(identical(family$role, c("DM_Hasta_Indeks", "Kontrol_Indeks",
                                   "DM_Hasta_Indeks")))
stopifnot(identical(family$embu_p_q01, c(1L, 3L, 5L)))
stopifnot(identical(family$beck_1, c(1, 2, NA)))
stopifnot(identical(family$embu_c_idx_q01, c(201L, 203L, 205L)))
stopifnot(identical(family$embu_c_sib_q01, c(202L, 204L, 206L)))
stopifnot(identical(family$srq_1, c(3, 4, 2)))
stopifnot(identical(family$srq_sib_1, c(NA, 5, 1)))
stopifnot(!"kia_1" %in% names(family))
stopifnot(!"embu_c_q01" %in% names(family))
expected_family_data_cols <- c(
  "source_row_number",
  "sira_no",
  "cocuk_no",
  "katilimci_cocuk",
  "is_index",
  "anket_tarihi",
  "katilimci_cocuk_dogum_tarihi",
  "katilimci_cocuk_sirasi",
  "katilimci_cocuk_cinsiyet",
  "anne_dogum_tarihi",
  "anne_antidepresan",
  "egitim_durumu",
  "calisma_durumu",
  "beck_1",
  "beck_2",
  "beck_total",
  "srq_1",
  "srq_2",
  "embu_p_likert_version",
  "embu_p_likert_version_original",
  "embu_p_conversion_method",
  "embu_p_outlier_n",
  "embu_c_idx_likert_version",
  "embu_c_idx_likert_version_original",
  "embu_c_idx_conversion_method",
  "embu_c_idx_outlier_n",
  "embu_c_idx_family_mixed_likert",
  "embu_outlier_n",
  "embu_likert_standardized",
  "kardes_source_row_number",
  "kardes_sira_no",
  "kardes_cocuk_no",
  "kardes_katilimci_cocuk",
  "kardes_is_index",
  "kardes_family_role",
  "kardes_role",
  "kardes_anket_tarihi",
  "kardes_dogum_tarihi",
  "kardes_sirasi",
  "kardes_cinsiyet",
  "kardes_yas",
  "srq_sib_1",
  "srq_sib_2",
  "embu_c_sib_likert_version",
  "embu_c_sib_likert_version_original",
  "embu_c_sib_conversion_method",
  "embu_c_sib_outlier_n",
  "embu_c_sib_family_mixed_likert",
  "kardes_embu_outlier_n",
  "kardes_embu_likert_standardized"
)
stopifnot(all(expected_family_data_cols %in% names(family)))
stopifnot(identical(family$source_row_number, c(1L, 3L, 5L)))
stopifnot(identical(family$kardes_source_row_number, c(2L, 4L, 6L)))
stopifnot(identical(family$kardes_cocuk_no, c("10-2", "20-4", "30-2")))
stopifnot(identical(family$kardes_anket_tarihi,
                    c("01.01.2024", "01.01.2024", "01.01.2024")))
stopifnot(identical(family$embu_c_idx_likert_version_original,
                    c("4pt", "6pt", "4pt")))
stopifnot(identical(family$embu_c_sib_likert_version_original,
                    c("4pt", "6pt", "4pt")))
stopifnot(identical(family$embu_c_sib_conversion_method,
                    c("none_original_4pt",
                      "item_embu_c_equip_percentile_rounded",
                      "none_original_4pt")))

final_long <- build_stage3_final_reference_long(long)
final_family <- build_stage3_final_reference_family(family)
c_cols <- paste0("embu_c_q", sprintf("%02d", 1:29))
final_long_expected_cols <- setdiff(
  names(long),
  stage3_final_reference_excluded_columns(long)
)
final_family_expected_cols <- setdiff(
  names(family),
  stage3_final_reference_excluded_columns(family)
)
final_beck_cols <- beck_cols
final_srq_cols <- srq_cols
final_srq_sib_cols <- sub("^srq_", "srq_sib_", srq_cols)
forbidden_final_reference_pattern <- paste(
  c(
    "source_row_number",
    "^sira_no$",
    "likert",
    "conversion",
    "outlier",
    "family_mixed_likert",
    "family_dm_inconsistent",
    "beck_total",
    "^kia_",
    "^srq(_sib)?_(total|sum|score|mean|category)"
  ),
  collapse = "|"
)

stopifnot(identical(names(final_long), final_long_expected_cols))
stopifnot(identical(names(final_family), final_family_expected_cols))
stopifnot(identical(grep("^beck_", names(final_long), value = TRUE),
                    final_beck_cols))
stopifnot(identical(grep("^beck_", names(final_family), value = TRUE),
                    final_beck_cols))
stopifnot(identical(grep("^srq_\\d+$", names(final_long), value = TRUE),
                    final_srq_cols))
stopifnot(identical(grep("^srq_\\d+$", names(final_family), value = TRUE),
                    final_srq_cols))
stopifnot(identical(grep("^srq_sib_", names(final_family), value = TRUE),
                    final_srq_sib_cols))
stopifnot(!any(grepl(forbidden_final_reference_pattern, names(final_long))))
stopifnot(!any(grepl(forbidden_final_reference_pattern, names(final_family))))
stopifnot(!any(unlist(final_long, use.names = FALSE) == "#N/A", na.rm = TRUE))
stopifnot(!any(unlist(final_family, use.names = FALSE) == "#N/A", na.rm = TRUE))
stopifnot(all(c(
  "beck_1",
  "srq_1",
  "anket_tarihi",
  "cocuk_yas",
  "anne_yas",
  "dm_yili"
) %in% names(final_long)))
stopifnot(all(c(
  "beck_1",
  "srq_1",
  "srq_sib_1",
  "anket_tarihi",
  "kardes_anket_tarihi",
  "cocuk_yas",
  "kardes_yas",
  "anne_yas",
  "dm_yili"
) %in% names(final_family)))
stopifnot(!"beck_total" %in% names(final_long))
stopifnot(!"beck_total" %in% names(final_family))
stopifnot(identical(
  final_long[setdiff(names(final_long), "embu_c_q25")],
  long[setdiff(names(final_long), "embu_c_q25")]
))
stopifnot(identical(
  final_family[
    setdiff(names(final_family), c("embu_c_idx_q25", "embu_c_sib_q25"))
  ],
  family[
    setdiff(names(final_family), c("embu_c_idx_q25", "embu_c_sib_q25"))
  ]
))
stopifnot(all(is.na(unlist(final_long[!final_long$is_index, p_cols]))))
stopifnot(!any(is.na(unlist(final_long[final_long$is_index, p_cols]))))
stopifnot(identical(final_family$kardes_role,
                    c("DM_Hasta_Kardes", "Kontrol_Kardes",
                      "DM_Hasta_Kardes")))

q25_long_fixture <- long
q25_long_fixture$embu_c_q25 <- c(1, 2, 3, 4, NA, 1)
q25_long_scored <- build_stage3_final_reference_long(q25_long_fixture)
stopifnot(identical(q25_long_scored$embu_c_q25,
                    c(4, 3, 2, 1, NA, 4)))

q25_family_fixture <- family
q25_family_fixture$embu_c_idx_q25 <- c(1, 2, 3)
q25_family_fixture$embu_c_sib_q25 <- c(4, NA, 1)
q25_family_scored <- build_stage3_final_reference_family(q25_family_fixture)
stopifnot(identical(q25_family_scored$embu_c_idx_q25, c(4, 3, 2)))
stopifnot(identical(q25_family_scored$embu_c_sib_q25, c(1, NA, 4)))

summary <- result$summary
stopifnot(summary$value[summary$metric == "long_rows"] == 6)
stopifnot(summary$value[summary$metric == "family_rows"] == 3)
stopifnot(summary$value[summary$metric == "sibling_rows_parent_report_na"] == 3)
stopifnot(summary$value[summary$metric == "index_authority_families"] == 1)
stopifnot(summary$value[summary$metric == "index_authority_differing_parent_report_cells"] > 0)
stopifnot(summary$value[summary$metric == "srq_outlier_cells_set_na"] == 2)
stopifnot(summary$value[summary$metric == "beck_outlier_cells_set_na"] == 2)
stopifnot(summary$value[summary$metric == "survey_date_corrected_families"] == 1)
stopifnot(summary$value[summary$metric == "child_birth_date_corrected_children"] == 1)
stopifnot(summary$value[summary$metric == "dm_diagnosis_corrected_families"] == 1)
stopifnot(summary$value[summary$metric == "dm_missing_diagnosis_families"] == 0)

stopifnot(nrow(index_authority) == 1)
stopifnot(identical(index_authority$aile_no, 10))
stopifnot(index_authority$differing_parent_report_cells > 0)
stopifnot(identical(index_authority$applied_rule,
                    "index_parent_report_retained_sibling_parent_report_set_na"))

stopifnot(all(c("role", "n", "embu_p_dolu", "embu_c_dolu", "bdi_dolu",
                "srq_dolu") %in% names(integrity)))
stopifnot(integrity$n[integrity$role == "DM_Hasta_Indeks"] == 2)
stopifnot(integrity$embu_p_dolu[integrity$role == "DM_Hasta_Kardes"] == 0)
stopifnot(integrity$bdi_dolu[integrity$role == "Kontrol_Kardes"] == 0)
stopifnot(integrity$srq_dolu[integrity$role == "Kontrol_Indeks"] == 1)

stopifnot(nrow(outliers) == 4)
stopifnot(sum(outliers$instrument == "BDI") == 2)
stopifnot(sum(outliers$instrument == "SRQ") == 2)

stopifnot(nrow(dm_missing) == 0)

stopifnot(nrow(dm_corrections) == 1)
stopifnot(identical(dm_corrections$aile_no, 30))
stopifnot(identical(dm_corrections$old_dm_tani_tarihi, NA_character_))
stopifnot(identical(dm_corrections$new_dm_tani_tarihi, "03.02.2014"))

stopifnot(nrow(survey_corrections) == 1)
stopifnot(identical(survey_corrections$aile_no, 30))
stopifnot(identical(survey_corrections$old_anket_tarihi, "01.01.2004"))
stopifnot(identical(survey_corrections$new_anket_tarihi, "01.01.2024"))
stopifnot(identical(survey_corrections$rows_corrected, 2L))

stopifnot(nrow(child_birth_corrections) == 1)
stopifnot(identical(child_birth_corrections$cocuk_no, "30-1"))
stopifnot(identical(child_birth_corrections$old_katilimci_cocuk_dogum_tarihi,
                    "01.01.1990"))
stopifnot(identical(child_birth_corrections$new_katilimci_cocuk_dogum_tarihi,
                    "01.01.2010"))
stopifnot(identical(child_birth_corrections$paired_kardes_rows_corrected, 1L))

cat("EMBU stage 3 family tests passed\n")
