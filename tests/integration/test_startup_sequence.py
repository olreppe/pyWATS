"""
Tests for client startup sequence and launcher infrastructure.

Validates:
- Shared launcher module works correctly
- Config loading/creation with proper instance paths
- Token sharing between instances
- Tray icon integration setup
- Startup sequence: service > client > UI
"""
import os
import json
import pytest
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch, MagicMock

if TYPE_CHECKING:
    from pywats_client.core.config import ClientConfig


@pytest.fixture
def test_token() -> str:
    """Get API token from env var or test fixture config."""
    token = os.environ.get("PYWATS_API_TOKEN", "")
    if not token:
        from cross_cutting.test_instances import get_test_instance_manager
        config = get_test_instance_manager().get_test_instance_config("A")
        token = config.token
    if not token:
        pytest.skip("No API token available (env or fixture config)")
    return token


class TestLauncherConfigLoading:
    """Test the shared launcher config loading logic."""

    def test_get_instance_base_path_windows(self) -> None:
        """Base path uses PROGRAMDATA on Windows."""
        from pywats_client.launcher import get_instance_base_path

        with patch("os.name", "nt"):
            with patch.dict(os.environ, {"PROGRAMDATA": "C:\\ProgramData"}):
                path = get_instance_base_path()
                assert "Virinco" in str(path)
                assert "pyWATS" in str(path)
                assert "instances" in str(path)

    def test_get_instance_base_path_linux(self) -> None:
        """Base path uses /var/lib/pywats on Linux."""
        from pywats_client.launcher import get_instance_base_path

        with patch("os.name", "posix"):
            path = get_instance_base_path()
            assert str(path) == "/var/lib/pywats/instances"

    def test_load_or_create_config_creates_new(self, tmp_path: Path) -> None:
        """Creating config for new instance sets name and creates dirs."""
        from pywats_client.launcher import load_or_create_config

        with patch("pywats_client.launcher.get_instance_base_path", return_value=tmp_path):
            config = load_or_create_config(
                instance_id="test_new",
                instance_name="Test New Instance"
            )

        assert config.instance_name == "Test New Instance"
        assert (tmp_path / "test_new" / "queue").is_dir()
        assert (tmp_path / "test_new" / "logs").is_dir()
        assert (tmp_path / "test_new" / "reports").is_dir()
        assert (tmp_path / "test_new" / "converters").is_dir()

    def test_load_or_create_config_loads_existing(self, tmp_path: Path) -> None:
        """Loading existing config reads from disk."""
        from pywats_client.launcher import load_or_create_config
        from pywats_client.core.config import ClientConfig

        # Create a config file first
        config_dir = tmp_path / "existing"
        config_dir.mkdir()
        config_path = config_dir / "client_config.json"
        cfg = ClientConfig(instance_id="existing")
        cfg.instance_name = "Existing Instance"
        cfg._config_path = config_path
        cfg.save()

        with patch("pywats_client.launcher.get_instance_base_path", return_value=tmp_path):
            loaded = load_or_create_config(
                instance_id="existing",
                instance_name="Ignored Name"
            )

        assert loaded.instance_name == "Existing Instance"


class TestTokenSharing:
    """Test API token sharing between client instances."""

    def test_share_token_from_instance(self, tmp_path: Path, test_token: str) -> None:
        """Token sharing copies token from source instance."""
        from pywats_client.launcher import share_token_from_instance
        from pywats_client.core.config import ClientConfig

        # Create source config with token
        source_dir = tmp_path / "default"
        source_dir.mkdir()
        source_cfg = ClientConfig(instance_id="default")
        source_cfg.api_token = test_token
        source_cfg.service_address = "https://python.wats.com"
        source_cfg._config_path = source_dir / "client_config.json"
        source_cfg.save()

        # Create target config without token
        target_cfg = ClientConfig(instance_id="client_b")
        target_cfg.api_token = ""

        with patch("pywats_client.launcher.get_instance_base_path", return_value=tmp_path):
            result = share_token_from_instance(target_cfg, "default")

        assert result is True
        assert target_cfg.api_token == test_token
        assert target_cfg.service_address == "https://python.wats.com"

    def test_share_token_skipped_when_already_set(self, tmp_path: Path, test_token: str) -> None:
        """Token sharing is skipped if target already has a token."""
        from pywats_client.launcher import share_token_from_instance
        from pywats_client.core.config import ClientConfig

        target_cfg = ClientConfig(instance_id="client_b")
        target_cfg.api_token = test_token

        with patch("pywats_client.launcher.get_instance_base_path", return_value=tmp_path):
            result = share_token_from_instance(target_cfg, "default")

        assert result is False
        assert target_cfg.api_token == test_token

    def test_share_token_from_nonexistent_source(self, tmp_path: Path) -> None:
        """Token sharing fails gracefully when source doesn't exist."""
        from pywats_client.launcher import share_token_from_instance
        from pywats_client.core.config import ClientConfig

        target_cfg = ClientConfig(instance_id="client_b")
        target_cfg.api_token = ""

        with patch("pywats_client.launcher.get_instance_base_path", return_value=tmp_path):
            result = share_token_from_instance(target_cfg, "nonexistent")

        assert result is False
        assert target_cfg.api_token == ""


class TestMigrateOldConfig:
    """Test legacy config migration."""

    def test_migrate_from_old_config(self, tmp_path: Path, test_token: str) -> None:
        """Migration copies settings from legacy config."""
        from pywats_client.launcher import migrate_old_config
        from pywats_client.core.config import ClientConfig

        # Create legacy config
        old_config_path = tmp_path / "config.json"
        old_config_path.write_text(json.dumps({
            "service_address": "https://python.wats.com",
            "api_token": test_token,
            "station_name": "TEST-STATION-A",
            "location": "Test Lab Alpha",
        }))

        # Create empty target config
        cfg = ClientConfig(instance_id="default")
        cfg.service_address = ""
        cfg.api_token = ""

        result = migrate_old_config(old_config_path, cfg, "default")

        assert result is True
        assert cfg.service_address == "https://python.wats.com"
        assert cfg.api_token == test_token
        assert cfg.station_name == "TEST-STATION-A"

    def test_migrate_skipped_when_configured(self, tmp_path: Path, test_token: str) -> None:
        """Migration is skipped if target already has settings."""
        from pywats_client.launcher import migrate_old_config
        from pywats_client.core.config import ClientConfig

        old_config_path = tmp_path / "config.json"
        old_config_path.write_text(json.dumps({
            "service_address": "https://live.wats.com",
            "api_token": test_token,
        }))

        cfg = ClientConfig(instance_id="default")
        cfg.service_address = "https://python.wats.com"
        cfg.api_token = test_token

        result = migrate_old_config(old_config_path, cfg, "default")

        assert result is False
        assert cfg.service_address == "https://python.wats.com"

    def test_migrate_nonexistent_old_config(self, tmp_path: Path) -> None:
        """Migration handles missing legacy config gracefully."""
        from pywats_client.launcher import migrate_old_config
        from pywats_client.core.config import ClientConfig

        cfg = ClientConfig(instance_id="default")
        result = migrate_old_config(tmp_path / "nonexistent.json", cfg, "default")
        assert result is False


class TestStartupSequence:
    """Tests to verify the expected startup sequence: service > client > UI."""

    def test_run_client_a_imports_launcher(self) -> None:
        """run_client_a.py delegates to the shared launcher."""
        import run_client_a
        # The module should have a main function
        assert callable(run_client_a.main)

    def test_run_client_b_imports_launcher(self) -> None:
        """run_client_b.py delegates to the shared launcher."""
        import run_client_b
        assert callable(run_client_b.main)

    def test_client_a_uses_default_instance(self) -> None:
        """Client A uses instance_id='default'."""
        # Verify by checking the launcher call would use "default"
        import run_client_a
        import inspect
        source = inspect.getsource(run_client_a.main)
        assert 'instance_id="default"' in source

    def test_client_b_uses_client_b_instance(self) -> None:
        """Client B uses instance_id='client_b'."""
        import run_client_b
        import inspect
        source = inspect.getsource(run_client_b.main)
        assert 'instance_id="client_b"' in source

    def test_client_a_enables_tray(self) -> None:
        """Client A has persistent tray icon enabled."""
        import run_client_a
        import inspect
        source = inspect.getsource(run_client_a.main)
        assert "enable_tray=True" in source

    def test_client_b_no_tray(self) -> None:
        """Client B does not have tray icon by default."""
        import run_client_b
        import inspect
        source = inspect.getsource(run_client_b.main)
        assert "enable_tray=False" in source

    def test_client_b_shares_token_from_a(self) -> None:
        """Client B inherits token from Client A."""
        import run_client_b
        import inspect
        source = inspect.getsource(run_client_b.main)
        assert 'share_token_from="default"' in source


class TestConfigPersistence:
    """Tests that config survives save → reload (simulated restart)."""

    def test_service_address_persists_across_reload(self, tmp_path: Path, test_token: str) -> None:
        """service_address survives save → new ClientConfig.load()."""
        from pywats_client.core.config import ClientConfig

        config_path = tmp_path / "persist_test.json"

        # First "process": create and save
        cfg1 = ClientConfig(instance_id="persist-test")
        cfg1.service_address = "https://python.wats.com"
        cfg1.api_token = test_token
        cfg1.station_name = "TEST-STATION-A"
        cfg1.save(str(config_path))

        # Second "process": load from disk (simulate restart)
        cfg2 = ClientConfig.load(str(config_path))

        assert cfg2.service_address == "https://python.wats.com"
        assert cfg2.api_token == test_token
        assert cfg2.station_name == "TEST-STATION-A"
        assert cfg2.instance_id == "persist-test"

    def test_runtime_credentials_fallback_to_env_vars(self, test_token: str) -> None:
        """get_runtime_credentials falls back to env vars when config is empty."""
        from pywats_client.core.config import ClientConfig

        cfg = ClientConfig(instance_id="env-test")
        cfg.service_address = ""
        cfg.api_token = ""

        env = {
            "PYWATS_SERVER_URL": "https://python.wats.com",
            "PYWATS_API_TOKEN": test_token,
        }
        with patch.dict(os.environ, env, clear=False):
            url, token = cfg.get_runtime_credentials()

        assert url == "https://python.wats.com"
        assert token == test_token

    def test_runtime_credentials_prefer_config_over_env(self, test_token: str) -> None:
        """get_runtime_credentials prefers config values over env vars."""
        from pywats_client.core.config import ClientConfig

        cfg = ClientConfig(instance_id="pref-test")
        cfg.service_address = "https://python.wats.com"
        cfg.api_token = test_token

        # Use different values in env to verify config takes priority
        env = {
            "PYWATS_SERVER_URL": "https://live.wats.com",
            "PYWATS_API_TOKEN": "env_should_not_win",
        }
        with patch.dict(os.environ, env, clear=False):
            url, token = cfg.get_runtime_credentials()

        assert url == "https://python.wats.com"
        assert token == test_token

    def test_proxy_settings_persist(self, tmp_path: Path) -> None:
        """Proxy settings survive save → reload."""
        from pywats_client.core.config import ClientConfig

        config_path = tmp_path / "proxy_persist.json"

        cfg1 = ClientConfig(instance_id="proxy-test")
        cfg1.proxy_mode = "manual"
        cfg1.proxy_host = "proxy.company.com"
        cfg1.proxy_port = 8080
        cfg1.save(str(config_path))

        cfg2 = ClientConfig.load(str(config_path))

        assert cfg2.proxy_mode == "manual"
        assert cfg2.proxy_host == "proxy.company.com"
        assert cfg2.proxy_port == 8080


class TestStartupOrder:
    """Tests that the launcher enforces service → client → UI startup order."""

    def test_launch_client_loads_config_before_gui(self) -> None:
        """launch_client() calls load_or_create_config before creating the window."""
        import inspect
        from pywats_client.launcher import launch_client

        source = inspect.getsource(launch_client)
        config_idx = source.find("config = load_or_create_config")
        # Look for actual window instantiation, not the import statement
        window_idx = source.find("window = ConfiguratorMainWindow")

        assert config_idx > 0, "launch_client should call load_or_create_config"
        assert window_idx > 0, "launch_client should instantiate ConfiguratorMainWindow"
        assert config_idx < window_idx, "Config loading must happen before window creation"

    def test_load_or_create_runs_migration_before_token_sharing(self) -> None:
        """load_or_create_config() runs migration before token sharing."""
        import inspect
        from pywats_client.launcher import load_or_create_config

        source = inspect.getsource(load_or_create_config)
        migrate_idx = source.find("migrate_old_config")
        share_idx = source.find("share_token_from_instance")

        assert migrate_idx > 0, "load_or_create_config should call migrate_old_config"
        assert share_idx > 0, "load_or_create_config should call share_token_from_instance"
        assert migrate_idx < share_idx, "Migration must happen before token sharing"

    def test_tray_icon_created_after_window(self) -> None:
        """Tray icon is set up after window creation."""
        import inspect
        from pywats_client.launcher import launch_client

        source = inspect.getsource(launch_client)
        window_idx = source.find("ConfiguratorMainWindow")
        tray_idx = source.find("_setup_tray_for_window")

        assert window_idx > 0
        assert tray_idx > 0
        assert window_idx < tray_idx, "Tray icon must be created after window"
