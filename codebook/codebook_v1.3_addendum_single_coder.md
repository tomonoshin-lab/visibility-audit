# Codebook v1.3 addendum — single-judge confirmatory design; withdrawal of the two-coder adjudication; outcome hierarchy

Status: addendum to `codebook_v1.md` (tag `v1.0-codebook`), `codebook_v1.1_addendum_version_strings.md` (tag `v1.1-codebook-addendum`) and `codebook_v1.2_addendum_referent_reach_coverage.md` (tag `v1.2-codebook-addendum`). It is fixed and committed **before** any confirmatory judgment is recorded in `templates/` (all judgment templates are blank at this commit). It changes the *procedure* by which judgments are made and verified. It changes no grading rule: the referent (R), reach (Q), identity (I), signal-definition (C2) and scheduled-review (C3) definitions of v1.0, as clarified by v1.2, stand unaltered, and so does the derived judgment used in Tables 2 and 3.

## 1. Single-judge confirmatory design

The confirmatory documentary judgments are made by the author alone. No second coder codes the material, and no inter-coder agreement statistic (raw agreement, Cohen's κ, Gwet's AC1) is computed or reported.

Verification is documentary instead of statistical. Every judgment row must carry, in addition to the grade:

- `source_docs` — the primary document relied on, by title and stable URL;
- `source_version_or_date` — its version, revision date, or the date on which the page was current;
- `section` — the section, table, or field list examined;
- `evidence_quote` — the text on which the grade rests, quoted verbatim (≤ 40 words) or, for a field list, the field names as published;
- `rationale` — one sentence connecting the quoted text to the grade;
- `judged_by`, `date` — the person and the date of the judgment.

A grade with no `evidence_quote` and no `section` is not recorded. The requirement is that a reader who disagrees with a grade can open the same document at the same place and record a different grade; that possibility, not an agreement coefficient, is what this design offers as verification.

Templates changed accordingly at this commit (blank): `S1_grades.csv`, `S2_c2c3_log.csv`, `S3_joinkeys.csv` gain `source_version_or_date`, `section`, `evidence_quote`, and rename `coder` to `judged_by`.

## 2. Withdrawal of the v1.1 adjudication procedure

The v1.1 addendum specified a four-class classification (V confirmed / P probable / A ambiguous / N not a version) of the 212 report–field units matched by the heuristic version-string detection, to be applied by two coders independently and then adjudicated. Blindness between coders is constitutive of that procedure; a single judge cannot execute it as specified. The procedure is therefore **withdrawn, not executed by one judge**, and no adjudicated class is reported for any unit.

What is reported instead:

- The detection itself, which is a deterministic computed output of `scripts/r1b_aggregate.py` (regular expression over MODEL_NUMBER, CATALOG_NUMBER, LOT_NUMBER, OTHER_ID_NUMBER, and the GS1 (10) segment of UDI-PUBLIC; first DEVICE row per report): 137 of 943 reports, 212 report–field units, distributed over four fields.
- All 212 units, already deposited verbatim with their field of origin in `out/r1b/version_strings_137_units.csv` (columns: `unit_id`, `mdr_report_key`, `idnumber`, `brand_name`, `field`, `field_value`, `matched_strings`), so that any reader can inspect them and classify them independently. This file is Supplementary Table S3's version-string component; no separate judgment template is created for it.

The count is reported as a heuristic detection over free-form identifier fields. It is **not** an estimate of the prevalence of software-version reporting: a matched string need not be a version, and a version written without a dotted numeral or a keyword is not matched. The finding the manuscript draws from it is the distribution across four fields that designate something else, which does not depend on the class of any individual unit.

`scripts/reliability.py`, `scripts/make_coderB_sheet.py`, `out/r1b/S3_version_strings_coding_sheet_blind.csv`, `templates/S3_version_strings_coding_sheet.csv` and `templates/S4_coding_sheet.csv` are retained in the repository for provenance and are not used in this analysis. `CODER_B_INSTRUCTIONS.md` is removed at this commit; it remains in the repository history.

## 3. Outcome hierarchy

Primary outcomes, each resting on a published layout, a public export, or a computed file:

1. the referent grade R of the structured identifiers each audited system exposes;
2. the reach grade Q of those identifiers;
3. the existence of a documented deterministic path from a postmarket event record to an upstream component (joinability audit), with coverage reported separately as defined in v1.2;
4. the record-level identity grade I at the four loci.

Secondary outcomes: the signal-definition (C2a/b) and scheduled-review (C3a/b) conditions. They rest on a search of published program documentation, in which a negative finding is weaker evidence than a field missing from a published layout, and the conclusions drawn from the primary outcomes do not depend on how they are scored.

This ordering is adopted at this revision, after the conditions had been scored in draft form in `drafts/` and before any confirmatory judgment is recorded in `templates/`. It reflects the evidence available for each condition, not the order in which they were examined, and is recorded here so that the distinction is dated rather than asserted after the fact.

## 4. Minimum confirmatory set

Before the manuscript is submitted, the following must be recorded in `templates/` under §1, from primary documents:

- `S0_system_inclusion.csv` — the two-tier universe with every exclusion and its reason;
- `S1_field_inventory.csv` and `S1_grades.csv` — the seven core surveillance systems and the adjacent disclosure scheme, plus the comparators;
- `S3_joinkeys.csv` and `S3_coverage.csv` — every documented join key used in the reachability claim, with `semantics_fixed` and the coverage quantities;
- `S2_c2c3_log.csv` — the secondary documentary search, with search terms and the sections examined;
- `evidence/` — an archived copy (PDF or saved page) of every document a row relies on, named `<system>_<yyyymmdd>.pdf`.

No claim graded in the manuscript may rest on a document that has no row in these files.

## 5. Provenance note

The instrument was developed iteratively during exploratory review of the audited systems; v1.0 froze the coding rules and the blank templates before confirmatory documentary coding. v1.1 and v1.2 clarified rules before any judgment was recorded. This addendum changes the confirmatory procedure, again before any judgment is recorded, and is dated by its commit. The change is a consequence of resource availability, not of any result: no confirmatory judgment existed when it was made.
