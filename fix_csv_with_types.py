#!/usr/bin/env python3
"""Add Internal/Public indicator columns for each endpoint."""

import re
from pathlib import Path

md_path = Path("docs/internal_documentation/SERVICE_ENDPOINT_REPORT.md")
csv_path = Path("docs/internal_documentation/SERVICE_ENDPOINT_REPORT.csv")

content = md_path.read_text(encoding="utf-8")

# CSV with endpoint type indicators
rows = [["Module", "Function", "Endpoint 1", "Type 1", "Endpoint 2", "Type 2", "Endpoint 3", "Type 3"]]

lines = content.split('\n')
current_module = None

for i, line in enumerate(lines):
    module_match = re.match(r'##\s+\d+\.\s+([A-Z]+)\s+MODULE', line)
    if module_match:
        current_module = module_match.group(1).title()
        print(f"\nProcessing {current_module}...")
        continue
    
    if current_module and re.match(r'\|\s*\d+\s*\|', line):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 5:
            continue
            
        if parts[1].replace('-', '').replace(':', '').strip() == '':
            continue
        if parts[1] in ['#', 'No']:
            continue
        
        func_col = parts[2] if len(parts) > 2 else ""
        func_match = re.search(r'`([^`]+)`', func_col)
        if not func_match:
            continue
        
        function_name = func_match.group(1)
        
        # Check visibility - ONLY PUBLIC
        visibility_col = parts[3] if len(parts) > 3 else ""
        if "Internal" in visibility_col or "⚠️" in visibility_col:
            continue
        
        endpoints_col = parts[4] if len(parts) > 4 else ""
        
        endpoints = []
        types = []
        
        # Parse endpoints and determine type
        for match in re.finditer(r'(GET|POST|PUT|DELETE|PATCH|SERVES)\s+[`/]([^`\n,\)]+)[`]?', endpoints_col):
            method = match.group(1)
            path = match.group(2).strip()
            
            if '/internal/' in path:
                endpoints.append(f"{method} {path}")
                types.append("Internal")
            else:
                endpoints.append(f"{method} {path}")
                types.append("Public")
        
        # Handle special cases
        if "no endpoint" in endpoints_col.lower():
            special_match = re.search(r'\(([^)]+)\)', endpoints_col)
            if special_match:
                endpoints = [f"(no endpoint - {special_match.group(1)})"]
                types = ["N/A"]
        elif "delegates to" in endpoints_col.lower():
            delegate_match = re.search(r'delegates to ([^)]+)', endpoints_col)
            if delegate_match:
                endpoints = [f"(delegates to {delegate_match.group(1).strip()})"]
                types = ["Delegate"]
        elif "same as" in endpoints_col.lower():
            endpoints = ["same as save() on exit"]
            types = ["Delegate"]
        
        # Pad to 3 endpoints
        while len(endpoints) < 3:
            endpoints.append("")
            types.append("")
        
        row = [
            current_module,
            function_name,
            endpoints[0], types[0],
            endpoints[1], types[1],
            endpoints[2], types[2]
        ]
        rows.append(row)
        print(f"  ✓ {function_name}")

print(f"\nTotal: {len(rows) - 1} PUBLIC functions")

# Write CSV
with csv_path.open('w', encoding='utf-8', newline='') as f:
    for row in rows:
        escaped = []
        for field in row:
            if ',' in field:
                escaped.append(f'"{field}"')
            else:
                escaped.append(field)
        f.write(','.join(escaped) + '\n')

print(f"✓ CSV written with endpoint type indicators")
