# pyWATS Beta Release Process

## ⚠️ IMPORTANT: Single Release Workflow

**There is only ONE way to release pyWATS while in beta:**

```powershell
.\scripts\bump.ps1
```

That's it. This script does everything:
1. ✅ Verifies you're on `main` with a clean working tree
2. ✅ Runs pre-release checks (lint + unit tests)
3. ✅ Bumps the beta version (e.g., `0.1.0b22` → `0.1.0b23`)
4. ✅ Updates version in both `pyproject.toml` and `src/pywats/__init__.py`
5. ✅ Commits the changes
6. ✅ Creates and pushes a git tag (e.g., `v0.1.0b23`)
7. ✅ Pushes to GitHub
8. ✅ Automatically triggers PyPI publish via GitHub Actions

## Branch Protection

Each release creates a protected release tag:
- Tags follow the pattern `v0.1.0bN` (e.g., `v0.1.0b23`)
- These tags are immutable and serve as release snapshots
- GitHub repository settings protect tags matching `v*` pattern

## Preview Mode

To see what would happen without making changes:

```powershell
.\scripts\bump.ps1 -DryRun
```

## Skip Pre-Release Checks

If you've already run checks manually:

```powershell
.\scripts\bump.ps1 -SkipChecks
```

## Common Mistakes to Avoid

❌ **DO NOT** manually edit version numbers  
❌ **DO NOT** manually create/push tags  
❌ **DO NOT** manually commit version bumps  
❌ **DO NOT** try to publish to PyPI manually  

✅ **ALWAYS** use `.\scripts\bump.ps1`

## Troubleshooting

### "Not on main branch"
```powershell
git checkout main
git pull
.\scripts\bump.ps1
```

### "Working tree is not clean"
```powershell
git status
# Commit or stash your changes first
.\scripts\bump.ps1
```

### "Pre-release checks failed"
Fix the failing tests/linting issues, commit, then run again.

## After Release

After running `bump.ps1`:
1. GitHub Actions automatically builds and publishes to PyPI (~2-3 minutes)
2. Check the Actions tab: https://github.com/olreppe/pyWATS/actions
3. Verify on PyPI: https://pypi.org/project/pywats-api/

## Integration Tests

Integration tests require a live WATS server and are NOT run automatically:

```powershell
.\scripts\pre_release_check.ps1 -IncludeIntegrationTests
```

Run these manually before important releases.

---

## For Future Stable Releases (v1.0.0+)

See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) for the full stable release process.
While in beta, ignore that checklist and just use `bump.ps1`.
