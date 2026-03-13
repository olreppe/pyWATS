#!/usr/bin/env python3
"""Add 'Uses Internal' column to SERVICE_ENDPOINT_REPORT.csv"""

import csv
from pathlib import Path

csv_path = Path("docs/internal_documentation/SERVICE_ENDPOINT_REPORT.csv")

# Read all rows
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Process header
header = rows[0]
new_header = [header[0], header[1], "Uses Internal"] + header[2:]

# Process data rows
new_rows = [new_header]
for row in rows[1:]:
    if len(row) < 8:
        row.extend([''] * (8 - len(row)))
    
    module = row[0]
    function = row[1]
    type1 = row[3] if len(row) > 3 else ''
    type2 = row[5] if len(row) > 5 else ''
    type3 = row[7] if len(row) > 7 else ''
    
    # Check if any endpoint is Internal
    uses_internal = "Yes" if "Internal" in [type1, type2, type3] else "No"
    
    # Build new row: Module, Function, Uses Internal, Endpoint 1, Type 1, ...
    new_row = [module, function, uses_internal] + row[2:]
    new_rows.append(new_row)

# Write back
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)

print(f"✓ Added 'Uses Internal' column")
print(f"✓ Total functions: {len(new_rows) - 1}")
internal_count = sum(1 for row in new_rows[1:] if row[2] == "Yes")
print(f"✓ Functions using internal endpoints: {internal_count}")
