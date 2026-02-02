"""
Example: Batch operations in pyWATS

This example demonstrates:
- Bulk create/update operations
- Parallel processing of requests
- Progress tracking for batch operations
- Error handling for batch processing
- Performance optimization techniques

Prerequisites:
- pyWATS installed and configured
"""

from pywats import Client
from pywats.core.exceptions import PyWATSError, ValidationError
import logging
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def bulk_create_sequential(client: Client, items: List[Dict[str, Any]]) -> List[Dict]:
    """
    Create multiple items sequentially.
    
    Simple but slow - processes one item at a time.
    """
    logger.info(f"\n=== Sequential Bulk Create ({len(items)} items) ===")
    
    results = []
    start_time = time.time()
    
    for i, item in enumerate(items, 1):
        try:
            logger.info(f"Creating item {i}/{len(items)}: {item.get('name', 'unknown')}")
            # Simulated API call
            result = {"id": f"ITEM-{i}", **item, "created": True}
            results.append(result)
            
        except PyWATSError as e:
            logger.error(f"Failed to create item {i}: {e}")
            results.append({"error": str(e), **item})
    
    elapsed = time.time() - start_time
    logger.info(f"Completed in {elapsed:.2f}s ({elapsed/len(items):.2f}s per item)")
    logger.info(f"Success: {sum(1 for r in results if 'created' in r)}/{len(items)}")
    
    return results


def bulk_create_parallel(client: Client, items: List[Dict[str, Any]], max_workers: int = 5) -> List[Dict]:
    """
    Create multiple items in parallel using ThreadPoolExecutor.
    
    Much faster for I/O-bound operations like API calls.
    """
    logger.info(f"\n=== Parallel Bulk Create ({len(items)} items, {max_workers} workers) ===")
    
    def create_single_item(item_with_index):
        """Create a single item (used by thread pool)."""
        index, item = item_with_index
        try:
            logger.info(f"Creating item {index + 1}/{len(items)}: {item.get('name', 'unknown')}")
            # Simulated API call
            time.sleep(0.1)  # Simulate network delay
            result = {"id": f"ITEM-{index + 1}", **item, "created": True}
            return result
            
        except PyWATSError as e:
            logger.error(f"Failed to create item {index + 1}: {e}")
            return {"error": str(e), **item}
    
    results = [None] * len(items)  # Preserve order
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_index = {
            executor.submit(create_single_item, (i, item)): i
            for i, item in enumerate(items)
        }
        
        # Collect results as they complete
        completed = 0
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            results[index] = future.result()
            completed += 1
            
            if completed % 10 == 0 or completed == len(items):
                logger.info(f"Progress: {completed}/{len(items)} completed")
    
    elapsed = time.time() - start_time
    logger.info(f"Completed in {elapsed:.2f}s ({elapsed/len(items):.2f}s per item)")
    logger.info(f"Success: {sum(1 for r in results if r and 'created' in r)}/{len(items)}")
    logger.info(f"Speedup: {(len(items) * 0.1 / elapsed):.1f}x vs sequential")
    
    return results


def batch_with_progress_tracking(client: Client, items: List[Dict[str, Any]]) -> List[Dict]:
    """
    Batch processing with detailed progress tracking.
    """
    logger.info(f"\n=== Batch with Progress Tracking ({len(items)} items) ===")
    
    results = []
    stats = {
        "total": len(items),
        "completed": 0,
        "succeeded": 0,
        "failed": 0,
        "start_time": time.time()
    }
    
    def print_progress():
        """Print current progress."""
        elapsed = time.time() - stats["start_time"]
        rate = stats["completed"] / elapsed if elapsed > 0 else 0
        eta = (stats["total"] - stats["completed"]) / rate if rate > 0 else 0
        
        logger.info(
            f"Progress: {stats['completed']}/{stats['total']} "
            f"(✓ {stats['succeeded']} / ✗ {stats['failed']}) "
            f"[{rate:.1f} items/s, ETA: {eta:.0f}s]"
        )
    
    for i, item in enumerate(items):
        try:
            # Simulated API call
            result = {"id": f"ITEM-{i+1}", **item, "created": True}
            results.append(result)
            stats["succeeded"] += 1
            
        except PyWATSError as e:
            logger.error(f"Failed item {i+1}: {e}")
            results.append({"error": str(e), **item})
            stats["failed"] += 1
        
        finally:
            stats["completed"] += 1
            
            # Print progress every 10 items or on completion
            if stats["completed"] % 10 == 0 or stats["completed"] == stats["total"]:
                print_progress()
    
    return results


def batch_with_error_handling(client: Client, items: List[Dict[str, Any]]) -> Dict[str, List]:
    """
    Batch processing with comprehensive error handling.
    
    Returns:
        Dictionary with 'succeeded', 'failed', and 'retried' lists
    """
    logger.info(f"\n=== Batch with Error Handling ({len(items)} items) ===")
    
    results = {
        "succeeded": [],
        "failed": [],
        "retried": []
    }
    
    for i, item in enumerate(items, 1):
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Processing item {i}/{len(items)} (attempt {attempt + 1})")
                
                # Simulated API call with validation
                if not item.get("name"):
                    raise ValidationError("Name is required", field_errors={"name": "Required"})
                
                result = {"id": f"ITEM-{i}", **item, "created": True}
                results["succeeded"].append(result)
                
                if attempt > 0:
                    results["retried"].append(result)
                
                break  # Success - don't retry
                
            except ValidationError as e:
                # Don't retry validation errors
                logger.error(f"Validation error for item {i}: {e}")
                results["failed"].append({"error": str(e), **item})
                break
                
            except PyWATSError as e:
                # Retry other errors
                if attempt < max_retries - 1:
                    logger.warning(f"Retrying item {i} after error: {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed item {i} after {max_retries} attempts: {e}")
                    results["failed"].append({"error": str(e), **item, "attempts": max_retries})
    
    # Summary
    logger.info(f"\nResults:")
    logger.info(f"  Succeeded: {len(results['succeeded'])}")
    logger.info(f"  Failed: {len(results['failed'])}")
    logger.info(f"  Retried: {len(results['retried'])}")
    
    return results


def batch_with_chunking(client: Client, items: List[Dict[str, Any]], chunk_size: int = 50) -> List[Dict]:
    """
    Process large batches in chunks to avoid overwhelming the API.
    """
    logger.info(f"\n=== Batch with Chunking ({len(items)} items, chunks of {chunk_size}) ===")
    
    all_results = []
    num_chunks = (len(items) + chunk_size - 1) // chunk_size
    
    for chunk_num in range(num_chunks):
        start_idx = chunk_num * chunk_size
        end_idx = min((chunk_num + 1) * chunk_size, len(items))
        chunk = items[start_idx:end_idx]
        
        logger.info(f"\nProcessing chunk {chunk_num + 1}/{num_chunks} ({len(chunk)} items)")
        
        # Process chunk
        chunk_results = []
        for item in chunk:
            try:
                result = {"id": f"ITEM-{start_idx + len(chunk_results) + 1}", **item, "created": True}
                chunk_results.append(result)
            except PyWATSError as e:
                chunk_results.append({"error": str(e), **item})
        
        all_results.extend(chunk_results)
        
        logger.info(f"Chunk {chunk_num + 1} completed: {len(chunk_results)} items processed")
        
        # Pause between chunks to avoid rate limiting
        if chunk_num < num_chunks - 1:
            logger.info("Pausing 1s before next chunk...")
            time.sleep(1)
    
    logger.info(f"\nAll chunks completed: {len(all_results)} total items")
    return all_results


def batch_update_optimization(client: Client, updates: List[Dict[str, Any]]) -> List[Dict]:
    """
    Optimized batch updates using conditional updates.
    
    Only sends updates if the data has actually changed.
    """
    logger.info(f"\n=== Optimized Batch Updates ({len(updates)} items) ===")
    
    results = []
    skipped = 0
    
    for update in updates:
        item_id = update.get("id")
        
        # Fetch current state (this would use cache in production)
        current = {"id": item_id, "name": "Old Name", "value": 100}
        
        # Check if update is needed
        needs_update = False
        for key, value in update.items():
            if key != "id" and current.get(key) != value:
                needs_update = True
                break
        
        if needs_update:
            logger.info(f"Updating {item_id}: {update}")
            # Perform update
            result = {**current, **update, "updated": True}
            results.append(result)
        else:
            logger.debug(f"Skipping {item_id}: no changes")
            results.append(current)
            skipped += 1
    
    logger.info(f"Updates completed: {len(results) - skipped} updated, {skipped} skipped")
    return results


def main():
    """Run all batch operation examples."""
    
    # Create a mock client
    client = Client(base_url="https://api.example.com", auth_token="dummy")
    
    # Generate sample data
    sample_items = [
        {"name": f"Item {i}", "value": i * 10, "category": f"cat{i % 5}"}
        for i in range(1, 51)
    ]
    
    # Example 1: Sequential processing
    bulk_create_sequential(client, sample_items[:10])
    
    # Example 2: Parallel processing
    bulk_create_parallel(client, sample_items[:20], max_workers=5)
    
    # Example 3: Progress tracking
    batch_with_progress_tracking(client, sample_items[:15])
    
    # Example 4: Error handling
    # Add some invalid items
    items_with_errors = sample_items[:10].copy()
    items_with_errors[5] = {"value": 50}  # Missing name
    batch_with_error_handling(client, items_with_errors)
    
    # Example 5: Chunked processing
    batch_with_chunking(client, sample_items, chunk_size=15)
    
    # Example 6: Optimized updates
    sample_updates = [
        {"id": f"ITEM-{i}", "name": f"Updated {i}", "value": i * 20}
        for i in range(1, 21)
    ]
    batch_update_optimization(client, sample_updates)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("pyWATS Batch Operations Examples")
    print("="*60)
    
    main()
    
    print("\n" + "="*60)
    print("Batch operations examples completed!")
    print("="*60 + "\n")
    
    print("\nKey Takeaways:")
    print("1. Use parallel processing for I/O-bound operations")
    print("2. Track progress for long-running batch jobs")
    print("3. Handle errors gracefully with retries")
    print("4. Use chunking for very large batches")
    print("5. Optimize by skipping unnecessary updates")
    print("6. Monitor rate limits and add delays if needed")
