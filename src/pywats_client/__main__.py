"""
pyWATS Client Entry Point

Run the client with:
    python -m pywats_client                 # Service mode (default) - runs background service
    python -m pywats_client service         # Background service mode (explicit)
    python -m pywats_client gui             # GUI only (for configuration - requires running service)
    
Or use CLI commands:
    pywats-client                           # Run background service (default)
    pywats-client service                   # Run background service
    pywats-client gui                       # Run GUI (connects to service)
    pywats-client config show               # Show configuration
    pywats-client config init               # Initialize config
    pywats-client status                    # Show status

Windows Service commands:
    pywats-client install-service           # Install Windows Service (requires admin)
    pywats-client uninstall-service         # Uninstall Windows Service (requires admin)

Or use the installed command:
    pywats-client
"""

import sys
import asyncio
import argparse
from pathlib import Path


def _check_gui_available() -> bool:
    """Check if Qt GUI is available"""
    try:
        import PySide6
        return True
    except ImportError:
        return False


def _run_gui_mode(config):
    """Run in GUI mode"""
    if not _check_gui_available():
        print("Error: GUI mode requires PySide6")
        print("Install with: pip install pywats-api[client]")
        print("Or run in headless mode: pywats-client --no-gui")
        sys.exit(1)
    
    from .gui.app import run_gui
    run_gui(config)


def _run_service_mode(instance_id: str = "default"):
    """
    Run in service mode (background process).
    
    This is the recommended way to run pyWATS Client.
    Service runs independently and can be controlled via IPC from GUI.
    """
    from .service.client_service import ClientService
    
    print(f"Starting pyWATS Client Service [instance: {instance_id}]")
    service = ClientService(instance_id)
    
    try:
        service.start()  # Blocks until stopped
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        service.stop()


def _run_headless_mode(config):
    """Run in simple headless mode (legacy - deprecated)"""
    print("Warning: Headless mode is deprecated. Use 'service' mode instead:")
    print("  python -m pywats_client service")
    print()
    
    from .core.client import WATSClient
    
    async def run_headless():
        client = WATSClient(config)
        try:
            await client.start()
            # Keep running until interrupted
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            await client.stop()
    
    asyncio.run(run_headless())


def main():
    """Main entry point"""
    # Check if this is a CLI subcommand or service mode
    # CLI commands: config, status, test-connection, converters, service, gui, tray
    cli_commands = ["config", "status", "test-connection", "converters", "service", "gui", "tray"]
    
    # Handle 'service' command - run background service
    if len(sys.argv) > 1 and sys.argv[1] == "service":
        parser = argparse.ArgumentParser(
            prog="pywats-client service",
            description="Run pyWATS Client as background service"
        )
        parser.add_argument(
            "--instance-id",
            type=str,
            default="default",
            help="Instance ID (default: default)"
        )
        args = parser.parse_args(sys.argv[2:])
        _run_service_mode(args.instance_id)
        return
    
    # Handle 'gui' command - run GUI only (connects to service)
    if len(sys.argv) > 1 and sys.argv[1] == "gui":
        parser = argparse.ArgumentParser(
            prog="pywats-client gui",
            description="Run pyWATS Client GUI"
        )
        parser.add_argument(
            "--instance-id",
            type=str,
            default="default",
            help="Instance ID to connect to (default: default)"
        )
        args = parser.parse_args(sys.argv[2:])
        
        if not _check_gui_available():
            print("Error: GUI mode requires PySide6")
            print("Install with: pip install pywats-api[client]")
            sys.exit(1)
        
        from .gui.app import run_gui
        from .core.config import get_default_config_path, ClientConfig
        
        # Load config for instance
        config_path = get_default_config_path(args.instance_id)
        config = ClientConfig.load_or_create(config_path)
        
        run_gui(config, instance_id=args.instance_id)
        return
    
    # Handle 'tray' command - run system tray icon
    if len(sys.argv) > 1 and sys.argv[1] == "tray":
        parser = argparse.ArgumentParser(
            prog="pywats-client tray",
            description="Run pyWATS Client system tray icon"
        )
        parser.add_argument(
            "--instance-id",
            type=str,
            default="default",
            help="Instance ID to connect to (default: default)"
        )
        args = parser.parse_args(sys.argv[2:])
        
        if not _check_gui_available():
            print("Error: Tray icon requires PySide6")
            print("Install with: pip install pywats-api[client]")
            sys.exit(1)
        
        from .service.service_tray import main as tray_main
        sys.exit(tray_main(args.instance_id))
    
    # Handle Service installation commands (Windows/Linux/macOS)
    if len(sys.argv) > 1 and sys.argv[1] == "install-service":
        if sys.platform == "win32":
            from .control.windows_service import WindowsServiceInstaller as ServiceInstaller
            installer_type = "windows"
        elif sys.platform == "darwin":
            from .control.unix_service import MacOSServiceInstaller as ServiceInstaller
            installer_type = "macos"
        elif sys.platform.startswith("linux"):
            from .control.unix_service import LinuxServiceInstaller as ServiceInstaller
            installer_type = "linux"
        else:
            print(f"ERROR: Unsupported platform: {sys.platform}")
            sys.exit(1)
        
        parser = argparse.ArgumentParser(
            prog="pywats-client install-service",
            description="Install pyWATS Client as a system service"
        )
        parser.add_argument(
            "--instance-id",
            type=str,
            default="default",
            help="Instance ID for the service (default: default)"
        )
        parser.add_argument(
            "--config",
            type=str,
            help="Path to configuration file"
        )
        
        if installer_type == "windows":
            parser.add_argument(
                "--use-sc",
                action="store_true",
                help="Use sc.exe instead of NSSM (not recommended)"
            )
        elif installer_type == "linux":
            parser.add_argument(
                "--user",
                type=str,
                help="User to run service as (default: current user)"
            )
        elif installer_type == "macos":
            parser.add_argument(
                "--user-agent",
                action="store_true",
                help="Install as Launch Agent instead of Daemon (no root required)"
            )
        
        args = parser.parse_args(sys.argv[2:])
        
        if installer_type == "windows":
            if args.use_sc:
                success = ServiceInstaller.install_with_sc(
                    instance_id=args.instance_id,
                    config_path=args.config
                )
            else:
                success = ServiceInstaller.install_with_nssm(
                    instance_id=args.instance_id,
                    config_path=args.config
                )
        elif installer_type == "linux":
            success = ServiceInstaller.install(
                instance_id=args.instance_id,
                config_path=args.config,
                user=getattr(args, 'user', None)
            )
        elif installer_type == "macos":
            success = ServiceInstaller.install(
                instance_id=args.instance_id,
                config_path=args.config,
                user_agent=getattr(args, 'user_agent', False)
            )
        
        sys.exit(0 if success else 1)
    
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall-service":
        if sys.platform == "win32":
            from .control.windows_service import WindowsServiceInstaller as ServiceInstaller
            installer_type = "windows"
        elif sys.platform == "darwin":
            from .control.unix_service import MacOSServiceInstaller as ServiceInstaller
            installer_type = "macos"
        elif sys.platform.startswith("linux"):
            from .control.unix_service import LinuxServiceInstaller as ServiceInstaller
            installer_type = "linux"
        else:
            print(f"ERROR: Unsupported platform: {sys.platform}")
            sys.exit(1)
        
        parser = argparse.ArgumentParser(
            prog="pywats-client uninstall-service",
            description="Uninstall pyWATS Client system service"
        )
        parser.add_argument(
            "--instance-id",
            type=str,
            default="default",
            help="Instance ID of the service to remove (default: default)"
        )
        
        if installer_type == "windows":
            parser.add_argument(
                "--use-sc",
                action="store_true",
                help="Use sc.exe instead of NSSM (not recommended)"
            )
        elif installer_type == "macos":
            parser.add_argument(
                "--user-agent",
                action="store_true",
                help="Uninstall Launch Agent instead of Daemon"
            )
        
        args = parser.parse_args(sys.argv[2:])
        
        if installer_type == "windows":
            if args.use_sc:
                success = ServiceInstaller.uninstall_with_sc(
                    instance_id=args.instance_id
                )
            else:
                success = ServiceInstaller.uninstall_with_nssm(
                    instance_id=args.instance_id
                )
        elif installer_type == "linux":
            success = ServiceInstaller.uninstall(
                instance_id=args.instance_id
            )
        elif installer_type == "macos":
            success = ServiceInstaller.uninstall(
                instance_id=args.instance_id,
                user_agent=getattr(args, 'user_agent', False)
            )
        
        sys.exit(0 if success else 1)
    
    # Handle 'service' subcommand separately (runs headless service)
    if len(sys.argv) > 1 and sys.argv[1] == "service":
        from .control.service import HeadlessService, ServiceConfig
        from .core.config import ClientConfig
        
        # Parse service-specific arguments
        parser = argparse.ArgumentParser(
            prog="pywats-client service",
            description="Run pyWATS Client in service mode (background daemon)"
        )
        parser.add_argument(
            "--config", "-c",
            type=str,
            help="Path to configuration file"
        )
        parser.add_argument(
            "--instance-id",
            type=str,
            help="Instance ID for multi-station mode"
        )
        parser.add_argument(
            "--daemon", "-d",
            action="store_true",
            help="Run as daemon (Unix only)"
        )
        parser.add_argument(
            "--api",
            action="store_true",
            help="Enable HTTP control API"
        )
        parser.add_argument(
            "--api-port",
            type=int,
            default=8765,
            help="HTTP API port (default: 8765)"
        )
        parser.add_argument(
            "--api-host",
            default="127.0.0.1",
            help="HTTP API host (default: 127.0.0.1)"
        )
        
        args = parser.parse_args(sys.argv[2:])  # Skip 'service' subcommand
        
        # Load config
        if args.config:
            config_path = Path(args.config)
            config = ClientConfig.load_or_create(config_path)
        else:
            config_dir = Path.home() / ".pywats_client"
            if args.instance_id:
                config_path = config_dir / f"config_{args.instance_id}.json"
            else:
                config_path = config_dir / "config.json"
            config = ClientConfig.load_or_create(config_path)
        
        # Apply instance ID override
        if args.instance_id:
            config.instance_id = args.instance_id
        
        # Create service config
        service_config = ServiceConfig(
            enable_api=args.api,
            api_host=args.api_host,
            api_port=args.api_port,
            daemon=args.daemon
        )
        
        # Run service
        print(f"Starting pyWATS Client Service (instance: {config.instance_id})")
        service = HeadlessService(config, service_config)
        service.run()
        sys.exit(0)
    
    if len(sys.argv) > 1 and sys.argv[1] in cli_commands:
        # Route to CLI handler
        from .control.cli import cli_main
        sys.exit(cli_main())
    
    # Legacy argument parsing for backward compatibility
    parser = argparse.ArgumentParser(
        description="pyWATS Client - WATS Test Report Management",
        epilog="""
CLI Commands (use 'pywats-client <command> --help' for details):
  service      Run in service mode (background daemon)
  config       Configuration management
  status       Show service status
  start        Start the service (with --daemon or --api options)
  stop         Stop a running daemon
  converters   Converter management
"""
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Run in headless mode without GUI"
    )
    parser.add_argument(
        "--instance-name",
        type=str,
        help="Instance name for this client"
    )
    parser.add_argument(
        "--service-address",
        type=str,
        help="WATS service address"
    )
    parser.add_argument(
        "--api-token",
        type=str,
        help="API token for authentication"
    )
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version and exit"
    )
    # New headless service options
    parser.add_argument(
        "--daemon", "-d",
        action="store_true",
        help="Run as daemon (implies --no-gui)"
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Enable HTTP control API (implies --no-gui)"
    )
    parser.add_argument(
        "--api-port",
        type=int,
        default=8765,
        help="HTTP API port (default: 8765)"
    )
    parser.add_argument(
        "--api-host",
        default="127.0.0.1",
        help="HTTP API host (default: 127.0.0.1)"
    )
    
    args = parser.parse_args()
    
    # Show version
    if args.version:
        from . import __version__
        print(f"pyWATS Client v{__version__}")
        sys.exit(0)
    
    # Load or create configuration
    from .core.config import ClientConfig
    
    if args.config:
        config_path = Path(args.config)
        config = ClientConfig.load_or_create(config_path)
    else:
        # Use default config location
        config_dir = Path.home() / ".pywats_client"
        config_path = config_dir / "config.json"
        config = ClientConfig.load_or_create(config_path)
    
    # Apply command line overrides
    if args.instance_name:
        config.instance_name = args.instance_name
    if args.service_address:
        config.service_address = args.service_address
    if args.api_token:
        config.api_token = args.api_token
    
    # Determine run mode
    # Default is now service mode (not GUI) since GUI is just for configuration
    use_gui = not args.no_gui and not args.daemon and not args.api
    
    if use_gui:
        # Explicit GUI mode requested
        print("Warning: Running GUI without explicit service mode.")
        print("The GUI is for configuration only. Make sure a service is running:")
        print("  python -m pywats_client service --instance-id default")
        print()
        _run_gui_mode(config)
    elif args.daemon or args.api:
        # Full headless service with API support
        from .control.service import HeadlessService, ServiceConfig
        
        service_config = ServiceConfig(
            enable_api=args.api,
            api_host=args.api_host,
            api_port=args.api_port,
            daemon=args.daemon,
        )
        
        service = HeadlessService(config, service_config)
        service.run()
    else:
        # Default: Run service mode
        instance_id = getattr(config, 'instance_id', 'default')
        print(f"Starting pyWATS Client Service (instance: {instance_id})")
        print("To configure, launch GUI: python -m pywats_client gui")
        print()
        _run_service_mode(instance_id)


if __name__ == "__main__":
    main()
