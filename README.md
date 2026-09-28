# visibility-audit

Materials that support the manuscript "US medical device surveillance cannot retrieve adverse events across products sharing a foundation model: an audit of identifier schemas and record linkage" (T. Aoki; under peer review): the codebook fixed before any confirmatory judgment, the recorded judgments with their sources, the computed record-linkage outputs and the code that produced them.

| Path | Content | Manuscript |
|---|---|---|
| `codebook/codebook_v1.md`, `codebook/document_register.md`, `codebook/templates_v1.0/` | Codebook, document register and blank judgment templates, fixed on 2 September 2026 before any confirmatory judgment | Methods (Study design) |
| `codebook/codebook_v1.1_…`, `codebook/codebook_v1.2_…`, `codebook/codebook_v1.3_…`, `codebook/templates_v1.3/` | Three addenda fixed on 3 September 2026 (Japan Standard Time); v1.3 replaced the second-coder design of v1.0 with single-author verification, withdrew the adjudication of version-like tokens specified in v1.1 and fixed the outcome hierarchy, while all judgment templates were blank | Supplementary Methods |
| `results/final_2026-09-26/` | Recorded judgments and tabulations, with a file-by-file map to the manuscript's tables and the correspondence between the manuscript's grades and the codebook | Tables 1–2; Supplementary Tables 1–6 |
| `CHANGELOG_2026-09-26.md` | Judgments changed after they were recorded | Supplementary Methods (deviations) |
| `out/` | Computed outputs: field inventories (`r1a`), DEVICE-file join and version-like token search (`r1b`), MDR master-file scan (`r1c`), AccessGUDID resolution (`gudid`) | Results; Supplementary Table 3 |
| `scripts/` | Code that produced `out/` and the figures | Supplementary Note 1 |
| `data/MANIFEST.md` | Download locations and SHA-256 hashes of the FDA files used; the files are not redistributed | Supplementary Note 1 |
| `PROVENANCE.md` | How this deposit relates to the author's full working record | — |

Where a codebook file refers to other files (for example draft folders, coding sheets for a second coder, or reliability scripts), those files belonged to procedures that were withdrawn or superseded and are not part of this deposit; see `PROVENANCE.md`.

## Reproducing the computed outputs

See `scripts/README.md`. The source study's replication files are at https://github.com/melificient/medAI; the FDA files are listed with their hashes in `data/MANIFEST.md`.

## Licence and citation

Documentation and data: CC BY 4.0. Code: MIT. See `LICENSE.md`. Cite as in `CITATION.cff`. Release v1.0 is archived on Zenodo: https://doi.org/10.5281/zenodo.23016647 (all versions: https://doi.org/10.5281/zenodo.23016646).
