import csv, sys, io
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open('data_sources/dim_farmer.csv', encoding='utf-8-sig') as f:
    r = list(csv.DictReader(f))
print("dim_farmer.csv examples:")
for row in r[:5]:
    # format safe print
    print({k: str(v).encode('ascii', 'replace').decode('ascii') for k, v in row.items()})

with open('data_sources/fact_afl_inspection.csv', encoding='utf-8-sig') as f:
    r2 = list(csv.DictReader(f))
print("\nfact_afl_inspection.csv unique farmer_uids:")
uids = set(row['farmer_uid'] for row in r2)
print(list(uids)[:10])
