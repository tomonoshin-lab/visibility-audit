#!/usr/bin/env python3
"""Extract DEVICE rows for the 943 keys from ONE MAUDE device file (used to run large files one at a time)."""
import sys, os, io, zipfile, pandas as pd
keys_path, dev_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out_dir, exist_ok=True)
keys = set(pd.read_csv(keys_path, dtype=str, keep_default_na=False)['mdr_report_key'].str.strip())
z = zipfile.ZipFile(dev_path); name = [n for n in z.namelist() if n.lower().endswith('.txt')][0]
fh = io.TextIOWrapper(z.open(name), encoding='latin-1', errors='replace')
cols = [c.strip().upper().replace(' ', '_') for c in fh.readline().rstrip('\r\n').split('|')]
out = []
for ch in pd.read_csv(fh, sep='|', names=cols, dtype=str, header=None, chunksize=250000, on_bad_lines='skip',
                      engine='c', quoting=3, keep_default_na=False, na_filter=False):
    m = ch[ch['MDR_REPORT_KEY'].str.strip().isin(keys)]
    if len(m): out.append(m)
df = pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=cols)
df['__source_file'] = os.path.basename(dev_path)
df.to_csv(os.path.join(out_dir, f"matched_{os.path.basename(dev_path).replace('.zip','')}.csv"), index=False)
with open(os.path.join(out_dir, 'layouts.txt'), 'a') as f: f.write(f"{os.path.basename(dev_path)}\t{len(cols)}\t{'|'.join(cols)}\n")
print(f"{os.path.basename(dev_path)}: {len(cols)} fields, {len(df)} matched rows")
