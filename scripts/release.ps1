<#
.SYNOPSIS
    Release automation script for pyWATS.
    
.DESCRIPTION
    This script handles version bumping and creates protected release branches
    that remain untouched for rollback purposes.
    
    Workflow:
    1. Validates current branch is 'main'
    2. Bumps version in pyproject.toml files
    3. Creates a release branch (release/vX.Y.Z)
    4. Tags the release
    5. Commits version bump to main
    6. Pushes both branches and tags
    
.PARAMETER BumpType
    Type of version bump: major, minor, or patch (default: patch)
    
.PARAMETER Package
    Which package to bump: 'api', 'agent', or 'all' (default: all)
    
.PARAMETER DryRun
    Preview what would happen without making changes
    
.EXAMPLE
    .\release.ps1 -BumpType patch
    # Bumps 0.1.0 -> 0.1.1
    
.EXAMPLE
    .\release.ps1 -BumpType minor -DryRun
    # Preview minor version bump (0.1.0 -> 0.2.0)
    
.EXAMPLE
    .\release.ps1 -BumpType major -Package agent
    # Major bump for agent package only
#>

param(
    [ValidateSet("major", "minor", "patch")]
    [string]$BumpType = "patch",
    
    [ValidateSet("api", "agent", "all")]
    [string]$Package = "all",
    
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# ============================================================================
# Configuration
# ============================================================================

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path "$RepoRoot\.git")) {
    $RepoRoot = Split-Path -Parent $PSScriptRoot
}

$PackageConfigs = @{
    "api" = @{
        PyprojectPath = "$RepoRoot\pyproject.toml"
        Name = "pywats-api"
    }
    "agent" = @{
        PyprojectPath = "$RepoRoot\packages\pywats-agent\pyproject.toml"
        Name = "pywats-agent"
    }
}

# ============================================================================
# Helper Functions
# ============================================================================

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "[>] " -ForegroundColor Cyan -NoNewline
    Write-Host $Message -ForegroundColor White
}

function Write-Success {
    param([string]$Message)
    Write-Host "  [OK] " -ForegroundColor Green -NoNewline
    Write-Host $Message -ForegroundColor Gray
}

function Write-Info {
    param([string]$Message)
    Write-Host "  [i] " -ForegroundColor Blue -NoNewline
    Write-Host $Message -ForegroundColor Gray
}

function Write-Warn {
    param([string]$Message)
    Write-Host "  [!] " -ForegroundColor Yellow -NoNewline
    Write-Host $Message -ForegroundColor Gray
}

function Write-DryRunMsg {
    param([string]$Message)
    Write-Host "  [DRY RUN] " -ForegroundColor Magenta -NoNewline
    Write-Host $Message -ForegroundColor Gray
}

function Get-CurrentVersion {
    param([string]$PyprojectPath)
    
    $content = Get-Content $PyprojectPath -Raw
    if ($content -match 'version\s*=\s*"([^"]+)"') {
        return $Matches[1]
    }
    throw "Could not find version in $PyprojectPath"
}

function Get-BumpedVersion {
    param(
        [string]$CurrentVersion,
        [string]$BumpType
    )
    
    # Handle pre-release versions (e.g., 0.1.0b5 -> 0.1.0)
    $cleanVersion = $CurrentVersion -replace '[a-zA-Z]+\d*$', ''
    $parts = $cleanVersion.Split('.')
    
    if ($parts.Count -lt 3) {
        $parts = @($parts[0], $parts[1], "0")
    }
    
    $major = [int]$parts[0]
    $minor = [int]$parts[1]
    $patch = [int]$parts[2]
    
    switch ($BumpType) {
        "major" { $major++; $minor = 0; $patch = 0 }
        "minor" { $minor++; $patch = 0 }
        "patch" { $patch++ }
    }
    
    return "$major.$minor.$patch"
}

function Set-Version {
    param(
        [string]$PyprojectPath,
        [string]$NewVersion
    )
    
    $content = Get-Content $PyprojectPath -Raw
    $newContent = $content -replace 'version\s*=\s*"[^"]+"', "version = `"$NewVersion`""
    
    if (-not $DryRun) {
        Set-Content -Path $PyprojectPath -Value $newContent -NoNewline
    }
}

function Get-CurrentBranch {
    return (git rev-parse --abbrev-ref HEAD).Trim()
}

function Test-CleanWorkingTree {
    $status = git status --porcelain
    return [string]::IsNullOrWhiteSpace($status)
}

# ============================================================================
# Main Release Flow
# ============================================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "              pyWATS Release Automation                        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host ""
    Write-Host "  DRY RUN MODE - No changes will be made" -ForegroundColor Magenta
}

# Step 1: Validate environment
Write-Step "Validating environment"

Push-Location $RepoRoot
try {
    $currentBranch = Get-CurrentBranch
    if ($currentBranch -ne "main") {
        throw "Must be on 'main' branch to release. Currently on: $currentBranch"
    }
    Write-Success "On main branch"
    
    if (-not (Test-CleanWorkingTree)) {
        throw "Working tree has uncommitted changes. Please commit or stash first."
    }
    Write-Success "Working tree is clean"
    
    # Pull latest
    if (-not $DryRun) {
        Write-Info "Pulling latest from origin..."
        git pull origin main --quiet
    }
    Write-Success "Up to date with origin"

}
catch {
    Write-Host ""
    Write-Host "ERROR: $_" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Step 2: Calculate versions
Write-Step "Calculating version changes"

$versions = @{}
$packagesToProcess = if ($Package -eq "all") { @("api", "agent") } else { @($Package) }

foreach ($pkg in $packagesToProcess) {
    $config = $PackageConfigs[$pkg]
    $currentVersion = Get-CurrentVersion -PyprojectPath $config.PyprojectPath
    $newVersion = Get-BumpedVersion -CurrentVersion $currentVersion -BumpType $BumpType
    
    $versions[$pkg] = @{
        Current = $currentVersion
        New = $newVersion
        Path = $config.PyprojectPath
        Name = $config.Name
    }
    
    Write-Info "$($config.Name): $currentVersion -> $newVersion"
}

# Determine release version (use highest version for tag)
$releaseVersion = ($versions.Values | ForEach-Object { $_.New } | Sort-Object -Descending)[0]
$releaseBranch = "release/v$releaseVersion"
$releaseTag = "v$releaseVersion"

Write-Host ""
Write-Info "Release branch: $releaseBranch"
Write-Info "Release tag: $releaseTag"

# Step 3: Confirm
Write-Host ""
$confirm = Read-Host "Proceed with release? (y/N)"
if ($confirm -notmatch '^[Yy]') {
    Write-Host ""
    Write-Host "Release cancelled." -ForegroundColor Yellow
    Pop-Location
    exit 0
}

# Step 4: Create release branch from current state
Write-Step "Creating release branch"

if ($DryRun) {
    Write-DryRunMsg "Would create branch: $releaseBranch"
}
else {
    # Check if branch already exists
    $branchExists = git branch --list $releaseBranch
    if ($branchExists) {
        throw "Release branch '$releaseBranch' already exists!"
    }
    
    git checkout -b $releaseBranch
    Write-Success "Created branch: $releaseBranch"
}

# Step 5: Update version files on release branch
Write-Step "Updating version files"

foreach ($pkg in $packagesToProcess) {
    $info = $versions[$pkg]
    
    if ($DryRun) {
        Write-DryRunMsg "Would update $($info.Path): $($info.New)"
    }
    else {
        Set-Version -PyprojectPath $info.Path -NewVersion $info.New
        Write-Success "Updated $($info.Name) to $($info.New)"
    }
}

# Step 6: Commit version bump on release branch
Write-Step "Committing release"

$commitMsg = "Release $releaseTag"

if ($DryRun) {
    Write-DryRunMsg "Would commit: $commitMsg"
}
else {
    git add -A
    git commit -m $commitMsg
    Write-Success "Committed version changes"
}

# Step 7: Tag the release
Write-Step "Tagging release"

if ($DryRun) {
    Write-DryRunMsg "Would create tag: $releaseTag"
}
else {
    git tag -a $releaseTag -m "Release $releaseTag"
    Write-Success "Created tag: $releaseTag"
}

# Step 8: Push release branch and tag
Write-Step "Pushing release branch"

if ($DryRun) {
    Write-DryRunMsg "Would push: $releaseBranch"
    Write-DryRunMsg "Would push tag: $releaseTag"
}
else {
    git push -u origin $releaseBranch
    git push origin $releaseTag
    Write-Success "Pushed $releaseBranch and $releaseTag to origin"
}

# Step 9: Switch back to main and update
Write-Step "Updating main branch"

if ($DryRun) {
    Write-DryRunMsg "Would switch back to main"
    Write-DryRunMsg "Would update main with version bump"
}
else {
    git checkout main
    
    # Merge the release into main (fast-forward)
    git merge $releaseBranch --no-edit
    git push origin main
    
    Write-Success "Main branch updated with release"
}

# Summary
Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "                    Release Complete!                          " -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Version: $releaseTag" -ForegroundColor Cyan
Write-Host "  Branch:  $releaseBranch" -ForegroundColor Cyan
Write-Host ""
Write-Host "  The release branch will remain untouched for rollback." -ForegroundColor Gray
Write-Host "  To rollback: git checkout $releaseBranch" -ForegroundColor Gray
Write-Host ""

Pop-Location
