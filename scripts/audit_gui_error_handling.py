"""
Audit GUI QMessageBox usage and suggest ErrorHandlingMixin replacements.

Categorizes QMessageBox calls into:
1. In exception handlers → use self.handle_error(e, context)
2. Confirmation dialogs → use self.confirm_action(message, title)
3. Simple warnings/errors → use self.show_warning/error/success(message, title)
4. Complex dialogs → manual review needed

Output: Detailed report with file-by-line suggestions for migration.
"""

import ast
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class QMessageBoxCall:
    """Represents a QMessageBox call found in source code."""
    file_path: Path
    line_number: int
    method: str  # warning, critical, information, question
    in_except_block: bool
    exception_variable: Optional[str]
    full_line: str
    context_lines: List[str]
    category: Literal['exception_handler', 'confirmation', 'simple_dialog', 'complex']
    suggestion: str


class QMessageBoxAuditor(ast.NodeVisitor):
    """AST visitor to find QMessageBox calls and categorize them."""
    
    def __init__(self, source_code: str, file_path: Path):
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.file_path = file_path
        self.calls: List[QMessageBoxCall] = []
        self.except_stack: List[ast.ExceptHandler] = []
    
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        """Track when we're inside except blocks."""
        self.except_stack.append(node)
        self.generic_visit(node)
        self.except_stack.pop()
    
    def visit_Call(self, node: ast.Call) -> None:
        """Find QMessageBox method calls."""
        if isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == 'QMessageBox'):
                
                method = node.func.attr
                if method in ['warning', 'critical', 'information', 'question']:
                    self._process_messagebox_call(node, method)
        
        self.generic_visit(node)
    
    def _process_messagebox_call(self, node: ast.Call, method: str) -> None:
        """Process a QMessageBox call and categorize it."""
        line_number = node.lineno
        
        # Get context (5 lines before and after)
        start = max(0, line_number - 6)
        end = min(len(self.source_lines), line_number + 5)
        context_lines = self.source_lines[start:end]
        
        # Check if in except block
        in_exception = len(self.except_stack) > 0
        exception_var = None
        if in_exception:
            exception_var = self.except_stack[-1].name
        
        # Get the actual line
        full_line = self.source_lines[line_number - 1] if line_number > 0 else ""
        
        # Categorize the call
        category, suggestion = self._categorize_call(
            method, in_exception, exception_var, full_line, context_lines
        )
        
        call = QMessageBoxCall(
            file_path=self.file_path,
            line_number=line_number,
            method=method,
            in_except_block=in_exception,
            exception_variable=exception_var,
            full_line=full_line.strip(),
            context_lines=context_lines,
            category=category,
            suggestion=suggestion
        )
        self.calls.append(call)
    
    def _categorize_call(
        self, 
        method: str, 
        in_exception: bool, 
        exception_var: Optional[str],
        full_line: str,
        context_lines: List[str]
    ) -> tuple[Literal['exception_handler', 'confirmation', 'simple_dialog', 'complex'], str]:
        """Categorize QMessageBox call and generate suggestion."""
        
        # Category 1: In exception handler
        if in_exception and method in ['warning', 'critical']:
            return (
                'exception_handler',
                f"self.handle_error({exception_var or 'e'}, \"<context>\")"
            )
        
        # Category 2: Confirmation dialog
        if method == 'question':
            # Check if comparing to StandardButton
            context_str = '\n'.join(context_lines)
            if 'StandardButton.Yes' in context_str or 'StandardButton.No' in context_str:
                return (
                    'confirmation',
                    'if self.confirm_action("<message>", "<title>"):'
                )
        
        # Category 3: Simple information/warning/critical (not in exception)
        if not in_exception:
            if method == 'information':
                return ('simple_dialog', 'self.show_success("<message>", "<title>")')
            elif method == 'warning':
                return ('simple_dialog', 'self.show_warning("<message>", "<title>")')
            elif method == 'critical':
                return ('simple_dialog', 'self.show_error("<message>", "<title>")')
        
        # Category 4: Complex (needs manual review)
        return ('complex', 'Manual review needed')


def audit_file(file_path: Path) -> List[QMessageBoxCall]:
    """Audit a single file for QMessageBox usage."""
    try:
        source_code = file_path.read_text(encoding='utf-8')
        tree = ast.parse(source_code, filename=str(file_path))
        
        auditor = QMessageBoxAuditor(source_code, file_path)
        auditor.visit(tree)
        
        return auditor.calls
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return []


def audit_directory(directory: Path, pattern: str = "*.py") -> List[QMessageBoxCall]:
    """Audit all Python files in a directory."""
    all_calls: List[QMessageBoxCall] = []
    
    for file_path in directory.rglob(pattern):
        calls = audit_file(file_path)
        all_calls.extend(calls)
    
    return all_calls


def print_report(calls: List[QMessageBoxCall]) -> None:
    """Print detailed audit report."""
    
    # Group by category
    by_category = {
        'exception_handler': [],
        'confirmation': [],
        'simple_dialog': [],
        'complex': []
    }
    for call in calls:
        by_category[call.category].append(call)
    
    print("=" * 80)
    print("GUI ERROR HANDLING AUDIT REPORT")
    print("=" * 80)
    print()
    print(f"Total QMessageBox calls found: {len(calls)}")
    print(f"  - Exception handlers: {len(by_category['exception_handler'])}")
    print(f"  - Confirmations: {len(by_category['confirmation'])}")
    print(f"  - Simple dialogs: {len(by_category['simple_dialog'])}")
    print(f"  - Complex (manual review): {len(by_category['complex'])}")
    print()
    
    # Print details for each category
    for category, category_calls in by_category.items():
        if not category_calls:
            continue
        
        print("=" * 80)
        print(f"{category.upper().replace('_', ' ')}")
        print("=" * 80)
        print()
        
        # Group by file
        by_file = {}
        for call in category_calls:
            if call.file_path not in by_file:
                by_file[call.file_path] = []
            by_file[call.file_path].append(call)
        
        for file_path, file_calls in sorted(by_file.items()):
            rel_path = file_path.relative_to(Path.cwd()) if file_path.is_relative_to(Path.cwd()) else file_path
            print(f"📄 {rel_path}")
            print()
            
            for call in sorted(file_calls, key=lambda c: c.line_number):
                print(f"  Line {call.line_number}: QMessageBox.{call.method}()")
                if call.in_except_block:
                    print(f"  In except block: {call.exception_variable or '(unnamed)'}")
                print(f"  Current: {call.full_line[:100]}...")
                print(f"  Suggested: {call.suggestion}")
                print()
            
            print()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Audit GUI QMessageBox usage and suggest ErrorHandlingMixin replacements"
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='src/pywats_ui/apps/configurator/pages',
        help='Path to audit (default: configurator pages)'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply automatic replacements (NOT IMPLEMENTED - manual migration recommended)'
    )
    
    args = parser.parse_args()
    
    target_path = Path(args.path)
    
    if not target_path.exists():
        print(f"Error: Path does not exist: {target_path}", file=sys.stderr)
        return 1
    
    print(f"Auditing: {target_path}")
    print()
    
    if target_path.is_file():
        calls = audit_file(target_path)
    else:
        calls = audit_directory(target_path)
    
    print_report(calls)
    
    # Summary by file
    print("=" * 80)
    print("SUMMARY BY FILE")
    print("=" * 80)
    print()
    
    by_file = {}
    for call in calls:
        if call.file_path not in by_file:
            by_file[call.file_path] = []
        by_file[call.file_path].append(call)
    
    for file_path in sorted(by_file.keys()):
        rel_path = file_path.relative_to(Path.cwd()) if file_path.is_relative_to(Path.cwd()) else file_path
        file_calls = by_file[file_path]
        
        # Count by category
        counts = {
            'exception_handler': sum(1 for c in file_calls if c.category == 'exception_handler'),
            'confirmation': sum(1 for c in file_calls if c.category == 'confirmation'),
            'simple_dialog': sum(1 for c in file_calls if c.category == 'simple_dialog'),
            'complex': sum(1 for c in file_calls if c.category == 'complex')
        }
        
        print(f"{rel_path}: {len(file_calls)} calls")
        print(f"  Exception handlers: {counts['exception_handler']}")
        print(f"  Confirmations: {counts['confirmation']}")
        print(f"  Simple dialogs: {counts['simple_dialog']}")
        print(f"  Complex: {counts['complex']}")
        print()
    
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("1. Review exception handlers - replace with self.handle_error(e, context)")
    print("2. Review confirmations - replace with self.confirm_action(message, title)")
    print("3. Review simple dialogs - replace with self.show_warning/error/success()")
    print("4. Manually review complex cases")
    print()
    print("Note: Automatic replacement NOT recommended due to context string requirements.")
    print("      Manual migration ensures appropriate context for each error.")
    print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
