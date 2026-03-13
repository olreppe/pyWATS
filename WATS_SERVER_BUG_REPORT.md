# WATS Server Bug Report: Export/Import Format Mismatch

**Reporter:** pyWATS Development Team  
**Date:** February 20, 2026  
**Server Version:** 2026.1.5.324  
**Server URL:** python.wats.com  
**Severity:** Critical - Blocks re-import of exported data

---

## Summary

The WATS server exports UUT reports in a format that fails validation when attempting to re-import the same data. Specifically, loop summary step validation rules differ between the export API and the import API.

---

## Issue Description

### Problem
Files exported via the WATS web interface or export API **cannot be re-imported** to the same server due to validation errors in loop structure fields (`num` and `endingIndex`).

### Expected Behavior
Data exported from WATS should be valid for re-import to WATS without modification.

### Actual Behavior
Exported reports fail import validation with error:
```
loop SequenceCallLoop: num is required to be one more than endingIndex.
```

---

## Reproduction Steps

1. **Export a UUT report** from WATS server (python.wats.com) with loop steps
   - Method: Web UI → Export → JSON (WSJF format)
   - Example Report ID: `2961a76f-5631-49c6-8e93-15fe31635531`

2. **Verify exported loop structure:**
   ```json
   {
     "loop": {
       "idx": null,
       "num": 3,
       "endingIndex": 3,
       "passed": 1,
       "failed": 2
     }
   }
   ```
   ✓ **Export format:** `num = endingIndex` (e.g., `num=3, endingIndex=3` for 3 iterations)

3. **Attempt to re-import** the exported file via API `POST /api/Report/WSJF`

4. **Result:** Import fails with validation error:
   ```
   400 Bad Request
   loop SequenceCallLoop: num is required to be one more than endingIndex.
   loop SequenceCallLoop: endingIndex is required to be the same as highest index.
   ```

---

## Technical Analysis

### Loop Structure Semantics

For a loop with **3 iterations** (indices: 0, 1, 2):

| Field | Export Value | Import Requirement | Interpretation |
|-------|--------------|-------------------|----------------|
| `idx` | `null` | `null` | Summary step marker |
| `num` | `3` | `4` ❌ | **MISMATCH:** Export uses iteration count, Import expects count+1 |
| `endingIndex` | `3` | `3` | One past highest index (array.length style) |
| `passed` | `1` | `1` | Count of passed iterations |
| `failed` | `2` | `2` | Count of failed iterations |

### The Conflict

- **Export API behavior:** Sets `num = endingIndex = 3` (iteration count equals ending index)
- **Import API validation:** Requires `num = endingIndex + 1` (expects `num = 4`)
- **Result:** Exported data is rejected by import validation

---

## Evidence

### Test Case: Server-Exported File

**File:** `uut-wsjf-export (16).json` (exported from python.wats.com)  
**Original Report ID:** `2961a76f-5631-49c6-8e93-15fe31635531`

**Loop Examples from Export:**

```json
{
  "name": "SequenceCallLoop",
  "loop": {
    "idx": null,
    "num": 3,
    "endingIndex": 3,
    "passed": 1,
    "failed": 2
  }
}
```

```json
{
  "name": "NumericLimitStepLoop",
  "loop": {
    "idx": null,
    "num": 2,
    "endingIndex": 2,
    "passed": 2,
    "failed": 0
  }
}
```

**Pattern:** All summary steps show `num == endingIndex`

### Re-Import Attempt Results

**HTTP Request:**
```
POST https://python.wats.com/api/Report/WSJF
Authorization: Bearer [token]
Content-Type: application/json
```

**HTTP Response:**
```
400 Bad Request

root -> step Loops -> step SequenceCallLoopSequence -> loop SequenceCallLoop: 
  endingIndex is required to be the same as highest index.

root -> step Loops -> step NumericLimitMultipleLoopsSequence -> loop NumericLimitMultipleLoops2: 
  num is required to be one more than endingIndex.
```

---

## Additional Validation Errors

Beyond the loop `num/endingIndex` mismatch, exported files also fail with:

1. **Status Mismatches:**
   ```
   step SinglePassDone: Status cannot be different from measurement status.
   step PassFailStep: Status cannot be different from measurement status.
   ```

2. **Measurement Limit Inconsistencies:**
   ```
   loop SequenceCallLoop2 -> Index 2 -> step StringStep -> stringMeas: 
     limit is required to match Summary step.
   ```

These suggest additional inconsistencies between export and import validation logic.

---

## Impact

### Severity: **Critical**

- **Blocks data migration**: Cannot move reports between WATS instances using export/import
- **Breaks backup/restore workflows**: Exported backups cannot be restored
- **Prevents re-processing**: Historical data cannot be re-submitted for analysis
- **API inconsistency**: Export and import APIs have incompatible data contracts

### Scope

- Affects **all reports with loop steps** (TestStand loops, For/While constructs)
- Observed across **multiple loop types**: SequenceCall loops, NumericLimit loops, PassFail loops, etc.
- **100% failure rate** for server-exported files containing loops in our testing

---

## Workaround

Currently, users must manually transform exported data to match import validation:

```python
# Required transformation for Summary steps
if loop.idx is None and loop.num is not None:
    loop.num = loop.endingIndex + 1  # Change from 3 to 4 for 3 iterations
```

**Note:** This workaround is unreliable as it modifies the reported data semantics.

---

## Recommendation

The WATS development team should:

1. **Align validation logic** between export and import APIs for loop fields
2. **Choose consistent semantics:**
   - **Option A:** `num = iteration count` → Both APIs use `num = endingIndex`
   - **Option B:** `num = array length style` → Both APIs use `num = endingIndex + 1`
3. **Update import validation** to accept server-exported format (backward compatibility)
4. **Review other validation discrepancies** (status matching, measurement limits)

---

## Testing Environment

- **WATS Server:** python.wats.com (version 2026.1.5.324)
- **API Client:** pyWATS Python API (custom client)
- **Test Files:** 
  - Count: 4,597 WSJF files
  - Source: Server exports + customer data
  - Loop failure rate: ~77% (3,554 failures)

---

## Contact Information

For follow-up questions or additional test data:
- **Project:** pyWATS Python API Development
- **Primary Contact:** [Your contact information]
- **Report Date:** February 20, 2026

---

## Appendix: Complete Error Message

```
Report submission failed (400): 
root -> step Pass/Fail tests -> step SinglePassDone: 
  Status cannot be different from measurement status.

root -> step Loops -> step SequenceCallLoopSequence -> loop SequenceCallLoop: 
  endingIndex is required to be the same as highest index.

root -> step Loops -> step SequenceCallLoopSequence -> loop SequenceCallLoop2 -> Index 2 -> step StringStep -> stringMeas: 
  limit is required to match Summary step.

root -> step Loops -> step SequenceCallLoopSequence -> step SequenceCallLoop2 -> step PassFailStep: 
  Status cannot be different from measurement status.

root -> step Loops -> step NumericLimitLoopSequence -> loop NumericLimitStepLoop: 
  endingIndex is required to be the same as highest index.

root -> step Loops -> step NumericLimitMultipleLoopsSequence -> loop NumericLimitMultipleLoops2: 
  endingIndex is required to be the same as highest index.

root -> step Loops -> step NumericLimitMultipleLoopsSequence -> loop NumericLimitMultipleLoops2: 
  num is required to be one more than endingIndex.
```

---

**End of Report**
