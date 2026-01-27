#!/bin/bash
# pyWATS Appliance First-Boot Configuration Script
#
# This script provides an interactive wizard for configuring the pyWATS
# appliance on first boot. It can also be run manually for reconfiguration.
#
# Usage:
#   sudo first-boot-setup.sh          # Interactive wizard
#   sudo first-boot-setup.sh --silent # Non-interactive (uses env vars)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration paths
CONFIG_FILE="/etc/pywats/config.json"
SERVICE_NAME="pywats-client"

# Default values
DEFAULT_HEALTH_PORT=8080
DEFAULT_LOG_LEVEL="INFO"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}ERROR: This script must be run as root (sudo)${NC}"
    exit 1
fi

# Print banner
print_banner() {
    clear
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║           pyWATS Virtual Appliance Configuration              ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# Print section header
print_section() {
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  $1${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Prompt for input with default value
prompt() {
    local prompt_text="$1"
    local default_value="$2"
    local var_name="$3"
    local is_password="$4"
    
    if [ "$is_password" = "password" ]; then
        echo -n -e "${GREEN}$prompt_text${NC} "
        read -s value
        echo ""
    else
        if [ -n "$default_value" ]; then
            echo -n -e "${GREEN}$prompt_text${NC} [${default_value}]: "
        else
            echo -n -e "${GREEN}$prompt_text${NC}: "
        fi
        read value
    fi
    
    if [ -z "$value" ]; then
        value="$default_value"
    fi
    
    eval "$var_name='$value'"
}

# Validate URL
validate_url() {
    local url="$1"
    if [[ $url =~ ^https?:// ]]; then
        return 0
    else
        return 1
    fi
}

# Test connection to WATS server
test_connection() {
    local url="$1"
    local token="$2"
    
    echo -n "Testing connection to WATS server... "
    
    # Try health endpoint
    local response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "${url}/api/health" 2>/dev/null || echo "000")
    
    if [ "$response" = "200" ] || [ "$response" = "401" ]; then
        echo -e "${GREEN}OK${NC}"
        return 0
    else
        echo -e "${RED}FAILED (HTTP $response)${NC}"
        return 1
    fi
}

# Configure network
configure_network() {
    print_section "Network Configuration"
    
    echo "Current network configuration:"
    ip addr show | grep -E "^[0-9]+:|inet " | head -10
    echo ""
    
    prompt "Configure static IP? (y/n)" "n" use_static
    
    if [ "$use_static" = "y" ] || [ "$use_static" = "Y" ]; then
        prompt "IP Address" "" static_ip
        prompt "Subnet mask (CIDR, e.g., 24)" "24" subnet
        prompt "Gateway" "" gateway
        prompt "DNS Server" "8.8.8.8" dns
        
        # Get interface name
        IFACE=$(ip route | grep default | awk '{print $5}' | head -1)
        
        # Create netplan config
        cat > /etc/netplan/01-pywats.yaml << EOF
network:
  version: 2
  ethernets:
    $IFACE:
      dhcp4: false
      addresses:
        - $static_ip/$subnet
      routes:
        - to: default
          via: $gateway
      nameservers:
        addresses:
          - $dns
EOF
        
        echo "Applying network configuration..."
        netplan apply
        
        echo -e "${GREEN}Network configured successfully${NC}"
    else
        echo "Keeping DHCP configuration."
    fi
}

# Configure WATS server connection
configure_wats() {
    print_section "WATS Server Configuration"
    
    # Server URL
    while true; do
        prompt "WATS Server URL (e.g., https://wats.company.com)" "" wats_url
        
        if validate_url "$wats_url"; then
            break
        else
            echo -e "${RED}Invalid URL. Please include http:// or https://${NC}"
        fi
    done
    
    # API Token
    prompt "API Token" "" wats_token "password"
    
    # Test connection
    echo ""
    if test_connection "$wats_url" "$wats_token"; then
        echo -e "${GREEN}Server connection verified!${NC}"
    else
        echo -e "${YELLOW}Warning: Could not verify server connection.${NC}"
        echo "The service will retry connection on startup."
        prompt "Continue anyway? (y/n)" "y" continue_anyway
        if [ "$continue_anyway" != "y" ] && [ "$continue_anyway" != "Y" ]; then
            echo "Configuration cancelled."
            exit 1
        fi
    fi
}

# Configure watch folders
configure_folders() {
    print_section "Folder Configuration"
    
    prompt "Watch folder (for incoming test files)" "/var/lib/pywats/watch" watch_folder
    prompt "Archive folder (for processed files)" "/var/lib/pywats/archive" archive_folder
    prompt "Failed folder (for failed files)" "/var/lib/pywats/failed" failed_folder
    
    # Create folders if they don't exist
    mkdir -p "$watch_folder" "$archive_folder" "$failed_folder"
    chown -R pywats:pywats "$watch_folder" "$archive_folder" "$failed_folder"
    
    echo -e "${GREEN}Folders created/verified${NC}"
}

# Write configuration file
write_config() {
    print_section "Saving Configuration"
    
    # Backup existing config
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "${CONFIG_FILE}.bak.$(date +%Y%m%d%H%M%S)"
    fi
    
    # Write new config
    cat > "$CONFIG_FILE" << EOF
{
    "server": {
        "url": "$wats_url",
        "token": "$wats_token"
    },
    "client": {
        "watch_folder": "$watch_folder",
        "archive_folder": "$archive_folder",
        "failed_folder": "$failed_folder"
    },
    "logging": {
        "level": "$DEFAULT_LOG_LEVEL",
        "file": "/var/log/pywats/client.log"
    },
    "health": {
        "port": $DEFAULT_HEALTH_PORT
    }
}
EOF
    
    # Set permissions
    chown pywats:pywats "$CONFIG_FILE"
    chmod 640 "$CONFIG_FILE"
    
    echo -e "${GREEN}Configuration saved to $CONFIG_FILE${NC}"
}

# Start service
start_service() {
    print_section "Starting pyWATS Service"
    
    echo "Enabling service..."
    systemctl enable $SERVICE_NAME
    
    echo "Starting service..."
    systemctl restart $SERVICE_NAME
    
    # Wait for service to start
    sleep 3
    
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}Service started successfully!${NC}"
        echo ""
        echo "Service status:"
        systemctl status $SERVICE_NAME --no-pager | head -10
    else
        echo -e "${RED}Service failed to start${NC}"
        echo ""
        echo "Check logs with: journalctl -u $SERVICE_NAME -f"
    fi
}

# Print summary
print_summary() {
    print_section "Configuration Complete!"
    
    # Get IP address
    local ip_addr=$(hostname -I | awk '{print $1}')
    
    echo "Your pyWATS appliance is now configured."
    echo ""
    echo "Summary:"
    echo "  ├─ WATS Server: $wats_url"
    echo "  ├─ Watch Folder: $watch_folder"
    echo "  ├─ Archive Folder: $archive_folder"
    echo "  ├─ Failed Folder: $failed_folder"
    echo "  └─ Health Endpoint: http://$ip_addr:$DEFAULT_HEALTH_PORT/health"
    echo ""
    echo "Useful commands:"
    echo "  ├─ Check service status: systemctl status $SERVICE_NAME"
    echo "  ├─ View logs: journalctl -u $SERVICE_NAME -f"
    echo "  ├─ Restart service: systemctl restart $SERVICE_NAME"
    echo "  └─ Edit config: nano $CONFIG_FILE"
    echo ""
    echo -e "${YELLOW}SECURITY: Remember to change the default 'pywats' user password!${NC}"
    echo "  Run: passwd pywats"
    echo ""
}

# Disable first-boot service (so it doesn't run again)
disable_firstboot() {
    if systemctl is-enabled --quiet pywats-firstboot 2>/dev/null; then
        systemctl disable pywats-firstboot
        rm -f /etc/systemd/system/pywats-firstboot.service
        systemctl daemon-reload
    fi
}

# Silent mode (non-interactive)
run_silent() {
    echo "Running in silent mode..."
    
    # Check required environment variables
    if [ -z "$PYWATS_SERVER_URL" ] || [ -z "$PYWATS_API_TOKEN" ]; then
        echo "ERROR: PYWATS_SERVER_URL and PYWATS_API_TOKEN must be set"
        exit 1
    fi
    
    wats_url="$PYWATS_SERVER_URL"
    wats_token="$PYWATS_API_TOKEN"
    watch_folder="${PYWATS_WATCH_FOLDER:-/var/lib/pywats/watch}"
    archive_folder="${PYWATS_ARCHIVE_FOLDER:-/var/lib/pywats/archive}"
    failed_folder="${PYWATS_FAILED_FOLDER:-/var/lib/pywats/failed}"
    
    # Create folders
    mkdir -p "$watch_folder" "$archive_folder" "$failed_folder"
    chown -R pywats:pywats "$watch_folder" "$archive_folder" "$failed_folder"
    
    write_config
    start_service
    disable_firstboot
    
    echo "Configuration complete."
}

# Main wizard
run_wizard() {
    print_banner
    
    echo "This wizard will help you configure your pyWATS appliance."
    echo "Press Ctrl+C at any time to cancel."
    echo ""
    prompt "Press Enter to continue..." "" continue_prompt
    
    configure_network
    configure_wats
    configure_folders
    write_config
    start_service
    disable_firstboot
    print_summary
}

# Main entry point
main() {
    if [ "$1" = "--silent" ] || [ "$1" = "-s" ]; then
        run_silent
    else
        run_wizard
    fi
}

main "$@"
