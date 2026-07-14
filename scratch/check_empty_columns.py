import csv
from collections import Counter

with open('data_sources/fact_afl_inspection.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

cols = ['status_harvest', 'land_situation', 'land_ownership', 'irrigation_system']
print(f"Total rows: {len(rows)}")

for col in cols:
    non_empty = [r.get(col, '').strip() for r in rows if r.get(col, '').strip()]
    print(f"\nColumn: '{col}' | Non-empty count: {len(non_empty)}")
    # Print top 5 values
    c = Counter(non_empty)
    print("  Top values:", c.most_common(5))
