source("R/31_final_plans.R")

publication <- final_publication_strategy()
evidence <- final_publication_evidence_map()
risk <- final_risk_matrix()
timeline <- final_timeline_24_week()
bundle <- final_planning_bundle()
manifest <- final_planning_manifest(bundle)

stopifnot(nrow(publication) == 3L)
stopifnot(setequal(publication$manuscript_id, c("M1", "M2", "M3")))
stopifnot(all(nzchar(publication$working_title)))
stopifnot(nrow(evidence) >= 9L)
stopifnot(all(evidence$manuscript_id %in% publication$manuscript_id))

stopifnot(nrow(risk) == 14L)
stopifnot(sum(risk$status == "aktif-izlem") >= 3L)
stopifnot(any(grepl("HbA1c", risk$risk)))
stopifnot(!any(risk$status == "deferred-sınır"))
stopifnot(any(grepl("LCA tertile", risk$mitigation)))

stopifnot(nrow(timeline) == 21L)
stopifnot(sum(timeline$status == "verified") >= 20L)
stopifnot(any(timeline$week == "23"))
stopifnot(any(timeline$week == "24"))

stopifnot(length(bundle) == 6L)
stopifnot(all(vapply(bundle, is.data.frame, logical(1))))
stopifnot(nrow(manifest) == 6L)
stopifnot(all(manifest$rows > 0L))

cat("[PASS] Final publication/risk/timeline plans\n")
