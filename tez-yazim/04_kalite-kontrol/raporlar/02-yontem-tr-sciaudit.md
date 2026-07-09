# Turkish Scientific Writing Audit

- Path: `chapters/02_yontem.qmd`
- Strictness: `certification`
- Human review required: `true`
- Scope note: This repo-local audit checks Turkish scientific writing signals only; it does not certify scientific truth, plagiarism, or clinical validity.

## Metrics

| Metric | Value |
|---|---:|
| Paragraphs | 22 |
| Sentences | 61 |
| Words | 1206 |
| Syllables | 3232 |
| Avg. words/sentence | 19.77 |
| Avg. syllables/word | 2.68 |
| Ateşman score | 38.98 |
| Ateşman label | hard |

## Issue Summary

- Errors: 0
- Warnings: 5
- Info: 1

## Issues

| Severity | Code | Line | Message | Evidence |
|---|---|---:|---|---|
| info | `abbreviation-review` | 11 | Check whether this abbreviation is expanded at first use and listed consistently. | PI |
| warning | `decimal-dot` | 37 | Use decimal comma in Turkish thesis prose unless this is a version number or identifier. | 0.30 |
| warning | `decimal-dot` | 37 | Use decimal comma in Turkish thesis prose unless this is a version number or identifier. | 7.5 |
| warning | `sentence-too-long` | 39 | Sentence exceeds 55 words; split or simplify. | H1-H4 birincil bulguları için Bayesian paralel hat (KISIM XII) frequentist dual reporting standardına ek raporlanır. brms multilevel mode... |
| warning | `decimal-dot` | 39 | Use decimal comma in Turkish thesis prose unless this is a version number or identifier. | 1.01 |
| warning | `decimal-dot` | 41 | Use decimal comma in Turkish thesis prose unless this is a version number or identifier. | 0.5 |

## Provider Layers

| Provider | Enabled | Status | Summary |
|---|---:|---|---|
| `zemberek` | true | `ok` | Zemberek morphology ran on 80 unique words; 63 had at least one analysis. |
| `gecturk` | true | `ok` | GECTurk endpoint responded with HTTP 200. |
| `tdk` | true | `ok` | TDK lookup completed for 6 terms. |
| `grok-judge` | true | `ok` | Grok judge completed with model grok-4.3; text sent was capped at 6000 characters. |

## Provider Findings

### zemberek

```json
[
  {
    "unknown_words_sample": [
      "osf",
      "https",
      "vqrt",
      "kanonik",
      "prospektif",
      "i̇lk",
      "ended",
      "registration",
      "psikometrik",
      "validasyon",
      "reflective",
      "i̇kinci",
      "secondary",
      "preregistration",
      "pytfe",
      "submit",
      "embargo"
    ]
  }
]
```

### gecturk

```json
[
  {
    "response": {
      "service": "gecturk-selfhost",
      "engine": "repo-local-deterministic-fallback",
      "strictness": "certification",
      "metrics": {
        "paragraphs": 15,
        "sentences": 34,
        "words": 638,
        "syllables": 1760,
        "average_words_per_sentence": 18.76,
        "average_syllables_per_word": 2.76,
        "atesman_score": 38.45,
        "atesman_label": "hard"
      },
      "issue_counts": {
        "error": 0,
        "warning": 1,
        "info": 1
      },
      "issues": [
        {
          "severity": "warning",
          "code": "space-before-punctuation",
          "line": 19,
          "message": "Remove whitespace before punctuation.",
          "evidence": "Birincil total-effect modellerinin kovaryat seti Causal DAG ile sabitlenecektir. Uygulanan analiz DAG'ında , kardeş yaş farkı ve aile büy..."
        },
        {
          "severity": "info",
          "code": "abbreviation-review",
          "line": 7,
          "message": "Check whether this abbreviation is expanded at first use and listed consistently.",
          "evidence": "PI"
        }
      ],
      "truncated": false
    }
  }
]
```

### tdk

```json
[
  {
    "term": "diyabet",
    "found": true,
    "headword": "diyabet",
    "first_meaning": "► şeker hastalığı"
  },
  {
    "term": "depresyon",
    "found": true,
    "headword": "depresyon",
    "first_meaning": "► bunalım"
  },
  {
    "term": "ebeveyn",
    "found": true,
    "headword": "ebeveyn",
    "first_meaning": "Anne ve baba"
  },
  {
    "term": "kardeş",
    "found": true,
    "headword": "kardeş",
    "first_meaning": "Aynı anne babadan doğmuş veya anne babalarından biri aynı olan çocukların birbirine göre adı; karındaş"
  },
  {
    "term": "ölçek",
    "found": true,
    "headword": "ölçek",
    "first_meaning": "Birim kabul edilen herhangi bir şeyin alabildiği kadar ölçü"
  },
  {
    "term": "yöntem",
    "found": true,
    "headword": "yöntem",
    "first_meaning": "Bir amaca erişmek için izlenen, tutulan yol; yordam, usul (II), prosedür"
  }
]
```

### grok-judge

```json
[
  {
    "scores": {
      "logical_flow": 3,
      "terminology": 4,
      "academic_register": 4,
      "turkish_naturalness": 2
    },
    "issues": [
      {
        "criterion": "logical_flow",
        "note": "Metin yarım cümle ile bitiyor ve bazı geçişler ani.",
        "severity": "warning"
      },
      {
        "criterion": "turkish_naturalness",
        "note": "Yoğun İngilizce terim ve kısaltma karışımı doğal akışı bozuyor.",
        "severity": "warning"
      },
      {
        "criterion": "terminology",
        "note": "Terimler genel olarak tutarlı ancak bazıları (latent, frame vb.) Türkçe karşılıklarla desteklenmeli.",
        "severity": "info"
      }
    ]
  }
]
```
