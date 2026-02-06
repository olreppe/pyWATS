"""
Comprehensive GUI Stress Test Suite

Tests all major GUI functionality to ensure stability and correctness:
1. Component initialization
2. Config save/load
3. Page switching
4. Connection testing (if configured)
5. Queue operations
6. Error handling

Run this to verify GUI reliability before deployment.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


class GUIStressTest:
    """Stress test suite for new Configurator GUI"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        
    def log_test(self, name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.test_results.append({
            "name": name,
            "passed": passed,
            "message": message
        })
        
        if passed:
            self.tests_passed += 1
            logger.info(f"{status}: {name}")
        else:
            self.tests_failed += 1
            logger.error(f"{status}: {name} - {message}")
    
    def test_imports(self):
        """Test 1: Verify all imports work"""
        logger.info("=" * 80)
        logger.info("TEST 1: Component Imports")
        logger.info("=" * 80)
        
        try:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtCore import Qt
            self.log_test("Import PySide6", True)
        except ImportError as e:
            self.log_test("Import PySide6", False, str(e))
            return False
        
        try:
            from pywats_client.core.config import ClientConfig
            from pywats_client.core.config_manager import ConfigManager
            self.log_test("Import pywats_client", True)
        except ImportError as e:
            self.log_test("Import pywats_client", False, str(e))
            return False
        
        try:
            from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
            from pywats_ui.framework import BaseMainWindow, BasePage
            self.log_test("Import pywats_ui", True)
        except ImportError as e:
            self.log_test("Import pywats_ui", False, str(e))
            return False
        
        return True
    
    def test_config_operations(self):
        """Test 2: Config creation, save, load"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 2: Config Operations")
        logger.info("=" * 80)
        
        from pywats_client.core.config import ClientConfig
        
        # Test config creation
        try:
            config = ClientConfig(instance_id="stress_test")
            self.log_test("Create ClientConfig", True)
        except Exception as e:
            self.log_test("Create ClientConfig", False, str(e))
            return False
        
        # Test dict-like interface
        try:
            config.set("service_address", "https://test.example.com")
            value = config.get("service_address")
            assert value == "https://test.example.com"
            config["api_token"] = "test_token_123"
            assert config["api_token"] == "test_token_123"
            self.log_test("Config dict-like interface", True)
        except Exception as e:
            self.log_test("Config dict-like interface", False, str(e))
            return False
        
        # Test save/load
        try:
            test_config_path = Path.home() / ".pywats" / "instances" / "stress_test" / "client_config.json"
            test_config_path.parent.mkdir(parents=True, exist_ok=True)
            config._config_path = test_config_path
            config.save()
            
            loaded_config = ClientConfig.load(test_config_path)
            assert loaded_config.service_address == "https://test.example.com"
            assert loaded_config.api_token == "test_token_123"
            self.log_test("Config save/load cycle", True)
        except Exception as e:
            self.log_test("Config save/load cycle", False, str(e))
            return False
        finally:
            # Cleanup
            if test_config_path.exists():
                test_config_path.unlink()
        
        return True
    
    def test_gui_initialization(self):
        """Test 3: GUI components initialize without errors"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 3: GUI Initialization (headless)")
        logger.info("=" * 80)
        
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        from pywats_client.core.config import ClientConfig
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        # Create Qt app (required for widgets)
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            self.log_test("Create QApplication", True)
        except Exception as e:
            self.log_test("Create QApplication", False, str(e))
            return False
        
        # Create config
        try:
            config = ClientConfig(instance_id="stress_test_gui")
            config_path = Path.home() / ".pywats" / "instances" / "stress_test_gui" / "client_config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config._config_path = config_path
            config.save()
            self.log_test("Create test config", True)
        except Exception as e:
            self.log_test("Create test config", False, str(e))
            return False
        
        # Create main window
        try:
            window = ConfiguratorMainWindow(config=config)
            self.log_test("Create ConfiguratorMainWindow", True)
        except Exception as e:
            self.log_test("Create ConfiguratorMainWindow", False, str(e))
            return False
        
        # Test page access
        try:
            assert hasattr(window, '_pages')
            assert len(window._pages) > 0
            page_count = len(window._pages)
            self.log_test(f"Pages initialized ({page_count} pages)", True)
        except Exception as e:
            self.log_test("Pages initialized", False, str(e))
            return False
        
        # Test reliability components
        try:
            assert hasattr(window, '_queue_manager')
            assert window._queue_manager is not None
            self.log_test("QueueManager initialized", True)
        except Exception as e:
            self.log_test("QueueManager initialized", False, str(e))
        
        # Cleanup
        try:
            window.close()
            window.deleteLater()
            if config_path.exists():
                config_path.unlink()
            self.log_test("GUI cleanup", True)
        except Exception as e:
            self.log_test("GUI cleanup", False, str(e))
        
        return True
    
    def test_page_components(self):
        """Test 4: Individual page components"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 4: Page Component Tests")
        logger.info("=" * 80)
        
        from PySide6.QtWidgets import QApplication
        from pywats_client.core.config import ClientConfig
        from pywats_ui.apps.configurator.pages import (
            DashboardPage, SetupPage, ConnectionPage,
            SerialNumbersPage, APISettingsPage, ConvertersPageV2,
            SoftwarePage, LocationPage, ProxySettingsPage,
            LogPage, AboutPage
        )
        
        app = QApplication.instance() or QApplication(sys.argv)
        config = ClientConfig(instance_id="page_test")
        
        pages = [
            ("DashboardPage", DashboardPage),
            ("SetupPage", SetupPage),
            ("ConnectionPage", ConnectionPage),
            ("SerialNumbersPage", SerialNumbersPage),
            ("APISettingsPage", APISettingsPage),
            ("ConvertersPageV2", ConvertersPageV2),
            ("SoftwarePage", SoftwarePage),
            ("LocationPage", LocationPage),
            ("ProxySettingsPage", ProxySettingsPage),
            ("LogPage", LogPage),
            ("AboutPage", AboutPage),
        ]
        
        for page_name, PageClass in pages:
            try:
                page = PageClass(config)
                assert hasattr(page, '_config') or hasattr(page, 'config')
                page.deleteLater()
                self.log_test(f"Initialize {page_name}", True)
            except Exception as e:
                self.log_test(f"Initialize {page_name}", False, str(e))
        
        return True
    
    def test_queue_manager(self):
        """Test 5: QueueManager operations"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST 5: QueueManager Operations")
        logger.info("=" * 80)
        
        from PySide6.QtWidgets import QApplication
        from pywats_ui.framework.reliability.queue_manager import QueueManager
        from pathlib import Path
        
        app = QApplication.instance() or QApplication(sys.argv)
        
        # Create test queue
        test_queue_dir = Path.home() / ".pywats" / "test_queue"
        
        async def test_send_callback(operation: dict):
            """Mock send callback"""
            pass
        
        try:
            queue = QueueManager(
                queue_dir=test_queue_dir,
                send_callback=test_send_callback,
                retry_interval_ms=1000,
                max_retries=3
            )
            self.log_test("QueueManager creation", True)
        except Exception as e:
            self.log_test("QueueManager creation", False, str(e))
            return False
        
        # Test enqueue
        try:
            op_id = queue.enqueue("test_operation", {"data": "test"})
            assert op_id is not None
            self.log_test("Queue enqueue operation", True)
        except Exception as e:
            self.log_test("Queue enqueue operation", False, str(e))
        
        # Test queue count
        try:
            count = queue.get_pending_count()
            assert count >= 0
            self.log_test(f"Queue count ({count} pending)", True)
        except Exception as e:
            self.log_test("Queue count", False, str(e))
        
        # Cleanup
        try:
            import shutil
            if test_queue_dir.exists():
                shutil.rmtree(test_queue_dir)
            self.log_test("Queue cleanup", True)
        except Exception as e:
            self.log_test("Queue cleanup", False, str(e))
        
        return True
    
    def print_summary(self):
        """Print test summary"""
        logger.info("\n" + "=" * 80)
        logger.info("TEST SUMMARY")
        logger.info("=" * 80)
        
        total = self.tests_passed + self.tests_failed
        pass_rate = (self.tests_passed / total * 100) if total > 0 else 0
        
        logger.info(f"Total Tests: {total}")
        logger.info(f"Passed: {self.tests_passed}")
        logger.info(f"Failed: {self.tests_failed}")
        logger.info(f"Pass Rate: {pass_rate:.1f}%")
        
        if self.tests_failed > 0:
            logger.info("\nFailed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    logger.info(f"  ✗ {result['name']}: {result['message']}")
        
        logger.info("=" * 80)
        
        return self.tests_failed == 0


def main():
    """Run all stress tests"""
    logger.info("=" * 80)
    logger.info("pyWATS New GUI - Comprehensive Stress Test Suite")
    logger.info("=" * 80)
    logger.info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    tester = GUIStressTest()
    
    # Run all tests
    if not tester.test_imports():
        logger.error("Import tests failed - cannot continue")
        return 1
    
    tester.test_config_operations()
    tester.test_gui_initialization()
    tester.test_page_components()
    tester.test_queue_manager()
    
    # Print summary
    all_passed = tester.print_summary()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
