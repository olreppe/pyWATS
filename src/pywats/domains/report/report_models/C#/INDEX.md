# 📖 Documentation Index

Welcome to the .NET 8 Core UUT and UUR Report Classes documentation!

## 📄 Documentation Files

### 1. [SUMMARY.md](SUMMARY.md) - **START HERE**
Quick overview of what's included, statistics, and key features.
- Task completion summary
- File statistics
- Key features checklist
- Quick code example

### 2. [QUICK_START.md](QUICK_START.md) - **For Developers**
Practical guide with code examples and usage scenarios.
- Main component overview
- Usage flow examples
- Common scenarios
- Code snippets
- Best practices

### 3. [README.md](README.md) - **Detailed Reference**
Comprehensive documentation of all classes and structure.
- Complete directory structure
- All class descriptions
- Enumeration definitions
- Dependencies
- Usage notes

### 4. [FILE_INVENTORY.md](FILE_INVENTORY.md) - **Complete Listing**
Full inventory of all 52 source files organized by category.
- File-by-file listing
- Categorized by purpose
- Location information
- Source project details

## 🗂️ Folder Structure

```
NET8_UUT_UUR_Classes/
│
├── 📄 INDEX.md              ← You are here
├── 📄 SUMMARY.md            ← Start here for overview
├── 📄 QUICK_START.md        ← Developer quick reference
├── 📄 README.md             ← Detailed documentation
├── 📄 FILE_INVENTORY.md     ← Complete file listing
│
├── 📂 UUTClasses/           (20 files)
│   └── UUT report creation classes
│
├── 📂 UURClasses/           (6 files)
│   └── UUR (repair) report classes
│
├── 📂 Schemas/              (3 files)
│   └── XML schema definitions
│
├── 📂 Core/                 (7 files)
│   ├── 📂 Security/         (3 files)
│   └── Core utilities
│
└── 📂 Statistics/           (5 files)
    └── Test statistics classes
```

## 🎯 Choose Your Path

### "I'm new and want a quick overview"
→ Start with [SUMMARY.md](SUMMARY.md)

### "I want to write code quickly"
→ Go to [QUICK_START.md](QUICK_START.md)

### "I need detailed class information"
→ Read [README.md](README.md)

### "I need to find a specific file"
→ Check [FILE_INVENTORY.md](FILE_INVENTORY.md)

## 🔍 Quick Search

### Looking for UUT report creation?
- Main class: `UUTClasses/UUTReport.cs`
- Steps: `UUTClasses/Step.cs`, `UUTClasses/SequenceCall.cs`
- Tests: `UUTClasses/NumericLimitTest.cs`, `UUTClasses/PassFailTest.cs`, etc.

### Looking for UUR report creation?
- Main class: `UURClasses/UURReport.cs`
- Failures: `UURClasses/Failure.cs`, `UURClasses/FailCodes.cs`
- Parts: `UURClasses/UURPartInfo.cs`

### Looking for enumerations?
- Main file: `Enums.cs`
- Core enums: `Core/Enum.cs`

### Looking for API entry point?
- Main API: `TDM.cs`
- Base class: `Report.cs`

## 📊 Statistics at a Glance

- **Total Files:** 56 (52 C# + 4 docs)
- **UUT Classes:** 20 files
- **UUR Classes:** 6 files
- **Core Infrastructure:** 10 files
- **Schemas:** 3 files
- **Statistics:** 5 files
- **Support Classes:** 8 files

## 🔧 Technology

- **Target:** .NET 8.0
- **Platform:** Windows 10.0.18362.0+
- **Language:** C# 12
- **Namespace:** Virinco.WATS.Interface

## 📞 Quick Reference

### Main Classes
| Purpose | Class | File |
|---------|-------|------|
| API Entry | `TDM` | TDM.cs |
| UUT Report | `UUTReport` | UUTClasses/UUTReport.cs |
| UUR Report | `UURReport` | UURClasses/UURReport.cs |
| Base Report | `Report` | Report.cs |

### Main Enumerations
| Enum | Purpose | File |
|------|---------|------|
| `UUTStatusType` | Test result status | Enums.cs |
| `StepStatusType` | Step result status | Enums.cs |
| `TestModeType` | API test mode | Enums.cs |
| `ValidationModeType` | Validation behavior | Enums.cs |

### Step Types
| Type | Purpose | File |
|------|---------|------|
| `NumericLimitStep` | Numeric measurements | UUTClasses/NumericLimitStep.cs |
| `PassFailStep` | Boolean tests | UUTClasses/PassFailStep.cs |
| `StringValueStep` | String comparisons | UUTClasses/StringValueStep.cs |
| `SequenceCall` | Test sequences | UUTClasses/SequenceCall.cs |
| `GenericStep` | Custom steps | UUTClasses/GenericStep.cs |

## 🚀 Get Started in 3 Steps

1. **Read** [SUMMARY.md](SUMMARY.md) - Understand what you have
2. **Study** [QUICK_START.md](QUICK_START.md) - Learn the patterns
3. **Reference** [README.md](README.md) - Deep dive as needed

## 💡 Pro Tips

- All classes use the `Virinco.WATS.Interface` namespace
- Report creation uses a fluent/builder pattern
- Steps are hierarchical - use SequenceCall for structure
- Validation can throw exceptions or auto-truncate
- Reports can be submitted online or queued offline

---

**Last Updated:** January 30, 2026  
**Documentation Version:** 1.0  
**Status:** ✅ Complete and Ready to Use
