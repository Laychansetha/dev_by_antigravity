import csv, sys, io
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_file(filename):
    print(f"\n===== {filename} =====")
    with open(f'data_sources/{filename}', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        print("Fields:", reader.fieldnames)
        rows = list(reader)
        print("First 3 rows:")
        for r in rows[:3]:
            # Print only key columns
            keys = ['data_year', 'farmer_uid', 'farmer_id', 'site_id', 'village_id', 'interview_key', 'variety']
            present_keys = {k: r.get(k) for k in keys if k in r}
            print(present_keys)
            # print full first row to see column values
            if r == rows[0]:
                print("Full first row:", {k: str(v).encode('ascii', 'replace').decode('ascii') for k, v in r.items() if v})

inspect_file('fact_thr_threshing.csv')
inspect_file('fact_ppr_purchase.csv')
inspect_file('fact_ppr_spec_record.csv')
