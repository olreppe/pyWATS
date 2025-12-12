# Environment Setup Guide - RECURRING ISSUE FIX

## 🔥 THE PROBLEM (Read This First!)

**SYMPTOM**: Environment not found, application can't connect to WATS server, missing configuration

**ROOT CAUSE**: The `.env` file is (correctly) ignored by `.gitignore`, but you need to create it locally from the template.

---

## ✅ THE SOLUTION (Follow Every Time)

### Step 1: Create Your .env File

Copy the template to create your environment file:

```powershell
Copy-Item .env.template .env
```

Or manually create `.env` from `.env.template`

### Step 2: Configure Your .env File

Edit the `.env` file with your actual WATS server credentials:

```dotenv
# pyWATS Environment Configuration

# WATS API Configuration
WATS_BASE_URL=https://your-actual-wats-server.com
WATS_AUTH_TOKEN=your_actual_base64_token_here
WATS_TIMEOUT=30.0
WATS_REFERRER=https://your-actual-wats-server.com/dashboard

# Development Settings
PYTHONPATH=./src
```

### Step 3: Verify the File Exists

```powershell
Test-Path .env
# Should return: True
```

### Step 4: Verify Virtual Environment

```powershell
Test-Path .venv
# Should return: True

# Activate it
.venv\Scripts\Activate.ps1
```

---

## 🔍 WHY THIS KEEPS HAPPENING

### The .gitignore Setup (CORRECT - Don't Change!)

Line 123 in `.gitignore`:
```
.env
```

**This is CORRECT!** The `.env` file contains sensitive credentials and should NEVER be committed to git.

### What Gets Committed vs. What Doesn't

| File | Git Status | Why |
|------|-----------|-----|
| `.env.template` | ✅ Committed | Safe template without credentials |
| `.env` | ❌ NEVER committed | Contains actual secrets |
| `.venv/` | ❌ Ignored | Virtual environment (line 124 in .gitignore) |
| `.venv-*/` | ❌ Ignored | Alternative venv names (line 125 in .gitignore) |

---

## 🚨 COMMON SCENARIOS & FIXES

### Scenario 1: Fresh Clone / New Machine
**Problem**: Just cloned the repo, no `.env` file exists  
**Fix**: Follow steps 1-2 above to create `.env` from template

### Scenario 2: Pulled Latest Changes
**Problem**: Your `.env` was accidentally deleted or not preserved  
**Fix**: Verify `.env` exists, if not, recreate from template (keep your credentials!)

### Scenario 3: Virtual Environment Missing
**Problem**: `.venv` folder doesn't exist  
**Fix**: 
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Scenario 4: Wrong Virtual Environment Active
**Problem**: Using wrong Python interpreter  
**Fix**: 
```powershell
# Deactivate any active env
deactivate

# Activate the project's venv
.venv\Scripts\Activate.ps1

# Verify
python --version
which python
```

---

## 📝 CHECKLIST (Run When Issue Occurs)

```powershell
# 1. Check if .env exists
if (!(Test-Path .env)) {
    Write-Host "❌ .env file missing - Creating from template..." -ForegroundColor Red
    Copy-Item .env.template .env
    Write-Host "✅ Created .env - EDIT IT WITH YOUR CREDENTIALS!" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
}

# 2. Check if .venv exists
if (!(Test-Path .venv)) {
    Write-Host "❌ Virtual environment missing - Creating..." -ForegroundColor Red
    python -m venv .venv
    Write-Host "✅ Created .venv" -ForegroundColor Green
} else {
    Write-Host "✅ .venv exists" -ForegroundColor Green
}

# 3. Activate virtual environment
.venv\Scripts\Activate.ps1

# 4. Verify Python is from .venv
$pythonPath = (Get-Command python).Source
Write-Host "Python location: $pythonPath"
if ($pythonPath -like "*\.venv\*") {
    Write-Host "✅ Using project virtual environment" -ForegroundColor Green
} else {
    Write-Host "⚠️ WARNING: Not using project .venv!" -ForegroundColor Yellow
}

# 5. Show .env contents (without secrets)
Write-Host "`n.env configuration:"
Get-Content .env | Select-String -Pattern "^[^#]" | Select-String -NotMatch "TOKEN|PASSWORD"
```

---

## 🔧 AUTOMATED FIX SCRIPT

Save this as `scripts/fix_environment.ps1`:

```powershell
# Fix Environment - Run this when you have environment issues
Write-Host "=== pyWATS Environment Fix ===" -ForegroundColor Cyan

# Check and create .env
if (!(Test-Path .env)) {
    Write-Host "`n❌ .env missing - creating from template" -ForegroundColor Red
    Copy-Item .env.template .env
    Write-Host "⚠️ IMPORTANT: Edit .env with your WATS credentials!" -ForegroundColor Yellow
    code .env  # Open in VS Code
} else {
    Write-Host "`n✅ .env exists" -ForegroundColor Green
}

# Check and create .venv
if (!(Test-Path .venv)) {
    Write-Host "`n❌ .venv missing - creating virtual environment" -ForegroundColor Red
    python -m venv .venv
    Write-Host "✅ Created .venv" -ForegroundColor Green
    
    # Install dependencies
    .venv\Scripts\Activate.ps1
    Write-Host "`nInstalling dependencies..."
    pip install -e ".[dev]"
} else {
    Write-Host "`n✅ .venv exists" -ForegroundColor Green
}

# Activate
Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
.venv\Scripts\Activate.ps1

# Verify
$pythonPath = (Get-Command python).Source
Write-Host "`nPython: $pythonPath"

if ($pythonPath -like "*\.venv\*") {
    Write-Host "✅ Environment setup complete!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Warning: Python not from .venv" -ForegroundColor Yellow
}
```

**Usage:**
```powershell
.\scripts\fix_environment.ps1
```

---

## 🎯 QUICK REFERENCE

### Daily Workflow
```powershell
# 1. Navigate to project
cd "C:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"

# 2. Activate environment
.venv\Scripts\Activate.ps1

# 3. Verify .env exists
Test-Path .env  # Should be True

# 4. Run your code
python src/main.py
```

### If Something Goes Wrong
```powershell
# Run the fix script
.\scripts\fix_environment.ps1

# OR manually:
# 1. Check .env exists, create if missing
# 2. Check .venv exists, create if missing  
# 3. Activate .venv
# 4. Verify configuration
```

---

## 📚 Additional Resources

- **Template File**: `.env.template` - Never contains secrets, safe to commit
- **Actual Config**: `.env` - Contains your secrets, NEVER commit
- **Virtual Env**: `.venv/` - Python packages, NEVER commit
- **gitignore**: `.gitignore` line 123-125 - Protects secrets

---

## ⚡ ONE-LINE FIX (When You're Frustrated)

```powershell
if (!(Test-Path .env)) { Copy-Item .env.template .env; Write-Host "EDIT .env NOW!" -ForegroundColor Yellow } ; .venv\Scripts\Activate.ps1
```

---

**Last Updated**: December 12, 2025  
**Issue Frequency**: Recurring after git operations (pull, clone, clean)  
**Prevention**: Always verify `.env` exists before running code
