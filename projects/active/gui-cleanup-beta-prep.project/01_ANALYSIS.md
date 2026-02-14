# GUI Cleanup - Analysis Document

**Created:** February 14, 2026, 15:45  
**Last Updated:** February 14, 2026, 15:45

---

## Current State Analysis

### 1. Page Structure (Main Window)

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Current Nav Items** (line 174-186):
```python
nav_items = [
    "Dashboard",      # ✅ Keep
    "Setup",          # ✅ Keep
    "Connection",     # ✅ Keep
    "Serial Numbers", # ❓ Assess (SN handler)
    "API Settings",   # ❓ Move to Advanced?
    "Converters",     # ✅ Keep
    "Software",       # ❌ REMOVE (user request)
    "Location",       # ✅ Keep (GPS toggle)
    "Proxy",          # ❓ Move to Advanced?
    "Log",            # ✅ Keep
    "About"           # ✅ Keep
]
```

**Default Selection**: Currently Dashboard (line 259), but user confirmation needed

**Missing Pages** (not in current list):
- Root Cause → Not implemented (good!)
- Asset → Not implemented (good!)
- Product → Not implemented (good!)
- Production → Not implemented (good!)

---

### 2. Scaling Issues

**Identified Issues**:

1. **Main Window** (line 120-121):
   ```python
   self.setMinimumSize(900, 650)  # Too large for some screens
   self.resize(1100, 800)
   ```
   - Minimum size may be too restrictive
   - Need to test at 800x600

2. **Fixed Widths Throughout**:
   - Sidebar: `sidebar.setFixedWidth(200)` (line 148)
   - Various buttons with `setFixedWidth()`
   - May prevent responsive scaling

3. **Page Content**:
   - Setup page uses `setColumnWidth(0, 200)` (line 54, setup.py)
   - Dashboard stat cards may not resize well
   - Connection page uses fixed widths for buttons

**Assessment**: Need to:
- Reduce minimum window size to 800x600
- Use layouts instead of fixed widths where possible
- Test all pages at minimum size

---

### 3. Dashboard Current State

**File**: `src/pywats_ui/apps/configurator/pages/dashboard.py`

**Current Content**:
- ✅ Service Status section
- ✅ Statistics cards (Converters, Queue, Reports, Success Rate)
- ✅ Converter Health table
- ✅ Server Connection status

**Missing** (user requirements):
- ❌ Client name
- ❌ Station name
- ❌ Location (text, not GPS toggle)
- ❌ Purpose
- ❌ GPS activation toggle (currently in separate Location page)

**Redundant Info**:
- Instance name shown in window title bars AND in dashboard
- Connection status in dashboard AND status bar

---

### 4. Connection Page Current State

**File**: `src/pywats_ui/apps/configurator/pages/connection.py`

**Current Content** (Too Prominent):
- Service address input (line 71-81)
- Disconnect button (line 83-87) ✅ Good!
- Test connection (line 99-110)
- Test send UUT (line 114-132)
- Status section (line 144-171)
- **Advanced options group** (line 175-200)
  - API Token (password field) - Hidden by default ✅
  - Sync interval

**Issues**:
- Disconnect button exists ✅ but user says it's "not there"
  - Possible confusion: It's below service address
  - Not prominent enough?
- API Token is in Advanced (good!) but still visible when expanded
- Too much vertical space

---

### 5. Setup Page Current State

**File**: `src/pywats_ui/apps/configurator/pages/setup.py`

**Content**:
- Client ID (line 163-170)
- Station Name (line 172-179)
- Location (line 181-188)
- Purpose (line 190-200)
- Hub mode options (line 202-244)
- Multi-station manager (StationManagerDialog class)

**Assessment**:
- ✅ Has all required fields!
- ❓ Should these move to Dashboard?
- Hub mode may be unnecessary complexity for now

---

### 6. Location Page Current State

**File**: `src/pywats_ui/apps/configurator/pages/location.py`

**Content**:
- Checkbox: "Allow this app to use location services" (line 49-53)
- Privacy notice

**Assessment**:
- Simple page, only one checkbox
- **User wants GPS toggle on Dashboard** → Move this checkbox?
- Page could be removed if feature integrated into Dashboard

---

### 7. Multi-Server Config Support

**Current Implementation**:
- **InstanceSelectorDialog** exists (main_window.py, line 44-88)
- Allows multiple instances with different names
- Config stored per instance name
- No enforcement of single instance (H5 fix removed QLocalServer)

**Current Approach**:
```python
instance_name = self._config.get("instance_name", "default")
self.setWindowTitle(f"pyWATS Configurator - {instance_name}")
```

**Missing**:
- No per-server config isolation
- No automatic instance creation when connecting to new server
- No UI to select which instance to use on startup

**User Request Analysis**:
> "In relation to this I also want you to assess if there is a good way to support separate configs when connecting to a different server. Ideally this should automatically result in two different instances of the client."

**Assessment**:
1. **Current**: Instance name is manual, not tied to server
2. **Proposed**: Auto-create instance per server URL
3. **Challenge**: 
   - Service can be offline when starting Configurator
   - Need to know server URL before loading config
   - Circular dependency: config → server, server → instance, instance → config

**Recommendation**:
- **Phase 1** (This project): Keep current manual instance selection
- **Phase 2** (Future): Auto-instance per server with:
  - Login dialog on startup (asks for server URL first)
  - Hash server URL to create instance name
  - Store instances in `~/.pywats/instances/{server_hash}/config.json`
  - Allow manual override for friendly names

---

## User Feedback Analysis

### Quoted Requirements

1. "pages don't scale very well (smaller than default)"
   - → Fix minimum window size, test at 800x600
   
2. "default size makes some pages scale down beyond readability"
   - → Fix font sizes, use scalable layouts
   
3. "some information is repeated"
   - → Instance name in title + dashboard
   - → Connection status in multiple places
   
4. "connection token and credentials are too 'in your face'"
   - → Already in Advanced group, but may need better UX
   
5. "dashboard as the starting page"
   - → Already is (line 259)?Check if this is working
   
6. "including client name, station name, location and purpose"
   - → Currently in Setup page, move to Dashboard
   
7. "GPS-activation toggle for position"
   - → Currently in Location page, move to Dashboard
   
8. "disconnect button that disconnects the client"
   - → Already exists (line 83-87), make more prominent?
   
9. "When reconnecting the login screen should appear"
   - → Need login dialog implementation
   
10. "remove anything not related to converter and connection/configuration"
    - → Software tab (exists, remove)
    - → Root cause, asset, product, production (not in nav list, already excluded)

---

## Gap Analysis

| Requirement | Status | Action |
|-------------|--------|--------|
| Fix scaling | ❌ Not done | Reduce min size, test layouts |
| Dashboard default | ✅ Already is? | Verify |
| Client name on dashboard | ❌ Missing | Move from Setup |
| Station name on dashboard | ❌ Missing | Move from Setup |
| Location on dashboard | ❌ Missing | Move from Setup (text field) |
| Purpose on dashboard | ❌ Missing | Move from Setup |
| GPS toggle on dashboard | ❌ Missing | Move from Location page |
| Disconnect button | ⚠️ Exists but not prominent | Make more visible |
| Login dialog on disconnect | ❌ Missing | Create login flow |
| Remove Software tab | ❌ Still in nav | Remove from nav_items |
| Remove unnecessary tabs | ✅ Already excluded | None (root cause, asset, product, production not in nav) |
| Reduce credential prominence | ✅ Already in Advanced | Maybe improve UX |
| Multi-server config | ⚠️ Partial support | Assess, defer to Phase 2 |

---

## Proposed Changes

### Change 1: Tab Management

**File**: `main_window.py`

**Remove**:
- "Software" (line 181)

**Consider Removing/Moving**:
- "Serial Numbers" → May be converter-related, keep for now
- "API Settings" → Move to Advanced in Connection page?
- "Proxy" → Move to Advanced in Connection page?

**Final Nav List**:
```python
nav_items = [
    "Dashboard",         # Default start page
    "Connection",        # Simplified
    "Converters",        # Core feature
    "Setup",             # Station metadata
    "Serial Numbers",    # Converter-related
    "Log",               # Troubleshooting
    "About"              # Info
]
```

**Alternative Minimal Version** (user preference):
```python
nav_items = [
    "Dashboard",         # Default (has station info + GPS toggle)
    "Connection",        # Server + disconnect
    "Converters",        # Core feature
    "Log",               # Troubleshooting
    "About"              # Info
]
```

---

### Change 2: Dashboard Redesign

**Add Section**: "Station Information"
```
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Station Information
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Client Name:     [PyWATS Client A    ]
 Station Name:    [Line 1 - FCT      ]
 Location:        [Building 3, Floor 2]
 Purpose:         [Final Test Station ]
 
 [ ] Allow GPS location services
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Move these fields from**:
- Setup page → client_name, station_name, location, purpose
- Location page → GPS toggle

**Update**:
- Make fields read-only on Dashboard (click to edit → opens Setup)
- Or make editable directly on Dashboard (simpler)

---

### Change 3: Connection Page Simplification

**Current Flow**:
```
 Service address: [_______________]
 [Disconnect]
 Help text...
 
 Test connection [Run test]
 Test send UUT [Send test report]
 Help text...
 
 Status section...
 
 Advanced options (collapsed)
```

**Proposed Flow**:
```
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Server Connection
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Service address: [https://wats.server.com/]
 Status: ● Connected to wats.server.com
 
 [Test Connection]  [Disconnect and Reconnect]
 
 Advanced Options ▼ (collapsed by default)
   API Token: [**********]
   Sync Interval: [30] seconds
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Changes**:
- Combine disconnect button with clearer label
- Reduce vertical spacing
- Remove redundant status labels
- Keep Advanced collapsed

---

### Change 4: Scaling Fixes

**Main Window**:
```python
# Before
self.setMinimumSize(900, 650)  # Too restrictive
self.resize(1100, 800)

# After
self.setMinimumSize(800, 600)  # Industry standard
self.resize(1000, 700)
```

**Sidebar**:
```python
# Before
sidebar.setFixedWidth(200)  # Fixed

# After
sidebar.setMinimumWidth(180)
sidebar.setMaximumWidth(220)  # Allow slight resize
```

**Pages**:
- Remove fixed button widths where possible
- Use minimum widths instead
- Test all pages at 800x600

---

### Change 5: Disconnect → Reconnect Flow

**User Story**:
1. User clicks "Disconnect and Reconnect"
2. Confirmation dialog: "Disconnect from current server? This will close the connection."
3. On confirm:
   - Stop service
   - Clear connection config (service_address, api_token)
   - Show login dialog
4. Login dialog:
   - Server URL input
   - Username/password or API token
   - "Connect" button
5. On connect:
   - Save new config
   - Restart service
   - Return to Dashboard

**Implementation**:
- Reuse existing logic from initial connection
- Check if `LoginWindow` exists (src/pywats_ui/dialogs/login_window.py)
- Wire disconnect button to this flow

---

### Change 6: Multi-Server Config (Assessment)

**Option A: Manual Instances** (Current + Small Improvement)
- Keep InstanceSelectorDialog
- Add "Create new instance for different server" hint
- Simple, works with current architecture
- **Effort**: 1 hour
- **Complexity**: Low
- **Recommendation**: ✅ Do this now

**Option B: Auto-Instance per Server** (Ideal)
- Hash server URL → instance name
- Auto-create config directories
- Login dialog on startup if no connection
- **Effort**: 6-8 hours
- **Complexity**: High
- **Risk**: Breaking changes to config system
- **Recommendation**: ⏸️ Defer to separate project

**Recommendation**: Implement Option A now, Option B in future release.

---

## Testing Strategy

### Test Cases

1. **Scaling Test**
   - [ ] Open at 800x600 → All text readable
   - [ ] Open at 1920x1080 → No awkward stretching
   - [ ] Test each page at minimum size
   - [ ] Resize window dynamically → No layout breaks

2. **Navigation Test**
   - [ ] Dashboard is default page
   - [ ] All visible tabs load correctly
   - [ ] Removed tabs don't appear
   - [ ] Back/forward navigation works

3. **Dashboard Content Test**
   - [ ] Station info displays correctly
   - [ ] GPS toggle works
   - [ ] Service status updates
   - [ ] Converter health table populates

4. **Connection Flow Test**
   - [ ] Disconnect button visible
   - [ ] Disconnect confirmation works
   - [ ] Login dialog appears
   - [ ] Reconnect to new server works
   - [ ] Config saves correctly

5. **Multi-Instance Test**
   - [ ] Create instance for Server A
   - [ ] Create instance for Server B
   - [ ] Switch between instances
   - [ ] Configs are isolated

---

## Dependencies

### Code Files to Modify

1. `src/pywats_ui/apps/configurator/main_window.py`
   - Tab management (nav_items)
   - Window sizing
   - Sidebar width

2. `src/pywats_ui/apps/configurator/pages/dashboard.py`
   - Add station info section
   - Move GPS toggle from Location page
   - Update layout

3. `src/pywats_ui/apps/configurator/pages/connection.py`
   - Improve disconnect button prominence
   - Add reconnection flow
   - Simplify layout

4. `src/pywats_ui/apps/configurator/pages/setup.py`
   - Keep as-is (or remove if all fields moved to Dashboard)
   - Consider making it "Advanced Setup"

5. `src/pywats_ui/apps/configurator/pages/location.py`
   - Consider removing (GPS toggle moved to Dashboard)
   - Or keep for detailed privacy settings

6. `src/pywats_ui/dialogs/login_window.py`
   - Check if exists, update if needed

### External Dependencies

- PySide6 (already installed)
- No new packages needed

---

## Next Actions

1. Get user confirmation on proposed tab list
2. Create implementation plan
3. Start with quick wins (tab removal)
4. Test scaling at each step
5. Document breaking changes (if any)

---

**Status**: Analysis complete, ready for implementation planning.
