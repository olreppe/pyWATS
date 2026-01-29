# Report Model Redesign Specification

**Status:** Planning / To-Do  
**Target Version:** 0.3.0  
**Breaking Changes:** Yes (major architectural refactor)  
**Estimated Effort:** 3-5 days development + 2 days testing  
**Priority:** Medium (type safety & maintainability improvement)

---

## Executive Summary

Redesign the Report model architecture (UUTReport/UURReport) using **Pydantic v2 discriminated unions**, **composition over inheritance**, and **strongly-typed field patterns**. This eliminates type-checking issues, improves API clarity, and aligns with best practices demonstrated in the Step discriminated union pattern.

**Key Goals:**
1. Eliminate `Optional[list[T]]` pattern causing unnecessary None checks
2. Fix inheritance-based field type overrides (Report.info vs UUTReport.info vs UURReport.uur_info)
3. Implement discriminated union for UUT/UUR report parsing
4. Preserve 100% JSON serialization compatibility with WATS API
5. Maintain backward compatibility in Python API surface

---

## 1. Current Architecture Problems

### 1.1 Inheritance Type Conflicts

**Current Pattern:**
```python
class Report(WATSBase):
    info: Optional[ReportInfo] = None
    sub_units: Optional[list[SubUnit]] = Field(default_factory=list)

class UUTReport(Report):
    info: Optional[UUTInfo] = Field(...)  # Type override - mypy error
    # sub_units inherited as Optional[list[SubUnit]]

class UURReport(Report):
    uur_info: UURInfo = Field(...)  # Different field name entirely
    sub_units: List[UURSubUnit] = Field(...)  # Type override - mypy error
```

**Problems:**
- UUTReport overrides `info` type from `ReportInfo` to `UUTInfo` (Liskov Substitution Principle violation)
- UURReport uses different field name (`uur_info`) to avoid conflict
- UURReport.sub_units contains `UURSubUnit` (with idx, parentIdx, failures) vs base `SubUnit`
- Type checkers flag these as incompatible overrides
- Requires `# type:ignore[assignment]` comments throughout

### 1.2 Optional[list] Anti-Pattern

**Current Pattern:**
```python
misc_infos: Optional[list[MiscInfo]] = Field(default_factory=list)

def add_misc_info(...):
    if self.misc_infos is None:  # Defensive check
        self.misc_infos = []
    self.misc_infos.append(mi)
```

**Problems:**
- Every adder method needs None check
- Field is never actually None (default_factory ensures empty list)
- Confuses API consumers: "Can this be None?"
- Extra branches in business logic

### 1.3 UUR Dual Process Code Confusion

**Current Pattern:**
```python
class UURReport(Report):
    process_code: int  # Inherited - REPAIR process code
    
class UURInfo(ReportInfo):
    test_operation_code: Optional[int]  # Original test process
    repair_process_code: Optional[int]  # Duplicate of parent?
    process_code: Optional[int]  # API requirement - which one?
```

**Problems:**
- Three different process code fields with unclear semantics
- Top-level `process_code` should be REPAIR process (per C# spec)
- UURInfo should track TEST OPERATION process
- API serialization requires processCode in uur object
- Current implementation doesn't enforce correct values

### 1.4 No Discriminated Union for Parsing

**Current Pattern:**
```python
# Service layer must know report type in advance
report = UUTReport.model_validate(json_data)  # Explicit type
```

**Missing:**
```python
# Cannot parse unknown report type automatically
report: UUTReport | UURReport = Report.parse(json_data)  # Doesn't exist
```

---

## 2. Proposed Architecture

### 2.1 Composition: ReportCommon

Extract shared fields into composable model:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ReportCommon(BaseModel):
    """Shared fields for all report types (composition pattern)."""
    
    id: UUID = Field(default_factory=uuid4)
    pn: str = Field(..., max_length=100, min_length=1)
    sn: str = Field(..., max_length=100, min_length=1)
    rev: str = Field(..., max_length=100, min_length=1)
    
    result: str = Field(default="P", max_length=1, pattern='^[PFDET]$')
    
    station_name: str = Field(
        ..., 
        max_length=100, 
        validation_alias="machineName",
        serialization_alias="machineName"
    )
    location: str = Field(..., max_length=100)
    purpose: str = Field(..., max_length=100)
    
    # Timing (always-present, synchronized)
    start: datetime = Field(default_factory=lambda: datetime.now().astimezone())
    start_utc: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        exclude=True  # Not sent to server
    )
    
    # Collections - NEVER Optional (always list)
    misc_infos: list[MiscInfo] = Field(
        default_factory=list,
        validation_alias="miscInfos",
        serialization_alias="miscInfos"
    )
    assets: list[Asset] = Field(default_factory=list)
    binary_data: list[BinaryData] = Field(
        default_factory=list,
        validation_alias="binaryData",
        serialization_alias="binaryData"
    )
    additional_data: list[AdditionalData] = Field(
        default_factory=list,
        validation_alias="additionalData",
        serialization_alias="additionalData"
    )
    
    # Output-only (from server)
    origin: Optional[str] = Field(default=None, exclude=True)
    product_name: Optional[str] = Field(
        default=None, 
        exclude=True,
        validation_alias="productName"
    )
    process_name: Optional[str] = Field(
        default=None,
        exclude=True, 
        validation_alias="processName"
    )
    
    @model_validator(mode='after')
    def sync_start_times(self) -> 'ReportCommon':
        """Keep start and start_utc synchronized."""
        if self.start.tzinfo is None:
            self.start = self.start.astimezone()
        self.start_utc = self.start.astimezone(timezone.utc)
        return self
    
    model_config = ConfigDict(populate_by_name=True)
```

**Benefits:**
- Single source of truth for shared behavior
- No inheritance conflicts
- Explicit composition relationship
- Validators centralized

### 2.2 UUTReport (Test Report)

```python
from typing import Literal
from pydantic import BaseModel, Field

class UUTReport(BaseModel):
    """Unit Under Test report (type='T')."""
    
    # Discriminator field
    type: Literal["T"] = "T"
    
    # Test operation process code
    process_code: int = Field(
        ...,
        validation_alias="processCode",
        serialization_alias="processCode"
    )
    
    # Composed common fields
    common: ReportCommon
    
    # UUT-specific info
    info: UUTInfo | None = Field(
        default=None,
        validation_alias="uut",
        serialization_alias="uut"
    )
    
    # UUT-specific root step sequence
    root: SequenceCall = Field(default_factory=SequenceCall)
    
    # UUT uses base SubUnit (no idx/parentIdx/failures)
    sub_units: list[SubUnit] = Field(
        default_factory=list,
        validation_alias="subUnits",
        serialization_alias="subUnits"
    )
    
    # =====================================================================
    # Passthrough properties (backward compatibility)
    # =====================================================================
    
    @property
    def id(self) -> UUID:
        return self.common.id
    
    @property
    def pn(self) -> str:
        return self.common.pn
    
    @property
    def sn(self) -> str:
        return self.common.sn
    
    @property
    def rev(self) -> str:
        return self.common.rev
    
    @property
    def result(self) -> str:
        return self.common.result
    
    @result.setter
    def result(self, value: str):
        self.common.result = value
    
    @property
    def station_name(self) -> str:
        return self.common.station_name
    
    @property
    def location(self) -> str:
        return self.common.location
    
    @property
    def purpose(self) -> str:
        return self.common.purpose
    
    @property
    def start(self) -> datetime:
        return self.common.start
    
    @property
    def misc_infos(self) -> list[MiscInfo]:
        return self.common.misc_infos
    
    @property
    def assets(self) -> list[Asset]:
        return self.common.assets
    
    @property
    def binary_data(self) -> list[BinaryData]:
        return self.common.binary_data
    
    # =====================================================================
    # Business methods
    # =====================================================================
    
    def get_root_sequence_call(self) -> SequenceCall:
        """Get main sequence (sets default name if needed)."""
        self.root.name = "MainSequence Callback"
        return self.root
    
    def add_misc_info(self, description: str, value: Any) -> MiscInfo:
        """Add misc info (no None check needed)."""
        mi = MiscInfo(description=description, string_value=str(value))
        self.common.misc_infos.append(mi)
        return mi
    
    def add_sub_unit(self, part_type: str, sn: str, pn: str, rev: str) -> SubUnit:
        """Add sub-unit to report."""
        su = SubUnit(part_type=part_type, sn=sn, pn=pn, rev=rev)
        self.sub_units.append(su)
        return su
    
    model_config = ConfigDict(populate_by_name=True)
```

### 2.3 UURReport (Repair Report)

```python
class UURReport(BaseModel):
    """Unit Under Repair report (type='R')."""
    
    # Discriminator field
    type: Literal["R"] = "R"
    
    # Top-level report process = REPAIR process code
    process_code: int = Field(
        ...,
        validation_alias="processCode",
        serialization_alias="processCode",
        description="Repair process code (RepairType.Code)"
    )
    
    # Composed common fields
    common: ReportCommon
    
    # UUR-specific info (contains test_operation_code)
    uur_info: UURInfo = Field(
        default_factory=UURInfo,
        validation_alias="uur",
        serialization_alias="uur"
    )
    
    # UUR uses extended UURSubUnit (with idx, parentIdx, failures)
    sub_units: list[UURSubUnit] = Field(
        default_factory=list,
        validation_alias="subUnits",
        serialization_alias="subUnits"
    )
    
    # Report-level attachments
    attachments: list[Attachment] = Field(
        default_factory=list,
        validation_alias="binaryData",
        serialization_alias="binaryData"
    )
    
    @model_validator(mode='after')
    def ensure_main_unit(self) -> 'UURReport':
        """Ensure main unit (idx=0) exists."""
        if not self.sub_units or not any(su.idx == 0 for su in self.sub_units):
            main = UURSubUnit.create_main_unit(
                pn=self.common.pn,
                sn=self.common.sn,
                rev=self.common.rev
            )
            self.sub_units.insert(0, main)
        return self
    
    @model_validator(mode='after')
    def sync_process_codes(self) -> 'UURReport':
        """
        Enforce dual process code architecture:
        - Top-level process_code = REPAIR process (what kind of repair)
        - uur_info.test_operation_code = TEST process (original test operation)
        - uur_info.process_code = API requirement (mirrors top-level)
        """
        # Sync uur_info.process_code with top-level repair process
        self.uur_info.process_code = self.process_code
        return self
    
    # =====================================================================
    # Passthrough properties (backward compatibility)
    # =====================================================================
    
    @property
    def id(self) -> UUID:
        return self.common.id
    
    @property
    def pn(self) -> str:
        return self.common.pn
    
    # ... (same pattern as UUTReport)
    
    # =====================================================================
    # UUR-specific properties
    # =====================================================================
    
    @property
    def test_operation_code(self) -> int | None:
        """Original test operation process code."""
        return self.uur_info.test_operation_code
    
    @property
    def repair_process_code(self) -> int:
        """Repair process code (alias for top-level process_code)."""
        return self.process_code
    
    @property
    def ref_uut(self) -> UUID | None:
        """Referenced UUT report GUID."""
        return self.uur_info.ref_uut
    
    # =====================================================================
    # Business methods
    # =====================================================================
    
    def get_main_unit(self) -> UURSubUnit:
        """Get main unit (idx=0)."""
        main = next((su for su in self.sub_units if su.idx == 0), None)
        if not main:
            raise ValueError("Main unit (idx=0) not found")
        return main
    
    def add_sub_unit(
        self, 
        pn: str, 
        sn: str, 
        rev: str = "", 
        part_type: str = "Unknown"
    ) -> UURSubUnit:
        """Add replacement sub-unit."""
        idx = max((su.idx for su in self.sub_units), default=0) + 1
        su = UURSubUnit(
            idx=idx,
            parent_idx=0,  # Single-level hierarchy
            pn=pn,
            sn=sn,
            rev=rev,
            part_type=part_type
        )
        self.sub_units.append(su)
        return su
    
    def add_failure(
        self,
        category: str,
        code: str,
        comment: str | None = None,
        component_ref: str | None = None
    ) -> UURFailure:
        """Add failure to main unit (idx=0)."""
        main = self.get_main_unit()
        return main.add_failure(category, code, comment, component_ref)
    
    model_config = ConfigDict(populate_by_name=True)
```

### 2.4 Discriminated Union for Parsing

```python
from typing import Annotated, Union
from pydantic import Discriminator

def _discriminate_report_type(v: Any) -> str:
    """
    Discriminator function for Report union.
    
    Handles both dict (JSON parsing) and model instances.
    Defaults to 'T' (UUT) if type field missing.
    """
    if isinstance(v, dict):
        return v.get("type", "T")
    return getattr(v, "type", "T")

# Public union type for parsing unknown reports
ReportType = Annotated[
    Union[UUTReport, UURReport],
    Discriminator(_discriminate_report_type),
]

# Usage in service layer:
def parse_report(data: dict[str, Any]) -> UUTReport | UURReport:
    """Parse report from JSON (auto-detects UUT vs UUR)."""
    from pydantic import TypeAdapter
    adapter = TypeAdapter(ReportType)
    return adapter.validate_python(data)
```

---

## 3. JSON Serialization Compatibility

### 3.1 Current JSON Structure (MUST BE PRESERVED)

**UUTReport JSON:**
```json
{
  "type": "T",
  "processCode": 100,
  "pn": "BOARD-001",
  "sn": "SN12345",
  "rev": "A",
  "machineName": "Station1",
  "location": "Line1",
  "purpose": "Production",
  "start": "2026-01-29T10:00:00+01:00",
  "miscInfos": [...],
  "subUnits": [...],
  "uut": {
    "fixtureId": "FIX-001",
    "testSocketIndex": 1
  },
  "root": {
    "stepType": "SEQ",
    "name": "MainSequence",
    "steps": [...]
  }
}
```

**UURReport JSON:**
```json
{
  "type": "R",
  "processCode": 500,
  "pn": "BOARD-001",
  "sn": "SN12345",
  "rev": "A",
  "machineName": "RepairStation",
  "location": "RMA",
  "purpose": "Repair",
  "start": "2026-01-29T11:00:00+01:00",
  "miscInfos": [...],
  "subUnits": [
    {
      "idx": 0,
      "pn": "BOARD-001",
      "sn": "SN12345",
      "rev": "A",
      "partType": "Main",
      "failures": [
        {
          "category": "Component",
          "code": "CAPACITOR_FAIL",
          "comment": "C10 shorted"
        }
      ]
    }
  ],
  "uur": {
    "processCode": 500,
    "testOperationCode": 100,
    "refUUT": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "userLoginName": "john.doe",
    "comment": "Replaced C10"
  }
}
```

### 3.2 Serialization Strategy

**Model Serializer Override:**
```python
from pydantic import model_serializer

class UUTReport(BaseModel):
    # ... fields ...
    
    @model_serializer
    def serialize_model(self) -> dict[str, Any]:
        """Flatten common fields to root level."""
        result = {
            "type": self.type,
            "processCode": self.process_code,
            **self.common.model_dump(
                by_alias=True,
                exclude={'id'}  # Handle separately if needed
            ),
            "uut": self.info.model_dump(by_alias=True) if self.info else None,
            "root": self.root.model_dump(by_alias=True),
            "subUnits": [su.model_dump(by_alias=True) for su in self.sub_units]
        }
        # Remove None values for cleaner JSON
        return {k: v for k, v in result.items() if v is not None}
```

**Deserialization Strategy:**
```python
from pydantic import model_validator

class UUTReport(BaseModel):
    # ... fields ...
    
    @model_validator(mode='before')
    @classmethod
    def extract_common_fields(cls, data: Any) -> dict[str, Any]:
        """Extract common fields into nested common object."""
        if isinstance(data, dict):
            # Build common dict from root-level fields
            common_data = {
                'id': data.get('id'),
                'pn': data.get('pn'),
                'sn': data.get('sn'),
                'rev': data.get('rev'),
                'result': data.get('result', 'P'),
                'machineName': data.get('machineName'),
                'location': data.get('location'),
                'purpose': data.get('purpose'),
                'start': data.get('start'),
                'miscInfos': data.get('miscInfos', []),
                'assets': data.get('assets', []),
                'binaryData': data.get('binaryData', []),
                'additionalData': data.get('additionalData', []),
            }
            
            # Return modified data structure
            return {
                'type': data.get('type', 'T'),
                'processCode': data.get('processCode'),
                'common': common_data,
                'info': data.get('uut'),
                'root': data.get('root', {}),
                'subUnits': data.get('subUnits', [])
            }
        return data
```

### 3.3 Validation Test Cases

**Must pass all existing JSON tests:**
```python
# Test UUT serialization roundtrip
uut = UUTReport(
    process_code=100,
    common=ReportCommon(pn="P1", sn="S1", rev="A", ...),
    ...
)
json_out = uut.model_dump(mode='json', by_alias=True)
assert json_out['processCode'] == 100
assert json_out['pn'] == "P1"  # Flattened from common
assert 'common' not in json_out  # Not in output

# Test UUT deserialization
json_in = {
    "type": "T",
    "processCode": 100,
    "pn": "P1",
    "sn": "S1",
    ...
}
uut2 = UUTReport.model_validate(json_in)
assert uut2.common.pn == "P1"
assert uut2.process_code == 100
```

---

## 4. Migration Strategy - Parallel Implementation

### 4.1 Phase 1: Parallel Directory Structure (Zero Risk)

**IMPORTANT: Understand the existing structure first!**

Current structure has **TWO separate concerns**:
```
src/pywats/domains/report/
├── models.py                   # QUERY MODELS (WATSFilter, ReportHeader, etc.)
│                               # ⚠️ NOT report structure - used for filtering/queries
│                               # These stay unchanged!
│
└── report_models/              # REPORT STRUCTURE MODELS (UUTReport, UURReport)
    ├── __init__.py             # This is what we're refactoring
    ├── report.py               # Base Report class
    ├── misc_info.py            # MiscInfo, etc.
    ├── sub_unit.py             # SubUnit base
    ├── uut/
    │   ├── uut_report.py       # UUTReport implementation
    │   ├── uut_info.py         # UUTInfo
    │   └── steps/              # Step hierarchy (already uses discriminated union!)
    └── uur/
        ├── uur_report.py       # UURReport implementation
        ├── uur_info.py         # UURInfo
        └── uur_sub_unit.py     # UURSubUnit (extended with idx, failures)
```

**Create parallel v2 directory:**

```
src/pywats/domains/report/
├── models.py                   # ✓ UNCHANGED - query models
│
├── report_models/              # ✓ UNCHANGED - v1 report structure
│   ├── __init__.py
│   ├── report.py
│   ├── uut/
│   │   ├── uut_report.py
│   │   └── uut_info.py
│   └── uur/
│       ├── uur_report.py
│       └── uur_info.py
│
└── report_models_v2/           # ✓ NEW - v2 report structure (parallel)
    ├── __init__.py
    ├── report_common.py        # NEW: Shared fields via composition
    ├── uut_report.py           # NEW: Composition-based UUTReport
    ├── uur_report.py           # NEW: Composition-based UURReport
    ├── report_union.py         # NEW: Discriminated union
    │
    ├── shared/                 # Shared models (copy from v1, may be symlinks)
    │   ├── misc_info.py        # Copy from ../report_models/misc_info.py
    │   ├── asset.py            # Copy from ../report_models/asset.py
    │   ├── binary_data.py
    │   ├── additional_data.py
    │   ├── chart.py
    │   └── attachment.py
    │
    ├── uut/
    │   ├── uut_info.py         # Same as v1 (may be symlink or copy)
    │   └── steps/              # ⚠️ REUSE v1 steps (discriminated union already works!)
    │                           # Use relative import: from ...report_models.uut.steps import *
    └── uur/
        ├── uur_info.py         # Same as v1 (may be symlink or copy)
        ├── uur_sub_unit.py     # Same as v1 (may be symlink or copy)
        └── sub_unit.py         # Base SubUnit (from v1)
```

**Critical Notes:**

1. **models.py is NOT involved** - it contains query/filter classes (WATSFilter, ReportHeader), not report structure
2. **Step hierarchy is already good** - uses discriminated union pattern, reuse from v1
3. **Shared models** - Copy small models to v2 or use relative imports from v1
4. **No conflicts** - v1 and v2 are completely isolated directories

**Benefits:**
- Zero risk of breaking existing code
- Can develop/test new models independently
- Easy A/B comparison of outputs
- Can switch between implementations via import path
- Old code continues working during entire development
- No confusion between query models (models.py) and report models (report_models/)

### 4.2 Phase 2: Feature Flag for Testing

**Add environment variable to control which implementation is used:**

```python
# src/pywats/domains/report/__init__.py
import os
from typing import TYPE_CHECKING

# Feature flag: USE_REPORT_V2=1 to enable new models
USE_V2 = os.getenv("USE_REPORT_V2", "0") == "1"

if USE_V2:
    # New composition-based models
    from .report_models_v2 import (
        ReportCommon,
        UUTReport,
        UURReport,
        ReportType,
        parse_report,
    )
else:
    # Old inheritance-based models (current)
    from .report_models import (
        Report,
        UUTReport,
        UURReport,
    )
    # Stub for v2-only features
    ReportType = UUTReport | UURReport  # type: ignore
    parse_report = None

# Always export both for explicit usage
from .report_models import (
    UUTReport as UUTReportV1,
    UURReport as UURReportV1,
)
from .report_models_v2 import (
    UUTReport as UUTReportV2,
    UURReport as UURReportV2,
)

__all__ = [
    "UUTReport",
    "UURReport",
    "UUTReportV1",  # Explicit v1
    "UURReportV2",  # Explicit v2
]
```

**Usage:**
```bash
# Use old models (default)
python script.py

# Use new models
USE_REPORT_V2=1 python script.py
```

### 4.3 Phase 3: Comparison Testing Framework

**Create test utilities to compare v1 vs v2 outputs:**

```python
# tests/report_models/test_v1_v2_comparison.py
import pytest
from pywats.domains.report import UUTReportV1, UUTReportV2
from pywats.domains.report.report_models_v2 import ReportCommon

def normalize_json(data: dict) -> dict:
    """Normalize JSON for comparison (sort keys, handle timestamps)."""
    # Remove server-generated fields
    for key in ['id', 'startUTC', 'origin', 'productName', 'processName']:
        data.pop(key, None)
    return data

class TestUUTReportCompatibility:
    """Compare v1 and v2 UUTReport outputs."""
    
    def test_serialization_identical(self):
        """Verify v1 and v2 produce identical JSON."""
        # Create v1 report (old way)
        v1_report = UUTReportV1(
            pn="BOARD-001",
            sn="SN12345",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="Line1",
            purpose="Production",
        )
        v1_report.add_misc_info("Operator", "John")
        
        # Create v2 report (new way)
        v2_report = UUTReportV2(
            process_code=100,
            common=ReportCommon(
                pn="BOARD-001",
                sn="SN12345",
                rev="A",
                station_name="Station1",
                location="Line1",
                purpose="Production",
            )
        )
        v2_report.add_misc_info("Operator", "John")
        
        # Serialize both
        v1_json = v1_report.model_dump(mode='json', by_alias=True)
        v2_json = v2_report.model_dump(mode='json', by_alias=True)
        
        # Normalize for comparison
        v1_normalized = normalize_json(v1_json)
        v2_normalized = normalize_json(v2_json)
        
        # Compare
        assert v1_normalized == v2_normalized, "JSON output differs!"
    
    def test_deserialization_compatible(self):
        """Verify both can parse same JSON."""
        json_data = {
            "type": "T",
            "processCode": 100,
            "pn": "BOARD-001",
            "sn": "SN12345",
            "rev": "A",
            "machineName": "Station1",
            "location": "Line1",
            "purpose": "Production",
            "miscInfos": [
                {"description": "Operator", "stringValue": "John"}
            ]
        }
        
        # Parse with both
        v1_parsed = UUTReportV1.model_validate(json_data)
        v2_parsed = UUTReportV2.model_validate(json_data)
        
        # Verify fields match
        assert v1_parsed.pn == v2_parsed.pn
        assert v1_parsed.sn == v2_parsed.sn
        assert len(v1_parsed.misc_infos) == len(v2_parsed.misc_infos)

class TestUURReportCompatibility:
    """Compare v1 and v2 UURReport outputs."""
    
    def test_serialization_identical(self):
        """Verify v1 and v2 produce identical UUR JSON."""
        # Similar pattern for UUR...
        pass
```

### 4.4 Phase 4: Integration Testing with Real WATS Server

**Test both implementations against actual WATS API:**

```python
# tests/integration/test_report_submission.py
import pytest
from uuid import uuid4

@pytest.mark.integration
@pytest.mark.parametrize("use_v2", [False, True])
async def test_submit_uut_report(wats_service, use_v2):
    """Submit UUT report using v1 or v2 model."""
    if use_v2:
        from pywats.domains.report import UUTReportV2 as UUTReport
        from pywats.domains.report.report_models_v2 import ReportCommon
        
        report = UUTReport(
            process_code=100,
            common=ReportCommon(
                pn=f"TEST-{uuid4().hex[:8]}",
                sn=f"SN-{uuid4().hex[:8]}",
                rev="A",
                station_name="TestStation",
                location="Lab",
                purpose="Testing",
            )
        )
    else:
        from pywats.domains.report import UUTReportV1 as UUTReport
        
        report = UUTReport(
            pn=f"TEST-{uuid4().hex[:8]}",
            sn=f"SN-{uuid4().hex[:8]}",
            rev="A",
            process_code=100,
            station_name="TestStation",
            location="Lab",
            purpose="Testing",
        )
    
    # Submit to server
    report_id = await wats_service.submit_report(report)
    assert report_id is not None
    
    # Retrieve and verify
    retrieved = await wats_service.get_report(report_id)
    assert retrieved.pn == report.pn
    assert retrieved.sn == report.sn
```

### 4.5 Phase 5: Gradual Cutover

**Once v2 is validated, switch default:**

1. Update `__init__.py` to use v2 by default:
   ```python
   # Default to v2 (can override with USE_REPORT_V1=1)
   USE_V2 = os.getenv("USE_REPORT_V1", "0") != "1"
   ```

2. Add deprecation warnings to v1:
   ```python
   # report_models/__init__.py
   import warnings
   warnings.warn(
       "report_models (v1) is deprecated. Switch to report_models_v2.",
       DeprecationWarning,
       stacklevel=2
   )
   ```

3. Update documentation to recommend v2

4. Keep v1 around for 1-2 minor versions

### 4.6 Phase 6: Remove v1 (Next Major Version)

1. Delete `report_models/` directory
2. Rename `report_models_v2/` → `report_models/`
3. Remove feature flag logic
4. Update version to 0.3.0

### 4.7 Comparison Test Matrix

**Create comprehensive comparison suite:**

| Test Case | V1 Input | V2 Input | Expected | Status |
|-----------|----------|----------|----------|--------|
| UUT Basic Fields | `UUTReport(pn=..., sn=...)` | `UUTReport(common=ReportCommon(...))` | Identical JSON | ✓ |
| UUT with MiscInfos | `add_misc_info()` | `add_misc_info()` | Identical JSON | ✓ |
| UUT with SubUnits | `add_sub_unit()` | `add_sub_unit()` | Identical JSON | ✓ |
| UUT with Steps | `root.add_numeric_step()` | `root.add_numeric_step()` | Identical JSON | ✓ |
| UUR Basic Fields | `UURReport(...)` | `UURReport(common=...)` | Identical JSON | ✓ |
| UUR with Failures | `add_failure()` | `add_failure()` | Identical JSON | ✓ |
| UUR Process Codes | Dual codes | Dual codes | Correct separation | ✓ |
| Parse Unknown Type | N/A | `parse_report(json)` | Auto-detect | ✓ |
| Server Submit | HTTP POST | HTTP POST | Same response | ✓ |
| Server Retrieve | HTTP GET | HTTP GET | Same parsing | ✓ |

### 4.8 Service Layer Compatibility

**Service layer supports both v1 and v2 transparently:**

```python
# src/pywats/domains/report/async_service.py
from typing import Union
from .report_models import UUTReport as UUTReportV1, UURReport as UURReportV1
from .report_models_v2 import UUTReport as UUTReportV2, UURReport as UURReportV2

class AsyncReportService:
    async def submit_report(
        self,
        report: Union[UUTReportV1, UURReportV1, UUTReportV2, UURReportV2, dict]
    ) -> str:
        """
        Submit report (accepts v1, v2, or dict).
        
        Serialization is identical for both versions.
        """
        if isinstance(report, dict):
            json_data = report
        else:
            json_data = report.model_dump(mode='json', by_alias=True)
        
        response = await self._repository.post_wsjf(json_data)
        return response
    
    async def get_report(
        self, 
        report_id: UUID,
        use_v2: bool = None  # Optional: force specific version
    ) -> Union[UUTReportV1, UURReportV1, UUTReportV2, UURReportV2]:
        """Get report (returns v1 or v2 based on feature flag)."""
        from . import USE_V2
        
        response = await self._repository.get_report(report_id)
        json_data = response.json()
        
        # Use v2 by default if enabled, or explicit override
        if use_v2 is None:
            use_v2 = USE_V2
        
        if use_v2:
            from .report_models_v2 import parse_report
            return parse_report(json_data)
        else:
            # V1 requires explicit type
            report_type = json_data.get('type', 'T')
            if report_type == 'T':
                return UUTReportV1.model_validate(json_data)
            else:
                return UURReportV1.model_validate(json_data)
```

---

## 5. Implementation Checklist

### Phase 1: Parallel Structure
- [ ] Verify existing structure (models.py vs report_models/)
- [ ] Create `report_models_v2/` directory
- [ ] Copy shared models to `report_models_v2/shared/` (MiscInfo, Asset, SubUnit, etc.)
- [ ] Set up relative imports for Step hierarchy (reuse v1 steps - already good!)
- [ ] Set up `__init__.py` with feature flag
- [ ] Add comparison test framework
- [ ] Document import strategy (copy vs symlink vs relative import)

### Phase 2: Core Models
- [ ] Create `ReportCommon` model
- [ ] Create `UUTReport` with composition
- [ ] Create `UURReport` with composition
- [ ] Add `ReportType` discriminated union
- [ ] Add `parse_report()` helper function

### Phase 3: Serialization
- [ ] Implement `@model_serializer` for flattening
- [ ] Implement `@model_validator(mode='before')` for extraction
- [ ] Test UUT JSON roundtrip (v2 standalone)
- [ ] Test UUR JSON roundtrip (v2 standalone)
- [ ] Validate against WATS API schema

### Phase 4: Comparison Testing
- [ ] Add v1 vs v2 UUT serialization comparison
- [ ] Add v1 vs v2 UUR serialization comparison
- [ ] Add v1 vs v2 deserialization comparison
- [ ] Test all edge cases (empty lists, None values, etc.)
- [ ] Document any deviations with justification
Phase 5: Service Layer
- [ ] Update `submit_report()` to accept both v1 and v2
- [ ] Update `get_report()` to return v1 or v2 based on flag
- [ ] Add factory methods for v2 models
- [ ] Test service layer with both implementations
- [ ] Verify backward compatibility maintained

### Phase 6: Integration Testing
- [ ] Test v1 submit to real WATS server
- [ ] Test v2 submit to real WATS server
- [ ] Compare server responses for deviations
- [ ] Test v1 retrieve from server
- [ ] Test v2 retrieve from server
- [ ] Cross-test: submit v1, retrieve with v2 parser
- [ ] Cross-test: submit v2, retrieve with v1 parser

### Phase 7: Switch Default
- [ ] Update feature flag to default v2=True
- [ ] Add deprecation warnings to v1
- [ ] Update documentation to show v2 as primary
- [ ] Keep v1 available for fallback

### Tests
- [ ] Add serialization test suite
- [ ] Add deserialization test suite
- [ ] Add discriminated union tests
- [ ] Update existing unit tests
- [ ] Add integration tests with WATS server

### Documentation
- [ ] Update API reference
- [ ] Update code examples
- [ ] Write migration guide
- [ ] Update changelog

### Type Safety
- [ ] Run mypy validation (should pass without type:ignore)
- [ ] Verify no inheritance type conflicts
- [ ] Verify no Optional[list] patterns remain
- [ ] Test with Python 3.10, 3.11, 3.12, 3.13

---

## 6. Risk Assessment

### High Risk
- **JSON compatibility break:** Serialization/deserialization must match exactly
  - **Mitigation:** Comprehensive roundtrip tests with real WATS data
  - **Validation:** Test against production WATS API before release

### Medium Risk
- **Breaking API changes:** Users must update code
  - **Mitigation:** Deprecation period with warnings (1-2 versions)
  - **Migration guide:** Provide automated migration script if possible

### Low Risk
- **Type checking improvements:** Should be transparent to users
- **Performance:** Composition may add minimal overhead
  - **Mitigation:** Benchmark serialization/deserialization

---

## 7. Success Criteria

1. **Type Safety:** Zero mypy errors in report models (no type:ignore needed)
2. **JSON Compatibility:** 100% roundtrip compatibility with WATS API
3. **Test Coverage:** >95% coverage on new models
4. **Performance:** <5% performance regression on serialization
5. **Documentation:** Complete migration guide with examples
6. **Backward Compatibility:** Deprecation warnings guide users smoothly

---

## 8. Open Questions

1. **Passthrough properties vs direct access?**
   - Option A: `report.common.pn` (explicit composition)
   - Option B: `report.pn` (backward compatible properties)
   - **Decision:** Use Option B for backward compatibility, mark common as internal

2. **Generic Report[T] for service layer?**
   - Could use `Generic[SubUnitT]` for sub_units typing
   - **Decision:** Not needed - discriminated union handles this better

3. **MiscInfo collection type?**
   - Current: `Optional[list[MiscInfo]]`
   - Proposed: `list[MiscInfo]` (never None)
   - **Decision:** Always list (remove Optional pattern everywhere)

4. **Validation context for SN/PN?**
   - Keep validation_context pattern from current implementation
   - **Decision:** Yes, preserve existing validation behavior

---

## 9. References

- **Design Document:** `pyWATS_Report_Object_Model_Refactor.md`
- **UUR Spec:** `UUR_IMPLEMENTATION_INSTRUCTIONS.md`
- **Step Discriminated U (Parallel Implementation)

| Phase | Duration | Dependencies | Risk |
|-------|----------|--------------|------|
| 1. Setup Parallel Structure | 0.5 day | None | Low |
| 2. Core Models (v2) | 1 day | Phase 1 | Low |
| 3. Serialization | 1 day | Phase 2 | Medium |
| 4. Comparison Testing | 1 day | Phase 3 | Low |
| 5. Service Layer Updates | 0.5 day | Phase 4 | Low |
| 6. Integration Testing | 1 day | Phase 5, WATS server | Medium |
| 7. Documentation | 0.5 day | Phase 6 | Low |
| 8. Validation & Refinement | 0.5 day | All phases | Low |
| **Total** | **6 days** | | |

**Benefits of Parallel Approach:**
- Can develop incrementally without breaking anything
- Easy rollback if issues found
- A/B testing validates compatibility
- Lower risk = faster development
- Can ship partial features for early feedback

**Note:** Add 15% buffer for comparison test debugging → **~7
| 1. Core Models | 1 day | Pydantic v2 knowledge |
| 2. Serialization | 1 day | Phase 1 complete |
| 3. Service Layer | 1 day | Phase 2 complete |
| 4. Testing | 2 days | Phase 3 complete, WATS test server |
| 5. Documentation | 1 day | Phase 4 complete |
| **Total** | **6 days** | |

**Note:** Add 20% buffer for unexpected issues → **~7-8 days total**

---

## Appendix A: Code Comparison

### Before (Current)
```python
class Report(WATSBase):
    info: Optional[ReportInfo] = None
    misc_infos: Optional[list[MiscInfo]] = Field(default_factory=list)
    
    def add_misc_info(self, desc: str, val: Any) -> MiscInfo:
        if self.misc_infos is None:  # Defensive check
            self.misc_infos = []
        mi = MiscInfo(description=desc, string_value=str(val))
        self.misc_infos.append(mi)
        return mi

class UUTReport(Report):
    info: Optional[UUTInfo] = Field(...)  # Type override - mypy error
    root: SequenceCall = Field(default_factory=SequenceCall)
```

### After (Proposed)
```python
class ReportCommon(BaseModel):
    misc_infos: list[MiscInfo] = Field(default_factory=list)  # Never None

class UUTReport(BaseModel):
    common: ReportCommon
    info: UUTInfo | None = Field(default=None)  # Proper typing
    root: SequenceCall = Field(default_factory=SequenceCall)
    
    @property
    def misc_infos(self) -> list[MiscInfo]:
## Appendix B: Feature Flag Usage Examples

### Development/Testing
```python
# Run tests with v1 (default)
pytest tests/domains/report/

# Run tests with v2
USE_REPORT_V2=1 pytest tests/domains/report/

# Run comparison tests (both)
pytest tests/report_models/test_v1_v2_comparison.py
```

### Application Code
```python
# Explicit v1 usage (always use old)
from pywats.domains.report import UUTReportV1
report = UUTReportV1(pn="...", sn="...", rev="...")

# Explicit v2 usage (always use new)
from pywats.domains.report import UUTReportV2
from pywats.domains.report.report_models_v2 import ReportCommon
report = UUTReportV2(
    process_code=100,
    common=ReportCommon(pn="...", sn="...", rev="...")
)

# Dynamic (respects USE_REPORT_V2 env var)
from pywats.domains.report import UUTReport
# Will use v1 or v2 based on environment
```

### Service Layer
```python
# Service automatically handles both
async with AsyncReportService(...) as service:
    # Submit works with v1 or v2
    await service.submit_report(report_v1)
    await service.submit_report(report_v2)
    
    # Retrieve respects feature flag
    report = await service.get_report(report_id)  # Returns v1 or v2
    
    # Or force specific version
    report_v2 = await service.get_report(report_id, use_v2=True)
```

---

## Appendix D: Avoiding Common Pitfalls

### Pitfall 1: Confusing models.py with report_models/
**Problem:** `models.py` contains query/filter classes (WATSFilter, ReportHeader), NOT report structure  
**Solution:** Only touch `report_models/` and `report_models_v2/` - leave `models.py` alone

### Pitfall 2: Breaking Step imports
**Problem:** Steps already use discriminated union pattern - don't rewrite them!  
**Solution:** Reuse v1 Step hierarchy via relative import:
```python
# In report_models_v2/uut_report.py
from ..report_models.uut.steps import SequenceCall
```

### Pitfall 3: Duplicating too much code
**Problem:** Copying all of report_models/ into v2  
**Solution:** Only create new versions of:
- `report.py` → becomes `report_common.py`
- `uut/uut_report.py` → new composition-based version
- `uur/uur_report.py` → new composition-based version
- `report_union.py` → NEW file for discriminated union

Reuse from v1:
- All Step classes (perfect as-is!)
- MiscInfo, Asset, Chart (stable, small)
- UUTInfo, UURInfo (may need minor tweaks for validators)

### Pitfall 4: Import cycles
**Problem:** v2 imports from v1, v1 imports from v2  
**Solution:** v2 can import from v1, but v1 NEVER imports from v2
```python
# ✓ OK - v2 uses v1 components
# report_models_v2/uut_report.py
from ..report_models.uut.steps import SequenceCall

# ✗ BAD - v1 should never know about v2
# report_models/uut/uut_report.py
from ..report_models_v2 import ReportCommon  # DON'T DO THIS
```

### Pitfall 5: Forgetting to update __init__.py exports
**Problem:** New v2 models exist but aren't exported  
**Solution:** Update `report_models_v2/__init__.py` to export all public classes
```python
# report_models_v2/__init__.py
from .uut_report import UUTReport
from .uur_report import UURReport
from .report_common import ReportCommon
from .report_union import ReportType, parse_report

__all__ = ["UUTReport", "UURReport", "ReportCommon", "ReportType", "parse_report"]
```

---

## Appendix E: Rollback Plan

If v2 has issues after default switch:

1. **Immediate rollback:**
   ```python
   # In __init__.py, change:
   USE_V2 = os.getenv("USE_REPORT_V1", "0") != "1"
   # Back to:
   USE_V2 = os.getenv("USE_REPORT_V2", "0") == "1"
   ```

2. **Emergency patch release:**
   - Set default back to v1
   - Document known v2 issues
   - Fix v2 in parallel
   - Re-enable when ready

3. **V1 remains available:**
   - Never deleted until 0.3.0 major version
   - Users can explicitly use `UUTReportV1`
   - Service layer supports both indefinitely

**No breaking changes until 0.3.0 release.**

---

        return self.common.misc_infos  # Passthrough
    
    def add_misc_info(self, desc: str, val: Any) -> MiscInfo:
        mi = MiscInfo(description=desc, string_value=str(val))
        self.common.misc_infos.append(mi)  # No None check needed
        return mi
```

---

**End of Specification**
