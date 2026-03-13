<#
.SYNOPSIS
    Sets up Client A as a persistent live installation on this machine.

.DESCRIPTION
    Registers a Windows Task Scheduler task that launches the pyWATS Client A
    GUI at user logon. This runs the current workspace code directly from the
    .venv, giving zero-overhead continuous testing.

    What it does:
    1. Creates a scheduled task "pyWATS Client A" that runs at user logon
    2. Points to the workspace .venv Python to run run_client_a.py
    3. Tray icon stays visible even when the window is minimized

    To remove:
        Unregister-ScheduledTask -TaskName "pyWATS Client A" -Confirm:$false

.EXAMPLE
    .\scripts\setup_client_a_autostart.ps1
#>

$ErrorActionPreference = "Stop"

# Resolve paths
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $WorkspaceRoot ".venv\Scripts\pythonw.exe"
$LauncherScript = Join-Path $WorkspaceRoot "run_client_a.py"
$TaskName = "pyWATS Client A"

Write-Host "=== pyWATS Client A Autostart Setup ===" -ForegroundColor Cyan
Write-Host ""

# Validate environment
if (-not (Test-Path $VenvPython)) {
    # Fallback to python.exe if pythonw.exe doesn't exist
    $VenvPython = Join-Path $WorkspaceRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $VenvPython)) {
        Write-Host "ERROR: .venv Python not found at $VenvPython" -ForegroundColor Red
        Write-Host "Run: python -m venv .venv && .venv\Scripts\pip install -e ." -ForegroundColor Yellow
        exit 1
    }
}

if (-not (Test-Path $LauncherScript)) {
    Write-Host "ERROR: run_client_a.py not found at $LauncherScript" -ForegroundColor Red
    exit 1
}

Write-Host "Workspace:  $WorkspaceRoot"
Write-Host "Python:     $VenvPython"
Write-Host "Launcher:   $LauncherScript"
Write-Host ""

# Check for existing task
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Task '$TaskName' already exists. Replacing..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the scheduled task
$Action = New-ScheduledTaskAction `
    -Execute $VenvPython `
    -Argument "`"$LauncherScript`"" `
    -WorkingDirectory $WorkspaceRoot

$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "pyWATS Client A - Live development instance running workspace code" | Out-Null

Write-Host ""
Write-Host "SUCCESS: Scheduled task '$TaskName' created!" -ForegroundColor Green
Write-Host ""
Write-Host "The client will start automatically at next logon." -ForegroundColor Cyan
Write-Host "To start it now: Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Cyan
Write-Host "To remove:       Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false" -ForegroundColor Gray
Write-Host ""

# Ask if user wants to start now
$startNow = Read-Host "Start Client A now? (Y/n)"
if ($startNow -ne 'n' -and $startNow -ne 'N') {
    Write-Host "Starting Client A..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 2
    
    $taskInfo = Get-ScheduledTaskInfo -TaskName $TaskName
    if ($taskInfo.LastTaskResult -eq 0 -or $taskInfo.LastTaskResult -eq 267009) {
        Write-Host "Client A is running!" -ForegroundColor Green
    } else {
        Write-Host "Task started (check tray icon in a few seconds)" -ForegroundColor Yellow
    }
}
