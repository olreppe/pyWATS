# Installation & Deployment Documentation

This directory contains guides for installing, deploying, and configuring the pyWATS client service across different platforms and environments.

## Client Installation

- **[Client Installation](client.md)** - End-user client installation for test stations
  - GUI mode setup
  - Headless mode setup
  - Configuration options
  - Converter installation
  - Multi-instance support

## Service Deployment

Install the client as a system service for automatic startup:

- **[Windows Service](windows-service.md)** - Install as Windows Service (auto-start on boot)
  - NSSM installation
  - Service configuration
  - Multiple instance setup
  - Troubleshooting

- **[Linux Service](linux-service.md)** - Install as systemd service (Ubuntu, RHEL, Debian)
  - Systemd unit file
  - Environment configuration
  - Service management
  - Log monitoring

- **[macOS Service](macos-service.md)** - Install as launchd daemon (auto-start on boot)
  - Launch agent setup
  - Plist configuration
  - Service management
  - Troubleshooting

## Container Deployment

- **[Docker Deployment](docker.md)** - Container deployment guide for production and development
  - Docker Compose setup
  - Environment variables
  - Volume mounting
  - Multi-container orchestration
  - Production best practices

## Documentation Structure

Each installation guide includes:
- **Prerequisites** - Required software and dependencies
- **Step-by-Step Instructions** - Detailed installation process
- **Configuration** - Environment variables and settings
- **Service Management** - Start, stop, restart commands
- **Troubleshooting** - Common issues and solutions
- **Verification** - How to confirm successful installation

## Quick Links

- **Quick Start**: See [client.md](client.md) for basic installation
- **Production**: See [docker.md](docker.md) for containerized deployment
- **Development**: See [../getting-started.md](../getting-started.md) for developer setup

## See Also

- **[../INDEX.md](../INDEX.md)** - Main documentation index
- **[../client-architecture.md](../client-architecture.md)** - Client service internals
- **[../getting-started.md](../getting-started.md)** - Developer installation and setup
- **[../env-variables.md](../env-variables.md)** - Environment variable reference
