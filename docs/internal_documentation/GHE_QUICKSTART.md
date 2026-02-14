# GitHub Enterprise Migration - Quick Start

## ✅ Migration Complete

The repository has been migrated to: **https://wats.ghe.com/WATS/pyWATS**

## Automated Sync (Recommended)

**Releases automatically sync to GHE via GitHub Actions!**

Setup required (one time):
1. Create GHE Personal Access Token with `repo` scope
2. Add as `GHE_TOKEN` secret to GitHub repository
3. See: [docs/internal_documentation/GHE_TOKEN_SETUP.md](docs/internal_documentation/GHE_TOKEN_SETUP.md)

Once configured, every PyPI release will automatically sync to GHE.

## Manual Sync (If Needed)

## Manual Sync (If Needed)

For non-release commits or manual syncing:

```powershell
# After pushing to GitHub, sync to GHE:
git push origin main
.\scripts\sync_to_ghe.ps1
```

## Release Workflow

```powershell
# Create and push tag:
git tag -a v0.1.0b39 -m "Release 0.1.0b39"
git push origin main --tags

# GitHub Actions will automatically:
# ✅ Build and publish to PyPI
# ✅ Sync main branch to GHE
# ✅ Sync all tags to GHE
```

No manual sync needed for releases!

## Full Documentation

See: [docs/internal_documentation/GHE_MIGRATION.md](docs/internal_documentation/GHE_MIGRATION.md)

---

**Migration Details:**
- **Source:** https://github.com/olreppe/pyWATS
- **Target:** https://wats.ghe.com/WATS/pyWATS.git
- **History:** From v0.1.0b1 (2025-12-14) onwards
- **First commit:** 8687e63 "Prepare for PyPI release 0.1.0b1"
