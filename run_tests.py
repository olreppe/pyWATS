#!/usr/bin/env python3
"""
PyWATS Test Runner

This script provides a convenient way to run different categories of tests.
Usage:
    python run_tests.py [module] [options]

Examples:
    python run_tests.py                    # Run all tests
    python run_tests.py pywats             # Run top-level pyWATS tests
    python run_tests.py app                # Run app module tests
    python run_tests.py report             # Run report module tests
    python run_tests.py --coverage         # Run with coverage report
    python run_tests.py --verbose          # Run with verbose output
"""

import sys
import subprocess
import argparse
from pathlib import Path


class TestRunner:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.tests_dir = self.root_dir / "tests"
        
    def run_command(self, cmd):
        """Run pytest command and return result"""
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode == 0
    
    def build_pytest_command(self, args):
        """Build pytest command based on arguments"""
        # Use virtual environment python if available
        venv_python = self.root_dir / ".venv" / "Scripts" / "python.exe"
        python_cmd = str(venv_python) if venv_python.exists() else "python"
        
        cmd = [python_cmd, "-m", "pytest"]
        
        # Base pytest options
        cmd.extend(["-v", "--tb=short"])
        
        # Coverage options
        if args.coverage:
            cmd.extend([
                "--cov=src/pyWATS",
                "--cov-report=html:htmlcov",
                "--cov-report=xml:coverage.xml",
                "--cov-report=term-missing"
            ])
        
        # Verbose output
        if args.verbose:
            cmd.append("-vv")
        
        # Determine test path
        test_path = self.get_test_selection(args)
        
        if test_path:
            cmd.append(str(test_path))
        else:
            cmd.append(str(self.tests_dir))
            
        # Add any additional pytest args
        if args.pytest_args:
            cmd.extend(args.pytest_args)
            
        return cmd
    
    def get_test_selection(self, args):
        """Determine which tests to run based on arguments"""
        test_path = None
        
        # Module-specific paths
        module_paths = {
            "pywats": self.tests_dir / "test_pywats_toplevel.py",
            "app": self.tests_dir / "modules" / "test_app.py",
            "asset": self.tests_dir / "modules" / "test_asset.py",
            "product": self.tests_dir / "modules" / "test_product.py",
            "production": self.tests_dir / "modules" / "test_production.py",
            "report": self.tests_dir / "modules" / "test_report.py",
            "software": self.tests_dir / "modules" / "test_software.py",
            "workflow": self.tests_dir / "modules" / "test_workflow.py",
            "modules": self.tests_dir / "modules"
        }
        
        # Check for module specification
        if args.module and args.module in module_paths:
            test_path = module_paths[args.module]
                
        return test_path
    
    def list_available_tests(self):
        """List all available test categories"""
        print("Available test categories:")
        print("\nTop Level:")
        print("  pywats      - pyWATS API connection tests")
        
        print("\nModule Tests:")
        print("  app         - App module tests")
        print("  asset       - Asset module tests")
        print("  product     - Product module tests")
        print("  production  - Production module tests")
        print("  report      - Report module tests")
        print("  software    - Software module tests")
        print("  workflow    - Workflow module tests")
        print("  modules     - All module tests")
        
        print("\nExamples:")
        print("  python run_tests.py              # All tests")
        print("  python run_tests.py pywats       # Top-level tests")
        print("  python run_tests.py app          # App module tests")
        print("  python run_tests.py modules      # All module tests")
        print("  python run_tests.py --coverage   # All tests with coverage")


def main():
    parser = argparse.ArgumentParser(
        description="PyWATS Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "module",
        nargs="?",
        help="Module to test (pywats, app, asset, product, production, report, software, workflow, modules)"
    )
    
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Run tests with coverage report"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true", 
        help="Verbose output"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available test categories"
    )
    
    parser.add_argument(
        "--pytest-args",
        nargs="*",
        help="Additional arguments to pass to pytest"
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.list:
        runner.list_available_tests()
        return
    
    # Build and run pytest command
    cmd = runner.build_pytest_command(args)
    success = runner.run_command(cmd)
    
    if not success:
        print("\n❌ Tests failed!")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()