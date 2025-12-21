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
    [switch]$SkipTests,
    [switch]$IncludeIntegrationTests
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

    # Keep default behavior aligned with CI: unit tests that do not require a live server.
    $env:WATS_BASE_URL = if ($env:WATS_BASE_URL) { $env:WATS_BASE_URL } else { "https://demo.wats.com" }
    $env:WATS_AUTH_TOKEN = if ($env:WATS_AUTH_TOKEN) { $env:WATS_AUTH_TOKEN } else { "dGVzdDp0ZXN0" }

    # Exclude server-dependent agent tests by default.
    & $VenvPython -m pytest api-agent-tests/ -m "not server" -v --tb=short -x

    if ($LASTEXITCODE -ne 0) {
        Write-Error-Custom "Unit tests failed"
        exit 1
    }

    Write-Success "Unit tests passed"

    if ($IncludeIntegrationTests) {
        Write-Step "Running agent server tests (requires live server + credentials)"
        & $VenvPython -m pytest api-agent-tests/ -m server -v --tb=short -x

        if ($LASTEXITCODE -ne 0) {
            Write-Error-Custom "Agent server tests failed"
            exit 1
        }

        Write-Success "Agent server tests passed"

        Write-Step "Running API integration tests (requires live server + credentials)"
        & $VenvPython -m pytest api-tests/ -v --tb=short -x
    
        if ($LASTEXITCODE -ne 0) {
            Write-Error-Custom "Integration tests failed"
            exit 1
        }

        Write-Success "Integration tests passed"
    }
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
Write-Host 'Next step: .\scripts\bump.ps1' -ForegroundColor Gray
Write-Host ""

