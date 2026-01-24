"""
Linux/macOS Service Installation for pyWATS Client

Provides tools for installing pyWATS Client as a system service:
- Linux: systemd service
- macOS: launchd daemon

Service will auto-start on system boot.
"""

import sys
import os
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class LinuxServiceInstaller:
    """
    Installs pyWATS Client as a systemd service on Linux.
    
    Works with Ubuntu, Debian, RHEL, CentOS, Fedora, and other systemd-based distributions.
    """
    
    SERVICE_NAME = "pywats-service"
    SYSTEMD_DIR = Path("/etc/systemd/system")
    
    @staticmethod
    def is_root() -> bool:
        """Check if running as root"""
        return os.geteuid() == 0
    
    @staticmethod
    def has_systemd() -> bool:
        """Check if systemd is available"""
        return Path("/run/systemd/system").exists()
    
    @classmethod
    def _get_service_unit_file(cls, instance_id: str = "default") -> Path:
        """Get path to systemd unit file"""
        if instance_id == "default":
            return cls.SYSTEMD_DIR / f"{cls.SERVICE_NAME}.service"
        else:
            return cls.SYSTEMD_DIR / f"{cls.SERVICE_NAME}@{instance_id}.service"
    
    @classmethod
    def _create_systemd_unit(
        cls,
        instance_id: str = "default",
        config_path: Optional[str] = None,
        python_exe: Optional[str] = None,
        user: Optional[str] = None
    ) -> str:
        """
        Create systemd unit file content.
        
        Args:
            instance_id: Instance ID for the service
            config_path: Path to config file
            python_exe: Path to Python executable
            user: User to run service as (defaults to current user)
            
        Returns:
            Unit file content as string
        """
        if not python_exe:
            python_exe = sys.executable
        
        if not user:
            import pwd
            user = pwd.getpwuid(os.getuid()).pw_name
        
        # Build service command
        exec_start = f"{python_exe} -m pywats_client service"
        
        if instance_id != "default":
            exec_start += f" --instance-id {instance_id}"
        
        if config_path:
            exec_start += f' --config "{config_path}"'
        
        # Data directory
        if user == "root":
            working_dir = "/var/lib/pywats"
            state_dir = "/var/lib/pywats"
        else:
            home = Path.home()
            working_dir = str(home / ".config" / "pywats_client")
            state_dir = working_dir
        
        # Service description
        description = "pyWATS Client Service"
        if instance_id != "default":
            description = f"pyWATS Client Service ({instance_id})"
        
        unit_content = f"""[Unit]
Description={description}
Documentation=https://github.com/olreppe/pyWATS
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User={user}
Group={user}
WorkingDirectory={working_dir}
ExecStart={exec_start}
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths={state_dir}

# Environment
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
"""
        return unit_content
    
    @classmethod
    def install(
        cls,
        instance_id: str = "default",
        config_path: Optional[str] = None,
        python_exe: Optional[str] = None,
        user: Optional[str] = None
    ) -> bool:
        """
        Install systemd service.
        
        Args:
            instance_id: Instance ID for the service
            config_path: Path to config file
            python_exe: Path to Python executable
            user: User to run service as
            
        Returns:
            True if installation successful
        """
        if not cls.is_root():
            print("ERROR: Root privileges required (use sudo)")
            return False
        
        if not cls.has_systemd():
            print("ERROR: systemd not found. This system may not use systemd.")
            print("Please install pyWATS manually or use your system's init system.")
            return False
        
        # Create unit file
        unit_file = cls._get_service_unit_file(instance_id)
        unit_content = cls._create_systemd_unit(instance_id, config_path, python_exe, user)
        
        try:
            # Write unit file
            print(f"Creating systemd unit file: {unit_file}")
            unit_file.write_text(unit_content)
            unit_file.chmod(0o644)
            
            # Reload systemd
            print("Reloading systemd daemon...")
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            
            # Enable service
            service_name = unit_file.stem
            print(f"Enabling service '{service_name}'...")
            subprocess.run(["systemctl", "enable", service_name], check=True)
            
            print(f"✓ Service '{service_name}' installed successfully")
            print(f"  Unit file: {unit_file}")
            print(f"  Instance ID: {instance_id}")
            print(f"  User: {user or 'current user'}")
            print(f"\nTo start the service:")
            print(f"  sudo systemctl start {service_name}")
            print(f"\nTo view logs:")
            print(f"  sudo journalctl -u {service_name} -f")
            
            return True
        
        except Exception as e:
            print(f"ERROR: Failed to install service: {e}")
            return False
    
    @classmethod
    def uninstall(cls, instance_id: str = "default") -> bool:
        """
        Uninstall systemd service.
        
        Args:
            instance_id: Instance ID of the service
            
        Returns:
            True if uninstallation successful
        """
        if not cls.is_root():
            print("ERROR: Root privileges required (use sudo)")
            return False
        
        unit_file = cls._get_service_unit_file(instance_id)
        service_name = unit_file.stem
        
        try:
            # Stop service
            print(f"Stopping service '{service_name}'...")
            subprocess.run(["systemctl", "stop", service_name], check=False)
            
            # Disable service
            print(f"Disabling service '{service_name}'...")
            subprocess.run(["systemctl", "disable", service_name], check=False)
            
            # Remove unit file
            if unit_file.exists():
                print(f"Removing unit file: {unit_file}")
                unit_file.unlink()
            
            # Reload systemd
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "reset-failed"], check=False)
            
            print(f"✓ Service '{service_name}' removed successfully")
            return True
        
        except Exception as e:
            print(f"ERROR: Failed to remove service: {e}")
            return False


class MacOSServiceInstaller:
    """
    Installs pyWATS Client as a launchd daemon on macOS.
    
    Creates a Launch Daemon (runs at boot) or Launch Agent (runs at login).
    """
    
    SERVICE_LABEL = "com.virinco.pywats.service"
    LAUNCH_DAEMONS_DIR = Path("/Library/LaunchDaemons")
    LAUNCH_AGENTS_DIR = Path("/Library/LaunchAgents")
    
    @staticmethod
    def is_root() -> bool:
        """Check if running as root"""
        return os.geteuid() == 0
    
    @classmethod
    def _get_plist_path(cls, instance_id: str = "default", user_agent: bool = False) -> Path:
        """Get path to launchd plist file"""
        base_dir = cls.LAUNCH_AGENTS_DIR if user_agent else cls.LAUNCH_DAEMONS_DIR
        
        if instance_id == "default":
            filename = f"{cls.SERVICE_LABEL}.plist"
        else:
            filename = f"{cls.SERVICE_LABEL}.{instance_id}.plist"
        
        return base_dir / filename
    
    @classmethod
    def _create_plist_content(
        cls,
        instance_id: str = "default",
        config_path: Optional[str] = None,
        python_exe: Optional[str] = None,
        user_agent: bool = False
    ) -> str:
        """
        Create launchd plist file content.
        
        Args:
            instance_id: Instance ID for the service
            config_path: Path to config file
            python_exe: Path to Python executable
            user_agent: If True, create Launch Agent instead of Daemon
            
        Returns:
            Plist file content as string
        """
        if not python_exe:
            python_exe = sys.executable
        
        # Build command arguments
        args = [python_exe, "-m", "pywats_client", "service"]
        
        if instance_id != "default":
            args.extend(["--instance-id", instance_id])
        
        if config_path:
            args.extend(["--config", config_path])
        
        # Label
        label = cls.SERVICE_LABEL
        if instance_id != "default":
            label = f"{cls.SERVICE_LABEL}.{instance_id}"
        
        # Working directory and log paths
        if user_agent:
            home = Path.home()
            working_dir = str(home / ".config" / "pywats_client")
            log_dir = str(home / "Library" / "Logs" / "pyWATS")
        else:
            working_dir = "/var/lib/pywats"
            log_dir = "/var/log/pywats"
        
        # Create log directory
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        
        stdout_log = f"{log_dir}/pywats-service.log"
        stderr_log = f"{log_dir}/pywats-service-error.log"
        
        # Format arguments for plist
        args_xml = "\n".join(f"        <string>{arg}</string>" for arg in args)
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{label}</string>
    
    <key>ProgramArguments</key>
    <array>
{args_xml}
    </array>
    
    <key>WorkingDirectory</key>
    <string>{working_dir}</string>
    
    <key>StandardOutPath</key>
    <string>{stdout_log}</string>
    
    <key>StandardErrorPath</key>
    <string>{stderr_log}</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
    </dict>
</dict>
</plist>
"""
        return plist_content
    
    @classmethod
    def install(
        cls,
        instance_id: str = "default",
        config_path: Optional[str] = None,
        python_exe: Optional[str] = None,
        user_agent: bool = False
    ) -> bool:
        """
        Install launchd service.
        
        Args:
            instance_id: Instance ID for the service
            config_path: Path to config file
            python_exe: Path to Python executable
            user_agent: If True, install as Launch Agent (user-level)
            
        Returns:
            True if installation successful
        """
        if not user_agent and not cls.is_root():
            print("ERROR: Root privileges required for system daemon (use sudo)")
            print("Or use --user-agent to install as user-level Launch Agent")
            return False
        
        # Create plist file
        plist_path = cls._get_plist_path(instance_id, user_agent)
        plist_content = cls._create_plist_content(instance_id, config_path, python_exe, user_agent)
        
        try:
            # Write plist file
            print(f"Creating launchd plist: {plist_path}")
            plist_path.write_text(plist_content)
            plist_path.chmod(0o644)
            
            # Load service
            label = cls.SERVICE_LABEL
            if instance_id != "default":
                label = f"{cls.SERVICE_LABEL}.{instance_id}"
            
            print(f"Loading service '{label}'...")
            subprocess.run(["launchctl", "load", str(plist_path)], check=True)
            
            service_type = "Launch Agent" if user_agent else "Launch Daemon"
            print(f"✓ {service_type} '{label}' installed successfully")
            print(f"  Plist: {plist_path}")
            print(f"  Instance ID: {instance_id}")
            print(f"\nTo start the service:")
            print(f"  sudo launchctl start {label}")
            print(f"\nTo view logs:")
            if user_agent:
                print(f"  tail -f ~/Library/Logs/pyWATS/pywats-service.log")
            else:
                print(f"  sudo tail -f /var/log/pywats/pywats-service.log")
            
            return True
        
        except Exception as e:
            print(f"ERROR: Failed to install service: {e}")
            return False
    
    @classmethod
    def uninstall(cls, instance_id: str = "default", user_agent: bool = False) -> bool:
        """
        Uninstall launchd service.
        
        Args:
            instance_id: Instance ID of the service
            user_agent: If True, uninstall Launch Agent
            
        Returns:
            True if uninstallation successful
        """
        if not user_agent and not cls.is_root():
            print("ERROR: Root privileges required (use sudo)")
            return False
        
        plist_path = cls._get_plist_path(instance_id, user_agent)
        label = cls.SERVICE_LABEL
        if instance_id != "default":
            label = f"{cls.SERVICE_LABEL}.{instance_id}"
        
        try:
            # Unload service
            print(f"Unloading service '{label}'...")
            subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
            
            # Remove plist file
            if plist_path.exists():
                print(f"Removing plist: {plist_path}")
                plist_path.unlink()
            
            print(f"✓ Service '{label}' removed successfully")
            return True
        
        except Exception as e:
            print(f"ERROR: Failed to remove service: {e}")
            return False
