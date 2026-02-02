"""Command-line interface for pyWATS Client service management.

Provides cross-platform commands for managing the pyWATS Client service:
- start: Start the service
- stop: Stop the service
- restart: Restart the service
- status: Show service status
- gui: Launch the GUI dashboard (if Qt available)

Example usage:
    $ pywats-client start
    $ pywats-client status
    $ pywats-client stop
    $ pywats-client gui
"""

import json
import logging
import sys
from pathlib import Path
from typing import Optional

import click

from .core.config_manager import ConfigManager
from .service_manager import ServiceManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def format_uptime(seconds: float) -> str:
    """Format uptime in seconds to human-readable string.
    
    Args:
        seconds: Uptime in seconds.
        
    Returns:
        Formatted string like "2h 34m 12s" or "45m 3s".
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    
    return " ".join(parts)


@click.group()
@click.option(
    '--instance-id',
    default='default',
    help='Service instance identifier (for running multiple instances)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose logging'
)
@click.pass_context
def cli(ctx, instance_id, verbose):
    """pyWATS Client Service Manager - Cross-platform service control.
    
    Manage pyWATS Client service across Windows, Linux, and macOS.
    """
    # Set up verbose logging if requested
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug(f"Verbose logging enabled")
    
    # Store ServiceManager in context for commands
    ctx.ensure_object(dict)
    ctx.obj['manager'] = ServiceManager(instance_id)
    ctx.obj['config_manager'] = ConfigManager(instance_id=instance_id)
    ctx.obj['instance_id'] = instance_id


@cli.command()
@click.pass_context
def start(ctx):
    """Start the pyWATS Client service.
    
    Cleans stale lock files, verifies service isn't already running,
    then starts the service using platform-specific methods.
    """
    manager: ServiceManager = ctx.obj['manager']
    instance_id = ctx.obj['instance_id']
    
    click.echo(f"Starting pyWATS Client service (instance: {instance_id})...")
    
    # Clean stale locks first
    cleaned = manager.clean_stale_locks()
    if cleaned > 0:
        click.echo(f"  Cleaned {cleaned} stale lock file(s)")
    
    # Check if already running
    if manager.is_running():
        click.secho("  Service is already running!", fg='yellow')
        status = manager.get_status()
        click.echo(f"  PID: {status['pid']}")
        if status['uptime']:
            click.echo(f"  Uptime: {format_uptime(status['uptime'])}")
        return
    
    # Start the service
    success = manager.start()
    
    if success:
        click.secho("✓ Service started successfully!", fg='green')
        
        # Show status
        status = manager.get_status()
        if status['pid']:
            click.echo(f"  PID: {status['pid']}")
        if status['log_file']:
            click.echo(f"  Logs: {status['log_file']}")
    else:
        click.secho("✗ Failed to start service", fg='red', err=True)
        click.echo("  Check logs for details", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def stop(ctx):
    """Stop the pyWATS Client service.
    
    Attempts graceful shutdown first (30s timeout), then force kills
    if the process doesn't exit cleanly.
    """
    manager: ServiceManager = ctx.obj['manager']
    instance_id = ctx.obj['instance_id']
    
    click.echo(f"Stopping pyWATS Client service (instance: {instance_id})...")
    
    # Check if running
    if not manager.is_running():
        click.secho("  Service is not running", fg='yellow')
        return
    
    # Get PID before stopping
    pid = manager.get_pid()
    if pid:
        click.echo(f"  Stopping PID: {pid}")
    
    # Stop the service
    success = manager.stop()
    
    if success:
        click.secho("✓ Service stopped successfully!", fg='green')
    else:
        click.secho("✗ Failed to stop service", fg='red', err=True)
        click.echo("  Process may require manual termination", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def restart(ctx):
    """Restart the pyWATS Client service.
    
    Stops the service (if running) then starts it again.
    """
    manager: ServiceManager = ctx.obj['manager']
    instance_id = ctx.obj['instance_id']
    
    click.echo(f"Restarting pyWATS Client service (instance: {instance_id})...")
    
    was_running = manager.is_running()
    
    if was_running:
        click.echo("  Stopping service...")
        if not manager.stop():
            click.secho("✗ Failed to stop service", fg='red', err=True)
            sys.exit(1)
        click.secho("  ✓ Stopped", fg='green')
    
    click.echo("  Starting service...")
    if not manager.start():
        click.secho("✗ Failed to start service", fg='red', err=True)
        sys.exit(1)
    
    click.secho("✓ Service restarted successfully!", fg='green')
    
    # Show status
    status = manager.get_status()
    if status['pid']:
        click.echo(f"  PID: {status['pid']}")
    if status['log_file']:
        click.echo(f"  Logs: {status['log_file']}")


@cli.command()
@click.pass_context
def status(ctx):
    """Show pyWATS Client service status.
    
    Displays detailed information including:
    - Running state
    - Process ID
    - Uptime
    - Log file location
    - Platform information
    """
    manager: ServiceManager = ctx.obj['manager']
    instance_id = ctx.obj['instance_id']
    
    click.echo(f"pyWATS Client Service Status (instance: {instance_id})")
    click.echo("=" * 60)
    
    status = manager.get_status()
    
    # Running status
    if status['running']:
        click.secho(f"  Status:      Running ✓", fg='green')
        click.echo(f"  PID:         {status['pid']}")
        
        if status['uptime']:
            uptime_str = format_uptime(status['uptime'])
            click.echo(f"  Uptime:      {uptime_str}")
    else:
        click.secho(f"  Status:      Stopped", fg='yellow')
    
    # Platform and instance
    click.echo(f"  Platform:    {status['platform']}")
    click.echo(f"  Instance ID: {status['instance_id']}")
    
    # Log file
    if status['log_file']:
        click.echo(f"  Log File:    {status['log_file']}")
    else:
        click.echo(f"  Log File:    Not found")
    
    click.echo("=" * 60)


@cli.command()
@click.pass_context
def gui(ctx):
    """Launch the pyWATS Client GUI dashboard.
    
    Checks for Qt availability and starts the service if not running.
    Opens the graphical dashboard for configuration and monitoring.
    """
    manager: ServiceManager = ctx.obj['manager']
    instance_id = ctx.obj['instance_id']
    
    # Check if Qt is available
    try:
        from PySide6.QtWidgets import QApplication
        HAS_QT = True
    except ImportError:
        HAS_QT = False
    
    if not HAS_QT:
        click.secho("✗ GUI not available", fg='red', err=True)
        click.echo("", err=True)
        click.echo("The GUI requires Qt (PySide6) which is not installed.", err=True)
        click.echo("", err=True)
        click.echo("To install GUI dependencies:", err=True)
        click.echo("  pip install pywats-api[client]", err=True)
        click.echo("", err=True)
        click.echo("Or use CLI commands instead:", err=True)
        click.echo("  pywats-client start", err=True)
        click.echo("  pywats-client status", err=True)
        sys.exit(1)
    
    # Check if service is running, start if not
    if not manager.is_running():
        click.echo("Service not running, starting...")
        if not manager.start():
            click.secho("✗ Failed to start service", fg='red', err=True)
            sys.exit(1)
        click.secho("✓ Service started", fg='green')
    
    # Launch GUI
    click.echo(f"Launching GUI dashboard (instance: {instance_id})...")
    
    try:
        # Import and launch the GUI
        # Note: This will need to be implemented in the actual dashboard module
        from pywats_client.dashboard import launch_dashboard
        
        launch_dashboard(instance_id)
        
    except ImportError:
        click.secho("✗ Dashboard module not found", fg='red', err=True)
        click.echo("", err=True)
        click.echo("The dashboard module is not available.", err=True)
        click.echo("Please ensure pywats-api[client] is properly installed.", err=True)
        sys.exit(1)
    except Exception as e:
        click.secho(f"✗ Error launching GUI: {e}", fg='red', err=True)
        logger.exception("GUI launch failed")
        sys.exit(1)


@cli.group()
@click.pass_context
def config(ctx):
    """Manage pyWATS Client configuration settings.
    
    View, modify, and reset configuration settings. Settings are stored
    in JSON format and can be edited directly or via CLI commands.
    """
    pass


@config.command('show')
@click.option(
    '--format',
    type=click.Choice(['json', 'text']),
    default='text',
    help='Output format (json or text)'
)
@click.pass_context
def config_show(ctx, format):
    """Display current configuration settings.
    
    Shows all configuration values in either human-readable text format
    or JSON format for parsing/piping.
    """
    config_mgr: ConfigManager = ctx.obj['config_manager']
    
    try:
        settings = config_mgr.load()
        
        if format == 'json':
            # Output as JSON
            click.echo(json.dumps(settings.to_dict(), indent=2))
        else:
            # Output as formatted text
            click.echo("pyWATS Client Configuration")
            click.echo("=" * 60)
            click.echo(f"Config File: {config_mgr.config_path}")
            click.echo(f"Instance ID: {config_mgr.instance_id}")
            click.echo("")
            
            # Connection settings
            click.echo("Connection:")
            click.echo(f"  Server URL:      {settings.server_url}")
            click.echo(f"  API Key:         {settings.api_key[:8]}... (hidden)" if settings.api_key else "  API Key:         (not set)")
            click.echo(f"  Username:        {settings.username or '(not set)'}")
            click.echo(f"  Timeout:         {settings.timeout_seconds}s")
            click.echo(f"  Retry Attempts:  {settings.retry_attempts}")
            click.echo("")
            
            # Caching settings
            click.echo("Caching:")
            cache_enabled = getattr(settings, 'enable_cache', True)
            cache_ttl = getattr(settings, 'cache_ttl_seconds', 300.0)
            cache_size = getattr(settings, 'cache_max_size', 1000)
            click.echo(f"  Enabled:         {cache_enabled}")
            click.echo(f"  TTL:             {cache_ttl}s")
            click.echo(f"  Max Size:        {cache_size} entries")
            click.echo("")
            
            # Metrics settings
            click.echo("Metrics:")
            metrics_enabled = getattr(settings, 'enable_metrics', True)
            metrics_port = getattr(settings, 'metrics_port', 9090)
            click.echo(f"  Enabled:         {metrics_enabled}")
            click.echo(f"  Port:            {metrics_port}")
            click.echo("")
            
            # Logging settings
            click.echo("Logging:")
            click.echo(f"  Level:           {settings.log_level}")
            click.echo("")
            
            click.echo("=" * 60)
    
    except Exception as e:
        click.secho(f"✗ Error loading configuration: {e}", fg='red', err=True)
        sys.exit(1)


@config.command('get')
@click.argument('key')
@click.pass_context
def config_get(ctx, key):
    """Get a specific configuration value.
    
    Retrieves a single configuration value by key name.
    Supports nested keys using dot notation (e.g., 'domains.report.timeout').
    
    Examples:
        pywats-client config get server_url
        pywats-client config get cache_ttl_seconds
    """
    config_mgr: ConfigManager = ctx.obj['config_manager']
    
    try:
        settings = config_mgr.load()
        settings_dict = settings.to_dict()
        
        # Support dot notation for nested keys
        value = settings_dict
        for part in key.split('.'):
            if isinstance(value, dict):
                value = value.get(part)
            else:
                value = None
                break
        
        if value is None:
            click.secho(f"✗ Key not found: {key}", fg='red', err=True)
            click.echo(f"\nAvailable keys:", err=True)
            _print_available_keys(settings_dict)
            sys.exit(1)
        
        # Output the value
        if isinstance(value, (dict, list)):
            click.echo(json.dumps(value, indent=2))
        else:
            click.echo(str(value))
    
    except Exception as e:
        click.secho(f"✗ Error: {e}", fg='red', err=True)
        sys.exit(1)


@config.command('set')
@click.argument('key')
@click.argument('value')
@click.option(
    '--type',
    type=click.Choice(['string', 'int', 'float', 'bool']),
    default='string',
    help='Value type (string, int, float, bool)'
)
@click.pass_context
def config_set(ctx, key, value, type):
    """Set a configuration value.
    
    Updates a single configuration value and saves to disk.
    Supports type conversion for int, float, and bool values.
    
    Examples:
        pywats-client config set server_url https://wats.example.com
        pywats-client config set cache_ttl_seconds 600 --type int
        pywats-client config set enable_cache true --type bool
    """
    config_mgr: ConfigManager = ctx.obj['config_manager']
    
    try:
        settings = config_mgr.load()
        
        # Convert value to appropriate type
        converted_value = _convert_value(value, type)
        
        # Set the value using setattr
        if '.' in key:
            click.secho(f"✗ Nested keys not supported for set operation", fg='red', err=True)
            click.echo("  Use 'pywats-client config edit' to modify nested values", err=True)
            sys.exit(1)
        
        if not hasattr(settings, key):
            click.secho(f"✗ Unknown key: {key}", fg='yellow')
            click.echo(f"\nAvailable keys:", err=True)
            _print_available_keys(settings.to_dict())
            click.echo(f"\nProceeding anyway (custom key)...")
        
        setattr(settings, key, converted_value)
        
        # Save the configuration
        config_mgr.save(settings)
        
        click.secho(f"✓ Configuration updated: {key} = {converted_value}", fg='green')
        click.echo(f"  Saved to: {config_mgr.config_path}")
    
    except Exception as e:
        click.secho(f"✗ Error: {e}", fg='red', err=True)
        sys.exit(1)


@config.command('reset')
@click.confirmation_option(prompt='Are you sure you want to reset all settings to defaults?')
@click.pass_context
def config_reset(ctx):
    """Reset all configuration to defaults.
    
    Resets all settings to their default values and saves to disk.
    This action requires confirmation and cannot be undone.
    """
    config_mgr: ConfigManager = ctx.obj['config_manager']
    
    try:
        settings = config_mgr.reset_to_defaults()
        click.secho("✓ Configuration reset to defaults", fg='green')
        click.echo(f"  Saved to: {config_mgr.config_path}")
    
    except Exception as e:
        click.secho(f"✗ Error: {e}", fg='red', err=True)
        sys.exit(1)


@config.command('path')
@click.pass_context
def config_path(ctx):
    """Show the configuration file path.
    
    Displays the path to the configuration file for this instance.
    Useful for finding and editing the config file directly.
    """
    config_mgr: ConfigManager = ctx.obj['config_manager']
    
    click.echo(f"Config File: {config_mgr.config_path}")
    
    if config_mgr.exists():
        click.secho("  Status: Exists ✓", fg='green')
    else:
        click.secho("  Status: Not found (will be created on first save)", fg='yellow')


@config.command('edit')
@click.pass_context
def config_edit(ctx):
    """Open configuration file in default editor.
    
    Opens the configuration file in your system's default text editor.
    Changes are applied immediately when the file is saved.
    """
    config_mgr: ConfigManager = ctx.obj['config_manager']
    
    # Ensure config file exists
    if not config_mgr.exists():
        click.echo("Creating default configuration file...")
        config_mgr.save()
    
    # Open in default editor
    try:
        import subprocess
        import platform
        
        if platform.system() == 'Windows':
            os.startfile(str(config_mgr.config_path))  # type: ignore
        elif platform.system() == 'Darwin':
            subprocess.call(['open', str(config_mgr.config_path)])
        else:
            subprocess.call(['xdg-open', str(config_mgr.config_path)])
        
        click.secho(f"✓ Opened: {config_mgr.config_path}", fg='green')
    
    except Exception as e:
        click.secho(f"✗ Error opening editor: {e}", fg='red', err=True)
        click.echo(f"\nManually edit: {config_mgr.config_path}", err=True)
        sys.exit(1)


def _convert_value(value: str, type: str):
    """Convert string value to specified type."""
    if type == 'int':
        return int(value)
    elif type == 'float':
        return float(value)
    elif type == 'bool':
        return value.lower() in ('true', '1', 'yes', 'on')
    else:
        return value


def _print_available_keys(settings_dict: dict, prefix: str = '', indent: int = 0):
    """Print available configuration keys."""
    for key, value in settings_dict.items():
        full_key = f"{prefix}.{key}" if prefix else key
        indent_str = "  " * indent
        
        if isinstance(value, dict):
            click.echo(f"{indent_str}{key}:")
            _print_available_keys(value, full_key, indent + 1)
        else:
            click.echo(f"{indent_str}{key}")


if __name__ == '__main__':
    cli()
