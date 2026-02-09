# pywats_client.queue - Class Reference

Auto-generated class reference for `pywats_client.queue`.

---

## `queue.persistent_queue`

### `PersistentQueue(MemoryQueue)`

_File-backed persistent queue extending MemoryQueue._

**Properties:**
- `queue_dir`

**Methods:**
- `add(data: Any, item_id: Optional[...], priority: int, max_attempts: Optional[...], metadata: Optional[...]) -> QueueItem`
- `clear(status: Optional[...]) -> int`
- `process_pending(processor: callable, include_failed: bool) -> Dict[...]`
- `remove(item_id: str) -> bool`
- `update(item: QueueItem) -> Any`

---
