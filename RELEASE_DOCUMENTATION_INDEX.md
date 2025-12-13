# pyWATS Release Documentation Index

This index helps you navigate all the release-related documentation.

## 📋 Documentation Overview

All documentation for releasing pyWATS as separate pip packages has been created. Use this index to find what you need.

---

## 🚀 Quick Start (Start Here!)

**File**: [`QUICK_START_RELEASE.md`](QUICK_START_RELEASE.md)

**Use when**: You want to release packages NOW and need a condensed guide.

**Contains**:
- TL;DR release commands
- Prerequisites checklist
- Step-by-step release process
- Quick troubleshooting
- Essential file locations

**Time to read**: 5-10 minutes

---

## 📦 Understanding the Packages

**File**: [`PACKAGE_OVERVIEW.md`](PACKAGE_OVERVIEW.md)

**Use when**: You need to understand what each package does and which one to use.

**Contains**:
- Description of all 4 packages (pywats, pywats-client-service, pywats-client-headless, pywats-client-gui)
- Comparison matrix
- Use case examples
- Installation decision tree
- System requirements
- FAQ

**Time to read**: 10-15 minutes

---

## 📖 Complete Release Guide

**File**: [`RELEASE_GUIDE.md`](RELEASE_GUIDE.md)

**Use when**: You want comprehensive documentation on the release process.

**Contains**:
- Complete package structure explanation
- Prerequisites setup
- Pre-release checklist
- Build process
- Testing procedures
- TestPyPI and PyPI upload
- Post-release tasks
- Troubleshooting guide
- Automation suggestions

**Time to read**: 20-30 minutes

---

## ✅ Detailed Checklist

**File**: [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)

**Use when**: You're actually performing a release and need to track progress.

**Contains**:
- Complete checklist template (copy for each release)
- Pre-release tasks
- Build phase checklist
- Testing phase checklist
- TestPyPI phase checklist
- PyPI release phase checklist
- Post-release tasks
- Rollback plan
- Sign-off sections

**Time to read**: Reference document (use during release)

---

## 📝 TODO List

**File**: [`TODO_FOR_RELEASE.md`](TODO_FOR_RELEASE.md)

**Use when**: You want to see what's done and what remains before first release.

**Contains**:
- Completed tasks (✅)
- Remaining tasks with priorities (HIGH/MEDIUM/LOW)
- Version management tasks
- Testing requirements
- Platform testing checklist
- PyPI account setup
- Questions to answer
- Priority summary

**Time to read**: 10-15 minutes

---

## 🔄 Migration Guide

**File**: [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md)

**Use when**: Users need to migrate from monorepo to packages, or you need to communicate changes.

**Contains**:
- Before/after comparison
- Migration steps for end users
- Migration steps for developers
- Code compatibility information
- Common migration scenarios
- Platform-specific updates (Docker, systemd, etc.)
- Benefits of migration

**Audience**: End users and developers using pyWATS

**Time to read**: 15-20 minutes

---

## 📦 Package-Specific Documentation

### Core API Library
**Location**: [`packages/pywats/`](packages/pywats/)
- `README.md` - Installation, usage, examples
- `CHANGELOG.md` - Version history
- `pyproject.toml` - Package configuration
- `MANIFEST.in` - Package contents

### Client Service Framework
**Location**: [`packages/pywats-client-service/`](packages/pywats-client-service/)
- `README.md` - Service framework documentation
- `CHANGELOG.md` - Version history
- `pyproject.toml` - Package configuration
- `MANIFEST.in` - Package contents

### Headless Client
**Location**: [`packages/pywats-client-headless/`](packages/pywats-client-headless/)
- `README.md` - CLI and HTTP API documentation
- `CHANGELOG.md` - Version history
- `pyproject.toml` - Package configuration
- `MANIFEST.in` - Package contents

### GUI Client
**Location**: [`packages/pywats-client-gui/`](packages/pywats-client-gui/)
- `README.md` - Desktop GUI documentation
- `CHANGELOG.md` - Version history
- `pyproject.toml` - Package configuration
- `MANIFEST.in` - Package contents

---

## 🛠️ Scripts

**Location**: [`scripts/`](scripts/)

All scripts are executable bash scripts (Linux/macOS) that also work on Windows with Git Bash or WSL.

### Build Script
**File**: `scripts/build_all_packages.sh`
- Builds all 4 packages
- Creates wheels and source distributions
- Shows build summary

**Usage**: `bash scripts/build_all_packages.sh`

### Test Installation Script
**File**: `scripts/test_local_install.sh`
- Creates temporary virtual environment
- Installs packages locally
- Tests imports and CLI
- Cleans up

**Usage**: `bash scripts/test_local_install.sh`

### TestPyPI Upload Script
**File**: `scripts/upload_to_testpypi.sh`
- Uploads all packages to TestPyPI
- Shows TestPyPI URLs for verification
- Provides test installation command

**Usage**: `bash scripts/upload_to_testpypi.sh`

### PyPI Release Script
**File**: `scripts/release_to_pypi.sh`
- Confirms you're ready to release
- Checks packages before upload
- Uploads to production PyPI
- Shows PyPI URLs

**Usage**: `bash scripts/release_to_pypi.sh`

---

## 📄 Legal & Licensing

**File**: [`LICENSE`](LICENSE)

**Type**: MIT License

**Copyright**: Virinco

All packages reference this central LICENSE file.

---

## 🗂️ Configuration Files

### Package Configurations
- `packages/*/pyproject.toml` - Package metadata and dependencies
- `packages/*/MANIFEST.in` - Files to include in distribution

### Repository Configuration
- `.gitignore` - Updated with package build artifacts
- Root `pyproject.toml` - May need updating for monorepo compatibility

---

## 📚 Additional Resources

### Existing Documentation (Referenced)
- `README.md` (root) - Main project README (may need updating)
- `docs/ARCHITECTURE.md` - System architecture
- `docs/usage/` - Module usage guides
- `src/pywats_client/control/HEADLESS_GUIDE.md` - Headless operation
- `src/pywats_client/GUI_CONFIGURATION.md` - GUI configuration

### External Resources
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Documentation](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

## 🎯 How to Use This Documentation

### For First-Time Release Manager
1. Read [`QUICK_START_RELEASE.md`](QUICK_START_RELEASE.md) - Get oriented
2. Read [`PACKAGE_OVERVIEW.md`](PACKAGE_OVERVIEW.md) - Understand packages
3. Review [`TODO_FOR_RELEASE.md`](TODO_FOR_RELEASE.md) - Check remaining tasks
4. Read [`RELEASE_GUIDE.md`](RELEASE_GUIDE.md) - Learn full process
5. Use [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) - During actual release

### For Quick Release (After First Time)
1. Update version numbers and CHANGELOGs
2. Follow [`QUICK_START_RELEASE.md`](QUICK_START_RELEASE.md)
3. Use [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) template

### For Users Migrating to Packages
1. Share [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md)
2. Point to [`PACKAGE_OVERVIEW.md`](PACKAGE_OVERVIEW.md) for package selection
3. Direct to package-specific READMEs for installation

### For Understanding Package Structure
1. Read [`PACKAGE_OVERVIEW.md`](PACKAGE_OVERVIEW.md)
2. Review package-specific READMEs in `packages/*/README.md`
3. Check dependency relationships in `pyproject.toml` files

---

## 📊 Documentation Status

| Document | Status | Last Updated | Audience |
|----------|--------|--------------|----------|
| QUICK_START_RELEASE.md | ✅ Complete | Current | Release Manager |
| RELEASE_GUIDE.md | ✅ Complete | Current | Release Manager |
| RELEASE_CHECKLIST.md | ✅ Complete | Current | Release Manager |
| TODO_FOR_RELEASE.md | ✅ Complete | Current | Release Manager |
| PACKAGE_OVERVIEW.md | ✅ Complete | Current | Everyone |
| MIGRATION_GUIDE.md | ✅ Complete | Current | End Users |
| packages/*/README.md | ✅ Complete | Current | Package Users |
| packages/*/CHANGELOG.md | ✅ Complete | Current | Package Users |
| LICENSE | ✅ Complete | Current | Everyone |
| Scripts | ✅ Complete | Current | Release Manager |

---

## ❓ Common Questions

**Q: Where do I start?**  
A: Read [`QUICK_START_RELEASE.md`](QUICK_START_RELEASE.md)

**Q: What packages exist?**  
A: See [`PACKAGE_OVERVIEW.md`](PACKAGE_OVERVIEW.md)

**Q: How do I do a complete release?**  
A: Follow [`RELEASE_GUIDE.md`](RELEASE_GUIDE.md) and [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)

**Q: What needs to be done before first release?**  
A: Check [`TODO_FOR_RELEASE.md`](TODO_FOR_RELEASE.md)

**Q: How do users migrate?**  
A: Share [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md)

**Q: Where are the build scripts?**  
A: In [`scripts/`](scripts/) directory

**Q: What version should I use?**  
A: See version management section in [`TODO_FOR_RELEASE.md`](TODO_FOR_RELEASE.md)

---

## 🔄 Keeping Documentation Updated

After each release:
- [ ] Update CHANGELOGs with release date
- [ ] Update version numbers in examples
- [ ] Check all links still work
- [ ] Update RELEASE_CHECKLIST.md if process changed
- [ ] Note lessons learned in TODO_FOR_RELEASE.md

---

## 📞 Support

For questions about the release process:
- Review this documentation first
- Check GitHub issues: https://github.com/olreppe/pyWATS/issues
- Consult Python Packaging Guide: https://packaging.python.org/

---

## Summary

All release documentation is complete and ready to use:

✅ **Quick Start Guide** - For fast releases  
✅ **Complete Guide** - For detailed understanding  
✅ **Checklists** - For tracking progress  
✅ **Package Docs** - For users  
✅ **Migration Guide** - For existing users  
✅ **Scripts** - For automation  
✅ **Legal** - LICENSE file created

**You have everything you need to release pyWATS packages to PyPI!** 🎉
