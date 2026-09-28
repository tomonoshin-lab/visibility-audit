#!/usr/bin/env python3
"""gudid_lookup.py — resolve UDI-DIs in AccessGUDID (author's machine; needs internet; standard library only).

Usage: python gudid_lookup.py udi_di_list_with_counts.csv gudid_lookup_results.csv
API:   https://accessgudid.nlm.nih.gov/api/v3/devices/lookup.json?di=<DI>
Structure verified 2026-09-02 on DI 03573026359119: gudid.device.{brandName, versionModelNumber, companyName,
premarketSubmissions.premarketSubmission[{submissionNumber, supplementNumber}], productCodes.fdaProductCode[{productCode}],
lotBatch, serialNumber, manufacturingDate, expirationDate, donationIdNumber, deviceRecordStatus, publicVersionNumber, publicVersionDate}
and top-level productCodes[{regulationNumber, deviceClass}].
"""
import sys, csv, json, time, datetime, urllib.request, urllib.parse, urllib.error
src, dst = sys.argv[1], sys.argv[2]
with open(src, newline="", encoding="utf-8") as f:
    rows_in = list(csv.DictReader(f))
dis = [r["udi_di"].strip() for r in rows_in if r.get("udi_di", "").strip()]
extra = {r["udi_di"].strip(): r for r in rows_in}
today = datetime.date.today().isoformat()
FIELDS = ["udi_di", "n_reports", "idnumbers_in_source_study", "resolved", "http_status", "brand_name", "version_or_model", "catalog_number",
          "company_name", "submission_numbers", "supplement_numbers", "submission_matches_source_study", "product_codes", "regulation_number",
          "device_class", "pi_lot_batch", "pi_serial", "pi_manufacturing_date", "pi_expiration_date", "device_record_status",
          "public_version_number", "public_version_date", "device_publish_date", "lookup_date"]
out = []
for di in dis:
    rec = {k: "" for k in FIELDS}; rec.update({"udi_di": di, "resolved": "N", "lookup_date": today,
           "n_reports": extra.get(di, {}).get("n_reports", ""), "idnumbers_in_source_study": extra.get(di, {}).get("idnumbers", "")})
    url = "https://accessgudid.nlm.nih.gov/api/v3/devices/lookup.json?di=" + urllib.parse.quote(di)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "visibility-audit/1.0 (academic research)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            rec["http_status"] = r.status; data = json.loads(r.read().decode("utf-8"))
        g = (data.get("gudid") or {}).get("device") or {}
        if g:
            rec["resolved"] = "Y"
            rec["brand_name"] = g.get("brandName") or ""; rec["version_or_model"] = g.get("versionModelNumber") or ""
            rec["catalog_number"] = g.get("catalogNumber") or ""; rec["company_name"] = g.get("companyName") or ""
            subs = ((g.get("premarketSubmissions") or {}).get("premarketSubmission") or [])
            if isinstance(subs, dict): subs = [subs]
            rec["submission_numbers"] = ";".join(str(s.get("submissionNumber") or "") for s in subs)
            rec["supplement_numbers"] = ";".join(str(s.get("supplementNumber") or "") for s in subs)
            src_ids = set(x for x in rec["idnumbers_in_source_study"].split(";") if x)
            got = set(str(s.get("submissionNumber") or "").upper() for s in subs)
            rec["submission_matches_source_study"] = "Y" if src_ids & got else ("N" if got else "no_submission_in_gudid")
            codes = ((g.get("productCodes") or {}).get("fdaProductCode") or [])
            if isinstance(codes, dict): codes = [codes]
            rec["product_codes"] = ";".join(str(c.get("productCode") or "") for c in codes)
            for k_out, k_in in [("pi_lot_batch", "lotBatch"), ("pi_serial", "serialNumber"), ("pi_manufacturing_date", "manufacturingDate"),
                                ("pi_expiration_date", "expirationDate"), ("device_record_status", "deviceRecordStatus"),
                                ("public_version_number", "publicVersionNumber"), ("public_version_date", "publicVersionDate"),
                                ("device_publish_date", "devicePublishDate")]:
                rec[k_out] = "" if g.get(k_in) is None else str(g.get(k_in))
            top = data.get("productCodes") or []
            if top:
                rec["regulation_number"] = str(top[0].get("regulationNumber") or ""); rec["device_class"] = str(top[0].get("deviceClass") or "")
    except urllib.error.HTTPError as e:
        rec["http_status"] = e.code
    except Exception as e:
        rec["http_status"] = f"error: {e}"
    out.append(rec); print(di, rec["resolved"], rec["http_status"], rec["submission_numbers"], "lotBatch=" + rec["pi_lot_batch"]); time.sleep(0.5)
with open(dst, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(out)
n = len(out); res = sum(r["resolved"] == "Y" for r in out); sub = sum(bool(r["submission_numbers"]) for r in out)
cov = sum(int(r["n_reports"] or 0) for r in out if r["resolved"] == "Y")
print(f"\nresolved {res}/{n} DIs (covering {cov} reports); with submission number {sub}/{n}; source-study match {sum(r['submission_matches_source_study']=='Y' for r in out)}/{n}")
