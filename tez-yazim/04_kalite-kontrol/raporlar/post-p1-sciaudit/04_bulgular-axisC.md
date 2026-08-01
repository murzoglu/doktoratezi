{
  "axis": "C-statistics",
  "counts": {
    "error": 0,
    "warning": 0,
    "info": 0
  },
  "findings": [],
  "checks_run": [
    "statcheck",
    "grim",
    "grimmer",
    "sprite",
    "confidence-intervals",
    "percentage-sums",
    "subgroup-sums",
    "effect-size"
  ],
  "caveat": "statcheck / GRIM / GRIMMER / SPRITE are TRIGGER signals for manual review, not a final arbiter. A flag is not proof of error or misconduct — innocent causes include rounding, an undisclosed multiple-comparison correction (statcheck does NOT recognise these), copy-paste slips, or a different N due to missing data. GRIM/GRIMMER/SPRITE apply only to integer-item scales; note false-positive risk on continuous measures. 'No findings' means 'no inconsistency in the machine-readable inline statistics', NOT 'scanned clean'.",
  "scope_note": "Document-internal statistical consistency only — evaluates the numbers AS PRESENTED, requires no raw data, code, or reproduction. Deterministic statcheck/GRIM/GRIMMER/SPRITE/CI/percentage/subgroup/effect-size checks."
}
