#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Git pre-commit hook - validates code before allowing commit

.DESCRIPTION
    Automatically runs basic validation before each commit.
    To install: Copy to .git/hooks/pre-commit (remove .ps1 extension)
    To bypass: git commit --no-verify
#>

$ErrorActionPreference = "Stop"

Write-Host "`n🔒 Pre-commit validation running...`n" -ForegroundColor Cyan

# Check if we're in the right directory
if (!(Test-Path "pyproject.toml")) {
    Write-Error "Not in project root"
    exit 1
}

# Quick import check
Write-Host "Checking imports..." -ForegroundColor Yellow
try {
    python -c "import pywats; print('✓ Imports OK')" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Import check failed!" -ForegroundColor Red
        Write-Host "Run: python -c 'import pywats'" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "✗ Import check failed!" -ForegroundColor Red
    exit 1
}

# Run type checking on staged files only
Write-Host "Type checking..." -ForegroundColor Yellow
$stagedPyFiles = git diff --cached --name-only --diff-filter=ACM | Where-Object { $_ -match '\.py$' -and $_ -match '^src/' }

if ($stagedPyFiles) {
    python -m mypy @stagedPyFiles --config-file pyproject.toml 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Type check failed on staged files!" -ForegroundColor Red
        Write-Host "Run: python -m mypy $($stagedPyFiles -join ' ')" -ForegroundColor Yellow
        Write-Host "Or bypass with: git commit --no-verify" -ForegroundColor Gray
        exit 1
    }
}

Write-Host "✓ Pre-commit validation passed!`n" -ForegroundColor Green
exit 0
