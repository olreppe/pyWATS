#!/usr/bin/env python3
"""
Script to automatically fix remaining type errors from mypy.
Run this before committing code to fix common type issues.
"""
import re
from pathlib import Path
from typing import cast

ROOT = Path(__file__).parent.parent / "src"

def fix_retry_handler_exceptions():
    """Fix exception constructors in retry_handler.py"""
    file = ROOT / "pywats" / "core" / "retry_handler.py"
    content = file.read_text(encoding="utf-8")
    
    # Fix ConnectionError in execute (sync)
    content = re.sub(
        r'(\s+except httpx\.ConnectError as e:\s+last_exception = ConnectionError\(\s+f"Failed to connect: \{e\}",\s+)url=endpoint',
        r'\1operation=f"{method} {endpoint}",\n                    details={"url": endpoint}',
        content
    )
    
    # Fix TimeoutError in execute (sync)
    content = re.sub(
        r'(\s+except httpx\.TimeoutException as e:\s+last_exception = TimeoutError\(\s+f"Request timed out: \{e\}",\s+)endpoint=endpoint',
        r'\1operation=f"{method} {endpoint}",\n                    details={"endpoint": endpoint}',
        content
    )
    
    # Fix PyWATSError (remove show_hints)
    content = content.replace(
        'raise PyWATSError(f"HTTP request failed: {e}", show_hints=False)',
        'raise PyWATSError(f"HTTP request failed: {e}")'
    )
    content = content.replace(
        'raise PyWATSError("Unexpected state: no response or exception after retries", show_hints=False)',
        'raise PyWATSError("Unexpected state: no response or exception after retries")'
    )
    
    file.write_text(content, encoding="utf-8")
    print(f"[OK] Fixed {file}")

def add_type_ignores_for_pydantic():
    """Add type: ignore comments for Pydantic auto-conversion"""
    file = ROOT / "pywats" / "domains" / "report" / "report_models" / "uut" / "steps" / "sequence_call.py"
    content = file.read_text(encoding="utf-8")
    
    # Add type: ignore for status parameter in step constructors (Pydantic handles str->enum)
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'Step(name=name' in line and 'status=' in line and '# type: ignore' not in line:
            lines[i] = line.rstrip() + '  # type: ignore[arg-type]'
    
    content = '\n'.join(lines)
    file.write_text(content, encoding="utf-8")
    print(f"[OK] Added type ignores to {file}")

if __name__ == "__main__":
    print("Fixing type errors...")
    fix_retry_handler_exceptions()
    add_type_ignores_for_pydantic()
    print("\n[DONE] Run mypy again to verify fixes")
