# Packer Template for pyWATS Virtual Appliance
#
# Builds OVA/QCOW2/VHD images for various hypervisors.
# Base: Ubuntu Server 22.04 LTS (minimal cloud image)
#
# Build commands:
#   packer build -var 'output_format=ova' pywats-appliance.pkr.hcl
#   packer build -var 'output_format=qcow2' pywats-appliance.pkr.hcl
#   packer build -var 'output_format=vhd' pywats-appliance.pkr.hcl

packer {
  required_plugins {
    qemu = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/qemu"
    }
    virtualbox = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/virtualbox"
    }
  }
}

# Variables
variable "output_format" {
  type        = string
  default     = "ova"
  description = "Output format: ova, qcow2, or vhd"
}

variable "ubuntu_version" {
  type        = string
  default     = "22.04"
  description = "Ubuntu LTS version"
}

variable "pywats_version" {
  type        = string
  default     = "1.0.0"
  description = "pyWATS version to install"
}

variable "vm_name" {
  type        = string
  default     = "pywats-appliance"
  description = "Virtual machine name"
}

variable "disk_size" {
  type        = string
  default     = "20G"
  description = "Virtual disk size"
}

variable "memory" {
  type        = number
  default     = 2048
  description = "Memory in MB"
}

variable "cpus" {
  type        = number
  default     = 2
  description = "Number of CPUs"
}

# Local variables
locals {
  iso_url      = "https://releases.ubuntu.com/${var.ubuntu_version}/ubuntu-${var.ubuntu_version}-live-server-amd64.iso"
  iso_checksum = "file:https://releases.ubuntu.com/${var.ubuntu_version}/SHA256SUMS"
  build_time   = formatdate("YYYY-MM-DD", timestamp())
}

# QEMU/KVM source (for QCOW2 output)
source "qemu" "pywats" {
  iso_url           = local.iso_url
  iso_checksum      = local.iso_checksum
  output_directory  = "output-qemu"
  shutdown_command  = "sudo shutdown -P now"
  disk_size         = var.disk_size
  format            = "qcow2"
  accelerator       = "kvm"
  http_directory    = "http"
  ssh_username      = "pywats"
  ssh_password      = "pywats"
  ssh_timeout       = "30m"
  vm_name           = "${var.vm_name}.qcow2"
  net_device        = "virtio-net"
  disk_interface    = "virtio"
  memory            = var.memory
  cpus              = var.cpus
  headless          = true
  boot_wait         = "5s"
  boot_command = [
    "<esc><wait>",
    "e<wait>",
    "<down><down><down><end>",
    " autoinstall ds=nocloud-net;seedfrom=http://{{ .HTTPIP }}:{{ .HTTPPort }}/",
    "<f10>"
  ]
}

# VirtualBox source (for OVA output)
source "virtualbox-iso" "pywats" {
  iso_url           = local.iso_url
  iso_checksum      = local.iso_checksum
  output_directory  = "output-virtualbox"
  shutdown_command  = "sudo shutdown -P now"
  disk_size         = parseint(replace(var.disk_size, "G", ""), 10) * 1024
  format            = "ova"
  http_directory    = "http"
  ssh_username      = "pywats"
  ssh_password      = "pywats"
  ssh_timeout       = "30m"
  vm_name           = var.vm_name
  guest_os_type     = "Ubuntu_64"
  memory            = var.memory
  cpus              = var.cpus
  headless          = true
  boot_wait         = "5s"
  vboxmanage = [
    ["modifyvm", "{{.Name}}", "--nat-localhostreachable1", "on"]
  ]
  boot_command = [
    "<esc><wait>",
    "e<wait>",
    "<down><down><down><end>",
    " autoinstall ds=nocloud-net;seedfrom=http://{{ .HTTPIP }}:{{ .HTTPPort }}/",
    "<f10>"
  ]
}

# Build definitions
build {
  name = "pywats-appliance"

  # Choose source based on output format
  dynamic "source" {
    for_each = var.output_format == "qcow2" ? [1] : []
    labels   = ["qemu.pywats"]
    content {}
  }

  dynamic "source" {
    for_each = var.output_format == "ova" ? [1] : []
    labels   = ["virtualbox-iso.pywats"]
    content {}
  }

  # Wait for cloud-init to complete
  provisioner "shell" {
    inline = [
      "while [ ! -f /var/lib/cloud/instance/boot-finished ]; do sleep 5; done",
      "sudo cloud-init clean --logs"
    ]
  }

  # Update system
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y python3 python3-pip python3-venv curl wget"
    ]
  }

  # Install pyWATS
  provisioner "shell" {
    inline = [
      "sudo mkdir -p /opt/pywats",
      "sudo python3 -m venv /opt/pywats/.venv",
      "sudo /opt/pywats/.venv/bin/pip install --upgrade pip",
      "sudo /opt/pywats/.venv/bin/pip install pywats-api[client-headless]"
    ]
  }

  # Copy configuration files
  provisioner "file" {
    source      = "files/"
    destination = "/tmp/pywats-files/"
  }

  # Setup systemd service and configuration
  provisioner "shell" {
    inline = [
      "sudo cp /tmp/pywats-files/pywats-client.service /etc/systemd/system/",
      "sudo mkdir -p /etc/pywats",
      "sudo cp /tmp/pywats-files/config.json /etc/pywats/",
      "sudo mkdir -p /var/lib/pywats/{watch,archive,failed}",
      "sudo mkdir -p /var/log/pywats",
      "sudo useradd -r -s /sbin/nologin pywats || true",
      "sudo chown -R pywats:pywats /var/lib/pywats /var/log/pywats /etc/pywats",
      "sudo chmod 640 /etc/pywats/config.json",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable pywats-client"
    ]
  }

  # Copy first-boot setup script
  provisioner "file" {
    source      = "files/first-boot-setup.sh"
    destination = "/tmp/first-boot-setup.sh"
  }

  provisioner "shell" {
    inline = [
      "sudo cp /tmp/first-boot-setup.sh /usr/local/bin/",
      "sudo chmod +x /usr/local/bin/first-boot-setup.sh"
    ]
  }

  # Setup first-boot service
  provisioner "shell" {
    inline = [
      "sudo cp /tmp/pywats-files/pywats-firstboot.service /etc/systemd/system/",
      "sudo systemctl enable pywats-firstboot"
    ]
  }

  # Cleanup
  provisioner "shell" {
    inline = [
      "sudo apt-get clean",
      "sudo rm -rf /tmp/pywats-files",
      "sudo rm -rf /var/lib/apt/lists/*",
      "sudo truncate -s 0 /etc/machine-id",
      "sudo rm -f /var/lib/dbus/machine-id",
      "sudo sync"
    ]
  }

  # Post-processors for format conversion
  post-processor "checksum" {
    checksum_types = ["sha256"]
    output         = "output/${var.vm_name}-${var.pywats_version}.{{.ChecksumType}}"
  }

  post-processor "manifest" {
    output     = "output/${var.vm_name}-${var.pywats_version}-manifest.json"
    strip_path = true
    custom_data = {
      pywats_version = var.pywats_version
      build_date     = local.build_time
      ubuntu_version = var.ubuntu_version
    }
  }
}
