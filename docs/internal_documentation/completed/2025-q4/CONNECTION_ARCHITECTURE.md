# pyWATS Client - Connection & Authentication Architecture

## Overview

This document describes the persistent connection and authentication architecture for pyWATS Client, including multi-instance support and application separation.

## Connection States

### User-Facing States

1. **Not Connected** (Initial/Logged Out)
   - No authentication credentials stored
   - User must authenticate with server URL and password
   - Login screen shown on startup

2. **Connected** (Authenticated & Online)
   - Valid authentication token stored
   - Server reachable via health checks
   - Full functionality available

3. **Offline** (Authenticated but Server Unreachable)
   - Valid authentication token stored
   - Server temporarily unreachable
   - Offline queuing active
   - Automatic reconnection attempts

### Internal States

```
┌─────────────────┐
│  Not Connected  │ ◄─── Initial state or after user logout
└────────┬────────┘
         │ User clicks "Connect"
         │ Enters: Server URL + Password
         ▼
┌─────────────────┐
│  Authenticating │ ◄─── Exchanging credentials for token
└────────┬────────┘
         │ Success: Store token + start health checks
         ▼
┌─────────────────┐
│    Connected    │ ◄─── Token valid + Server reachable
│     (Online)    │
└────────┬────────┘
         │ Health check fails
         ▼
┌─────────────────┐
│    Offline      │ ◄─── Token valid but server unreachable
└────────┬────────┘
         │ Health check succeeds
         └──────────► Back to Connected
```

## Authentication Flow

### Initial Authentication

```
User Input:
├── Server URL (https://company.wats.com)
└── Password (user-specific API password)

Authentication Process:
1. Validate server URL format
2. Exchange password for API token
3. Store encrypted token in config
4. Store connection state = "Connected"
5. Start health monitoring
6. Launch main GUI
```

### Token Storage

```json
{
  "instance_id": "abc123",
  "connection": {
    "server_url": "https://company.wats.com",
    "token_encrypted": "...",  // AES encrypted
    "connection_state": "Connected",
    "last_connected": "2025-12-12T10:00:00Z",
    "username": "station01"
  }
}
```

### Health Monitoring

```python
# Connection health check interval (configurable)
health_check_interval = 30  # seconds

# Health check API call
async def check_health():
    try:
        # Simple API call to verify connectivity
        response = await client.process.refresh()
        return True  # Server reachable
    except:
        return False  # Server unreachable
```

## Multi-Instance Support

### Instance Identification

Each pyWATS Client instance has:
- **Instance ID**: Unique identifier (UUID or user-defined)
- **Instance Name**: User-friendly name ("Station 1", "Line A - EOL")
- **Storage Path**: Dedicated folder for config/data

### Instance Storage Structure

```
%APPDATA%/pyWATS/
├── instances/
│   ├── station1/              ← Instance 1
│   │   ├── config.json
│   │   ├── queue/
│   │   ├── converters/
│   │   └── logs/
│   ├── line-a-eol/            ← Instance 2
│   │   ├── config.json
│   │   ├── queue/
│   │   └── ...
│   └── default/               ← Default instance
│       └── ...
└── instances.json             ← Instance registry
```

### Instance Registry

```json
{
  "instances": [
    {
      "id": "station1",
      "name": "Station 1",
      "path": "C:/ProgramData/pyWATS/instances/station1",
      "type": "configurator",
      "last_used": "2025-12-12T10:00:00Z"
    },
    {
      "id": "line-a-eol",
      "name": "Line A - End of Line",
      "path": "C:/ProgramData/pyWATS/instances/line-a-eol",
      "type": "yield_monitor",
      "last_used": "2025-12-12T09:30:00Z"
    }
  ],
  "default_instance": "station1"
}
```

## Application Split

### 1. pyWATS Client Configurator

**Purpose**: Configuration and administrative tasks

**Features**:
- Connection management
- Converter configuration
- Serial number pool management
- Process list synchronization
- Software distribution settings
- Report queue management
- System settings

**Access**: Requires authentication

### 2. pyWATS Yield Monitor

**Purpose**: Real-time operator interface for SPC

**Features**:
- Live yield monitoring
- SPC charts (X-bar, R, Cpk)
- Alert notifications
- Operator dashboard
- Minimal configuration required

**Access**: Can run with read-only access

### Shared Services

Both applications share:
- Connection service (same authentication)
- Data storage (same instance)
- Report queue
- Process cache

## Connection Management Service

### Enhanced ConnectionService

```python
class ConnectionService:
    """
    Manages persistent connection with health monitoring.
    
    Features:
    - Password-to-token authentication
    - Encrypted token storage
    - Connection health monitoring
    - Automatic reconnection
    - State persistence
    """
    
    def __init__(self, instance_config: InstanceConfig):
        self.config = instance_config
        self._status = ConnectionState.NOT_CONNECTED
        self._health_check_task = None
        self._health_check_interval = 30
        
    async def authenticate(self, server_url: str, password: str) -> bool:
        """
        Authenticate with server and store token.
        
        Args:
            server_url: WATS server URL
            password: User password
            
        Returns:
            True if authentication successful
        """
        # Exchange password for token
        token = await self._exchange_credentials(server_url, password)
        
        if token:
            # Encrypt and store token
            self.config.connection.token_encrypted = encrypt(token)
            self.config.connection.server_url = server_url
            self.config.connection.state = "Connected"
            self.config.save()
            
            # Start health monitoring
            await self.start_health_monitoring()
            return True
        
        return False
    
    async def disconnect(self):
        """User-initiated disconnect. Clear credentials."""
        # Stop health monitoring
        await self.stop_health_monitoring()
        
        # Clear token and state
        self.config.connection.token_encrypted = None
        self.config.connection.state = "Not Connected"
        self.config.save()
        
        self._status = ConnectionState.NOT_CONNECTED
    
    async def start_health_monitoring(self):
        """Start periodic health checks."""
        if self._health_check_task:
            return
        
        self._health_check_task = asyncio.create_task(
            self._health_check_loop()
        )
    
    async def _health_check_loop(self):
        """Periodic health check loop."""
        while True:
            try:
                # Simple API call to check connectivity
                await self._client.process.refresh()
                
                # Server reachable
                if self._status == ConnectionState.OFFLINE:
                    logger.info("Connection restored")
                    self._status = ConnectionState.CONNECTED
                    
            except Exception as e:
                # Server unreachable
                if self._status == ConnectionState.CONNECTED:
                    logger.warning(f"Connection lost: {e}")
                    self._status = ConnectionState.OFFLINE
            
            await asyncio.sleep(self._health_check_interval)
```

## Login Screen

### Separate Login Window

The login screen is shown:
- On first launch (no stored credentials)
- After user logout
- When stored token is invalid/expired

```
┌────────────────────────────────────┐
│        pyWATS Client Login         │
├────────────────────────────────────┤
│                                    │
│  Server URL:                       │
│  ┌──────────────────────────────┐ │
│  │ https://company.wats.com     │ │
│  └──────────────────────────────┘ │
│                                    │
│  Password:                         │
│  ┌──────────────────────────────┐ │
│  │ ●●●●●●●●●●●●                 │ │
│  └──────────────────────────────┘ │
│                                    │
│  ☐ Remember connection             │
│                                    │
│  Instance:                         │
│  ┌──────────────────────────────┐ │
│  │ Station 1              ▼     │ │
│  └──────────────────────────────┘ │
│                                    │
│     [Cancel]      [Connect]        │
│                                    │
│  Status: Connecting...             │
└────────────────────────────────────┘
```

### Post-Authentication Flow

```
Successful Authentication
    ↓
Store token + state = "Connected"
    ↓
Start health monitoring service
    ↓
Close login window
    ↓
Launch selected application:
    ├── Configurator (default)
    └── Yield Monitor
```

## Configuration Schema Updates

### Enhanced ClientConfig

```python
@dataclass
class ConnectionConfig:
    """Connection-specific configuration"""
    server_url: str = ""
    token_encrypted: str = ""  # AES encrypted API token
    connection_state: str = "Not Connected"  # "Not Connected", "Connected"
    last_connected: Optional[datetime] = None
    username: str = ""
    health_check_interval: int = 30  # seconds
    auto_reconnect: bool = True

@dataclass
class InstanceConfig:
    """Instance-specific configuration"""
    instance_id: str
    instance_name: str
    instance_type: str  # "configurator", "yield_monitor"
    storage_path: Path
    connection: ConnectionConfig
    # ... rest of config
```

## Implementation Phases

### Phase 1: Connection Service Enhancement
- [x] Design architecture
- [ ] Implement ConnectionState enum
- [ ] Add password-to-token authentication
- [ ] Implement token encryption/storage
- [ ] Add health monitoring loop
- [ ] Add disconnect functionality

### Phase 2: Login Screen
- [ ] Create LoginWindow (separate QMainWindow)
- [ ] Add server URL input
- [ ] Add password input (masked)
- [ ] Add instance selector
- [ ] Implement authentication flow
- [ ] Add connection status display

### Phase 3: Multi-Instance Support
- [ ] Create instance registry
- [ ] Implement instance storage structure
- [ ] Add instance management (create/delete/switch)
- [ ] Update config to support instances
- [ ] Add instance selection to login

### Phase 4: Application Split
- [ ] Extract configurator functionality
- [ ] Create yield monitor application
- [ ] Implement shared service access
- [ ] Add application launcher

### Phase 5: Integration & Testing
- [ ] Update existing GUI to check auth state
- [ ] Test multi-instance scenarios
- [ ] Test connection persistence
- [ ] Test offline/online transitions
- [ ] Test authentication flow

## Security Considerations

### Token Encryption

```python
from cryptography.fernet import Fernet

# Use machine-specific key derivation
def get_encryption_key() -> bytes:
    """Get machine-specific encryption key."""
    # Derive key from machine ID + salt
    machine_id = get_machine_id()
    return derive_key(machine_id)

def encrypt_token(token: str) -> str:
    """Encrypt API token for storage."""
    f = Fernet(get_encryption_key())
    return f.encrypt(token.encode()).decode()

def decrypt_token(encrypted: str) -> str:
    """Decrypt stored API token."""
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted.encode()).decode()
```

### Password Handling

- Never store passwords
- Only use password for initial token exchange
- Clear password from memory after use
- Use secure password input field (masked)

## Benefits

1. **Better UX**: Users see a clear connection state
2. **Offline Support**: Client works offline with queuing
3. **Security**: Tokens encrypted, passwords never stored
4. **Multi-Instance**: Multiple stations on same PC
5. **Flexibility**: Different apps for different roles
6. **Reliability**: Automatic reconnection on network issues

## Migration from Current System

Current system has:
- `service_address` field
- `api_token` field (stored as plain text)
- No connection state persistence

Migration:
1. Detect old config format
2. Encrypt existing token
3. Set connection_state = "Connected" if token exists
4. Migrate to new structure
5. Show login on next disconnect

---

**Status**: Design Complete - Ready for Implementation
**Last Updated**: December 12, 2025
