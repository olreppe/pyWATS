# pyWATS Security Guide

This comprehensive guide documents all security features and best practices for pyWATS Client, covering IPC communication, converter sandboxing, file handling, configuration security, and production deployment.

## Table of Contents

1. [Security Overview](#security-overview)
2. [IPC Communication Security](#ipc-communication-security)
3. [Converter Security](#converter-security)
4. [File Handling Security](#file-handling-security)
5. [Configuration Security](#configuration-security)
6. [Best Practices](#best-practices)

---

## Security Overview

### Security Principles

pyWATS uses a **defense-in-depth** security approach with multiple layers:

1. **Authentication** - Shared secret authentication for IPC communication
2. **Rate Limiting** - Token bucket algorithm to prevent abuse
3. **Process Isolation** - Sandboxed converter execution
4. **Static Analysis** - Validates converter code before execution
5. **Atomic Operations** - Prevents data corruption during file operations
6. **Resource Limits** - Prevents resource exhaustion attacks

### Threat Model

pyWATS uses a **pragmatic security approach**:

- **Target Environment:** Secure stations behind machine authentication
- **Threat Model:** Prevent accidents and basic abuse, not sophisticated attacks
- **Philosophy:** "Friendly" environment - trusted users on controlled machines

### What pyWATS Security Protects Against

✅ **Protected:**
- Accidental connections from other programs
- Basic unauthorized access
- Request flooding (accidental or intentional)
- Accidental resource exhaustion
- Simple malicious code injection
- Unauthorized file system access
- Dangerous module imports
- Data loss and corruption during file operations
- Race conditions from concurrent access

❌ **NOT Protected:**
- Local privilege escalation
- Root/Admin access to machine
- Memory inspection attacks
- Hardware attacks
- Sophisticated attacks (side channels, timing attacks)
- Kernel-level exploits
- Physical access

### Security Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    pyWATS Client Architecture                    │
│                                                                  │
│  ┌──────────────┐          ┌──────────────────┐                │
│  │   GUI App    │◄────────►│  AsyncIPCServer  │                │
│  │              │  Socket  │  - Auth Handler  │                │
│  │ AsyncIPCClient│          │  - Rate Limiter  │                │
│  └──────────────┘          └──────────────────┘                │
│         │                           │                            │
│         │     Shared Secret         │                            │
│         └───────────────────────────┘                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              AsyncConverterPool                              ││
│  │                                                              ││
│  │  ┌─────────────────┐    ┌─────────────────────────────────┐││
│  │  │ Trusted Mode    │    │ Sandboxed Mode                  │││
│  │  │ (Direct exec)   │    │ ┌─────────────────────────────┐ │││
│  │  │                 │    │ │ ConverterSandbox            │ │││
│  │  │                 │    │ │  - ConverterValidator       │ │││
│  │  │                 │    │ │  - SandboxProcess           │ │││
│  │  │                 │    │ │  - SandboxConfig            │ │││
│  │  │                 │    │ └─────────────────────────────┘ │││
│  │  └─────────────────┘    │ ┌─────────────────────────────┐ │││
│  │                         │ │ sandbox_runner.py           │ │││
│  │                         │ │  (Isolated Subprocess)      │ │││
│  │                         │ │  - SafeFileHandler          │ │││
│  │                         │ │  - RestrictedImporter       │ │││
│  │                         │ └─────────────────────────────┘ │││
│  │                         └─────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Safe File Operations                            ││
│  │  - Atomic Writes        - File Locking                      ││
│  │  - Backup Recovery      - Config Validation                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## IPC Communication Security

Inter-Process Communication (IPC) in pyWATS Client connects the GUI to the background service using Unix domain sockets (or named pipes on Windows). This section covers authentication and rate limiting features.

### IPC Architecture

```
┌──────────────┐          ┌──────────────────┐
│   GUI App    │◄────────►│  AsyncIPCServer  │
│              │  Socket  │                  │
│ AsyncIPCClient│          │  - Auth Handler  │
│              │          │  - Rate Limiter  │
└──────────────┘          └──────────────────┘
        │                         │
        │     Shared Secret       │
        └─────────────────────────┘
              (file-based)
```

### Shared Secret Authentication

The IPC server uses a shared secret for authentication:

1. **Secret Generation:** Service generates 256-bit random token on startup
2. **Secret Storage:** Stored in user-specific secure location
3. **Client Authentication:** Client reads secret and sends with connection
4. **Validation:** Server validates using timing-safe comparison

#### Secret Storage Locations

| Platform | Location |
|----------|----------|
| Linux/macOS | `~/.config/pywats/secrets/<instance_id>.key` |
| Windows | `%LOCALAPPDATA%\pyWATS\secrets\<instance_id>.key` |

Files are created with restricted permissions:
- Unix: `0600` (owner read/write only)
- Windows: Current user only

#### Authentication Flow

```
Client                              Server
   │                                   │
   │──────── Connect ─────────────────►│
   │                                   │
   │◄─────── Welcome ──────────────────│
   │                                   │
   │──────── auth <token> ────────────►│
   │                                   │
   │◄─────── OK | DENIED ──────────────│
   │                                   │
   │──────── (authenticated) ─────────►│
```

#### Implementation

**Server-side (AsyncIPCServer):**

```python
async def _handle_auth(self, client_id: str, parts: List[str]):
    """Handle authentication request."""
    if len(parts) < 2:
        return "ERROR missing_token"
    
    token = parts[1]
    
    # Timing-safe comparison
    if secrets.compare_digest(token, self._auth_token):
        self._authenticated_clients.add(client_id)
        return "OK authenticated"
    else:
        return "DENIED invalid_token"
```

**Client-side (AsyncIPCClient):**

```python
async def _authenticate(self):
    """Authenticate with the server."""
    token = load_secret(self._instance_id)
    if not token:
        raise IPCAuthError("No secret available")
    
    response = await self._send_command(f"auth {token}")
    if not response.startswith("OK"):
        raise IPCAuthError(f"Authentication failed: {response}")
```

### Rate Limiting

#### Token Bucket Algorithm

The server implements rate limiting using a token bucket:

- **Bucket Size (Burst):** 20 requests
- **Refill Rate:** 100 requests per minute
- **Per-Client:** Each connection has its own bucket

#### Behavior

1. Each request consumes one token
2. Tokens refill over time
3. When bucket is empty, requests are rejected
4. `ping` command is always allowed (for health checks)

#### Configuration

```python
from pywats_client.core.security import RateLimiter

# Create rate limiter with custom settings
limiter = RateLimiter(
    max_tokens=20,          # Burst size
    refill_rate=100,        # Tokens per minute
    cleanup_interval=300,   # Clean old buckets every 5 min
)
```

#### Rate Limit Response

When rate limit is exceeded:

```
Client: some_command
Server: RATE_LIMIT rate_limit_exceeded
```

### IPC Security API

#### Core Security Module

Location: `src/pywats_client/core/security.py`

##### Secret Management

```python
from pywats_client.core.security import (
    generate_secret,
    save_secret,
    load_secret,
    delete_secret,
)

# Generate new secret
secret = generate_secret()  # 64-character hex string

# Save to secure location
save_secret("instance-1", secret)

# Load secret
loaded = load_secret("instance-1")

# Delete secret
delete_secret("instance-1")
```

##### Token Validation

```python
from pywats_client.core.security import validate_token

# Timing-safe comparison
is_valid = validate_token(provided_token, expected_token)
```

##### Rate Limiting

```python
from pywats_client.core.security import RateLimiter

limiter = RateLimiter()

# Check if request allowed
if limiter.check("client-1"):
    # Process request
    pass
else:
    # Rate limited
    pass

# Reset a client's bucket
limiter.reset("client-1")
```

### IPC Commands

#### Authentication Commands

| Command | Description | Auth Required |
|---------|-------------|---------------|
| `ping` | Health check | No |
| `auth <token>` | Authenticate | No |
| `status` | Get service status | Yes |
| `start` | Start service | Yes |
| `stop` | Stop service | Yes |

#### Example Session

```
# Connect to server
> ping
< PONG

# Authenticate
> auth abc123...
< OK authenticated

# Now can use protected commands
> status
< RUNNING processing_files=5

# Unauthenticated commands rejected
> status  # (without auth)
< ERROR authentication_required
```

### IPC Troubleshooting

#### Authentication Failures

**Symptom:** `DENIED invalid_token`

**Solutions:**
1. Check secret file exists in correct location
2. Verify file permissions allow reading
3. Ensure service and client use same instance ID
4. Restart service to regenerate secret

#### Rate Limiting Issues

**Symptom:** `RATE_LIMIT rate_limit_exceeded`

**Solutions:**
1. Reduce request frequency
2. Use batch commands where possible
3. Check for runaway loops in client code
4. Increase rate limits if legitimate use case

#### Permission Errors

**Symptom:** Cannot read/write secret file

**Solutions:**
1. Check directory permissions
2. Run as correct user
3. Ensure parent directories exist

---

## Converter Security

Converters in pyWATS process external data files (test results, logs, etc.) and transform them into WATS reports. Since converters may come from various sources (built-in, user-created, third-party), the client provides a sandboxing system to execute converters securely.

### Converter Security Model

pyWATS uses a **defense-in-depth** approach for converters:

1. **Static Analysis** - Validates converter code before execution
2. **Process Isolation** - Runs converters in separate subprocess
3. **Capability-Based Permissions** - Fine-grained permission control
4. **Resource Limits** - Prevents resource exhaustion

### Sandbox Architecture

#### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    AsyncConverterPool                        │
│                                                              │
│  ┌─────────────────┐    ┌─────────────────────────────────┐│
│  │ Trusted Mode    │    │ Sandboxed Mode                  ││
│  │ (Direct exec)   │    │ ┌─────────────────────────────┐ ││
│  │                 │    │ │ ConverterSandbox            │ ││
│  │                 │    │ │  - ConverterValidator       │ ││
│  │                 │    │ │  - SandboxProcess           │ ││
│  │                 │    │ │  - SandboxConfig            │ ││
│  │                 │    │ └─────────────────────────────┘ ││
│  └─────────────────┘    │ ┌─────────────────────────────┐ ││
│                         │ │ sandbox_runner.py           │ ││
│                         │ │  (Isolated Subprocess)      │ ││
│                         │ │  - SafeFileHandler          │ ││
│                         │ │  - RestrictedImporter       │ ││
│                         │ └─────────────────────────────┘ ││
│                         └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

#### Execution Flow

1. **Converter Registration** - Pool validates converter source
2. **File Detection** - Watchdog triggers file event
3. **Sandbox Decision** - Check if sandbox should be used
4. **Process Creation** - Spawn isolated subprocess
5. **Converter Loading** - Load converter in restricted environment
6. **Execution** - Run conversion with resource limits
7. **Result Collection** - Retrieve result via IPC
8. **Cleanup** - Terminate subprocess

### Using the Sandbox

#### Default Behavior

By default, the `AsyncConverterPool` runs converters in the sandbox:

```python
from pywats_client.service import AsyncConverterPool

# Sandbox is enabled by default
pool = AsyncConverterPool(
    config=config,
    api=api,
    enable_sandbox=True,  # Default
)
```

#### Disabling the Sandbox

For trusted converters or development, you can disable the sandbox:

```python
# Disable sandbox for all converters
pool = AsyncConverterPool(
    config=config,
    api=api,
    enable_sandbox=False,
)
```

#### Per-Converter Trust Mode

Individual converters can be marked as trusted:

```python
from pywats_client.converters import FileConverter

class MyTrustedConverter(FileConverter):
    @property
    def trusted_mode(self) -> bool:
        # Skip sandbox for this converter
        return True
```

### Sandbox Configuration

#### SandboxConfig

The `SandboxConfig` class controls sandbox behavior:

```python
from pywats_client.converters import (
    SandboxConfig,
    SandboxCapability,
    ResourceLimits,
)

config = SandboxConfig(
    # Capabilities granted to converters
    capabilities=frozenset([
        SandboxCapability.READ_INPUT,
        SandboxCapability.WRITE_OUTPUT,
        SandboxCapability.LOG_INFO,
    ]),
    
    # Resource limits
    resource_limits=ResourceLimits(
        timeout_seconds=300,      # 5 minutes max
        memory_mb=512,            # 512 MB memory
        cpu_time_seconds=120,     # 2 minutes CPU
    ),
    
    # Blocked imports (dangerous modules)
    blocked_imports=frozenset([
        "subprocess", "os.system", "socket",
        "ctypes", "multiprocessing",
    ]),
)
```

#### Capabilities

The `SandboxCapability` enum defines what converters can do:

| Capability | Description |
|------------|-------------|
| `READ_INPUT` | Read input file(s) |
| `WRITE_OUTPUT` | Write output file(s) |
| `NETWORK_WATS` | Connect to WATS API |
| `NETWORK_LOCAL` | Connect to localhost |
| `NETWORK_FULL` | Full network access |
| `LOG_DEBUG` | Write debug logs |
| `LOG_INFO` | Write info logs |
| `LOG_WARNING` | Write warning logs |
| `LOG_ERROR` | Write error logs |
| `FILE_TEMP` | Create temp files |
| `SHELL_EXECUTE` | Execute shell commands (use with caution!) |

Default capabilities are minimal:
- `READ_INPUT`
- `WRITE_OUTPUT`
- `LOG_INFO`
- `LOG_WARNING`
- `LOG_ERROR`

#### Resource Limits

```python
from pywats_client.converters import ResourceLimits

limits = ResourceLimits(
    # Time limits
    timeout_seconds=300.0,     # Wall-clock timeout (default: 5 min)
    cpu_time_seconds=120.0,    # CPU time limit (default: 2 min)
    
    # Memory limits
    memory_mb=512,             # Max memory (default: 512 MB)
    
    # File limits
    max_output_size_mb=100,    # Max output file size (default: 100 MB)
    max_open_files=50,         # Max open file descriptors
    
    # Process limits
    max_processes=1,           # Prevent fork bombs
)
```

### Static Analysis (Validation)

Before executing a converter, the `ConverterValidator` performs static analysis:

#### Blocked Patterns

The validator detects dangerous code patterns:

- **Dangerous Imports:** `subprocess`, `socket`, `ctypes`, `multiprocessing`, etc.
- **Dangerous Calls:** `eval()`, `exec()`, `compile()`, `__import__()`, `os.system()`
- **Syntax Errors:** Invalid Python code

#### Using the Validator

```python
from pywats_client.converters import ConverterValidator, SandboxConfig

config = SandboxConfig()
validator = ConverterValidator(config)

# Validate source code
source = open("my_converter.py").read()
is_valid, issues = validator.validate_source(source)

if not is_valid:
    print("Validation failed:")
    for issue in issues:
        print(f"  - {issue}")
```

#### Example: Blocked Converter

```python
# This converter will be REJECTED by the validator
import subprocess  # BLOCKED!

class BadConverter:
    def convert_file(self, file_path, args):
        # This will never run - blocked at validation
        subprocess.run(["rm", "-rf", "/"])
```

### Writing Sandbox-Safe Converters

#### Best Practices

1. **Use Standard Library Only** - Avoid external dependencies when possible
2. **No Network Access** - Don't make HTTP requests unless necessary
3. **No Shell Commands** - Never use `os.system()` or `subprocess`
4. **File I/O via Parameters** - Only read/write the provided paths
5. **Handle Errors Gracefully** - Return error results, don't crash

#### Example: Safe Converter

```python
"""Example of a sandbox-safe converter."""

from pathlib import Path
import json


class SafeCSVConverter:
    """Converts CSV files to WATS reports."""
    
    @property
    def name(self) -> str:
        return "SafeCSVConverter"
    
    @property
    def file_patterns(self) -> list:
        return ["*.csv"]
    
    def convert_file(self, file_path: Path, args: dict):
        """
        Convert a CSV file to a report.
        
        Args:
            file_path: Path to input file (sandbox provides access)
            args: Converter arguments from config
        
        Returns:
            dict with status, report, and metadata
        """
        try:
            # Read input (allowed via READ_INPUT capability)
            content = file_path.read_text()
            lines = content.strip().split('\n')
            
            # Parse CSV (simple example)
            header = lines[0].split(',')
            data = [line.split(',') for line in lines[1:]]
            
            # Build report
            report = {
                "type": "UUT",
                "partNumber": args.get("part_number", "UNKNOWN"),
                "serialNumber": data[0][0] if data else "UNKNOWN",
                "result": "Passed",
            }
            
            return {
                "status": "Success",
                "report": report,
                "metadata": {
                    "rows_processed": len(data),
                }
            }
            
        except Exception as e:
            return {
                "status": "Failed",
                "error": str(e),
            }
```

### Converter Error Handling

#### Sandbox Exceptions

```python
from pywats_client.converters import (
    SandboxError,
    SandboxTimeoutError,
    SandboxSecurityError,
)

try:
    result = await sandbox.run_converter(...)
except SandboxTimeoutError:
    print("Converter exceeded time limit")
except SandboxSecurityError:
    print("Converter failed security validation")
except SandboxError:
    print("General sandbox error")
```

#### Handling Converter Failures

Converter failures are captured and returned:

```python
result = await sandbox.run_converter(...)

if result.get("status") == "Failed":
    error = result.get("error", "Unknown error")
    print(f"Conversion failed: {error}")
```

### Performance Considerations

#### Subprocess Overhead

The sandbox spawns a new Python process for each conversion, which has overhead:

- **Process creation:** ~100-200ms on Windows, ~50-100ms on Unix
- **IPC communication:** ~1-10ms per message

For high-throughput scenarios, consider:
- Using `trusted_mode` for verified converters
- Batch processing multiple files per subprocess (future feature)

#### Memory Usage

Each sandboxed converter runs in a separate process with its own memory space. Default limit is 512 MB per converter.

### Converter Troubleshooting

#### Converter Rejected by Validator

**Symptom:** `SandboxSecurityError: Converter validation failed`

**Solutions:**
1. Check for blocked imports
2. Remove dangerous function calls
3. If the module is safe, add to `allowed_imports`

#### Timeout Errors

**Symptom:** `SandboxTimeoutError: Converter timed out`

**Solutions:**
1. Increase `timeout_seconds` in `ResourceLimits`
2. Optimize converter code
3. Use `trusted_mode` for known-slow converters

#### Memory Limit Exceeded

**Symptom:** Process killed by OS

**Solutions:**
1. Increase `memory_mb` in `ResourceLimits`
2. Process files in smaller chunks
3. Use streaming instead of loading entire files

### Full Sandbox Configuration Example

```python
from pywats_client.converters import (
    SandboxCapability,
    ResourceLimits,
    SandboxConfig,
    ConverterSandbox,
)

# Create custom configuration
config = SandboxConfig(
    capabilities=frozenset([
        SandboxCapability.READ_INPUT,
        SandboxCapability.WRITE_OUTPUT,
        SandboxCapability.LOG_INFO,
        SandboxCapability.NETWORK_WATS,  # Allow WATS API calls
    ]),
    resource_limits=ResourceLimits(
        timeout_seconds=600,  # 10 minutes for slow converters
        memory_mb=1024,       # 1 GB for large files
    ),
    blocked_imports=frozenset([
        "subprocess", "os.system", "socket",
        "ctypes", "multiprocessing",
        "requests",  # Block HTTP library too
    ]),
)

# Create sandbox with custom config
sandbox = ConverterSandbox(default_config=config)

# Run converter
result = await sandbox.run_converter(
    converter_path=Path("my_converter.py"),
    converter_class="MyConverter",
    input_path=Path("input.csv"),
    args={"part_number": "PN-001"},
)
```

---

## File Handling Security

The pyWATS Client uses robust file handling utilities to prevent data loss, corruption, and race conditions during file operations.

### Core Security Guarantees

- **Atomic writes**: Files are written completely or not at all
- **Backup recovery**: Automatic fallback to backup files if main file is corrupted
- **File locking**: Cross-platform file locking to prevent concurrent access issues
- **Validation and repair**: Configuration files are validated and can be automatically repaired

### SafeFileWriter

Provides atomic write operations that prevent partial writes and data corruption.

```python
from pywats_client.core.file_utils import SafeFileWriter

# Write JSON atomically with backup
SafeFileWriter.write_json_atomic(
    path="/path/to/config.json",
    data={"key": "value"},
    create_backup=True  # Creates .bak file before overwriting
)

# Write text atomically
SafeFileWriter.write_text_atomic(
    path="/path/to/file.txt",
    content="File contents",
    encoding="utf-8"
)

# Write binary data atomically
SafeFileWriter.write_bytes_atomic(
    path="/path/to/file.bin",
    data=b"\x00\x01\x02"
)
```

#### How Atomic Writes Work

1. Data is written to a temporary file (`.tmp` extension)
2. The temporary file is flushed and synced to disk
3. If a backup is requested and the original exists, it's copied to `.bak`
4. The temporary file is atomically renamed to the target path
5. If any step fails, the original file remains untouched

This prevents:
- Partial writes from crashes or power failures
- Corrupted files from interrupted writes
- Data loss from write failures

### SafeFileReader

Provides safe read operations with automatic backup recovery.

```python
from pywats_client.core.file_utils import SafeFileReader

# Read JSON with automatic backup recovery
data = SafeFileReader.read_json_safe("/path/to/config.json")
# If config.json is corrupted but config.json.bak exists and is valid,
# the backup is automatically restored and returned

# Read text with fallback
content = SafeFileReader.read_text_safe("/path/to/file.txt")
```

#### Recovery Behavior

1. Attempts to read the main file
2. If the main file is corrupted (JSON parse error, etc.), checks for `.bak` file
3. If backup is valid, restores it to the main file and returns its contents
4. If both are corrupted, returns `None`

### File Locking

Cross-platform file locking prevents race conditions when multiple processes access the same file.

```python
from pywats_client.core.file_utils import locked_file

# Use as context manager
with locked_file("/path/to/file.json", mode="w", timeout=5.0) as f:
    json.dump(data, f)

# Read with lock
with locked_file("/path/to/file.json", mode="r", timeout=10.0) as f:
    data = json.load(f)
```

#### Platform Support

- **Unix/Linux/macOS**: Uses `fcntl.flock()` for file locking
- **Windows**: Uses `msvcrt.locking()` for file locking

#### Lock Types

- Write mode (`w`, `a`): Exclusive lock (blocks other readers and writers)
- Read mode (`r`): Shared lock (allows other readers, blocks writers)

#### Lock Timeouts

```python
from pywats_client.core.file_utils import locked_file

try:
    with locked_file(path, mode='w', timeout=5.0) as f:
        # ... write operations
        pass
except TimeoutError:
    logger.error("Could not acquire file lock within timeout")
```

### Path Validation and Race Condition Prevention

When working with file paths, several security considerations apply:

#### Path Traversal Prevention

Always validate paths to prevent directory traversal attacks:

```python
from pathlib import Path

def safe_path_join(base_dir: Path, user_path: str) -> Path:
    """Safely join user-provided path to base directory."""
    # Resolve to absolute path
    full_path = (base_dir / user_path).resolve()
    
    # Ensure result is within base_dir
    if not str(full_path).startswith(str(base_dir.resolve())):
        raise ValueError("Path traversal detected")
    
    return full_path
```

#### TOCTOU (Time-of-Check Time-of-Use) Prevention

File locking prevents race conditions between checking and using files:

```python
# Bad: Race condition between check and use
if os.path.exists(path):
    with open(path) as f:  # File might be deleted here!
        data = f.read()

# Good: Atomic check-and-use with locking
try:
    with locked_file(path, mode='r', timeout=5.0) as f:
        data = f.read()
except FileNotFoundError:
    # Handle missing file
    pass
```

---

## Configuration Security

Configuration files in pyWATS Client contain sensitive information and must be handled securely.

### Configuration Validation

#### Validating Configuration

```python
from pywats_client.core.config import ClientConfig

# Load config
config = ClientConfig.load("/path/to/config.json")

# Validate
errors = config.validate()
if errors:
    print("Configuration errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Configuration is valid")

# Quick check
if config.is_valid():
    print("Config OK")
```

#### Validated Fields

- `instance_id`: Required, non-empty
- `sync_interval_seconds`: Must be non-negative
- `max_retry_attempts`: Must be non-negative
- `retry_interval_seconds`: Must be non-negative
- `proxy_port`: Must be 0-65535
- `yield_threshold`: Must be 0.0-100.0
- `log_level`: Must be DEBUG, INFO, WARNING, ERROR, or CRITICAL
- `station_name_source`: Must be hostname, config, or manual
- `proxy_mode`: Must be none, system, or manual
- `converters`: Each converter is validated individually

### Automatic Repair

```python
# Repair individual config
config = ClientConfig()
config.sync_interval_seconds = -100  # Invalid!

repairs = config.repair()
# repairs = ["Reset negative sync_interval_seconds to 300"]
# config.sync_interval_seconds is now 300

# Load and repair in one step
config, repairs = ClientConfig.load_and_repair("/path/to/config.json")
if repairs:
    print(f"Made {len(repairs)} repairs:")
    for repair in repairs:
        print(f"  - {repair}")
```

#### Automatic Repair Rules

| Field | Invalid Value | Repaired To |
|-------|--------------|-------------|
| `instance_id` | Empty | "default" |
| `sync_interval_seconds` | Negative | 300 |
| `max_retry_attempts` | Negative | 5 |
| `retry_interval_seconds` | Negative | 60 |
| `proxy_port` | < 0 or > 65535 | 8080 |
| `yield_threshold` | < 0 | 0.0 |
| `yield_threshold` | > 100 | 100.0 |
| `log_level` | Invalid | "INFO" |
| `station_name_source` | Invalid | "hostname" |
| `proxy_mode` | Invalid | "system" |

### Credential Encryption

Sensitive credentials (API tokens, passwords) should be stored encrypted:

```python
from pywats_client.core.security import (
    encrypt_credential,
    decrypt_credential,
)

# Encrypt sensitive data before saving
encrypted = encrypt_credential("my-api-token", "instance-1")
config.api_token_encrypted = encrypted
config.save()

# Decrypt when needed
api_token = decrypt_credential(config.api_token_encrypted, "instance-1")
```

**Note:** Encryption keys are stored in the same secure location as IPC secrets.

### Configuration File Permissions

Configuration files should have restricted permissions:

#### Unix/Linux/macOS

```bash
# Set restrictive permissions
chmod 600 ~/.config/pywats/config.json
chmod 700 ~/.config/pywats/
```

#### Windows

```powershell
# Remove access for all users except current user
icacls "%LOCALAPPDATA%\pyWATS\config.json" /inheritance:r /grant:r "%USERNAME%:F"
```

### Converter Configuration Validation

Converter configurations have their own validation:

```python
from pywats_client.core.config import ConverterConfig

converter = ConverterConfig(
    name="My Converter",
    module_path="my_module.MyConverter",
    converter_type="file",
    watch_folder="/path/to/watch"
)

errors = converter.validate()
# Validates:
# - name is required
# - module_path is required
# - converter_type is valid
# - watch_folder required for file/folder converters
# - schedule required for scheduled converters
# - threshold values in valid ranges
```

---

## Best Practices

This section provides a comprehensive security checklist for production deployments.

### Production Deployment Checklist

#### 1. IPC Security

- ✅ Verify secret files have restrictive permissions (0600 on Unix)
- ✅ Use unique instance IDs for each service instance
- ✅ Monitor logs for authentication failures
- ✅ Set appropriate rate limits based on expected usage
- ✅ Ensure service and client versions match
- ✅ Use separate user accounts for multi-user systems

#### 2. Converter Security

- ✅ Enable sandbox for all third-party converters
- ✅ Review converter source code before deployment
- ✅ Use minimal capabilities (READ_INPUT, WRITE_OUTPUT, LOG_*)
- ✅ Set appropriate resource limits for your environment
- ✅ Test converters in sandbox before production
- ✅ Only use `trusted_mode` for thoroughly reviewed converters
- ✅ Monitor converter execution times and memory usage
- ✅ Keep sandbox configuration in version control

#### 3. File Handling Security

- ✅ Always use atomic writes for critical data
- ✅ Enable backups for important files (`create_backup=True`)
- ✅ Use file locking for shared files
- ✅ Validate configuration after loading
- ✅ Implement proper error handling for file operations
- ✅ Use `load_and_repair()` for robustness
- ✅ Set restrictive file permissions on config files
- ✅ Validate user-provided paths to prevent traversal

#### 4. Configuration Security

- ✅ Validate configuration on startup
- ✅ Encrypt sensitive credentials
- ✅ Set file permissions to 600 (Unix) or equivalent (Windows)
- ✅ Store configuration in user-specific directories
- ✅ Never commit secrets to version control
- ✅ Use environment-specific configurations
- ✅ Regularly review and update configurations
- ✅ Enable automatic repair for production resilience

#### 5. Logging and Monitoring

- ✅ Enable INFO level logging minimum
- ✅ Monitor for authentication failures
- ✅ Monitor for rate limit violations
- ✅ Monitor converter sandbox violations
- ✅ Monitor file operation failures
- ✅ Set up alerts for security events
- ✅ Regularly review security logs
- ✅ Implement log rotation

#### 6. System Security

- ✅ Keep pyWATS Client updated
- ✅ Run service as non-privileged user
- ✅ Use machine authentication for stations
- ✅ Implement network-level security
- ✅ Keep Python and dependencies updated
- ✅ Use virtual environments
- ✅ Regular security audits

### Code Examples for Secure Implementation

#### Secure Service Initialization

```python
from pywats_client.service import AsyncConverterPool, AsyncIPCServer
from pywats_client.core.config import ClientConfig
from pywats_client.converters import SandboxConfig, ResourceLimits, SandboxCapability

# Load and validate configuration
config, repairs = ClientConfig.load_and_repair("/path/to/config.json")
if repairs:
    logger.warning(f"Configuration repaired: {repairs}")

# Create secure sandbox configuration
sandbox_config = SandboxConfig(
    capabilities=frozenset([
        SandboxCapability.READ_INPUT,
        SandboxCapability.WRITE_OUTPUT,
        SandboxCapability.LOG_INFO,
        SandboxCapability.LOG_WARNING,
        SandboxCapability.LOG_ERROR,
    ]),
    resource_limits=ResourceLimits(
        timeout_seconds=300,
        memory_mb=512,
        cpu_time_seconds=120,
    ),
    blocked_imports=frozenset([
        "subprocess", "os.system", "socket",
        "ctypes", "multiprocessing", "requests",
    ]),
)

# Create converter pool with sandbox enabled
pool = AsyncConverterPool(
    config=config,
    api=api,
    enable_sandbox=True,
    sandbox_config=sandbox_config,
)

# Create IPC server with authentication
ipc_server = AsyncIPCServer(
    instance_id=config.instance_id,
    enable_auth=True,
    rate_limiter=RateLimiter(
        max_tokens=20,
        refill_rate=100,
    ),
)

# Start services
await pool.start()
await ipc_server.start()
```

#### Secure File Operations

```python
from pywats_client.core.file_utils import (
    SafeFileWriter,
    SafeFileReader,
    locked_file,
)
from pathlib import Path

def save_report_securely(report_data: dict, output_path: Path):
    """Save report with all security best practices."""
    try:
        # Validate path to prevent traversal
        safe_path = validate_output_path(output_path)
        
        # Use atomic write with backup
        SafeFileWriter.write_json_atomic(
            path=safe_path,
            data=report_data,
            create_backup=True,
        )
        
        # Set restrictive permissions (Unix)
        if hasattr(os, 'chmod'):
            safe_path.chmod(0o600)
            
        logger.info(f"Report saved securely: {safe_path}")
        
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
        raise

def load_config_securely(config_path: Path) -> dict:
    """Load configuration with validation and recovery."""
    # Use safe reader with backup recovery
    data = SafeFileReader.read_json_safe(config_path)
    
    if data is None:
        logger.error("Configuration corrupted and no valid backup")
        # Create fresh config
        data = create_default_config()
        SafeFileWriter.write_json_atomic(
            path=config_path,
            data=data,
            create_backup=False,
        )
    
    return data

def update_shared_file(file_path: Path, update_fn):
    """Update file with proper locking."""
    try:
        with locked_file(file_path, mode='r+', timeout=10.0) as f:
            # Read current data
            data = json.load(f)
            
            # Apply update
            updated = update_fn(data)
            
            # Write back atomically
            f.seek(0)
            f.truncate()
            json.dump(updated, f, indent=2)
            
    except TimeoutError:
        logger.error("Could not acquire file lock")
        raise
    except Exception as e:
        logger.error(f"Failed to update file: {e}")
        raise
```

#### Secure Converter Implementation

```python
"""Example of a production-ready secure converter."""

from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ProductionConverter:
    """Production-ready converter with security best practices."""
    
    @property
    def name(self) -> str:
        return "ProductionConverter"
    
    @property
    def file_patterns(self) -> list:
        return ["*.csv", "*.txt"]
    
    @property
    def trusted_mode(self) -> bool:
        # Only enable after thorough review
        return False
    
    def convert_file(self, file_path: Path, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert file with comprehensive error handling.
        
        Args:
            file_path: Path to input file
            args: Converter arguments
            
        Returns:
            Result dictionary with status and data
        """
        try:
            # Validate inputs
            if not file_path.exists():
                return self._error_result("File not found")
            
            if file_path.stat().st_size > 100 * 1024 * 1024:  # 100MB
                return self._error_result("File too large")
            
            # Process file safely
            content = self._read_file_safely(file_path)
            report = self._process_content(content, args)
            
            # Validate output
            if not self._validate_report(report):
                return self._error_result("Invalid report generated")
            
            return {
                "status": "Success",
                "report": report,
                "metadata": {
                    "file_size": file_path.stat().st_size,
                    "converter_version": "1.0.0",
                }
            }
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}", exc_info=True)
            return self._error_result(str(e))
    
    def _read_file_safely(self, file_path: Path) -> str:
        """Read file with proper encoding handling."""
        try:
            # Try UTF-8 first
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1
            return file_path.read_text(encoding='latin-1')
    
    def _process_content(self, content: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Process file content."""
        # Implementation here
        return {}
    
    def _validate_report(self, report: Dict[str, Any]) -> bool:
        """Validate report structure."""
        required_fields = ["type", "partNumber", "serialNumber", "result"]
        return all(field in report for field in required_fields)
    
    def _error_result(self, error: str) -> Dict[str, Any]:
        """Create error result."""
        return {
            "status": "Failed",
            "error": error,
        }
```

### Security Testing

#### Test Checklist

- ✅ Test authentication with invalid tokens
- ✅ Test rate limiting with burst requests
- ✅ Test sandbox with malicious converters
- ✅ Test file operations with corrupted files
- ✅ Test concurrent file access
- ✅ Test configuration validation and repair
- ✅ Test path traversal prevention
- ✅ Test resource limit enforcement

#### Security Test Example

```python
import pytest
from pywats_client.core.security import validate_token, RateLimiter
from pywats_client.converters import ConverterValidator, SandboxConfig

def test_authentication_timing_safety():
    """Verify timing-safe comparison."""
    valid_token = "a" * 64
    
    # Should not be vulnerable to timing attacks
    assert validate_token(valid_token, valid_token) is True
    assert validate_token("b" * 64, valid_token) is False
    
def test_rate_limiting():
    """Verify rate limiting works."""
    limiter = RateLimiter(max_tokens=5, refill_rate=60)
    
    # Should allow burst
    for i in range(5):
        assert limiter.check("client-1") is True
    
    # Should reject after burst exhausted
    assert limiter.check("client-1") is False
    
def test_converter_validation():
    """Verify dangerous converters are blocked."""
    validator = ConverterValidator(SandboxConfig())
    
    dangerous_code = """
import subprocess
subprocess.run(["rm", "-rf", "/"])
    """
    
    is_valid, issues = validator.validate_source(dangerous_code)
    assert is_valid is False
    assert any("subprocess" in issue.lower() for issue in issues)
```

### Incident Response

#### Security Incident Checklist

1. **Detect**: Monitor logs for unusual activity
2. **Isolate**: Stop affected service instances
3. **Investigate**: Review logs and configuration
4. **Remediate**: Fix vulnerabilities, rotate secrets
5. **Recover**: Restart services with updated configuration
6. **Review**: Post-incident analysis and documentation

#### Example Monitoring Script

```python
#!/usr/bin/env python3
"""Security monitoring script."""

import re
from pathlib import Path
from datetime import datetime, timedelta


def monitor_security_events(log_file: Path, hours: int = 24):
    """Monitor log file for security events."""
    cutoff = datetime.now() - timedelta(hours=hours)
    
    # Patterns to watch for
    patterns = {
        "auth_failures": re.compile(r"DENIED invalid_token"),
        "rate_limits": re.compile(r"RATE_LIMIT rate_limit_exceeded"),
        "sandbox_violations": re.compile(r"SandboxSecurityError"),
        "file_errors": re.compile(r"FileNotFoundError|PermissionError"),
    }
    
    events = {key: [] for key in patterns}
    
    with log_file.open() as f:
        for line in f:
            # Parse timestamp
            # ... (implementation)
            
            # Check patterns
            for event_type, pattern in patterns.items():
                if pattern.search(line):
                    events[event_type].append(line)
    
    # Report findings
    for event_type, matches in events.items():
        if matches:
            print(f"\n{event_type}: {len(matches)} events")
            for match in matches[:5]:  # Show first 5
                print(f"  {match.strip()}")

if __name__ == "__main__":
    monitor_security_events(Path("/var/log/pywats/service.log"))
```

---

## Implementation References

### Files

**IPC Security:**
- `src/pywats_client/core/security.py` - Security utilities
- `src/pywats_client/service/async_ipc_server.py` - Server with auth/rate limiting
- `src/pywats_client/service/async_ipc_client.py` - Client with authentication

**Converter Security:**
- `src/pywats_client/converters/sandbox.py` - Sandbox implementation
- `src/pywats_client/converters/validator.py` - Converter validation
- `src/pywats_client/converters/config.py` - Sandbox configuration
- `src/pywats_client/service/async_converter_pool.py` - Pool with sandbox integration

**File Handling:**
- `src/pywats_client/core/file_utils.py` - Safe file operations
- `src/pywats_client/core/config.py` - Configuration validation

### Tests

**Security Tests:**
- `tests/client/test_security.py` - Security module tests (16 tests)
- `tests/client/test_ipc_auth.py` - IPC authentication tests (12 tests)
- `tests/client/test_sandbox.py` - Sandbox tests
- `tests/client/test_file_utils.py` - File utilities tests

### See Also

- [Troubleshooting Guide](../TROUBLESHOOTING.md) - Common issues and solutions
- [Getting Started Guide](../getting-started.md) - Initial setup
- [Configuration Reference](../reference/configuration.md) - Configuration options
