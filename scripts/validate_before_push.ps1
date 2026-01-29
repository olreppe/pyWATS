#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run all GitHub Actions checks locally before pushing

.DESCRIPTION
    Validates code quality, type checking, and tests locally to catch
    issues before they fail in CI/CD. Runs the exact same commands as
    GitHub Actions workflows.

.EXAMPLE
    .\scripts\validate_before_push.ps1
    
.EXAMPLE
    .\scripts\validate_before_push.ps1 -SkipTests
#>

param(
    [switch]$SkipTests,
    [switch]$SkipTypeCheck,
    [switch]$Fast  # Skip slow tests
)

$ErrorActionPreference = "Continue"
$script:FailureCount = 0

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " $Message" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Failure {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    $script:FailureCount++
}

# Ensure we're in the project root
if (!(Test-Path "pyproject.toml")) {
    Write-Error "Must run from project root directory"
    exit 1
}

# Activate virtual environment if not already active
if (!$env:VIRTUAL_ENV) {
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        Write-Host "Activating virtual environment..." -ForegroundColor Yellow
        & .venv\Scripts\Activate.ps1
    } else {
        Write-Warning "No virtual environment found. Install dependencies first with: pip install -e .[dev]"
    }
}

# =============================================================================
# 1. TYPE CHECKING (matches GitHub Actions workflow)
# =============================================================================
if (!$SkipTypeCheck) {
    Write-Step "Running Type Checking (mypy)"
    
    $mypyResult = python -m mypy src/pywats --config-file pyproject.toml 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Type checking passed"
    } else {
        Write-Failure "Type checking failed"
        Write-Host $mypyResult -ForegroundColor Red
    }
}

# =============================================================================
# 2. UNIT TESTS (matches GitHub Actions test workflow)
# =============================================================================
if (!$SkipTests) {
    Write-Step "Running Unit Tests"
    
    $testArgs = @(
        "tests/",
        "-v",
        "--tb=short",
        "-x",  # Stop on first failure
        "-m", "not server"  # Skip server integration tests
    )
    
    if ($Fast) {
        $testArgs += @("-m", "not slow")
    }
    
    python -m pytest @testArgs
    if ($LASTEXITCODE -eq 0) {
        Write-Success "All tests passed"
    } else {
        Write-Failure "Tests failed"
    }
}

# =============================================================================
# 3. IMPORT CHECK (quick sanity check)
# =============================================================================
Write-Step "Checking Module Imports"

$importCheck = python -c "import pywats; print('pywats OK')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Module imports successfully"
} else {
    Write-Failure "Module import failed"
    Write-Host $importCheck -ForegroundColor Red
}

# =============================================================================
# 4. BUILD CHECK
# =============================================================================
Write-Step "Checking Package Build"

python -m build --sdist --wheel --outdir dist/ . 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Success "Package builds successfully"
} else {
    Write-Failure "Package build failed"
}

# =============================================================================
# SUMMARY
# =============================================================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($script:FailureCount -eq 0) {
    Write-Host " ALL CHECKS PASSED" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Safe to push to GitHub!" -ForegroundColor Green
    exit 0
}
else {
    Write-Host " $($script:FailureCount) CHECK(S) FAILED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Fix issues before pushing!" -ForegroundColor Red
    exit 1
}
