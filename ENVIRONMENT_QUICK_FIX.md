# 🔥 ENVIRONMENT NOT FOUND - QUICK FIX

**Last Updated**: December 12, 2025

## ⚡ FASTEST FIX (Copy & Paste This)

```powershell
# Run this in PowerShell at project root:
.\scripts\fix_environment.ps1
```

OR manually:

```powershell
# 1. Create .env if missing
if (!(Test-Path .env)) { Copy-Item .env.template .env; code .env }

# 2. Activate virtual environment
.venv\Scripts\Activate.ps1

# 3. Verify
Test-Path .env; Test-Path .venv
```

---

## 🎯 THE PROBLEM

**Line 123 in `.gitignore`** has `.env` which means:
- ✅ Your credentials stay safe (good!)
- ❌ You need to recreate `.env` on every fresh clone/pull (annoying!)

**The `.env` file contains your WATS credentials and is NEVER committed to git for security.**

---

## 📋 QUICK CHECKLIST

Run these commands to diagnose:

```powershell
# Check if .env exists
Test-Path .env         # Should be True

# Check if .venv exists  
Test-Path .venv        # Should be True

# Check Python location
(Get-Command python).Source   # Should contain ".venv"
```

---

## 📖 FULL DOCUMENTATION

See **[ENVIRONMENT_SETUP_GUIDE.md](ENVIRONMENT_SETUP_GUIDE.md)** for:
- Complete explanation
- Why this keeps happening
- All scenarios & fixes
- Prevention strategies

---

## ✅ AFTER FIXING

Remember to **edit your `.env` file** with actual credentials:

```dotenv
WATS_BASE_URL=https://your-actual-server.com
WATS_AUTH_TOKEN=your_actual_token_here
```

The template has placeholder values that won't work!
