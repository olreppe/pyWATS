"""
Audit Exception Logging Script

Finds logger.error() and logger.warning() calls in except blocks that lack exc_info parameter.

Why:
- Stack traces are essential for debugging exceptions
- logger.exception() or logger.error(..., exc_info=True) preserve stack traces
- Currently many except blocks log without context

Usage:
    # Audit only (report findings)
    python scripts/audit_exception_logging.py

    # Apply fixes (use logger.exception for errors)
    python scripts/audit_exception_logging.py --apply

    # Target specific layer
    python scripts/audit_exception_logging.py --layer api
"""

import argparse
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ExceptionLoggingAuditor:
    """Audits and fixes exception logging patterns."""

    def __init__(self, root_dir: Path, layer: str = "all"):
        self.root_dir = root_dir
        self.layer = layer
        self.stats = {
            "scanned": 0,
            "needs_update": 0,
            "already_correct": 0,
            "updated": 0,
            "errors": 0
        }

    def get_target_paths(self) -> List[Path]:
        """Get list of Python files to analyze based on layer."""
        src_dir = self.root_dir / "src"

        if self.layer == "api":
            patterns = ["pywats/**/*.py"]
            exclude = ["pywats_*"]
        elif self.layer == "client":
            patterns = ["pywats_client/**/*.py"]
            exclude = []
        elif self.layer == "gui":
            patterns = ["pywats_ui/**/*.py"]
            exclude = []
        elif self.layer == "events":
            patterns = ["pywats_events/**/*.py"]
            exclude = []
        else:  # all
            patterns = ["**/*.py"]
            exclude = ["__pycache__"]

        files = []
        for pattern in patterns:
            for file_path in src_dir.glob(pattern):
                if any(exc in str(file_path) for exc in exclude):
                    continue
                if "__pycache__" in str(file_path) or file_path.name.startswith("test_"):
                    continue
                if file_path.is_file():
                    files.append(file_path)

        return sorted(files)

    def find_exception_logging_issues(self, file_path: Path) -> Dict:
        """Find logger calls in except blocks without exc_info."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {
                "file": file_path,
                "status": "error",
                "error": str(e)
            }

        # Parse AST to find except blocks
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            return {
                "file": file_path,
                "status": "error",
                "error": f"SyntaxError: {e}"
            }

        issues = []
        
        # Walk AST to find ExceptHandler nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                # Look for logger.error/warning calls within this except block
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        # Check if it's a logger.error or logger.warning call
                        if isinstance(child.func, ast.Attribute):
                            if (hasattr(child.func.value, 'id') and 
                                child.func.value.id in ['logger', 'self._logger'] and
                                child.func.attr in ['error', 'warning']):
                                
                                # Check if exc_info is already present
                                has_exc_info = any(
                                    kw.arg == 'exc_info' for kw in child.keywords
                                )
                                
                                if not has_exc_info:
                                    # Get line number
                                    line_num = child.lineno
                                    
                                    # Get the actual line of code
                                    lines = content.split('\n')
                                    if line_num <= len(lines):
                                        code_line = lines[line_num - 1].strip()
                                        
                                        issues.append({
                                            "line": line_num,
                                            "code": code_line,
                                            "method": child.func.attr,
                                            "logger": child.func.value.id if hasattr(child.func.value, 'id') else 'logger'
                                        })

        if issues:
            return {
                "file": file_path,
                "status": "needs_update",
                "issues": issues,
                "content": content
            }
        else:
            return {
                "file": file_path,
                "status": "correct"
            }

    def apply_fixes(self, analysis: Dict) -> bool:
        """Apply fixes to a file by adding exc_info=True or using logger.exception."""
        if analysis["status"] != "needs_update":
            return False

        file_path = analysis["file"]
        content = analysis["content"]
        lines = content.split('\n')

        # Sort issues by line number (descending) to modify from bottom up
        issues = sorted(analysis["issues"], key=lambda x: x["line"], reverse=True)

        modified = False
        for issue in issues:
            line_num = issue["line"] - 1  # 0-indexed
            if line_num >= len(lines):
                continue

            original_line = lines[line_num]
            
            # Strategy: For .error() calls, replace with .exception()
            # For .warning() calls, add exc_info=True
            
            if issue["method"] == "error":
                # Replace logger.error( with logger.exception(
                new_line = re.sub(
                    r'logger\.error\(',
                    r'logger.exception(',
                    original_line
                )
                # Also handle self._logger.error(
                new_line = re.sub(
                    r'self\._logger\.error\(',
                    r'self._logger.exception(',
                    new_line
                )
            else:  # warning
                # Add exc_info=True parameter
                # Find the closing parenthesis and inject before it
                # This is tricky with multiline calls, so we'll use simple pattern
                if original_line.rstrip().endswith(')'):
                    # Single line call - inject before closing paren
                    new_line = original_line.rstrip()[:-1] + ', exc_info=True)'
                elif original_line.rstrip().endswith(','):
                    # Line ends with comma - don't modify (likely multiline)
                    continue
                else:
                    # Complex case - skip for manual review
                    continue

            if new_line != original_line:
                lines[line_num] = new_line
                modified = True

        if modified:
            try:
                file_path.write_text('\n'.join(lines), encoding='utf-8')
                return True
            except Exception as e:
                print(f"ERROR writing {file_path}: {e}")
                return False

        return False

    def run(self, apply: bool = False) -> None:
        """Run the audit process."""
        print("=" * 80)
        print("Exception Logging Auditor")
        print("=" * 80)
        print(f"Root: {self.root_dir}")
        print(f"Layer: {self.layer}")
        print(f"Mode: {'APPLY FIXES' if apply else 'AUDIT ONLY'}")
        print("=" * 80)

        # Get target files
        files = self.get_target_paths()
        print(f"\nScanning {len(files)} Python files\n")

        # Analyze files
        needs_update = []
        already_correct = []
        errors = []

        for file_path in files:
            self.stats["scanned"] += 1
            result = self.find_exception_logging_issues(file_path)

            if result["status"] == "needs_update":
                needs_update.append(result)
                self.stats["needs_update"] += 1
            elif result["status"] == "correct":
                already_correct.append(result)
                self.stats["already_correct"] += 1
            else:  # error
                errors.append(result)
                self.stats["errors"] += 1

        # Report findings
        print("\n" + "=" * 80)
        print("AUDIT RESULTS")
        print("=" * 80)
        print(f"Files scanned: {self.stats['scanned']}")
        print(f"Already correct: {self.stats['already_correct']}")
        print(f"Needs update: {self.stats['needs_update']}")
        print(f"Errors: {self.stats['errors']}")
        print()

        if errors:
            print("\nERRORS:")
            for err in errors:
                print(f"  ❌ {err['file'].relative_to(self.root_dir)}: {err['error']}")

        if needs_update:
            # Count total issues
            total_issues = sum(len(r["issues"]) for r in needs_update)
            print(f"\nFILES WITH ISSUES ({len(needs_update)} files, {total_issues} issues):")
            
            for result in needs_update[:30]:
                rel_path = result['file'].relative_to(self.root_dir)
                print(f"\n  📝 {rel_path} ({len(result['issues'])} issues)")
                for issue in result['issues'][:5]:  # Show first 5 issues per file
                    print(f"      Line {issue['line']}: {issue['method']}() - {issue['code'][:80]}")
                if len(result['issues']) > 5:
                    print(f"      ... and {len(result['issues']) - 5} more")
            
            if len(needs_update) > 30:
                remaining = len(needs_update) - 30
                remaining_issues = sum(len(r["issues"]) for r in needs_update[30:])
                print(f"\n  ... and {remaining} more files ({remaining_issues} issues)")

        # Apply fixes if requested
        if apply and needs_update:
            print("\n" + "=" * 80)
            print("APPLYING FIXES")
            print("=" * 80)
            print("Strategy:")
            print("  - logger.error() → logger.exception() (auto includes exc_info)")
            print("  - logger.warning() → logger.warning(..., exc_info=True)")
            print()

            for result in needs_update:
                if self.apply_fixes(result):
                    self.stats["updated"] += 1
                    rel_path = result['file'].relative_to(self.root_dir)
                    print(f"  ✅ Updated: {rel_path} ({len(result['issues'])} changes)")

            print(f"\n✅ Successfully updated {self.stats['updated']} files!")

        elif not apply and needs_update:
            print("\n" + "=" * 80)
            print("AUDIT ONLY - No changes applied")
            print("Run with --apply to fix issues automatically")
            print("=" * 80)

        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Files scanned: {self.stats['scanned']}")
        print(f"Already correct: {self.stats['already_correct']}")
        print(f"Need fixes: {self.stats['needs_update']}")
        if apply:
            print(f"Fixed: {self.stats['updated']}")
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Audit exception logging for missing exc_info parameters"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply fixes (default: audit only)"
    )
    parser.add_argument(
        "--layer",
        choices=["all", "api", "client", "gui", "events"],
        default="all",
        help="Target specific layer (default: all)"
    )

    args = parser.parse_args()

    # Get project root
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    # Run auditor
    auditor = ExceptionLoggingAuditor(root_dir, layer=args.layer)
    auditor.run(apply=args.apply)


if __name__ == "__main__":
    main()
