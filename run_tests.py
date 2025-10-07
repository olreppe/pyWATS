#!/usr/bin/env python3
"""
PyWATS Test Runner

This script provides a convenient way to run different categories of tests.
Usage:
    python run_tests.py [module] [test_type] [options]

Examples:
    python run_tests.py                    # Run all tests
    python run_tests.py unit              # Run all unit tests
    python run_tests.py models            # Run all model tests
    python run_tests.py models unit       # Run unit tests for models only
    python run_tests.py uur               # Run all UUR-related tests
    python run_tests.py --coverage        # Run with coverage report
    python run_tests.py --verbose         # Run with verbose output
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
        cmd = ["python", "-m", "pytest"]
        
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
        
        # Determine test path and markers
        test_path, markers = self.get_test_selection(args)
        
        if test_path:
            cmd.append(str(test_path))
        else:
            cmd.append(str(self.tests_dir))
            
        # Add markers
        if markers:
            cmd.extend(["-m", " and ".join(markers)])
            
        # Add any additional pytest args
        if args.pytest_args:
            cmd.extend(args.pytest_args)
            
        return cmd
    
    def get_test_selection(self, args):
        """Determine which tests to run based on arguments"""
        test_path = None
        markers = []
        
        # Module-specific paths
        module_paths = {
            "models": self.tests_dir / "unit" / "models",
            "modules": self.tests_dir / "unit" / "modules", 
            "core": self.tests_dir / "unit" / "core",
            "uut": self.tests_dir / "unit" / "models" / "report" / "uut",
            "uur": self.tests_dir / "unit" / "models" / "report" / "uur",
            "api": self.tests_dir / "unit" / "core",
            "integration": self.tests_dir / "integration",
            "e2e": self.tests_dir / "e2e"
        }
        
        # Test type paths
        type_paths = {
            "unit": self.tests_dir / "unit",
            "integration": self.tests_dir / "integration", 
            "e2e": self.tests_dir / "e2e"
        }
        
        # Check for module specification
        if args.module in module_paths:
            test_path = module_paths[args.module]
        elif args.module in type_paths:
            test_path = type_paths[args.module]
            
        # Check for test type specification
        if args.test_type:
            if args.test_type in ["unit", "integration", "e2e"]:
                markers.append(args.test_type)
            elif args.test_type in ["models", "modules", "api"]:
                markers.append(args.test_type)
                
        return test_path, markers
    
    def list_available_tests(self):
        """List all available test categories"""
        print("Available test categories:")
        print("\nTest Types:")
        print("  unit        - All unit tests")
        print("  integration - All integration tests") 
        print("  e2e         - All end-to-end tests")
        
        print("\nModules:")
        print("  models      - All model tests")
        print("  modules     - All module tests")
        print("  core        - Core functionality tests")
        print("  api         - API layer tests")
        
        print("\nSpecific Areas:")
        print("  uut         - UUT report tests")
        print("  uur         - UUR report tests")
        
        print("\nExamples:")
        print("  python run_tests.py unit models    # Unit tests for models")
        print("  python run_tests.py uur            # All UUR tests")
        print("  python run_tests.py --coverage     # All tests with coverage")


def main():
    parser = argparse.ArgumentParser(
        description="PyWATS Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "module",
        nargs="?",
        help="Module to test (models, modules, core, uut, uur, unit, integration, e2e)"
    )
    
    parser.add_argument(
        "test_type", 
        nargs="?",
        help="Type of tests to run (unit, integration, e2e, models, modules, api)"
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