"""
Client A Launcher (Master Instance)

Launches the primary pyWATS client instance with instance_id="default".
This is the master instance - simulates a live production installation.

Instance Configuration (System-wide):
- Instance ID: "default"
- Config: C:/ProgramData/Virinco/pyWATS/instances/default/client_config.json
- Queue: C:/ProgramData/Virinco/pyWATS/instances/default/queue/
- Logs: C:/ProgramData/Virinco/pyWATS/instances/default/logs/

Features:
- Persistent system tray icon (always visible)
- Runs current workspace code directly (zero-overhead dev testing)

Usage:
    python run_client_a.py
"""

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)


def main():
    """Launch Client A (master instance) with tray icon."""
    from pywats_client.launcher import launch_client
    return launch_client(
        instance_id="default",
        instance_name="Client A (Master)",
        enable_tray=True
    )


if __name__ == "__main__":
    sys.exit(main())
