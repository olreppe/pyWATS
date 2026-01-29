#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quick validation - just imports and fast tests

.DESCRIPTION
    Runs a fast subset of checks for rapid iteration during development.
    Use validate_before_push.ps1 for full pre-push validation.
#>

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "Quick Validation Started" -ForegroundColor Cyan
Write-Host ""

# Check imports
Write-Host "Checking imports..." -ForegroundColor Yellow
& python -c "import pywats; import pywats.core.parallel; print('Imports OK')"

# Run fast tests only
Write-Host ""
Write-Host "Running fast tests..." -ForegroundColor Yellow
& python -m pytest tests/ -x -q -m "not server and not slow" --tb=line

Write-Host ""
Write-Host "Quick validation passed!" -ForegroundColor Green
Write-Host ""
