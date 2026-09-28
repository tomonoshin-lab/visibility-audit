# Document register — sources for the S1/S2/S3 audits
Access each document, record the access date in the relevant sheet, and archive a copy (PDF/print-to-PDF) in `evidence/` named `<system>_<yyyymmdd>.pdf`. G0-verified items are marked ✔.

## A. Systems (S1 field inventories, S3 join keys, identity loci)
| System | Documents to read | What to extract | Status |
|---|---|---|---|
| MDR master record, DEVICE, PATIENT, TEXT files (MAUDE) | MAUDE data files page and file descriptions: https://www.fda.gov/medical-devices/mandatory-reporting-requirements-manufacturers-importers-and-device-user-facilities/manufacturer-and-user-facility-device-experience-database-maude ; yearly ZIPs `mdrfoiYYYY.zip`, `deviceYYYY.zip`, `patientYYYY.zip`, `foitextYYYY.zip` (2013–2023 needed for the 943 reports) | Field names and descriptions per file; `MDR_REPORT_KEY` join; DEVICE fields (MODEL_NUMBER, CATALOG_NUMBER, LOT_NUMBER, OTHER_ID_NUMBER, DEVICE_REPORT_PRODUCT_CODE, UDI-DI, UDI-PUBLIC) | Partially ✔ (via openFDA docs); confirm from FDA layout page |
| openFDA device/event | https://open.fda.gov/apis/device/event/ (searchable fields reference) | Field list (device.*, mdr_report_key, product_problems), confirms mirror | To do |
| MAUDE search interface | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfMAUDE/search.cfm | Searchable fields (product code/class, brand, manufacturer, product problem, event type, report number, PMA/510(k) number, UDI, dates) | Partially ✔ |
| AEMS device module | https://www.fda.gov/drugs/fda-adverse-event-monitoring-system-aems (device data migration; dashboard documentation; data download description) | Whether a device dataset/dashboard exists on the access date; its field list; any version/component field | To do (may not be live) |
| Product classification / product codes | FDA Product Classification database download `foiclass.zip` and page: https://www.fda.gov/medical-devices/classify-your-medical-device/product-code-classification-database | Fields (PRODUCTCODE, DEVICENAME, DEVICECLASS, REGULATIONNUMBER, …); referent = type | To do |
| 510(k) releasable database | `pmn96cur.zip` (already inventoried: 22 fields) and file description page | STATEORSUMM semantics; KNUMBER join | ✔ computed |
| GUDID / AccessGUDID | FDA GUDID Data Elements Reference Table PDF: https://www.fda.gov/media/120974/download ; AccessGUDID schema/download: https://accessgudid.nlm.nih.gov/download/schema | Element list; Version or Model Number; FDA Premarket Submission Number / Supplement Number; PI flags; absence of component/model elements | ✔ (element table to be archived) |
| AI-Enabled Medical Devices List | https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices (download CSV/XLSX) | 6 columns; update date; foundation-model tagging statement | ✔ (4 March 2026 update; 1,451 devices) |
| ONC HTI-1 source attributes | 45 CFR 170.315(b)(11)(iv): https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-170/subpart-C/section-170.315 ; ONC DSI fact sheet: https://www.healthit.gov/wp-content/uploads/2023/12/HTI-1_DSI_fact-sheet_508.pdf | 13 evidence-based / 31 predictive attributes; none is a registry key; no cross-product link | ✔ |
| Sentinel / BEST | Sentinel Common Data Model documentation (sentinelinitiative.org → Data → SCDM); BEST (CBER) program description | Exposure tables (dispensing NDC; procedure codes); whether any device identifier (UDI) table exists; documented joins to MDR/GUDID | To do |
| Form FDA 3500A / eMDR | Instructions: https://www.fda.gov/media/133177/download ; eMDR data elements (HL7 ICSR implementation) | Section D fields (D1–D4); no version field | ✔ (3500A); eMDR to do |

## B. Regulations and guidance cited for identity (S3 identity loci)
- 21 CFR 801.3 (lot or batch incl. software version) ✔ https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-801/subpart-A/section-801.3
- 21 CFR 820.3 (batch or lot; QMSR correction eff. 2 Feb 2026) ✔ https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820/subpart-A/section-820.3
- 21 CFR 801.50(a) (stand-alone software conveys version in PI) ✔ https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-801/subpart-B/section-801.50
- 21 CFR 830.50(a) (new DI on new version or model) ✔ https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-830/subpart-B/section-830.50

## C. Programs (S2 C2/C3 documentary search)
### C1. CDRH device postmarket signal management
Documents: MDR regulation 21 CFR Part 803 and MDR guidance for manufacturers; "Medical Device Reporting (MDR): How to Report Medical Device Problems"; CDRH postmarket surveillance program pages (Section 522, MedSun, NEST); "Strengthening Our National System for Medical Device Postmarket Surveillance" (2012) and update (2013); CDRH signal management/safety communications process descriptions; PCCP final guidance (Dec 2024); AI-enabled device software functions lifecycle draft guidance (Jan 2025); §524B cybersecurity guidance (2023); discussion paper FDA-2026-N-7874 §VI–VII.
Search terms: `component`, `shared`, `platform`, `class`, `class-level`, `aggregate`, `signal definition`, `signal detection`, `scheduled`, `quarterly`, `periodic`, `software version`, `version`, `third-party`, `foundation model`, `model`, `library`, `bill of materials`, `SBOM`, `UDI`.
### C2. FAERS/AEMS drug program (aligned comparator)
Documents: AEMS page and dashboard documentation ✔; FAERS ASCII data documentation (ASC_NTS) — `prod_ai` ✔; quarterly potential-signals page and Jan–Mar 2024 report ✔ (21 U.S.C. 355(k)(5)); CDER signal management descriptions (Office of Surveillance and Epidemiology).
### C3. VSD Rapid Cycle Analysis (aligned comparator, class key)
Documents: Goddard et al. 2022 (Vaccine 40:5153); VSD RCA protocol/methods reports (CDC ISO); CVX/MVX code set pages (CDC IIS).
### C4. §506K + FAERS/Sentinel, June–July 2025 (unaligned comparator)
Documents: FDA press release 18 Jul 2025; Sarepta community letter 19 Jul 2025; CBER safety communication 14 Nov 2025; §506K draft guidance (May 2024); Sentinel System Assessment 2022–2024 (2025); FAERS quarterly signals Q1 2025 (Elevidys entry).
### C5. §524B SBOM (partial comparator)
Documents: FD&C §524B; FDA cybersecurity premarket guidance (2023, SBOM section); CISA medical advisories (ICSMA) format; FDA cybersecurity safety communications (e.g., URGENT/11, 1 Oct 2019).

## D. Comparator sources already verified in G0
- FDAAA §921 → 21 U.S.C. 355(k)(5); Cures Act §3075 amended "bi-weekly screening" → "screenings" ✔
- Class-level rows, Jan–Mar 2024: GLP-1 receptor agonists; S1P receptor modulators; CGRP inhibitors ✔
- AEMS launch 11 March 2026; MAUDE migration planned mid-2026 ✔
