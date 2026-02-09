# UURReport Object Model - Class Diagram

**Comprehensive class diagram for UUR (Unit Under Repair) report structure**

**Generated:** February 8, 2026  
**Scope:** All classes involved in UURReport with public members and methods

---

## UURReport Class Hierarchy

```mermaid
classDiagram
    %% Core Report Hierarchy
    class WATSBase {
        <<abstract>>
        +model_dump() dict
        +model_dump_json() str
        +model_validate(data) Self
    }
    
    class Report~SubUnitT~ {
        <<Generic Base>>
        +id: UUID
        +type: str
        +pn: str
        +sn: str
        +rev: str
        +process_code: int
        +result: ReportResult
        +station_name: str
        +location: str
        +purpose: str
        +operator: str
        +start: datetime
        +exec_time: float
        +comment: str
        +misc_info: MiscInfo
        +assets: List~Asset~
        +binary_data: List~BinaryData~
        +additional_data: List~AdditionalData~
        +sub_units: List~SubUnitT~
        +info: ReportInfo
        +validate_sn(sn) str
        +validate_pn(pn) str
        +get_assets_by_type(asset_type) List~Asset~
        +add_asset(asset) void
        +add_binary_data(data) void
    }
    
    class UURReport {
        +type: Literal["R"]
        +info: UURInfo
        +sub_units: List~UURSubUnit~
        +asset_stats: List
        +repair_process_code: int
        +test_process_code: int
        +get_main_unit() UURSubUnit
        +get_sub_unit(idx) UURSubUnit
        +add_sub_unit(pn, sn, rev, parent_idx) UURSubUnit
        +add_failure_to_main(category, code, comment) UURFailure
        +get_all_failures() List~UURFailure~
        +get_failures_by_category(category) List~UURFailure~
        +link_to_uut(uut_id) void
        +set_repair_operation(code) void
        +set_test_operation(code) void
    }
    
    WATSBase <|-- Report
    Report <|-- UURReport
    
    %% UUR Info
    class ReportInfo {
        <<Base>>
        +operator: str
        +comment: str
        +exec_time: float
        +serialize_exec_time(value) float
    }
    
    class UURInfo {
        +process_code: int
        +process_code_format: str
        +process_name: str
        +test_operation_code: int
        +test_operation_name: str
        +test_operation_guid: UUID
        +ref_uut: UUID
        +work_order: str
        +work_order_format: str
        +rma_number: str
        +rma_number_format: str
        +customer_number: str
        +customer_number_format: str
        +failure_description: str
        +repair_description: str
        +repair_time: float
        +repair_time_format: str
        +technician: str
        +cost: float
        +cost_format: str
        +link_to_uut(uut_id) void
        +set_repair_description(description) void
        +set_failure_description(description) void
    }
    
    ReportInfo <|-- UURInfo
    UURReport --> UURInfo : info
    
    %% Sub Units with Failures
    class SubUnit {
        +pn: str
        +rev: str
        +sn: str
        +part_type: str
        +validate_sn(sn) str
        +validate_pn(pn) str
    }
    
    class UURSubUnit {
        +sn: str
        +part_type: str
        +idx: int
        +parent_idx: int
        +position: int
        +replaced_idx: int
        +failures: List~UURFailure~
        +create_main_unit(pn, sn, rev)$ UURSubUnit
        +create_sub_unit(pn, sn, rev, idx, parent_idx)$ UURSubUnit
        +add_failure(category, code, comment, com_ref, func_block) UURFailure
        +remove_failure(index) bool
        +get_failure(index) UURFailure
        +has_failures() bool
        +failure_count() int
        +get_failures_by_category(category) List~UURFailure~
        +clear_failures() void
        +mark_as_replaced(replaced_idx) void
    }
    
    SubUnit <|-- UURSubUnit
    UURReport --> UURSubUnit : sub_units
    
    %% Failure Records
    class UURFailure {
        +category: str
        +code: str
        +comment: str
        +com_ref: str
        +func_block: str
        +ref_step_id: int
        +ref_step_name: str
        +art_number: str
        +art_rev: str
        +art_vendor: str
        +lot_code: str
        +date_code: str
        +set_component_reference(com_ref, func_block) void
        +set_article_info(art_number, art_rev, art_vendor) void
        +link_to_uut_step(step_id, step_name) void
    }
    
    UURSubUnit --> UURFailure : failures
    
    %% Supporting Classes
    class Asset {
        +sn: str
        +asset_type: str
        +pn: str
        +usage_count: int
        +calibration_date: datetime
        +calibration_due: datetime
        +validate_sn(sn) str
    }
    
    class BinaryData {
        +content_type: str
        +data: str
        +name: str
        +get_bytes() bytes
        +from_bytes(data, name, content_type)$ BinaryData
    }
    
    class Attachment {
        +name: str
        +content_type: str
        +data: str
        +size: int
        +get_bytes() bytes
        +from_file(path)$ Attachment
        +from_bytes(data, name)$ Attachment
    }
    
    class AdditionalData {
        +name: str
        +value: str
    }
    
    class MiscInfo {
        +items: List~MiscInfoItem~
        +add_item(key, value) void
        +get_item(key) str
        +remove_item(key) bool
    }
    
    class UURMiscInfo {
        +ref_part_number: str
        +ref_part_revision: str
        +ref_location: str
        +ref_station: str
        +ref_purpose: str
    }
    
    UURReport --> Asset : assets
    UURReport --> BinaryData : binary_data
    UURReport --> MiscInfo : misc_info
    MiscInfo <|-- UURMiscInfo
    
    %% Enums
    class ReportResult {
        <<enumeration>>
        Passed
        Failed
        Done
        Error
        Terminated
    }
```

---

## Dual Process Code Architecture

UURReport has a unique dual process code design:

```mermaid
graph LR
    A[UURReport] -->|process_code<br/>Repair Operation| B[500: Repair<br/>510: RMA Repair<br/>520: Rework]
    A -->|info.process_code<br/>Test Operation| C[100: EOL Test<br/>50: PCBA Test<br/>200: Calibration]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
```

**Report.process_code** (top-level) = **What KIND of repair** was performed
- Example: 500 = "Repair", 510 = "RMA Repair", 520 = "Rework"

**UURInfo.process_code** (uur object) = **What TEST was running** when failure occurred
- Example: 100 = "End of Line Test", 50 = "PCBA Test"

---

## Sub-Unit Hierarchy with Failures

```mermaid
graph TD
    A[Main Unit<br/>idx=0<br/>SN: MAIN-001] -->|parent_idx=0| B[Sub-Unit 1<br/>idx=1<br/>SN: SUB-001]
    A -->|parent_idx=0| C[Sub-Unit 2<br/>idx=2<br/>SN: SUB-002]
    B -->|parent_idx=1| D[Sub-Unit 3<br/>idx=3<br/>SN: SUB-003]
    
    A -.->|failures| E[Failure 1: CAP_FAIL<br/>com_ref: C12]
    A -.->|failures| F[Failure 2: TRACE_BREAK<br/>func_block: POWER]
    B -.->|failures| G[Failure 3: IC_FAIL<br/>com_ref: U5]
    
    style A fill:#faa,stroke:#333,stroke-width:3px
    style B fill:#ffa,stroke:#333,stroke-width:2px
    style C fill:#ffa,stroke:#333,stroke-width:2px
    style D fill:#afa,stroke:#333,stroke-width:1px
    style E fill:#fdd,stroke:#333,stroke-width:1px
    style F fill:#fdd,stroke:#333,stroke-width:1px
    style G fill:#fdd,stroke:#333,stroke-width:1px
```

**Key Concepts:**
- **idx=0** is always the main unit being repaired
- **parent_idx** creates hierarchy (which unit contains which)
- **failures** are attached to the specific unit where they were found
- **replaced_idx** tracks component replacements

---

## Linking to Original UUT Report

```mermaid
sequenceDiagram
    participant Test as UUTReport
    participant Fail as Failed Test
    participant Repair as UURReport
    participant Link as UURInfo.ref_uut
    
    Test->>Fail: Test fails
    Note over Fail: result=Failed<br/>step causes failure
    Fail->>Repair: Create repair report
    Repair->>Link: Set ref_uut = UUT.id
    Note over Link: Links repair to<br/>original test
    Repair->>Repair: Add failures found
    Note over Repair: failures reference<br/>UUT step IDs
```

---

## Key Relationships

### Composition
- **UURReport** contains:
  - `info: UURInfo` - Repair/test information with UUT reference
  - `sub_units: List[UURSubUnit]` - Units with failures (idx=0 is main)
  - `assets: List[Asset]` - Equipment used during repair
  - `binary_data: List[BinaryData]` - Photos, documents
  - `misc_info: MiscInfo` - Key-value metadata

### Hierarchy
- **UURSubUnit** extends SubUnit with:
  - `idx` - Unit index (0 = main unit)
  - `parent_idx` - Parent in hierarchy
  - `failures` - List of failures on this unit
  - `replaced_idx` - Index of unit this replaced

### Failure Tracking
- **UURFailure** captures:
  - Category and code (failure taxonomy)
  - Component reference (C12, R5, U3)
  - Article info (part number of failed component)
  - Link to UUT step that found the failure

---

## Usage Example

```python
from pywats.domains.report import UURReport, UURSubUnit, UURFailure

# Create UUR report
uur = UURReport(
    pn="WIDGET-001",
    sn="SN123456",
    rev="A",
    process_code=500,  # Repair operation
    station_name="RepairStation",
    location="Lab",
    purpose="Repair"
)

# Set test operation that was running when failure occurred
uur.info.process_code = 100  # EOL Test
uur.info.process_name = "End of Line Test"

# Link to failed UUT report
uur.info.ref_uut = uut_report_id

# Get main unit (automatically created, idx=0)
main = uur.get_main_unit()

# Add failure to main unit
failure1 = main.add_failure(
    category="Component",
    code="CAP_FAIL",
    comment="Electrolytic capacitor failed",
    com_ref="C12",
    func_block="POWER_SUPPLY"
)

# Set article info for failed component
failure1.art_number = "CAP-100uF-25V"
failure1.art_vendor = "Vendor-A"

# Link failure to UUT step
failure1.ref_step_id = 42
failure1.ref_step_name = "Measure Supply Voltage"

# Add sub-unit with failure
sub1 = uur.add_sub_unit(
    pn="MODULE-001",
    sn="MOD-789",
    rev="B",
    parent_idx=0  # Child of main unit
)
sub1.idx = 1

sub1.add_failure(
    category="Assembly",
    code="SOLDER_DEFECT",
    comment="Cold solder joint",
    com_ref="J3"
)

# Set repair description
uur.info.repair_description = "Replaced C12 and reworked solder joint on J3"
uur.info.technician = "John Doe"
uur.info.repair_time = 1800.0  # 30 minutes in seconds

# Submit repair report
await api.report.submit_uur(uur)
```

---

## Comparison: UUT vs UUR

| Feature | UUTReport | UURReport |
|---------|-----------|-----------|
| **Purpose** | Test execution | Repair documentation |
| **Type** | "T" | "R" |
| **Steps** | ✅ Root SequenceCall with hierarchy | ❌ No test steps |
| **Failures** | ❌ Inferred from failed steps | ✅ Explicit UURFailure records |
| **Process Code** | Single (test operation) | Dual (repair + test) |
| **Sub-Units** | UUTSubUnit (with optional root) | UURSubUnit (with idx, failures) |
| **Info Object** | UUTInfo | UURInfo (with ref_uut link) |
| **Hierarchy** | Step tree | Sub-unit parent/child |

---

**Related Documentation:**
- [UUTReport Object Model](UUT_OBJECT_MODEL.md)
- [Report Domain Guide](../../../docs/guides/report-domain.md)
- [Repair Workflow Guide](../../../docs/guides/repair-workflow.md)
