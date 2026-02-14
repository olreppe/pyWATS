# Multi-Instance Setup and Old GUI Removal Plan

## Phase 1: Remove Old GUI (pywats_client.gui)
**Files to DELETE:**
- src/pywats_client/gui/ (entire directory)
  * EXCEPT: Keep any shared utilities if referenced elsewhere

**Files to UPDATE:**
- Remove old GUI imports from test_both_guis.py (update to use instance A/B pattern)
- Update run_gui.py if it exists
- Check for any other references

## Phase 2: Multi-Instance Analysis

### Current Multi-Instance Support ✅
**Already Implemented:**
1. **ConfigManager** - Supports instance_id parameter
   - Path: `~/.pywats/instances/{instance_id}/client_config.json`
   - Default instance: "default"
   - Multi-instance: Any custom instance_id

2. **ClientConfig** - Has instance_id field
   - Tracks which instance it belongs to
   - Can be loaded per-instance

3. **Queue Paths** - Should be instance-specific
   - Currently: `~/.pywats/queue/` (GLOBAL - needs fix!)
   - Should be: `~/.pywats/instances/{instance_id}/queue/`

4. **Log Files** - Should be instance-specific
   - Currently: `client.log` (GLOBAL - needs fix!)
   - Should be: `instances/{instance_id}/client.log`

### Multi-Instance Gaps to Fix 🔧
1. **Queue Directory** - Not instance-specific
2. **Log File Paths** - Not instance-specific
3. **Reports Folder** - Not instance-specific
4. **Converters Folder** - Not instance-specific
5. **Cache Directory** - Should be instance-specific

## Phase 3: Dual Client Setup (A + B)

**Client A (Master - "default"):**
- Instance ID: "default"
- Config: `~/.pywats/instances/default/client_config.json`
- Queue: `~/.pywats/instances/default/queue/`
- Logs: `~/.pywats/instances/default/logs/`
- Port: 8080 (if API enabled)

**Client B (Secondary - "client_b"):**
- Instance ID: "client_b"
- Config: `~/.pywats/instances/client_b/client_config.json`
- Queue: `~/.pywats/instances/client_b/queue/`
- Logs: `~/.pywats/instances/client_b/logs/`
- Port: 8081 (if API enabled)

**Test Fixtures:**
- test_both_guis.py → Update to launch A and B as separate instances
- Create test_instance_isolation.py → Verify no cross-contamination
- Create test_multi_instance.py → Test concurrent operation

## Phase 4: Implementation Steps

### Step 1: Remove Old GUI
```bash
git rm -r src/pywats_client/gui/
```

### Step 2: Fix Multi-Instance Paths
Update ConfiguratorMainWindow and config handling to use instance-specific paths for:
- Queue directory
- Log files  
- Reports folder
- Converters folder
- Cache directory

### Step 3: Create Dual Instance Launchers
- run_client_a.py (master, instance="default")
- run_client_b.py (secondary, instance="client_b")
- test_both_instances.py (launches both)

### Step 4: Update Test Fixtures
- Update test_both_guis.py to use new dual instance pattern
- Create instance isolation tests
- Create concurrent operation tests

### Step 5: Documentation
- Document multi-instance configuration
- Update README with dual instance testing
- Create MULTI_INSTANCE_GUIDE.md

## Phase 5: Verification

### Tests to Run:
1. ✅ Client A runs alone (single instance)
2. ✅ Client B runs alone (different instance)
3. ✅ Both run concurrently without conflicts
4. ✅ Configs are isolated
5. ✅ Queues are isolated
6. ✅ Logs are isolated
7. ✅ No port conflicts (if API enabled)

### Expected Outcomes:
- Old GUI completely removed
- All features preserved in new GUI
- True multi-instance support
- No file/resource conflicts between instances
- Clean test fixtures for A + B testing

---

**Execution Order:**
1. Backup current state (git commit)
2. Remove old GUI
3. Fix multi-instance paths
4. Create dual launchers
5. Update test fixtures
6. Test everything
7. Document
8. Final commit
