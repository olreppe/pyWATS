# Git Repository Migration Guide

This document outlines the steps to migrate the pyWATS repository from `olreppe/pyWATS` to the company's official GitHub organization.

## Pre-Migration Status

### Repository Statistics (After Cleanup)
| Metric | Value |
|--------|-------|
| **Current Remote** | `https://github.com/olreppe/pyWATS.git` |
| **Total Commits** | 363 |
| **Branches** | 1 (main only) |
| **Tags** | 30 (v0.1.0b2 → v0.1.0b35) |
| **Size** | ~37 MB |

### Cleanup Completed
- [x] Deleted 31 stale remote branches
- [x] Deleted 25 stale local branches
- [x] Pruned remote tracking references
- [x] All version tags preserved

### Known History Bloat
The following deleted files still exist in git history (~180 MB total):

| File | Size | Notes |
|------|------|-------|
| `scale.txt` | 146 MB | Test file, deleted |
| `Large.xml` | 21 MB | Test file, deleted |
| `tmp.txt` | 11 MB | Temporary file |
| `itextsharp.dll` | 3.9 MB | .NET DLL |
| Various ATML XMLs | ~5 MB each | Test fixtures |

**Recommendation**: Consider using `git filter-repo` to remove these from history before migration, or accept the bloat for full history preservation.

---

## Prerequisites

### 1. Company GitHub Account Access
- [ ] Confirm your company GitHub username
- [ ] Ensure you have permission to create repositories in the organization
- [ ] Or request an empty repository be created for you

### 2. Create Personal Access Token (PAT)
1. Log into GitHub with your **company account**
2. Go to: **Settings → Developer settings → Personal access tokens → Fine-grained tokens**
3. Click **Generate new token**
4. Configure:
   - **Token name**: `pyWATS-migration`
   - **Expiration**: 7 days (short-lived for migration)
   - **Repository access**: Select the target repository
   - **Permissions**:
     - `Contents`: Read and write
     - `Metadata`: Read
5. Copy and save the token securely

### 3. Repository Information
Fill in before migration:

```
Company Organization: ________________
Repository Name:      ________________
Full URL:            https://github.com/________/________.git
```

---

## Migration Options

### Option A: Direct Migration (Recommended)
Preserves full history. Simple and maintains all commit references.

```powershell
cd "c:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"

# Add company remote
git remote add company https://github.com/COMPANY-ORG/pyWATS.git

# Push main branch
git push company main

# Push all tags
git push company --tags

# Verify
git remote -v
```

### Option B: Clean History Migration
Removes large files from history first (~180 MB savings).

```powershell
# Install git-filter-repo
pip install git-filter-repo

# Create a fresh clone for filtering (don't filter your working copy!)
git clone --mirror https://github.com/olreppe/pyWATS.git pyWATS-mirror
cd pyWATS-mirror

# Remove files larger than 5 MB from history
git filter-repo --strip-blobs-bigger-than 5M --force

# Push to company remote
git remote add company https://github.com/COMPANY-ORG/pyWATS.git
git push company --all
git push company --tags
```

**Warning**: This rewrites commit SHAs. Old commit links will break.

### Option C: Shallow Clone Migration
Fresh start with recent history only.

```powershell
# Clone with limited history (last 100 commits)
git clone --depth=100 --single-branch https://github.com/olreppe/pyWATS.git pyWATS-shallow
cd pyWATS-shallow

# Fetch tags
git fetch --tags

# Push to company remote
git remote set-url origin https://github.com/COMPANY-ORG/pyWATS.git
git push origin main
git push origin --tags
```

---

## Authentication for Dual GitHub Accounts

Since you have separate personal and company GitHub accounts:

### Option 1: HTTPS with Credential Prompt
Git will prompt for credentials when pushing to the new remote:
- **Username**: Your company GitHub username
- **Password**: Your Personal Access Token (NOT password)

### Option 2: SSH Keys (Better for Long-term)

```powershell
# Generate SSH key for company account
ssh-keygen -t ed25519 -C "your.email@company.com" -f $HOME\.ssh\id_company

# Display public key to add to GitHub
Get-Content $HOME\.ssh\id_company.pub
```

Add the public key to your company GitHub account:
**Settings → SSH and GPG keys → New SSH key**

Create/edit `~/.ssh/config`:
```
Host github-company
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_company
    IdentitiesOnly yes

Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Then use SSH URL format:
```powershell
git remote add company git@github-company:COMPANY-ORG/pyWATS.git
```

---

## Post-Migration Tasks

### 1. Update CI/CD Workflows
The following workflows need attention in the new repository:

| Workflow | File | Action Required |
|----------|------|-----------------|
| Tests | `.github/workflows/test.yml` | Should work as-is |
| PyPI Publish | `.github/workflows/publish.yml` | Reconfigure trusted publishing |
| Docs | `.github/workflows/docs.yml` | Update if using GitHub Pages |

### 2. Reconfigure PyPI Trusted Publishing
1. Go to [PyPI](https://pypi.org) → Your projects → `pywats` → Settings → Publishing
2. Remove old trusted publisher (olreppe/pyWATS)
3. Add new trusted publisher:
   - Owner: `COMPANY-ORG`
   - Repository: `pyWATS`
   - Workflow: `publish.yml`

### 3. Archive Old Repository
On the old `olreppe/pyWATS` repository:
1. Go to **Settings → General**
2. Scroll to **Danger Zone**
3. Click **Archive this repository**

This makes it read-only while preserving it for reference.

### 4. Update Local Remote
After migration, update your local working copy:

```powershell
cd "c:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"

# Option A: Replace origin
git remote set-url origin https://github.com/COMPANY-ORG/pyWATS.git

# Option B: Keep both remotes
git remote rename origin personal
git remote add origin https://github.com/COMPANY-ORG/pyWATS.git
git fetch origin
git branch --set-upstream-to=origin/main main
```

### 5. Update Documentation
Search and replace repository URLs in:
- [ ] `README.md`
- [ ] `pyproject.toml` (if URLs specified)
- [ ] `docs/` folder
- [ ] Any hardcoded GitHub links

---

## Migration Checklist

### Before Migration
- [ ] Company org name and repo URL confirmed
- [ ] Personal Access Token created
- [ ] Empty repository created in company org
- [ ] Decided on migration option (A, B, or C)

### During Migration
- [ ] Added company remote
- [ ] Pushed main branch
- [ ] Pushed all tags
- [ ] Verified push completed successfully

### After Migration
- [ ] PyPI trusted publishing reconfigured
- [ ] CI/CD workflows tested
- [ ] Local remote updated
- [ ] Old repository archived
- [ ] Documentation URLs updated
- [ ] Team notified of new repository location

---

## Troubleshooting

### "Permission denied" when pushing
- Verify PAT has correct permissions
- Ensure you're using PAT as password, not GitHub password
- Check repository exists and you have write access

### "Repository not found"
- Verify the URL is correct
- Ensure the repository exists (not just the organization)
- Check you're authenticated with the correct account

### Credential caching issues
```powershell
# Clear cached credentials
git credential reject
protocol=https
host=github.com

# Or use credential manager
git config --global credential.helper manager
```

---

## References

- [GitHub: Duplicating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/duplicating-a-repository)
- [GitHub: Managing remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories)
- [PyPI: Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [git-filter-repo](https://github.com/newren/git-filter-repo)

---

*Last updated: January 25, 2026*
