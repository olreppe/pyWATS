# VS Code F5 Debugging Setup Guide

## Issue: "Select Startup Item" when pressing F5

This guide will help you fix the F5 debugging issue in VS Code.

## Step-by-Step Fix

### 1. **Reload VS Code Window**
   - Press `Ctrl+Shift+P`
   - Type "Developer: Reload Window"
   - Press Enter

### 2. **Select Python Interpreter**
   - Press `Ctrl+Shift+P`
   - Type "Python: Select Interpreter"
   - Choose: `./venv/Scripts/python.exe` 
   - The bottom-left should show: `Python 3.13.1 64-bit (venv: venv)`

### 3. **Go to Run and Debug Panel**
   - Press `Ctrl+Shift+D` (or click the Run and Debug icon)
   - You should see a dropdown at the top

### 4. **Select Launch Configuration**
   - In the dropdown, select **"Python: Main Script"**
   - This will be your default F5 configuration

### 5. **Test F5 Debugging**
   - Open `main.py` 
   - Press **F5** - it should start debugging
   - Or try `debug_test.py` for a simple test

## Alternative Launch Configurations

Available in the dropdown:
- **Python: Main Script** - Runs main.py (recommended default)
- **Python: Debug Test** - Runs debug_test.py (simple test)
- **Python: Current File** - Runs whatever file is currently open
- **Python: MES/TDM Example** - Runs the MES/TDM examples
- **Python: Test MES/TDM** - Runs MES/TDM tests

## If F5 Still Doesn't Work

### Check Python Extension
1. Go to Extensions (`Ctrl+Shift+X`)
2. Search for "Python"
3. Ensure "Python" by Microsoft is installed and enabled
4. Also ensure "Python Debugger" is installed

### Verify Configuration Files
- `.vscode/launch.json` - Contains debug configurations
- `.vscode/settings.json` - Contains workspace settings
- `pyWATS.code-workspace` - Workspace file (optional)

### Manual Debug Start
If F5 doesn't work:
1. Go to Run and Debug panel (`Ctrl+Shift+D`)
2. Select "Python: Main Script" from dropdown
3. Click the green play button (??)

### Check Output for Errors
1. View ? Output (`Ctrl+Shift+U`)
2. Select "Python" from the dropdown
3. Look for any error messages

## Testing Your Setup

### Quick Test with debug_test.py
1. Open `debug_test.py`
2. Set a breakpoint on line 45 (click left of line number)
3. Press F5 or select "Python: Debug Test"
4. The debugger should stop at your breakpoint

### Debugging Features to Test
- **Breakpoints** - Click left of line numbers
- **Step Over** - F10
- **Step Into** - F11  
- **Variables Panel** - Shows variable values
- **Debug Console** - Interactive Python console

## Expected Behavior

When F5 is working correctly:
1. VS Code opens the integrated terminal
2. Activates the virtual environment
3. Starts the Python debugger
4. Runs your script with debugging capabilities
5. Stops at any breakpoints you've set

## Common Issues

### "Select Startup Item" Error
- **Cause**: No default launch configuration selected
- **Fix**: Select "Python: Main Script" from the Run and Debug dropdown

### "Python Interpreter Not Found"
- **Cause**: VS Code can't find the Python interpreter
- **Fix**: Use `Ctrl+Shift+P` ? "Python: Select Interpreter"

### "debugpy not found"
- **Cause**: Missing debugpy package
- **Fix**: Already installed - `./venv/Scripts/python.exe -m pip install debugpy`

## Files Updated

The following files have been configured for F5 debugging:
- `.vscode/launch.json` - Debug configurations
- `.vscode/settings.json` - Python interpreter settings
- `pyWATS.code-workspace` - Workspace configuration
- `debug_test.py` - Simple debugging test file

## Success Indicator

F5 is working when you see:
- ? The Run and Debug panel shows your configurations
- ? F5 starts the debugger without errors
- ? Terminal shows: "Python 3.13.1 64-bit (venv: venv)"
- ? Your script runs with debugging capabilities