# scripts/R/25_bayes_prior_center_sensitivity.R
# P0-1 yaniti: onsel MERKEZ duyarliligi (yalniz onsel-genislik degil).
# H1 reddetme (birincil), H3 sicaklik (isaret-catismasi) ve H3 reddetme icin
# uc onsel merkezinde (skeptik 0 / literatur-yonu / ters) BF10, pd, ROPE, estimate.
suppressPackageStartupMessages({ library(targets); library(brms) })
source("R/00_paths.R"); source("R/22_bayesian_parallel.R")
paths <- thesis_paths(); out_tables <- file.path(paths$outputs_dir, "tables")
dir.create(out_tables, showWarnings = FALSE, recursive = TRUE)
tar_load(c(df_family_ses, df_long_scored))
pf <- bayes_prepare_family(df_family_ses)
pl <- bayes_prepare_long(df_long_scored, df_family_ses)

fit_h1_center <- function(df_long, outcome, pm, psd = 0.50,
                          iter = 4000L, warmup = 1500L, chains = 4L, seed = 20260428L) {
  f <- sprintf("%s ~ group_f * family_role_f + anne_yas_z + ses_latent_z + (1 | aile_no_f)", outcome)
  pr <- c(
    brms::set_prior(sprintf("normal(%.3f, %.3f)", pm, psd), class = "b", coef = "group_fDM"),
    brms::set_prior("normal(0, 0.50)", class = "b"),
    brms::set_prior("normal(0, 2)", class = "Intercept"),
    brms::set_prior("student_t(3, 0, 2.5)", class = "sigma"),
    brms::set_prior("student_t(3, 0, 2.5)", class = "sd"))
  fit <- tryCatch(suppressMessages(suppressWarnings(brms::brm(
    formula = stats::as.formula(f), data = df_long, prior = pr, sample_prior = "yes",
    iter = iter, warmup = warmup, chains = chains, seed = seed, cores = chains,
    backend = "rstan", refresh = 0,
    control = list(adapt_delta = 0.95, max_treedepth = 12)))), error = function(e) e)
  fit
}
fit_h3_center <- function(df_family, outcome, pm, psd = 0.50, ...) {
  res <- bayes_h3_one_outcome(df_family, outcome, prior_mean = pm, prior_sd = psd)
  res
}
summ_row <- function(hyp, outcome, pm, psd, fit) {
  if (inherits(fit, "error") || is.null(fit)) {
    return(data.frame(hypothesis=hyp, outcome=outcome, prior_center=pm, prior_sd=psd,
      estimate=NA, ci_lo=NA, ci_hi=NA, pd=NA, rope_pct=NA, bf10=NA, bf_class="Indeterminate",
      max_rhat=NA, n_divergent=NA, stringsAsFactors=FALSE))
  }
  s <- bayes_extract_summary(fit, "^b_group_fDM")
  bf <- bayes_savage_dickey_bf(fit, "b_group_fDM", prior_sd = psd)
  dv <- tryCatch(rstan::get_num_divergent(fit$fit), error=function(e) NA_integer_)
  rh <- tryCatch(max(brms::rhat(fit), na.rm=TRUE), error=function(e) NA_real_)
  data.frame(hypothesis=hyp, outcome=outcome, prior_center=pm, prior_sd=psd,
    estimate=s$estimate[1], ci_lo=s$ci_lo[1], ci_hi=s$ci_hi[1], pd=s$pd[1],
    rope_pct=s$rope_pct[1], bf10=bf, bf_class=bayes_bf_classify(bf),
    max_rhat=rh, n_divergent=dv, stringsAsFactors=FALSE)
}

jobs <- list(
  list(h="H1", oc="embu_c_reddetme_mean", centers=c(0.0, 0.20, -0.20), fam=FALSE),
  list(h="H3", oc="embu_p_sicaklik_mean", centers=c(0.0, 0.20, -0.20), fam=TRUE),
  list(h="H3", oc="embu_p_reddetme_mean", centers=c(0.0, -0.15, 0.15), fam=TRUE)
)
rows <- list()
for (j in jobs) for (pm in j$centers) {
  cat(sprintf("[fit] %s %s center=%.2f\n", j$h, j$oc, pm)); flush.console()
  if (j$fam) {
    r <- fit_h3_center(pf, j$oc, pm)
    fit <- if (is.list(r) && !is.null(r$fit)) r$fit else NULL
  } else {
    fit <- fit_h1_center(pl, j$oc, pm)
  }
  rows[[length(rows)+1L]] <- summ_row(j$h, j$oc, pm, 0.50, fit)
}
out <- do.call(rbind, rows)
utils::write.csv(out, file.path(out_tables, "bayes_prior_center_sensitivity.csv"), row.names = FALSE)
cat("\n[done] bayes_prior_center_sensitivity.csv\n"); print(out[,c("hypothesis","outcome","prior_center","estimate","pd","bf10","bf_class")])

# --- II-5: H3 TOST esdegerlik siniri (SESOI) duyarliligi (0.20/0.25/0.30) ------
# Ek 5 (@tbl-apa-tost-sensitivity) icin tost_sensitivity.csv uretir; boylece
# "scripts/R/25 + scripts/R/05 + tar_make" dizisi tum denetim-yaniti ek
# tablolarini temiz klonda yeniden uretir.
source("R/21_robustness_sensitivity.R")
tost_prepared <- robust_prepare_frame(df_family_ses)
tost_out <- do.call(rbind, lapply(c(0.20, 0.25, 0.30),
  function(b) robust_tost(tost_prepared, sesoi_d = b)))
utils::write.csv(tost_out, file.path(out_tables, "tost_sensitivity.csv"), row.names = FALSE)
cat("\n[done] tost_sensitivity.csv\n")
print(tost_out[, intersect(c("outcome","sesoi","observed_d","tost_p","nhst_p","decision"), names(tost_out))])

