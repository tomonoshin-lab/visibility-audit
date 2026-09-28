# Codebook v1.4 addendum — classification by rule; the author's role; rules for boundary cases

Status: addendum to `codebook_v1.md` and addenda v1.1–v1.3. Written on 29 September 2026, **after** the confirmatory classifications were recorded (26 September 2026). It does not edit any earlier file: v1.0 (2 September 2026) and v1.1–v1.3 (3 September 2026) remain as fixed. It records the procedure that was followed and states, as rules, the boundary decisions that the recorded codes embody. Applying these rules to the recorded evidence reproduces every recorded code in `results/final_2026-09-26/`; no code changes.

## 1. Procedure (replaces the first paragraph of v1.3 §1)

v1.3 §1 stated that the confirmatory documentary judgments are made by the author alone. That statement is replaced as follows.

- Codes are assigned by applying the decision rules of v1.0, as clarified by v1.2 and by §2 below, to the recorded evidence: the field lists and layouts of each data source and the verbatim quotations logged for each document.
- The author's role is to fix the rules. Where the rules do not determine a unique code, the case is resolved by stating a new, dated rule that applies to every unit, not by a decision about the single case.
- Classification may be carried out with software, including an AI assistant. The documentary requirements of v1.3 §1 (source document, version or date, section, verbatim quotation of up to 40 words, rationale) apply to every code, so that any reader can re-apply the rules to the same evidence.

The single-judge wording of v1.3 is therefore superseded; the withdrawal of the second coder and of the v1.1 adjudication, and the outcome hierarchy of v1.3 §§2–3, stand.

## 2. Rules for boundary cases

Referent grade (C1):

- **B1. Free text.** A component is represented at R1 (mention) when free text that describes an individual report, device or submission, and that the data source distributes or displays, can carry its name, whether or not that text is searchable. Text that describes a device type (for example, a classification definition) does not describe any product's dependency and does not raise the grade.
- **B2. Linked documents.** A document held outside a database but linked to a record by a structured field (for example, the 510(k) summary linked through STATEORSUMM) counts as free text of that data source under B1.
- **B3. Class keys.** A code whose referent is a product counts as R2 for a shared component when a documented list, fixed before the analysis, maps product codes to the component and the surveillance query uses that list. Its reach is graded as for any R2 identifier.
- **B4. Premarket structured records.** A structured identifier or record of a component held only in premarket submissions or in a premarket reference file is R2 with Q0, because no event record reaches it.
- **B5. Documents that describe the model.** A plan, label, card or report whose documented content includes a description of the upstream model is R1. A procedure whose documented output is a product-level result (a benchmark, a review of sampled outputs, a performance-monitoring result) and does not record which component the product uses is R0.

Signal definition and scheduled review (C2, C3):

- **B6. Absent and Not documented.** Absent requires a documented signal-detection or review procedure with at least a defined unit, method, trigger or schedule that is not keyed to a shared component or does not concern adverse events; this includes procedures documented for another purpose, such as vulnerability management. A recommendation, question, statement of intent, data-access tool or one-off study without such a procedure is Not documented.
- **B7. Flags.** A document is flagged when it could be cited against a code of absence, for example because it names components or describes action or grouping across manufacturers.
- **B8. Data-source level.** The C2 or C3 code of a data source is the highest code among the documents logged for its surveillance program, in the order Present, Absent, Not documented. Identifier sources without a surveillance function are not coded (—).

## 3. Unchanged

The grade definitions (R, Q, I, C2a/b, C3a/b), the decision rules (a)–(d) of v1.0 §2, the definition of coverage in v1.2, and the outcome hierarchy of v1.3 §3 are unchanged.
