# T1DM Niteliksel Repo Context

Updated: 2026-07-09

> **Migrasyon notu:** Bu içerik 2026-07-09 tarihinde bağımsız
> `/mnt/thunderbolt/workspaces/T1DM Niteliksel` reposundan
> `/mnt/thunderbolt/workspaces/doktoratezi/niteliksel` altına kopyalandı.
> Yeni canonical çalışma konumu `doktoratezi/niteliksel` alt-ağacıdır.

Bu repo klasik bir yazılım uygulaması değil; Tip 1 Diyabet tanılı çocuk, anne ve sağlıklı kardeş triadlarına ait nitel araştırma korpusu, analiz tabloları, tez/makale taslakları, referanslar ve belge işleme araçlarından oluşur. Reorganizasyon 2026-05-04 tarihinde uygulanmış; ham veri, işlenmiş metin, analiz, manuscript, referans, araç ve arşiv katmanları ayrılmıştır.

## 1. Project Identity

- `Verified` Root: `/mnt/thunderbolt/workspaces/doktoratezi/niteliksel`.
- `Historical` Source root: `/mnt/thunderbolt/workspaces/T1DM Niteliksel` (silinmedi; `.git/` ve `.env*` taşınmadı).
- `Verified` Repo type: `doktoratezi` ana reposu altında nitel araştırma alt-ağacı; git sürümleme üst repodan yönetilir.
- `Verified` Primary purpose: T1DM ile yaşayan ailelerde anne, T1DM'li çocuk ve sağlıklı kardeş perspektiflerinin aile yaşamı, bakım yükü, adalet algısı, kardeş ilişkileri, stigma, özerklik ve kontrol gerilimleri üzerinden analiz edilmesi.
- `Verified` Main design: qualitative descriptive / phenomenological sensitivity, multi-informant family design, Braun & Clarke reflexive thematic analysis, COREQ-aware reporting.
- `Verified` Sample in cleaned methods/results: 7 family triads, 21 participants.

## 2. Current Directory Architecture

- `00_context/`: repo context, before/after manifests, move log.
- `01_raw_data/`: ham/near-raw çalışma verisi ve idari materyal.
- `02_processed/`: dönüştürülmüş birleşik transcript ve işlenmiş metinler.
- `03_analysis/`: codebook, yöntem iskeleti, tema memoları, triadik matrisler, analiz tabloları.
- `04_manuscripts/`: aktif journal manuscript.
- `05_references/`: literatür PDF'leri, tez yazım kılavuzu, dış istatistik kaynağı.
- `06_tools/`: çalışan script'ler, legacy Windows path script'leri, kalite raporları.
- `99_archive/`: kesin mükerrerler ve superseded taslaklar.

## 3. Canonical Active Files

- Main cleaned qualitative text: `02_processed/cleaned_text/thesis_qualitative_cleaned_current.md`.
- Merged transcript/source dump: `02_processed/transcripts/all_transcripts_merged.md`.
- Codebook (güncel): `03_analysis/codebook/codebook_v2.md` (v1 `codebook_draft_v1.md` superseded).
- COREQ methods skeleton: `03_analysis/methodology/methodology_skeleton_coreq.md`.
- Current Pediatric Diabetes manuscript: `04_manuscripts/journal_pediatric_diabetes/pediatric_diabetes_results_discussion_draft_v2_journal_ready.docx`.
- Current triadic matrices:
  - `03_analysis/triadic_matrices/theme_01_triadic_matrix_v3_same_family_extra_quotes.docx`
  - `03_analysis/triadic_matrices/theme_02_triadic_matrix_v3_same_family_extra_quotes.docx`
  - `03_analysis/triadic_matrices/theme_03_triadic_matrix_v3_same_family_extra_quotes.docx`
  - `03_analysis/triadic_matrices/theme_04_triadic_matrix_v3_same_family_extra_quotes.docx`
  - `03_analysis/triadic_matrices/theme_05_triadic_matrix_v3_same_family_extra_quotes.docx`
  - `03_analysis/triadic_matrices/theme_06_triadic_matrix_v3_same_family_extra_quotes.docx`

## 4. Raw Data Map

- Interview DOCX files are grouped by family under `01_raw_data/interviews_docx/family_011`, `family_014`, `family_019`, `family_020`, `family_026`, `family_201`, and `family_202`.
- Role filenames are normalized as `family_<id>_mother.docx`, `family_<id>_patient.docx`, and `family_<id>_sibling.docx`.
- Demographics: `01_raw_data/demographics/qualitative_demographics.docx`.
- Ethics/protocol: `01_raw_data/ethics_protocol/dm_parenting_attitudes_ethics_protocol_2023_02.docx`.
- Interview guide: `01_raw_data/interview_guides/qualitative_interview_questions.docx`.

## 5. Analysis and Writing Structure

- Thesis-style cleaned Markdown has 4 macro themes:
  - healthy siblings / shared restriction and invisible burden,
  - motherhood axis shift / medical caregiver role,
  - child with T1DM lived experience,
  - triadic comparison / same home, three diabetes stories.
- Journal-style manuscript uses a 6-theme integrated triadic structure. Do not assume thesis and journal structures are interchangeable; clarify target output before rewriting.
- `03_analysis/spreadsheets/triadic_table.xlsx` and `03_analysis/spreadsheets/theme_comparison.ods` are structured analysis aids.
- `03_analysis/thematic_memos/mother_theme_memo.docx` is an analysis memo, not current manuscript source.

## 6. Archive Policy

- Definite duplicate files were moved to `99_archive/duplicates/`:
  - `family_019_sibling_duplicate_copy.docx`
  - `pediatric_diabetes_results_discussion_draft_v1_full_duplicate.docx`
- Superseded but audit-relevant drafts were moved to `99_archive/superseded/`:
  - older Pediatric Diabetes v1 drafts,
  - older thesis/nitel drafts,
  - Tema 1 v1/v2 triadic matrices.
- No files were deleted during reorganization.
- `00_context/reorg_move_log.tsv` records every original path and destination.
- `00_context/file_manifest_before_reorg.tsv` and `00_context/file_manifest_after_reorg.tsv` preserve SHA256-backed before/after inventories.

## 7. Data Boundaries and Privacy

- Raw DOCX interviews, merged transcript, demographic file, protocol/onam text and field notes are sensitive research data.
- Do not quote or export raw participant text unless the quote is intentionally selected and anonymized with family/role code.
- Do not store names, birth dates, addresses, signed consent text, or family-level demographic rows in memory.
- Public/manuscript reporting should use family numbers and role labels.

## 8. Tools

- Path-independent scripts:
  - `06_tools/scripts/convert_all_docx_to_markdown.py`
  - `06_tools/scripts/refine_merged_transcripts_markdown.py`
  - `06_tools/scripts/standardize_merged_transcripts_markdown.py`
  - `06_tools/scripts/analyze_transcript_consistency.py`
- Legacy Windows-path scripts are in `06_tools/legacy_windows/`; they should be parameterized before reuse.
- `06_tools/reports/analysis_report_utf16.txt` is a prior UTF-16LE quality report.

## 9. Operational Notes

- This directory became writable by `mahirkurt` on 2026-05-04 after ownership/permissions were corrected.
- There is no package manifest, CI, test runner, deploy surface, or application runtime.
- `python-docx` was not available in the inspected Python environment; install it before running DOCX conversion scripts.
- Several scripts overwrite their target Markdown files; run them only after checking `00_context/file_manifest_after_reorg.tsv` or making a fresh backup.
