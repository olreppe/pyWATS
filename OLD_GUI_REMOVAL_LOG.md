# Old GUI Removal and Multi-Instance Setup

**Date:** February 5, 2026

## Actions Taken

### Phase 1: Old GUI Removal ✅
- Removed `src/pywats_client/gui/` directory (entire old GUI)
- Converters page has fallback to QPlainTextEdit (no feature loss)
- test_both_guis.py will be updated to use new dual instance pattern

### Phase 2: Multi-Instance Path Fixes ✅
Fixed instance-specific paths:
- Queue: `~/.pywats/instances/{instance_id}/queue/`
- Logs: `~/.pywats/instances/{instance_id}/logs/`
- Reports: `~/.pywats/instances/{instance_id}/reports/`
- Converters: `~/.pywats/instances/{instance_id}/converters/`

### Phase 3: Dual Instance Setup ✅
Created:
- `run_client_a.py` - Master instance (instance_id="default")
- `run_client_b.py` - Secondary instance (instance_id="client_b")
- `test_both_instances.py` - Launch both for testing

### Phase 4: Test Verification
- Single instance test (A alone)
- Single instance test (B alone)
- Dual instance test (A + B concurrent)
- Instance isolation verification
