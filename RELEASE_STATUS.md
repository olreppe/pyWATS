# PyPI Release Status - December 14, 2025

## ✅ RELEASED TO PyPI!

**Version 0.1.0b1** has been published to PyPI!

- **Package URL:** https://pypi.org/project/pywats-api/
- **Install:** `pip install pywats-api`
- **Tag:** `v0.1.0b1`
- **Commit:** `ee6f67d`

### Release Summary

- [x] LICENSE (MIT)
- [x] CHANGELOG.md
- [x] MANIFEST.in
- [x] GitHub Actions workflows (publish.yml, test.yml)
- [x] pyproject.toml (version 0.1.0b1, author Virinco AS)
- [x] __init__.py with __version__ and __wats_server_version__
- [x] Test configs secured (gitignored + templates)
- [x] Hardcoded URLs cleaned from tests
- [x] README.md with PyPI badges and install instructions
- [x] PyPI Trusted Publishing configured
- [x] Tag created and pushed: `v0.1.0b1`
- [x] GitHub Actions workflow triggered

## Package Details

- **Name:** pywats-api
- **Version:** 0.1.0b1 (beta)
- **Author:** Virinco AS
- **License:** MIT
- **Python:** >=3.10
- **WATS Server Required:** 2025.3.9.824+

## Installation Options

```bash
# Core API library only
pip install pywats-api

# With GUI client (requires Qt)
pip install pywats-api[client]

# Headless client (no Qt - for servers, Raspberry Pi)
pip install pywats-api[client-headless]
```

---
*This file can be deleted after verifying the release on PyPI.*
