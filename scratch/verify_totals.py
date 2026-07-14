import csv

with open('data_sources/fact_afl_inspection.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

# 1. Sum over all rows
sum_planted = 0.0
sum_fallow = 0.0
sum_other = 0.0

for r in rows:
    sum_planted += float(r['planted_area_ha']) if r.get('planted_area_ha') else 0.0
    sum_fallow += float(r['fallow_area_ha']) if r.get('fallow_area_ha') else 0.0
    sum_other += float(r['other_(ha)']) if r.get('other_(ha)') else 0.0

sum_individual = sum_planted + sum_fallow + sum_other

# 2. Sum unique surface_area_ha per (data_year, interview_key, parcel_id)
seen_parcels = {}
for r in rows:
    y = r['data_year']
    uid = r['interview_key']
    pid = r['parcel_id']
    key = (y, uid, pid)
    surf = float(r['surface_area_ha']) if r.get('surface_area_ha') else 0.0
    
    if key not in seen_parcels:
        seen_parcels[key] = surf
    else:
        # Check if they are the same
        if abs(seen_parcels[key] - surf) > 0.01:
            print(f"Warning: Discrepancy for key {key}: {seen_parcels[key]} vs {surf}")

sum_unique_surf = sum(seen_parcels.values())

print(f"Sum of planted:         {sum_planted:.2f}")
print(f"Sum of fallow:          {sum_fallow:.2f}")
print(f"Sum of other:           {sum_other:.2f}")
print(f"Sum of individual cols: {sum_individual:.2f}")
print(f"Sum of unique surf:     {sum_unique_surf:.2f}")
print(f"Difference:             {abs(sum_individual - sum_unique_surf):.4f}")
