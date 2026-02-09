# Report Object Models - Complete Class Diagrams

**Comprehensive class diagrams for WATS report structures**

**Generated:** February 8, 2026  
**Author:** Auto-generated from source code analysis

---

## 📚 Available Resources

### Class Reference (Text-Based List) 📝

#### [Report Class Reference](REPORT_CLASS_REFERENCE.md) ⭐
**Complete class signatures for all report-related classes**

Simple, compact list including:
- All 34 classes in the Report→UUT/UUR hierarchy
- Complete method and property signatures
- Inheritance relationships
- Usage examples and quick reference structures

**Use for:** API reference, code completion, understanding class interfaces

---

## 📊 Available Diagrams

### Comprehensive Diagrams (Single Large Diagram)

#### [UUTReport Object Model](UUT_OBJECT_MODEL.md) ⭐
**Unit Under Test (Test Report)**

Complete class diagram showing:
- UUTReport hierarchy (Report → UUTReport)
- Step types (SequenceCall, NumericStep, PassFailStep, etc.)
- Measurement classes (NumericMeasurement, BooleanMeasurement, StringMeasurement)
- UUTInfo with test-specific fields
- Supporting classes (Asset, BinaryData, Attachment, Chart)

**Use for:** Understanding test report structure, step hierarchies, and test data organization

---

#### [UURReport Object Model](UUR_OBJECT_MODEL.md) ⭐
**Unit Under Repair (Repair Report)**

Complete class diagram showing:
- UURReport hierarchy (Report → UURReport)
- UURSubUnit with failure tracking
- UURFailure records
- UURInfo with dual process codes and UUT linking
- Repair-specific workflows

**Use for:** Understanding repair report structure, failure tracking, and UUT-UUR relationships

---

### Printable Diagrams (Multiple Small Diagrams) 🖨️

#### [UUTReport Printable Diagrams](UUT_OBJECT_MODEL_PRINTABLE.md) 📄
**Broken into 7 separate diagrams, one per page**

1. Core report structure
2. UUTInfo & sub-units
3. Assets & binary data
4. Step base & SequenceCall
5. Measurement steps
6. Other step types
7. Measurement classes

**Includes:** Export instructions for PNG/SVG/PDF

---

#### [UURReport Printable Diagrams](UUR_OBJECT_MODEL_PRINTABLE.md) 📄
**Broken into 8 separate diagrams, one per page**

1. Core repair report
2. Dual process codes (visual)
3. UURInfo structure
4. UURSubUnit hierarchy
5. Sub-unit hierarchy example
6. UURFailure structure
7. UUT-UUR linking flow
8. Assets & supporting data

**Includes:** Export instructions for PNG/SVG/PDF

---

## 🔍 Quick Comparison

| Aspect | UUTReport | UURReport |
|--------|-----------|-----------|
| **Purpose** | Document test execution | Document repair activities |
| **Type Code** | "T" | "R" |
| **Has Test Steps** | ✅ Yes (SequenceCall hierarchy) | ❌ No |
| **Has Failures** | ❌ No (inferred from steps) | ✅ Yes (UURFailure list) |
| **Process Code** | Single (test operation) | Dual (repair + test ops) |
| **Sub-Units** | UUTSubUnit (optional test steps) | UURSubUnit (idx-based hierarchy) |
| **Info Class** | UUTInfo (fixture, socket, batch) | UURInfo (ref_uut, work order, RMA) |
| **Main Use Case** | Production testing, EOL, PCBA | Repair, rework, RMA processing |

---

## 📖 Class Diagram Features

### What's Included (All Public Members)

✅ **Properties** - All public fields with types  
✅ **Methods** - All public methods with signatures  
✅ **Inheritance** - Complete class hierarchy  
✅ **Relationships** - Composition, aggregation, associations  
✅ **Enums** - All enumeration types  
✅ **Generics** - Generic type parameters shown  

### What's Excluded (Private Implementation)

❌ Private fields (prefixed with `_`)  
❌ Internal helper methods  
❌ Pydantic validators (validation logic)  
❌ Serialization details  

---

## 🎯 Usage Scenarios

### When to Use UUTReport

```python
# Production testing
uut = UUTReport(
    pn="WIDGET-001",
    sn="SN123456",
    process_code=100,  # End of Line Test
    station_name="Station1",
    location="Factory",
    purpose="Production"
)

# Add test steps
root = uut.root
root.add_numeric_step("Voltage", 5.0, CompOp.GELE, 4.5, 5.5, "V")
root.add_boolean_step("LED Test", True)

# Submit
await api.report.submit_uut(uut)
```

### When to Use UURReport

```python
# Repair documentation
uur = UURReport(
    pn="WIDGET-001",
    sn="SN123456",
    process_code=500,  # Repair operation
    station_name="RepairStation",
    location="Lab",
    purpose="Repair"
)

# Link to failed test
uur.info.ref_uut = failed_uut_id
uur.info.process_code = 100  # Test that was running

# Document failures
main = uur.get_main_unit()
main.add_failure("Component", "CAP_FAIL", "C12 failed", com_ref="C12")

# Submit
await api.report.submit_uur(uur)
```

---

## 🏗️ Architecture Insights

### Shared Base: Report Class

Both UUTReport and UURReport inherit from the generic `Report<SubUnitT>` base class:

```python
class Report(Generic[SubUnitT]):
    # Common fields
    id: UUID
    pn: str
    sn: str
    rev: str
    process_code: int
    result: ReportResult
    station_name: str
    location: str
    purpose: str
    # ... etc
```

**Benefits of inheritance:**
- Code reuse (validation, serialization)
- Consistent API interface
- Type safety via generics
- Polymorphic handling in APIs

### Type Safety via Generics  

```python
# UUTReport uses UUTSubUnit
class UUTReport(Report[UUTSubUnit]):
    sub_units: List[UUTSubUnit]

# UURReport uses UURSubUnit  
class UURReport(Report[UURSubUnit]):
    sub_units: List[UURSubUnit]
```

This ensures type safety: can't accidentally add UURSubUnit to UUTReport!

---

## 📐 Diagram Legend

### Mermaid Class Diagram Symbols

```
┌─────────────┐
│  ClassName  │  Regular class
└─────────────┘

┌─────────────┐
│<<abstract>> │  Abstract class (cannot instantiate)
│  ClassName  │
└─────────────┘

┌─────────────┐
│<<enumeration>>  Enumeration type
│  EnumName   │
└─────────────┘

┌─────────────┐
│<<Generic>>  │  Generic class with type parameter
│  Class~T~   │
└─────────────┘
```

### Relationship Types

- `<|--` Inheritance (is-a)
- `-->` Association/Composition (has-a)
- `..>` Dependency (uses)

### Member Visibility

- `+` Public (included in diagrams)
- `-` Private (excluded from diagrams)
- `*` Abstract method
- `$` Static method

---

## 🔗 Related Documentation

### Domain Guides
- [Report Domain Guide](../../guides/report-domain.md) - Comprehensive usage guide
- [Repair Workflow Guide](../../guides/repair-workflow.md) - UUT → UUR workflow
- [Step Types Reference](../../guides/step-types.md) - All step types explained

### API Reference
- [Complete Class Reference](class_reference/pywats_api_complete.md) - All API classes
- [Report Domain Reference](class_reference/domain_report.md) - Report domain classes
- [Sphinx API Docs](README.md) - Auto-generated API documentation

### Architecture
- [API-Client-UI Communication Analysis](../../projects/active/api-client-ui-communication-analysis.project/README.md)
- [Architecture Patterns](../../guides/architecture.md)

### Examples
- [UUT Report Examples](../../examples/report/) - Working code samples
- [Repair Report Examples](../../examples/report/repair/) - UUR examples

---

## 🛠️ Regenerating Diagrams

These diagrams are manually maintained based on the source code. To update:

1. **Analyze Source Code:**
   ```powershell
   # Generate class reference (auto-extracts all classes)
   python scripts\generate_class_reference.py
   ```

2. **Update Diagrams:**
   - Review changes in `docs/api/class_reference/domain_report.md`
   - Update Mermaid diagrams in `UUT_OBJECT_MODEL.md` and `UUR_OBJECT_MODEL.md`
   - Add new classes, properties, methods

3. **Validate:**
   - Ensure Mermaid syntax is correct (view in VS Code or GitHub)
   - Cross-reference with actual source code
   - Test example code snippets

---

## 📝 Changelog

| Date | Change | Diagrams Updated |
|------|--------|------------------|
| 2026-02-08 | Initial creation with complete class diagrams | UUT, UUR |
| 2026-02-08 | Added usage examples and comparison table | README |

---

**Maintained by:** Development Team  
**Location:** `docs/api/`  
**Format:** Markdown with Mermaid class diagrams
