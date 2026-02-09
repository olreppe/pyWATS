# pywats_ui.dialogs - Class Reference

Auto-generated class reference for `pywats_ui.dialogs`.

---

## `dialogs.login_window`

### `AuthWorker(QObject)`

_Worker for performing authentication in a separate thread._

**Class Variables:**
- `finished`

**Methods:**
- `run() -> Any`

---

### `LoginWindow(QDialog)`

_Login dialog for pyWATS Client authentication._

**Class Variables:**
- `authenticated`

**Methods:**
- `show_login_dialog(cls, config: Optional[...], parent) -> Optional[...]`

---

## `dialogs.settings_dialog`

### `APIGeneralSettingsPanel(SettingsPanel)`

_General API settings panel._

**Methods:**
- `load_settings(config: Any) -> Any`
- `save_settings(config: Any) -> Any`
- `setup_ui() -> Any`

---

### `AppDomainPanel(DomainSettingsPanel)`

_App/Statistics domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

---

### `AssetDomainPanel(DomainSettingsPanel)`

_Asset domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

---

### `ClientConnectionPanel(SettingsPanel)`

_Client connection settings._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `ClientConverterPanel(SettingsPanel)`

_Client converter settings._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `ClientLocationPanel(SettingsPanel)`

_Client location services settings._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `ClientObservabilityPanel(SettingsPanel)`

_Client observability settings - metrics and health endpoints._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `ClientPerformancePanel(SettingsPanel)`

_Client performance settings - HTTP caching and queue configuration._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `ClientProxyPanel(SettingsPanel)`

_Client proxy settings - full configuration matching WATS Client design._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `DomainSettingsPanel(SettingsPanel)`

_Base panel for domain-specific settings._

**Class Variables:**
- `domain_name: str`
- `domain_description: str`

**Methods:**
- `load_domain_specific_settings(config: Any) -> Any`
- `load_settings(config: Any) -> Any`
- `save_domain_specific_settings(config: Any) -> Any`
- `save_settings(config: Any) -> Any`
- `setup_domain_specific_ui() -> Any`
- `setup_ui() -> Any`

---

### `GUIAppearancePanel(SettingsPanel)`

_GUI appearance settings._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `GUIStartupPanel(SettingsPanel)`

_GUI startup and window settings._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `GUITabsPanel(SettingsPanel)`

_GUI tabs visibility settings._

**Methods:**
- `load_settings(config: ClientConfig) -> Any`
- `save_settings(config: ClientConfig) -> Any`
- `setup_ui() -> Any`

---

### `ProcessDomainPanel(DomainSettingsPanel)`

_Process domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

**Methods:**
- `load_domain_specific_settings(config: Any) -> Any`
- `save_domain_specific_settings(config: Any) -> Any`
- `setup_domain_specific_ui() -> Any`

---

### `ProductDomainPanel(DomainSettingsPanel)`

_Product domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

**Methods:**
- `load_domain_specific_settings(config: Any) -> Any`
- `save_domain_specific_settings(config: Any) -> Any`
- `setup_domain_specific_ui() -> Any`

---

### `ProductionDomainPanel(DomainSettingsPanel)`

_Production domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

**Methods:**
- `load_domain_specific_settings(config: Any) -> Any`
- `save_domain_specific_settings(config: Any) -> Any`
- `setup_domain_specific_ui() -> Any`

---

### `ReportDomainPanel(DomainSettingsPanel)`

_Report domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

**Methods:**
- `load_domain_specific_settings(config: Any) -> Any`
- `save_domain_specific_settings(config: Any) -> Any`
- `setup_domain_specific_ui() -> Any`

---

### `RootCauseDomainPanel(DomainSettingsPanel)`

_RootCause domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

---

### `SettingsDialog(QDialog)`

_Settings dialog with TreeView navigation._

**Class Variables:**
- `settings_changed`

**Methods:**
- `closeEvent(event: QCloseEvent) -> Any`

---

### `SettingsPanel(QWidget)`

_Base class for all settings panels._

**Class Variables:**
- `settings_changed`

**Properties:**
- `is_modified`

**Methods:**
- `clear_modified() -> Any`
- `load_settings(config: Any) -> Any`
- `mark_modified() -> Any`
- `save_settings(config: Any) -> Any`
- `setup_ui() -> Any`

---

### `SoftwareDomainPanel(DomainSettingsPanel)`

_Software domain settings._

**Class Variables:**
- `domain_name`
- `domain_description`

**Methods:**
- `load_domain_specific_settings(config: Any) -> Any`
- `save_domain_specific_settings(config: Any) -> Any`
- `setup_domain_specific_ui() -> Any`

---
