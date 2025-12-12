# Fix Environment - Run this when you have environment issues
# Location: scripts/fix_environment.ps1
# Usage: .\scripts\fix_environment.ps1

Write-Host "=== pyWATS Environment Fix ===" -ForegroundColor Cyan
Write-Host "Diagnosing and fixing environment issues...`n" -ForegroundColor Cyan

$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot

# Check and create .env
Write-Host "Checking .env file..." -NoNewline
if (!(Test-Path .env)) {
    Write-Host " ❌ MISSING" -ForegroundColor Red
    if (Test-Path .env.template) {
        Write-Host "Creating .env from template..." -ForegroundColor Yellow
        Copy-Item .env.template .env
        Write-Host "✅ Created .env" -ForegroundColor Green
        Write-Host "`n⚠️  IMPORTANT: You must edit .env with your actual WATS credentials!" -ForegroundColor Yellow
        Write-Host "Opening .env in editor..." -ForegroundColor Cyan
        
        # Try to open in VS Code, fall back to notepad
        try {
            code .env
        } catch {
            notepad .env
        }
    } else {
        Write-Host "❌ ERROR: .env.template not found!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host " ✅ EXISTS" -ForegroundColor Green
    # Verify it has content
    $envContent = Get-Content .env -Raw
    if ($envContent -match "WATS_BASE_URL=https://your-") {
        Write-Host "⚠️  WARNING: .env appears to have default values!" -ForegroundColor Yellow
        Write-Host "Please update with your actual WATS server credentials." -ForegroundColor Yellow
    }
}

# Check and create .venv
Write-Host "`nChecking virtual environment..." -NoNewline
if (!(Test-Path .venv)) {
    Write-Host " ❌ MISSING" -ForegroundColor Red
    Write-Host "Creating virtual environment (this may take a minute)..." -ForegroundColor Yellow
    
    try {
        python -m venv .venv
        Write-Host "✅ Created .venv" -ForegroundColor Green
        
        # Activate and install dependencies
        Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
        & .venv\Scripts\Activate.ps1
        
        Write-Host "Installing dependencies..." -ForegroundColor Cyan
        pip install --upgrade pip
        pip install -e ".[dev]"
        
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
    } catch {
        Write-Host "❌ ERROR creating virtual environment: $_" -ForegroundColor Red
        Pop-Location
        exit 1
    }
} else {
    Write-Host " ✅ EXISTS" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
try {
    & .venv\Scripts\Activate.ps1
    Write-Host "✅ Activated" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR activating: $_" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Verify Python location
Write-Host "`nVerifying Python interpreter..." -NoNewline
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pythonPath -and ($pythonPath -like "*\.venv\*" -or $pythonPath -like "*\.venv-*\*")) {
    Write-Host " ✅ CORRECT" -ForegroundColor Green
    Write-Host "Using: $pythonPath" -ForegroundColor Gray
} else {
    Write-Host " ⚠️  WARNING" -ForegroundColor Yellow
    Write-Host "Python location: $pythonPath" -ForegroundColor Yellow
    Write-Host "This may not be the project's virtual environment!" -ForegroundColor Yellow
}

# Show Python version
Write-Host "`nPython version:" -NoNewline
$version = python --version 2>&1
Write-Host " $version" -ForegroundColor Cyan

# Summary
Write-Host "`n=== Environment Status ===" -ForegroundColor Cyan
Write-Host "✅ .env file: " -NoNewline -ForegroundColor Green
if (Test-Path .env) { Write-Host "Present" } else { Write-Host "Missing" -ForegroundColor Red }

Write-Host "✅ Virtual environment: " -NoNewline -ForegroundColor Green  
if (Test-Path .venv) { Write-Host "Present" } else { Write-Host "Missing" -ForegroundColor Red }

Write-Host "✅ Python location: " -NoNewline -ForegroundColor Green
Write-Host "$pythonPath"

Write-Host "`n🎉 Environment fix complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Verify .env has your actual WATS credentials (not template defaults)"
Write-Host "2. Run your code: python src/main.py"
Write-Host "3. If issues persist, check ENVIRONMENT_SETUP_GUIDE.md"

Pop-Location
