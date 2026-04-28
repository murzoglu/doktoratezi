source("R/07_reproducibility.R")
source("R/01_io.R")

stopifnot(requireNamespace("digest", quietly = TRUE))

temp_csv <- tempfile(fileext = ".csv")
utils::write.csv(
  data.frame(aile_no = 1:2, group = c("Kontrol", "DM"), stringsAsFactors = FALSE),
  temp_csv,
  row.names = FALSE
)
temp_sha <- digest::digest(temp_csv, file = TRUE, algo = "sha256")
temp_lock <- tempfile(fileext = ".lock")
writeLines(
  c(
    "FINAL_REFERENCE CANONICAL ANALYSIS BASE LOCK",
    "============================================",
    "",
    "status=LOCKED_CANONICAL_ANALYSIS_BASE",
    "lock_date=2026-04-26",
    "project=doktoratezi-test",
    "",
    "Canonical CSV files:",
    sprintf("- `%s`: rows=2; columns=2; sha256=%s", normalize_reference_path(temp_csv), temp_sha)
  ),
  temp_lock
)

loaded <- validate_and_load(temp_csv, temp_lock, reader = "utils")
stopifnot(nrow(loaded) == 2L)
stopifnot(ncol(loaded) == 2L)
stopifnot(identical(attr(loaded, "validated_hash"), temp_sha))
stopifnot(identical(attr(loaded, "lock_date"), "2026-04-26"))

manifest <- final_reference_validation_manifest(temp_lock, temp_csv, reader = "utils")
stopifnot(nrow(manifest) == 1L)
stopifnot(isTRUE(manifest$ok))

bad_lock <- tempfile(fileext = ".lock")
writeLines(
  c(
    "status=LOCKED_CANONICAL_ANALYSIS_BASE",
    "lock_date=2026-04-26",
    "project=doktoratezi-test",
    "",
    "Canonical CSV files:",
    sprintf("- `%s`: rows=2; columns=2; sha256=%s", normalize_reference_path(temp_csv), paste(rep("0", 64), collapse = ""))
  ),
  bad_lock
)
stopifnot(inherits(
  try(validate_and_load(temp_csv, bad_lock, reader = "utils"), silent = TRUE),
  "try-error"
))

family_fixture <- data.frame(
  aile_no = c(1, 2),
  group = c("Kontrol", "DM"),
  katilimci_cocuk_cinsiyet = c(0, 1),
  kardes_cinsiyet = c(0, 0),
  egitim_durumu = c(2, 4),
  cocuk_yas = c(10, 13),
  kardes_yas = c(8, 15),
  katilimci_cocuk_sirasi = c(1, 2),
  kardes_sirasi = c(2, 1),
  dm_yili = c(NA_real_, 4),
  hba1c = c(NA_real_, 7.2)
)
prepared_family <- prepare_family(family_fixture)
stopifnot(all(c("aile_no_f", "group_f", "age_gap", "same_sex", "tani_yasi", "hba1c_target") %in% names(prepared_family)))
stopifnot(identical(as.character(prepared_family$group_f), c("Kontrol", "DM")))
stopifnot(identical(prepared_family$age_gap, c(2, 2)))
stopifnot(is.na(prepared_family$tani_yasi[1]))
stopifnot(identical(unname(prepared_family$tani_yasi[2]), 9))
stopifnot(identical(as.character(prepared_family$hba1c_target[2]), "Hedef_alti"))

long_fixture <- data.frame(
  aile_no = c(1, 1, 2),
  role = c("Kontrol_Indeks", "Kontrol_Kardes", "DM_Hasta_Indeks"),
  group = c("Kontrol", "Kontrol", "DM"),
  family_role = c("index", "sibling", "index"),
  katilimci_cocuk_cinsiyet = c(0, 1, 1),
  cocuk_yas = c(10, 12, 15)
)
prepared_long <- prepare_long(long_fixture)
stopifnot(all(c("aile_no_f", "role_f", "group_f", "family_role_f", "cinsiyet_f", "age_cat") %in% names(prepared_long)))
stopifnot(identical(as.character(prepared_long$age_cat), c("7-10", "11-13", "14-17")))
stopifnot(inherits(
  try(prepare_long(long_fixture[, setdiff(names(long_fixture), "role")]), silent = TRUE),
  "try-error"
))
