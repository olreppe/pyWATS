# Contributing to PyWATS

> **Project Attribution**: PyWATS was designed and implemented by **Ola Lund Reppe** (Integration Architect, The WATS Company AS) using AI-assisted development.

## Changelog Management

PyWATS uses a **split changelog** structure to keep the main changelog readable:

| File | Purpose |
|------|---------|
| `CHANGELOG.md` | Current/upcoming changes only |
| `CHANGELOG-BETA.md` | Archived beta version history |
| `MIGRATION.md` | Detailed migration examples for breaking changes |

### Adding Changelog Entries

1. **Add entries to `[Unreleased]` section in `CHANGELOG.md`**
2. **Keep entries concise** - one line per change, no code blocks
3. **For breaking changes**, add a link to MIGRATION.md:
   ```markdown
   - `SomeMethod()` removed - Use `NewMethod()` ([migration](MIGRATION.md#section))
   ```
4. **Add detailed migration examples to `MIGRATION.md`** (with code blocks)

### Entry Format

```markdown
### Added
- `ClassName` - Brief description of what it does

### Changed  
- **Feature name** - What changed and why

### Removed (Breaking)
- `removed_method()` - Use `replacement()` ([migration](MIGRATION.md#section))

### Fixed
- Brief description of bug fix
```

### When Releasing

1. Change `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`
2. Add new empty `[Unreleased]` section at top
3. Keep only recent releases in main CHANGELOG (archive old ones to CHANGELOG-BETA.md)

### What NOT to Do

- ❌ Don't add code blocks to CHANGELOG.md (put them in MIGRATION.md)
- ❌ Don't add migration examples to CHANGELOG.md
- ❌ Don't duplicate content between files
- ❌ Don't add entries to CHANGELOG-BETA.md (it's an archive)

## Code Style

- Python 3.10+ with type hints
- Pydantic models for data validation
- `pywats` = memory-only (no file I/O)
- `pywats_client` = file operations allowed
