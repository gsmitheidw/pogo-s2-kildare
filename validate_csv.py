import csv
from io import StringIO

valid_types = {"PokéStop", "Gym", "Nominated", "Potential", "NotPogo"}
issues = []

with open("kildare_poi.csv", encoding="utf-8") as f:
    raw_lines = f.readlines()

# Check for malformed lines manually
for i, raw_line in enumerate(raw_lines, start=1):
    quote_count = raw_line.count('"')
    if quote_count % 2 != 0:
        issues.append(f"- Row {i}: Unmatched quote in line")

# Now parse with Python's CSV module for better handling of quotes
with open("kildare_poi.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    
    coord_map = {}
    name_map = {}

    for i, row in enumerate(reader, start=2):  # 2 = line after header
        if len(row) not in (4, 5):
            issues.append(f"- Row {i}: Expected 4 or 5 fields, got {len(row)}")
            continue

        name, lat_str, lng_str, typ = row[0:4]
        notes = row[4] if len(row) == 5 else ""

        name = name.strip()
        typ = typ.strip()

        try:
            lat = float(lat_str)
            lng = float(lng_str)
        except ValueError:
            issues.append(f"- Row {i}: Invalid lat/lng format")
            continue

        if '"' in name and not name.startswith('"'):
            issues.append(f"- Row {i}: Unescaped quote in name field")

        if typ not in valid_types:
            issues.append(f"- Row {i}: Invalid type '{typ}'")

        coord_key = (lat, lng)
        if coord_key in coord_map:
            issues.append(f"- Row {i}: Duplicate coordinates (also row {coord_map[coord_key]})")
        else:
            coord_map[coord_key] = i

        if name in name_map:
            prev_lat, prev_lng, prev_row = name_map[name]
            if abs(lat - prev_lat) > 0.00001 or abs(lng - prev_lng) > 0.00001:
                issues.append(f"- Row {i}: Name '{name}' has different coords from row {prev_row}")
        else:
            name_map[name] = (lat, lng, i)

# Output
if issues:
    print("Found issues:\n")
    for issue in issues:
        print(issue)
else:
    print("✔  No obvious errors found in the CSV.")

