# Deployment Infrastructure

This folder contains platform-specific deployment configurations and packaging files.

**⚠️ NOT Published** - These files are excluded from the PyPI package and are for development/deployment use only.

## Folder Structure

```
deployment/
├── README.md                   # This file
├── debian/                     # Debian/Ubuntu packaging
│   ├── control
│   ├── postinst
│   ├── prerm
│   ├── postrm
│   └── pywats-client.service
├── rpm/                        # RHEL/Rocky/AlmaLinux packaging
│   └── pywats-client.spec
├── selinux/                    # SELinux policy module
│   ├── pywats.te
│   ├── pywats.fc
│   └── install.sh
├── packer/                     # VM appliance templates
│   ├── template.pkr.hcl
│   └── autoinstall.yaml
└── docker/                     # Docker deployment
    ├── Dockerfile
    └── docker-compose.yml
```

## Platform Packaging

### Debian/Ubuntu (.deb)

Build DEB package for Debian-based distributions:

```bash
cd deployment/debian
dpkg-buildpackage -b -uc -us
```

**Supports:**
- Ubuntu 22.04/24.04 LTS
- Debian 11/12
- Raspberry Pi OS (64-bit)

### RHEL/Rocky/AlmaLinux (.rpm)

Build RPM package for Red Hat-based distributions:

```bash
cd deployment/rpm
rpmbuild -ba pywats-client.spec
```

**Supports:**
- RHEL 8/9
- Rocky Linux 8/9
- AlmaLinux 8/9

### SELinux Policy

Install SELinux policy module (RHEL/Rocky/Alma):

```bash
cd deployment/selinux
sudo ./install.sh
```

## Container Deployment

### Docker

Build and run Docker container:

```bash
cd deployment/docker
docker-compose up -d
```

Or build manually:

```bash
docker build -t pywats-client -f deployment/docker/Dockerfile .
```

**Multi-architecture support:**
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM64/Apple Silicon)

## VM Appliances

### Packer

Build VM appliances for multiple hypervisors:

```bash
cd deployment/packer
packer build template.pkr.hcl
```

**Output formats:**
- OVA (VMware/VirtualBox)
- QCOW2 (KVM/Proxmox)
- VHD (Hyper-V)

**Base:** Ubuntu 22.04 LTS with pyWATS pre-installed

## CI/CD Integration

### GitHub Actions

Deployment workflows are defined in `.github/workflows/`:
- `docker.yml` - Docker image builds and publishing
- `test-platforms.yml` - Multi-platform testing

### Building Packages in CI

All platform packages are built automatically on release:
1. DEB packages for Ubuntu/Debian
2. RPM packages for RHEL/Rocky/Alma
3. Docker images for amd64/arm64
4. VM appliances for hypervisors

## Packaging Configuration

### Excluded from PyPI

This entire `deployment/` folder is excluded via `MANIFEST.in`:

```plaintext
prune deployment
```

### Included in Git

All deployment files are tracked in git for version control and CI/CD.

## Platform Documentation

For detailed platform setup and compatibility:

- **[Platform Compatibility Guide](../docs/platforms/platform-compatibility.md)** - Complete matrix
- **[Windows IoT LTSC](../docs/platforms/windows-iot-ltsc.md)** - IoT-specific setup
- **[Docker Deployment](../docs/installation/docker.md)** - Container guide
- **[Windows Service](../docs/installation/windows-service.md)** - Windows setup
- **[Linux Service](../docs/installation/linux-service.md)** - systemd setup
- **[macOS Service](../docs/installation/macos-service.md)** - launchd setup

## Contributing

When adding new platform support:

1. Create appropriate packaging files in this folder
2. Add CI/CD workflow in `.github/workflows/`
3. Update platform documentation in `docs/platforms/`
4. Test on target platform before merging
5. Update `docs/platforms/platform-compatibility.md`

## Support

For deployment issues, refer to:
- [Error Catalog](../docs/reference/error-catalog.md)
- [Quick Reference](../docs/reference/quick-reference.md)
- Platform-specific guides in `docs/platforms/`
