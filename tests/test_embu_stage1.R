source("R/02_embu_stage1.R")

make_test_raw <- function() {
  p_order <- c(28, 20, 8, 12, 15, 17, 21, 4, 1, 9, 23, 13, 16, 26, 22,
               10, 25, 14, 24, 5, 19, 3, 11, 2, 18, 27, 29, 6, 7)
  c_order <- c(1, 13, 6, 17, 20, 3, 24, 26, 8, 12, 5, 28, 16, 22, 10,
               21, 18, 2, 29, 27, 11, 14, 4, 25, 15, 19, 9, 23, 7)

  core <- data.frame(
    "Sıra No" = 1:2,
    "Aile No" = c(10, 10),
    "Çocuk No" = c(101, 102),
    "Çocuk Adı Soyadı" = c("A B", "C D"),
    "Anket Tarihi" = c("01.01.2023", "02.01.2024"),
    "Katılımcı Çocuk" = c(1, 2),
    check.names = FALSE
  )

  p_values <- matrix(2, nrow = 2, ncol = 29)
  p_values[1, match(14, p_order)] <- 14
  p <- as.data.frame(p_values, check.names = FALSE)
  names(p) <- sprintf("EMBU-P Soru %d. test", p_order)

  c_values <- matrix(3, nrow = 2, ncol = 29)
  c_values[1, match(7, c_order)] <- 1
  c_values[1, match(8, c_order)] <- 2
  c_values[1, match(9, c_order)] <- 3
  c_values[1, match(10, c_order)] <- 4
  c_values[2, match(7, c_order)] <- 6
  c_values[2, match(3, c_order)] <- 21
  c <- as.data.frame(c_values, check.names = FALSE)
  names(c) <- sprintf("(EMBU-C) %d - test", c_order)

  cbind(core, p, c)
}

result <- standardize_embu_stage1(make_test_raw())
clean <- result$data

stopifnot(nrow(clean) == 2)
stopifnot(!"cocuk_adi_soyadi" %in% names(clean))
stopifnot(all(paste0("embu_p_q", sprintf("%02d", 1:29)) %in% names(clean)))
stopifnot(all(paste0("embu_c_q", sprintf("%02d", 1:29)) %in% names(clean)))

embu_p_pos <- match(paste0("embu_p_q", sprintf("%02d", 1:29)), names(clean))
embu_c_pos <- match(paste0("embu_c_q", sprintf("%02d", 1:29)), names(clean))
stopifnot(identical(embu_p_pos, seq(min(embu_p_pos), max(embu_p_pos))))
stopifnot(identical(embu_c_pos, seq(min(embu_c_pos), max(embu_c_pos))))

stopifnot(is.na(clean$embu_p_q14[1]))
stopifnot(clean$embu_p_outlier_n[1] == 1)
stopifnot(is.na(clean$embu_c_q03[2]))
stopifnot(identical(
  as.integer(clean[1, paste0("embu_c_q", sprintf("%02d", 7:10))]),
  c(2L, 3L, 4L, 1L)
))
stopifnot(clean$embu_c_q10[2] == 6)
stopifnot(clean$embu_c_outlier_n[2] == 1)

stopifnot(identical(clean$embu_p_likert_version, c("6pt", "6pt")))
stopifnot(identical(clean$embu_c_likert_version, c("4pt", "6pt")))
stopifnot(identical(clean$embu_c_family_mixed_likert, c(TRUE, TRUE)))

stopifnot(nrow(result$outliers) == 2)
stopifnot(all(c("source_row_number", "form", "item", "raw_value", "clean_action") %in%
                names(result$outliers)))

cat("EMBU stage 1 tests passed\n")
