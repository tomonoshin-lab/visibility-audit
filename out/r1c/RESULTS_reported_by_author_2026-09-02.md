# r1c results (author run, 2026-09-02 JST 21:38–21:54; Anaconda Python 3.12.4, pandas 2.2.2)
Input: mdrfoithru2025.zip (717 MB) → mdrfoiThru2025.txt (6.80 GB), streamed. Scan 947.7 s; aggregate 3.4 s.
Layout: 86 fields; PMA_PMN_NUM = field 81 (field 80 = REPORTER_COUNTRY_CODE; 82 EXEMPTION_NUMBER; 83–86 SUMMARY_REPORT, NOE_SUMMARIZED, SUPPL_DATES_FDA_RECEIVED, SUPPL_DATES_MFR_RECEIVED).
Population (23,636,517 reports): fill_any 0.7718; regulatory-format 0.7269; EXEMPT* 556,123; other non-conforming 506,118; distinct numbers 36,518; 3,341 rows with unparseable DATE_RECEIVED.
By year (regulatory-format): ≤2005 0.00025; 2006 0.128; 2007 0.392; 2010 0.628; 2013 0.677; 2016 0.757; 2020 0.749; 2023 0.789; 2025 0.800.
2013–2023 window: 15,463,770 reports; fill_any 0.7946; regulatory-format 0.7505.
943 subset: master rows 943/943; DATE_RECEIVED identical 943/943; PMA_PMN_NUM populated 943/943 (selection on key); equals Babic idnumber 913/943 (96.8%); 30 disagreements all within-manufacturer 510(k) succession (one family 25; another 5); all 943 rows DATE_CHANGED 2025-07…2026-01 (bulk rebuild). EXEMPTION_NUMBER 0/943; SUMMARY_REPORT Y 1/943.
Files to add to the repository: out/r1c/{per_file.jsonl, matched_mdrfoithru2025.csv, layouts.txt, population_fill_by_year.csv, summary_943.json, field80_vs_idnumber.csv}
