#!/usr/bin/env python3
"""r1c_master_submission_field.py — population of the premarket submission number in the MDR master file (MDRFOI).

Run one yearly file at a time (foreground):  python r1c_master_submission_field.py keys_943.csv mdrfoi2019.zip out/r1c
Then aggregate:                               python r1c_master_submission_field.py keys_943.csv --aggregate out/r1c

Per file it records: the header (field names, count), the name of the PMA/510(k) field, the number of reports in the file,
the number with a populated submission number (population-wide fill), and the rows for the 943 keys (all columns).
Aggregation reports: population-wide fill per year; fill within the 943 (expected near 100% because the 943 were selected
by submission number — a selection effect that must be stated); agreement between field 80 and the source study's idnumber.
"""
import sys, os, io, glob, zipfile, json, pandas as pd
PLACEHOLDER = {"", "NI", "NA", "N/A", "*", "UNKNOWN", "UNK", "NONE"}
def find_col(cols):
    for c in cols:
        u = c.upper()
        if ("PMA" in u and ("PMN" in u or "510" in u)) or u in ("PMA_PMN_NUM", "PMA_PMN_NUMBER"):
            return c
    return None
def one(keys_path, path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    keys = set(pd.read_csv(keys_path, dtype=str, keep_default_na=False)["mdr_report_key"].str.strip())
    z = zipfile.ZipFile(path); name = [n for n in z.namelist() if n.lower().endswith(".txt")][0]
    fh = io.TextIOWrapper(z.open(name), encoding="latin-1", errors="replace")
    cols = [c.strip().upper().replace(" ", "_") for c in fh.readline().rstrip("\r\n").split("|")]
    sub = find_col(cols); n = 0; filled = 0; numbered = 0; exempt = 0; distinct = set(); matched = []; by_year = {}
    NUM = r"^(K|P|DEN|N|H|BK|BP|BN|D)\d{5,7}(\/S\d+)?$"
    for ch in pd.read_csv(fh, sep="|", names=cols, dtype=str, header=None, chunksize=250000, on_bad_lines="skip",
                          engine="c", quoting=3, keep_default_na=False, na_filter=False):
        n += len(ch)
        if sub:
            v = ch[sub].str.strip().str.upper()
            ok = ~v.isin(PLACEHOLDER); isnum = v.str.match(NUM); isex = v.str.startswith("EXEMPT")
            filled += int(ok.sum()); numbered += int(isnum.sum()); exempt += int(isex.sum()); distinct.update(v[isnum].unique().tolist())
            yr = pd.to_datetime(ch["DATE_RECEIVED"], format="%m/%d/%Y", errors="coerce").dt.year
            for y, g in pd.DataFrame({"y": yr, "ok": ok, "num": isnum}).groupby("y"):
                d = by_year.setdefault(int(y), {"reports": 0, "populated_any": 0, "populated_number": 0})
                d["reports"] += len(g); d["populated_any"] += int(g["ok"].sum()); d["populated_number"] += int(g["num"].sum())
        m = ch[ch["MDR_REPORT_KEY"].str.strip().isin(keys)]
        if len(m): matched.append(m)
    mdf = pd.concat(matched, ignore_index=True) if matched else pd.DataFrame(columns=cols)
    base = os.path.basename(path).replace(".zip", "")
    mdf.to_csv(os.path.join(out_dir, f"matched_{base}.csv"), index=False)
    rec = {"file": os.path.basename(path), "n_fields": len(cols), "submission_field": sub, "reports_in_file": n,
           "populated_any": filled, "populated_submission_number": numbered, "exempt": exempt,
           "fill_rate_any": round(filled / n, 4) if n else None, "fill_rate_number": round(numbered / n, 4) if n else None,
           "distinct_submission_numbers": len(distinct), "matched_943_rows": len(mdf), "by_year": by_year}
    with open(os.path.join(out_dir, "per_file.jsonl"), "a") as f: f.write(json.dumps(rec) + "\n")
    with open(os.path.join(out_dir, "layouts.txt"), "a") as f: f.write(f"{os.path.basename(path)}\t{len(cols)}\t{'|'.join(cols)}\n")
    print(rec)
def aggregate(keys_path, out_dir):
    keys = pd.read_csv(keys_path, dtype=str, keep_default_na=False); keys["mdr_report_key"] = keys["mdr_report_key"].str.strip()
    per = pd.read_json(os.path.join(out_dir, "per_file.jsonl"), lines=True).sort_values("file")
    per.to_csv(os.path.join(out_dir, "population_fill_by_year.csv"), index=False)
    parts = [pd.read_csv(p, dtype=str, keep_default_na=False) for p in sorted(glob.glob(os.path.join(out_dir, "matched_*.csv")))]
    m = pd.concat(parts, ignore_index=True); m["MDR_REPORT_KEY"] = m["MDR_REPORT_KEY"].str.strip()
    m = m.drop_duplicates("MDR_REPORT_KEY").merge(keys, left_on="MDR_REPORT_KEY", right_on="mdr_report_key", how="right")
    sub = find_col([c for c in m.columns])
    v = m[sub].fillna("").str.strip().str.upper() if sub else pd.Series([""] * len(m))
    populated = ~v.isin(PLACEHOLDER)
    agree = (v == m["idnumber"].str.strip().str.upper())
    summ = {"n_943": len(m), "master_rows_found": int(m[sub].notna().sum()) if sub else 0, "submission_field": sub,
            "populated_within_943": int(populated.sum()), "equals_source_study_idnumber": int((agree & populated).sum()),
            "note": "fill within the 943 is subject to selection on the key; use population_fill_by_year.csv for the representative rate"}
    json.dump(summ, open(os.path.join(out_dir, "summary_943.json"), "w"), indent=2)
    m[["MDR_REPORT_KEY", "idnumber", sub] if sub else ["MDR_REPORT_KEY", "idnumber"]].to_csv(os.path.join(out_dir, "field80_vs_idnumber.csv"), index=False)
    print(per.to_string(index=False)); print(json.dumps(summ, indent=2))
if __name__ == "__main__":
    if "--aggregate" in sys.argv: aggregate(sys.argv[1], sys.argv[3])
    else: one(sys.argv[1], sys.argv[2], sys.argv[3])
