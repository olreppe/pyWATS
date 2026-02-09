# UUTReport Object Model - Printable Diagrams

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

### Option 4: GitHub/Browser
1. View .md file on GitHub
2. Right-click rendered diagram → "Save image as..."
3. Or use browser dev tools to export SVG

---

## Diagram 1: UUTReport - Core Structure

**Top-level report structure with header information**

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
    
    class UUTReport {
        +type: Literal["T"]
        +info: UUTInfo
        +root: SequenceCall
        +sub_units: List~UUTSubUnit~
        +misc_info: MiscInfo
        +assets: List~Asset~
        +binary_data: List~BinaryData~
        +additional_data: List~AdditionalData~
        +test_operation_code: int
        +get_root_sequence_call() SequenceCall
        +add_sub_unit(pn, sn, rev) UUTSubUnit
        +get_all_steps() List~Step~
        +get_failed_steps() List~Step~
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
    Report <|-- UUTReport
    UUTReport --> ReportResult : result
```

---

## Diagram 2: UUTReport - Info and Sub-Units

**UUTInfo and SubUnit structure**

```mermaid
classDiagram
    class UUTReport {
        +info: UUTInfo
        +sub_units: List~UUTSubUnit~
    }
    
    class ReportInfo {
        <<Base>>
        +operator: str
        +comment: str
        +exec_time: float
    }
    
    class UUTInfo {
        +fixture_id: str
        +socket_index: int
        +socket_index_format: str
        +error_code: int
        +error_code_format: str
        +error_message: str
        +batch_number: str
        +batch_fail_count: int
        +batch_loop_index: int
        +step_id_caused_uut_failure: int
        +referenced_by_uurs: List~RefUURs~
    }
    
    class RefUURs {
        +id: UUID
        +start: str
    }
    
    class SubUnit {
        +pn: str
        +rev: str
        +sn: str
        +part_type: str
        +validate_sn(sn) str
        +validate_pn(pn) str
    }
    
    class UUTSubUnit {
        +root: SequenceCall
    }
    
    ReportInfo <|-- UUTInfo
    SubUnit <|-- UUTSubUnit
    UUTReport --> UUTInfo
    UUTReport --> UUTSubUnit
    UUTInfo --> RefUURs
```

---

## Diagram 3: UUTReport - Assets and Binary Data

**Supporting data structures**

```mermaid
classDiagram
    class UUTReport {
        +assets: List~Asset~
        +binary_data: List~BinaryData~
        +additional_data: List~AdditionalData~
        +misc_info: MiscInfo
    }
    
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
    
    UUTReport --> Asset
    UUTReport --> BinaryData
    UUTReport --> AdditionalData
    UUTReport --> MiscInfo
```

---

## Diagram 4: Step Hierarchy - Base and Container

**Step base class and SequenceCall container**

```mermaid
classDiagram
    class Step {
        <<abstract>>
        +step_type: str
        +name: str
        +group: str
        +status: StepStatus
        +id: int|str
        +error_code: int|str
        +error_message: str
        +report_text: str
        +start: str
        +tot_time: float|str
        +parent: SequenceCall
        +attachments: List~Attachment~
        +charts: List~Chart~
        +validate_step()* bool
        +set_status(status) void
        +add_attachment(attachment) void
        +is_failed() bool
        +is_passed() bool
    }
    
    class SequenceCall {
        +step_type: Literal["SequenceCall"]
        +sequence: SequenceCallInfo
        +caller: SequenceCallInfo
        +steps: StepList
        +loop_info: LoopInfo
        +add_step(step) Step
        +add_numeric_step(...) NumericStep
        +add_boolean_step(...) PassFailStep
        +add_string_step(...) StringValueStep
        +add_sequence_call(name) SequenceCall
        +get_all_steps() List~Step~
        +get_failed_steps() List~Step~
        +propagate_failure() void
    }
    
    class SequenceCallInfo {
        +path: str
        +name: str
        +version: str
        +file_path: str
    }
    
    class LoopInfo {
        +loop_index: int
        +loop_count: int
    }
    
    class StepStatus {
        <<enumeration>>
        Passed
        Failed
        Done
        Error
        Skipped
        Terminated
    }
    
    Step <|-- SequenceCall
    SequenceCall --> SequenceCallInfo
    SequenceCall --> LoopInfo
    Step --> StepStatus
    SequenceCall --> Step : contains steps
```

---

## Diagram 5: Step Types - Measurement Steps

**Numeric, Boolean, and String test steps**

```mermaid
classDiagram
    class Step {
        <<abstract>>
        +step_type: str
        +name: str
        +status: StepStatus
    }
    
    class NumericStep {
        +step_type: Literal["ET_NLT"]
        +measurement: NumericMeasurement
        +value: float|str
        +comp: CompOp
        +limit_l: float|str
        +limit_h: float|str
        +unit: str
        +set_limits(low, high, comp) void
        +set_value(value, unit) void
    }
    
    class MultiNumericStep {
        +step_type: Literal["ET_MNLT"]
        +measurements: List~NumericMeasurement~
        +add_measurement(...) NumericMeasurement
        +get_measurement(name) NumericMeasurement
    }
    
    class PassFailStep {
        +step_type: Literal["ET_PLT"]
        +measurement: BooleanMeasurement
        +value: bool
        +set_value(value) void
    }
    
    class MultiBooleanStep {
        +step_type: Literal["ET_MPLT"]
        +measurements: List~BooleanMeasurement~
        +add_measurement(name, value) BooleanMeasurement
    }
    
    class StringValueStep {
        +step_type: Literal["ET_SLT"]
        +measurement: StringMeasurement
        +value: str
        +set_value(value) void
    }
    
    class MultiStringStep {
        +step_type: Literal["ET_MSLT"]
        +measurements: List~StringMeasurement~
        +add_measurement(name, value) StringMeasurement
    }
    
    Step <|-- NumericStep
    Step <|-- MultiNumericStep
    Step <|-- PassFailStep
    Step <|-- MultiBooleanStep
    Step <|-- StringValueStep
    Step <|-- MultiStringStep
```

---

## Diagram 6: Step Types - Other Steps

**Generic, Action, Chart, and Unknown steps**

```mermaid
classDiagram
    class Step {
        <<abstract>>
        +step_type: str
        +name: str
        +status: StepStatus
    }
    
    class GenericStep {
        +step_type: Literal["ET_STR"]
        +flow_type: FlowType
        +string_value: str
    }
    
    class ActionStep {
        +step_type: Literal["ActionStep"]
        +action_type: str
    }
    
    class ChartStep {
        +step_type: Literal["ChartStep"]
        +charts: List~Chart~
        +add_chart(chart) Chart
    }
    
    class UnknownStep {
        +step_type: str
        +raw_data: dict
    }
    
    class Chart {
        +chart_type: ChartType
        +name: str
        +x_axis: List~float~
        +y_axis: List~float~
        +x_label: str
        +y_label: str
        +create_xy_chart(...)$ Chart
    }
    
    class FlowType {
        <<enumeration>>
        If
        Else
        Case
        Loop
        End
    }
    
    class ChartType {
        <<enumeration>>
        XY
        Histogram
        Polar
    }
    
    Step <|-- GenericStep
    Step <|-- ActionStep
    Step <|-- ChartStep
    Step <|-- UnknownStep
    ChartStep --> Chart
    GenericStep --> FlowType
    Chart --> ChartType
```

---

## Diagram 7: Measurement Classes

**Measurement data structures with limits**

```mermaid
classDiagram
    class BaseMeasurement {
        <<abstract>>
        +status: StepStatus
        +name: str
    }
    
    class NumericMeasurement {
        +value: float|str
        +value_format: str
        +comp: CompOp
        +limit_l: float|str
        +limit_h: float|str
        +limit_l_format: str
        +limit_h_format: str
        +unit: str
        +evaluate() bool
        +validate_limits() bool
    }
    
    class BooleanMeasurement {
        +value: bool
    }
    
    class StringMeasurement {
        +value: str
    }
    
    class CompOp {
        <<enumeration>>
        EQ
        NE
        LT
        LE
        GT
        GE
        GTLT
        GTLE
        GELT
        GELE
        +evaluate(value, low, high) bool
        +validate_limits(low, high) bool
    }
    
    BaseMeasurement <|-- NumericMeasurement
    BaseMeasurement <|-- BooleanMeasurement
    BaseMeasurement <|-- StringMeasurement
    NumericMeasurement --> CompOp
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

3. **Alternative: Create PDF from Images:**
   ```bash
   # Export all diagrams as PNG
   # Then combine with ImageMagick:
   convert diagram*.png combined.pdf
   
   # Or use online tools like:
   # - Smallpdf.com
   # - ilovepdf.com
   ```

4. **Print from VS Code Preview:**
   - Install "Markdown Preview Mermaid Support"
   - Open this file
   - Ctrl+Shift+V (preview)
   - Print preview → each diagram should fit on one page

---

## Quick Reference: Diagram Purpose

| Diagram | Content | Use For |
|---------|---------|---------|
| **Diagram 1** | Core report structure | Understanding report hierarchy |
| **Diagram 2** | UUTInfo & sub-units | Test information and components |
| **Diagram 3** | Assets & binary data | Supporting data structures |
| **Diagram 4** | Step base & SequenceCall | Test hierarchy foundation |
| **Diagram 5** | Measurement steps | Numeric/boolean/string tests |
| **Diagram 6** | Other step types | Generic/action/chart steps |
| **Diagram 7** | Measurement classes | Limit definitions and evaluations |

---

**Related:** [UUR Printable Diagrams](UUR_OBJECT_MODEL_PRINTABLE.md)
