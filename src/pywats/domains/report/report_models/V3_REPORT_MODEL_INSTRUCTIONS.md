# Report Models v3 - Requirements & Design Brief

## Original Requirements

We need to do a third try on getting the report models right.

I have created a directory report_models_v3:

1. Use the same strategy by making the v3 a coexising version of the report modelling:

2. Previsously I required that the user facing interface was completely unchanged from the v1-variant. In this approach I'm willing to make small adjustments to this if they a) provide a logical (for the user) syntax. b) improves the design/architecture. c) the outputted json and report creation functionallitys and abilities remain the same

3. Strive for a clean preferably inherrited architecture but you will probably have to mix patterns to get this right. Finding the right mix is core for this. There are several concepts that actually are inherited byt the original design (c# and the v1 python are both somewhat flawed and influenced by new functions being patched on top). A solution that is architecturally perfect on the surface, and that corrects to fit the expected jason in the back end could be a solution by configuring / overriding serialization but that might increase maintanace. That said, this part oif the api has been unchanged for a long time.

4. Analyze the C# code included in the /C# folder to see exacly how the C# code solves this. Keep in mind that this works on a WRML backend that is different from our JSON backend. Also look at the v1 and v2 documentation to understand the previous ideas and what we need from the v3. I am not happy with the mixin solution in v2.

5. Make a implementation plan for v3 and a architectural desription that explains the design and lists the strengts and weaknesses. Also asses the surface diff from v1.

---

## Key Insight (Updated 2026-01-30)

**The current `report_models/` IS v1** (just not labeled). The v3 goal is to be the **"correct" implementation of v1** - fixing architectural issues while:

1. **Preserving C# factory methods** - `add_numeric_step()`, `add_sequence_call()` stay on SequenceCall
2. **Also allowing constructors** - Steps can be created directly, then added to sequences
3. **Maintaining hierarchical SequenceCall structure** - Parent injection, step trees
4. **Same JSON output format** - API compatibility is non-negotiable
5. **Fixing C# design flaws** that were carried over to Python v1

---

## Quick Reference

### Document Index
- **[ARCHITECTURE_ANALYSIS.md](ARCHITECTURE_ANALYSIS.md)** - Full technical analysis (START HERE)
- **[C#/INDEX.md](C#/INDEX.md)** - C# reference code documentation
- **[C#/QUICK_START.md](C#/QUICK_START.md)** - C# usage patterns

### Key Classes to Implement

| Class | Purpose | C# Equivalent |
|-------|---------|---------------|
| `UUTReport` | Test report container | `UUTReport.cs` |
| `SequenceCall` | Step container with factories | `SequenceCall.cs` |
| `NumericLimitStep` | Numeric measurement step | `NumericLimitStep.cs` |
| `PassFailStep` | Boolean pass/fail step | `PassFailStep.cs` |
| `StringValueStep` | String comparison step | `StringValueStep.cs` |
| `GenericStep` | Flow control, actions | `GenericStep.cs` |

### Factory Method Mapping (C# → Python v3)

```python
# C# Pattern:
# uut.GetRootSequenceCall().AddNumericLimitStep("Test").AddTest(5.0, 4.5, 5.5, "V")

# Python v3 Pattern (same as v1):
root = report.get_root_sequence_call()
root.add_numeric_step(name="Test", value=5.0, low_limit=4.5, high_limit=5.5, unit="V")

# Python v3 Two-Step Pattern (NEW - matches C# more closely):
step = root.add_numeric_limit_step("Test")
step.add_test(value=5.0, low_limit=4.5, high_limit=5.5, unit="V", comp_op=CompOp.GELE)
```

---

## Implementation Status

- [ ] Phase 1: Core Infrastructure (base classes, enums)
- [ ] Phase 2: Step Classes (SequenceCall, NumericLimitStep, etc.)
- [ ] Phase 3: Report Classes (UUTReport, UURReport)
- [ ] Phase 4: Serialization & Validation
- [ ] Phase 5: Integration & Testing