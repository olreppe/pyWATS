## Description
Complete service/GUI separation architecture

## Changes
- Service architecture redesign matching C# WATS Client
- System tray moved to service
- GUI improvements (simplified nav, File menu)
- API auto-discovery
- Environment variable fixes for credential persistence

## Testing
- [x] Service starts and runs
- [x] GUI connects to service via IPC
- [x] Credentials persist between sessions
- [x] Auto-discovery works

## Documentation
- [x] Updated GETTING_STARTED.md
- [x] Updated ENV_VARIABLES.md
