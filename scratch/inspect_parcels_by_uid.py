import csv, sys, io
from collections import defaultdict

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('data_sources/fact_afl_inspection.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Group by (data_year, true_farmer_uid, parcel_id)
# Note: interview_key is the true farmer uid in the inspection table
parcels = defaultdict(list)
for r in rows:
    y = r['data_year']
    uid = r['interview_key']
    pid = r['parcel_id']
    parcels[(y, uid, pid)].append(r)

print(f"Total rows: {len(rows)}")
print(f"Total unique (year, farmer_uid, parcel_id) groups: {len(parcels)}")

# Let's check the relationship between surface_area_ha, planted_area_ha, fallow_area_ha, other_(ha) for a few groups
count = 0
for key, group in parcels.items():
    # Only print if group has multiple rows or has fallow/other values
    has_fallow_or_other = any(r.get('fallow_area_ha') or r.get('other_(ha)') for r in group)
    is_multi_row = len(group) > 1
    
    if is_multi_row or has_fallow_or_other:
        print(f"\nGroup: {key}")
        # Get unique surface_area_ha values in this group
        surfaces = {r['surface_area_ha'] for r in group}
        print(f"  Unique surface_area_ha in group: {surfaces}")
        
        # Calculate sum of planted, fallow, and other for each row, and also check if we sum them across rows
        tot_planted = 0.0
        tot_fallow = 0.0
        tot_other = 0.0
        
        for r in group:
            p = float(r['planted_area_ha']) if r.get('planted_area_ha') else 0.0
            f_val = float(r['fallow_area_ha']) if r.get('fallow_area_ha') else 0.0
            o = float(r['other_(ha)']) if r.get('other_(ha)') else 0.0
            print(f"    Plot:{r['plot_code']} Surf:{r['surface_area_ha']} Planted:{p} Fallow:{f_val} Other:{o}")
            tot_planted += p
            tot_fallow += f_val
            tot_other += o
        
        print(f"  Summed Planted: {tot_planted} | Summed Fallow: {tot_fallow} | Summed Other: {tot_other}")
        print(f"  Total Sum (Planted + Fallow + Other): {tot_planted + tot_fallow + tot_other}")
        
        count += 1
        if count >= 10:
            break
