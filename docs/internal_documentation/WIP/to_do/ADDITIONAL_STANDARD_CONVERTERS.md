# Additional Standard Converters - Implementation Plan

**Created:** 2026-01-26  
**Updated:** 2026-01-26  
**Status:** 🔄 In Progress  
**Priority:** Medium (extends platform compatibility)  
**Estimated Effort:** Varies by converter

---

## Executive Summary

This document tracks implementation of converters for industry-standard electronics test formats identified in the [Electronics Test Log Formats Scan](../ideas/electronics_test_log_formats_and_standards_scan.md).

### Current Converter Status

| Format | Status | File | Notes |
|--------|--------|------|-------|
| IEEE ATML (1671/1636.1) | ✅ Implemented | `atml_converter.py` (1173 lines) | Supports v2.02, 5.00, 6.01 |
| Teradyne i3070 ICT | ✅ Implemented | `teradyne_ict_converter.py` (803 lines) | Text log format |
| Teradyne Spectrum ICT | ✅ Implemented | `teradyne_spectrum_ict_converter.py` | XML format |
| SPEA Flying Probe | ✅ Implemented | `spea_converter.py` | XML format |
| Seica XML | ✅ Implemented | `seica_xml_converter.py` | XML format |
| XJTAG Boundary Scan | ✅ Implemented | `xjtag_converter.py` | XML format |
| Klippel | ✅ Implemented | `klippel_converter.py` | Acoustic testing |
| **Keysight TestExec SL** | ✅ **Implemented** | `keysight_testexec_sl_converter.py` | Functional test XML |
| ~~STDF/ATDF~~ | ❌ Dropped | - | Semiconductor wafer/die only - out of WATS scope |
| **IPC-CFX Events** | 📋 Architecture Study | See [IPC-CFX Architecture](./IPC_CFX_ARCHITECTURE.md) | Not a converter - event system |

---

## ~~1. STDF Converter (Semiconductor ATE)~~ - DROPPED

### Decision: Out of Scope

**Standard Test Data Format (STDF)** is a de facto standard for semiconductor ATE results but is **not relevant to WATS** because:

- STDF is designed for **die/wafer-level testing** (IC fabrication)
- WATS focuses on **board/assembly-level testing** with serialized units
- STDF tracks wafer maps, bin sorting, die coordinates - not applicable to PCB testing
- Component-level testing has specialized tools (e.g., Yield management systems)

The semiconductor testing domain has different requirements:
- Parts don't have meaningful serial numbers (die on wafer)
- Results are aggregated by lot/wafer/bin
- Different yield analytics needed

**Recommendation:** If semiconductor testing support is ever needed, evaluate dedicated semiconductor yield management systems (YAMAN, PDMA, etc.) rather than extending WATS.

---

## 1. Keysight TestExec SL Converter ✅ IMPLEMENTED

### Status

**✅ COMPLETED** - Implemented as `keysight_testexec_sl_converter.py`

### Overview

**Keysight TestExec SL** (formerly Agilent) is a functional test executive that outputs XML result files. Widely used for PCB/PCBA functional testing.

### Implementation Details

| Property | Value |
|----------|-------|
| **File** | `src/pywats_client/converters/standard/keysight_testexec_sl_converter.py` |
| **Lines** | ~700 |
| **Version** | 1.0.0 |

### Supported Features

- [x] Multiple XML root elements (`TestResults`, `TestExecResults`, `Results`)
- [x] Namespace handling (Keysight, Agilent, or none)
- [x] Header extraction (program, station, operator)
- [x] UUT extraction (serial, part number, revision)
- [x] Test mapping to `NumericLimitStep` and `PassFailStep`
- [x] Test groups mapped to `SequenceCall`
- [x] Summary extraction (status, duration, pass/fail counts)

### Configurable Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `operationTypeCode` | Integer | 20 | WATS operation type code |
| `defaultStation` | String | "TestExec SL" | Station name if not in XML |
| `includePassedMeasurements` | Boolean | true | Include passed test measurements |
| `treatMissingLimitsAsPassFail` | Boolean | true | Tests without limits → pass/fail steps |

### Sample File Sources (for testing)

- Request from Keysight/customers using TestExec SL
- Check Keysight application notes for examples

---

## 2. IPC-CFX Integration - Architecture Decision

### ⚠️ NOT A FILE CONVERTER

**IPC-CFX (IPC-2591)** is fundamentally different from file-based formats:

| Aspect | File Converter | IPC-CFX |
|--------|---------------|---------|
| **Trigger** | File created | AMQP message received |
| **Timing** | Batch | Real-time |
| **Transport** | File system | Message broker |
| **Communication** | One-way | Bidirectional |

### Architecture Investigation

A detailed architecture investigation has been completed:

📄 **[IPC-CFX Architecture Investigation](./IPC_CFX_ARCHITECTURE.md)**

Key findings:
1. CFX should be a **separate integration module** (`pywats_cfx`)
2. It should support **multiple WATS domains** (Report, Asset, Product, Production)
3. Consider as part of a **broader event system** design

### CFX Message Topics Relevant to WATS

| CFX Topic | WATS Domain | Data Flow |
|-----------|-------------|-----------|
| `UnitsTested` | Report | CFX → WATS |
| `UnitsInspected` | Report | CFX → WATS |
| `MaterialsInstalled` | Product (BOM) | CFX ↔ WATS |
| `FaultOccurred` | Asset | CFX → WATS |
| `MaintenancePerformed` | Asset | CFX → WATS |
| `WorkStarted/Completed` | Production | CFX ↔ WATS |

### Recommendation

Implement as a separate project: **pyWATS CFX Integration Module**

| Phase | Description | Effort |
|-------|-------------|--------|
| Phase 1 | Core AMQP infrastructure + TestHandler | 2-3 weeks |
| Phase 2 | Domain handlers (Asset, Product, Production) | 2-3 weeks |
| Phase 3 | Bidirectional integration | 2-3 weeks |
| **Total** | Complete CFX integration | **6-9 weeks** |

See the [detailed architecture document](./IPC_CFX_ARCHITECTURE.md) for implementation proposal.

---

## 4. Additional Formats (Lower Priority)

### 4.1 Keysight i3070 ICT Log

**Status:** ✅ Already implemented as `TeradyneICTConverter`

The i3070 format is the same as Teradyne ICT format (Keysight acquired Agilent's board test business which used similar format to Teradyne).

### 4.2 IEEE 1149.x Boundary Scan Results

**Status:** ⚠️ Partial (via XJTAG converter)

Boundary scan protocols are standardized but result formats are vendor-specific:
- XJTAG: ✅ Implemented
- Teradyne PathFinder: Could add if needed
- JTAG Technologies: Could add if needed

### 4.3 QIF (Quality Information Framework)

**Status:** ❌ Not planned

QIF is primarily for dimensional metrology, not electronics test. Lower priority unless specific customer need.

---

## 3. Implementation Summary

### Completed

| Converter | Status | Date |
|-----------|--------|------|
| Keysight TestExec SL | ✅ Implemented | 2026-01-26 |

### Dropped

| Format | Reason |
|--------|--------|
| STDF/ATDF | Semiconductor wafer/die testing - out of WATS scope |

### Deferred to Separate Project

| Project | Reason |
|---------|--------|
| IPC-CFX Integration | Not a file converter - requires dedicated event system |

---

## 4. Development Guidelines

### Converter Template

All converters should follow the established pattern:

```python
from pywats_client.converters.file_converter import FileConverter
from pywats_client.converters.context import ConverterContext
from pywats_client.converters.models import (
    ConverterSource,
    ConverterResult,
    ValidationResult,
)
from pywats.domains.report.report_models import UUTReport, StepStatus

class NewFormatConverter(FileConverter):
    """
    Converter description.
    
    Format documentation: [link]
    """
    
    name = "New Format Converter"
    version = "1.0.0"
    file_extensions = [".ext"]
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """Validate file is correct format."""
        ...
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """Convert file to UUTReport."""
        ...
```

### Testing Requirements

1. Unit tests with mock data
2. Integration tests with real sample files
3. Edge cases: empty results, errors, multi-site
4. Performance tests for large files

---

## 5. Reference Links

### Standards & Specifications

| Standard | Description | Link |
|----------|-------------|------|
| IEEE 1671 (ATML) | Test markup language framework | https://standards.ieee.org/ieee/1671/4865/ |
| IEEE 1671.1 | ATML Test Descriptions | https://standards.ieee.org/ieee/1671.1/4928/ |
| IEEE 1636.1 | ATML Test Results | https://standards.ieee.org/ieee/1636.1/4776/ |
| IPC-2591 | CFX connectivity standard | https://www.ipc.org/ipc-cfx |

### Vendor Documentation

| Vendor | Product | Documentation |
|--------|---------|---------------|
| Keysight | i3070 ICT | https://www.keysight.com/us/en/assets/9018-07549/user-manuals/9018-07549.pdf |
| Keysight | TestExec SL | https://www.keysight.com/us/en/assets/7018-02229/application-notes/5990-4367.pdf |
| Teradyne | ICT Overview | https://www.teradyne.com/applications/in-circuit-testing/ |
| Teradyne | Boundary Scan | https://www.teradyne.com/scan-pathfinder-ii-faq/ |
| NI | TestStand ATML | https://www.ni.com/docs/en-US/bundle/teststand-atml-toolkit/page/atml-td-standards-146.html |

### Existing Libraries (Reference)

| Library | Language | Format | Link |
|---------|----------|--------|------|
| CFX SDK | C# | IPC-CFX | https://github.com/IPCConnectedFactoryExchange/CFX |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | Implemented Keysight TestExec SL converter | AI Assistant |
| 2026-01-26 | Dropped STDF (out of scope for WATS) | AI Assistant |
| 2026-01-26 | Created IPC-CFX architecture investigation document | AI Assistant |
| 2026-01-26 | Initial plan created from electronics test format scan | AI Assistant |
