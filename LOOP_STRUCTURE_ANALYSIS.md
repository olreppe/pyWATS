# Loop Structure Analysis from Server Example

**Report ID:** 2961a76f-5631-49c6-8e93-15fe31635531  
**Created:** 2026-02-03  
**Status:** ✅ BREAKTHROUGH - Loop structure reverse-engineered from valid server example

---

## Key Finding: Two Types of Loop Steps

The WATS server expects **two distinct loop step types**:

### 1. Summary Step (Loop Header)

**Purpose:** Provides aggregated statistics for ALL iterations in the loop

**Loop Object Structure:**
```json
"loop": {
  "idx": null,         // ✅ MUST be null for summary steps
  "num": 3,            // ✅ Total number of iterations
  "endingIndex": 3,    // ✅ One past the last iteration index (if idx goes 0,1,2 then endingIndex is 3)
  "passed": 1,         // ✅ Count of iterations with status "P"
  "failed": 2          // ✅ Count of iterations with status "F"
}
```

**Example from Server (Step ID 50):**
```json
{
  "id": 50,
  "group": "M",
  "stepType": "SequenceCall",
  "loop": {
    "idx": null,
    "num": 3,
    "endingIndex": 3,
    "passed": 1,
    "failed": 2
  },
  "name": "SequenceCallLoop",
  "status": "F",
  "totTime": 0.0,
  "causedUUTFailure": false,
  "steps": [
    // Template steps (51-55) - not iterations!
  ]
}
```

**Critical Rules:**
- `idx` MUST be `null`
- `num` = total number of iterations (array length)
- `endingIndex` = `num` (one past last index, like array.length)
- `passed` = count of iteration steps with `status: "P"`
- `failed` = count of iteration steps with `status: "F"`
- `status` of summary step = "F" if any iteration failed, otherwise "P"
- **Contains template/structure steps, NOT the actual iteration steps**

---

### 2. Iteration Steps (Loop Body Instances)

**Purpose:** Individual execution instances of the loop body

**Loop Object Structure:**
```json
"loop": {
  "idx": 0,            // ✅ Specific iteration index (0, 1, 2, ...)
  "num": null,         // ✅ MUST be null for iteration steps
  "endingIndex": null, // ✅ MUST be null
  "passed": null,      // ✅ MUST be null
  "failed": null       // ✅ MUST be null
}
```

**Example from Server (Step ID 56 - Iteration 0):**
```json
{
  "id": 56,
  "group": "M",
  "stepType": "SequenceCall",
  "loop": {
    "idx": 0,
    "num": null,
    "endingIndex": null,
    "passed": null,
    "failed": null
  },
  "name": "SequenceCallLoop",
  "status": "F",
  "totTime": 0.0,
  "causedUUTFailure": false,
  "steps": [
    // Actual execution steps for iteration 0
  ]
}
```

**Critical Rules:**
- `idx` MUST be a specific index value (0-based: 0, 1, 2, ...)
- `num`, `endingIndex`, `passed`, `failed` MUST all be `null`
- `status` reflects the actual pass/fail of this iteration
- **Contains the actual executed steps for this iteration**

---

## Complete Loop Example Structure

```json
{
  "steps": [
    // SUMMARY STEP (Header)
    {
      "id": 50,
      "stepType": "SequenceCall",
      "loop": {
        "idx": null,       // Summary indicator
        "num": 3,          // 3 iterations total
        "endingIndex": 3,  // Length (one past last index)
        "passed": 1,       // 1 passed (idx 1)
        "failed": 2        // 2 failed (idx 0, 2)
      },
      "name": "SequenceCallLoop",
      "status": "F",       // Failed because 2 iterations failed
      "steps": [
        // Template steps (not iterations)
      ]
    },
    
    // ITERATION 0
    {
      "id": 56,
      "stepType": "SequenceCall",
      "loop": {
        "idx": 0,          // First iteration
        "num": null,
        "endingIndex": null,
        "passed": null,
        "failed": null
      },
      "name": "SequenceCallLoop",
      "status": "F",       // This iteration failed
      "steps": [
        // Actual executed steps for idx 0
      ]
    },
    
    // ITERATION 1
    {
      "id": 62,
      "stepType": "SequenceCall",
      "loop": {
        "idx": 1,          // Second iteration
        "num": null,
        "endingIndex": null,
        "passed": null,
        "failed": null
      },
      "name": "SequenceCallLoop",
      "status": "P",       // This iteration passed
      "steps": [
        // Actual executed steps for idx 1
      ]
    },
    
    // ITERATION 2
    {
      "id": 66,
      "stepType": "SequenceCall",
      "loop": {
        "idx": 2,          // Third iteration
        "num": null,
        "endingIndex": null,
        "passed": null,
        "failed": null
      },
      "name": "SequenceCallLoop",
      "status": "F",       // This iteration failed
      "steps": [
        // Actual executed steps for idx 2
      ]
    }
  ]
}
```

---

## Validation Rules Explained

Based on server semantic validation errors we encountered:

### Rule 1: "endingIndex required to be same as highest index"

**MISUNDERSTOOD!** This error message is misleading. From the server example:
- Highest `idx` value: 2
- `endingIndex` in summary: 3

**Correct interpretation:** `endingIndex` should be **one more than the highest idx** (like array length).
- If iterations are idx 0, 1, 2 → endingIndex = 3
- If iterations are idx 0, 1, 2, 3, 4 → endingIndex = 5

### Rule 2: "num required to be one more than endingIndex"

**MISUNDERSTOOD!** From the server example:
- `num`: 3
- `endingIndex`: 3

**Correct interpretation:** `num` should **equal** `endingIndex` (both represent the total iteration count).
- num = total iterations
- endingIndex = one past last index = total iterations
- **Therefore: num = endingIndex**

### Rule 3: "step X in Summary step requires a match"

**Correct!** The summary step's substeps must match the structure/template that iterations follow. However:
- Summary step contains the **template structure**
- Iteration steps contain **actual execution data**
- Measurements in iterations can vary (different values, some steps may be skipped, etc.)

### Rule 4: passed + failed counts

**From server example:**
- Iteration 0 (id 56): status "F" → failed
- Iteration 1 (id 62): status "P" → passed
- Iteration 2 (id 66): status "F" → failed
- Summary: passed=1, failed=2 ✅

**Rule:** Count the `status` field of each iteration step:
- `passed` = count of iteration steps with `status: "P"`
- `failed` = count of iteration steps with `status: "F"`

---

## Implications for Converter

### Current State
Our WSJF files from customers contain:
- Only **iteration steps** (idx: 0, 1, 2, ...)
- **NO summary steps**

### What We Need to Do

**Phase 1: Detect Loops**
1. Group consecutive same-name steps with loop objects
2. Identify highest idx value
3. Count passed/failed by status

**Phase 2: Generate Summary Step**
```python
# Pseudocode
iterations = [step for step in steps if step.loop and step.loop.idx is not None]
summary_step = create_summary_step(
    name=iterations[0].name,
    loop=LoopInfo(
        idx=None,
        num=len(iterations),
        endingIndex=len(iterations),  # Same as num!
        passed=sum(1 for it in iterations if it.status == "P"),
        failed=sum(1 for it in iterations if it.status == "F")
    ),
    steps=extract_template_steps(iterations[0])  # Use first iteration as template
)
```

**Phase 3: Insert Summary Before Iterations**
```python
# Insert summary step before first iteration
steps.insert(first_iteration_index, summary_step)
```

### Complexity Assessment

**HIGH COMPLEXITY - Multi-week effort:**
1. **Loop detection algorithm** - Group by name + loop presence
2. **Nested loop handling** - Summary steps at each level
3. **Template extraction** - Which iteration to use as template?
4. **ID management** - Renumber all subsequent step IDs
5. **Status calculation** - Handle complex pass/fail logic
6. **Edge cases:**
   - Partial loops (not all iterations present)
   - Different step structures across iterations
   - Missing loop objects
   - Mixed loop/non-loop steps

---

## Recommended Approach

### Option A: Full Implementation (4-6 weeks)
Build complete loop transformer with:
- Loop detection
- Summary generation
- Template extraction
- Nested loop support
- Comprehensive testing

**Pros:** Processes all files  
**Cons:** Complex, time-consuming, high risk

### Option B: Document Limitations (1-2 days)
Accept that files with complex loops will fail:
- Document loop requirements
- Process only non-loop or simple-loop files
- 20% success rate may be acceptable for current phase

**Pros:** Ship quickly, focus on other issues  
**Cons:** 80% of files still fail

### Option C: Hybrid Approach (1-2 weeks)
Implement basic single-level loop transformer:
- Detect simple single-level loops
- Generate basic summary steps
- Skip nested/complex loops

**Pros:** Balance complexity vs coverage  
**Cons:** Still doesn't handle all cases

---

## User's Hypothesis - VALIDATED ✅

> "I think the point of the summary step is to state how many loops in total 
> (can exceed the logged loops) and a failure summary"

**CORRECT!** The summary step:
- States total iterations (`num`)
- Provides failure summary (`passed`, `failed`)
- CAN exceed logged loops if using `endingIndex` > `num` (though server example shows them equal)

---

## Next Steps

1. **Discuss approach with user** - Full vs Hybrid vs Document limitations
2. **If proceeding:** Create loop transformer specification
3. **If deferring:** Document loop limitations for users
4. **Regardless:** Update CHANGELOG with current 20% success milestone

**Decision needed:** How much engineering effort to invest in loop transformation?

