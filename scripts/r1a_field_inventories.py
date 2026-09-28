#!/usr/bin/env python3
"""r1a_field_inventories.py — computed subset of the schema audit.

Reproduces, end to end from the public replication repository of Babic et al. (2025),
  (1) the field inventories of three systems: the 943-report MDR master extract (15 fields),
      the 510(k) releasable database pmn96cur (22 fields), the FDA AI-enabled device list snapshot (6 fields);
  (2) the missingness replication under the source study's conventions
      (event location: blank or 'I' = No Information; health professional: blank or 'I';
       event date and reporter occupation: blank; event types M/IN/D);
  (3) S1 field-inventory rows for the three systems (designated meaning to be completed by the coder).

Usage:
  git clone --depth 1 https://github.com/melificient/medAI.git
  python r1a_field_inventories.py --repo medAI --out out_r1a
"""
import argparse, json, os, sys
import pandas as pd

def blank(s: pd.Series) -> pd.Series:
    return s.isna() | (s.astype(str).str.strip() == "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="path to the cloned melificient/medAI repository")
    ap.add_argument("--out", default="out_r1a")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    ae = pd.read_stata(os.path.join(a.repo, "943_AEs_for_fda_devices.dta"))
    k = pd.read_excel(os.path.join(a.repo, "raw", "pmn96cur.xlsx"), nrows=50)
    ai = pd.read_excel(os.path.join(a.repo, "raw", "fda_ai_devices_may2024.xlsx"), nrows=50)

    inventories = {
        "MDR master record (943-report extract)": list(ae.columns),
        "510(k) releasable database (pmn96cur)": list(k.columns),
        "FDA AI-enabled device list (May 2024 snapshot)": list(ai.columns),
    }
    rows = []
    for system, cols in inventories.items():
        for c in cols:
            rows.append({"system": system, "field_name": c, "designated_meaning": "", "data_type": "",
                         "referent_class": "", "structured": "", "controlled_values": "", "join_key_to": "",
                         "component_related": "", "source_doc": "Babic et al. repository", "notes": "computed"})
    pd.DataFrame(rows).to_csv(os.path.join(a.out, "S1_computed_fields.csv"), index=False)

    counts = {s: len(c) for s, c in inventories.items()}
    counts["total_fields"] = sum(len(c) for c in inventories.values())
    # structured upstream-component identifiers: none of the field names designates a component
    component_terms = ("model_id", "foundation", "component", "library", "upstream", "lineage", "sbom", "version")
    comp_fields = [c for cols in inventories.values() for c in cols if any(t in c.lower() for t in component_terms)]
    counts["structured_upstream_component_identifiers"] = len(comp_fields)
    counts["candidate_fields_matching_component_terms"] = comp_fields

    n = len(ae)
    ev_loc = ae["event_location"].astype(str).str.strip()
    hp = ae["health_professional"].astype(str).str.strip()
    repl = {
        "n_reports": n,
        "event_location_missing_blank_or_I": int(ev_loc.isin(["", "I"]).sum()),
        "health_professional_missing_blank_or_I": int(hp.isin(["", "I"]).sum()),
        "date_of_event_missing": int(blank(ae["date_of_event"]).sum()),
        "reporter_occupation_missing": int(blank(ae["reporter_occupation_code"]).sum()),
        "event_type_counts": ae["event_type"].value_counts().to_dict(),
        "date_received_years": pd.to_datetime(ae["date_received"], format="%m/%d/%Y", errors="coerce").dt.year.value_counts().sort_index().to_dict(),
        "unique_devices_idnumber": int(ae["idnumber"].nunique()),
        "mdr_report_key_unique": int(ae["mdr_report_key"].nunique()),
    }
    with open(os.path.join(a.out, "r1a_summary.json"), "w") as f:
        json.dump({"field_counts": counts, "missingness_replication": repl}, f, indent=2, default=str)
    ae[["mdr_report_key", "idnumber", "date_received"]].to_csv(os.path.join(a.out, "keys_943.csv"), index=False)
    print(json.dumps({"field_counts": counts, "missingness_replication": repl}, indent=2, default=str))
    print(f"\nwrote {a.out}/S1_computed_fields.csv, r1a_summary.json, keys_943.csv")

if __name__ == "__main__":
    main()
