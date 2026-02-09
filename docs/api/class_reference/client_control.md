# pywats_client.control - Class Reference

Auto-generated class reference for `pywats_client.control`.

---

## `control.cli`

### `ConfigCLI`

_CLI interface for configuration management_

**Properties:**
- `config`

**Methods:**
- `disable_converter(name: str) -> Any`
- `enable_converter(name: str) -> Any`
- `get_value(key: str) -> Any`
- `init_config(server_url: Optional[...], api_token: Optional[...], station_name: Optional[...], interactive: bool) -> Any`
- `list_converters() -> List[...]`
- `set_value(key: str, value: str) -> Any`
- `show_config(format: str) -> Any`
- `show_status() -> Dict[...]`
- `test_connection() -> bool`

---

## `control.service`

### `HeadlessService`

_Headless service runner for pyWATS Client._

**Methods:**
- `run() -> int`
- `stop() -> Any`

---

### `ServiceConfig`

_Configuration for headless service wrapper_

**Class Variables:**
- `log_to_file: bool`
- `log_file: str`
- `log_level: str`

---

## `control.service_adapter`

### `LinuxSystemdAdapter(ServiceAdapter)`

_Linux Service using systemd_

**Properties:**
- `platform_name`
- `requires_admin`

**Methods:**
- `get_status(instance_id) -> ServiceStatus`
- `install(instance_id, startup, config_path) -> bool`
- `is_installed(instance_id) -> bool`
- `restart(instance_id) -> bool`
- `start(instance_id) -> bool`
- `stop(instance_id) -> bool`
- `uninstall(instance_id) -> bool`

---

### `MacOSLaunchdAdapter(ServiceAdapter)`

_macOS Service using launchd_

**Properties:**
- `platform_name`
- `requires_admin`

**Methods:**
- `get_status(instance_id) -> ServiceStatus`
- `install(instance_id, startup, config_path) -> bool`
- `is_installed(instance_id) -> bool`
- `restart(instance_id) -> bool`
- `start(instance_id) -> bool`
- `stop(instance_id) -> bool`
- `uninstall(instance_id) -> bool`

---

### `ServiceAdapter(ABC)`

_Abstract base class for platform-specific service adapters._

**Properties:**
- `platform_name`
- `requires_admin`

**Methods:**
- `get_status(instance_id: str) -> ServiceStatus`
- `install(instance_id: str, startup: str, config_path: Optional[...]) -> bool`
- `is_installed(instance_id: str) -> bool`
- `restart(instance_id: str) -> bool`
- `start(instance_id: str) -> bool`
- `stop(instance_id: str) -> bool`
- `uninstall(instance_id: str) -> bool`

---

### `ServiceState(Enum)`

_Cross-platform service states_

**Class Variables:**
- `UNKNOWN`
- `STOPPED`
- `STARTING`
- `RUNNING`
- `STOPPING`
- `PAUSED`
- `NOT_INSTALLED`

---

### `ServiceStatus`

_Cross-platform service status_

**Class Variables:**
- `state: ServiceState`
- `name: str`
- `display_name: str`
- `instance_id: str`
- `pid: Optional[...]`
- `message: str`

---

### `WindowsNSSMAdapter(ServiceAdapter)`

_Windows Service using NSSM wrapper_

**Properties:**
- `platform_name`
- `requires_admin`

**Methods:**
- `get_status(instance_id) -> ServiceStatus`
- `install(instance_id, startup, config_path) -> bool`
- `is_installed(instance_id) -> bool`
- `restart(instance_id) -> bool`
- `start(instance_id) -> bool`
- `stop(instance_id) -> bool`
- `uninstall(instance_id) -> bool`

---

### `WindowsNativeServiceAdapter(ServiceAdapter)`

_Windows Service using pywin32 - appears in Task Manager_

**Properties:**
- `platform_name`
- `requires_admin`

**Methods:**
- `get_status(instance_id) -> ServiceStatus`
- `install(instance_id, startup, config_path) -> bool`
- `is_installed(instance_id) -> bool`
- `restart(instance_id) -> bool`
- `start(instance_id) -> bool`
- `stop(instance_id) -> bool`
- `uninstall(instance_id) -> bool`

---

## `control.unix_service`

### `LinuxServiceInstaller`

_Installs pyWATS Client as a systemd service on Linux._

**Class Variables:**
- `SERVICE_NAME`
- `SYSTEMD_DIR`

**Methods:**
- `get_service_status(cls, instance_id: str) -> Optional[...]`
- `has_systemd() -> bool`
- `install(cls, instance_id: str, config_path: Optional[...], python_exe: Optional[...], user: Optional[...], silent: bool) -> int`
- `is_root() -> bool`
- `is_service_installed(cls, instance_id: str) -> bool`
- `uninstall(cls, instance_id: str, silent: bool) -> int`

---

### `MacOSServiceInstaller`

_Installs pyWATS Client as a launchd daemon on macOS._

**Class Variables:**
- `SERVICE_LABEL`
- `LAUNCH_DAEMONS_DIR`
- `LAUNCH_AGENTS_DIR`

**Methods:**
- `get_service_status(cls, instance_id: str) -> Optional[...]`
- `install(cls, instance_id: str, config_path: Optional[...], python_exe: Optional[...], user_agent: bool, silent: bool) -> int`
- `is_root() -> bool`
- `is_service_installed(cls, instance_id: str, user_agent: bool) -> bool`
- `uninstall(cls, instance_id: str, user_agent: bool, silent: bool) -> int`

---

## `control.windows_native_service`

### `PyWATSService(Unknown)`

_Native Windows Service for pyWATS Client._

**Methods:**
- `SvcDoRun()`
- `SvcOtherEx(control: int, event_type: int, data) -> Any`
- `SvcStop()`

---

### `ServiceFramework`

---

### `win32serviceutil`

---

## `control.windows_service`

### `WindowsServiceInstaller`

_Installs pyWATS Client as a Windows Service._

**Class Variables:**
- `SERVICE_NAME`
- `SERVICE_DISPLAY_NAME`
- `SERVICE_DESCRIPTION`

**Methods:**
- `find_nssm() -> Optional[...]`
- `install_with_nssm(cls, instance_id: str, config_path: Optional[...], python_exe: Optional[...]) -> bool`
- `install_with_sc(cls, instance_id: str, config_path: Optional[...]) -> bool`
- `is_admin() -> bool`
- `uninstall_with_nssm(cls, instance_id: str) -> bool`
- `uninstall_with_sc(cls, instance_id: str) -> bool`

---
