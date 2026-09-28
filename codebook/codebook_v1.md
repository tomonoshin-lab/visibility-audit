# Codebook v1.0 — Alignment audit of US device-surveillance schemas
Version 1.0 · To be committed to the public repository BEFORE any judgment is recorded (record the commit hash in Methods).
Any change after judgments begin creates v1.1 with a dated change note; no retroactive edits.

## 0. Units of judgment
| Supplementary table | Unit | Coders |
|---|---|---|
| S1 field inventory | (system, file/table, field) | A (computed or documentary) |
| S1 grades | system | A, B independently → adjudication |
| S2 C2/C3 | surveillance program (CDRH device program; each comparator program) × sub-condition | A, B independently → adjudication |
| S3 join keys / reachability | (from_system, from_field, to_system, to_field) | A; B checks a random 30% |
| S3 identity loci | (locus, file family) | A, B independently |

"Publicly documented" means: a layout document, data dictionary, schema, form instruction, regulation, guidance, or dashboard documentation published by the operating body and accessible without login on the access date. Undocumented internal functions are out of scope and are never inferred.

## 1. Terms
- **Upstream component**: a model, library, vector, or other artifact incorporated into more than one regulated product and not itself the regulated product (e.g., a foundation model, an ML library, an AAV capsid).
- **Structured identifier**: a field with a designated meaning and a value space constrained enough for equality-based linkage (codes, controlled vocabulary, numbered identifiers with fixed format). Free text is not structured even if it usually contains a name.
- **Semantically designated**: the field's documented meaning is the referent in question (e.g., "software version" is designated; "lot number" that may lawfully contain a version is not).
- **Referent class** of an identifier (record one per structured identifier): `report` · `article` (marketed device/model/catalog/lot/UDI-DI) · `type` (product code, classification) · `submission` (K/P/DEN number, MAF number) · `component` · `establishment` · `other`.
- **Deterministic hop**: a join that uses a structured key with fixed semantics on both sides. A hop through free text, attached PDFs, or manual lookup is non-deterministic.

## 2. Key condition C1 — referent grade R (per system)
Assign the highest grade supported by documentation.
| Grade | Rule | Examples |
|---|---|---|
| **R2** | At least one structured identifier whose designated meaning is an upstream component (or a component version), with constrained values | MAF file number (names the model file); SBOM component entries; `prod_ai` (active ingredient) |
| **R1** | A component can appear only in free-text fields or attached documents | 510(k) summary PDFs; MDR narrative text; HTI-1 source-attribute text |
| **R0** | No representation of a component in any form | 15-field MDR master extract; AI device list (6 fields) |
Decision rules: (a) a boolean flag ("uses AI", "incorporates a foundation model") is R0 — it does not name the component; (b) a structured identifier of the wrong referent (article, type, submission) is R0 for C1 — record its referent in S1; (c) a field that *may* contain a component name without designation (e.g., "other identifier") is R1; (d) grade the system as documented on the access date; note announced changes separately.

## 3. Key condition C1 — reach grade Q (only when R2)
| Grade | Rule | Evidence required |
|---|---|---|
| **Q0** | The identifier is local to one record or submission; no documented index or query returns all products sharing it | MAF (reference by authorization, per submission); SBOM (per submission) |
| **Q1** | A documented query, index, or download returns all regulated products sharing the identifier | Dashboard/search field documented for the key; downloadable index keyed on it |
| **Q2** | Q1 and the key is carried in, or joins deterministically to, postmarket event records | Event-record layout includes the key (`prod_ai` in FAERS/AEMS DRUG); or a documented deterministic join chain to it |
C1 is met iff R2 ∧ Q≥1. Horizontal event aggregation requires R2 ∧ Q2. For R0/R1 systems, Q is "—".

## 4. Signal definition (C2) and scheduled review (C3) — program level
Score once for the CDRH device postmarket signal-management program and once per comparator program.
| Sub-condition | Present | Partial | Absent |
|---|---|---|---|
| **C2a** component-class signal definition stated in advance | A published definition of a hazard over the class of products sharing a component (case definition, risk window, or equivalent) | Generic criteria applied class-wide (e.g., disproportionality thresholds) or definitions published by another body (e.g., CISA advisories) | No such definition found after the documented search |
| **C2b** bound to a structured key | The definition names/uses an R2 key | — | No key, or key not R2 |
| **C3a** scheduled review at component-class unit | A documented recurring schedule (weekly/quarterly/statutory) that reviews component-class aggregates | Recurring review exists but component-class aggregation is optional/ad hoc | Review is event-triggered or product-level only |
| **C3b** consumes key-based aggregates | Documentation shows aggregates keyed on the R2 identifier enter the scheduled review | — | Otherwise |
Search protocol (S2): for each program, search the document set in `document_register.md` with the term list there; log document title, version/date, URL, access date, search terms, section examined, judgment, rationale. "Absent" may only be recorded after all listed documents have been searched and logged.

## 5. Record-level identity — grade I (per file family, at four loci)
Loci: (a) reporter submission (Form FDA 3500A / eMDR data elements); (b) agency-held record (documented only through published layouts; never inferred); (c) public export (MAUDE/AEMS files); (d) public query interface.
| Grade | Rule |
|---|---|
| **I0** | No device-identifying field in the record |
| **I1** | Structured identity of the marketed article (brand, model, catalog, serial, lot, UDI-DI) |
| **I2** | A software version is capturable only inside multi-purpose fields whose designated meaning is not version (lot/batch per 21 CFR 801.3; UDI production identifier per 21 CFR 801.50(a)); no designated version field, no fixed format, no retrieval by version |
| **I3** | A designated, normalized software-version field exists |
| **I4** | Identity of the deployed configuration as a whole (e.g., a fingerprint over composed elements) |
Fill-rate conventions (secondary construct, mirrors the source study): blank/NaN and "No Information" placeholders (`NI`, `NO INFORMATION`, `UNKNOWN`, `UNK`, `*`) count as missing; `NA`, `N/A`, `NOT APPLICABLE` count as populated and are reported separately. Fill rates bound identity from above; no inference from population to version identifiability.

## 6. Join keys and reachability (S3)
Record an edge only when both endpoints are documented fields. Mark `structured=Y` only for deterministic hops (Section 1). Origin for reachability = MDR master record (and the AEMS device master when available). Report: reachable set via structured edges; longest deterministic path; terminal node before any hop toward a component becomes non-deterministic or absent.

## 7. Worked examples (from the computed subset and G0-verified sources)
- MDR master extract (15 fields): R0; identity I0; join key `MDR_REPORT_KEY` → DEVICE/TEXT.
- MDR DEVICE file: R0 (structured identifiers: article); I2 (lot/UDI may carry a version by 801.3/801.50(a)); narratives R1.
- 510(k) releasable DB (22 fields): R1 via `STATEORSUMM`-located summaries; referent: submission.
- AI-enabled device list (6 fields): R0; the announced foundation-model "tag" would remain R0 (flag, not identifier).
- GUDID: R0; referent article; join keys UDI-DI, FDA Premarket Submission Number.
- Foundation Model MAF (as described): R2, Q0; C2a/C3a absent.
- §524B SBOM: R2, Q0; C2a partial (advisories), C2b absent, C3a absent.
- FAERS/AEMS `prod_ai`: R2, Q2; C2a partial, C2b present; C3a present (21 U.S.C. 355(k)(5) quarterly), C3b present.
- CVX/MVX + VSD: R2 as a class key (record caveat), Q2; C2a/b present; C3a/b present.
- §506K + FAERS/Sentinel (June–July 2025): R0 for the vector (text only); C2a/C3a absent.

## 8. Coder procedure
1. Both coders receive codebook v1.0, `document_register.md`, and the S1 field inventories; they do not discuss judgments until both sheets are submitted.
2. Each judgment carries a rationale citing the document and section.
3. Adjudication: disagreements resolved by discussion with the codebook rule cited; the adjudicated value and note go to S4. If a rule is found ambiguous, the codebook is versioned (v1.1) and both coders re-code the affected units.
4. Reliability: raw agreement, Cohen's κ, and Gwet's AC1 per item and overall (`scripts/reliability.py`).
