# Ham-veri sertifikasyon dogrulamasi: kanonik base -> pipeline skorlama -> rapor degerleri
# Hash zaten dogrulandi (lock ile eslesti). Burada her sayiyi base'den yeniden hesaplayip
# raporun (duzeltilmis) degerleriyle karsilastiriyoruz.
suppressWarnings(suppressMessages({
  source("R/10_derived_scores.R")
  have_psych <- requireNamespace("psych", quietly = TRUE)
}))
options(width = 200)

fam  <- read.csv("data/processed/FINAL_REFERENCE__analysis_base_family.csv", stringsAsFactors = FALSE, check.names = FALSE)
long <- read.csv("data/processed/FINAL_REFERENCE__analysis_base_long.csv",  stringsAsFactors = FALSE, check.names = FALSE)
fams <- derive_family_scores(fam)
longs <- derive_long_scores(long)

results <- list()
chk <- function(label, computed, report, tol = 0.05, fmt = "%.3f") {
  comp_s <- if (is.numeric(computed)) sprintf(fmt, computed) else as.character(computed)
  rep_s  <- if (is.numeric(report))   sprintf(fmt, report)   else as.character(report)
  if (is.numeric(computed) && is.numeric(report)) {
    ok <- isTRUE(abs(computed - report) <= tol)
  } else {
    ok <- isTRUE(as.character(computed) == as.character(report))
  }
  results[[length(results) + 1]] <<- data.frame(label = label, computed = comp_s, report = rep_s,
                                                 status = ifelse(ok, "PASS", "FAIL"), stringsAsFactors = FALSE)
}
g <- fam$group
prop_lvl <- function(v, grp, lvl) {  # pozitif duzeyin grup-ici orani (%)
  tapply(v == lvl, grp, function(x) 100 * mean(x, na.rm = TRUE))
}

cat("================ N & ROL ================\n")
chk("family N", nrow(fam), 241, 0, "%d"); chk("DM aile", sum(g=="DM"), 120, 0, "%d"); chk("Kontrol aile", sum(g=="Kontrol"), 121, 0, "%d")
chk("long N", nrow(long), 482, 0, "%d")
rc <- table(long$role)
chk("rol DM_Indeks", rc[["DM_Hasta_Indeks"]], 120, 0, "%d"); chk("rol DM_Kardes", rc[["DM_Hasta_Kardes"]], 120, 0, "%d")
chk("rol Kontrol_Indeks", rc[["Kontrol_Indeks"]], 121, 0, "%d"); chk("rol Kontrol_Kardes", rc[["Kontrol_Kardes"]], 121, 0, "%d")

cat("================ TABLO 1 DEMOGRAFIK ================\n")
amed <- tapply(fam$anne_yas, g, median, na.rm = TRUE)
chk("anne_yas medyan Kontrol", amed[["Kontrol"]], 37.3, 0.3, "%.1f"); chk("anne_yas medyan DM", amed[["DM"]], 38.5, 0.3, "%.1f")
# egitim modal
emod <- function(x) as.numeric(names(sort(table(x), decreasing = TRUE))[1])
epct <- function(x, m) 100*mean(x==m, na.rm=TRUE)
ek <- emod(fam$egitim_durumu[g=="Kontrol"]); ed <- emod(fam$egitim_durumu[g=="DM"])
chk("anne egitim mod Kontrol", ek, 3, 0, "%d"); chk("anne egitim mod DM", ed, 1, 0, "%d")
chk("anne egitim mod% Kontrol", epct(fam$egitim_durumu[g=="Kontrol"], ek), 34.7, 1.0, "%.1f")
chk("anne egitim mod% DM", epct(fam$egitim_durumu[g=="DM"], ed), 30.8, 1.0, "%.1f")
sek <- emod(fam$es_egitim_durumu[g=="Kontrol"]); chk("es egitim mod Kontrol", sek, 3, 0, "%d")
# ISEI ortalama + es==aile ozdeslik
imk <- tapply(fam$aile_isei08, g, mean, na.rm=TRUE)
chk("aile ISEI mean Kontrol", imk[["Kontrol"]], 31.35, 0.5, "%.2f"); chk("aile ISEI mean DM", imk[["DM"]], 34.49, 0.5, "%.2f")
ident <- isTRUE(all.equal(fam$es_isei08, fam$aile_isei08))
chk("es_isei08 == aile_isei08 (ozdeslik)", as.character(ident), "TRUE", fmt="%s")
# binary % (pozitif duzey tespiti)
cat("--- binary var degerleri ---\n")
for (v in c("ev_sahipligi","arabaniz_var_mi","kronik_hastalik_durumu","anne_antidepresan","es_calisma_durumu")) cat(v, ":", paste(names(table(fam[[v]])), table(fam[[v]]), sep="="), "\n")
# ev/araba/es_calisma: level 1 = pozitif; kronik: level 1 = hastalik var; antidep: Evet
ev <- prop_lvl(fam$ev_sahipligi, g, 1); chk("ev sahipligi% Kontrol", ev[["Kontrol"]], 46.3, 1.5, "%.1f"); chk("ev sahipligi% DM", ev[["DM"]], 45.0, 1.5, "%.1f")
ar <- prop_lvl(fam$arabaniz_var_mi, g, 1); chk("araba% Kontrol", ar[["Kontrol"]], 44.6, 1.5, "%.1f"); chk("araba% DM", ar[["DM"]], 51.7, 1.5, "%.1f")
kr <- prop_lvl(fam$kronik_hastalik_durumu, g, 1); chk("kronik% Kontrol (duzeltilmis)", kr[["Kontrol"]], 28.9, 1.5, "%.1f"); chk("kronik% DM (duzeltilmis)", kr[["DM"]], 24.2, 1.5, "%.1f")
ad_lvl <- names(sort(table(fam$anne_antidepresan), decreasing=TRUE)); ad_pos <- setdiff(unique(fam$anne_antidepresan), ad_lvl[1])[1]
adp <- prop_lvl(fam$anne_antidepresan, g, ifelse(is.na(ad_pos), 1, ad_pos))
cat("antidep pozitif duzey:", as.character(ifelse(is.na(ad_pos),1,ad_pos)), "\n")
chk("antidep% Kontrol", adp[["Kontrol"]], 9.1, 1.5, "%.1f"); chk("antidep% DM", adp[["DM"]], 29.2, 1.5, "%.1f")
ec <- prop_lvl(fam$es_calisma_durumu, g, 1); chk("es calisma% Kontrol", ec[["Kontrol"]], 95.9, 1.5, "%.1f"); chk("es calisma% DM", ec[["DM"]], 92.5, 1.5, "%.1f")
om <- tapply(fam$ev_oda_sayisi, g, mean, na.rm=TRUE); chk("ev oda mean Kontrol", om[["Kontrol"]], 1.72, 0.06, "%.2f"); chk("ev oda mean DM", om[["DM"]], 1.67, 0.06, "%.2f")
csm <- tapply(fam$cocuk_sayisi, g, median, na.rm=TRUE); chk("cocuk sayisi medyan Kontrol", csm[["Kontrol"]], 3.0, 0.01, "%.1f"); chk("cocuk sayisi medyan DM", csm[["DM"]], 3.0, 0.01, "%.1f")

cat("================ BECK ================\n")
bm <- tapply(fams$beck_total, g, mean, na.rm=TRUE); chk("beck_total mean Kontrol", bm[["Kontrol"]], 12.4, 0.5, "%.1f"); chk("beck_total mean DM", bm[["DM"]], 13.2, 0.5, "%.1f")
sev_k <- as.character(names(sort(table(fams$beck_severity[g=="Kontrol"]), decreasing=TRUE))[1])
sev_d <- as.character(names(sort(table(fams$beck_severity[g=="DM"]), decreasing=TRUE))[1])
chk("beck severity mod Kontrol", sev_k, "Minimal", fmt="%s"); chk("beck severity mod DM", sev_d, "Hafif", fmt="%s")
cat("beck severity bantlari (kanonik cut):", paste(levels(fams$beck_severity), collapse=" / "), "\n")
cat("beck clinical (>=17) tablo:\n"); print(table(fams$beck_clinical))

cat("================ HbA1c + STRATA (DM) ================\n")
dm <- fam[g=="DM", ]
n_h <- sum(!is.na(dm$hba1c)); chk("HbA1c non-missing n", n_h, 39, 0, "%d")
chk("HbA1c medyan", median(dm$hba1c, na.rm=TRUE), 9.0, 0.2, "%.1f")
u7 <- sum(dm$hba1c < 7, na.rm=TRUE); chk("HbA1c <7 sayisi", u7, 8, 0, "%d"); chk("HbA1c <7 %", 100*u7/n_h, 20.5, 1.0, "%.1f")
# tani yasi = cocuk_yas - dm_yili
ty <- dm$cocuk_yas - dm$dm_yili
strata <- cut(ty, breaks=c(-Inf,5,10,Inf), right=FALSE, labels=c("erken<5","okul5-10","ergen>=10"))
st <- table(strata); cat("strata (cut <5 / [5,10) / >=10):\n"); print(st)
chk("strata erken<5", as.integer(st[["erken<5"]]), 24, 0, "%d"); chk("strata okul", as.integer(st[["okul5-10"]]), 69, 0, "%d"); chk("strata ergen", as.integer(st[["ergen>=10"]]), 27, 0, "%d")

cat("================ EMBU SKOR + ALPHA ================\n")
emap <- embu_subscale_map(); for (s in names(emap)) chk(paste0("EMBU madde n: ", s), length(emap[[s]]), c(sicaklik=9,asiri_koruma=7,reddetme=8,karsilastirma=5)[[s]], 0, "%d")
if (have_psych) {
  rcols <- embu_score_item_columns("embu_p", emap$reddetme)
  a <- suppressMessages(psych::alpha(fam[rcols], warnings = FALSE))$total$raw_alpha
  chk("EMBU-P reddetme Cronbach alpha", a, 0.45, 0.02, "%.3f")
}

cat("================ H5 ICC (anne x indeks) ================\n")
icc_pair <- function(a, b) { # ICC(A,1) tek-olcumlu mutlak uyum; psych ICC2
  d <- na.omit(cbind(a, b)); if (nrow(d) < 5) return(NA_real_)
  if (have_psych) suppressMessages(psych::ICC(d)$results["Single_random_raters","ICC"]) else NA_real_
}
exp_icc <- list(sicaklik=c(K=0.145,D=0.027), asiri_koruma=c(K=0.204,D=0.009),
                reddetme=c(K=0.029,D=-0.006), karsilastirma=c(K=0.103,D=0.084))
ndir <- 0
for (s in names(emap)) {
  ap <- fams[[paste0("embu_p_", s, "_mean")]]; ci <- fams[[paste0("embu_c_idx_", s, "_mean")]]
  iK <- icc_pair(ap[g=="Kontrol"], ci[g=="Kontrol"]); iD <- icc_pair(ap[g=="DM"], ci[g=="DM"])
  chk(paste0("ICC ", s, " Kontrol"), iK, exp_icc[[s]][["K"]], 0.03, "%.3f")
  chk(paste0("ICC ", s, " DM"), iD, exp_icc[[s]][["D"]], 0.03, "%.3f")
  if (isTRUE(iK > iD)) ndir <- ndir + 1
}
chk("H5 yon: kac alt olcekte Kontrol>DM (4 olmali)", ndir, 4, 0, "%d")

cat("================ H1 aile-ici ICC (long, EMBU-C reddetme) ================\n")
le <- derive_embu_scores(long, "embu_c", "embu_c")
yr <- le$embu_c_reddetme_mean; aile <- long$aile_no
vv <- tapply(yr, aile, function(x) if (sum(!is.na(x))==2) diff(range(x, na.rm=TRUE)) else NA)
# unconditional ICC via aov
df1 <- na.omit(data.frame(y=yr, a=factor(aile)))
m <- aov(y ~ a, data=df1); ms <- summary(m)[[1]][,"Mean Sq"]; k <- 2
icc1 <- (ms[1]-ms[2])/(ms[1]+(k-1)*ms[2])
chk("H1 aile ICC (EMBU-C reddetme)", icc1, 0.14, 0.06, "%.3f")

cat("\n================ SONUC TABLOSU ================\n")
res <- do.call(rbind, results)
print(res, row.names = FALSE)
cat(sprintf("\nTOPLAM: %d kontrol | PASS: %d | FAIL: %d\n", nrow(res), sum(res$status=="PASS"), sum(res$status=="FAIL")))
if (any(res$status=="FAIL")) { cat("\n--- FAIL olanlar ---\n"); print(res[res$status=="FAIL",], row.names=FALSE) }
