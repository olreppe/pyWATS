"""Tests for {{AppTitle}} application."""

import pytest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """Qt Application fixture."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_import():
    """Test that the application module can be imported."""
    from pywats_ui.apps import {{app_name}}
    assert {{app_name}}.__version__


def test_main_window_creation(qapp):
    """Test that main window can be created."""
    from pywats_ui.apps.{{app_name}}.main_window import {{AppTitle}}Window
    
    window = {{AppTitle}}Window()
    assert window.windowTitle() == "pyWATS {{AppTitle}}"
    assert window.width() == 800
    assert window.height() == 600


def test_config():
    """Test configuration management."""
    from pywats_ui.apps.{{app_name}}.config import AppConfig
    
    config = AppConfig("test_{{app_name}}")
    
    # Test default values
    assert config.get("window_width") == 800
    assert config.get("window_height") == 600
    
    # Test set/get
    config.set("custom_key", "custom_value")
    assert config.get("custom_key") == "custom_value"
    
    # Test save/load
    config.save()
    config2 = AppConfig("test_{{app_name}}")
    assert config2.get("custom_key") == "custom_value"


# Add your custom tests here
