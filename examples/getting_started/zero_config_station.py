"""Zero-Configuration Example - Auto-Detection of Station

This example demonstrates pyWATS auto-detecting the station name
from the environment without requiring manual configuration.

Station auto-detection priority (highest to lowest):
1. PYWATS_STATION environment variable
2. COMPUTERNAME environment variable (Windows)
3. socket.gethostname() (cross-platform fallback)
"""

import os
from pywats import pyWATS
from pywats.core.station import Station, Purpose

print("=" * 70)
print("pyWATS Zero-Configuration Example")
print("=" * 70)
print()

# Example 1: Default auto-detection (uses hostname)
print("Example 1: Default Auto-Detection")
print("-" * 70)

# Create API client without specifying station
api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-token-here"
)

print(f"Auto-detected station: {api.station.name}")
print(f"  Location: {api.station.location or '(not set)'}")
print(f"  Purpose: {api.station.purpose}")
print()

# Example 2: Environment variable override
print("Example 2: Environment Variable Override")
print("-" * 70)

# Set PYWATS_STATION environment variable
os.environ['PYWATS_STATION'] = 'PRODUCTION-LINE-01'

# Create new client - will use environment variable
api2 = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-token-here"
)

print(f"Station from PYWATS_STATION: {api2.station.name}")
print(f"  Location: {api2.station.location or '(not set)'}")
print(f"  Purpose: {api2.station.purpose}")
print()

# Clean up
del os.environ['PYWATS_STATION']

# Example 3: Manual override still works
print("Example 3: Manual Station Configuration")
print("-" * 70)

# Explicitly provide station (overrides auto-detection)
custom_station = Station(
    name="CUSTOM-STATION",
    location="Building A, Floor 2",
    purpose=Purpose.PRODUCTION
)

api3 = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-token-here",
    station=custom_station
)

print(f"Custom station: {api3.station.name}")
print(f"  Location: {api3.station.location}")
print(f"  Purpose: {api3.station.purpose}")
print()

# Example 4: Change station after creation
print("Example 4: Change Station After Creation")
print("-" * 70)

# Start with auto-detection
api4 = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-token-here"
)

print(f"Initial station: {api4.station.name}")

# Change station later
api4.station = Station(
    name="UPDATED-STATION",
    location="Lab 3",
    purpose=Purpose.DEBUG
)

print(f"Updated station: {api4.station.name}")
print(f"  Location: {api4.station.location}")
print(f"  Purpose: {api4.station.purpose}")
print()

# Example 5: Multi-station hub mode
print("Example 5: Multi-Station Hub Mode")
print("-" * 70)

# Create hub client
hub = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-token-here"
)

# Add multiple stations to registry
hub.stations.add("line-1", Station("LINE-01", "Building A", Purpose.PRODUCTION))
hub.stations.add("line-2", Station("LINE-02", "Building A", Purpose.PRODUCTION))
hub.stations.add("debug", Station("DEBUG-STATION", "Lab", Purpose.DEBUG))

# Switch between stations
hub.stations.set_active("line-1")
print(f"Active station: {hub.station.name}")

hub.stations.set_active("debug")
print(f"Active station: {hub.station.name}")
print()

print("=" * 70)
print("Benefits of Auto-Detection:")
print("=" * 70)
print("✓ Zero configuration required for simple setups")
print("✓ Automatically uses computer hostname as station name")
print("✓ Easy to override via environment variable (PYWATS_STATION)")
print("✓ Manual configuration still fully supported")
print("✓ Perfect for production lines with consistent naming")
print()

print("Common Patterns:")
print("-" * 70)
print("1. Dev/Test: Auto-detect from hostname (zero config)")
print("2. Production: Set PYWATS_STATION env var per station")
print("3. Custom: Provide explicit Station object")
print("4. Multi-station: Use StationRegistry for hub mode")
print()
