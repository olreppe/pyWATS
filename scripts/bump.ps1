<#
.SYNOPSIS
    Beta bump + tag + push for pyWATS.

.DESCRIPTION
    This is the single supported bump flow for pyWATS while in beta.

    Publishing is triggered by pushing a git tag that matches 'v*' (see .github/workflows/publish.yml).

    Default behavior:
      - verifies you're on main with clean working tree
      - runs local pre-release checks (lint + unit tests)
      - bumps the version (beta by default)
      - updates all version locations (pyproject + __version__ constants)
      - commits, tags, and pushes

.PARAMETER BumpType
    One of:
    - beta  : 0.1.0b19 -> 0.1.0b20 (or 0.1.0 -> 0.1.0b1)
      - patch : 0.1.0b17 -> 0.1.1b1
      - minor : 0.1.0b17 -> 0.2.0b1
      - major : 0.1.0b17 -> 1.0.0b1

    Note: examples are illustrative; the script bumps based on the current version.

.PARAMETER DryRun
    Preview what would happen without making changes.

.PARAMETER SkipChecks
    Skip running scripts/pre_release_check.ps1.

.PARAMETER NoPush
    Do not push commits/tags to origin.

.EXAMPLE
    .\scripts\bump.ps1

.EXAMPLE
    .\scripts\bump.ps1 -BumpType beta -DryRun

.EXAMPLE
    .\scripts\bump.ps1 -BumpType patch
#>

param(
    [ValidateSet("beta", "patch", "minor", "major")]
    [string]$BumpType = "beta",

    [switch]$DryRun,
    [switch]$SkipChecks,
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"

# ============================================================================
# Configuration
# ============================================================================

$RepoRoot = Split-Path -Parent $PSScriptRoot

# ============================================================================
# Helpers
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

function Write-DryRunMsg {
    param([string]$Message)
    Write-Host "  [DRY RUN] " -ForegroundColor Magenta -NoNewline
    Write-Host $Message -ForegroundColor Gray
}

function Get-CurrentBranch {
    return (git rev-parse --abbrev-ref HEAD).Trim()
}

function Test-CleanWorkingTree {
    $status = git status --porcelain
    return [string]::IsNullOrWhiteSpace($status)
}

function Get-PyprojectVersion {
    param([string]$PyprojectPath)

    $content = Get-Content $PyprojectPath -Raw
    if ($content -match 'version\s*=\s*"([^\"]+)"') {
        return $Matches[1]
    }
    throw "Could not find version in $PyprojectPath"
}

function ConvertFrom-Version {
    param([string]$Version)

    # Accept: X.Y.Z or X.Y.ZbN
    if ($Version -notmatch '^(\d+)\.(\d+)\.(\d+)(?:b(\d+))?$') {
        throw "Unsupported version format: '$Version' (expected X.Y.Z or X.Y.ZbN)"
    }

    return @{
        Major = [int]$Matches[1]
        Minor = [int]$Matches[2]
        Patch = [int]$Matches[3]
        Beta  = if ($Matches[4]) { [int]$Matches[4] } else { $null }
    }
}

function Format-Version {
    param(
        [int]$Major,
        [int]$Minor,
        [int]$Patch,
        [Nullable[int]]$Beta
    )

    if ($null -eq $Beta) {
        return "$Major.$Minor.$Patch"
    }

    return "$Major.$Minor.$Patch" + "b$Beta"
}

function Get-BumpedVersion {
    param(
        [string]$CurrentVersion,
        [string]$BumpType
    )

    $v = ConvertFrom-Version -Version $CurrentVersion

    $major = $v.Major
    $minor = $v.Minor
    $patch = $v.Patch
    $beta  = $v.Beta

    switch ($BumpType) {
        "beta" {
            if ($null -eq $beta) {
                $beta = 1
            }
            else {
                $beta = $beta + 1
            }
        }
        "patch" {
            $patch = $patch + 1
            $beta = 1
        }
        "minor" {
            $minor = $minor + 1
            $patch = 0
            $beta = 1
        }
        "major" {
            $major = $major + 1
            $minor = 0
            $patch = 0
            $beta = 1
        }
        default {
            throw "Unsupported bump type: $BumpType"
        }
    }

    return Format-Version -Major $major -Minor $minor -Patch $patch -Beta $beta
}

function Set-PyprojectVersion {
    param(
        [string]$PyprojectPath,
        [string]$NewVersion
    )

    $content = Get-Content $PyprojectPath -Raw
    # Only match the project version (after [project] section), not tool configs like python_version
    $newContent = $content -replace '(?m)^version\s*=\s*"[^\"]+"', "version = `"$NewVersion`""

    if ($DryRun) {
        Write-DryRunMsg "Would update $PyprojectPath -> $NewVersion"
        return
    }

    Set-Content -Path $PyprojectPath -Value $newContent -NoNewline
    Write-Success "Updated $PyprojectPath"
}

function Set-PythonInitVersion {
    param(
        [string]$InitPyPath,
        [string]$NewVersion
    )

    $content = Get-Content $InitPyPath -Raw

    if ($content -notmatch '__version__\s*=\s*"[^\"]+"') {
        throw "Could not find __version__ in $InitPyPath"
    }

    $newContent = $content -replace '__version__\s*=\s*"[^\"]+"', "__version__ = `"$NewVersion`""

    if ($DryRun) {
        Write-DryRunMsg "Would update $InitPyPath -> $NewVersion"
        return
    }

    Set-Content -Path $InitPyPath -Value $newContent -NoNewline
    Write-Success "Updated $InitPyPath"
}

# ============================================================================
# Main
# ============================================================================

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "                 pyWATS Beta Bump + Tag                        " -ForegroundColor Cyan
Write-Host "===============================================================" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host ""
    Write-Host "  DRY RUN MODE - No changes will be made" -ForegroundColor Magenta
}

Push-Location $RepoRoot
try {
    Write-Step "Validating git state"

    $currentBranch = Get-CurrentBranch
    if ($currentBranch -ne "main") {
        throw "Must be on 'main' branch. Currently on: $currentBranch"
    }
    Write-Success "On main branch"

    if (-not (Test-CleanWorkingTree)) {
        if ($DryRun) {
            Write-Info "Working tree has uncommitted changes (dry run allowed)"
        }
        else {
            throw "Working tree has uncommitted changes. Please commit or stash first."
        }
    }
    else {
        Write-Success "Working tree is clean"
    }

    if (-not $DryRun) {
        Write-Info "Pulling latest from origin..."
        git pull origin main --quiet

        Write-Info "Fetching tags from origin..."
        git fetch --tags --quiet
    }
    Write-Success "Up to date with origin"

    if (-not $SkipChecks) {
        Write-Step "Running pre-release checks (lint + unit tests)"

        if ($DryRun) {
            Write-DryRunMsg "Would run: .\\scripts\\pre_release_check.ps1"
        }
        else {
            & "$RepoRoot\scripts\pre_release_check.ps1"
        }
    }

    Write-Step "Checking Domain Health"

    $healthDir = "$RepoRoot\docs\internal_documentation\domain_health"
    if (Test-Path $healthDir) {
        $staleHealthChecks = Get-ChildItem "$healthDir\*.md" -Exclude "README.md","TEMPLATE.md" | 
            Where-Object { $_.LastWriteTime -lt (Get-Date).AddMonths(-3) }
        
        if ($staleHealthChecks) {
            Write-Host ""
            Write-Host "  ⚠️  WARNING: Some domain health checks are outdated (>3 months)!" -ForegroundColor Yellow
            Write-Host ""
            $staleHealthChecks | ForEach-Object {
                $age = [int]((Get-Date) - $_.LastWriteTime).TotalDays
                Write-Host "    - $($_.BaseName): $age days old" -ForegroundColor Yellow
            }
            Write-Host ""
            Write-Host "  Run: .\scripts\domain_health_check.ps1 -FindStale" -ForegroundColor Gray
            Write-Host ""
            $response = Read-Host "Continue anyway? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                throw "Release cancelled - please update domain health checks first"
            }
        }
        else {
            Write-Success "All domain health checks are current"
        }
    }
    else {
        Write-Info "Domain health checks not found (skipping)"
    }

    Write-Step "Checking CHANGELOG"

    $changelogPath = "$RepoRoot\CHANGELOG.md"
    $changelogContent = Get-Content $changelogPath -Raw

    if ($changelogContent -match '## \[Unreleased\]\s*$' -or $changelogContent -match '## \[Unreleased\]\s*\n\s*\n\s*##') {
        Write-Host "" 
        Write-Host "  ⚠️  WARNING: CHANGELOG.md has no unreleased changes!" -ForegroundColor Yellow
        Write-Host "" 
        Write-Host "  The [Unreleased] section appears to be empty." -ForegroundColor Yellow
        Write-Host "  Please update CHANGELOG.md before bumping the version." -ForegroundColor Yellow
        Write-Host "" 
        $response = Read-Host "Continue anyway? (y/N)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            throw "Release cancelled - please update CHANGELOG.md first"
        }
    }
    else {
        Write-Success "CHANGELOG.md has unreleased changes"
    }

    Write-Step "Calculating version"

    $currentVersion = Get-PyprojectVersion -PyprojectPath "$RepoRoot\pyproject.toml"
    $newVersion = Get-BumpedVersion -CurrentVersion $currentVersion -BumpType $BumpType

    Write-Info "Current: $currentVersion"
    Write-Info "New:     $newVersion"

    $tag = "v$newVersion"

    Write-Step "Checking tag availability"

    $existingTag = git tag --list $tag

    if ($existingTag) {
        if ($DryRun) {
            Write-DryRunMsg "Tag already exists: $tag"
        }
        else {
            throw "Tag '$tag' already exists"
        }
    }
    else {
        if ($DryRun) {
            Write-DryRunMsg "Tag is available: $tag"
        }
        else {
            Write-Success "Tag is available: $tag"
        }
    }

    Write-Step "Updating version files"
    Set-PyprojectVersion -PyprojectPath "$RepoRoot\pyproject.toml" -NewVersion $newVersion
    Set-PythonInitVersion -InitPyPath "$RepoRoot\src\pywats\__init__.py" -NewVersion $newVersion

    Write-Step "Updating Sphinx API documentation version"
    
    if ($DryRun) {
        Write-DryRunMsg "Would update Sphinx conf.py version to $newVersion"
    }
    else {
        # Update version in Sphinx conf.py (GitHub Actions will build the docs)
        $confPath = "$RepoRoot\docs\api\conf.py"
        $confContent = Get-Content $confPath -Raw
        $confContent = $confContent -replace "release\s*=\s*'[^']+'", "release = '$newVersion'"
        $confContent = $confContent -replace "version\s*=\s*'[^']+'", "version = '$($newVersion -replace 'b.*$', '')'"
        Set-Content -Path $confPath -Value $confContent -NoNewline
        Write-Success "Updated Sphinx conf.py version"
        Write-Info "Sphinx documentation will be built by GitHub Actions during publish"
    }

    Write-Step "Committing + tagging"

    if ($DryRun) {
        Write-DryRunMsg "Would commit: Bump version to $tag"
        Write-DryRunMsg "Would tag:    $tag"
    }
    else {
        git add -A
        git commit -m "Bump version to $tag"

        git tag -a $tag -m "Beta bump $tag"
        Write-Success "Committed and tagged $tag"
    }

    if (-not $NoPush) {
        Write-Step "Pushing"

        if ($DryRun) {
            Write-DryRunMsg "Would push: origin main"
            Write-DryRunMsg "Would push tag: $tag"
        }
        else {
            git push origin main
            git push origin $tag
            Write-Success "Pushed main and $tag"
        }
    }
    else {
        Write-Info "NoPush set: not pushing to origin"
    }

    Write-Host ""
    Write-Host "===============================================================" -ForegroundColor Green
    Write-Host "                      Bump Complete!                           " -ForegroundColor Green
    Write-Host "===============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Version: $tag" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Publish trigger: push tag '$tag' (v*)" -ForegroundColor Gray
    Write-Host ""
}
finally {
    Pop-Location
}
