# Sync Changes to GitHub Enterprise
# Pushes current branch and tags to GHE
#
# Usage: .\sync_to_ghe.ps1 [-Branch main] [-PushTags]

param(
    [string]$Branch = "",  # Empty = current branch
    [switch]$PushTags = $false,
    [switch]$All = $false,
    [string]$RemoteName = "ghe"
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sync to GitHub Enterprise" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify we're in a git repo
if (-not (Test-Path ".git")) {
    Write-Host "Error: Not in a git repository" -ForegroundColor Red
    exit 1
}

# Verify GHE remote exists
$gheRemote = git remote get-url $RemoteName 2>$null
if (-not $gheRemote) {
    Write-Host "Error: Remote '$RemoteName' not configured" -ForegroundColor Red
    Write-Host "Run: .\scripts\setup_ghe_sync.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Target: $gheRemote" -ForegroundColor Yellow
Write-Host ""

# Get current branch if not specified
if ([string]::IsNullOrEmpty($Branch)) {
    $Branch = git branch --show-current
    if ([string]::IsNullOrEmpty($Branch)) {
        Write-Host "Error: Not on a branch (detached HEAD?)" -ForegroundColor Red
        exit 1
    }
}

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host "Warning: You have uncommitted changes:" -ForegroundColor Yellow
    Write-Host $status -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne 'y' -and $continue -ne 'Y') {
        Write-Host "Sync cancelled." -ForegroundColor Red
        exit 1
    }
    Write-Host ""
}

# Show what will be pushed
Write-Host "Will push:" -ForegroundColor Cyan
if ($All) {
    Write-Host "  - All branches" -ForegroundColor Yellow
} else {
    Write-Host "  - Branch: $Branch" -ForegroundColor Yellow
}
if ($PushTags) {
    Write-Host "  - All tags" -ForegroundColor Yellow
}
Write-Host ""

$confirm = Read-Host "Continue? (y/N)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "Sync cancelled." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Syncing to GitHub Enterprise..." -ForegroundColor Green

try {
    if ($All) {
        Write-Host "  Pushing all branches..." -ForegroundColor Gray
        git push $RemoteName --all
    } else {
        Write-Host "  Pushing branch $Branch..." -ForegroundColor Gray
        git push $RemoteName $Branch
    }
    
    if ($PushTags) {
        Write-Host "  Pushing tags..." -ForegroundColor Gray
        git push $RemoteName --tags
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Sync Complete!" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Changes pushed to: $gheRemote" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "Error during sync:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  - Authentication required (check credentials)" -ForegroundColor Gray
    Write-Host "  - Branch diverged (pull from GHE first)" -ForegroundColor Gray
    Write-Host "  - Network connectivity" -ForegroundColor Gray
    exit 1
}
