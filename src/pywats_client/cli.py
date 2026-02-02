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

import logging
import sys
from pathlib import Path

import click

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


if __name__ == '__main__':
    cli()
