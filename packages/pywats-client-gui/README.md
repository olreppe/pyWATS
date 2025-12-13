# pyWATS Client GUI

Desktop GUI application for pyWATS - Qt-based client for Windows, macOS, and Linux desktop environments.

## Features

- **Modern Qt Interface**: Clean, professional PySide6-based UI
- **Connection Management**: Visual connection status and configuration
- **Converter Management**: Browse, configure, and test converters
- **Queue Visualization**: Monitor report queue in real-time
- **Log Viewer**: Built-in log viewing and filtering
- **Multiple Instances**: Run multiple client instances simultaneously
- **Tab Customization**: Show/hide tabs based on your workflow
- **Software Management**: Track and manage software versions (optional)
- **Debug Mode**: Integrated debug logging for troubleshooting

## Installation

```bash
pip install pywats-client-gui
```

### System Requirements

- Python >= 3.8
- Windows 10+, macOS 10.15+, or Linux with X11/Wayland
- PySide6 (Qt 6.4+) - installed automatically
- ~200MB disk space for Qt libraries

## Quick Start

### Launch GUI

```bash
# Run the GUI
pywats-client-gui

# Or use Python module
python -m pywats_client
```

### First Time Setup

1. **Connection Settings**
   - Enter your WATS server URL
   - Provide API token (base64-encoded credentials)
   - Test connection

2. **Configure Converters**
   - Set converter directory path
   - GUI will auto-discover converters
   - Test converters on sample files

3. **Set Watch Paths**
   - Add directories to monitor for test data
   - Enable auto-processing

4. **Start Services**
   - Click "Start" to begin processing
   - Monitor status in real-time

## User Interface

### Main Window Tabs

#### Connection Tab
- Configure WATS server connection
- Test connection status
- View server information
- Manage authentication

#### Converter Tab
- List all available converters
- View converter details
- Test converter on files
- Add/remove converter paths
- Converter statistics

#### Queue Tab
- View pending reports
- Monitor processing status
- Retry failed reports
- Clear completed items
- Export queue data

#### Logs Tab
- View application logs
- Filter by level (DEBUG, INFO, WARNING, ERROR)
- Search log entries
- Export logs
- Enable debug mode

#### Software Tab (Optional)
- Manage software versions
- Track software deployment
- View software history

#### SN Handler Tab (Optional)
- Serial number management
- Unit registration
- Serial number lookup

### Status Bar

Shows real-time status:
- Connection status (green = connected)
- Queue status (pending/processing/failed)
- Converter count
- Service status (running/stopped)

## Configuration

### GUI Settings

Access via **Settings → Preferences**:

```json
{
  "gui": {
    "tabs": {
      "show_software": false,
      "show_sn_handler": false,
      "show_logs": true,
      "show_converters": true,
      "show_queue": true
    },
    "theme": "default",
    "window_size": [1200, 800],
    "log_level": "INFO"
  }
}
```

### Tab Customization

Hide/show tabs based on your needs:

```python
# In configuration
{
  "gui": {
    "tabs": {
      "show_software": false,      # Hide software tab
      "show_sn_handler": false,    # Hide SN handler tab
      "show_logs": true,           # Show logs tab
      "show_converters": true,     # Show converters tab
      "show_queue": true           # Show queue tab
    }
  }
}
```

### Debug Mode

Enable detailed logging:

1. **Via GUI**: Settings → Enable Debug Mode
2. **Via Code**:
   ```python
   from pywats import enable_debug_logging
   enable_debug_logging()
   ```

Debug mode shows:
- All API requests/responses
- Converter operations
- Queue processing details
- Service lifecycle events

## Multiple Instances

Run multiple client instances for different stations:

```bash
# Instance 1
pywats-client-gui --instance-name "Station 1" --config station1.json

# Instance 2
pywats-client-gui --instance-name "Station 2" --config station2.json
```

Each instance:
- Has separate configuration
- Independent queue
- Own converter set
- Isolated logs

## Advanced Features

### Custom Converters

Converters are auto-discovered from the converter directory:

```python
# converters/my_converter.py
from pywats_client.converters import BaseConverter
from pywats.models import UUTReport

class MyGUIConverter(BaseConverter):
    name = "My Custom Converter"
    description = "Converts .test files"
    
    def can_convert(self, file_path):
        return file_path.suffix == '.test'
    
    def convert(self, file_path):
        # Your conversion logic
        report = UUTReport(...)
        return report
```

The GUI will:
- Automatically detect the converter
- Show it in the converter list
- Allow testing it on files
- Display conversion results

### Keyboard Shortcuts

- `Ctrl+R`: Refresh current view
- `Ctrl+T`: Test connection
- `Ctrl+S`: Start/Stop services
- `Ctrl+L`: Focus log search
- `Ctrl+Q`: Quit application
- `F5`: Refresh data
- `F12`: Toggle debug mode

### Export Data

Export various data formats:

- **Queue**: Export to CSV/JSON
- **Logs**: Export filtered logs
- **Reports**: Export report summaries
- **Statistics**: Export processing statistics

## Troubleshooting

### GUI Won't Start

Check PySide6 installation:
```bash
python -c "import PySide6; print(PySide6.__version__)"
```

Reinstall if needed:
```bash
pip uninstall PySide6
pip install PySide6
```

### Display Issues on Linux

Install Qt dependencies:
```bash
# Ubuntu/Debian
sudo apt install libxcb-xinerama0 libxcb-cursor0

# Fedora
sudo dnf install qt6-qtbase-gui
```

### High DPI Displays

Qt auto-scales, but you can override:
```bash
export QT_AUTO_SCREEN_SCALE_FACTOR=1
pywats-client-gui
```

### Dark Mode

GUI respects system theme. Force dark mode:
```bash
export QT_QPA_PLATFORMTHEME=darkmode
pywats-client-gui
```

## Platform-Specific Notes

### Windows

- Install via pip normally
- Creates Start Menu shortcut
- Runs in system tray
- Auto-start support via Task Scheduler

### macOS

- Install via pip normally
- Creates .app bundle
- Dock integration
- Native menu bar
- Dark mode support

### Linux

- Requires X11 or Wayland
- Desktop entry created automatically
- System tray integration (if supported)
- Follows desktop theme

## Building Standalone Executable

Create standalone executable with PyInstaller:

```bash
pip install pyinstaller

# Windows
pyinstaller --name pyWATS-Client \
  --windowed \
  --onefile \
  --icon icon.ico \
  -m pywats_client

# macOS
pyinstaller --name pyWATS-Client \
  --windowed \
  --onefile \
  --icon icon.icns \
  -m pywats_client

# Linux
pyinstaller --name pywats-client \
  --windowed \
  --onefile \
  -m pywats_client
```

## Requirements

- Python >= 3.8
- pywats >= 2.0.0
- pywats-client-service >= 2.0.0
- PySide6 >= 6.4.0

## Related Packages

- **pywats**: Core API library
- **pywats-client-service**: Client service framework (included)
- **pywats-client-headless**: CLI and HTTP API (separate)

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please visit:
- GitHub: https://github.com/olreppe/pyWATS
- Documentation: [GUI Configuration Guide](https://github.com/olreppe/pyWATS/blob/main/src/pywats_client/GUI_CONFIGURATION.md)
- Issues: https://github.com/olreppe/pyWATS/issues
