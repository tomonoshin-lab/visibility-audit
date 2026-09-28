#!/usr/bin/env python3
"""Aggregate per-file matched DEVICE rows (from r1b_extract_one.py) into the identity-audit outputs."""
import sys, os, re, glob, pandas as pd
keys_path, parts_dir, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out_dir, exist_ok=True)
PLACEHOLDER_NI = {"NI","NO INFORMATION","UNKNOWN","UNK","*","N/I","NOT AVAILABLE","UNAVAILABLE","UNKN"}
PLACEHOLDER_NA = {"NA","N/A","NOT APPLICABLE","N.A."}
TARGET = ["BRAND_NAME","GENERIC_NAME","MODEL_NUMBER","CATALOG_NUMBER","LOT_NUMBER","OTHER_ID_NUMBER","DEVICE_REPORT_PRODUCT_CODE","EXPIRATION_DATE_OF_DEVICE","UDI-DI","UDI-PUBLIC"]
VERSION_RE = re.compile(r"(?i)(?:\bv(?:er(?:sion)?)?\.?\s*\d+(?:\.\d+)+\b|\b\d+\.\d+(?:\.\d+)+\b|\brev(?:ision)?\.?\s*[A-Z0-9]+\b|\bversion\b|\bsw\s*\d|\bfirmware\b|\bsoftware\b)")
keys = pd.read_csv(keys_path, dtype=str, keep_default_na=False); keyset = set(keys['mdr_report_key'].str.strip())
dev = pd.concat([pd.read_csv(p, dtype=str, keep_default_na=False) for p in sorted(glob.glob(os.path.join(parts_dir,'matched_*.csv')))], ignore_index=True)
dev['MDR_REPORT_KEY'] = dev['MDR_REPORT_KEY'].str.strip()
dev['DEVICE_SEQUENCE_NO_num'] = pd.to_numeric(dev['DEVICE_SEQUENCE_NO'], errors='coerce')
dev = dev.sort_values(['MDR_REPORT_KEY','DEVICE_SEQUENCE_NO_num'])
mult = dev.groupby('MDR_REPORT_KEY').size()
dev1 = dev.drop_duplicates('MDR_REPORT_KEY', keep='first').copy()
dev.to_csv(os.path.join(out_dir,'matched_device_rows_all.csv'), index=False)
missing = sorted(keyset - set(dev1['MDR_REPORT_KEY']))
pd.DataFrame({'mdr_report_key': missing}).to_csv(os.path.join(out_dir,'reports_without_device_row.csv'), index=False)
def classify(v):
    s = str(v).strip().upper()
    if s == "": return "blank"
    if s in PLACEHOLDER_NI: return "placeholder"
    if s in PLACEHOLDER_NA: return "na_populated"
    return "populated"
n = len(keyset); rows=[]
for f in TARGET:
    cls = dev1[f].map(classify).value_counts().to_dict()
    pop=cls.get('populated',0); na=cls.get('na_populated',0)
    rows.append({'field':f,'n_reports':n,'reports_with_device_row':len(dev1),'populated':pop,'na_populated':na,
                 'blank':cls.get('blank',0)+(n-len(dev1)),'placeholder':cls.get('placeholder',0),
                 'fill_rate_incl_NA':round((pop+na)/n,4),'fill_rate_excl_NA':round(pop/n,4)})
fr=pd.DataFrame(rows); fr.to_csv(os.path.join(out_dir,'fill_rates.csv'), index=False)
# placeholder value census (what strings appear in the identifier fields)
census=[]
for f in ["MODEL_NUMBER","CATALOG_NUMBER","LOT_NUMBER","OTHER_ID_NUMBER","UDI-DI","UDI-PUBLIC"]:
    vc = dev1[f].str.strip().str.upper().value_counts().head(12)
    for val,c in vc.items(): census.append({'field':f,'value':val if val else '<blank>','count':int(c)})
pd.DataFrame(census).to_csv(os.path.join(out_dir,'value_census_top12.csv'), index=False)
vrows=[]
for f in ["MODEL_NUMBER","CATALOG_NUMBER","LOT_NUMBER","OTHER_ID_NUMBER","UDI-PUBLIC"]:
    vals = dev1[f].astype(str); nonblank = vals[vals.str.strip()!=""]
    hits = nonblank[nonblank.str.contains(VERSION_RE)]
    vrows.append({'field':f,'n_nonblank':int(len(nonblank)),'version_like_tokens':int(len(hits)),'share_of_nonblank':round(len(hits)/len(nonblank),4) if len(nonblank) else None,'examples':'; '.join(hits.head(8).tolist())})
pd.DataFrame(vrows).to_csv(os.path.join(out_dir,'version_pattern_scan.csv'), index=False)
u = dev1['UDI-DI'].str.strip(); u = u[(u!="") & ~u.str.upper().isin(PLACEHOLDER_NI|PLACEHOLDER_NA)]
pd.DataFrame({'udi_di':sorted(u.unique())}).to_csv(os.path.join(out_dir,'udi_di_list.csv'), index=False)
# per-device (idnumber) population of UDI-DI and per-year
dev1 = dev1.merge(keys[['mdr_report_key','idnumber','date_received']], left_on='MDR_REPORT_KEY', right_on='mdr_report_key', how='left')
dev1['year'] = pd.to_datetime(dev1['date_received'], format='%m/%d/%Y', errors='coerce').dt.year
by_year = dev1.groupby('year').apply(lambda g: pd.Series({'n':len(g),'udi_di_populated':int((g['UDI-DI'].map(classify)=='populated').sum()),'model_populated':int((g['MODEL_NUMBER'].map(classify)=='populated').sum()),'lot_populated':int((g['LOT_NUMBER'].map(classify)=='populated').sum())})).reset_index()
by_year.to_csv(os.path.join(out_dir,'fill_by_year.csv'), index=False)
by_dev = dev1.groupby('idnumber').apply(lambda g: pd.Series({'n_reports':len(g),'udi_di_populated':int((g['UDI-DI'].map(classify)=='populated').sum()),'distinct_model_numbers':g['MODEL_NUMBER'].str.strip().replace('',pd.NA).dropna().nunique(),'distinct_lot_values':g['LOT_NUMBER'].str.strip().replace('',pd.NA).dropna().nunique()})).reset_index().sort_values('n_reports',ascending=False)
by_dev.to_csv(os.path.join(out_dir,'fill_by_device.csv'), index=False)
with open(os.path.join(out_dir,'summary.txt'),'w') as fh:
    fh.write(f"reports: {n}; with DEVICE row: {len(dev1)}; without: {len(missing)}; reports with >1 device row: {int((mult>1).sum())}; max rows per report: {int(mult.max())}\n")
    fh.write(fr.to_string(index=False)+"\n\nversion-like tokens:\n"+pd.DataFrame(vrows).drop(columns=['examples']).to_string(index=False)+"\n")
    fh.write(f"\ndistinct UDI-DI values: {u.nunique()}\n")
print(open(os.path.join(out_dir,'summary.txt')).read())
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = fr
fig, ax = plt.subplots(figsize=(7,3.2))
ax.bar(d['field'], d['fill_rate_excl_NA'], color='#4C72B0', label='populated')
ax.bar(d['field'], d['fill_rate_incl_NA']-d['fill_rate_excl_NA'], bottom=d['fill_rate_excl_NA'], color='#DD8452', label="'Not applicable' (counted populated)")
ax.set_ylabel('share of 943 reports'); ax.set_ylim(0,1); ax.legend(frameon=False, fontsize=8)
plt.xticks(rotation=35, ha='right', fontsize=8); plt.tight_layout(); fig.savefig(os.path.join(out_dir,'fig2b_fill_rates.png'), dpi=300)
