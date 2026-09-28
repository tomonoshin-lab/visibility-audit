# Data manifest

Large FDA downloads used by the audit scripts. The files themselves are not committed (`.gitignore`: `data/*.zip`); they are listed here with size, SHA-256, download timestamp (file modification time on the author's machine, JST), and source URL so that any run can be reproduced against the same release.

## MAUDE DEVICE files (used by r1b)

Source: FDA MAUDE data files, https://www.accessdata.fda.gov/MAUDE/ftparea/ (`device<year>.zip`). Downloaded 2026-09-02 (JST 19:41–19:43). SHA-256 as recorded in `out/r1b/MANIFEST_device_files_sha256.txt`:

| File | SHA-256 |
|---|---|
| device2013.zip | b0d308277a7d75502bcddfeed33dd684cebdc21b8dd3d191154694939c2ca0b5 |
| device2014.zip | c6a43c9008bf947543c636520e3d2dd5fa06f86c67374cdf83a75daf84b5ce0e |
| device2015.zip | 7388afe0ee29a13c3b06361a7df1afe7c72b83b5a427f0672395fce7884d1b79 |
| device2016.zip | e15612f179e5987a00aa145dc5720efd853f503613405303ca6fb75d6a226232 |
| device2017.zip | 208e39a444b691edaf3f958ba972ecc7be7d1aea99036ff00dcf3668a052c993 |
| device2018.zip | 32b08a97c4f0889b63003af0cc0f6d4a3f8cfeb1e6aa09d8f48ccda2bcd61783 |
| device2019.zip | ce058cfca6b9e80cc9e2cc5dcb57172361e73f9c385ba21c51638b112183743f |
| device2020.zip | 2a70246bbd75e69296edaf523f06436d54e414cf37616bb2818c4d035c52d12f |
| device2021.zip | 3f8502baa09a020b7340b64ae5ad78e361031c054d3df3289db8d3396481eb2f |
| device2022.zip | 4f057893c42d533c3a56c7d8dec15f3526574c8cc4ee3d291770281aea314128 |
| device2023.zip | 8d3fb8e41d29fdefdab39194b458142c1339768a714cd1240dd62ffe54e42b6b |

Each yearly DEVICE file has 34 pipe-delimited fields (`out/r1b/layouts.txt`).

## MAUDE MDR master files (used by r1c)

Source: FDA MAUDE data files, https://www.accessdata.fda.gov/MAUDE/ftparea/ .

| File | Size (bytes) | SHA-256 | Downloaded (JST) | Content |
|---|---|---|---|---|
| mdrfoi.zip | 75,643,290 | 1f9d136612fb6f67215b7ecc011937fb0be0c39f4a882ec2f18dee9e450407be | 2026-09-02 20:06 | current-year master (`mdrfoi.txt`, 730,177,164 bytes; 2,078,651 reports, all received 2026; FDA release dated 2026-08-04) |
| mdrfoithru2025.zip | 717,482,502 | f29f23e21fcee23937abbe01600484b45c1c4285c91e11cf618a96159bbf11a5 | 2026-09-02 20:16 | cumulative master through 2025 (`mdrfoiThru2025.txt`, 6,803,681,977 bytes; 23,636,517 reports) |

Both master files have 86 pipe-delimited fields (`out/r1c/layouts.txt`); `PMA_PMN_NUM` is field 81.

## Source-study replication repository (used by r1a)

`git clone --depth 1 https://github.com/melificient/medAI.git` → `data/medAI/` (files: `943_AEs_for_fda_devices.dta`, `raw/pmn96cur.xlsx`, `raw/fda_ai_devices_may2024.xlsx`). Not committed here; see `out/r1a/r1a_summary.json` for the computed subset.

## AccessGUDID (used by gudid_lookup.py)

API v3 lookups, https://accessgudid.nlm.nih.gov/api/v3/devices/lookup.json?di=<DI>, executed 2026-09-02 (JST 22:21–22:22) for the 39 distinct UDI-DIs; per-record `lookup_date` and `public_version_number`/`public_version_date` are in `out/gudid/gudid_lookup_results.csv`.

## Docket submission record

(to be filled after submission to FDA-2026-N-7874: date, Receipt/Tracking Number, Comment ID)
