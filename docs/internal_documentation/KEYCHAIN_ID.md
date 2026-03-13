# Credential Storage & Clone-Safe Identity

**Date:** February 18, 2026  
**Status:** Proposal  
**Author:** pyWATS Team

---

## Problem

When a station is cloned (disk image, directory copy, VM snapshot), the cloned station connects to WATS immediately using the original's credentials — no prompt, no conflict detection. This happens because `api_token`, `proxy_password`, and `webhook_auth_value` are stored as **plaintext in `client_config.json`**, which travels with any copy.

| What gets cloned | Should it? |
|---|---|
| Service address, station name, log settings, queue config | **Yes** — safe to share |
| API token, proxy password, webhook auth | **No** — must be unique per station |

---

## Proposed Solution: OS Keychain via `keyring`

Move all secrets out of config files and into the operating system's native credential store using Python's [`keyring`](https://pypi.org/project/keyring/) library (MIT, 50M+ monthly downloads — used by pip, Azure CLI, AWS CLI).

### Platform Backends

| Platform | Backend | Machine-Bound | Survives Clone |
|---|---|---|---|
| Windows | Credential Manager (DPAPI) | Yes — encrypted to machine+user SID | **No** |
| macOS | Keychain | Yes — per-machine-user | **No** |
| Linux (desktop) | GNOME Keyring / KDE Wallet | Yes — user session keyring | **No** |
| Linux (headless) | Fallback to Fernet + machine-ID | Yes — key derived from `/etc/machine-id` | **No** |

### API

```python
import keyring

# Store (once, during setup)
keyring.set_password("pyWATS/default", "api_token", "base64credential")

# Retrieve (every startup)
token = keyring.get_password("pyWATS/default", "api_token")
# Returns None if not found → prompt user
```

---

## Architecture

```
client_config.json (clonable)          OS Credential Store (not clonable)
┌──────────────────────────────┐       ┌──────────────────────────────┐
│ service_address: "https://…" │       │ pyWATS/{instance_id}:        │
│ station_name: "STATION-01"   │       │   api_token     = "base64…" │
│ proxy_host: "proxy:8080"     │       │   proxy_password = "…"      │
│ instance_id: "default"       │       │   webhook_auth   = "…"      │
│ log_level: "INFO"            │       │   ipc_secret     = "hex…"   │
│ … (settings only, NO secrets)│       └──────────────────────────────┘
└──────────────────────────────┘                 ↑ machine-bound
        safe to clone ✓                          ↑ empty after clone ✓
```

## Startup Flow

```
Start → Load config.json → keyring.get_password("api_token")
                              │
                         ┌────┴─────┐
                         │ Found?   │
                         ├── Yes ───┤→ Normal startup (connect to WATS)
                         ├── No ────┤→ Prompt for credentials (GUI/CLI)
                         └──────────┘   → Store in keyring → continue
```

A cloned station has no keyring entries → **forced to re-authenticate before connecting**.

---

## Migration

On first startup after upgrade:

1. If `api_token` exists in `client_config.json` → copy to keyring → remove from JSON
2. Same for `proxy_password` and `webhook_auth_value`
3. Legacy configs continue to work — migration is automatic and one-time

## Headless Fallback

If no OS keyring is available (Docker, headless server):

1. Fall back to existing `encryption.py` Fernet encryption (key derived from machine-ID)
2. Secrets stored encrypted on disk — still machine-bound, still clone-safe
3. Environment variable override remains supported (`PYWATS_API_TOKEN`)

## Dependencies

```
keyring>=24.0.0          # Required — single dependency, pure Python
keyrings.alt>=5.0.0      # Optional — file-based backend for headless Linux
```

---

## Summary

| Aspect | Current | Proposed |
|---|---|---|
| Secret storage | Plaintext in JSON | OS keychain (DPAPI / Keychain / Secret Service) |
| Clone safety | None — clone connects immediately | Clone has empty keyring → prompt |
| Cross-platform | N/A | Windows, macOS, Linux (desktop + headless) |
| Migration effort | — | Automatic on first startup |
| New dependencies | — | 1 (`keyring`) |
| Config file changes | Contains secrets | Settings only — safe to clone/share |
