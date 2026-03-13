"""
Fetch example report from WATS server to analyze loop structure.
"""
import json
from src.pywats import pyWATS

# Initialize API with credentials
api = pyWATS(
    base_url="https://python.wats.com",
    token="cHlXQVRTX0FQSV9BVVRPVEVTVDo2cGhUUjg0ZTVIMHA1R3JUWGtQZlY0UTNvbmk2MiM="
)

# Fetch the report
report_id = "2961a76f-5631-49c6-8e93-15fe31635531"
print(f"Fetching report {report_id}...")

try:
    # Get report
    report_obj = api.report.get_report(report_id)
    
    # Convert to dictionary (WSJF format) - use mode='json' to serialize UUID/datetime
    if report_obj:
        report = report_obj.model_dump(mode='json', by_alias=True, exclude_none=True)
    else:
        print("Report not found")
        exit(1)
    
    # Save to file
    output_file = "example_report_from_server.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Report saved to: {output_file}")
    
    # Analyze loop structure
    def analyze_step(step, path="root", indent=0):
        prefix = "  " * indent
        name = step.get('name', 'Unnamed')
        step_type = step.get('stepType', 'Unknown')
        
        print(f"{prefix}Step: {name} ({step_type})")
        
        if 'loop' in step and step['loop']:
            loop = step['loop']
            print(f"{prefix}  Loop fields:")
            for key, value in loop.items():
                print(f"{prefix}    {key}: {value}")
        
        # Check child steps
        if 'steps' in step and step['steps']:
            for child in step['steps'][:3]:  # First 3 children
                analyze_step(child, f"{path}/{name}", indent + 1)
            if len(step['steps']) > 3:
                print(f"{prefix}  ... and {len(step['steps']) - 3} more steps")
    
    print("\n=== ANALYZING LOOP STRUCTURE ===\n")
    
    root = report.get('root', {})
    if 'steps' in root and root['steps']:
        # Find first step with loops
        for step in root['steps']:
            if 'steps' in step and step['steps']:
                for substep in step['steps']:
                    if 'loop' in substep and substep['loop']:
                        print("=== FOUND STEP WITH LOOP ===")
                        analyze_step(substep, "root", 0)
                        print("\n")
                        break
                break
    
    print(f"\nFull report structure saved to: {output_file}")

except Exception as e:
    print(f"Error fetching report: {e}")
    import traceback
    traceback.print_exc()
