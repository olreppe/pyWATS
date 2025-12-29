# GitHub Repository Settings

## Branch Protection for Releases

To ensure release integrity, configure the following in GitHub:

### Settings → Branches → Add branch protection rule

**Branch name pattern:** `main`

Enable:
- ✅ Require a pull request before merging
  - Require approvals: 1
- ✅ Require status checks to pass before merging
  - Require branches to be up to date before merging
  - Status checks: (add any CI checks when available)
- ✅ Do not allow bypassing the above settings

### Settings → Tags → Add tag protection rule

**Tag name pattern:** `v*`

This protects all release tags (e.g., `v0.1.0b23`) from being deleted or force-pushed.

## Creating Protected Release Branches (Future)

For major releases (v1.0.0, v2.0.0), create release branches:

```powershell
# When releasing v1.0.0
git checkout -b release/v1.0
git push -u origin release/v1.0
```

Then add branch protection rule:

**Branch name pattern:** `release/v*`

Enable same protections as `main`.

## Current Setup

While in beta, each release creates a tag (e.g., `v0.1.0b23`) which serves as the release snapshot. The `main` branch continues to evolve.

Once stable (v1.0.0+), we'll create `release/v1.0` branch for patch releases while `main` continues development.

---

**Note:** Branch protection settings must be configured in GitHub's web interface. This file documents the required settings for maintainers.
