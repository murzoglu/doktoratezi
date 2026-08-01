# [KESIFSEL - POST-HOC] Faz V SAP KISIM L (§136-141) audit runner
#
# Artik Iliski Yuzeyi (Residual Association Surface) — OSF Layer 6.
# I/O YALNIZ bu runner'da; ciktilar YALNIZ outputs/tables/ altina yazilir.
# Kanonik CSV'lere yazma yoktur; yukleme R/01_io.R uzerinden dogrulanir.
# Konsola yalniz agregat/kosum durumu yazilir; satir-duzeyi veri DOKULMEZ.

source("R/07_reproducibility.R")
source("R/01_io.R")
source("R/10_derived_scores.R")
source("R/11_ses_composites.R")
source("R/64_phase5_residual_associations.R")

paths <- canonical_final_reference_paths()
loaded <- load_final_reference_data(paths)

df_family <- prepare_family(loaded$family)
df_long <- prepare_long(loaded$long)
df_family_scored <- derive_family_scores(df_family)
df_family_ses <- derive_ses_composites(df_family_scored)$data

result <- run_phase5_residual_associations_pipeline(
  df_family_ses = df_family_ses,
  n_boot = 1000L,
  sesoi_r = 0.10,
  sesoi_d = 0.20,
  seed = 20260714L
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write_audit_csv <- function(df, path) {
  if (is.null(df) || nrow(df) == 0L) {
    stub <- data.frame(note = "empty result", statu = "[KESIFSEL - POST-HOC]",
      stringsAsFactors = FALSE)
    utils::write.csv(stub, path, row.names = FALSE, fileEncoding = "UTF-8")
  } else {
    utils::write.csv(df, path, row.names = FALSE, fileEncoding = "UTF-8")
  }
}

write_audit_csv(result$beck_sibling,
  "outputs/tables/phase5_beck_sibling.csv")
write_audit_csv(result$informant_transmission,
  "outputs/tables/phase5_informant_transmission.csv")
write_audit_csv(result$overprotection_gradient,
  "outputs/tables/phase5_overprotection_gradient.csv")
write_audit_csv(result$education_gap,
  "outputs/tables/phase5_education_gap.csv")
write_audit_csv(result$same_sex_sibling,
  "outputs/tables/phase5_same_sex_sibling.csv")
write_audit_csv(result$fdr,
  "outputs/tables/phase5_fdr.csv")
write_audit_csv(result$target_summary,
  "outputs/tables/phase5_target_summary.csv")

# --- Konsol ozeti (yalniz agregat) ---
cat("=== Faz V KISIM L — Artik Iliski Yuzeyi (§136-141) ===\n")

bs <- result$beck_sibling
bs_ok <- bs[bs$statu_kosum == "ok", , drop = FALSE]
if (nrow(bs_ok) > 0L) {
  cat("[§136 Beck->SRQ] ham r (kismi std_beta):\n")
  for (i in seq_len(nrow(bs_ok))) {
    cat(sprintf("  %-9s r=%.3f [%.3f, %.3f] p=%.3f | std_beta=%.3f p=%.3f\n",
      bs_ok$boyut[i], bs_ok$ham_r[i], bs_ok$ham_ci_alt[i], bs_ok$ham_ci_ust[i],
      bs_ok$ham_p[i], bs_ok$std_beta[i], bs_ok$p[i]))
  }
}

tr <- result$informant_transmission
tr_ok <- tr[tr$statu_kosum == "ok", , drop = FALSE]
if (nrow(tr_ok) > 0L) {
  cat("[§137 transmisyon] a(Beck->P) / b(P->C_idx) / dolayli [GA]:\n")
  for (i in seq_len(nrow(tr_ok))) {
    cat(sprintf("  %-14s a=%.3f(p=%.3f) b=%.3f(p=%.3f) dolayli=%.4f [%.4f, %.4f]\n",
      tr_ok$boyut[i], tr_ok$a_yolu[i], tr_ok$a_p[i], tr_ok$b_yolu[i], tr_ok$b_p[i],
      tr_ok$dolayli[i], tr_ok$dolayli_ci_alt[i], tr_ok$dolayli_ci_ust[i]))
  }
}

og <- result$overprotection_gradient
og_joint <- og[og$analiz == "birlesik_model" & og$statu_kosum == "ok", , drop = FALSE]
if (nrow(og_joint) > 0L) {
  cat("[§138 asiri koruma birlesik model] std_beta:\n")
  cat(sprintf("  %s\n", paste(sprintf("%s=%.3f(p=%.3f)", og_joint$terim, og_joint$std_beta,
    og_joint$p), collapse = ", ")))
}

eg <- result$education_gap
eg_ok <- eg[eg$statu_kosum == "ok", , drop = FALSE]
if (nrow(eg_ok) > 0L) {
  cat("[§139 egitim farki]\n")
  for (i in seq_len(nrow(eg_ok))) {
    cat(sprintf("  %s -> %s: r=%.3f [%.3f, %.3f] p=%.3f\n",
      eg_ok$yordayici[i], eg_ok$boyut[i], eg_ok$r[i], eg_ok$ci_alt[i],
      eg_ok$ci_ust[i], eg_ok$p[i]))
  }
}

ss <- result$same_sex_sibling
ss_ok <- ss[ss$statu_kosum == "ok", , drop = FALSE]
if (nrow(ss_ok) > 0L) {
  cat("[§140 same_sex->SRQ] Cohen d (grup1 eksi grup0):\n")
  for (i in seq_len(nrow(ss_ok))) {
    cat(sprintf("  %-9s d=%.3f p=%.3f | TOST(d=.20) %s\n",
      ss_ok$boyut[i], ss_ok$cohen_d[i], ss_ok$t_p[i], ss_ok$tost_karar[i]))
  }
}

fdr <- result$fdr
if (nrow(fdr) > 0L) {
  cat(sprintf("[FDR/BH] %d test; anlamli (p_bh<.05)=%d\n",
    nrow(fdr), sum(fdr$p_bh < 0.05, na.rm = TRUE)))
}

cat(sprintf("Durum: TAMAM (n_aile=%d). Tum tablolar outputs/tables/phase5_*.csv\n",
  result$target_summary$n_aile))

invisible(result)
