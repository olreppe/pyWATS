# GitHub Enterprise Migration Guide

**Date:** 2026-01-27  
**Source:** https://github.com/olreppe/pyWATS  
**Target:** https://wats.ghe.com/WATS/pyWATS.git  
**Strategy:** Shallow clone from first pip release (v0.1.0b1)

---

## Overview

This repository is being migrated to GitHub Enterprise while maintaining the original GitHub repository in parallel. The migration includes history from the first PyPI release (v0.1.0b1, commit `8687e63`) onwards.

### Why Shallow Clone?

- **Cleaner history:** Starts from first public release rather than all development commits
- **Smaller repository:** Reduces clone time and disk usage
- **Professional baseline:** First release commit includes proper licensing, CI/CD, and documentation
- **Easier migration:** Avoids migrating early experimental commits

---

## Migration Process

### Prerequisites

1. Access to GitHub Enterprise at https://wats.ghe.com
2. Repository created at https://wats.ghe.com/WATS/pyWATS.git
3. Git credentials configured for GHE

### Step 1: Initial Migration

Run the migration script to create and populate the GHE repository:

```powershell
cd "C:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"
.\scripts\migrate_to_ghe.ps1
```

This script will:
1. Create a shallow clone from first release (v0.1.0b1, 2025-12-14)
2. Fetch all commits since that date
3. Fetch all tags (v0.1.0b2 through current)
4. Push to GitHub Enterprise

**First Release Commit:**
```
commit 8687e63a3117a7b0d27fa59000e7dd62cd77d26a
Date:   Sun Dec 14 01:38:43 2025 +0100
Subject: Prepare for PyPI release 0.1.0b1
```

### Step 2: Configure Your Working Copy

Add GHE as a remote to your existing working directory:

```powershell
cd "C:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"
.\scripts\setup_ghe_sync.ps1
```

Verify remotes:
```powershell
git remote -v
```

Expected output:
```
ghe     https://wats.ghe.com/WATS/pyWATS.git (fetch)
ghe     https://wats.ghe.com/WATS/pyWATS.git (push)
origin  https://github.com/olreppe/pyWATS.git (fetch)
origin  https://github.com/olreppe/pyWATS.git (push)
```

### Step 3: Set GHE Repository Details

Configure the repository on GitHub Enterprise:

1. Navigate to: https://wats.ghe.com/WATS/pyWATS/settings
2. Set repository details:
   - **Description:** Python client and API for Virinco WATS test data management system
   - **Website:** https://wats.com
   - **Topics:** wats, test-automation, electronics-manufacturing, quality-data, api-client
   - **Default branch:** main
3. Configure branch protection for `main`:
   - Require pull request reviews (optional)
   - Require status checks to pass (if CI/CD configured)
4. Add collaborators/teams as needed

---

## Daily Workflow

### Option 1: Sync to Both Remotes

Continue pushing to GitHub (public), then sync to GHE:

```powershell
# Normal workflow
git add .
git commit -m "your changes"
git push origin main

# Sync to GHE
.\scripts\sync_to_ghe.ps1
```

### Option 2: Use GHE as Primary

Switch to using GHE as primary remote:

```powershell
# Set GHE as default push
git push --set-upstream ghe main

# Push normally (goes to GHE)
git push

# Sync back to GitHub when needed
git push origin main
```

### Sync Script Options

```powershell
# Sync current branch
.\scripts\sync_to_ghe.ps1

# Sync specific branch
.\scripts\sync_to_ghe.ps1 -Branch feature/my-feature

# Sync all branches
.\scripts\sync_to_ghe.ps1 -All

# Sync current branch + tags (for releases)
.\scripts\sync_to_ghe.ps1 -PushTags
```

---

## Release Workflow

When creating a new release:

1. Update version and changelog
2. Commit and tag on GitHub:
   ```powershell
   git tag -a v0.1.0b39 -m "Release 0.1.0b39"
   git push origin main --tags
   ```

3. Sync to GHE:
   ```powershell
   .\scripts\sync_to_ghe.ps1 -PushTags
   ```

4. GitHub Actions will build and publish to PyPI (from GitHub)
5. GHE has the tagged release for internal reference

---

## Repository Comparison

| Aspect | GitHub (origin) | GitHub Enterprise (ghe) |
|--------|----------------|-------------------------|
| **URL** | github.com/olreppe/pyWATS | wats.ghe.com/WATS/pyWATS |
| **History** | Full (from 2584ba2) | Shallow (from 8687e63) |
| **First Commit** | 2024 (initial structure) | 2025-12-14 (v0.1.0b1) |
| **Purpose** | Public, PyPI releases | Internal, WATS team |
| **CI/CD** | GitHub Actions → PyPI | Optional internal CI |
| **Access** | Public | WATS organization only |
| **Primary Use** | Releases, public issues | Development, internal docs |

---

## Troubleshooting

### Authentication Issues

If prompted for credentials when pushing to GHE:

```powershell
# Use Git Credential Manager
git config --global credential.helper manager-core

# Or configure GHE token
git config --global credential.https://wats.ghe.com.username your-username
```

### Diverged Branches

If branches diverge between GitHub and GHE:

```powershell
# Option 1: Force push (if GHE is secondary)
git push ghe main --force

# Option 2: Merge (if both have unique commits)
git fetch ghe
git merge ghe/main
git push ghe main
```

### Large History Issues

If shallow clone includes too much history:

```powershell
# Create even shallower clone (from specific tag)
git clone --depth 1 --branch v0.1.0b1 https://github.com/olreppe/pyWATS.git
```

---

## Scripts Reference

### Migration Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `migrate_to_ghe.ps1` | Initial migration | Once, to create GHE repo |
| `setup_ghe_sync.ps1` | Add GHE remote | Once per working copy |
| `sync_to_ghe.ps1` | Sync changes to GHE | Daily, after pushing to GitHub |

### Script Locations

All scripts are in: `scripts/`

```
scripts/
├── migrate_to_ghe.ps1      # One-time migration
├── setup_ghe_sync.ps1      # Configure working copy
└── sync_to_ghe.ps1         # Daily sync
```

---

## Migration Checklist

- [ ] Run `migrate_to_ghe.ps1` to create GHE repository
- [ ] Verify repository at https://wats.ghe.com/WATS/pyWATS
- [ ] Set repository description and topics
- [ ] Configure branch protection rules
- [ ] Add team members/collaborators
- [ ] Run `setup_ghe_sync.ps1` in working copy
- [ ] Test sync with `sync_to_ghe.ps1`
- [ ] Update team documentation with GHE URL
- [ ] Configure CI/CD on GHE (if needed)
- [ ] Archive or update old internal references

---

## Maintaining Both Repositories

### GitHub (Public)
- ✅ Keep as source of truth for releases
- ✅ Continue PyPI publishing workflow
- ✅ Public issue tracking
- ✅ External contributions

### GitHub Enterprise (Internal)
- ✅ Internal development reference
- ✅ WATS team collaboration
- ✅ Internal documentation (kept in repo)
- ✅ May include proprietary customer examples
- ⚠️ Synced from GitHub (not source of truth initially)

### Transition Plan

**Phase 1 (Current):** GitHub primary, GHE mirror
- All commits to GitHub
- Regular sync to GHE

**Phase 2 (Future):** GHE primary, GitHub for releases
- Development on GHE
- Release branches pushed to GitHub for PyPI
- GitHub becomes release-only

**Phase 3 (Optional):** GHE only
- If package becomes internal-only
- Archive GitHub repository

---

## Related Documentation

- [PyPI Publishing Workflow](../.github/workflows/publish.yml)
- [Release Checklist](./internal_documentation/release_checklist.md)
- [Development Roadmap](./internal_documentation/WIP/to_do/ROADMAP.md)

---

## Support

For migration issues:
1. Check script output for specific errors
2. Verify GHE access and permissions
3. Contact WATS IT if GHE repository issues
4. Review Git credential configuration

---

**Last Updated:** 2026-01-27  
**Migration Status:** Ready to execute
