# pyWATS Configuration Settings - Complete Reference

**For GUI Settings Dialog Implementation**  
**Last Updated:** 2026-02-02

This document provides a complete reference of all configuration settings across the pyWATS ecosystem (Client, Service, and API layers) for implementing the GUI settings dialog.

---

## Table of Contents

1. [Configuration Overview](#configuration-overview)
2. [Client Configuration (ClientConfig)](#client-configuration-clientconfig)
3. [API Settings (APISettings)](#api-settings-apisettings)
4. [Domain-Specific Settings](#domain-specific-settings)
5. [Service & Component Settings](#service--component-settings)
6. [Configuration File Format](#configuration-file-format)
7. [GUI Settings Dialog Sections](#gui-settings-dialog-sections)

---

## Configuration Overview

### Configuration Hierarchy

```
ClientConfig (pywats_client.core.config)
├── Instance Settings (instance_id, instance_name)
├── Server Connection (service_address, api_token, username)
├── Station Settings (station_name, location, purpose)
├── Multi-Station Mode (station_presets, active_station_key)
├── Serial Number Handler (sn_mode, sn_prefix, sn_start, etc.)
├── Proxy Settings (proxy_mode, proxy_host, proxy_port, etc.)
├── Sync Settings (sync_interval_seconds, process_sync_enabled)
├── Offline Storage (reports_folder, offline_queue_enabled)
├── HTTP Cache Settings (enable_cache, cache_ttl_seconds, cache_max_size) ⭐ NEW
├── Metrics Settings (enable_metrics, metrics_port) ⭐ NEW
├── Converters (converters: List[ConverterConfig])
├── Yield Monitor (yield_monitor_enabled, yield_threshold)
├── HTTP API (api_enabled, api_host, api_port, etc.)
├── Webhooks (webhook_converter_url, webhook_report_url, etc.)
├── GUI Settings (show_software_tab, start_minimized, etc.)
├── Logging (log_level, log_file)
└── Service (service_auto_start, auto_connect)

APISettings (pywats.core.config)
├── Connection (timeout_seconds, max_retries, retry_delay_seconds)
├── Error Handling (error_mode: STRICT | LENIENT)
├── Logging (log_requests, log_responses)
├── SSL (verify_ssl)
└── Domain Settings
    ├── product: ProductDomainSettings
    ├── report: ReportDomainSettings
    ├── production: ProductionDomainSettings
    ├── process: ProcessDomainSettings
    ├── software: SoftwareDomainSettings
    ├── asset: AssetDomainSettings
    ├── rootcause: RootCauseDomainSettings
    └── app: AppDomainSettings

ConverterConfig (pywats_client.core.config)
├── Identity (name, module_path, description)
├── Watch Folders (watch_folder, done_folder, error_folder, pending_folder)
├── Type (converter_type: FILE | FOLDER | SCHEDULED)
├── State (enabled)
├── Priority (priority: 1-10) ⭐ NEW
├── Processing (file_patterns, folder_patterns)
├── Validation (alarm_threshold, reject_threshold)
├── Retry (max_retries, retry_delay_seconds)
├── Schedule (schedule_interval_seconds, cron_expression, run_on_startup)
├── Folder Readiness (readiness_marker, min_file_count)
└── Post-processing (post_action, archive_folder)
```

---

## Client Configuration (ClientConfig)

**Location:** `src/pywats_client/core/config.py`  
**Class:** `ClientConfig`  
**File:** `config.json` in instance directory

### 1. Instance Identification

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `schema_version` | str | "2.0" | Config file format version | *(internal)* |
| `instance_id` | str | "default" | Unique instance identifier | General |
| `instance_name` | str | "WATS Client" | Human-readable name | General |

### 2. Server Connection ⭐ **CRITICAL**

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `service_address` | str | "" | WATS server URL (e.g., "https://wats.company.com") | Connection |
| `api_token` | str | "" | API token (Base64 username:password) | Connection |
| `username` | str | "" | Username for display | Connection |

### 3. Station Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `station_name` | str | "" | Station name for reports (machineName) | Station |
| `location` | str | "" | Station location | Station |
| `purpose` | str | "" | Station purpose (Production, Development, etc.) | Station |
| `station_description` | str | "" | Optional description | Station |
| `auto_detect_location` | bool | False | Use GPS/network for location | Station |
| `include_station_in_reports` | bool | True | Apply station info to reports | Station |
| `station_name_source` | str | "hostname" | Source: "hostname", "config", "manual" | Station |

### 4. Multi-Station Mode (Hub)

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `multi_station_enabled` | bool | False | Enable multi-station support | Station |
| `station_presets` | List[StationPreset] | [] | List of station configurations | Station |
| `active_station_key` | str | "" | Currently active preset | Station |

**StationPreset Fields:**
- `key` (str) - Unique identifier
- `name` (str) - Station name
- `location` (str) - Location
- `purpose` (str) - Purpose
- `description` (str) - Description
- `is_default` (bool) - Is default station

### 5. Serial Number Handler

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `sn_mode` | str | "Manual Entry" | "Manual Entry", "Auto-increment", "Barcode Scanner", "External Source" | Serial Number |
| `sn_prefix` | str | "" | Serial number prefix | Serial Number |
| `sn_start` | int | 1 | Starting number | Serial Number |
| `sn_padding` | int | 6 | Zero-padding width | Serial Number |
| `sn_com_port` | str | "Auto-detect" | COM port for barcode scanner | Serial Number |
| `sn_terminator` | str | "Enter (CR)" | Barcode terminator | Serial Number |
| `sn_validate_format` | bool | False | Validate SN format | Serial Number |
| `sn_pattern` | str | "" | Regex pattern for validation | Serial Number |
| `sn_check_duplicates` | bool | True | Check for duplicate SNs | Serial Number |

### 6. Proxy Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `proxy_mode` | str | "system" | "none", "system", "manual" | Proxy |
| `proxy_host` | str | "" | Proxy hostname | Proxy |
| `proxy_port` | int | 8080 | Proxy port | Proxy |
| `proxy_auth` | bool | False | Enable proxy authentication | Proxy |
| `proxy_username` | str | "" | Proxy username | Proxy |
| `proxy_password` | str | "" | Proxy password | Proxy |
| `proxy_bypass` | str | "" | Bypass list (comma-separated) | Proxy |

### 7. Sync Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `sync_interval_seconds` | int | 300 | Sync interval (5 minutes) | Sync |
| `process_sync_enabled` | bool | True | Enable process synchronization | Sync |

### 8. Offline Storage

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `reports_folder` | str | "reports" | Folder for offline reports | Offline |
| `offline_queue_enabled` | bool | True | Enable offline queue | Offline |
| `max_retry_attempts` | int | 5 | Max retry attempts for failed uploads | Offline |
| `retry_interval_seconds` | int | 60 | Retry interval | Offline |

### 9. Queue Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `max_queue_size` | int | 10000 | Max reports in queue (0=unlimited) | Queue |
| `max_concurrent_uploads` | int | 5 | Concurrent upload threads | Queue |

### 10. HTTP Cache Settings ⭐ **NEW** (v0.3.0+)

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `enable_cache` | bool | **True** | Enable HTTP response caching for GET requests | Performance |
| `cache_ttl_seconds` | float | **300.0** | Cache time-to-live (5 minutes) | Performance |
| `cache_max_size` | int | **1000** | Maximum cached responses | Performance |

**Cache Tuning Guidelines:**
- **Real-time data:** `enable_cache=False`
- **Reports (change frequently):** `cache_ttl_seconds=60-300` (1-5 min)
- **Products/processes:** `cache_ttl_seconds=600-3600` (10-60 min)
- **Configuration:** `cache_ttl_seconds=3600-7200` (1-2 hours)
- **Scripts:** `cache_max_size=100-500`
- **Applications:** `cache_max_size=500-1000`
- **Dashboards:** `cache_max_size=1000-5000`

### 11. Metrics & Observability Settings ⭐ **NEW** (v0.3.0+)

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `enable_metrics` | bool | **True** | Enable Prometheus metrics collection | Observability |
| `metrics_port` | int | **9090** | Prometheus metrics port | Observability |

**Related Endpoints:**
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness probe (Kubernetes)
- `GET /health/live` - Liveness probe (Kubernetes)
- `GET /metrics` - Prometheus metrics (if enabled)

### 12. Converter Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `converters_folder` | str | "converters" | Folder for converter modules | Converters |
| `converters` | List[ConverterConfig] | [] | List of converter configurations | Converters |
| `converters_enabled` | bool | True | Global converter enable/disable | Converters |

### 13. Yield Monitor Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `yield_monitor_enabled` | bool | False | Enable yield monitoring | Yield Monitor |
| `yield_threshold` | float | 95.0 | Yield threshold percentage | Yield Monitor |

### 14. HTTP API Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `api_enabled` | bool | False | Enable HTTP API server | HTTP API |
| `api_host` | str | "127.0.0.1" | API bind address | HTTP API |
| `api_port` | int | 8080 | API port | HTTP API |
| `api_base_path` | str | "/api/v1" | API base path | HTTP API |
| `api_cors_enabled` | bool | False | Enable CORS | HTTP API |
| `api_cors_origins` | str | "*" | Allowed origins | HTTP API |
| `api_auth_type` | str | "None" | "None", "API Key", "Bearer Token", "Basic Auth" | HTTP API |
| `api_rate_limit_enabled` | bool | False | Enable rate limiting | HTTP API |
| `api_rate_limit_requests` | int | 100 | Requests per window | HTTP API |
| `api_rate_limit_window` | int | 60 | Window in seconds | HTTP API |

### 15. Webhook Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `webhook_converter_url` | str | "" | Converter event webhook | Webhooks |
| `webhook_report_url` | str | "" | Report submission webhook | Webhooks |
| `webhook_service_url` | str | "" | Service event webhook | Webhooks |
| `webhook_auth_header` | str | "" | Auth header name | Webhooks |
| `webhook_auth_value` | str | "" | Auth header value | Webhooks |

### 16. GUI Tab Visibility

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `show_software_tab` | bool | True | Show software tab | GUI |
| `show_sn_handler_tab` | bool | True | Show serial number tab | GUI |
| `show_converters_tab` | bool | True | Show converters tab | GUI |
| `show_location_tab` | bool | True | Show location tab | GUI |
| `show_proxy_tab` | bool | True | Show proxy tab | GUI |

### 17. Connection State

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `auto_connect` | bool | True | Auto-connect on startup | Connection |
| `was_connected` | bool | False | Remember last connection state | *(internal)* |

### 18. Service Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `service_auto_start` | bool | True | Start service on system startup | Service |

### 19. Logging

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `log_level` | str | "INFO" | "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" | Logging |
| `log_file` | str | "client.log" | Log file name | Logging |

### 20. GUI Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `start_minimized` | bool | False | Start minimized | GUI |
| `minimize_to_tray` | bool | True | Minimize to system tray | GUI |

---

## Converter Configuration (ConverterConfig)

**Location:** `src/pywats_client/core/config.py`  
**Class:** `ConverterConfig`  
**Nested in:** `ClientConfig.converters`

### Converter Fields

| Field | Type | Default | Description | Required |
|-------|------|---------|-------------|----------|
| `name` | str | - | Human-readable name | ✅ |
| `module_path` | str | - | Python module path (e.g., "converters.CSVConverter") | ✅ |
| `watch_folder` | str | "" | Folder to watch for files/folders | For FILE/FOLDER |
| `done_folder` | str | "" | Folder for successfully converted files | No |
| `error_folder` | str | "" | Folder for failed files | No |
| `pending_folder` | str | "" | Folder for suspended files (retry) | No |
| `converter_type` | str | "file" | "file", "folder", "scheduled" | No |
| `enabled` | bool | True | Enable/disable converter | No |
| `priority` | int | **5** | Processing priority (1=highest, 10=lowest) ⭐ NEW | No |
| `arguments` | Dict | {} | Configuration arguments passed to converter | No |
| `file_patterns` | List[str] | ["*.*"] | File patterns to match | No |
| `folder_patterns` | List[str] | ["*"] | Folder patterns to match | No |
| `alarm_threshold` | float | 0.5 | Warn below this (but allow) | No |
| `reject_threshold` | float | 0.2 | Reject below this | No |
| `max_retries` | int | 3 | Maximum retry attempts | No |
| `retry_delay_seconds` | int | 60 | Retry delay | No |
| `schedule_interval_seconds` | int | None | For scheduled converters | For SCHEDULED |
| `cron_expression` | str | None | For scheduled converters | For SCHEDULED |
| `run_on_startup` | bool | False | Run immediately on load | No |
| `readiness_marker` | str | "COMPLETE.marker" | Marker file for folder readiness | For FOLDER |
| `min_file_count` | int | None | Min files before checking readiness | For FOLDER |
| `post_action` | str | "move" | "move", "delete", "archive", "keep" | No |
| `archive_folder` | str | "" | For "archive" post action | No |
| `description` | str | "" | Converter description | No |
| `author` | str | "" | Author name | No |
| `version` | str | "1.0.0" | Converter version | No |

**Priority Guidelines:**
- **1-2:** Real-time, critical converters (immediate processing)
- **3-5:** Normal priority (default=5)
- **6-8:** Batch processing (can wait)
- **9-10:** Low priority, background tasks

---

## API Settings (APISettings)

**Location:** `src/pywats/core/config.py`  
**Class:** `APISettings`  
**Usage:** Injected into pyWATS/AsyncWATS constructors

### API Connection Settings

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `timeout_seconds` | int | 30 | HTTP request timeout | API Settings |
| `max_retries` | int | 3 | Maximum retry attempts | API Settings |
| `retry_delay_seconds` | int | 1 | Delay between retries | API Settings |

### API Error Handling

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `error_mode` | ErrorMode | STRICT | "strict" or "lenient" | API Settings |

**Error Mode Behavior:**
- **STRICT:** Raises exceptions for 404/empty responses (production)
- **LENIENT:** Returns `None` for 404/empty responses (scripts/exploration)

### API Logging

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `log_requests` | bool | False | Log HTTP requests | API Settings |
| `log_responses` | bool | False | Log HTTP responses | API Settings |

### API SSL/TLS

| Field | Type | Default | Description | GUI Section |
|-------|------|---------|-------------|-------------|
| `verify_ssl` | bool | True | Verify SSL certificates | API Settings |

---

## Domain-Specific Settings

Each domain has its own settings class inheriting from `DomainSettings`.

### Base Domain Settings (All Domains)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | True | Whether domain is enabled |
| `cache_enabled` | bool | True | Whether caching is enabled |
| `cache_ttl_seconds` | int | 300 | Cache TTL (5 minutes) |

### Product Domain (`ProductDomainSettings`)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `auto_create_products` | bool | False | Auto-create products if not found |
| `default_revision` | str | "A" | Default revision for new products |

### Report Domain (`ReportDomainSettings`)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `auto_submit` | bool | True | Auto-submit reports after creation |
| `validate_before_submit` | bool | True | Validate reports before submission |
| `include_attachments` | bool | True | Include attachments in reports |
| `max_attachment_size_mb` | int | 10 | Max attachment size in MB |

### Production Domain (`ProductionDomainSettings`)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `auto_reserve_serials` | bool | True | Auto-reserve serial numbers |
| `serial_reserve_count` | int | 10 | Number of serials to reserve |
| `validate_serial_format` | bool | False | Validate serial number format |

### Process Domain (`ProcessDomainSettings`)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `refresh_interval_seconds` | int | 300 | Refresh interval (5 minutes) |
| `auto_refresh` | bool | True | Enable automatic refresh |

### Software Domain (`SoftwareDomainSettings`)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `auto_download` | bool | False | Auto-download software updates |
| `download_path` | str | "./downloads" | Download path |

### Asset, RootCause, App Domains

These use base `DomainSettings` only (no additional fields).

---

## Service & Component Settings

### Connection Config (`ConnectionConfig`)

**Location:** `src/pywats_client/core/connection_config.py`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `server_url` | str | "" | Server URL |
| `username` | str | "" | Username |
| `token_encrypted` | str | "" | Encrypted API token |
| `token_version` | int | 1 | Token format version |
| `connection_state` | str | "Not Connected" | Connection state |
| `last_connected` | str | None | ISO datetime |
| `last_disconnected` | str | None | ISO datetime |
| `health_check_interval` | int | 30 | Health check interval (seconds) |
| `health_check_timeout` | int | 10 | Health check timeout |
| `auto_reconnect` | bool | True | Auto-reconnect on disconnect |
| `max_reconnect_attempts` | int | 0 | 0 = unlimited |
| `reconnect_delay` | int | 10 | Delay between reconnect attempts |

### Service Config (`ServiceConfig`)

**Location:** `src/pywats_client/control/service.py`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `log_to_file` | bool | True | Log to file |
| `log_file` | str | "pywats_service.log" | Log file name |
| `log_level` | str | "INFO" | Log level |

---

## Configuration File Format

### config.json Structure

```json
{
  "schema_version": "2.0",
  "instance_id": "default",
  "instance_name": "WATS Client",
  "service_address": "https://wats.company.com",
  "api_token": "base64_encoded_token",
  "username": "station1",
  
  "station_name": "ICT-STATION-01",
  "location": "Production Floor - Building A",
  "purpose": "Production",
  "station_name_source": "config",
  "include_station_in_reports": true,
  
  "enable_cache": true,
  "cache_ttl_seconds": 300.0,
  "cache_max_size": 1000,
  
  "enable_metrics": true,
  "metrics_port": 9090,
  
  "sync_interval_seconds": 300,
  "offline_queue_enabled": true,
  "max_queue_size": 10000,
  
  "converters_enabled": true,
  "converters": [
    {
      "name": "CSV Converter",
      "module_path": "converters.csv_converter.CSVConverter",
      "watch_folder": "C:/watch/csv",
      "done_folder": "C:/watch/csv/done",
      "error_folder": "C:/watch/csv/error",
      "converter_type": "file",
      "enabled": true,
      "priority": 5,
      "file_patterns": ["*.csv"],
      "arguments": {
        "delimiter": ",",
        "encoding": "utf-8"
      }
    }
  ],
  
  "log_level": "INFO",
  "auto_connect": true,
  "service_auto_start": true
}
```

---

## GUI Settings Dialog Sections

### Recommended Tab/Section Organization

#### 1. **General** Tab
- Instance identification (instance_id, instance_name)
- Logging (log_level, log_file)

#### 2. **Connection** Tab ⭐ **PRIORITY**
- Server connection (service_address, api_token, username)
- Auto-connect settings
- Connection state display

#### 3. **Station** Tab
- Station identification (station_name, location, purpose)
- Station name source
- Multi-station mode (enable, presets list, active station)

#### 4. **Performance** Tab ⭐ **NEW**
- **HTTP Cache Settings:**
  - Enable cache (checkbox)
  - Cache TTL (slider: 60-7200 seconds, with presets)
  - Cache max size (slider: 100-5000 entries)
  - Cache statistics display (hits, misses, hit rate, current size)
  - Clear cache button
- **Queue Settings:**
  - Max queue size
  - Max concurrent uploads

#### 5. **Observability** Tab ⭐ **NEW**
- **Metrics:**
  - Enable metrics (checkbox)
  - Metrics port (default: 9090)
  - Metrics endpoint preview: `http://localhost:9090/metrics`
- **Health Endpoints:**
  - Health check interval
  - Display health endpoint URLs

#### 6. **Sync** Tab
- Sync interval
- Process sync enabled

#### 7. **Offline** Tab
- Offline queue enabled
- Reports folder
- Max retry attempts
- Retry interval

#### 8. **Converters** Tab
- Converters enabled (global toggle)
- Converters folder
- Converters list with add/edit/delete
- **Per-converter settings:**
  - Name, module path, description
  - Watch folders (watch, done, error, pending)
  - Converter type (FILE/FOLDER/SCHEDULED)
  - Enabled checkbox
  - **Priority slider (1-10)** ⭐ NEW
  - File/folder patterns
  - Validation thresholds
  - Retry settings
  - Schedule settings (for SCHEDULED type)
  - Post-processing

#### 9. **Serial Number** Tab
- Serial number mode
- Prefix, start, padding
- COM port, terminator (for barcode scanner)
- Validation settings

#### 10. **Proxy** Tab
- Proxy mode (none/system/manual)
- Proxy host, port
- Proxy authentication
- Bypass list

#### 11. **HTTP API** Tab
- API enabled
- API host, port, base path
- CORS settings
- Authentication type
- Rate limiting

#### 12. **Webhooks** Tab
- Converter webhook URL
- Report webhook URL
- Service webhook URL
- Authentication header

#### 13. **API Settings** Tab
- Timeout, retries, retry delay
- Error mode (STRICT/LENIENT)
- Log requests/responses
- Verify SSL

#### 14. **Domain Settings** Tab
- Expandable sections for each domain:
  - Product
  - Report
  - Production
  - Process
  - Software
  - Asset
  - RootCause
  - App

#### 15. **Advanced** Tab
- GUI tab visibility toggles
- Service auto-start
- GUI settings (start minimized, minimize to tray)

---

## New in v0.3.0 - Performance & Observability

### HTTP Cache Settings ⭐

**ClientConfig Fields:**
- `enable_cache: bool = True`
- `cache_ttl_seconds: float = 300.0`
- `cache_max_size: int = 1000`

**GUI Implementation:**
```python
# Performance Tab - HTTP Cache Section
cache_group = QGroupBox("HTTP Response Caching")

# Enable checkbox
enable_cache_cb = QCheckBox("Enable HTTP response caching")
enable_cache_cb.setChecked(config.enable_cache)

# TTL slider with presets
ttl_layout = QHBoxLayout()
ttl_label = QLabel("Cache TTL (seconds):")
ttl_slider = QSlider(Qt.Horizontal)
ttl_slider.setRange(60, 7200)
ttl_slider.setValue(config.cache_ttl_seconds)
ttl_value_label = QLabel(f"{config.cache_ttl_seconds}s")

# Preset buttons
preset_layout = QHBoxLayout()
preset_buttons = [
    ("1 min (Reports)", 60),
    ("5 min (Default)", 300),
    ("10 min (Products)", 600),
    ("1 hour (Config)", 3600)
]

# Size slider
size_layout = QHBoxLayout()
size_label = QLabel("Max cache size:")
size_slider = QSlider(Qt.Horizontal)
size_slider.setRange(100, 5000)
size_slider.setValue(config.cache_max_size)
size_value_label = QLabel(f"{config.cache_max_size} entries")

# Statistics display (read-only)
stats_group = QGroupBox("Cache Statistics")
# Display: hits, misses, hit rate, current size
```

### Metrics Settings ⭐

**ClientConfig Fields:**
- `enable_metrics: bool = True`
- `metrics_port: int = 9090`

**GUI Implementation:**
```python
# Observability Tab - Metrics Section
metrics_group = QGroupBox("Prometheus Metrics")

# Enable checkbox
enable_metrics_cb = QCheckBox("Enable Prometheus metrics collection")
enable_metrics_cb.setChecked(config.enable_metrics)

# Port spinner
port_layout = QHBoxLayout()
port_label = QLabel("Metrics port:")
port_spinner = QSpinBox()
port_spinner.setRange(1024, 65535)
port_spinner.setValue(config.metrics_port)

# Endpoint preview (read-only)
endpoint_label = QLabel(f"Metrics URL: http://localhost:{config.metrics_port}/metrics")
endpoint_label.setStyleSheet("color: gray;")

# Open in browser button
open_button = QPushButton("Open in Browser")
```

### Converter Priority ⭐

**ConverterConfig Field:**
- `priority: int = 5` (range: 1-10)

**GUI Implementation:**
```python
# Converter Dialog - Priority Section
priority_group = QGroupBox("Processing Priority")

# Priority slider
priority_slider = QSlider(Qt.Horizontal)
priority_slider.setRange(1, 10)
priority_slider.setValue(converter.priority)
priority_slider.setTickPosition(QSlider.TicksBelow)
priority_slider.setTickInterval(1)

# Priority labels
priority_layout = QHBoxLayout()
priority_layout.addWidget(QLabel("High (1)"))
priority_layout.addStretch()
priority_layout.addWidget(QLabel("Normal (5)"))
priority_layout.addStretch()
priority_layout.addWidget(QLabel("Low (10)"))

# Priority description
priority_desc = QLabel(
    "Priority 1-2: Real-time, critical\n"
    "Priority 3-5: Normal (default=5)\n"
    "Priority 6-8: Batch processing\n"
    "Priority 9-10: Low priority, background"
)
priority_desc.setStyleSheet("color: gray; font-size: 9pt;")
```

---

## Configuration Validation

### Required Fields

**ClientConfig:**
- `schema_version` (auto-set)
- `instance_id` (auto-set to "default")
- `instance_name` (auto-set to "WATS Client")

**For Connection:**
- `service_address` (user must provide)
- `api_token` (user must provide)

**ConverterConfig:**
- `name` (user must provide)
- `module_path` (user must provide)
- `watch_folder` (for FILE/FOLDER types)
- `schedule_interval_seconds` OR `cron_expression` (for SCHEDULED type)

### Validation Rules

```python
# ConverterConfig validation
errors = converter_config.validate()  # Returns List[str]

# Example validation:
# - name not empty
# - module_path not empty
# - watch_folder not empty (for FILE/FOLDER)
# - 0.0 <= alarm_threshold <= 1.0
# - 0.0 <= reject_threshold <= 1.0
# - reject_threshold <= alarm_threshold
# - schedule configured (for SCHEDULED)
```

---

## Best Practices for GUI Implementation

### 1. **Connection Tab Priority**
Show connection settings first - they're required for basic operation.

### 2. **Cache Settings with Presets**
Provide preset buttons for common TTL values:
- 1 minute (reports)
- 5 minutes (default)
- 10 minutes (products)
- 1 hour (configuration)

### 3. **Cache Statistics Real-Time Display**
Show live cache statistics when connected:
```
Cache: 450/1000 entries | Hit rate: 85.2% | 1,245 hits, 217 misses
```

### 4. **Metrics Endpoint Testing**
Add "Test Connection" button for metrics endpoint to verify it's accessible.

### 5. **Priority Visual Feedback**
Color-code priority slider:
- 1-2: Red (high priority)
- 3-5: Green (normal)
- 6-10: Gray (low priority)

### 6. **Converter List with Priority Badge**
Show priority badge in converter list:
```
[P1] Critical Converter (Enabled)
[P5] CSV Converter (Enabled)
[P8] Batch Uploader (Disabled)
```

### 7. **Save Confirmation**
Show confirmation when saving settings:
```
Settings saved successfully.
Cache settings will apply immediately.
Service restart required for: [metrics_port]
```

### 8. **Settings Dependencies**
Disable dependent fields when parent is disabled:
- Disable cache TTL/size when `enable_cache=False`
- Disable metrics port when `enable_metrics=False`

---

## Configuration Migration

### Schema Versioning

Current schema: **2.0**

Migration path:
```python
if config.get("schema_version") is None:
    # Migrate from 1.0 to 2.0
    config = migrate_v1_to_v2(config)

# Always set current version
config["schema_version"] = "2.0"
```

### New Field Defaults

When adding new fields, provide sensible defaults:
```python
config.setdefault("enable_cache", True)
config.setdefault("cache_ttl_seconds", 300.0)
config.setdefault("cache_max_size", 1000)
config.setdefault("enable_metrics", True)
config.setdefault("metrics_port", 9090)
```

---

**End of Configuration Reference**

For implementation examples, see:
- `src/pywats_client/gui/settings_dialog.py` - Existing settings dialog
- `docs/guides/performance.md` - Cache configuration guide
- `docs/guides/observability.md` - Metrics configuration guide
- `examples/client/configuration.py` - Configuration examples
