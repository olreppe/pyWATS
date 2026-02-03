# Internal Endpoint Risk Documentation

**Last Updated:** February 3, 2026  
**Audience:** Users, Developers, DevOps  
**Severity:** Medium-High (Pre-release), Low (Stable)

---

## ⚠️ Overview

pyWATS currently connects to an **internal WATS server endpoint** whose structure and API contract **may change without notice**. This creates a dependency risk that users should be aware of, especially in pre-release and beta versions.

---

## 📊 Risk Assessment by Version

| Version Type | Risk Level | Endpoint Stability | User Impact |
|-------------|------------|-------------------|-------------|
| **0.x.xbX** (Pre-release) | 🔴 **HIGH** | May change daily | API calls may break |
| **0.x.x** (Beta) | 🟡 **MEDIUM** | Relatively stable | Occasional issues |
| **1.0.0+** (Stable) | 🟢 **LOW** | Versioned, guaranteed | Minimal risk |

---

## 🎯 What This Means for Users

### Potential Issues

If the internal endpoint structure changes, you may experience:

1. **Authentication Failures**
   ```python
   # Error example
   AuthenticationError: Invalid credentials
   # Even though credentials are correct
   ```

2. **Data Format Changes**
   ```python
   # Expected: Report object
   report = wats.report.get("123")
   
   # Actual: May receive unexpected format
   # Error: KeyError: 'serial_number'
   ```

3. **Missing or Renamed Fields**
   ```python
   # Old endpoint returned:
   {"serialNumber": "SN123", "status": "passed"}
   
   # New endpoint returns:
   {"serial_number": "SN123", "test_status": "passed"}
   # pyWATS expects old field names → error
   ```

4. **API Method Failures**
   ```python
   # Method worked yesterday
   reports = wats.report.query_reports(status="passed")
   
   # Today: 404 Not Found
   # Endpoint was renamed or removed
   ```

---

## 🛠️ What To Do If This Happens

### Step 1: Update pyWATS

```bash
# Check current version
pip show pywats

# Update to latest
pip install --upgrade pywats

# Verify new version
pip show pywats
```

### Step 2: Check Release Notes

```bash
# Visit GitHub releases
https://github.com/olreppe/pyWATS/releases

# Look for:
- Endpoint compatibility fixes
- Breaking change notices
- Migration guides
```

### Step 3: Verify Endpoint Compatibility

```python
from pywats import WATS

# Test basic connectivity
wats = WATS(base_url="https://your-server")

try:
    # Simple test query
    result = wats.report.get("test-id")
    print("✅ Endpoint compatible")
except Exception as e:
    print(f"❌ Endpoint issue: {e}")
```

### Step 4: Contact Support

If issues persist after updating:

1. **Check GitHub Issues:**
   - https://github.com/olreppe/pyWATS/issues
   - Search for "endpoint" or your specific error

2. **Open New Issue:**
   - Include pyWATS version
   - Include error message
   - Include minimal reproducible example

3. **Contact Development Team:**
   - Email: [your-team-email]
   - Slack: #pywats-support

### Step 5: Rollback (If Critical)

```bash
# Find last working version
pip list | grep pywats

# Rollback to specific version
pip install pywats==0.1.5  # Replace with last working version

# Verify
python -c "import pywats; print(pywats.__version__)"
```

---

## 🔮 Mitigation Roadmap

We are actively working to eliminate this risk:

### Phase 1: Versioned Endpoints (Target: v0.3.0)
- [ ] Implement `/api/v1/` endpoint prefix
- [ ] Version all API routes
- [ ] Support multiple API versions simultaneously
- [ ] Graceful degradation for older clients

### Phase 2: Backward Compatibility (Target: v0.5.0)
- [ ] Endpoint change detection
- [ ] Automatic field mapping
- [ ] Deprecation warnings before removals
- [ ] 6-month deprecation period

### Phase 3: Stable API Contract (Target: v1.0.0)
- [ ] Formal API specification (OpenAPI)
- [ ] Semantic versioning for API changes
- [ ] Breaking changes only in major versions
- [ ] Migration tools for version upgrades

---

## 📋 Current Endpoint Dependencies

### Critical Endpoints

| Endpoint | Used By | Risk If Changed |
|----------|---------|-----------------|
| `/api/report/get` | `wats.report.get()` | High - core functionality |
| `/api/report/query` | `wats.report.query_reports()` | High - core functionality |
| `/api/product/get` | `wats.product.get()` | Medium - product lookups |
| `/api/process/list` | `wats.process.list_processes()` | Low - admin features |

### Authentication Endpoints

| Endpoint | Used By | Risk If Changed |
|----------|---------|-----------------|
| `/auth/token` | `WATS.__init__()` | **CRITICAL** - auth breaks entirely |
| `/auth/validate` | Token validation | High - session issues |

---

## 🔍 Monitoring & Alerts

### Automated Checks (Future)

We plan to implement:

1. **Endpoint Health Monitoring:**
   - Automated daily checks against known endpoints
   - Alert if endpoint structure changes
   - Publish compatibility status

2. **Version Compatibility Matrix:**
   ```
   pyWATS Version | Endpoint Version | Status
   0.2.0-beta.1   | Internal 2.3.x   | ✅ Compatible
   0.2.0-beta.2   | Internal 2.4.x   | ⚠️  Partial
   0.3.0          | API v1           | ✅ Versioned
   ```

3. **Breaking Change Notifications:**
   - Email alerts for endpoint changes
   - RSS feed for compatibility updates
   - Slack notifications for critical issues

---

## 📖 Best Practices for Users

### 1. Pin Your Version (Production)

```toml
# pyproject.toml or requirements.txt
pywats==0.2.0  # Exact version, not >=0.2.0
```

**Why:** Prevents surprise updates with breaking endpoint changes

### 2. Test Updates in Staging First

```bash
# Development/Staging
pip install --upgrade pywats

# Run your test suite
pytest tests/

# If successful, promote to production
```

### 3. Use Try-Except for Critical Calls

```python
from pywats import WATS
from pywats.exceptions import AuthenticationError, APIError
import logging

wats = WATS(base_url="https://server")

try:
    report = wats.report.get("SN123")
except AuthenticationError:
    logging.error("Authentication failed - endpoint may have changed")
    # Fallback logic or alert
except APIError as e:
    logging.error(f"API error: {e}")
    # Investigate or rollback
```

### 4. Monitor Release Notes

- Subscribe to GitHub releases
- Check before updating
- Read migration guides

### 5. Keep Backups of Working Versions

```bash
# Save working wheel locally
pip download pywats==0.2.0 -d ./backups/

# Install from backup if needed
pip install ./backups/pywats-0.2.0-py3-none-any.whl
```

---

## 🐛 Known Issues & Workarounds

### Issue 1: Authentication Token Format Changed

**Symptom:**
```
AuthenticationError: Invalid token format
```

**Cause:** Internal auth endpoint expects different token structure

**Workaround:**
```python
# Update to latest pyWATS
pip install --upgrade pywats

# If that doesn't work, clear cached tokens
import os
os.remove(os.path.expanduser("~/.pywats/token_cache.json"))

# Re-authenticate
wats = WATS(base_url="https://server", username="user", password="pass")
```

### Issue 2: Report Fields Renamed

**Symptom:**
```
AttributeError: 'Report' object has no attribute 'serialNumber'
```

**Cause:** Endpoint switched from camelCase to snake_case

**Workaround:**
```python
# Old code
serial = report.serialNumber

# New code (0.2.0+)
serial = report.serial_number
```

---

## 📞 Support & Contact

### Reporting Endpoint-Related Issues

**GitHub Issue Template:**
```markdown
**Issue:** Endpoint compatibility error

**pyWATS Version:** 0.2.0-beta.1
**Server Version:** [if known]
**Error Message:**
```
[paste error]
```

**Steps to Reproduce:**
1. Initialize WATS client
2. Call wats.report.get("123")
3. Observe error

**Expected Behavior:** Should return Report object

**Actual Behavior:** AuthenticationError
```

### Emergency Hotline

For **production-blocking** endpoint issues:
- Email: [emergency-email]
- On-call: [phone/pager]
- Response SLA: 4 hours

---

## 📅 Timeline to Stability

| Milestone | Target | Status |
|-----------|--------|--------|
| Versioned Endpoints (v0.3.0) | Q2 2026 | 🚧 Planned |
| Backward Compat (v0.5.0) | Q3 2026 | 💡 Planned |
| Stable API Contract (v1.0.0) | Q4 2026 | 💡 Planned |
| Public API Specification | Q4 2026 | 💡 Planned |

---

## ✅ When This Document Becomes Obsolete

This risk documentation will be **archived** when:

- [ ] Versioned endpoints implemented (`/api/v1/`)
- [ ] Backward compatibility guaranteed
- [ ] Breaking change policy established
- [ ] Migration path for all endpoint changes
- [ ] Reached stable v1.0.0

**Target:** Q4 2026

---

**For the latest status, see:** [GitHub Milestones](https://github.com/olreppe/pyWATS/milestones)
