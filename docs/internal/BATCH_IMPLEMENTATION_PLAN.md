# Batch Operations Implementation Plan

> **Status**: 📋 PLANNED  
> **Priority**: MEDIUM  
> **Estimated Effort**: 1-2 weeks  
> **Target Version**: 0.2.0  
> **Dependency**: Async API (recommended but not required)

---

## Overview

Batch operations allow users to perform multiple API calls efficiently. Instead of making N individual requests, batch operations can:
1. **Parallelize** - Run requests concurrently (with async)
2. **Bulk endpoint** - Use server-side batch APIs where available
3. **Optimize** - Reduce overhead of connection setup

---

## Current State

| Operation | Current | Problem |
|-----------|---------|---------|
| Get 100 products | 100 sequential calls | Slow (~30s) |
| Submit 50 reports | 50 sequential calls | Very slow (~60s) |
| Update 200 assets | 200 sequential calls | Extremely slow |

**Example of current inefficiency**:
```python
# Current: Sequential, slow
products = []
for pn in part_numbers:  # 100 items
    product = api.product.get_product(pn)  # ~300ms each
    products.append(product)
# Total: ~30 seconds
```

---

## Goals

### Must Have
- [ ] Batch get operations for all domains
- [ ] Batch create/update where server supports
- [ ] Result aggregation with error handling
- [ ] Progress callbacks for long operations
- [ ] Configurable concurrency limits

### Nice to Have
- [ ] Automatic chunking for very large batches
- [ ] Resume capability for interrupted batches
- [ ] Dry-run mode for validation
- [ ] Transaction-like rollback (where supported)

### Out of Scope
- Distributed batch processing
- Background/queued batch jobs
- Cross-domain batch operations

---

## Design Decisions

### Decision 1: Return Type for Batch Operations

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. List of Results** ✅ | `list[Result[T]]` | Preserves order, handles errors | Extra unwrapping |
| B. Dict by key | `dict[str, T]` | Easy lookup | Loses order, awkward errors |
| C. Tuple (success, failures) | `(list[T], list[Error])` | Clear separation | Loses mapping |
| D. BatchResult object | Custom container | Rich metadata | Complex API |

**Decision**: Option A - Return `list[Result[T]]`

**Rationale**:
- Consistent with existing Result types
- Preserves input order
- Each result independently success/failure
- Pattern already familiar from functional programming

```python
results = await api.product.get_products_batch(["P1", "P2", "P3"])
for i, result in enumerate(results):
    if result.is_success:
        print(f"{part_numbers[i]}: {result.value.description}")
    else:
        print(f"{part_numbers[i]}: FAILED - {result.error}")
```

### Decision 2: Sync vs Async Batch

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Sync only | Thread pool | Works without async | Limited parallelism |
| **B. Async only** | `asyncio.gather()` | Best performance | Requires async |
| C. Both | Sync wrapper over async | Flexibility | Complexity |

**Decision**: Option B primarily, with Option C for convenience

**Rationale**:
- True batch benefits require async
- Can provide sync wrapper using `asyncio.run()` for simple cases
- Users who need batch likely can adopt async

### Decision 3: Error Handling Strategy

```python
# Option A: Fail-fast (stop on first error)
results = await api.batch_get(items, fail_fast=True)

# Option B: Collect all errors (default) ✅
results = await api.batch_get(items)  # All attempted

# Option C: Configurable retry per item
results = await api.batch_get(items, retry_failed=True)
```

**Decision**: Option B default, with Option A available

### Decision 4: Concurrency Limiting

```python
# Using semaphore pattern
async def batch_get(self, keys: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_one(key):
        async with semaphore:
            return await self.get(key)
    
    return await asyncio.gather(*[fetch_one(k) for k in keys])
```

**Default concurrency**: 10 (respects rate limiting)

---

## Implementation Phases

### Phase 1: Core Batch Infrastructure (Week 1)

**Scope**: Base batch utilities and product domain

**Files to create**:
- `src/pywats/core/batch.py` (NEW)
- Update domain services with batch methods

**Deliverables**:
```python
# src/pywats/core/batch.py
from typing import TypeVar, Callable, Awaitable, List
from ..shared import Result, Success, Failure
import asyncio

T = TypeVar("T")
K = TypeVar("K")

async def batch_execute(
    keys: List[K],
    operation: Callable[[K], Awaitable[T]],
    max_concurrent: int = 10,
    on_progress: Optional[Callable[[int, int], None]] = None,
) -> List[Result[T]]:
    """
    Execute batch operations with concurrency control.
    
    Args:
        keys: List of input keys
        operation: Async function to call for each key
        max_concurrent: Maximum concurrent operations
        on_progress: Optional callback (completed, total)
    
    Returns:
        List of Results in same order as keys
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    completed = 0
    
    async def execute_one(key: K) -> Result[T]:
        nonlocal completed
        async with semaphore:
            try:
                value = await operation(key)
                return Success(value)
            except Exception as e:
                return Failure.from_exception(e)
            finally:
                completed += 1
                if on_progress:
                    on_progress(completed, len(keys))
    
    tasks = [execute_one(k) for k in keys]
    return await asyncio.gather(*tasks)
```

**Product Service Batch Methods**:
```python
# src/pywats/domains/product/async_service.py
class AsyncProductService:
    async def get_products_batch(
        self,
        part_numbers: List[str],
        max_concurrent: int = 10,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> List[Result[Product]]:
        """
        Fetch multiple products concurrently.
        
        Args:
            part_numbers: List of part numbers to fetch
            max_concurrent: Max concurrent requests (default: 10)
            on_progress: Progress callback (completed, total)
        
        Returns:
            List of Result[Product] in same order as input
        
        Example:
            >>> results = await api.product.get_products_batch(
            ...     ["PART-1", "PART-2", "PART-3"]
            ... )
            >>> for pn, result in zip(part_numbers, results):
            ...     if result.is_success:
            ...         print(f"{pn}: {result.value.description}")
        """
        return await batch_execute(
            keys=part_numbers,
            operation=self.get_product,
            max_concurrent=max_concurrent,
            on_progress=on_progress,
        )
```

**Acceptance Criteria**:
- [ ] `batch_execute()` utility function works
- [ ] Product batch methods implemented
- [ ] Progress callbacks work
- [ ] Errors don't break entire batch
- [ ] Concurrency limiting works

### Phase 2: All Domain Batch Methods (Week 1-2)

**Scope**: Add batch methods to all domains

**Methods to add**:

| Domain | Batch Method | Description |
|--------|--------------|-------------|
| Product | `get_products_batch(pns)` | Fetch multiple products |
| Asset | `get_assets_batch(ids)` | Fetch multiple assets |
| Production | `get_units_batch(sns)` | Fetch multiple units |
| Report | `get_reports_batch(ids)` | Fetch multiple reports |
| Report | `submit_reports_batch(reports)` | Submit multiple reports |
| Analytics | `get_yield_batch(filters)` | Multiple yield queries |

**Acceptance Criteria**:
- [ ] All read domains have batch get
- [ ] Report domain has batch submit
- [ ] Consistent API across domains

### Phase 3: Sync Wrappers (Week 2)

**Scope**: Provide sync API for batch operations

```python
# src/pywats/domains/product/service.py
class ProductService:
    def get_products_batch(
        self,
        part_numbers: List[str],
        max_concurrent: int = 10,
    ) -> List[Result[Product]]:
        """
        Fetch multiple products (sync wrapper over async).
        
        Note: For best performance, use AsyncPyWATS directly.
        """
        import asyncio
        
        async def _batch():
            async with AsyncProductService(self._client) as svc:
                return await svc.get_products_batch(
                    part_numbers, 
                    max_concurrent
                )
        
        return asyncio.run(_batch())
```

**Acceptance Criteria**:
- [ ] Sync batch methods work
- [ ] Still faster than sequential (uses async internally)
- [ ] Clear docs that async is preferred

### Phase 4: Advanced Features (Week 2)

**Scope**: Chunking, resume, progress

**Auto-Chunking**:
```python
async def get_products_batch(
    self,
    part_numbers: List[str],
    chunk_size: int = 100,  # Process in chunks
    max_concurrent: int = 10,
) -> List[Result[Product]]:
    results = []
    for i in range(0, len(part_numbers), chunk_size):
        chunk = part_numbers[i:i + chunk_size]
        chunk_results = await batch_execute(
            chunk, self.get_product, max_concurrent
        )
        results.extend(chunk_results)
    return results
```

**Resume Capability**:
```python
async def get_products_batch(
    self,
    part_numbers: List[str],
    skip_completed: Optional[Set[str]] = None,  # Already done
) -> List[Result[Product]]:
    to_fetch = [pn for pn in part_numbers if pn not in (skip_completed or set())]
    ...
```

---

## Usage Examples

### Basic Batch Get

```python
from pywats import AsyncPyWATS

async def main():
    async with AsyncPyWATS(base_url="...", token="...") as api:
        part_numbers = ["WIDGET-001", "WIDGET-002", "WIDGET-003"]
        
        results = await api.product.get_products_batch(part_numbers)
        
        for pn, result in zip(part_numbers, results):
            if result.is_success:
                print(f"✓ {pn}: {result.value.description}")
            else:
                print(f"✗ {pn}: {result.error}")
```

### With Progress Callback

```python
from pywats import AsyncPyWATS

async def main():
    async with AsyncPyWATS(base_url="...", token="...") as api:
        part_numbers = [f"PART-{i:04d}" for i in range(1000)]
        
        def on_progress(completed, total):
            pct = (completed / total) * 100
            print(f"\rProgress: {completed}/{total} ({pct:.1f}%)", end="")
        
        results = await api.product.get_products_batch(
            part_numbers,
            max_concurrent=20,
            on_progress=on_progress,
        )
        
        print(f"\nCompleted: {sum(1 for r in results if r.is_success)}")
        print(f"Failed: {sum(1 for r in results if r.is_failure)}")
```

### Batch Report Submission

```python
from pywats import AsyncPyWATS
from pywats.models import UUTReport

async def submit_test_results(reports: list[UUTReport]):
    async with AsyncPyWATS(base_url="...", token="...") as api:
        results = await api.report.submit_reports_batch(
            reports,
            max_concurrent=5,  # Lower for writes
        )
        
        successful = [r.value for r in results if r.is_success]
        failed = [(reports[i], r.error) for i, r in enumerate(results) if r.is_failure]
        
        print(f"Submitted: {len(successful)}")
        for report, error in failed:
            print(f"Failed {report.serial_number}: {error}")
```

### Sync Batch (Convenience)

```python
from pywats import pyWATS

# Sync API with batch (uses async internally)
api = pyWATS(base_url="...", token="...")

results = api.product.get_products_batch(
    ["PART-1", "PART-2", "PART-3"],
    max_concurrent=10,
)

for result in results:
    if result.is_success:
        print(result.value.part_number)
```

---

## API Reference

### BatchResult Type

```python
from pywats.shared import Result, Success, Failure

# Result is a union type
Result[T] = Success[T] | Failure

# Success contains the value
class Success(Generic[T]):
    value: T
    is_success: bool = True
    is_failure: bool = False

# Failure contains error info
class Failure:
    error: Exception
    error_code: ErrorCode
    message: str
    is_success: bool = False
    is_failure: bool = True
```

### Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_concurrent` | `int` | 10 | Maximum parallel requests |
| `on_progress` | `Callable[[int, int], None]` | None | Progress callback |
| `chunk_size` | `int` | 100 | Items per chunk (large batches) |
| `fail_fast` | `bool` | False | Stop on first error |

---

## Server-Side Batch Endpoints

Some WATS endpoints may support batch operations natively:

| Endpoint | Native Batch? | Notes |
|----------|---------------|-------|
| GET /api/Product | ✅ Returns all | Use filter instead of batch get |
| POST /api/Report | ❌ Single | Must use client-side batch |
| GET /api/Unit | ✅ Query | Use filter with multiple SNs |

Where server supports batch, use it:
```python
# Instead of:
results = await api.product.get_products_batch(["A", "B", "C"])

# Use filter when possible:
products = await api.product.get_products(filter={"partNumbers": ["A", "B", "C"]})
```

---

## Performance Expectations

| Batch Size | Sequential | Batch (10 concurrent) | Speedup |
|------------|------------|----------------------|---------|
| 10 items | ~3s | ~0.3s | 10x |
| 100 items | ~30s | ~3s | 10x |
| 1000 items | ~5min | ~30s | 10x |

*Assumes 300ms average response time*

---

## Testing Strategy

### Unit Tests

```python
@pytest.mark.asyncio
async def test_batch_get_products():
    """Test batch product fetch."""
    async with AsyncPyWATS(...) as api:
        results = await api.product.get_products_batch(
            ["PART-1", "PART-2", "NONEXISTENT"]
        )
        
        assert len(results) == 3
        assert results[0].is_success
        assert results[1].is_success
        assert results[2].is_failure

@pytest.mark.asyncio
async def test_batch_concurrency_limit():
    """Test that concurrency is limited."""
    concurrent_count = 0
    max_concurrent = 0
    
    async def mock_get(key):
        nonlocal concurrent_count, max_concurrent
        concurrent_count += 1
        max_concurrent = max(max_concurrent, concurrent_count)
        await asyncio.sleep(0.1)
        concurrent_count -= 1
        return key
    
    await batch_execute(
        keys=list(range(20)),
        operation=mock_get,
        max_concurrent=5,
    )
    
    assert max_concurrent <= 5

@pytest.mark.asyncio
async def test_batch_progress_callback():
    """Test progress callback is called."""
    progress_calls = []
    
    def on_progress(completed, total):
        progress_calls.append((completed, total))
    
    await api.product.get_products_batch(
        ["P1", "P2", "P3"],
        on_progress=on_progress,
    )
    
    assert len(progress_calls) == 3
    assert progress_calls[-1] == (3, 3)
```

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Rate limit exceeded | Medium | Medium | Respect rate limiter, lower default concurrency |
| Memory issues with large batches | Low | Medium | Chunking, streaming results |
| Server overload | Low | High | Configurable concurrency, backoff |
| Partial failures confusing | Medium | Low | Clear Result type, good docs |

---

## Timeline

| Day | Deliverable |
|-----|-------------|
| 1-2 | Core batch_execute utility |
| 3-4 | Product batch methods |
| 5-6 | All domain batch methods |
| 7-8 | Sync wrappers |
| 9-10 | Testing & documentation |

---

## Success Metrics

- [ ] 10x speedup for batch operations vs sequential
- [ ] Zero rate limit violations with default settings
- [ ] All batch methods return `List[Result[T]]`
- [ ] Progress callbacks work correctly
- [ ] Documentation and examples complete
