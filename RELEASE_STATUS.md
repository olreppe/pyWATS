# PyPI Release Status - December 14, 2025

## ✅ COMPLETED

All PyPI release preparation is done and pushed to GitHub (commit `8687e63`):

- [x] LICENSE (MIT)
- [x] CHANGELOG.md
- [x] MANIFEST.in
- [x] GitHub Actions workflows (publish.yml, test.yml)
- [x] pyproject.toml updated (version 0.1.0b1, author Virinco AS)
- [x] __init__.py with __version__ and __wats_server_version__
- [x] Test configs secured (gitignored + templates)
- [x] Hardcoded URLs cleaned from tests
- [x] README.md with PyPI badges and install instructions
- [x] PyPI Trusted Publishing configured (user confirmed)

## 🔜 NEXT STEP: Create Release Tag

After system restart, run these commands to trigger the PyPI release:

```powershell
cd "C:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"
git tag v0.1.0b1
git push origin v0.1.0b1
```

**Alternative:** Create release via GitHub web UI:
1. Go to https://github.com/olreppe/pyWATS/releases/new
2. Tag: `v0.1.0b1`
3. Target: `main`
4. Title: `v0.1.0b1 - Initial Beta Release`
5. Click "Publish release"

## What Happens Next

Once the tag is pushed:
1. GitHub Actions `publish.yml` workflow triggers automatically
2. Tests run first
3. Package builds (sdist + wheel)
4. Publishes to PyPI via Trusted Publishing
5. Package available at: https://pypi.org/project/pywats-api/

## Package Details

- **Name:** pywats-api
- **Version:** 0.1.0b1 (beta)
- **Author:** Virinco AS
- **License:** MIT
- **Python:** >=3.8
- **WATS Server Required:** 2025.3.9.824+

---
*Delete this file after successful release.*
