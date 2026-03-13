#!/usr/bin/env python3
"""Parse SERVICE_ENDPOINT_REPORT.md and extract all functions to CSV."""

import re
from pathlib import Path

md_path = Path("docs/internal_documentation/SERVICE_ENDPOINT_REPORT.md")
csv_path = Path("docs/internal_documentation/SERVICE_ENDPOINT_REPORT.csv")

# Read markdown
content = md_path.read_text(encoding="utf-8")

# Find all module sections
module_pattern = r'## (\d+)\.\s+([A-Z]+.*?)\(.*?\)'
modules = re.findall(module_pattern, content)

print(f"Found {len(modules)} modules")

# CSV rows
rows = [["Module", "Function", "Visibility", "Endpoint 1", "Endpoint 2", "Endpoint 3"]]

# Parse each module section
current_module = None
current_subsection = None

# Split content into lines for processing
lines = content.split('\n')

for i, line in enumerate(lines):
    # Detect module header
    module_match = re.match(r'##\s+\d+\.\s+([A-Z]+.*?)\s+', line)
    if module_match:
        current_module = module_match.group(1).split('(')[0].strip()
        # Remove "MODULE" suffix  
        current_module = current_module.replace(" MODULE", "").strip()
        current_subsection = None
        print(f"\nProcessing module: {current_module}")
        continue
    
    # Detect subsection (BoxBuildTemplate, Health Server, etc.)
    subsection_match = re.match(r'###\s+(.*)\s*$', line)
    if subsection_match:
        subsection_title = subsection_match.group(1).strip()
        if "BoxBuildTemplate" in subsection_title:
            current_subsection = "BoxBuildTemplate"
        elif "Health Server" in subsection_title:
            current_subsection = "HealthServer"
        else:
            current_subsection = None
    
    # Parse function table rows - look for rows starting with | number |
    if current_module and re.match(r'\|\s*\d+\s*\|', line):
        # Split by | and clean
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
            
        # Skip header/separator rows
        if parts[1].replace('-', '').replace(':', '').strip() == '':
            continue
        if parts[1] in ['#', 'No', 'Handler', 'File', 'Package']:
            continue
        
        # Extract function name from second column
        func_col = parts[2] if len(parts) > 2 else ""
        
        # Skip if it's a module summary row or header
        if '**' in func_col or func_col.startswith('Class') or func_col.startswith('Source'):
            continue
        
        # Extract function name (remove backticks and parameters)
        func_match = re.search(r'`([^`]+)`', func_col)
        if not func_match:
            continue
        
        function_name = func_match.group(1)
        
        # Determine visibility (Public/Internal)
        visibility = "Public"
        if len(parts) > 3:
            vis_col = parts[3]
            if "Internal" in vis_col or "⚠️" in vis_col:
                visibility = "Internal"
        
        # Extract endpoints from remaining columns
        endpoints_col = parts[4] if len(parts) > 4 else ""
        
        # Parse multiple endpoints
        endpoints = []
        
        # Look for GET/POST/PUT/DELETE/PATCH patterns
        endpoint_pattern = r'(GET|POST|PUT|DELETE|PATCH|SERVES)\s+[`/]([^`\n,]+)[`]?'
        for match in re.finditer(endpoint_pattern, endpoints_col):
            method = match.group(1)
            path = match.group(2).strip()
            endpoints.append(f"{method} {path}")
        
        # Handle special cases
        if "no endpoint" in endpoints_col.lower():
            endpoints = ["(no endpoint - " + re.search(r'\(([^)]+)\)', endpoints_col).group(1) + ")"]
        elif "delegates to" in endpoints_col.lower():
            delegate_match = re.search(r'delegates to ([^)]+)', endpoints_col)
            if delegate_match:
                endpoints = ["(delegates to " + delegate_match.group(1).strip() + ")"]
        elif "same as" in endpoints_col.lower():
            endpoints = ["same as save() on exit"]
        
        # Fill in up to 3 endpoint columns
        while len(endpoints) < 3:
            endpoints.append("")
        
        # Select module name (include subsection if applicable)
        module_name = current_module
        if current_subsection:
            module_name = f"{current_module} ({current_subsection})"
        
        # Add row
        row = [
            module_name,
            function_name,
            visibility,
            endpoints[0] if len(endpoints) > 0 else "",
            endpoints[1] if len(endpoints) > 1 else "",
            endpoints[2] if len(endpoints) > 2 else ""
        ]
        rows.append(row)
        print(f"  Added: {function_name}")

print(f"\nTotal functions extracted: {len(rows) - 1}")

# Write CSV
with csv_path.open('w', encoding='utf-8', newline='') as f:
    for row in rows:
        # Escape commas in fields
        escaped_row = []
        for field in row:
            if ',' in field and not field.startswith('('):
                escaped_row.append(field)
            else:
                escaped_row.append(field)
        f.write(','.join(escaped_row) + '\n')

print(f"CSV written to {csv_path}")
print(f"Total lines: {len(rows)}")
