# Scripts

| Script | Produces | Run |
|---|---|---|
| `r1a_field_inventories.py` | `out/r1a/` (field inventories of the source study's files; 943-key list; preflight replication) | `git clone --depth 1 https://github.com/melificient/medAI.git` then `python r1a_field_inventories.py --repo medAI --out out/r1a` |
| `r1b_extract_one.py`, `r1b_aggregate.py` | `out/r1b/` (DEVICE-file join, fill rates, version-like token search, UDI-DI list) | For each DEVICE file 2013–2023: `python r1b_extract_one.py out/r1a/keys_943.csv device2019.zip parts/`; then `python r1b_aggregate.py out/r1a/keys_943.csv parts/ out/r1b` |
| `r1c_master_submission_field.py` | `out/r1c/` (MDR master-file scan: submission-number fill by year; the 943 master records) | `python r1c_master_submission_field.py out/r1a/keys_943.csv mdrfoithru2025.zip out/r1c`, then `python r1c_master_submission_field.py out/r1a/keys_943.csv --aggregate out/r1c` |
| `gudid_lookup.py` | `out/gudid/` (AccessGUDID resolution of the 39 UDI-DIs) | `python gudid_lookup.py out/r1b/udi_di_list_with_counts.csv gudid_lookup_results.csv` |
| `figures_manuscript.py` | Figures 1–2 and Supplementary Figures 1–2 (to `figures_out/`) | `python figures_manuscript.py` |
| `rerun_2026-09-26/r1a_field_inventories.py` | `results/final_2026-09-26/r1a_rerun_2026-09-26.json` (re-execution of the field inventories and preflight replication) | `python rerun_2026-09-26/r1a_field_inventories.py medAI` |

The master-file scan writes every column of the 943 master records; the deposited `out/r1c/master_extract_943.csv` keeps only the columns used in the analysis (see `PROVENANCE.md`).
