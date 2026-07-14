import json
import re

with open('data/dashboard_data.js', encoding='utf-8') as f:
    content = f.read()

# Extract JSON from dashboard_data.js
# It usually starts with var _dashboard_data = { ... } or similar
match = re.search(r'=\s*(\{.*\});?', content, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    print("Keys in dashboard_data:", data.keys())
    print("\nYearly trend keys and sample:")
    for y in data.get('yearly_trend', []):
        print(f"Year {y['year']}:")
        print("  cert:", y.get('cert'))
        print("  land_sit:", y.get('land_sit'))
        print("  land_own:", y.get('land_own'))
        print("  irrigation:", y.get('irrigation'))
else:
    print("Could not parse JSON from dashboard_data.js")
