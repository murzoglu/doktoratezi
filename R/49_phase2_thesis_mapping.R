# [KESIFSEL - POST-HOC] Faz II SAP KISIM XXXII/94, 95
# Tez Bolum 6 Eslemesi + Makale 4-6 Plan
#
# 94 — Bolum 6 (Post-Hoc Genisleme) chapters/06_post_hoc_genisleme.qmd
#      icin paragraph eslemesi: hangi Faz II audit/figur hangi alt-bolume
#      yansiyacak. Sapma disiplini etiketleri her paragrafta korunur.
#
# 95 — Makale 4-6 yayin plan: CSR'daki 3-makale planina ek olarak Faz II
#      bulgularinin ayri yayinlar olarak konumlandirilmasi.

phase2_thesis_chapter06_mapping <- function() {
  data.frame(
    chapter_section = c(
      "6.1 Faz II'nin Epistemik Statusu ve Sapma Disiplini",
      "6.2 Multi-Informant Yapisal Genisletme (KISIM XX)",
      "6.3 Psikometrik Robustlestirme (KISIM XXI)",
      "6.4 Antidepresan ve Mental Saglik Yuku (KISIM XXII)",
      "6.5 H5 Diadik Tutarlilik Genisletmesi (KISIM XXIII)",
      "6.6 Klinik Stratifikasyon (KISIM XXIV)",
      "6.7 Nedensel Aracilik Sensitivitesi (KISIM XXV)",
      "6.8 Distribusyonel Yaklasimlar (KISIM XXVI)",
      "6.9 Multiverse Genisletme (KISIM XXVII)",
      "6.10 Meta-Analitik Birlestirme (KISIM XXVIII)",
      "6.11 Klinik Karar Modeli Ic-Validasyon (KISIM XXIX/84-85)",
      "6.12 Mevcut Ornek Guc Karakterizasyonu (KISIM XXX/87-89)",
      "6.13 Genel Sonuc ve Tezin Sinirliliklari (Faz II Lensi)"
    ),
    primary_audit_csv = c(
      "—",
      "phase2_trifactor_*, phase2_disc_*, phase2_xinfo_*",
      "phase2_floor_irt_*, phase2_omegah_*, phase2_esem_*",
      "phase2_ad_*",
      "phase2_h5ext_*",
      "phase2_hba1c_*",
      "phase2_imai_*, phase2_dag_*",
      "phase2_dist_*",
      "phase2_multi_*",
      "phase2_meta_*",
      "phase2_clinical_snb, phase2_clinical_dca_heatmap",
      "phase2_power_multilevel, phase2_power_apim, phase2_power_bayesian_ssd",
      "phase2_apa_summary_table"
    ),
    primary_figure = c(
      "—",
      "phase2_f01_trifactor.png + phase2_f02_xinfo.png",
      "phase2_f03_floor_irt.png",
      "phase2_f04_h5_strat.png (AD x H5 strata)",
      "phase2_f04_h5_strat.png (paylasilir)",
      "—",
      "—",
      "—",
      "phase2_f05_h1_spec_curve.png",
      "phase2_f06_meta_forest.png",
      "—",
      "—",
      "—"
    ),
    headline_finding = c(
      "OSF Layer 3 amendment + Tip 3 sapma disiplini",
      "Cocuk method varyansi %60 (Operations Triad ampirik karsiligi)",
      "EMBU-C reddetme omega_h_s = .009 (alt skor savunulamaz); floor-aware d=0.37",
      "AD mediator NS; AD x grup H1 stabil; Beck x AD sicaklik sinirda uncoupling",
      "Sibling reddetme ICC=0 DM grubunda; H5 strat pooled DM=.179",
      "HbA1c x sicaklik pd=.944 (Pinquart prior amplified, n=39)",
      "Imai-Keele rho_critical < 0.05 (very fragile); c' triangulation 3/3 anlamli",
      "Reddetme tau_0.75 = +.250; sigma posterior pd=.987; beta reg p<10^-6",
      "H1 multiverse %75 anlamli; SCA inferential perm p=.0002",
      "Pooled = 0.139 [0.049, 0.230]; bu calisma meta-pool merkezinde",
      "AUC=.703 CSR ile birebir; sNB=.86 esik 0.05; ic-val pratigi",
      "n=241'de d=0.20 power=.535; mevcut ornek guc-sinirini karakterize eder",
      "Sentez: H1 reddetme bulgusunun multi-katmanli triangulation"
    ),
    deviation_label = "[KESIFSEL - POST-HOC]",
    osf_reference = "Layer 3 amendment (OSF-LAYER3-AMENDMENT.md)",
    stringsAsFactors = FALSE
  )
}

phase2_publication_plan <- function() {
  # Yeni veri toplama gerektiren makaleler (Faz III replication required)
  # cikarildi; sadece mevcut veriyle self-contained yazilabilen makaleler.
  data.frame(
    paper_id = paste0("Makale_", 4:6),
    title = c(
      "Multi-Informant Discrepancy as Diverging Operations: A Trifactor + LDS Analysis in Pediatric Type 1 Diabetes",
      "Floor-Aware IRT Reveals Hidden Effect of Pediatric Chronic Illness on Perceived Maternal Rejection",
      "Maternal Antidepressant Use as a Mediator/Moderator of Parenting Outcomes in Pediatric Type 1 Diabetes Families"
    ),
    primary_kisim = c("XX", "XXI", "XXII"),
    primary_findings = c(
      "Trifactor: cocuk method varyansi %60.7; Sibling reddetme ICC DM=0 vs Kontrol=0.32; latent discrepancy variance dominant",
      "Floor effect 8/8 EMBU-P reddetme item > %62; Tobit-aware d_indeks=0.37 (manifest 0.16'in 2.3x); omega_h_s reddetme=.009",
      "AD mediator indirect NS but c' direct anlamli; Beck x AD sicaklik moderation sinirda; H5 reddetme DM/AD-var r=0.15 vs DM/AD-yok r=-0.09"
    ),
    target_journal_primary = c(
      "Journal of Child Psychology and Psychiatry (IF ~7)",
      "Psychometrika (IF ~3) / Educational and Psychological Measurement",
      "Pediatric Diabetes (IF ~3.5) / Journal of Pediatric Psychology"
    ),
    target_journal_alternate = c(
      "Psychological Methods / Development and Psychopathology",
      "Applied Psychological Measurement",
      "Diabetes Care / Health Psychology"
    ),
    word_target = c(8000L, 6000L, 7000L),
    figures_target = c(4L, 3L, 4L),
    tables_target = c(3L, 3L, 4L),
    submission_target = c("2027-Q3 (Faz II self-contained)",
      "2027-Q3 (Faz II self-contained)",
      "2027-Q3 (Faz II self-contained)"),
    osf_layer = "Layer 3 (Faz II) self-contained",
    data_status = "Mevcut Faz I kanonik baz yeterli — yeni veri gerekmez",
    stringsAsFactors = FALSE
  )
}

phase2_quarto_chapter_paragraph_seeds <- function() {
  list(
    s6_1 = "Faz II analizleri ana SAP'nin (KISIM I-XVIII) kapsami disinda kalan, calisma-sonu verilerinden tetiklenen 13 bilimsel boslugu kapatmak amaciyla yurutulmustur. Tum bulgular [KEŞİFSEL · POST-HOC] etiketi ile raporlanir; OSF Layer 3 amendment kapsaminda kayitlanmis ve replikasyon zorunlulugu ile birlikte konumlandirilmistir. Bu bolum, Faz II'nin 11 yeni R modulu ve 200+ targets ile uretilen 39 dogrulanmis post-hoc analizinin sentezini sunar.",

    s6_2 = "Multi-informant analiz katmaninda Trifactor T-CFA modeli (Mâsse 2020 / Eid 2008 CT-C(M-1)) anne-indeks-kardes ortak olcum yapisini test etmis; cocuk method varyansi %60.7 olarak gozlemlenmistir (anne reference). Latent informant discrepancy SEM'de reddetme alt olceginde anne-cocuk latent korelasyonu r = .025 (CSR §11.5.6 manifest ICC zayifliginin latent dogrulayicisi); LDS varyans dekompozisyonu 4/4 alt olcekte discrepancy ratio > .50 ('dominant') sergilemistir. Cross-informant GGM 16 edge'in yalniz 1'i (%6.3) cross-informant olarak kestirilmistir.",

    s6_3 = "Psikometrik robustlestirme katmaninda EMBU-P reddetme item kumesinde 7/8 madde > %80 floor effect dogrulanmis; floor-aware Tobit IRT (mirt empiricalhist) altinda EMBU-C reddetme indeks Cohen's d = +0.37 (manifest mean d=0.16'nin 2.3 kati). Bifactor S-1 reliability generalization analizi EMBU-P icin omega_h = .660, ECV = .409 — multidimensional yapi; en kritik bulgu EMBU-C reddetme alt-olcek-spesifik omega_h_s = .009 (pratik sifir): reddetme alt skoru psikometrik olarak ayri kullanim icin savunulamaz.",

    s6_4 = "Anne antidepresan kullanim hatti analizleri (n=241; AD-var=46) AD'nin DM grup uyeligi ile parenting tutumlari arasinda mediator rolu olusturmadigini gostermistir (4/4 outcome icin BCa indirect %95 GA sifiri icerir). H1 multilevel modelde group_dm:ad_bin etkilesimi tum 4 outcome icin NS — H1 reddetme bulgusu AD-strata baginsiz. Beck x AD sicaklik aliskanligi sinirda anlamli (β=-.166, p=.107) — Klein-Moosbrugger tedavi-aracilı uncoupling on-sinyali. H5 stratified Pearson r reddetme: DM/AD-var=+.147 vs DM/AD-yok=-.091.",

    s6_5 = "H5 diadik tutarlilik genisletmesinde MTMM CT-C(M-1) cocuk method varyansi %60.7 dogrulamis; Beck x grup moderation reddetme alt olceginde sinirda anlamli (β=+.122, %95 boot CI[-.004, +.249]); sibling-pair concordance ICC reddetme alt olceginde DM=0 (tam ortagonal) vs Kontrol=.322 (orta uyum) — McHale 2000 PDT (parental differential treatment) hipotezinin guclu ampirik karsiligi; H5 strateji-duzeyi metafor REML pooling DM = +.179 [+.097, +.260], heterogeneity tau=.073.",

    s6_6 = "DM-only HbA1c klinik stratifikasyonunda (n=39) Bayesian joint model Pinquart 2018 + Anderson 2002 informative prior (Normal(0.16, 0.10)) altinda sicaklik (pd=.944) ve karsilastirma (pd=.946) outcome'larinda HbA1c ile pozitif yon — frequentist NS ama Bayesian probability of direction yuksek. Tani yasi cubic spline 4/4 outcome'da 'linear sufficient' (CSR §12.5.2 dogrulayici). ISPAD <%7 logistic n_events=8 yetersiz guc; OR yon karsilastirma=2.27 (anlamsiz ama ters yon dikkati).",

    s6_7 = "Nedensel aracilik sensitivitesi modulu Imai-Keele-Tingley (2010) manuel rho_critical formulu ile uygulanmis; tum 4 outcome icin ρ_critical < 0.05 ('very_fragile_to_unmeasured_confounding') — sequential ignorability kirilganligi cok yuksek. c' direct effect triangulation 3 paralel mediation modelinde 3/3 reddetme ve 3/3 asiri koruma yolunun anlamli kalmasi (β = +.146-.198) H1 birincil bulgusunun mediation-bagimsiz dogrulayicisidir. PC algoritmasi yerine dagitty conditional independence implications ile manuel partial correlation testi: 12/12 test 'consistent' — DAG yapisi veri ile uyumlu. 3-level varyans modelinde sicaklik alt olceginde ICC_year=.154 (LRT p<.001); group_dm 2-level → 3-level gecisinde sicaklik yön degistirir (+.124 → -.078) — CSR §13.5 negctrl flag'inin yapisal yaniti.",

    s6_8 = "Distribusyonel yaklasimlar kuyruk-bagimli heterojenite ortaya koymustur: quantile regression reddetme tau=0.75 β=+.250 (medyan etkinin 1.7 kati); sigma posterior 3/4 outcome icin sifirin ustunde (DM grubunda hem ortalama hem varyans yukari yonlu kayma); beta regression bounded outcome reddetme β=+0.462 (p<10^-6, log-odds olcekde manifest mean'in 3 kati).",

    s6_9 = "H1 multiverse 120 spec random subset analizi: 120/120 ok, medyan β=+0.134, %75 spec'inde p<.05, %100'unde pozitif yön. SCA inferential test 5000 permutation altinda observed t=4.084, perm p=.0002 — H1 reddetme bulgusu spec curve toplu inferential test'inde null hipotezini reddediyor. CSR §13.6'da raporlanan H1 vs H3 multiverse paradoksunun yapisal cozumu: iki ayri veri seti (cocuk vs anne perspektifleri).",

    s6_10 = "Bayesian meta-analytic pooling 4 prior meta-analiz (Pinquart 2013, Pinquart 2018, Lovejoy 2000, Vermaes 2012) + bu calismanin 4 outcome estimate'i metafor REML fallback ile birlestirilmis: pooled = +0.139 [+0.049, +0.230], tau=0.106 — sıfırı net olarak disarda, bu calismanın bulgusu 8-study meta-pool merkezinde. Posterior predictive replication 4/4 outcome 'ppc_consistent'; empirical Bayes shrinkage 4/4 outcome 'expected_random_outlier_rate' — Bayesian validation katmanlari triangule.",

    s6_11 = "Yuksek-risk anne sinıflandırma modeli (BDI≥17) extended logistic AUC=.703 (n=238) CSR §12.4 ile birebir tutarlı; standardized net benefit (Kerr 2016) threshold 0.05'te sNB=.86; DCA threshold-sensitivity 10×10 heatmap mevcut ornek uzerinde Vickers 2006 net-benefit egrisini sunmustur. Bu KISIM ic-validasyonlu raporlama hatti olarak tezde konumlandirilmistir.",

    s6_12 = "Manuel Monte Carlo multilevel power simulasyonu (200 sim) d=0.20 ICC=0.20 altında n_aile=241 icin power=.535 — CSR'in mevcut H1 bulgusu güç-sınırı altında pozitif sinyal yakalayabilmistir. APIM sample size r=0.20'de n_dyad=165, Bayesian SSD ROPE=±0.10 SD altinda HDI=.20 hedefi icin n≥500 onerilir. Bu power karakterizasyonu mevcut ornekteki bulgularinin guvenirlik aralığını ortaya koyar; tum analizler n=241 kanonik bazda tamamlanmistir.",

    s6_13 = "Faz II'nin sentezi: H1 reddetme birincil bulgusu (CSR §11.1: β=0.16, BF₁₀=8.12) [KEŞİFSEL · POST-HOC] cercevede coklu-katmanli triangulation ile guclendirilmistir — Trifactor T-CFA latent yapisal dogrulama, floor-aware IRT 2.3× amplification, multiverse %75 spec anlamli, SCA inferential perm p=.0002, Bayesian meta-pool merkezde, c' direct triangulation 3/3 anlamli, PPC ppc_consistent, EB outlier expected. CSR'da raporlanan ana sonuclarin hicbiri DEGISMEZ; Faz II bulgulari mevcut Faz I kanonik baz uzerinde tamamlanmistir. Yeni veri toplama gerektiren ileri-faz analizler (longitudinal trajectory, dis-validasyon, cok-merkezli replikasyon) bu calismanin kapsami disinda birakilmistir; Faz II'den ureyen sibling PDT, AD-aracili pathway ve distribusyonel heterojenite gibi yeni hipotezler tartismada gelecek arastirma onerisi olarak sunulur."
  )
}

run_phase2_thesis_mapping_pipeline <- function() {
  chapter_mapping <- phase2_thesis_chapter06_mapping()
  publication_plan <- phase2_publication_plan()
  paragraph_seeds <- phase2_quarto_chapter_paragraph_seeds()

  list(
    chapter_mapping = chapter_mapping,
    publication_plan = publication_plan,
    paragraph_seeds_summary = data.frame(
      section = names(paragraph_seeds),
      n_chars = vapply(paragraph_seeds, nchar, integer(1L), USE.NAMES = FALSE),
      stringsAsFactors = FALSE
    ),
    target_summary = data.frame(
      analysis = "phase2_thesis_mapping",
      n_chapter_sections = nrow(chapter_mapping),
      n_publications_planned = nrow(publication_plan),
      kanit_kategorisi = "[KESIFSEL - POST-HOC]",
      sapma_tipi = "Tip 3 (Faz II SAP KISIM XXXII/94, 95)",
      reference_doc = "STATISTICAL-ANALYSIS-PLAN-PHASE-2.md",
      quarto_chapter = "chapters/06_post_hoc_genisleme.qmd",
      stringsAsFactors = FALSE
    )
  )
}

if (!exists("%||%", mode = "function")) {
  `%||%` <- function(a, b) if (is.null(a)) b else a
}
