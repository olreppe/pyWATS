# pyWATS Report Object Model Refactor (UUT + UUR)

This proposes an object-model redesign for **Report → UUTReport/UURReport** using **Pydantic v2** patterns: **discriminated unions**, **composition-first modeling**, and **minimal inheritance**. It also aligns **UUR dual-process semantics** (repair vs original test operation).

---

## 1) What’s causing the clunkiness in the current code

- **Field-type overrides in subclasses** (e.g., `Report.info: ReportInfo | None` vs `UUTReport.info: UUTInfo | None`). This works, but typing tools and model expectations get messy.
- **`Optional[list[T]]` with `default_factory=list`** creates unnecessary `None` branches.
- **UUR sub_units are a different element type** (`UURSubUnit`) than `Report.sub_units` (`SubUnit`), forcing overrides and `type:ignore`.
- **UUR has two “process” concepts**:
  - Top-level report `processCode` = **REPAIR process code**
  - UUR header contains the original **TEST operation process code**

If the model doesn’t make this explicit, aliases/properties fight each other.

---

## 2) The core redesign: discriminated union at the Report boundary

Parse unknown report payloads via a **discriminated union** on `Report.type` (`'T'` or `'R'`), just like you already do for steps. This removes the need for a single base class that tries to be both UUT and UUR.

```python
from typing import Annotated, Union, Literal
from pydantic import Discriminator

def _discriminate_report_type(v) -> str:
    # Accept both dicts and instances
    t = getattr(v, "type", None) if not isinstance(v, dict) else v.get("type")
    return t or "T"

ReportType = Annotated[
    Union["UUTReport", "UURReport"],
    Discriminator(_discriminate_report_type),
]
```

**Why this helps**

- You stop overriding core fields with different types.
- Each report variant can declare its own `info`, `sub_units`, etc.
- Your “parsing boundary” becomes clean and explicit.

---

## 3) Composition-first: split shared fields into `ReportCommon`

Instead of overriding many fields in subclasses, move shared fields into a single composable model. Each concrete report type then declares its own variant fields with correct typing.

```python
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class ReportCommon(BaseModel):
    id: UUID
    pn: str
    sn: str
    rev: str

    station_name: str = Field(
        ...,
        validation_alias="machineName",
        serialization_alias="machineName",
    )
    location: str
    purpose: str

    # Always-list: no Optional[list[...] ]
    misc_infos: list["MiscInfo"] = Field(
        default_factory=list,
        validation_alias="miscInfos",
        serialization_alias="miscInfos",
    )
    assets: list["Asset"] = Field(default_factory=list)
    binary_data: list["BinaryData"] = Field(
        default_factory=list,
        validation_alias="binaryData",
        serialization_alias="binaryData",
    )
    additional_data: list["AdditionalData"] = Field(
        default_factory=list,
        validation_alias="additionalData",
        serialization_alias="additionalData",
    )

    start: datetime | None = None
    start_utc: datetime | None = Field(
        default=None,
        validation_alias="startUTC",
        serialization_alias="startUTC",
        exclude=True,
    )

    model_config = dict(populate_by_name=True)
```

> If you don’t like `report.common.pn`, add passthrough properties on the concrete report types (shown below).

---

## 4) Concrete report types keep their own strongly-typed fields

### 4.1 `UUTReport`

```python
from typing import Literal
from pydantic import BaseModel, Field

class UUTReport(BaseModel):
    type: Literal["T"] = "T"

    # Test operation process code
    process_code: int = Field(
        ...,
        validation_alias="processCode",
        serialization_alias="processCode",
    )

    common: ReportCommon

    info: "UUTInfo" | None = Field(
        default=None,
        validation_alias="uut",
        serialization_alias="uut",
    )

    root: "SequenceCall" = Field(default_factory=lambda: SequenceCall())

    # Convenience passthroughs if desired
    @property
    def pn(self) -> str: return self.common.pn

    @property
    def misc_infos(self) -> list["MiscInfo"]: return self.common.misc_infos
```

### 4.2 `UURReport` (dual process codes)

Your spec says: **Top-level report processCode = REPAIR process**, while the embedded UUR header stores the original **TEST operation**.

```python
class UURReport(BaseModel):
    type: Literal["R"] = "R"

    # Top-level WATSReport.Process = REPAIR process code
    process_code: int = Field(
        ...,
        validation_alias="processCode",
        serialization_alias="processCode",
    )

    common: ReportCommon

    uur_info: "UURInfo" = Field(
        default_factory=lambda: UURInfo(),
        validation_alias="uur",
        serialization_alias="uur",
    )

    # UUR-specific subunits with idx/parent_idx/failures etc
    sub_units: list["UURSubUnit"] = Field(
        default_factory=list,
        validation_alias="subUnits",
        serialization_alias="subUnits",
    )

    # Expose original test operation code
    @property
    def test_operation_code(self) -> int | None:
        return self.uur_info.test_operation_code
```

---

## 5) Fix the Optional[list] pattern everywhere

Replace:

- `Optional[list[T]] = Field(default_factory=list)`

with:

- `list[T] = Field(default_factory=list)`

Then remove branches like:

```python
if self.misc_infos is None:
    self.misc_infos = []
```

Your adders become one-liners and the model behaves like a value object, not a nullable pointer graph.

---

## 6) About using Generics (`TypeVar`) for `Report[T]`

Generics can help editor/mypy type-checking when you construct reports in code, but they **don’t** solve parsing unknown JSON (you still need a union at the boundary).

If you want generics, do it on **small reusable traits**, not the whole Report.

```python
from typing import TypeVar, Generic
from pydantic import BaseModel, Field

SubT = TypeVar("SubT", bound="SubUnitBase")

class HasSubUnits(Generic[SubT], BaseModel):
    sub_units: list[SubT] = Field(default_factory=list)
```

But for API input/output: **discriminated unions beat generics**.

---

## 7) “Worst case” areas and patterns that scale

- **Steps:** keep using discriminated unions. Map server aliases/type_ids to one canonical internal tag in a discriminator function.
- **MiscInfo:** avoid generics unless the server truly has multiple shapes. If it does, use a discriminated union (same pattern as steps).
- **Sub-units:** don’t force a single base SubUnit type. UUR sub-units carry extra indexing/failures, so model them as a separate type and keep them local to `UURReport`.
- **ReportInfo:** prefer `UUTInfo` and `UURInfo` fields on their respective reports rather than a single `Report.info` that changes type via overrides.

---

## 8) Suggested migration plan (low risk)

1. **Remove Optional[list] + null checks** in current models.
2. Introduce **ReportCommon** and update `UUTReport`/`UURReport` to use it  
   - keep passthrough properties to avoid breaking existing code
3. Introduce **ReportType** discriminated union for deserialization entry points.
4. Align **UUR processCode semantics**: top-level repair process vs header test operation (keep both explicit).

---

## Notes tied to your files

- `Report` base and optional-list patterns: `report.py`
- `UUTReport` design: `uut_report.py`, `uut_info.py`
- `UURReport` and dual process semantics: `uur_report.py`, `uur_info.py`, `UUR_IMPLEMENTATION_INSTRUCTIONS.md`
- `SubUnit` base: `sub_unit.py`
