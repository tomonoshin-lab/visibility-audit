# Provenance

This repository is a curated deposit of the materials that support the manuscript. It was assembled on 27 September 2026 from the author's working record, which is a local version history begun on 2 September 2026. The working record also holds material not needed to check the manuscript: planning notes, draft field extractions and provisional grades prepared with an AI assistant (Claude, Anthropic) before the codebook was fixed, a draft classification of the 212 version-like token units prepared for the withdrawn adjudication, materials for the withdrawn second-coder procedure, figures of an earlier draft, and run logs. None of the draft material was treated as a judgment. The working record is retained by the author and is available to the journal's editors on request.

## Correspondence with the working record

| Item | Working record | Deposited as |
|---|---|---|
| Codebook, document register and blank templates fixed on 2 September 2026 (22:55 JST) | commit `a76bf07a77a187541a120a8054b4bcef7a29d692`, tag `v1.0-codebook` | `codebook/codebook_v1.md`, `codebook/document_register.md`, `codebook/templates_v1.0/` |
| Addendum v1.1 (3 September 2026, 08:06 JST) | commit `2018b6e`, tag `v1.1-codebook-addendum` | `codebook/codebook_v1.1_addendum_version_strings.md` |
| Addendum v1.2 (3 September 2026, 08:47 JST) | commit `1cf192d`, tag `v1.2-codebook-addendum` | `codebook/codebook_v1.2_addendum_referent_reach_coverage.md` |
| Addendum v1.3 (3 September 2026, 14:18 JST) | commit `70034df`, tag `v1.3-codebook-addendum` | `codebook/codebook_v1.3_addendum_single_coder.md`, `codebook/templates_v1.3/` |
| Computed outputs (2 September 2026) | `out/` at commit `65c2410` | `out/` (selected files; see below) |

The codebook files and blank templates are byte-identical to the files in the working record at the commits listed; their SHA-256 values are in `SHA256SUMS`. The SHA-256 of a Git bundle of the complete working record (all commits and tags) is:

`b2fba327d96882d2ace24cff1fa12f420591f026d32652ddb4a2d3f7b03233c4`

so that the record shown to editors can be checked against this deposit.

## Changes made in assembling this deposit

- `out/r1c/master_extract_943.csv` is a column subset of the 943 master records written by the master-file scan: report key, report number, dates received and changed, event type, submission number, exemption number and summary-report flag. The omitted columns include the names, addresses and telephone numbers of manufacturer contacts, which the analysis does not use; the full rows are reproduced by running `scripts/r1c_master_submission_field.py` on the FDA file.
- In the two run logs (`out/r1c/r1c_run_author_2026-09-02.log`, `out/gudid/gudid_run_author_2026-09-02.log`) the local directory path of the author's computer is replaced by `<author-dir>`; nothing else is changed.
- Outputs of the withdrawn second-coder procedure and figures of an earlier draft are not included.
