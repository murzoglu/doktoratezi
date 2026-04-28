#!/usr/bin/env Rscript
# =============================================================================
# 00_preprocessing.R
# Veri on isleme: kontroller, duzeltmeler, temizleme, CSV kaydetme
# =============================================================================

.libPaths(c("~/R/libs", .libPaths()))
Sys.setlocale("LC_ALL", "en_US.UTF-8")

# Turkce -> ASCII donusturucu (tum script boyunca kullanilir)
tr_to_ascii <- function(s) {
  chartr("\u0131\u0130\u00e7\u00c7\u011f\u011e\u00f6\u00d6\u015f\u015e\u00fc\u00dc",
         "iIcCgGoOsSuU", s)
}

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(stringr)
  library(lubridate)
})

# --- 1. Veri Yukleme ---
cat("=== 1. VERI YUKLEME ===\n")
raw_files <- list.files("data/raw", pattern = "\\.csv$", full.names = TRUE)
raw_path <- raw_files[grepl("HA", raw_files)][1]
safe_path <- "data/raw/_temp_raw.csv"
file.copy(raw_path, safe_path, overwrite = TRUE)
cat(sprintf("Dosya: %s\n", raw_path))

# CRLF -> LF donusumu (Windows formatli CSV)
lines <- readLines(safe_path, encoding = "UTF-8", warn = FALSE)
writeLines(lines, safe_path, useBytes = FALSE)
df <- read.csv(safe_path, check.names = FALSE, stringsAsFactors = FALSE,
               na.strings = c("", "NA"))
file.remove(safe_path)
cat(sprintf("Yuklenen: %d satir, %d sutun\n", nrow(df), ncol(df)))

# Sutun adlarini goster
col_names <- names(df)
cat(sprintf("Sutun adlari basariyla okundu: %d sutun\n", length(col_names)))

# --- 2. PII Sutunlarini Kaldir ---
cat("\n=== 2. KISISEL VERI TEMIZLIGI ===\n")

# Sutun 3 = "Cocuk Adi Soyadi" (indeks 4, 1-based)
pii_idx <- which(grepl("Ad.*Soyad", col_names))
if (length(pii_idx) > 0) {
  cat(sprintf("Kaldirilan sutunlar: %s (indeks: %s)\n",
              paste(col_names[pii_idx], collapse = ", "),
              paste(pii_idx, collapse = ", ")))
  df <- df[, -pii_idx, drop = FALSE]
  col_names <- names(df)
} else {
  cat("PII sutunu bulunamadi!\n")
}

# --- 3. Temel Veri Kontrolleri ---
cat("\n=== 3. TEMEL VERI KONTROLLERI ===\n")

# Sutun referanslari (isim icinde arama)
# Sutun adlarini ASCII'ye cevir (eslesme icin)
col_names_ascii <- tr_to_ascii(col_names)

find_col <- function(pattern) {
  idx <- grep(pattern, col_names_ascii, perl = TRUE)
  if (length(idx) == 0) return(NULL)
  return(col_names[idx])
}

col_katilimci <- find_col("Kat.*Cocuk$")[1]
col_aile <- find_col("Aile.No")[1]
col_sira_no <- find_col("Sira.No")[1]
col_cocuk_no <- find_col("Cocuk.No")[1]
col_dogum <- find_col("Kat.*Cocuk.*Dogum")[1]
col_cinsiyet <- find_col("Kat.*Cocuk.*Cinsiyet")[1]
col_cocuk_sirasi <- find_col("Kat.*Cocuk.*Siras")[1]

cat(sprintf("  Katilimci sutunu: %s\n", col_katilimci))
cat(sprintf("  Aile No sutunu: %s\n", col_aile))

# 3a. Katilimci Cocuk dagilimi
cat("\n--- 3a. Katilimci Cocuk Dagilimi ---\n")
print(table(df[[col_katilimci]], useNA = "always"))

# 3b. Eksik veri kontrolu
cat("\n--- 3b. Eksik Veri Oranlari (>%5 olan sutunlar) ---\n")
na_pcts <- sapply(df, function(x) mean(is.na(x)) * 100)
high_na <- sort(na_pcts[na_pcts > 5], decreasing = TRUE)
if (length(high_na) > 0) {
  for (cn in names(high_na)) {
    cat(sprintf("  %s: %%%.1f eksik\n", substr(cn, 1, 60), high_na[cn]))
  }
} else {
  cat("  Yok\n")
}

# 3c. Aile ciftleri kontrolu
cat("\n--- 3c. Aile Ciftleri Kontrolu ---\n")
dm_fam <- df[df[[col_katilimci]] %in% c(1, 2), ]
dm_summary <- tapply(dm_fam[[col_katilimci]], dm_fam[[col_aile]],
                     function(x) paste(sort(unique(x)), collapse = ","))
ctrl_fam <- df[df[[col_katilimci]] %in% c(3, 4), ]
ctrl_summary <- tapply(ctrl_fam[[col_katilimci]], ctrl_fam[[col_aile]],
                       function(x) paste(sort(unique(x)), collapse = ","))
cat(sprintf("  DM aileleri: %d (tumu cift: %s)\n",
            length(dm_summary), ifelse(all(dm_summary == "1,2"), "EVET", "HAYIR")))
cat(sprintf("  Kontrol aileleri: %d (tumu cift: %s)\n",
            length(ctrl_summary), ifelse(all(ctrl_summary == "3,4"), "EVET", "HAYIR")))

# 3d. Deger araligi kontrolleri
cat("\n--- 3d. Deger Araligi Kontrolleri ---\n")

beck_cols <- col_names[grep("^Beck ", col_names_ascii)]
embu_p_cols <- col_names[grep("^EMBU-P", col_names_ascii)]
embu_c_cols <- col_names[grep("^\\(EMBU-C\\)", col_names_ascii)]
kia_cols <- col_names[grep("^KIA ", col_names_ascii)]

cat(sprintf("  Beck sutun sayisi: %d\n", length(beck_cols)))
cat(sprintf("  EMBU-P sutun sayisi: %d\n", length(embu_p_cols)))
cat(sprintf("  EMBU-C sutun sayisi: %d\n", length(embu_c_cols)))
cat(sprintf("  KIA sutun sayisi: %d\n", length(kia_cols)))

check_range <- function(data_cols, label, expected_min, expected_max) {
  vals <- unlist(df[, data_cols, drop = FALSE])
  vals <- suppressWarnings(as.numeric(vals))
  vals <- vals[!is.na(vals)]
  actual_range <- range(vals)
  out_of_range <- sum(vals < expected_min | vals > expected_max)
  cat(sprintf("  %s (beklenen %d-%d): gercek aralik = %d-%d, aralik disi = %d\n",
              label, expected_min, expected_max,
              actual_range[1], actual_range[2], out_of_range))
}

check_range(beck_cols, "Beck", 0, 3)
check_range(embu_p_cols, "EMBU-P", 1, 6)
check_range(embu_c_cols, "EMBU-C", 1, 6)  # protokolde 1-4 ama veride 1-6 olabilir
check_range(kia_cols, "KIA", 1, 5)

# 3e. Cinsiyet kodlamasi
cat("\n--- 3e. Cinsiyet Kodlamasi ---\n")
cat("  0=Kiz, 1=Erkek\n")
print(table(df[[col_cinsiyet]], useNA = "always"))

# 3f. Tarih kontrolleri
cat("\n--- 3f. Tarih Kontrolleri ---\n")
date_col_names <- c(find_col("Anket.Tarihi")[1],
                    find_col("Anne.Dogum")[1],
                    find_col("Kat.*Dogum.Tarihi")[1],
                    find_col("DM.Tani.Tarihi")[1],
                    find_col("Kardes.Dogum")[1],
                    find_col("Es.Dogum.Tarihi")[1])
date_col_names <- date_col_names[!is.na(date_col_names)]

for (dc in date_col_names) {
  vals <- df[[dc]]
  vals <- vals[!is.na(vals)]
  parsed <- suppressWarnings(dmy(vals))
  n_fail <- sum(is.na(parsed))
  cat(sprintf("  %s: %d/%d parse edilemedi\n", substr(dc, 1, 40), n_fail, length(vals)))
}

# 3g. Duplike kontrolu
cat("\n--- 3g. Duplike Kontrolu ---\n")
dup_sira <- sum(duplicated(df[[col_sira_no]]))
dup_cocuk <- sum(duplicated(df[[col_cocuk_no]]))
cat(sprintf("  Sira No duplike: %d\n", dup_sira))
cat(sprintf("  Cocuk No duplike: %d\n", dup_cocuk))

# --- 4. Anne Verisi Duzeltme ---
cat("\n=== 4. ANNE VERISI DUZELTME ===\n")

# Anne sutunlari: demografik (indeks 6-30 orijinal -> PII kaldirildiktan sonra 5-29)
# + Beck + EMBU-P
anne_demo_cols <- col_names[grepl("(Anne|Antidepresan|Cocuk.Say|Medeni|Es.Sa|Es.Dog|Egitim|Calisma|Calistig|Ev.Sahip|Ev.Oda|Araba|Kronik|Hastalik.*Engel|Esiniz.*Kronik|Es.Hastalik)", col_names_ascii)]
anne_all_cols <- unique(c(anne_demo_cols, beck_cols, embu_p_cols))

cat(sprintf("Anne sutun sayisi: %d\n", length(anne_all_cols)))

fix_count <- 0
for (aile in unique(df[[col_aile]])) {
  aile_rows <- which(df[[col_aile]] == aile)
  if (length(aile_rows) != 2) next

  types <- df[[col_katilimci]][aile_rows]
  if (all(sort(types) == c(1, 2))) {
    ref_idx <- aile_rows[types == 1]
    other_idx <- aile_rows[types == 2]
  } else if (all(sort(types) == c(3, 4))) {
    ref_idx <- aile_rows[types == 3]
    other_idx <- aile_rows[types == 4]
  } else {
    next
  }

  for (col in anne_all_cols) {
    ref_val <- df[[col]][ref_idx]
    other_val <- df[[col]][other_idx]

    ref_na <- is.na(ref_val)
    other_na <- is.na(other_val)

    if (!ref_na && (other_na || (!other_na && as.character(ref_val) != as.character(other_val)))) {
      df[[col]][other_idx] <- ref_val
      fix_count <- fix_count + 1
    }
  }
}
cat(sprintf("Duzeltilen hucre sayisi: %d\n", fix_count))

# --- 5. Kontrol Grubu Swap ---
cat("\n=== 5. KONTROL GRUBU SWAP ===\n")
swap_families <- c(42, 44, 46, 48, 50, 51, 52, 56)

# Cocuga ozgu sutunlar + EMBU-C + KIA
# NOT: Katilimci Cocuk (3/4 kodu) swap edilMEZ - amac kodu sabit tutup veriyi degistirmek
child_specific_cols <- c(col_dogum, col_cocuk_sirasi, col_cinsiyet,
                         find_col("DM.Tani")[1],
                         find_col("Kardes.Dogum.Tarihi")[1],
                         find_col("Kardes.Cinsiyet")[1],
                         embu_c_cols, kia_cols)
child_specific_cols <- child_specific_cols[!is.na(child_specific_cols)]

swap_count <- 0
for (aile in swap_families) {
  aile_rows <- which(df[[col_aile]] == aile)
  if (length(aile_rows) != 2) {
    cat(sprintf("  UYARI: Aile %d'de 2 satir bulunamadi!\n", aile))
    next
  }

  types <- df[[col_katilimci]][aile_rows]
  if (!all(sort(types) == c(3, 4))) {
    cat(sprintf("  UYARI: Aile %d kontrol ailesi degil!\n", aile))
    next
  }

  idx3 <- aile_rows[types == 3]
  idx4 <- aile_rows[types == 4]

  for (col in child_specific_cols) {
    temp <- df[[col]][idx3]
    df[[col]][idx3] <- df[[col]][idx4]
    df[[col]][idx4] <- temp
  }
  swap_count <- swap_count + 1
  cat(sprintf("  Aile %d: swap yapildi\n", aile))
}
cat(sprintf("Toplam swap: %d aile\n", swap_count))

# --- 6. Swap Sonrasi Dogrulama ---
cat("\n=== 6. SWAP SONRASI DOGRULAMA ===\n")
labels <- c("DM cocuk", "DM kardes", "Kontrol cocuk", "Kontrol kardes")
for (grp in 1:4) {
  grp_data <- df[df[[col_katilimci]] == grp, ]
  ages <- suppressWarnings(
    as.numeric(difftime(dmy("01-01-2024"), dmy(grp_data[[col_dogum]]), units = "days")) / 365.25
  )
  genders <- suppressWarnings(as.numeric(grp_data[[col_cinsiyet]]))
  cat(sprintf("  Grup %d (%s): n=%d, yas_ort=%.1f, erkek%%=%.1f\n",
              grp, labels[grp], nrow(grp_data),
              mean(ages, na.rm = TRUE),
              mean(genders, na.rm = TRUE) * 100))
}

# --- 7. Sutun Adlarini Sadelestir ---
cat("\n=== 7. SUTUN ADLARI SADELESTIRME ===\n")

new_names <- names(df)

# EMBU-P: soru numarasini cikar
for (i in seq_along(new_names)) {
  n <- new_names[i]
  if (grepl("^EMBU-P", n)) {
    soru_no <- str_extract(n, "\\d+")
    new_names[i] <- paste0("EMBU_P_", soru_no)
  } else if (grepl("^\\(EMBU-C\\)", n)) {
    soru_no <- str_extract(n, "(?<=\\) )\\d+")
    new_names[i] <- paste0("EMBU_C_", soru_no)
  } else if (grepl("^KIA", n)) {
    soru_no <- str_extract(n, "\\d+")
    new_names[i] <- paste0("KIA_", soru_no)
  } else if (grepl("^Beck", n)) {
    soru_no <- str_extract(n, "\\d+")
    new_names[i] <- paste0("Beck_", soru_no)
  }
}

# Genel temizlik
new_names <- gsub("\\s+", "_", new_names)
new_names <- gsub("[?]", "", new_names)
new_names <- gsub("[&]", "_", new_names)
new_names <- gsub("__+", "_", new_names)
new_names <- gsub("_$", "", new_names)

new_names <- tr_to_ascii(new_names)

names(df) <- new_names

cat(sprintf("Sutun sayisi: %d\n", ncol(df)))
cat("Tum sutun adlari:\n")
for (i in seq_along(new_names)) {
  cat(sprintf("  %3d: %s\n", i, new_names[i]))
}

# --- 8. Son Kontroller ---
cat("\n=== 8. SON KONTROLLER ===\n")

# Anne verisi tutarlilik (duzeltme sonrasi)
col_aile_new <- names(df)[grep("Aile", names(df))[1]]
col_kt_new <- names(df)[grep("Kat", names(df))[1]]

# Son kontrol icin anne sutunlarini bul (artik ASCII adlar var)
anne_pattern <- "^(Anne|Beck_|EMBU_P_|Cocuk_Say|Medeni|Es_|Egitim|Calisma|Calistigi|Ev_|Araba|Kronik|Hastalik|Antidepresan)"
anne_check_cols <- names(df)[grepl(anne_pattern, names(df))]
if (length(anne_check_cols) < 10) {
  cat("  (Genis arama yapiliyor...)\n")
  anne_check_cols <- names(df)[5:min(ncol(df), 80)]
}

inconsistent <- 0
inconsistent_details <- list()
for (aile in unique(df[[col_aile_new]])) {
  aile_rows <- which(df[[col_aile_new]] == aile)
  if (length(aile_rows) != 2) next

  for (col in anne_check_cols) {
    v1 <- df[[col]][aile_rows[1]]
    v2 <- df[[col]][aile_rows[2]]
    if (is.na(v1) & is.na(v2)) next
    if (is.na(v1) | is.na(v2)) {
      inconsistent <- inconsistent + 1
      inconsistent_details[[length(inconsistent_details) + 1]] <- sprintf("Aile %s, %s: NA vs deger", aile, col)
      next
    }
    if (as.character(v1) != as.character(v2)) {
      inconsistent <- inconsistent + 1
      inconsistent_details[[length(inconsistent_details) + 1]] <- sprintf("Aile %s, %s: '%s' vs '%s'", aile, col, v1, v2)
    }
  }
}
cat(sprintf("  Anne verisi kalan uyumsuzluk: %d hucre\n", inconsistent))
if (inconsistent > 0 && inconsistent <= 20) {
  for (d in inconsistent_details) cat(sprintf("    %s\n", d))
}
cat(sprintf("  Toplam satir: %d\n", nrow(df)))
cat(sprintf("  Toplam sutun: %d\n", ncol(df)))

# --- 9. Kaydet ---
cat("\n=== 9. KAYIT ===\n")
out_dir <- "data/cleaned"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
out_path <- file.path(out_dir, "cleaned_dataset.csv")
# Veri icerigindeki Turkce karakterleri de ASCII'ye cevir
for (j in seq_len(ncol(df))) {
  if (is.character(df[[j]])) {
    non_na <- !is.na(df[[j]])
    df[[j]][non_na] <- tr_to_ascii(df[[j]][non_na])
  }
}
write.csv(df, out_path, row.names = FALSE, fileEncoding = "UTF-8")
cat(sprintf("Kaydedildi: %s\n", out_path))
cat(sprintf("Dosya boyutu: %.1f KB\n", file.size(out_path) / 1024))

cat("\n=== ISLEM TAMAMLANDI ===\n")
