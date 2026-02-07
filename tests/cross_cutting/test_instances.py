"""
Test Instance Management

Provides persistent test client instances (ClientA, ClientB) that:
- Store configurations in tests/fixtures/instances/ (version controlled)
- Have isolated data directories in tests/fixtures/instances/data/ (gitignored)
- Can be used by tests via pytest fixtures
- Can also run with GUI for manual testing

Usage in tests:
    def test_something(wats_client):
        # wats_client is a pyWATS API client using Client A config
        pass

    def test_with_client_b(wats_client_b):
        # wats_client_b is a pyWATS API client using Client B config
        pass

Usage for manual testing:
    python -m tests.cross_cutting.test_instances --client A --gui
    python -m tests.cross_cutting.test_instances --client B --gui
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Literal, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from pywats import pyWATS
    from pywats_client.core.config import ClientConfig

logger = logging.getLogger(__name__)

# Base paths - go up from cross_cutting/ to tests/, then to fixtures/instances/
TESTS_DIR = Path(__file__).parent.parent
FIXTURES_DIR = TESTS_DIR / "fixtures"
INSTANCES_DIR = FIXTURES_DIR / "instances"
DATA_DIR = INSTANCES_DIR / "data"

# Test instance identifiers
TestInstanceID = Literal["A", "B"]


@dataclass
class InstanceConfig:
    """Configuration for a test instance."""
    instance_id: TestInstanceID
    name: str
    description: str

    # Connection settings - use environment variables or load from config file
    base_url: str = ""  # Will be loaded from config file or env
    token: str = ""  # Will be loaded from config file or env

    # Client-specific settings
    station_name: str = ""
    location: str = ""

    # Feature flags for testing different scenarios
    converters_enabled: bool = True
    offline_mode: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "name": self.name,
            "description": self.description,
            "base_url": self.base_url,
            "token": self.token,
            "station_name": self.station_name,
            "location": self.location,
            "converters_enabled": self.converters_enabled,
            "offline_mode": self.offline_mode,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InstanceConfig":
        # Map JSON keys to dataclass field names
        mapped = {
            "instance_id": data.get("instance_id", ""),
            "name": data.get("instance_name") or data.get("name", ""),
            "description": data.get("description", ""),
            "base_url": data.get("service_address") or data.get("base_url", ""),
            "token": data.get("api_token") or data.get("token", ""),
            "station_name": data.get("station_name", ""),
            "location": data.get("location", ""),
            "converters_enabled": data.get("converters_enabled", True),
            "offline_mode": data.get("offline_mode", False),
        }
        return cls(**mapped)


# Default configurations for test instances
DEFAULT_INSTANCES: Dict[TestInstanceID, InstanceConfig] = {
    "A": InstanceConfig(
        instance_id="A",
        name="Test Client A",
        description="Primary test instance - standard configuration",
        station_name="TEST-STATION-A",
        location="Test Lab Alpha",
    ),
    "B": InstanceConfig(
        instance_id="B",
        name="Test Client B",
        description="Secondary test instance - alternative configuration",
        station_name="TEST-STATION-B",
        location="Test Lab Beta",
        converters_enabled=False,  # Different config for comparison testing
    ),
}


class InstanceManager:
    """
    Manages test client instances.

    Each instance has:
    - A config file in tests/fixtures/instances/client_{id}_config.json
    - A data directory in tests/fixtures/instances/data/client_{id}/
    - Isolated reports, logs, and converter directories
    """

    def __init__(self):
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure all necessary directories exist."""
        INSTANCES_DIR.mkdir(parents=True, exist_ok=True)
        DATA_DIR.mkdir(exist_ok=True)

        # Create .gitignore for data directory
        gitignore = DATA_DIR / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text("# Ignore test instance data\n*\n!.gitignore\n")

    def get_instance_config_path(self, instance_id: TestInstanceID) -> Path:
        """Get path to instance config file."""
        return INSTANCES_DIR / f"client_{instance_id.lower()}_config.json"

    def get_instance_data_dir(self, instance_id: TestInstanceID) -> Path:
        """Get path to instance data directory."""
        data_dir = DATA_DIR / f"client_{instance_id.lower()}"
        data_dir.mkdir(exist_ok=True)
        return data_dir

    def get_test_instance_config(self, instance_id: TestInstanceID) -> InstanceConfig:
        """
        Load or create test instance configuration.

        Checks for existing config file, otherwise prompts user to create from template.
        """
        config_path = self.get_instance_config_path(instance_id)
        template_path = INSTANCES_DIR / f"client_{instance_id.lower()}_config.template.json"

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            config = InstanceConfig.from_dict(data)
            
            # Check if using placeholder token
            if not config.token or config.token == "YOUR_BASE64_ENCODED_TOKEN_HERE":
                raise ValueError(
                    f"Test instance {instance_id} config has no valid API token.\n"
                    f"Please edit: {config_path}\n"
                    f"And replace the token placeholder with a real Base64-encoded API token.\n"
                    f"You can generate tokens at: https://your-wats-server/api/token"
                )
            return config

        # Config doesn't exist - check for template
        if template_path.exists():
            raise FileNotFoundError(
                f"Test instance config not found: {config_path}\n\n"
                f"To set up test instances:\n"
                f"1. Copy the template: {template_path}\n"
                f"   To: {config_path}\n"
                f"2. Edit the config and add your real WATS server URL and API token\n"
                f"3. Re-run the tests\n\n"
                f"Note: Config files with real tokens are gitignored for security."
            )

        # No config or template - use defaults (creates config without valid token)
        config = DEFAULT_INSTANCES.get(instance_id)
        if config is None:
            raise ValueError(f"Unknown instance ID: {instance_id}")

        # Save for persistence
        self.save_test_instance_config(config)
        logger.warning(
            f"Created default config for instance {instance_id} at {config_path}. "
            f"Please edit and add valid credentials before running server tests."
        )
        return config

    def save_test_instance_config(self, config: InstanceConfig) -> None:
        """Save test instance configuration."""
        config_path = self.get_instance_config_path(config.instance_id)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, indent=2)

    def get_client_config(self, instance_id: TestInstanceID) -> "ClientConfig":
        """
        Get a ClientConfig configured for the test instance.

        Returns a ClientConfig object that can be used with pyWATSApplication.
        """
        from pywats_client.core.config import ClientConfig

        test_config = self.get_test_instance_config(instance_id)
        data_dir = self.get_instance_data_dir(instance_id)

        # Create ClientConfig with test instance settings
        client_config = ClientConfig(
            instance_id=f"TEST-{instance_id}",
            instance_name=test_config.name,
            service_address=test_config.base_url,
            api_token=test_config.token,
            station_name=test_config.station_name,
            location=test_config.location,
            # Paths relative to data directory
            reports_folder=str(data_dir / "reports"),
            converters_folder=str(data_dir / "converters"),
            log_file=str(data_dir / "client.log"),
            # Feature settings
            converters_enabled=test_config.converters_enabled,
            # Disable tray for tests
            minimize_to_tray=False,
            start_minimized=False,
        )

        # Store config path for saving
        client_config._config_path = data_dir / "config.json"

        return client_config

    def get_api_client(self, instance_id: TestInstanceID) -> "pyWATS":
        """
        Get a pyWATS API client for the test instance.

        This is a simple API client without the full application layer.
        """
        from pywats import pyWATS

        test_config = self.get_test_instance_config(instance_id)

        return pyWATS(
            base_url=test_config.base_url,
            token=test_config.token
        )

    def list_instances(self) -> Dict[TestInstanceID, InstanceConfig]:
        """List all configured test instances."""
        instances = {}
        for instance_id in ["A", "B"]:
            try:
                instances[instance_id] = self.get_test_instance_config(instance_id)
            except Exception:
                instances[instance_id] = DEFAULT_INSTANCES[instance_id]
        return instances

    def reset_instance(self, instance_id: TestInstanceID) -> None:
        """Reset a test instance to defaults."""
        import shutil

        # Remove data directory
        data_dir = self.get_instance_data_dir(instance_id)
        if data_dir.exists():
            shutil.rmtree(data_dir)

        # Remove config file
        config_path = self.get_instance_config_path(instance_id)
        if config_path.exists():
            config_path.unlink()

        logger.info(f"Reset test instance {instance_id}")


# Global manager instance
_manager: Optional[InstanceManager] = None


def get_test_instance_manager() -> InstanceManager:
    """Get the global test instance manager."""
    global _manager
    if _manager is None:
        _manager = InstanceManager()
    return _manager


# Convenience functions
def get_client_a() -> "ClientConfig":
    """Get ClientConfig for Test Instance A."""
    return get_test_instance_manager().get_client_config("A")


def get_client_b() -> "ClientConfig":
    """Get ClientConfig for Test Instance B."""
    return get_test_instance_manager().get_client_config("B")


def get_api_client_a() -> "pyWATS":
    """Get pyWATS API client for Test Instance A."""
    return get_test_instance_manager().get_api_client("A")


def get_api_client_b() -> "pyWATS":
    """Get pyWATS API client for Test Instance B."""
    return get_test_instance_manager().get_api_client("B")


# CLI for manual testing
def main():
    """CLI for managing test instances."""
    import argparse

    parser = argparse.ArgumentParser(description="Manage pyWATS test instances")
    parser.add_argument(
        "--client", "-c",
        choices=["A", "B"],
        default="A",
        help="Test instance to use (default: A)"
    )
    parser.add_argument(
        "--gui", "-g",
        action="store_true",
        help="Launch GUI with the test instance"
    )
    parser.add_argument(
        "--reset", "-r",
        action="store_true",
        help="Reset the test instance to defaults"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all test instances"
    )
    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="Show info about the test instance"
    )

    args = parser.parse_args()
    manager = get_test_instance_manager()

    if args.list:
        print("\n=== Test Instances ===")
        for instance_id, config in manager.list_instances().items():
            print(f"\nClient {instance_id}: {config.name}")
            print(f"  Description: {config.description}")
            print(f"  URL: {config.base_url}")
            print(f"  Station: {config.station_name}")
        print()
        return

    if args.reset:
        print(f"Resetting test instance {args.client}...")
        manager.reset_instance(args.client)
        print("Done!")
        return

    if args.info:
        config = manager.get_test_instance_config(args.client)
        data_dir = manager.get_instance_data_dir(args.client)
        print(f"\n=== Test Instance {args.client} ===")
        print(f"Name: {config.name}")
        print(f"Description: {config.description}")
        print(f"URL: {config.base_url}")
        print(f"Station: {config.station_name}")
        print(f"Location: {config.location}")
        print(f"Data Directory: {data_dir}")
        print()
        return

    if args.gui:
        print(f"Launching GUI with Test Instance {args.client}...")
        client_config = manager.get_client_config(args.client)

        # Import and run GUI (using new pywats_ui package)
        from pywats_ui.apps.configurator.main import main as run_gui
        run_gui()  # Uses default config
        return

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
