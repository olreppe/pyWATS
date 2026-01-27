# Setup GitHub Enterprise Sync for Existing Working Copy
# Adds GHE remote to your current working directory
#
# Usage: .\setup_ghe_sync.ps1

param(
    [string]$GHERemoteUrl = "https://wats.ghe.com/WATS/pyWATS.git",
    [string]$RemoteName = "ghe"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup GitHub Enterprise Sync" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify we're in a git repo
if (-not (Test-Path ".git")) {
    Write-Host "Error: Not in a git repository root directory" -ForegroundColor Red
    Write-Host "Please run this script from: C:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS" -ForegroundColor Yellow
    exit 1
}

# Check if remote already exists
$existingRemote = git remote get-url $RemoteName 2>$null
if ($existingRemote) {
    Write-Host "Remote '$RemoteName' already exists: $existingRemote" -ForegroundColor Yellow
    $replace = Read-Host "Replace with $GHERemoteUrl ? (y/N)"
    if ($replace -eq 'y' -or $replace -eq 'Y') {
        git remote remove $RemoteName
        Write-Host "Removed existing remote" -ForegroundColor Green
    } else {
        Write-Host "Keeping existing remote. Exiting." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Adding GitHub Enterprise remote..." -ForegroundColor Green
git remote add $RemoteName $GHERemoteUrl

Write-Host ""
Write-Host "Current remotes:" -ForegroundColor Cyan
git remote -v

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now sync to GitHub Enterprise using:" -ForegroundColor Cyan
Write-Host "  .\scripts\sync_to_ghe.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Or manually:" -ForegroundColor Cyan
Write-Host "  git push $RemoteName main" -ForegroundColor Yellow
Write-Host "  git push $RemoteName --tags" -ForegroundColor Yellow
Write-Host ""
