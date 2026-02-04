# Side-by-Side GUI Test Fixture

Compare the old (A) and new (B) pyWATS GUI implementations running simultaneously.

## Overview

This test fixture launches both GUI versions side by side:
- **Client A** (Original): `pywats_client/gui` - Production stable version
- **Client B** (Improved): `pywats_ui/apps/configurator` - Reliability-enhanced version

## Features

### Token Sharing
Client B automatically reads the API token from Client A's configuration if B's token is missing. This allows seamless testing without re-authenticating.

### Separate Configurations
Each client uses its own configuration instance to prevent conflicts:
- Client A: `~/.pywats/config/<instance>.json`
- Client B: `~/.pywats/config/<instance>_new.json`

### Side-by-Side Layout
- Client A positioned on the left (50, 50)
- Client B positioned on the right (700, 50)

## Usage

### Basic Launch
```bash
python test_both_guis.py
```
Launches both GUIs with default instance name.

### Specify Instance
```bash
python test_both_guis.py --instance dev
```
Uses "dev" as the instance name for configurations.

### Disable Token Sharing
```bash
python test_both_guis.py --no-token-share
```
Prevents automatic token sharing from A to B.

## What to Test

### Feature Comparison
- ✅ All pages present in both GUIs
- ✅ Configuration options match
- ✅ API endpoints identical
- ✅ File paths and converters compatible

### Reliability Improvements (Client B)
- **H1 (Error Handling)**: All user operations show error dialogs instead of crashing
- **H3 (Event Loop)**: Async operations don't block UI
- **H4 (Cleanup)**: Resources cleaned up on window close
- **C1 (Queue Manager)**: Offline queue for API requests
- **C3 (Offline Capability)**: Visual indicators and auto-sync when reconnecting
- **M1 (Retry Logic)**: Network operations retry with exponential backoff

### Specific Test Scenarios

#### 1. Connection Resilience
- **Client A**: May freeze when service is down
- **Client B**: Shows offline banner, queues requests, auto-reconnects

#### 2. Configuration Changes
- **Client A**: Changes might be lost on crash
- **Client B**: Auto-saves on every change with validation

#### 3. Error Handling
- **Client A**: May show cryptic errors or crash
- **Client B**: User-friendly error dialogs with retry options

#### 4. Converters Page
- **Both**: Should show same system converters
- **Client B**: Better error handling for malformed files
- **Client B**: More informative status messages

## Expected Behavior

### On Launch
```
================================================================
pyWATS Side-by-Side GUI Test Fixture
================================================================
Instance: default
Client A: Old GUI (pywats_client.gui)
Client B: New GUI (pywats_ui.apps.configurator)
================================================================

Checking token sharing...
✓ Found token in Client A config (length: 256)
✓ Token shared from Client A to Client B

Launching Client A (Old GUI)...
✓ Client A launched successfully

Launching Client B (New GUI)...
✓ Client B launched successfully

================================================================
Both GUIs launched successfully!
Compare features, reliability, and UI improvements.
================================================================
```

### Window Titles
- **Client A**: `pyWATS Client A (Original) - <instance>`
- **Client B**: `pyWATS Client B (Improved) - <instance>`

## Troubleshooting

### Client A Fails to Launch
```
Failed to launch Client A: No module named 'pywats_client.gui'
```
**Solution**: Old GUI module not found. Run with only Client B:
```bash
python run_configurator.py --instance test
```

### Client B Fails to Launch
```
Failed to launch Client B: No module named 'pywats_ui'
```
**Solution**: New GUI not installed. Install in development mode:
```bash
pip install -e .
```

### No Token Sharing
```
ℹ No token found in Client A config
```
**Action**: Configure Client A first, then relaunch test fixture.

### Both Windows on Same Position
**Solution**: Manually move windows to compare side by side.

## Architecture Differences

### Client A (Original)
- Direct IPC communication with service
- Basic error handling (try/catch)
- Synchronous operations
- Manual refresh for status
- No offline queue

### Client B (Improved)
- Same IPC + QueueManager for offline capability
- Comprehensive error handling with user dialogs (H1)
- Async operations with event loop guards (H3)
- Auto-refresh with ConnectionMonitor
- Offline queue with auto-retry (C1)
- Cleanup on close (H4)
- Multi-instance support (H5)

## Migration Status

All 11 configurator pages migrated:
- ✅ Dashboard
- ✅ Setup
- ✅ Connection
- ✅ Serial Numbers
- ✅ API Settings
- ✅ **Converters** ← Latest
- ✅ Software
- ✅ Location
- ✅ Proxy
- ✅ Log
- ✅ About

## Next Steps

1. **Run test fixture**: Validate both GUIs side by side
2. **Compare features**: Ensure parity between versions
3. **Test reliability**: Simulate network failures, service restarts
4. **Document differences**: Note any behavior changes
5. **Update CHANGELOG**: Document improvements

## Exit

Close either window or press `Ctrl+C` in terminal to shut down both GUIs.
