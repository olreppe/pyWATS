# UURReport Object Model - Printable Diagrams

**Broken down into separate diagrams for printing (one per page)**

**Generated:** February 8, 2026  
**Format:** Individual Mermaid diagrams optimized for single-page printing

---

## Export Options for Mermaid Diagrams

### Option 1: Mermaid Live Editor (Recommended for Printing) ⭐
1. Visit https://mermaid.live/
2. Paste diagram code
3. Click **Actions** → Export as:
   - **PNG** (high resolution, recommended)
   - **SVG** (vector, scales perfectly)
   - **PDF** (direct to printable format)

### Option 2: VS Code Extensions
**Install:** "Markdown Preview Mermaid Support" or "Mermaid Preview"
1. Open .md file in VS Code
2. Right-click diagram → "Export as PNG/SVG"
3. Or use Command Palette → "Mermaid: Export Diagram"

### Option 3: Command Line (Batch Export)
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Export to PNG
mmdc -i diagram.mmd -o output.png -w 2400 -H 1800

# Export to PDF
mmdc -i diagram.mmd -o output.pdf
```

---

## Diagram 1: UURReport - Core Structure

**Top-level repair report structure**

```mermaid
classDiagram
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
        +validate_sn(sn) str
        +validate_pn(pn) str
    }
    
    class UURReport {
        +type: Literal["R"]
        +info: UURInfo
        +sub_units: List~UURSubUnit~
        +asset_stats: List
        +misc_info: MiscInfo
        +assets: List~Asset~
        +binary_data: List~BinaryData~
        +repair_process_code: int
        +test_process_code: int
        +get_main_unit() UURSubUnit
        +get_sub_unit(idx) UURSubUnit
        +add_sub_unit(...) UURSubUnit
        +add_failure_to_main(...) UURFailure
        +get_all_failures() List~UURFailure~
    }
    
    class ReportResult {
        <<enumeration>>
        Passed
        Failed
        Done
        Error
        Terminated
    }
    
    WATSBase <|-- Report
    Report <|-- UURReport
    UURReport --> ReportResult
```

---

## Diagram 2: UURReport - Dual Process Codes

**Process code architecture explanation**

```mermaid
graph TB
    A[UURReport] -->|process_code<br/>Top Level| B[Repair Operation Code]
    A -->|info.process_code<br/>UURInfo| C[Test Operation Code]
    
    B --> B1[500: Repair]
    B --> B2[510: RMA Repair]
    B --> B3[520: Rework]
    
    C --> C1[100: EOL Test]
    C --> C2[50: PCBA Test]
    C --> C3[200: Calibration]
    
    style A fill:#f9f,stroke:#333,stroke-width:3px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
    style B1 fill:#ddf,stroke:#333
    style B2 fill:#ddf,stroke:#333
    style B3 fill:#ddf,stroke:#333
    style C1 fill:#dfd,stroke:#333
    style C2 fill:#dfd,stroke:#333
    style C3 fill:#dfd,stroke:#333
    
    note1[What KIND of repair<br/>was performed]
    note2[What TEST was running<br/>when failure occurred]
    
    B -.-> note1
    C -.-> note2
```

---

## Diagram 3: UURInfo Structure

**UUR-specific information**

```mermaid
classDiagram
    class UURReport {
        +info: UURInfo
    }
    
    class ReportInfo {
        <<Base>>
        +operator: str
        +comment: str
        +exec_time: float
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
        +rma_number: str
        +customer_number: str
        +failure_description: str
        +repair_description: str
        +repair_time: float
        +technician: str
        +cost: float
        +link_to_uut(uut_id) void
        +set_repair_description(desc) void
        +set_failure_description(desc) void
    }
    
    ReportInfo <|-- UURInfo
    UURReport --> UURInfo
```

---

## Diagram 4: UURSubUnit Hierarchy

**Sub-unit structure with index-based hierarchy**

```mermaid
classDiagram
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
        +create_sub_unit(...)$ UURSubUnit
        +add_failure(...) UURFailure
        +remove_failure(index) bool
        +get_failure(index) UURFailure
        +has_failures() bool
        +failure_count() int
        +get_failures_by_category(cat) List~UURFailure~
        +clear_failures() void
        +mark_as_replaced(idx) void
    }
    
    class UURReport {
        +sub_units: List~UURSubUnit~
        +get_main_unit() UURSubUnit
    }
    
    SubUnit <|-- UURSubUnit
    UURReport --> UURSubUnit
```

---

## Diagram 5: Sub-Unit Hierarchy Example

**Visual representation of idx/parent_idx relationships**

```mermaid
graph TD
    A[Main Unit<br/>idx=0<br/>pn: PCB-001<br/>sn: MAIN-123] 
    B[Sub-Unit<br/>idx=1<br/>parent_idx=0<br/>pn: MODULE-A<br/>sn: MOD-456]
    C[Sub-Unit<br/>idx=2<br/>parent_idx=0<br/>pn: MODULE-B<br/>sn: MOD-789]
    D[Sub-Unit<br/>idx=3<br/>parent_idx=1<br/>pn: CHIP-X<br/>sn: CHIP-111]
    
    A -->|contains| B
    A -->|contains| C
    B -->|contains| D
    
    E[Failure 1<br/>CAP_FAIL<br/>com_ref: C12]
    F[Failure 2<br/>TRACE_BREAK<br/>func_block: PWR]
    G[Failure 3<br/>IC_FAIL<br/>com_ref: U5]
    
    A -.->|failures| E
    A -.->|failures| F
    B -.->|failures| G
    
    style A fill:#faa,stroke:#333,stroke-width:3px
    style B fill:#ffa,stroke:#333,stroke-width:2px
    style C fill:#ffa,stroke:#333,stroke-width:2px
    style D fill:#afa,stroke:#333,stroke-width:1px
    style E fill:#fdd,stroke:#333,stroke-width:1px
    style F fill:#fdd,stroke:#333,stroke-width:1px
    style G fill:#fdd,stroke:#333,stroke-width:1px
```

---

## Diagram 6: UURFailure Structure

**Failure record details**

```mermaid
classDiagram
    class UURSubUnit {
        +failures: List~UURFailure~
        +add_failure(...) UURFailure
    }
    
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
        +set_component_reference(...) void
        +set_article_info(...) void
        +link_to_uut_step(id, name) void
    }
    
    UURSubUnit --> UURFailure
```

---

## Diagram 7: UUT-UUR Linking Flow

**How repair reports link to test reports**

```mermaid
sequenceDiagram
    participant T as UUTReport
    participant F as Failed Test
    participant R as UURReport
    participant U as UURInfo
    participant S as UURSubUnit
    participant Fail as UURFailure
    
    T->>F: Test executes
    Note over F: result=Failed<br/>Step 42 fails
    
    F->>R: Create repair report
    R->>U: Initialize UURInfo
    U->>U: Set ref_uut = UUT.id
    U->>U: Set process_code = 100<br/>(test that failed)
    
    R->>S: Get main unit (idx=0)
    S->>Fail: Add failure
    Fail->>Fail: Set ref_step_id=42<br/>(step from UUT)
    
    Note over R: UUR now linked<br/>to original UUT
    
    R->>R: Document repair
    R->>R: Submit to server
```

---

## Diagram 8: Assets and Supporting Data

**Assets, binary data, and misc info**

```mermaid
classDiagram
    class UURReport {
        +assets: List~Asset~
        +binary_data: List~BinaryData~
        +additional_data: List~AdditionalData~
        +misc_info: MiscInfo
        +asset_stats: List
    }
    
    class Asset {
        +sn: str
        +asset_type: str
        +pn: str
        +usage_count: int
        +calibration_date: datetime
        +calibration_due: datetime
    }
    
    class BinaryData {
        +content_type: str
        +data: str
        +name: str
        +get_bytes() bytes
        +from_bytes(...)$ BinaryData
    }
    
    class AdditionalData {
        +name: str
        +value: str
    }
    
    class MiscInfo {
        +items: List~MiscInfoItem~
        +add_item(key, value) void
        +get_item(key) str
    }
    
    class UURMiscInfo {
        +ref_part_number: str
        +ref_part_revision: str
        +ref_location: str
        +ref_station: str
        +ref_purpose: str
    }
    
    UURReport --> Asset
    UURReport --> BinaryData
    UURReport --> AdditionalData
    UURReport --> MiscInfo
    MiscInfo <|-- UURMiscInfo
```

---

## Printing Instructions

### For Best Print Quality:

1. **Export each diagram separately** using Mermaid Live Editor:
   - Copy diagram code
   - Paste into https://mermaid.live/
   - Export as PNG (2400x1800 or higher)
   - Or export as PDF for vector quality

2. **Page Setup Recommendations:**
   - Orientation: **Landscape**
   - Paper: **Letter or A4**
   - Margins: **0.5 inch all sides**
   - Scale: **Fit to page width**

3. **Alternative: Screenshot from VS Code:**
   - Install "Markdown Preview Mermaid Support"
   - Open preview (Ctrl+Shift+V)
   - Screenshot each diagram
   - Paste into Word/PowerPoint

4. **Batch Export Script:**
   ```bash
   # Save each diagram block to separate .mmd files
   # Then export all:
   for file in uur_diagram_*.mmd; do
       mmdc -i "$file" -o "${file%.mmd}.png" -w 2400 -H 1800
   done
   ```

---

## Quick Reference: Diagram Purpose

| Diagram | Content | Use For |
|---------|---------|---------|
| **Diagram 1** | Core repair report | Understanding UUR structure |
| **Diagram 2** | Dual process codes | Process code architecture |
| **Diagram 3** | UURInfo details | Repair-specific information |
| **Diagram 4** | UURSubUnit class | Sub-unit with failure methods |
| **Diagram 5** | Hierarchy example | Visual idx/parent_idx relationships |
| **Diagram 6** | UURFailure class | Failure record structure |
| **Diagram 7** | UUT-UUR linking | How repairs link to tests |
| **Diagram 8** | Assets & data | Supporting structures |

---

## Key Concepts Reference

### Main Unit (idx=0)
- Always the primary unit being repaired
- Created automatically when UURReport is instantiated
- Access via `uur.get_main_unit()`

### Parent-Child Hierarchy
- `idx` - Unique identifier for each unit
- `parent_idx` - Index of containing unit
- `position` - Position within parent
- Enables multi-level assembly tracking

### Failure Attribution
- Failures attached to specific sub-units
- `ref_step_id` links to original UUT test step
- Component reference (`com_ref`) for traceability
- Article info tracks replaced components

### Dual Process Codes
- **Report.process_code** - Repair operation (500, 510, 520)
- **UURInfo.process_code** - Test operation that failed (100, 50, 200)
- Enables analysis: "Which tests have most repairs?"

---

**Related:** [UUT Printable Diagrams](UUT_OBJECT_MODEL_PRINTABLE.md)
