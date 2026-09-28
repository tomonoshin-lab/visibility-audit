"""R1a executed subset: field inventories + missingness replication.

Runs entirely from the public replication repository of Babic et al.
(npj Digit Med 8:328, 2025): https://github.com/melificient/medAI
Outputs: field inventories for (i) the 943-report MDR master extract,
(ii) the 510(k) releasable database (pmn96cur), (iii) the FDA
AI-enabled device list snapshot; and an exact replication of the
published blank-entry counts, run as a preflight check before the
identity audit. Deposit output as Supplementary Table S1 (part).
"""
import pandas as pd, json, sys, datetime

REPO = sys.argv[1] if len(sys.argv) > 1 else "medAI-main"

ae  = pd.read_stata(f"{REPO}/943_AEs_for_fda_devices.dta")
pmn = pd.read_excel(f"{REPO}/raw/pmn96cur.xlsx", nrows=5)
ai  = pd.read_excel(f"{REPO}/raw/fda_ai_devices_may2024.xlsx", nrows=5)

IDENT_TOKENS = ("model", "catalog", "lot", "udi", "version", "brand", "device_id", "serial")
def identity_like(cols):
    return [c for c in cols if any(t in c.lower() for t in IDENT_TOKENS)]

def blank(s):
    x = s.astype(str).str.strip().str.lower()
    return int(((x == "") | (x == "nan") | (x == "nat") | (x == "none")).sum())

def coded_no_info(s):
    # MAUDE codes "No Information" as the literal code "I" in these fields
    return int((s.astype(str).str.strip().str.upper() == "I").sum())

report = {
    "run_date": str(datetime.date.today()),
    "master_extract": {
        "n_reports": int(len(ae)),
        "n_fields": int(len(ae.columns)),
        "fields": list(ae.columns),
        "identity_like_fields": identity_like(ae.columns),  # expected: []
    },
    "pmn96cur_510k_releasable": {
        "n_fields": int(len(pmn.columns)),
        "fields": list(pmn.columns),
        "identity_like_fields": identity_like(pmn.columns),
        "component_fields": [],  # no field names any incorporated component
    },
    "fda_ai_device_list": {
        "n_fields": int(len(ai.columns)),
        "fields": list(ai.columns),
        "upstream_model_field": None,  # no such field in the schema
    },
    "missingness_replication": {
        # missing = blank + coded "I" (No Information); mirrors Babic et al.
        "event_location_missing": blank(ae["event_location"]) + coded_no_info(ae["event_location"]),            # expected 943 (369 blank + 574 I)
        "health_professional_missing": blank(ae["health_professional"]) + coded_no_info(ae["health_professional"]),  # expected 690 = 73% (509 blank + 181 I)
        "date_of_event_missing": int(pd.to_datetime(ae["date_of_event"], errors="coerce").isna().sum()),  # expected 298 = 32%
        "reporter_occupation_missing": blank(ae["reporter_occupation_code"]),  # expected 283 = 30%
        "event_type_split_M_IN_D": ae["event_type"].astype(str).value_counts().to_dict(),  # expected 857/84/2
    },
}
print(json.dumps(report, indent=2))
