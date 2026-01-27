#!/bin/bash
# Install SELinux policy module for pyWATS
#
# This script installs the pyWATS SELinux policy module on RHEL/Rocky/AlmaLinux.
# Run as root.

set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: This script must be run as root"
    exit 1
fi

# Check if SELinux is enabled
if ! command -v getenforce &> /dev/null; then
    echo "SELinux tools not found. Is this an SELinux-enabled system?"
    exit 1
fi

SELINUX_STATUS=$(getenforce)
echo "SELinux status: $SELINUX_STATUS"

if [ "$SELINUX_STATUS" = "Disabled" ]; then
    echo "SELinux is disabled. No policy module needed."
    exit 0
fi

# Check for required tools
for cmd in checkmodule semodule_package semodule semanage; do
    if ! command -v $cmd &> /dev/null; then
        echo "Installing required tool: $cmd"
        dnf install -y policycoreutils-python-utils selinux-policy-devel
        break
    fi
done

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Building SELinux policy module..."

# Compile the policy module
checkmodule -M -m -o pywats.mod pywats.te

# Create the policy package
semodule_package -o pywats.pp -m pywats.mod -f pywats.fc

echo "Installing SELinux policy module..."

# Install the policy module
semodule -i pywats.pp

echo "Setting file contexts..."

# Apply file contexts
semanage fcontext -a -t pywats_etc_t "/etc/pywats(/.*)?" 2>/dev/null || true
semanage fcontext -a -t pywats_var_lib_t "/var/lib/pywats(/.*)?" 2>/dev/null || true
semanage fcontext -a -t pywats_log_t "/var/log/pywats(/.*)?" 2>/dev/null || true

# Restore contexts on existing directories
if [ -d /etc/pywats ]; then
    restorecon -Rv /etc/pywats
fi
if [ -d /var/lib/pywats ]; then
    restorecon -Rv /var/lib/pywats
fi
if [ -d /var/log/pywats ]; then
    restorecon -Rv /var/log/pywats
fi

# Allow binding to port 8080 if not already allowed
semanage port -a -t http_cache_port_t -p tcp 8080 2>/dev/null || true

echo ""
echo "=========================================="
echo "SELinux policy module installed!"
echo "=========================================="
echo ""
echo "The pyWATS service can now run with SELinux in enforcing mode."
echo ""
echo "To verify:"
echo "  semodule -l | grep pywats"
echo ""
echo "To remove the policy module:"
echo "  semodule -r pywats"
echo ""

# Verify installation
echo "Installed modules:"
semodule -l | grep pywats || echo "Warning: Module not found in list"

echo ""
echo "Done!"
