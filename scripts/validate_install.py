#!/usr/bin/env python3
"""
pyWATS Installation Validator

This standalone script validates that pyWATS is correctly installed and configured.
Customers run this after installation to verify everything works before production use.

Usage:
    python validate_install.py
    python validate_install.py --server-url https://your-server.wats.com
    python validate_install.py --full

Exit Codes:
    0 - All checks passed
    1 - Warnings (may work but not optimal)
    2 - Failures (will not work correctly)
"""

import sys
import os
import json
import socket
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional, Dict, Any


# =============================================================================
# Check Functions
# =============================================================================

def check_python_version() -> Tuple[bool, str]:
    """Check Python version is 3.10+"""
    version = sys.version_info
    if version >= (3, 10):
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (requires 3.10+)"


def check_pywats_import() -> Tuple[bool, str]:
    """Check pyWATS can be imported"""
    try:
        import pywats
        return True, f"pyWATS {pywats.__version__}"
    except ImportError as e:
        return False, f"Cannot import pywats: {e}"


def check_pywats_client_import() -> Tuple[bool, str]:
    """Check pyWATS Client can be imported"""
    try:
        import pywats_client
        version = getattr(pywats_client, '__version__', 'unknown')
        return True, f"pyWATS Client {version}"
    except ImportError as e:
        return False, f"Cannot import pywats_client: {e}"


def check_required_packages() -> Tuple[bool, str]:
    """Check required packages are installed"""
    required = ['httpx', 'pydantic']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "All required packages installed"


def check_optional_gui() -> Tuple[Optional[bool], str]:
    """Check GUI packages (optional)"""
    try:
        import PySide6
        return True, f"PySide6 available (GUI supported)"
    except ImportError:
        return None, "PySide6 not installed (headless only)"


def check_optional_service() -> Tuple[Optional[bool], str]:
    """Check service packages (platform-specific)"""
    if sys.platform == 'win32':
        try:
            import win32serviceutil
            return True, "pywin32 available (Windows Service supported)"
        except ImportError:
            return None, "pywin32 not installed (Windows Service unavailable)"
    return None, "Not applicable on this platform"


def check_config_directory() -> Tuple[bool, str]:
    """Check config directory exists and is writable"""
    if sys.platform == 'win32':
        config_dir = Path.home() / ".pywats_client"
    else:
        config_dir = Path.home() / ".pywats_client"
        # Also check system directory
        sys_config = Path("/etc/pywats")
        if sys_config.exists():
            config_dir = sys_config
    
    if config_dir.exists():
        test_file = config_dir / ".validation_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
            return True, f"Writable: {config_dir}"
        except PermissionError:
            return False, f"Not writable: {config_dir}"
    else:
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            return True, f"Created: {config_dir}"
        except PermissionError:
            return False, f"Cannot create: {config_dir}"


def check_network_connectivity() -> Tuple[bool, str]:
    """Check basic network connectivity"""
    test_hosts = [
        ('8.8.8.8', 53),
        ('1.1.1.1', 53),
    ]
    
    for host, port in test_hosts:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            return True, "Internet connection available"
        except (socket.timeout, socket.error):
            continue
    
    return False, "No internet connection"


def check_wats_server(server_url: str) -> Tuple[bool, str]:
    """Check WATS server connectivity"""
    try:
        import httpx
        
        with httpx.Client(timeout=15.0) as client:
            # Try version endpoint
            try:
                response = client.get(f"{server_url.rstrip('/')}/api/version")
                if response.status_code == 200:
                    try:
                        data = response.json()
                        version = data.get('version', data.get('Version', 'unknown'))
                        return True, f"WATS Server: {version}"
                    except Exception:
                        return True, "WATS Server reachable"
            except httpx.HTTPError:
                pass
            
            # Try health endpoint
            try:
                response = client.get(f"{server_url.rstrip('/')}/api/health")
                if response.status_code < 500:
                    return True, "WATS Server reachable"
            except httpx.HTTPError:
                pass
        
        return False, "Cannot reach WATS server"
    except ImportError:
        return False, "httpx not installed, cannot verify server"
    except Exception as e:
        return False, f"Error: {str(e)}"


def check_health_endpoint() -> Tuple[Optional[bool], str]:
    """Check local health endpoint (if service is running)"""
    health_port = int(os.environ.get('PYWATS_HEALTH_PORT', '8080'))
    
    try:
        sock = socket.create_connection(('127.0.0.1', health_port), timeout=2)
        sock.close()
        
        try:
            import httpx
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"http://127.0.0.1:{health_port}/health")
                if response.status_code == 200:
                    return True, f"Health endpoint OK (port {health_port})"
        except Exception:
            pass
        
        return True, f"Health endpoint listening (port {health_port})"
    except (socket.timeout, socket.error):
        return None, f"Health endpoint not running (port {health_port})"


def check_selinux() -> Tuple[Optional[bool], str]:
    """Check SELinux status (Linux only)"""
    if sys.platform != 'linux':
        return None, "Not applicable (not Linux)"
    
    if not Path('/etc/selinux').exists():
        return None, "SELinux not installed"
    
    try:
        import subprocess
        result = subprocess.run(
            ['getenforce'],
            capture_output=True,
            text=True,
            timeout=5
        )
        mode = result.stdout.strip()
        
        if mode == 'Enforcing':
            # Check for pywats policy
            result = subprocess.run(
                ['semodule', '-l'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if 'pywats' in result.stdout:
                return True, "SELinux Enforcing + pywats policy loaded"
            return False, "SELinux Enforcing but pywats policy NOT loaded"
        elif mode == 'Permissive':
            return None, "SELinux Permissive (will work, not hardened)"
        return True, f"SELinux: {mode}"
    except Exception:
        return None, "Could not check SELinux status"


# =============================================================================
# Report Generation
# =============================================================================

def run_validation(server_url: Optional[str] = None, full: bool = False) -> Dict[str, Any]:
    """Run all validation checks and return results"""
    results = {
        'timestamp': datetime.now().isoformat(),
        'platform': {
            'system': sys.platform,
            'python': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        },
        'checks': [],
        'summary': {'pass': 0, 'warn': 0, 'fail': 0}
    }
    
    # Core checks
    checks = [
        ("Python Version", check_python_version),
        ("pyWATS Library", check_pywats_import),
        ("pyWATS Client", check_pywats_client_import),
        ("Required Packages", check_required_packages),
        ("GUI Support", check_optional_gui),
        ("Service Support", check_optional_service),
        ("Config Directory", check_config_directory),
        ("Network", check_network_connectivity),
    ]
    
    # Server check
    if server_url:
        checks.append(("WATS Server", lambda: check_wats_server(server_url)))
    
    # Full checks
    if full:
        checks.append(("Health Endpoint", check_health_endpoint))
        checks.append(("SELinux", check_selinux))
    
    for name, check_fn in checks:
        try:
            passed, message = check_fn()
            
            if passed is True:
                status = 'pass'
                results['summary']['pass'] += 1
            elif passed is False:
                status = 'fail'
                results['summary']['fail'] += 1
            else:  # None = warning/skip
                status = 'warn'
                results['summary']['warn'] += 1
            
            results['checks'].append({
                'name': name,
                'status': status,
                'message': message
            })
        except Exception as e:
            results['checks'].append({
                'name': name,
                'status': 'fail',
                'message': f"Error: {str(e)}"
            })
            results['summary']['fail'] += 1
    
    # Overall status
    if results['summary']['fail'] > 0:
        results['overall'] = 'FAIL'
    elif results['summary']['warn'] > 0:
        results['overall'] = 'WARN'
    else:
        results['overall'] = 'PASS'
    
    return results


def print_results(results: Dict[str, Any]) -> None:
    """Print validation results in human-readable format"""
    symbols = {'pass': '✅', 'warn': '⚠️ ', 'fail': '❌'}
    
    print()
    print("=" * 60)
    print("  pyWATS Installation Validation")
    print("=" * 60)
    print(f"\nPlatform: {results['platform']['system']}")
    print(f"Python:   {results['platform']['python']}")
    print(f"Time:     {results['timestamp']}")
    print()
    
    for check in results['checks']:
        symbol = symbols[check['status']]
        print(f"{symbol} {check['name']}: {check['message']}")
    
    print()
    print("-" * 60)
    summary = results['summary']
    print(f"Summary: {summary['pass']} pass, {summary['warn']} warn, {summary['fail']} fail")
    
    overall_symbol = {
        'PASS': '✅',
        'WARN': '⚠️ ',
        'FAIL': '❌'
    }[results['overall']]
    
    print(f"\nOverall: {overall_symbol} {results['overall']}")
    
    if results['overall'] == 'FAIL':
        print("\n⚠️  Installation has issues that must be resolved.")
        print("   Run 'python -m pywats_client diagnose' for detailed diagnostics.")
    elif results['overall'] == 'WARN':
        print("\n⚠️  Installation will work but may have limited functionality.")
    else:
        print("\n✅ Installation validated successfully!")
    
    print("=" * 60)
    print()


# =============================================================================
# Main
# =============================================================================

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate pyWATS installation"
    )
    parser.add_argument(
        '--server-url',
        type=str,
        default=os.environ.get('PYWATS_SERVER_URL'),
        help='WATS server URL to verify connectivity'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run additional checks (health endpoint, SELinux)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Only output status (exit code indicates result)'
    )
    
    args = parser.parse_args()
    
    # Run validation
    results = run_validation(
        server_url=args.server_url,
        full=args.full
    )
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    elif not args.quiet:
        print_results(results)
    
    # Exit code
    if results['overall'] == 'FAIL':
        sys.exit(2)
    elif results['overall'] == 'WARN':
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
