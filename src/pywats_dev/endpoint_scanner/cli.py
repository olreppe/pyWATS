"""CLI command for endpoint scanning and risk assessment."""

import sys
from pathlib import Path
import argparse

from .scanner import EndpointScanner
from .analyzer import UsageAnalyzer
from .report_generator import ReportGenerator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scan pyWATS endpoints and generate risk assessment report"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("docs/INTERNAL_ENDPOINT_RISK_AUTOMATED.md"),
        help="Output path for generated report (default: docs/INTERNAL_ENDPOINT_RISK_AUTOMATED.md)"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Print report to stdout instead of writing to file"
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Only print summary statistics"
    )
    
    args = parser.parse_args()
    
    # Find project root (directory containing src/)
    try:
        cwd = Path.cwd()
        if (cwd / "src" / "pywats").exists():
            project_root = cwd
        elif (cwd.parent / "src" / "pywats").exists():
            project_root = cwd.parent
        else:
            print("❌ Error: Could not find pyWATS project root (looking for src/pywats)")
            print(f"   Current directory: {cwd}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error finding project root: {e}")
        sys.exit(1)
    
    routes_file = project_root / "src" / "pywats" / "core" / "routes.py"
    src_dir = project_root / "src" / "pywats"
    
    if not routes_file.exists():
        print(f"❌ Error: routes.py not found at {routes_file}")
        sys.exit(1)
    
    print("🔍 Scanning endpoints...")
    scanner = EndpointScanner(routes_file)
    endpoints = scanner.scan()
    print(f"   ✅ Found {len(endpoints)} endpoints")
    
    print("📊 Analyzing usage...")
    analyzer = UsageAnalyzer(src_dir)
    usage_map = analyzer.analyze(endpoints)
    
    summary = analyzer.get_usage_summary()
    print(f"   ✅ Analyzed {summary['total_endpoints']} endpoints")
    print(f"   ✅ Found {summary['total_usage_count']} total usages")
    
    if args.stats_only:
        print("\n📈 Summary Statistics:")
        print(f"   Total Endpoints: {summary['total_endpoints']}")
        print(f"   Used: {summary['used_endpoints']} ({summary['used_endpoints']/summary['total_endpoints']*100:.1f}%)")
        print(f"   Unused: {summary['unused_endpoints']}")
        print(f"   Total Usage Count: {summary['total_usage_count']}")
        print(f"   Avg Usage: {summary['avg_usage_per_endpoint']:.1f} per endpoint")
        
        print("\n🔝 Top 10 Most Used:")
        for i, usage in enumerate(analyzer.get_most_used_endpoints(10), 1):
            print(f"   {i}. {usage.endpoint_path} - {usage.usage_count}x")
        
        return
    
    print("📝 Generating report...")
    generator = ReportGenerator(endpoints, usage_map)
    report = generator.generate_full_report()
    
    if args.dry_run:
        print("\n" + "="*80)
        print(report)
        print("="*80)
    else:
        output_path = project_root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"   ✅ Report written to: {output_path}")
        print(f"\n✨ Done! Generated {len(report)} characters of analysis.")


if __name__ == "__main__":
    main()
