# pyWATS Installation Troubleshooting Guide

This guide covers common installation and configuration issues across all supported platforms.

---

## Quick Diagnostics

### Run the Diagnostic Tool

```bash
# If pyWATS is installed
python -m pywats_client diagnose

# With JSON output for support tickets
python -m pywats_client diagnose --json > diagnostics.json

# Or use the standalone script
python scripts/validate_install.py --full
```

### Check Service Status

**Windows:**
```powershell
Get-Service pyWATSClient
sc query pyWATSClient
```

**Linux (systemd):**
```bash
systemctl status pywats-client
journalctl -u pywats-client -n 50
```

**macOS (launchd):**
```bash
launchctl list | grep pywats
cat /var/log/pywats/stdout.log
```

---

## Windows Issues

### Installation Fails

#### "Windows protected your PC" (SmartScreen)
**Cause:** Unsigned installer  
**Solution:** Click "More info" → "Run anyway", or right-click → Properties → Unblock

#### "Access denied" during install
**Cause:** Not running as Administrator  
**Solution:** Right-click installer → "Run as administrator"

#### Missing Visual C++ Runtime
**Error:** `VCRUNTIME140.dll not found`  
**Solution:** Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Service Issues

#### Service won't start
1. Check Event Viewer: `eventvwr.msc` → Windows Logs → Application
2. Verify config.json is valid JSON
3. Check permissions on config directory

```powershell
# Check service status
sc query pyWATSClient

# View service errors
Get-EventLog -LogName Application -Source "pyWATSClient" -Newest 10
```

#### Service starts but stops immediately
**Cause:** Invalid configuration or missing token  
**Solution:**
1. Check `%PROGRAMDATA%\pyWATS\config.json`
2. Verify WATS server URL is correct
3. Ensure API token is valid

### Antivirus Issues

#### False positive detection
Some antivirus software may flag PyInstaller executables.

**Solutions:**
1. Add exclusion for `C:\Program Files\pyWATS\`
2. Whitelist `pywats-client.exe`
3. Report false positive to AV vendor

**Known AV Issues:**
- Windows Defender: Usually OK after SmartScreen bypass
- Symantec: May quarantine - add exclusion
- McAfee: May block network - add exception

---

## Linux Issues

### Installation Fails

#### DEB: Dependency errors
```bash
# Fix broken dependencies
sudo apt-get -f install

# Or install with dependencies
sudo apt-get install ./pywats-client.deb
```

#### RPM: Package conflicts
```bash
# Check for conflicts
rpm -ivh --test pywats-client.rpm

# Force install (not recommended)
rpm -ivh --force pywats-client.rpm
```

### Service Issues

#### systemd: Service fails to start
```bash
# Check status
systemctl status pywats-client

# Check logs
journalctl -u pywats-client -f

# Common fixes:
# 1. Check config file
cat /etc/pywats/config.json | python3 -m json.tool

# 2. Check permissions
ls -la /etc/pywats/
ls -la /var/lib/pywats/
ls -la /var/log/pywats/

# 3. Check user exists
id pywats
```

#### Permission denied on directories
```bash
# Fix ownership
sudo chown -R pywats:pywats /var/lib/pywats
sudo chown -R pywats:pywats /var/log/pywats
sudo chmod 750 /var/lib/pywats
```

### SELinux Issues (RHEL/Rocky/Alma)

#### Service blocked by SELinux
```bash
# Check for denials
sudo ausearch -m AVC -ts recent
sudo sealert -a /var/log/audit/audit.log

# Temporary: Set permissive mode
sudo setenforce 0

# Generate custom policy from denials
sudo ausearch -m AVC -ts recent | audit2allow -M pywats_local
sudo semodule -i pywats_local.pp

# Install official policy
cd /path/to/pywats/deployment/selinux
sudo ./install-selinux.sh
```

#### Common SELinux denials and fixes:

| Denial | Fix |
|--------|-----|
| `avc: denied { connect }` | Allow network: `setsebool -P httpd_can_network_connect 1` |
| `avc: denied { write }` to /var/log | Relabel: `restorecon -Rv /var/log/pywats` |
| `avc: denied { read }` config | Check file context: `ls -Z /etc/pywats/` |

---

## macOS Issues

### Installation Fails

#### "App is damaged and can't be opened"
**Cause:** Gatekeeper blocking unsigned app  
**Solution:**
```bash
# Remove quarantine attribute
xattr -cr "/Applications/pyWATS Client.app"
```

#### "Cannot be opened because the developer cannot be verified"
**Solution:**
1. System Preferences → Security & Privacy
2. Click "Open Anyway" next to the blocked app
3. Or: Right-click app → Open → Open

### Service Issues

#### launchd service won't start
```bash
# Check if loaded
launchctl list | grep pywats

# Load manually
launchctl load ~/Library/LaunchAgents/com.wats.pywats-client.plist

# Check for errors
launchctl error <error_code>

# View logs
cat /var/log/pywats/stderr.log
```

#### Permission issues
```bash
# Create directories
mkdir -p ~/Library/Application\ Support/pyWATS
mkdir -p ~/Library/Logs/pyWATS

# Fix permissions
chmod 755 ~/Library/Application\ Support/pyWATS
```

---

## Docker Issues

### Container won't start

#### Check logs
```bash
docker logs pywats-client
docker logs pywats-client --tail 50
```

#### Volume permission issues
```bash
# Check container user
docker exec pywats-client id

# Fix host directory permissions
sudo chown -R 1000:1000 /path/to/data

# Or run as root (not recommended for production)
docker run --user root ...
```

#### Health check failing
```bash
# Check health endpoint
docker exec pywats-client curl -f http://localhost:8080/health

# Check if service started
docker exec pywats-client ps aux
```

### Network Issues

#### Can't reach WATS server
```bash
# Test from container
docker exec pywats-client curl -v https://your-wats-server.com/api/version

# Check DNS
docker exec pywats-client nslookup your-wats-server.com

# Check if behind proxy
docker run -e HTTP_PROXY=http://proxy:8080 ...
```

---

## Raspberry Pi Issues

### Performance Issues

#### High memory usage
- Use headless mode (`--headless`)
- Limit concurrent file processing
- Increase swap (temporarily):
  ```bash
  sudo dphys-swapfile swapoff
  sudo nano /etc/dphys-swapfile  # Set CONF_SWAPSIZE=1024
  sudo dphys-swapfile setup
  sudo dphys-swapfile swapon
  ```

#### Slow file processing
- Use USB SSD instead of SD card
- Reduce logging level
- Disable watchdog polling (use inotify)

### Architecture Issues

#### Wrong architecture error
```
Exec format error
```
**Cause:** Running x86 binary on ARM  
**Solution:** Use ARM64 package or build from source:
```bash
pip install pywats-api[client-headless]
```

---

## Network & Connection Issues

### Can't connect to WATS server

1. **Check URL format:**
   ```
   ✓ https://company.wats.com
   ✗ https://company.wats.com/
   ✗ http://company.wats.com (must be HTTPS)
   ```

2. **Test connectivity:**
   ```bash
   curl -v https://your-server.wats.com/api/version
   ```

3. **Check proxy settings:**
   ```bash
   # Environment variables
   export HTTP_PROXY=http://proxy:8080
   export HTTPS_PROXY=http://proxy:8080
   export NO_PROXY=localhost,127.0.0.1
   ```

### SSL/TLS errors

#### Certificate verification failed
```
ssl.SSLCertVerificationError: certificate verify failed
```

**Solutions:**
1. Update CA certificates:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update && sudo apt-get install ca-certificates
   
   # RHEL/Rocky
   sudo dnf update ca-certificates
   ```

2. Check system time (certificate validation requires correct time)

3. For self-signed certs (development only):
   ```python
   # In config - NOT recommended for production
   "server": {
     "verify_ssl": false
   }
   ```

### Authentication errors

#### 401 Unauthorized
- Verify API token is correct
- Check token hasn't expired
- Ensure token has required permissions

#### 403 Forbidden
- Token may lack required scope
- Check if IP is allowlisted (if applicable)

---

## Configuration Issues

### Invalid JSON

```bash
# Validate JSON syntax
python3 -c "import json; json.load(open('/etc/pywats/config.json'))"

# Pretty-print for inspection
cat config.json | python3 -m json.tool
```

### Common config.json errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Expecting property name` | Trailing comma | Remove comma after last item |
| `Invalid \escape` | Backslash in path | Use forward slash or escape: `\\` |
| `Unterminated string` | Missing quote | Check for matching quotes |

### Minimal working config

```json
{
  "server": {
    "url": "https://your-company.wats.com",
    "token": "your-api-token"
  },
  "watch": {
    "directories": ["/path/to/test/results"],
    "patterns": ["*.json", "*.xml"]
  }
}
```

---

## Getting Help

### Information to Include in Support Requests

1. **Diagnostic output:**
   ```bash
   python -m pywats_client diagnose --json > diagnostics.json
   ```

2. **System information:**
   - OS and version
   - Python version
   - pyWATS version

3. **Logs:**
   - Service logs (last 100 lines)
   - Any error messages

4. **Steps to reproduce**

### Support Channels

- **GitHub Issues:** https://github.com/olreppe/pyWATS/issues
- **Documentation:** https://github.com/olreppe/pyWATS/docs
- **Email:** support@wats.com
