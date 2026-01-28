# GitHub Enterprise Token Setup

**For:** Automated sync in GitHub Actions publish workflow  
**Required:** GHE_TOKEN secret in GitHub repository

---

## Create Personal Access Token on GHE

1. Navigate to GitHub Enterprise: https://wats.ghe.com
2. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Click **Generate new token** → **Generate new token (classic)**
4. Configure token:
   - **Note:** "GitHub Actions - pyWATS sync"
   - **Expiration:** 1 year (or No expiration for service accounts)
   - **Scopes:** Select:
     - ✅ `repo` (Full control of private repositories)
       - Includes: repo:status, repo_deployment, public_repo, repo:invite, security_events

5. Click **Generate token**
6. **Copy the token immediately** (you won't see it again!)

---

## Add Token to GitHub Repository

1. Go to GitHub (public): https://github.com/olreppe/pyWATS
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Configure:
   - **Name:** `GHE_TOKEN`
   - **Secret:** Paste the token from GHE
5. Click **Add secret**

---

## Verify Configuration

After adding the token, the next release will automatically sync to GHE:

```yaml
# Workflow runs on tag push:
git tag -a v0.1.0b39 -m "Release 0.1.0b39"
git push origin main --tags
```

The workflow will:
1. ✅ Build package
2. ✅ Publish to PyPI
3. ✅ Push main branch to GHE
4. ✅ Push all tags to GHE

---

## Token Permissions

The token needs:
- **Push access** to `https://wats.ghe.com/WATS/pyWATS`
- **Branch protection bypass** (if main branch is protected on GHE)

---

## Token Rotation

**When to rotate:**
- Every 12 months (best practice)
- If token is compromised
- When team member with token access leaves

**How to rotate:**
1. Create new token on GHE (same steps as above)
2. Update `GHE_TOKEN` secret on GitHub
3. Revoke old token on GHE
4. Test with next release

---

## Troubleshooting

### Authentication Failed

**Error:** `fatal: Authentication failed`

**Solution:**
1. Verify token has `repo` scope
2. Verify token hasn't expired
3. Verify you have push access to GHE repository
4. Regenerate token if necessary

### Push Rejected

**Error:** `[remote rejected]`

**Solutions:**
- Check if main branch is protected on GHE
- Verify token user has bypass permissions
- Check repository permissions on GHE

### No Sync Job Running

**Error:** Job skipped or not visible

**Solutions:**
- Verify `GHE_TOKEN` secret exists (exact name)
- Check workflow succeeded (sync only runs after successful PyPI publish)
- Review Actions logs for error details

---

## Security Best Practices

✅ **Use fine-grained tokens when available** (more secure than classic)  
✅ **Set expiration dates** (force regular rotation)  
✅ **Limit scope to minimum required** (`repo` only)  
✅ **Use service account** (not personal account) if available  
✅ **Audit token usage** regularly in GHE settings  
✅ **Revoke immediately** if compromised

---

## Alternative: Deploy Keys

For production, consider using deploy keys instead of PAT:

1. Generate SSH key pair:
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-pywats-sync"
   ```

2. Add public key to GHE repository deploy keys (with write access)
3. Add private key as GitHub secret: `GHE_DEPLOY_KEY`
4. Update workflow to use SSH instead of HTTPS

**Benefits:**
- More secure (key-based auth)
- No expiration
- Repository-scoped
- Can't be used for other repos

---

## Workflow Configuration

Current workflow at: [.github/workflows/publish.yml](.github/workflows/publish.yml)

```yaml
sync-to-ghe:
  name: Sync to GitHub Enterprise
  needs: build-and-publish
  env:
    GHE_TOKEN: ${{ secrets.GHE_TOKEN }}
```

---

**Last Updated:** 2026-01-27  
**Owner:** WATS Development Team
