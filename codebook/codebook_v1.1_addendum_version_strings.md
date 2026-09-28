# Codebook v1.1 addendum — adjudication of version-like strings in MDR DEVICE identifier fields

Status: addendum to `codebook_v1.md` (tag `v1.0-codebook`), fixed and committed **before** any classification of the matched strings is recorded. It does not change any rule in v1.0; it adds the classification rule for one computed output.

## Object
The heuristic detection in `scripts/r1b_aggregate.py` (regular expression over MODEL_NUMBER, CATALOG_NUMBER, LOT_NUMBER, OTHER_ID_NUMBER, UDI-PUBLIC; first DEVICE row per report) flags 137 of the 943 reports and 212 report–field units (`out/r1b/version_strings_137_units.csv`). Because dotted numerals can also be model or catalog designations, each unit is classified by two coders independently, blind to each other and to the LLM-assisted draft in `drafts/`, using `out/r1b/S3_version_strings_coding_sheet_blind.csv` (template: `templates/S3_version_strings_coding_sheet.csv`).

## Unit
One report–field pair (`unit_id` = `<MDR_REPORT_KEY>:<field>`). The report-level class is the strongest class among its units (V > P > A > N).

## Classes (mutually exclusive)
- **V — confirmed version.** The field value contains an explicit version marker attached to a numeral or token: the words *version*, *ver*, *v* + number, *SW*, *software*, *firmware*, *rev*/*revision*; or the GS1 (10) lot segment of the public UDI carries a token that names a software product followed by a numeral (e.g., `(10)FFRCT_2.60.1.1`); or a version identifier that the labeler's own GUDID record designates as a software version (`out/gudid/gudid_lookup_results.csv`, `version_or_model`).
- **P — probable version.** A dotted numeral with three or more components (x.y.z…) in a field of a device whose marketed article is software (SaMD, PACS, planning or analysis software), with no evidence that the numeral is a model or catalog designation.
- **A — ambiguous.** A dotted numeral that could equally be a model, catalog, or part designation (hardware devices; numerals resembling sizes, dates, or part numbers), or a *rev* token that may denote a hardware revision.
- **N — not a version.** The pattern matched but the value is clearly not a software version (e.g., a measurement, a date, a lot code with dots).

## Procedure
1. Coder A and coder B classify every unit independently (`coder_A`/`coder_B`, with a one-line rationale each).
2. Agreement is computed with `scripts/reliability.py` (raw agreement, Cohen's κ, Gwet's AC1) at the unit level.
3. Disagreements are adjudicated jointly; the adjudicated class and note are recorded (`adjudicated`, `adjudication_note`).
4. Reported quantities: units and reports by adjudicated class; the count of reports with at least one V or P unit is the **adjudicated count of undesignated version capture**; the 137 remains the heuristic upper bound and the V-only count the lower bound.

## Relation to the manuscript
Results (identity section) reports the adjudicated counts alongside the heuristic count; Methods (identity audit) cites this addendum and its commit hash; Supplementary Table S3 deposits the full sheet.
