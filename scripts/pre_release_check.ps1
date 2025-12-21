<#
.SYNOPSIS
    Pre-release validation script for pyWATS.
    
.DESCRIPTION
    Runs the same checks as CI before creating a release:
    - Flake8 linting for critical errors (syntax, undefined names)
    - All tests (agent + API)
    
.EXAMPLE
    .\scripts\pre_release_check.ps1
    
.EXAMPLE
    .\scripts\pre_release_check.ps1 -SkipTests
    # Skip tests, only run linting
#>

param(
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"

# ============================================================================
# Configuration
# ============================================================================

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = "$RepoRoot\.venv\Scripts\python.exe"

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

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "  [ERROR] " -ForegroundColor Red -NoNewline
    Write-Host $Message -ForegroundColor Gray
}

# ============================================================================
# Pre-flight checks
# ============================================================================

Write-Step "Pre-release validation checks"

if (-not (Test-Path $VenvPython)) {
    Write-Error-Custom "Virtual environment not found at $VenvPython"
    Write-Host "  Run: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# ============================================================================
# Linting - Critical errors only (same as CI)
# ============================================================================

Write-Step "Running flake8 (critical errors only)"
Write-Host "  Checking for: syntax errors, undefined names" -ForegroundColor Gray

& $VenvPython -m flake8 src/pywats --count --select=E9,F63,F7,F82 --show-source --statistics

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Flake8 found critical errors (see above)"
    Write-Host ""
    Write-Host "  These are the same errors that will fail CI." -ForegroundColor Yellow
    Write-Host "  Fix them before releasing." -ForegroundColor Yellow
    exit 1
}

Write-Success "No critical linting errors"

# ============================================================================
# Tests (optional)
# ============================================================================

if (-not $SkipTests) {
    Write-Step "Running test suite"
    Write-Host "  This may take a few minutes..." -ForegroundColor Gray
    
    & $VenvPython -m pytest api-agent-tests/ api-tests/ -v --tb=short -x
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Tests failed"
        exit 1
    }
    
    Write-Success "All tests passed"
}

# ============================================================================
# Summary
# ============================================================================

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  Pre-release checks passed" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ready to release!" -ForegroundColor Cyan
Write-Host 'Next step: .\scripts\release.ps1 -BumpType patch' -ForegroundColor Gray
Write-Host ""

