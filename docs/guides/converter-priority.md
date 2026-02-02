# Converter Priority Guide

This guide explains how to use converter priority to ensure critical real-time production data is processed before low-priority batch uploads.

## Overview

PyWATS converters support priority-based processing to prevent large batch uploads from blocking real-time production data. The system uses a heap-based priority queue where lower numbers = higher priority.

**Priority Scale:**
- **1-2**: Critical real-time production data (highest priority)
- **3-4**: Important converters requiring fast processing
- **5**: Normal converters (default if not specified)
- **6-7**: Lower priority background processing
- **8-10**: Batch uploads, historical data migrations (lowest priority)

## Use Cases

### Problem: Batch Uploads Blocking Real-Time Data

**Scenario:** You have two converters:
1. Real-time production data from test stations (needs immediate upload)
2. Historical data batch upload (10,000 files)

Without priority, the batch upload can block real-time data for hours.

**Solution:** Set different priorities:

```json
{
  "converters": [
    {
      "name": "Real-Time Production",
      "type": "wats_xml",
      "priority": 1,
      "watch_folder": "C:\\Production\\Realtime",
      ...
    },
    {
      "name": "Historical Batch Upload",
      "type": "csv_batch", 
      "priority": 8,
      "watch_folder": "C:\\Production\\Archive",
      ...
    }
  ]
}
```

**Result:** Real-time files are always processed first, even if thousands of batch files are queued.

## Configuration

### Via Configuration File

Edit your `config.json` (typically at `~/.pywats/config.json`):

```json
{
  "converters": [
    {
      "name": "Critical Production",
      "module_path": "my_converters.ProductionConverter",
      "priority": 1,
      "watch_folder": "/data/production",
      "enabled": true
    },
    {
      "name": "Background Migration",
      "module_path": "my_converters.MigrationConverter", 
      "priority": 9,
      "watch_folder": "/data/migration",
      "enabled": true
    }
  ]
}
```

### Via GUI

When configuring a converter in the PyWATS Client GUI:

1. Open **Converters** page
2. Select your converter or create a new one
3. Set **Priority** field (1-10)
4. Save configuration

### In Code (Advanced)

If you're instantiating converters programmatically:

```python
from pywats_client.converters import FileConverter

class MyConverter(FileConverter):
    def __init__(self):
        super().__init__(priority=1)  # High priority
    
    # ... rest of converter implementation
```

**Note:** Priority from configuration file overrides the code-level default.

## Architecture

### How Priority Works

1. **Configuration Loading:**
   - AsyncConverterPool loads converter configs from `config.json`
   - Reads `priority` field (defaults to 5 if not specified)

2. **Converter Instantiation:**
   - Creates converter instance
   - Sets `converter.priority` from config

3. **File Detection:**
   - Watchdog detects new file
   - `AsyncConversionItem` created with converter's priority
   - Item added to priority queue

4. **Processing:**
   - MemoryQueue uses min-heap for priority ordering
   - Lower priority numbers dequeued first
   - Same-priority items processed FIFO

### Queue Flow

```
File Created
    ↓
AsyncConversionItem(file, converter, priority=converter.priority)
    ↓
AsyncQueueAdapter.put_nowait(item, priority)
    ↓
MemoryQueue (heap-based)
    ↓
AsyncConverterPool processes highest priority first
    ↓
Report submitted to WATS
```

### Components

- **MemoryQueue**: Thread-safe heap-based priority queue (foundation)
- **AsyncQueueAdapter**: Bridges threading (MemoryQueue) to asyncio (AsyncConverterPool)
- **AsyncConverterPool**: Manages converter workers and priority-based task distribution
- **ConverterConfig**: Stores priority setting (persisted in config.json)

## Best Practices

### Priority Assignment Guidelines

1. **Real-Time Production (1-2)**
   - Live test station data
   - Production line monitoring
   - Time-critical quality checks

2. **Important Processing (3-4)**
   - End-of-shift reports
   - Hourly aggregations
   - Customer-facing dashboards

3. **Normal Processing (5 - default)**
   - Standard file conversions
   - Regular batch jobs
   - Development/testing converters

4. **Background Processing (6-7)**
   - Analytics processing
   - Report generation
   - Non-urgent aggregations

5. **Batch Uploads (8-10)**
   - Historical data migrations
   - Archive processing
   - Cleanup operations

### Common Patterns

#### Pattern 1: Tiered Processing

```json
{
  "converters": [
    {"name": "Station_1_Realtime", "priority": 1},
    {"name": "Station_2_Realtime", "priority": 1},
    {"name": "Station_3_Realtime", "priority": 1},
    {"name": "Hourly_Aggregation", "priority": 4},
    {"name": "Daily_Reports", "priority": 6},
    {"name": "Historical_Import", "priority": 9}
  ]
}
```

#### Pattern 2: Customer vs Internal

```json
{
  "converters": [
    {"name": "Customer_Production", "priority": 1},
    {"name": "Internal_Testing", "priority": 7},
    {"name": "Development", "priority": 9}
  ]
}
```

#### Pattern 3: Time-Sensitive vs Batch

```json
{
  "converters": [
    {"name": "Live_Test_Results", "priority": 1},
    {"name": "Nightly_Archive_Import", "priority": 8}
  ]
}
```

## Monitoring

### Check Converter Priority

View configured priorities:

```bash
pywats-client converters list
```

### Queue Status

Monitor queue depth and priority distribution:

```bash
pywats-client queue status
pywats-client queue list
```

### Logs

Priority information appears in logs:

```
2026-02-02 10:15:23 [INFO] Queued (priority=1): test_result.xml via Real-Time Production
2026-02-02 10:15:24 [INFO] Queued (priority=8): archive_001.csv via Historical Batch
2026-02-02 10:15:25 [DEBUG] Processing priority=1 item first
```

## Troubleshooting

### Low-Priority Items Never Process

**Symptom:** Batch uploads stay in queue indefinitely.

**Cause:** High-priority converters continuously adding new items.

**Solution:**
- Reduce high-priority converter volume (filter files, adjust watch folders)
- Increase `max_concurrent` workers in AsyncConverterPool
- Temporarily disable or adjust priority of batch converters

### Priority Not Taking Effect

**Symptom:** Items processed in wrong order.

**Checklist:**
1. ✅ Priority field set in config.json?
2. ✅ Service restarted after config change?
3. ✅ Using AsyncConverterPool (not legacy queue)?
4. ✅ pyWATS version ≥ 0.3.0b1?

**Debug:**
```bash
# Verify config
cat ~/.pywats/config.json | grep -A 10 "converters"

# Check logs for priority values
tail -f ~/.pywats/logs/pywats-client.log | grep priority
```

### All Items Have Same Priority

**Symptom:** Queue behaves like FIFO despite different priority settings.

**Cause:** Priority not set in config, all defaulting to 5.

**Solution:** Explicitly set priority in converter configs (see Configuration section above).

## Migration Notes

### Upgrading from Previous Versions

If upgrading from pyWATS < 0.3.0:

1. **Configuration:** Priority field is optional, defaults to 5 if not specified
2. **Behavior:** No breaking changes - existing converters work without modification
3. **Performance:** Priority-based queue is more efficient than previous FIFO queue

### Adding Priority to Existing Converters

Edit `~/.pywats/config.json`:

```json
{
  "converters": [
    {
      "name": "My Existing Converter",
      // ... existing fields ...
      "priority": 1  // ← ADD THIS LINE
    }
  ]
}
```

Restart service:

```bash
pywats-client service restart
```

## Related Documentation

- [Queue Architecture](../internal_documentation/QUEUE_ARCHITECTURE.md) - Technical deep-dive
- [AsyncQueueAdapter API](../api/pywats.queue.md#asyncqueueadapter) - Developer reference
- [Thread Safety Guide](thread-safety.md) - AsyncQueueAdapter thread safety guarantees
- [Getting Started](../getting-started.md) - Basic converter setup

## Support

For questions or issues:

1. Check logs: `~/.pywats/logs/pywats-client.log`
2. Review configuration: `~/.pywats/config.json`
3. Test queue: `pywats-client queue status`
4. Open issue: https://github.com/olreppe/pyWATS/issues
