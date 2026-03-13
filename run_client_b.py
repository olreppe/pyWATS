"""
Client B Launcher (Secondary Instance)

Launches the secondary pyWATS client instance with instance_id="client_b".
Uses token sharing from Client A if no API token is configured.

Instance Configuration (System-wide):
- Instance ID: "client_b"
- Config: C:/ProgramData/Virinco/pyWATS/instances/client_b/client_config.json
- Queue: C:/ProgramData/Virinco/pyWATS/instances/client_b/queue/
- Logs: C:/ProgramData/Virinco/pyWATS/instances/client_b/logs/

Usage:
    python run_client_b.py
"""

import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)


def main():
    """Launch Client B (secondary instance) with token sharing from A."""
    from pywats_client.launcher import launch_client
    return launch_client(
        instance_id="client_b",
        instance_name="Client B (Secondary)",
        share_token_from="default",
        enable_tray=False
    )


if __name__ == "__main__":
    sys.exit(main())
