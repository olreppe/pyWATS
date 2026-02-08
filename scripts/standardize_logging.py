"""
Standardize Logger Initialization Script

Replaces `logging.getLogger(__name__)` with `get_logger(__name__)` across the codebase.

Why:
- get_logger() enables correlation IDs and structured logging
- Provides consistent logging configuration
- Future-proof for logging enhancements

Usage:
    # Dry-run (report only)
    python scripts/standardize_logging.py

    # Apply changes
    python scripts/standardize_logging.py --apply

    # Target specific layer
    python scripts/standardize_logging.py --layer api
    python scripts/standardize_logging.py --layer client
    python scripts/standardize_logging.py --layer gui
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


class LoggerStandardizer:
    """Automated logger standardization tool."""

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
            # Core API layer: pywats package
            patterns = ["pywats/**/*.py"]
            exclude = ["pywats_*"]  # Exclude client/events/ui/cfx
        elif self.layer == "client":
            # Client layer: pywats_client package
            patterns = ["pywats_client/**/*.py"]
            exclude = []
        elif self.layer == "gui":
            # GUI layer: pywats_ui package
            patterns = ["pywats_ui/**/*.py"]
            exclude = []
        elif self.layer == "events":
            # Events layer: pywats_events package
            patterns = ["pywats_events/**/*.py"]
            exclude = []
        else:  # all
            patterns = ["**/*.py"]
            exclude = ["__pycache__"]

        files = []
        for pattern in patterns:
            for file_path in src_dir.glob(pattern):
                # Skip excluded patterns
                if any(exc in str(file_path) for exc in exclude):
                    continue
                # Skip __pycache__ and test files
                if "__pycache__" in str(file_path) or file_path.name.startswith("test_"):
                    continue
                if file_path.is_file():
                    files.append(file_path)

        return sorted(files)

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single file for logger usage."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {
                "file": file_path,
                "status": "error",
                "error": str(e)
            }

        # Check for logging.getLogger(__name__) pattern
        old_pattern = re.compile(r'logger = logging\.getLogger\(__name__\)')
        old_module_pattern = re.compile(r'self\._logger = logging\.getLogger\(__name__\)')

        has_old_logger = bool(old_pattern.search(content))
        has_old_module_logger = bool(old_module_pattern.search(content))

        if not (has_old_logger or has_old_module_logger):
            return {
                "file": file_path,
                "status": "correct",
                "message": "Already using get_logger or no logger"
            }

        # Check if get_logger is already imported
        has_get_logger_import = bool(re.search(r'from pywats\.core\.logging import.*get_logger', content))

        # Check which import pattern is used
        has_logging_import = bool(re.search(r'^import logging$', content, re.MULTILINE))
        has_from_logging = bool(re.search(r'^from logging import', content, re.MULTILINE))

        return {
            "file": file_path,
            "status": "needs_update",
            "has_old_logger": has_old_logger,
            "has_old_module_logger": has_old_module_logger,
            "has_get_logger_import": has_get_logger_import,
            "has_logging_import": has_logging_import,
            "has_from_logging": has_from_logging,
            "content": content
        }

    def update_file(self, analysis: Dict) -> bool:
        """Update a single file to use get_logger."""
        if analysis["status"] != "needs_update":
            return False

        file_path = analysis["file"]
        content = analysis["content"]
        original_content = content

        # Step 1: Add get_logger import if not present
        if not analysis["has_get_logger_import"]:
            # Find the right place to add import
            if analysis["has_logging_import"]:
                # Add after "import logging"
                content = re.sub(
                    r'(import logging\n)',
                    r'\1from pywats.core.logging import get_logger\n',
                    content,
                    count=1
                )
            elif analysis["has_from_logging"]:
                # Add before "from logging import"
                content = re.sub(
                    r'(from logging import)',
                    r'from pywats.core.logging import get_logger\n\1',
                    content,
                    count=1
                )
            else:
                # No logging import - add at top after docstring/imports
                # Find first import statement
                import_match = re.search(r'^(import |from )', content, re.MULTILINE)
                if import_match:
                    insert_pos = import_match.start()
                    content = (
                        content[:insert_pos] +
                        "from pywats.core.logging import get_logger\n" +
                        content[insert_pos:]
                    )
                else:
                    # No imports at all - add after docstring or at top
                    docstring_end = re.search(r'"""\n\n', content)
                    if docstring_end:
                        insert_pos = docstring_end.end()
                    else:
                        insert_pos = 0
                    content = (
                        content[:insert_pos] +
                        "\nfrom pywats.core.logging import get_logger\n\n" +
                        content[insert_pos:]
                    )

        # Step 2: Replace logging.getLogger(__name__) with get_logger(__name__)
        if analysis["has_old_logger"]:
            content = re.sub(
                r'logger = logging\.getLogger\(__name__\)',
                r'logger = get_logger(__name__)',
                content
            )

        # Step 3: Replace self._logger = logging.getLogger(__name__)
        if analysis["has_old_module_logger"]:
            content = re.sub(
                r'self\._logger = logging\.getLogger\(__name__\)',
                r'self._logger = get_logger(__name__)',
                content
            )

        # Only write if content changed
        if content != original_content:
            try:
                file_path.write_text(content, encoding='utf-8')
                return True
            except Exception as e:
                print(f"ERROR writing {file_path}: {e}")
                return False

        return False

    def run(self, apply: bool = False) -> None:
        """Run the standardization process."""
        print("=" * 80)
        print("Logger Standardization Tool")
        print("=" * 80)
        print(f"Root: {self.root_dir}")
        print(f"Layer: {self.layer}")
        print(f"Mode: {'APPLY' if apply else 'DRY RUN'}")
        print("=" * 80)

        # Get target files
        files = self.get_target_paths()
        print(f"\nFound {len(files)} Python files to analyze\n")

        # Analyze files
        needs_update = []
        already_correct = []
        errors = []

        for file_path in files:
            self.stats["scanned"] += 1
            result = self.analyze_file(file_path)

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
        print("ANALYSIS RESULTS")
        print("=" * 80)
        print(f"Total files scanned: {self.stats['scanned']}")
        print(f"Already correct: {self.stats['already_correct']}")
        print(f"Needs update: {self.stats['needs_update']}")
        print(f"Errors: {self.stats['errors']}")
        print()

        if errors:
            print("\nERRORS:")
            for err in errors:
                print(f"  ❌ {err['file'].relative_to(self.root_dir)}: {err['error']}")

        if needs_update:
            print(f"\nFILES NEEDING UPDATE ({len(needs_update)}):")
            for result in needs_update[:20]:  # Show first 20
                rel_path = result['file'].relative_to(self.root_dir)
                print(f"  📝 {rel_path}")
            if len(needs_update) > 20:
                print(f"  ... and {len(needs_update) - 20} more files")

        # Apply changes if requested
        if apply and needs_update:
            print("\n" + "=" * 80)
            print("APPLYING CHANGES")
            print("=" * 80)

            for result in needs_update:
                if self.update_file(result):
                    self.stats["updated"] += 1
                    rel_path = result['file'].relative_to(self.root_dir)
                    print(f"  ✅ Updated: {rel_path}")
                else:
                    print(f"  ⚠️  Skipped: {result['file'].relative_to(self.root_dir)}")

            print(f"\n✅ Successfully updated {self.stats['updated']} files!")

        elif not apply and needs_update:
            print("\n" + "=" * 80)
            print("DRY RUN - No changes applied")
            print("Run with --apply to update files")
            print("=" * 80)

        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Scanned: {self.stats['scanned']} files")
        print(f"Correct: {self.stats['already_correct']} files")
        print(f"Needs update: {self.stats['needs_update']} files")
        if apply:
            print(f"Updated: {self.stats['updated']} files")
            print(f"Coverage: {((self.stats['already_correct'] + self.stats['updated']) / self.stats['scanned'] * 100):.1f}%")
        else:
            print(f"Potential coverage: {((self.stats['already_correct'] + self.stats['needs_update']) / self.stats['scanned'] * 100):.1f}%")
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Standardize logger initialization across pyWATS codebase"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (default: dry-run only)"
    )
    parser.add_argument(
        "--layer",
        choices=["all", "api", "client", "gui", "events"],
        default="all",
        help="Target specific layer (default: all)"
    )

    args = parser.parse_args()

    # Get project root (2 levels up from scripts/)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent

    # Run standardizer
    standardizer = LoggerStandardizer(root_dir, layer=args.layer)
    standardizer.run(apply=args.apply)


if __name__ == "__main__":
    main()
