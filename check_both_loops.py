import json

file_path = r'C:\ProgramData\Virinco\pyWATS\instances\default\WSJF\Error\SUCCESS_TEST_1004est-295_FATPartNo_Rev1_2026-02-12_12-48-04.json'

with open(file_path) as f:
    data = json.load(f)

def check_step(step, depth=0):
    if depth > 10:
        return 0
    
    count = 0
    has_loop = 'loop' in step
    has_Loop = 'Loop' in step
    
    if has_loop and has_Loop:
        print(f"Found step with BOTH loop and Loop: {step.get('name', 'unknown')}")
        count = 1
    elif has_loop or has_Loop:
        keys_found = []
        if has_loop:
            keys_found.append('loop')
        if has_Loop:
            keys_found.append('Loop')
        print(f"Step {step.get('name', 'unknown')} has: {', '.join(keys_found)}")
    
    if 'steps' in step and isinstance(step['steps'], list):
        for child in step['steps']:
            if isinstance(child, dict):
                count += check_step(child, depth+1)
    
    return count

print(f"Checking: {file_path}")
print()
total = check_step(data.get('root', {}))
print()
print(f"Total steps with BOTH loop and Loop: {total}")
