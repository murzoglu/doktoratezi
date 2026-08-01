# Turkish Scientific Writing Audit (sci-audit axis G)

- Path: `chapters/01_giris_ve_amac.qmd`
- Strictness: `certification`
- Human review required: `true`
- Scope note: This audit checks Turkish scientific writing signals only (sci-audit axis G); it does not certify scientific truth, citation validity, plagiarism, or clinical validity (see axes A-F).

## Metrics

| Metric | Value |
|---|---:|
| Paragraphs | 10 |
| Sentences | 45 |
| Words | 1276 |
| Syllables | 3868 |
| Avg. words/sentence | 28.36 |
| Avg. syllables/word | 3.03 |
| Ateşman score | 3.03 |
| Ateşman label | very-hard |

## Issue Summary

- Errors (blocker): 0
- Warnings (major): 7
- Info (minor): 1

## Issues

| Severity | Code | Line | Message | Evidence |
|---|---|---:|---|---|
| warning | `decimal-dot` | 3 | Use the decimal comma in Turkish scientific prose unless this is a version number or identifier. | 108.300 |
| warning | `decimal-dot` | 3 | Use the decimal comma in Turkish scientific prose unless this is a version number or identifier. | 149.500 |
| info | `abbreviation-review` | 3 | Check whether this abbreviation is expanded at first use and used consistently. | IDF |
| warning | `sentence-long` | 7 | Sentence is long; check readability and ambiguity. | Doğrudan T1DM'li çocuk ve ergenlere odaklanan sistematik derleme de bu örüntüyü desteklemektedir: destekleyici ve özerklik destekleyici e... |
| warning | `sentence-long` | 11 | Sentence is long; check readability and ambiguity. | T1DM özelindeki güncel nitel kanıt da sağlıklı kardeşlerin tanı dönemini ve sonrasını sıklıkla karşılanmamış gereksinimler çerçevesinde d... |
| warning | `sentence-long` | 17 | Sentence is long; check readability and ambiguity. | Bu doğrultuda tezin temel araştırma sorusu, T1DM tanılı çocuğu olan ailelerde ebeveynlik tutumu, anne depresif belirtileri ve kardeş iliş... |
| warning | `sentence-long` | 21 | Sentence is long; check readability and ambiguity. | İlk üç alt amaç, aile üyelerinin ebeveynlik ve ilişki bildirimlerini gruplar arasında karşılaştırmaya yöneliktir: T1DM tanılı çocuklar il... |
| warning | `readability-very-hard` | 1 | Ateşman score is very low; verify the difficulty is justified by scientific content. | 3.03 |

## Provider Layers

| Provider | Enabled | Status | Summary |
|---|---:|---|---|
| `zemberek` | false | `skipped` | Not requested. Use --enable-zemberek. |
| `gecturk` | false | `skipped` | Not requested. Use --enable-gecturk. |
| `tdk` | false | `skipped` | Not requested. Use --enable-tdk. |
| `llm-judge` | false | `skipped` | Not requested. Use the style-judge subagent, or --enable-grok in CI. |
