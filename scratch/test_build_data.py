import sys, io, os, csv, json
from collections import defaultdict

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, 'data_sources')

def read_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding='utf-8-sig', errors='replace') as f:
        return list(csv.DictReader(f))

def safe_float(val, default=0.0):
    try:
        v = float(str(val).strip())
        return v if v == v else default
    except (TypeError, ValueError):
        return default

def normalize_cert(s):
    s = (s or '').strip().lower()
    if not s: return 'Unknown'
    if s in ('organic', 'orgainic'): return 'Organic'
    if s in ('new_organic', 'new organic', 'adhoc', 'ad hoc'): return 'New Organic'
    if s in ('ibis 1', 'ibis i', 'ibis1', 'ibis i', 'ibis i'): return 'Ibis I'
    if s in ('ibis 2', 'ibis ii', 'ibis2', 'ibis ii'): return 'Ibis II'
    if s in ('wf', 'wildlife friendly', 'wildlife-friendly'): return 'WF'
    return s.title()

def normalize_farmer_status(s):
    s = (s or '').strip().lower()
    if not s: return 'Unknown'
    if 'new' in s: return 'New'
    if 'rejoin' in s: return 'Rejoin'
    if 'existing' in s: return 'Existing'
    return s.title()

def main():
    sites_raw    = {r['site_id']: r   for r in read_csv('dim_site.csv')}
    villages_raw = {str(r['village_id']): r for r in read_csv('dim_village.csv')}
    farmers_list = read_csv('dim_farmer.csv')
    farmers_map  = {r['farmer_uid']: r for r in farmers_list}

    def farmer_site_id(uid):
        return farmers_map.get(uid, {}).get('site_id', '')

    def farmer_village_id(uid):
        return farmers_map.get(uid, {}).get('village_id', '')

    inspections  = read_csv('fact_afl_inspection.csv')
    
    # Check unique uids using interview_key
    print(f"Total rows in fact_afl_inspection: {len(inspections)}")
    unique_uids = set(r.get('interview_key', '') for r in inspections if r.get('interview_key'))
    print(f"Unique uids in fact_afl_inspection: {len(unique_uids)}")
    
    matched = sum(1 for uid in unique_uids if uid in farmers_map)
    print(f"Matched unique uids in dim_farmer: {matched}")

main()
