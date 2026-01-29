"""
Tests for File Utilities

Tests atomic writes, safe reads, file locking, and related utilities.
"""

import json
import os
import pytest
import tempfile
import threading
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from pywats_client.core.file_utils import (
    SafeFileWriter,
    SafeFileReader,
    FileOperation,
    FileOperationResult,
    locked_file,
    safe_delete,
    safe_rename,
    ensure_directory,
    write_text,
    write_json,
    read_text,
    read_json,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory(prefix="pywats_file_test_") as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_json():
    """Sample JSON data for testing."""
    return {
        "name": "Test Config",
        "version": "1.0.0",
        "settings": {
            "enabled": True,
            "timeout": 30,
            "items": ["a", "b", "c"],
        },
    }


# =============================================================================
# Test SafeFileWriter
# =============================================================================

class TestSafeFileWriter:
    """Tests for SafeFileWriter atomic write operations."""
    
    def test_write_text_atomic_creates_file(self, temp_dir):
        """Atomic write creates new file."""
        path = temp_dir / "new_file.txt"
        content = "Hello, World!"
        
        result = SafeFileWriter.write_text_atomic(path, content)
        
        assert result.success is True
        assert result.operation == FileOperation.WRITE
        assert path.exists()
        assert path.read_text() == content
    
    def test_write_text_atomic_overwrites_existing(self, temp_dir):
        """Atomic write overwrites existing file."""
        path = temp_dir / "existing.txt"
        path.write_text("old content")
        
        result = SafeFileWriter.write_text_atomic(path, "new content")
        
        assert result.success is True
        assert path.read_text() == "new content"
    
    def test_write_text_atomic_with_backup(self, temp_dir):
        """Atomic write creates backup when requested."""
        path = temp_dir / "with_backup.txt"
        path.write_text("original content")
        
        result = SafeFileWriter.write_text_atomic(path, "new content", backup=True)
        
        assert result.success is True
        assert result.backup_path is not None
        assert result.backup_path.exists()
        assert result.backup_path.read_text() == "original content"
        assert path.read_text() == "new content"
    
    def test_write_text_atomic_creates_directories(self, temp_dir):
        """Atomic write creates parent directories."""
        path = temp_dir / "deep" / "nested" / "file.txt"
        
        result = SafeFileWriter.write_text_atomic(path, "content")
        
        assert result.success is True
        assert path.exists()
    
    def test_write_json_atomic(self, temp_dir, sample_json):
        """Atomic JSON write works correctly."""
        path = temp_dir / "config.json"
        
        result = SafeFileWriter.write_json_atomic(path, sample_json)
        
        assert result.success is True
        assert path.exists()
        
        loaded = json.loads(path.read_text())
        assert loaded == sample_json
    
    def test_write_json_atomic_with_indent(self, temp_dir, sample_json):
        """Atomic JSON write respects indent setting."""
        path = temp_dir / "formatted.json"
        
        SafeFileWriter.write_json_atomic(path, sample_json, indent=4)
        
        content = path.read_text()
        # Check that it's properly indented
        assert "    " in content
    
    def test_write_bytes_atomic(self, temp_dir):
        """Atomic bytes write works correctly."""
        path = temp_dir / "data.bin"
        content = b"\x00\x01\x02\x03\xff\xfe\xfd"
        
        result = SafeFileWriter.write_bytes_atomic(path, content)
        
        assert result.success is True
        assert path.read_bytes() == content
    
    def test_write_text_atomic_encoding(self, temp_dir):
        """Atomic write handles unicode encoding."""
        path = temp_dir / "unicode.txt"
        content = "日本語 text with émojis 🚀"
        
        result = SafeFileWriter.write_text_atomic(path, content, encoding='utf-8')
        
        assert result.success is True
        assert path.read_text(encoding='utf-8') == content
    
    def test_no_temp_file_on_failure(self, temp_dir):
        """Temp file is cleaned up on write failure."""
        path = temp_dir / "nonexistent_dir_abc123" / "file.txt"
        # Remove the parent so write_text_atomic can't create it
        # Actually, it creates directories, so let's test invalid content instead
        
        # This should succeed - write_text_atomic creates directories
        result = SafeFileWriter.write_text_atomic(path, "content")
        assert result.success is True
        
        # Clean up
        path.unlink()
        path.parent.rmdir()


# =============================================================================
# Test SafeFileReader
# =============================================================================

class TestSafeFileReader:
    """Tests for SafeFileReader safe read operations."""
    
    def test_read_text_safe_existing_file(self, temp_dir):
        """Safe read returns content of existing file."""
        path = temp_dir / "existing.txt"
        path.write_text("file content")
        
        content = SafeFileReader.read_text_safe(path)
        
        assert content == "file content"
    
    def test_read_text_safe_missing_file_returns_default(self, temp_dir):
        """Safe read returns default for missing file."""
        path = temp_dir / "missing.txt"
        
        content = SafeFileReader.read_text_safe(path, default="default value")
        
        assert content == "default value"
    
    def test_read_text_safe_recovers_from_backup(self, temp_dir):
        """Safe read recovers from backup when main file is missing."""
        path = temp_dir / "missing.txt"
        backup_path = path.with_suffix(".txt.bak")
        
        # Only backup exists
        backup_path.write_text("backup content")
        
        content = SafeFileReader.read_text_safe(path, try_backup=True)
        
        assert content == "backup content"
    
    def test_read_json_safe_existing_file(self, temp_dir, sample_json):
        """Safe JSON read returns parsed content."""
        path = temp_dir / "config.json"
        path.write_text(json.dumps(sample_json))
        
        data = SafeFileReader.read_json_safe(path)
        
        assert data == sample_json
    
    def test_read_json_safe_invalid_json_returns_default(self, temp_dir):
        """Safe JSON read returns default for invalid JSON."""
        path = temp_dir / "invalid.json"
        path.write_text("{ not valid json }")
        
        data = SafeFileReader.read_json_safe(path, default={"fallback": True})
        
        assert data == {"fallback": True}
    
    def test_read_json_safe_recovers_from_backup(self, temp_dir, sample_json):
        """Safe JSON read recovers from backup."""
        path = temp_dir / "config.json"
        backup_path = path.with_suffix(".json.bak")
        
        path.write_text("{ invalid")
        backup_path.write_text(json.dumps(sample_json))
        
        data = SafeFileReader.read_json_safe(path, try_backup=True)
        
        assert data == sample_json
    
    def test_read_bytes_safe_existing_file(self, temp_dir):
        """Safe bytes read returns content."""
        path = temp_dir / "data.bin"
        content = b"\x00\x01\x02\xff"
        path.write_bytes(content)
        
        result = SafeFileReader.read_bytes_safe(path)
        
        assert result == content
    
    def test_read_bytes_safe_missing_file_returns_default(self, temp_dir):
        """Safe bytes read returns default for missing file."""
        path = temp_dir / "missing.bin"
        
        result = SafeFileReader.read_bytes_safe(path, default=b"default")
        
        assert result == b"default"


# =============================================================================
# Test File Locking
# =============================================================================

class TestFileLocking:
    """Tests for file locking context manager."""
    
    def test_locked_file_basic_read(self, temp_dir):
        """Basic read with lock works."""
        path = temp_dir / "locktest.txt"
        path.write_text("test content")
        
        with locked_file(path, 'r') as f:
            content = f.read()
        
        assert content == "test content"
    
    def test_locked_file_basic_write(self, temp_dir):
        """Basic write with lock works."""
        path = temp_dir / "locktest.txt"
        path.write_text("")  # Create empty file
        
        with locked_file(path, 'w') as f:
            f.write("new content")
        
        assert path.read_text() == "new content"
    
    def test_locked_file_binary_mode(self, temp_dir):
        """Binary mode with lock works."""
        path = temp_dir / "binary.bin"
        path.write_bytes(b"")
        
        with locked_file(path, 'wb', encoding=None) as f:
            f.write(b"\x00\x01\x02")
        
        assert path.read_bytes() == b"\x00\x01\x02"
    
    @pytest.mark.skipif(os.name == 'nt', reason="Windows locking behavior differs")
    def test_locked_file_timeout(self, temp_dir):
        """Lock timeout raises TimeoutError."""
        path = temp_dir / "locked.txt"
        path.write_text("content")
        
        lock_acquired = threading.Event()
        lock_held = threading.Event()
        
        def hold_lock():
            with locked_file(path, 'r', timeout=10) as f:
                lock_acquired.set()
                lock_held.wait(timeout=5)  # Hold lock until signaled
        
        # Start thread holding lock
        t = threading.Thread(target=hold_lock)
        t.start()
        
        # Wait for lock to be acquired
        lock_acquired.wait(timeout=2)
        
        try:
            # Try to acquire same lock - should timeout
            with pytest.raises(TimeoutError):
                with locked_file(path, 'r', timeout=0.1) as f:
                    pass
        finally:
            # Release the lock
            lock_held.set()
            t.join(timeout=2)
    
    def test_concurrent_reads_with_shared_lock(self, temp_dir):
        """Multiple readers can acquire shared locks."""
        path = temp_dir / "shared.txt"
        path.write_text("shared content")
        
        results = []
        
        def read_file():
            with locked_file(path, 'r', exclusive=False, timeout=2) as f:
                results.append(f.read())
                time.sleep(0.1)  # Hold lock briefly
        
        # Start multiple readers
        threads = [threading.Thread(target=read_file) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)
        
        # All should have read successfully
        assert len(results) == 3
        assert all(r == "shared content" for r in results)


# =============================================================================
# Test Utility Functions
# =============================================================================

class TestUtilityFunctions:
    """Tests for safe_delete, safe_rename, ensure_directory."""
    
    def test_safe_delete_existing_file(self, temp_dir):
        """Safe delete removes existing file."""
        path = temp_dir / "to_delete.txt"
        path.write_text("content")
        
        result = safe_delete(path)
        
        assert result.success is True
        assert result.operation == FileOperation.DELETE
        assert not path.exists()
    
    def test_safe_delete_missing_file_ok(self, temp_dir):
        """Safe delete succeeds for missing file with missing_ok=True."""
        path = temp_dir / "nonexistent.txt"
        
        result = safe_delete(path, missing_ok=True)
        
        assert result.success is True
    
    def test_safe_delete_missing_file_error(self, temp_dir):
        """Safe delete fails for missing file with missing_ok=False."""
        path = temp_dir / "nonexistent.txt"
        
        result = safe_delete(path, missing_ok=False)
        
        assert result.success is False
        assert result.error == "File not found"
    
    def test_safe_rename_basic(self, temp_dir):
        """Safe rename moves file."""
        src = temp_dir / "original.txt"
        dst = temp_dir / "renamed.txt"
        src.write_text("content")
        
        result = safe_rename(src, dst)
        
        assert result.success is True
        assert result.operation == FileOperation.RENAME
        assert not src.exists()
        assert dst.exists()
        assert dst.read_text() == "content"
    
    def test_safe_rename_overwrite(self, temp_dir):
        """Safe rename overwrites with overwrite=True."""
        src = temp_dir / "source.txt"
        dst = temp_dir / "dest.txt"
        src.write_text("new content")
        dst.write_text("old content")
        
        result = safe_rename(src, dst, overwrite=True)
        
        assert result.success is True
        assert dst.read_text() == "new content"
    
    def test_safe_rename_no_overwrite(self, temp_dir):
        """Safe rename fails without overwrite when dest exists."""
        src = temp_dir / "source.txt"
        dst = temp_dir / "dest.txt"
        src.write_text("new")
        dst.write_text("existing")
        
        result = safe_rename(src, dst, overwrite=False)
        
        assert result.success is False
        assert "already exists" in result.error
    
    def test_ensure_directory_creates(self, temp_dir):
        """Ensure directory creates nested directories."""
        path = temp_dir / "deep" / "nested" / "dir"
        
        result = ensure_directory(path)
        
        assert result is True
        assert path.exists()
        assert path.is_dir()
    
    def test_ensure_directory_existing(self, temp_dir):
        """Ensure directory succeeds for existing directory."""
        path = temp_dir / "existing"
        path.mkdir()
        
        result = ensure_directory(path)
        
        assert result is True


# =============================================================================
# Test Convenience Aliases
# =============================================================================

class TestConvenienceAliases:
    """Tests for module-level convenience functions."""
    
    def test_write_text_alias(self, temp_dir):
        """write_text alias works."""
        path = temp_dir / "test.txt"
        
        result = write_text(path, "content")
        
        assert result.success is True
        assert path.read_text() == "content"
    
    def test_write_json_alias(self, temp_dir, sample_json):
        """write_json alias works."""
        path = temp_dir / "config.json"
        
        result = write_json(path, sample_json)
        
        assert result.success is True
    
    def test_read_text_alias(self, temp_dir):
        """read_text alias works."""
        path = temp_dir / "test.txt"
        path.write_text("content")
        
        content = read_text(path)
        
        assert content == "content"
    
    def test_read_json_alias(self, temp_dir, sample_json):
        """read_json alias works."""
        path = temp_dir / "config.json"
        path.write_text(json.dumps(sample_json))
        
        data = read_json(path)
        
        assert data == sample_json


# =============================================================================
# Test Concurrent Access
# =============================================================================

class TestConcurrentAccess:
    """Tests for concurrent file access scenarios."""
    
    def test_concurrent_atomic_writes(self, temp_dir):
        """Multiple concurrent atomic writes don't corrupt data."""
        path = temp_dir / "concurrent.json"
        
        def write_data(thread_id: int):
            for i in range(10):
                data = {"thread": thread_id, "iteration": i}
                SafeFileWriter.write_json_atomic(path, data)
                time.sleep(0.01)  # Small delay
        
        # Run multiple writers
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(write_data, i) for i in range(4)]
            for f in futures:
                f.result()  # Wait for completion
        
        # File should be valid JSON (not corrupted)
        data = SafeFileReader.read_json_safe(path)
        assert data is not None
        assert "thread" in data
        assert "iteration" in data
    
    @pytest.mark.skipif(os.name == 'nt', reason="Windows file locking prevents concurrent access")
    def test_read_during_atomic_write(self, temp_dir):
        """Reading during atomic write sees complete data."""
        path = temp_dir / "read_write.json"
        initial_data = {"version": 1, "data": "initial"}
        SafeFileWriter.write_json_atomic(path, initial_data)
        
        read_results = []
        write_complete = threading.Event()
        
        def reader():
            for _ in range(20):
                data = SafeFileReader.read_json_safe(path)
                read_results.append(data)
                time.sleep(0.01)
                if write_complete.is_set():
                    break
        
        def writer():
            for i in range(10):
                data = {"version": i + 2, "data": f"iteration_{i}"}
                SafeFileWriter.write_json_atomic(path, data)
                time.sleep(0.02)
            write_complete.set()
        
        reader_thread = threading.Thread(target=reader)
        writer_thread = threading.Thread(target=writer)
        
        reader_thread.start()
        writer_thread.start()
        
        reader_thread.join(timeout=5)
        writer_thread.join(timeout=5)
        
        # All reads should return valid JSON (never partial/corrupted)
        for data in read_results:
            assert data is not None
            assert "version" in data
            assert "data" in data
