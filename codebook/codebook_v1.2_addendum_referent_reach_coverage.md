# Codebook v1.2 addendum — referent rule for dossier and class keys; reach versus coverage

Status: addendum to `codebook_v1.md` (tag `v1.0-codebook`) and `codebook_v1.1_addendum_version_strings.md` (tag `v1.1-codebook-addendum`), fixed and committed **before** any judgment is recorded in `templates/` (all judgment templates are blank at this commit). It clarifies two rules whose v1.0 wording was found ambiguous during external review of the manuscript, per §8.3 of v1.0 ("if a rule is found ambiguous, the codebook is versioned and both coders re-code the affected units"). No judgment values are supplied here.

## 1. Referent grade R — dossier references and class keys are not component identifiers

R2 requires a structured identifier whose *designated* referent is an upstream component or a component version (v1.0 §1 "semantically designated"; §2). Two cases are clarified:

- **Dossier reference.** A structured identifier whose designated referent is a file, dossier, or submission that *describes* a component (e.g., a Foundation Model Master File number) has referent class `submission`, not `component`, unless the governing description defines the identifier as a stable identifier of one specific component version. As described in the FDA discussion paper, the MAF number is therefore **not R2** ("structured dossier identifier; one-to-one identity with a model version not specified"). The v1.0 §2 example "MAF file number (names the model file)" and the §7 worked example "Foundation Model MAF (as described): R2, Q0" are superseded by this rule. Q is still recorded for the identifier (it is structured), so the MAF profile becomes: R = not R2 (dossier reference), Q = Q0.
- **Class key.** A structured identifier whose designated referent is a class or type of product (e.g., a CVX vaccine-type code, a product code) is not a component identifier. When a comparator is scored on such a key, R is recorded as **n/a (class key)** rather than R2, and the comparator is used to check reach (Q), C2, and C3 only. The v1.0 §7 example "CVX/MVX + VSD: R2 as a class key" is superseded: record `n/a (class key)`, Q2, C2a/b present, C3a/b present.

`templates/S1_grades.csv`: the `R_grade` column accepts `R0`, `R1`, `R2`, or `n/a (class key)`; for a dossier reference record `R0/R1 as applicable` with the note "structured dossier reference; not R2" and the referent class `submission` in `referent_of_structured_identifiers`.

## 2. Reach grade Q — schema-level property; deterministic hop requires referential stability

Q is graded on the **documented schema**. A hop is deterministic (v1.0 §1) only if it uses a structured key with fixed semantics on both sides **and** the same key value names the same object in both systems (referential stability). A key that names one point in a succession of objects (e.g., a premarket submission number naming one clearance in a device family's succession of clearances), where the two systems may anchor to different points, is recorded in `templates/S3_joinkeys.csv` with `semantics_fixed = N` and a note; such a hop does not support Q2.

Q2 therefore means: the key is carried in the postmarket event record, or a documented chain of deterministic hops (as just defined) reaches it from the event record.

## 3. Coverage — a separate record-level quantity, never folded into Q

**Coverage** is the share of event records for which a documented path can actually be traversed. It is bounded above by (a) the population of each joining key in the event records and (b) the agreement of the key's values across the joined systems. Coverage is recorded in `templates/S3_coverage.csv` (new in this addendum; columns: `path`, `hop`, `key`, `population_pct`, `population_basis`, `agreement_stat`, `agreement_basis`, `source`, `notes`) and reported alongside the Q grade. It does not enter the Q grade or the derived judgment of Table 2.

Computed values already deposited (no judgment involved): premarket submission number populated in 75.1% of 2013–2023 MDR master reports (`out/r1c/population_fill_by_year.csv`); UDI-DI populated in 446/943 (47.3%) of the source-study reports (`out/r1b/`); GUDID submission number present for 21/38 resolved identifiers and differing from the master file's for 10/21 (`out/gudid/`).

## 4. Derived judgment (Table 2 rule) — unchanged in substance, restated

A mechanism closes the lineage gap iff it introduces or requires a component identifier at R2 that is deterministically reachable from postmarket event records (Q2), directly or through documented deterministic hops as defined in §2. Coverage is reported separately and does not enter the judgment.

## 5. Provenance note

The instrument was developed iteratively during exploratory review of the audited systems; v1.0 froze the formal coding rules and blank templates before confirmatory documentary coding. This addendum is committed before any confirmatory judgment is recorded and is dated by its commit. The docket comment (FDA-2026-N-7874) places the Table 2 rule on a dated public record; that timestamp dates the decision rule for scoring subsequent agency documents and is not a preregistration of the audit, part of whose computed subset preceded the comment.
