import json
import glob

# Find test5 file
files = glob.glob(r'C:\ProgramData\Virinco\pyWATS\instances\default\WSJF\Error\test5_*.json')
if not files:
    print("No test5 files found")
    exit(1)

with open(files[0], 'r') as f:
    data = json.load(f)

print(f"File: {files[0]}")

def check_step(step, path='root', depth=0):
    """Check if step has loop or Loop keys."""
    if depth > 10:  # Limit depth
        return
    
    keys = list(step.keys())
    has_loop = 'loop' in keys
    has_Loop = 'Loop' in keys
    
    if has_loop or has_Loop:
        print(f"  {path}: loop={has_loop}, Loop={has_Loop}")
        if has_loop:
            print(f"    loop keys: {list(step['loop'].keys())}")
        if has_Loop:
            print(f"    Loop keys: {list(step['Loop'].keys())}")
    
    # Recurse
    if 'steps' in step and isinstance(step['steps'], list):
        for child in step['steps'][:3]:  # First 3 only
            if isinstance(child, dict):
                name = child.get('name', '?')
                check_step(child, f"{path}->{name}", depth+1)

if 'root' in data:
    check_step(data['root'])
else:
    print("No root in data")
