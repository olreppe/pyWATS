# GitHub to GitHub Enterprise Migration Script
# Migrates pyWATS repository from github.com to wats.ghe.com
# Creates shallow clone from first PyPI release (v0.1.0b1)
#
# Usage: .\migrate_to_ghe.ps1

param(
    [string]$SourceRepo = "https://github.com/olreppe/pyWATS.git",
    [string]$TargetRepo = "https://wats.ghe.com/WATS/pyWATS.git",
    [string]$FirstReleaseCommit = "8687e63a3117a7b0d27fa59000e7dd62cd77d26a",  # v0.1.0b1
    [string]$TempDir = "$env:TEMP\pywats-migration"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "pyWATS GitHub Enterprise Migration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Source:      $SourceRepo" -ForegroundColor Yellow
Write-Host "Target:      $TargetRepo" -ForegroundColor Yellow
Write-Host "From commit: $FirstReleaseCommit (v0.1.0b1)" -ForegroundColor Yellow
Write-Host ""

# Confirm with user
$confirm = Read-Host "Continue with migration? (y/N)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "Migration cancelled." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 1: Cleaning up temp directory..." -ForegroundColor Green
if (Test-Path $TempDir) {
    Remove-Item -Path $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir | Out-Null
Set-Location $TempDir

Write-Host "Step 2: Creating shallow clone from first release..." -ForegroundColor Green
Write-Host "  Cloning with shallow depth from commit $FirstReleaseCommit" -ForegroundColor Gray
git clone --depth 1000 $SourceRepo pyWATS-temp
Set-Location pyWATS-temp

# Get all commits since first release
Write-Host "Step 3: Fetching full history from first release..." -ForegroundColor Green
git fetch --shallow-since="2025-12-14" origin

Write-Host "Step 4: Fetching all tags..." -ForegroundColor Green
git fetch --tags origin

Write-Host "Step 5: Adding GitHub Enterprise remote..." -ForegroundColor Green
git remote add ghe $TargetRepo
git remote -v

Write-Host ""
Write-Host "Step 6: Ready to push to GitHub Enterprise" -ForegroundColor Green
Write-Host "  This will push:" -ForegroundColor Yellow
Write-Host "    - All branches" -ForegroundColor Yellow
Write-Host "    - All tags" -ForegroundColor Yellow
Write-Host "    - History from $FirstReleaseCommit onwards" -ForegroundColor Yellow
Write-Host ""

$pushConfirm = Read-Host "Push to $TargetRepo ? (y/N)"
if ($pushConfirm -ne 'y' -and $pushConfirm -ne 'Y') {
    Write-Host "Push cancelled. Temp clone available at: $TempDir" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Step 7: Pushing to GitHub Enterprise..." -ForegroundColor Green
Write-Host "  Pushing all branches..." -ForegroundColor Gray
git push ghe --all

Write-Host "  Pushing all tags..." -ForegroundColor Gray
git push ghe --tags

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Migration Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository successfully migrated to:" -ForegroundColor Green
Write-Host "  $TargetRepo" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Verify repository at: https://wats.ghe.com/WATS/pyWATS" -ForegroundColor White
Write-Host "  2. Set repository description and settings on GHE" -ForegroundColor White
Write-Host "  3. Add sync remote to your working copy (see sync_to_ghe.ps1)" -ForegroundColor White
Write-Host ""
Write-Host "Cleanup:" -ForegroundColor Cyan
Write-Host "  Temp directory: $TempDir" -ForegroundColor Gray
Write-Host "  Run: Remove-Item '$TempDir' -Recurse -Force" -ForegroundColor Gray
Write-Host ""
