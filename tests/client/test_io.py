"""
Tests for pywats_client.io module

Tests file I/O utilities for attachments.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

from pywats_client.io import (
    AttachmentIO,
    FileInfo,
    load_attachment,
    save_attachment,
    DEFAULT_MAX_ATTACHMENT_SIZE,
)


class TestFileInfo:
    """Tests for FileInfo dataclass."""
    
    def test_create_file_info(self):
        """Test creating FileInfo with all attributes."""
        info = FileInfo(
            content=b"test content",
            name="test.txt",
            mime_type="text/plain",
            size=12
        )
        assert info.content == b"test content"
        assert info.name == "test.txt"
        assert info.mime_type == "text/plain"
        assert info.size == 12
    
    def test_file_info_binary_content(self):
        """Test FileInfo with binary content."""
        binary_data = bytes([0x00, 0x01, 0xFF, 0xFE])
        info = FileInfo(
            content=binary_data,
            name="binary.bin",
            mime_type="application/octet-stream",
            size=len(binary_data)
        )
        assert info.content == binary_data
        assert info.size == 4


class TestAttachmentIOFromFile:
    """Tests for AttachmentIO.from_file() method."""
    
    def test_from_file_basic(self, tmp_path):
        """Test loading attachment from file."""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"Hello, World!")
        
        attachment = AttachmentIO.from_file(test_file)
        
        assert attachment.name == "test.txt"
        assert attachment.get_bytes() == b"Hello, World!"
    
    def test_from_file_with_custom_name(self, tmp_path):
        """Test loading attachment with custom name."""
        test_file = tmp_path / "original.txt"
        test_file.write_bytes(b"content")
        
        attachment = AttachmentIO.from_file(test_file, name="custom.txt")
        
        assert attachment.name == "custom.txt"
    
    def test_from_file_with_custom_content_type(self, tmp_path):
        """Test loading attachment with custom content type."""
        test_file = tmp_path / "data.dat"
        test_file.write_bytes(b"binary data")
        
        attachment = AttachmentIO.from_file(
            test_file,
            content_type="application/custom"
        )
        
        assert attachment.content_type == "application/custom"
    
    def test_from_file_auto_detect_mime_type_text(self, tmp_path):
        """Test auto-detection of MIME type for text file."""
        test_file = tmp_path / "readme.txt"
        test_file.write_bytes(b"readme content")
        
        attachment = AttachmentIO.from_file(test_file)
        
        assert attachment.content_type == "text/plain"
    
    def test_from_file_auto_detect_mime_type_json(self, tmp_path):
        """Test auto-detection of MIME type for JSON file."""
        test_file = tmp_path / "config.json"
        test_file.write_bytes(b'{"key": "value"}')
        
        attachment = AttachmentIO.from_file(test_file)
        
        assert attachment.content_type == "application/json"
    
    def test_from_file_auto_detect_mime_type_unknown(self, tmp_path):
        """Test fallback MIME type for unknown extension."""
        test_file = tmp_path / "data.xyz123"
        test_file.write_bytes(b"some data")
        
        attachment = AttachmentIO.from_file(test_file)
        
        assert attachment.content_type == "application/octet-stream"
    
    def test_from_file_not_found(self):
        """Test FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            AttachmentIO.from_file("/nonexistent/path/file.txt")
    
    def test_from_file_exceeds_max_size(self, tmp_path):
        """Test ValueError when file exceeds max size."""
        test_file = tmp_path / "large.bin"
        test_file.write_bytes(b"x" * 1000)  # 1000 bytes
        
        with pytest.raises(ValueError, match="exceeds maximum"):
            AttachmentIO.from_file(test_file, max_size=500)
    
    def test_from_file_respects_default_max_size(self):
        """Test that DEFAULT_MAX_ATTACHMENT_SIZE is defined."""
        assert DEFAULT_MAX_ATTACHMENT_SIZE == 10 * 1024 * 1024  # 10 MB
    
    def test_from_file_with_failure_idx(self, tmp_path):
        """Test loading attachment with failure index."""
        test_file = tmp_path / "uur_attachment.png"
        test_file.write_bytes(b"image data")
        
        attachment = AttachmentIO.from_file(test_file, failure_idx=0)
        
        # The attachment should have the failure index set
        assert attachment.failure_idx == 0
    
    def test_from_file_string_path(self, tmp_path):
        """Test from_file accepts string path."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"content")
        
        attachment = AttachmentIO.from_file(str(test_file))
        
        assert attachment.name == "test.txt"
    
    def test_from_file_delete_after(self, tmp_path):
        """Test delete_after option removes source file."""
        test_file = tmp_path / "temp.txt"
        test_file.write_bytes(b"temporary content")
        
        assert test_file.exists()
        
        attachment = AttachmentIO.from_file(test_file, delete_after=True)
        
        # File should be deleted
        assert not test_file.exists()
        # But attachment should have content
        assert attachment.get_bytes() == b"temporary content"
    
    def test_from_file_delete_after_handles_error(self, tmp_path):
        """Test delete_after handles deletion errors gracefully."""
        test_file = tmp_path / "readonly.txt"
        test_file.write_bytes(b"content")
        
        # Make file read-only (may not work on all systems)
        with patch('pathlib.Path.unlink') as mock_unlink:
            mock_unlink.side_effect = OSError("Permission denied")
            
            # Should not raise, just log warning
            attachment = AttachmentIO.from_file(test_file, delete_after=True)
            
            assert attachment.get_bytes() == b"content"


class TestAttachmentIOReadFile:
    """Tests for AttachmentIO.read_file() method."""
    
    def test_read_file_basic(self, tmp_path):
        """Test reading file info."""
        test_file = tmp_path / "data.txt"
        test_file.write_bytes(b"Hello!")
        
        info = AttachmentIO.read_file(test_file)
        
        assert info.content == b"Hello!"
        assert info.name == "data.txt"
        assert info.mime_type == "text/plain"
        assert info.size == 6
    
    def test_read_file_binary(self, tmp_path):
        """Test reading binary file."""
        test_file = tmp_path / "image.png"
        binary_data = bytes([0x89, 0x50, 0x4E, 0x47])  # PNG header
        test_file.write_bytes(binary_data)
        
        info = AttachmentIO.read_file(test_file)
        
        assert info.content == binary_data
        assert info.mime_type == "image/png"
    
    def test_read_file_not_found(self):
        """Test FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError, match="File not found"):
            AttachmentIO.read_file("/nonexistent/file.txt")
    
    def test_read_file_exceeds_max_size(self, tmp_path):
        """Test ValueError when file exceeds max size."""
        test_file = tmp_path / "big.bin"
        test_file.write_bytes(b"x" * 2000)
        
        with pytest.raises(ValueError, match="exceeds maximum"):
            AttachmentIO.read_file(test_file, max_size=1000)
    
    def test_read_file_unknown_extension(self, tmp_path):
        """Test unknown extension falls back to octet-stream."""
        test_file = tmp_path / "data.unknownext"
        test_file.write_bytes(b"data")
        
        info = AttachmentIO.read_file(test_file)
        
        assert info.mime_type == "application/octet-stream"


class TestAttachmentIOSave:
    """Tests for AttachmentIO.save() method."""
    
    @pytest.fixture
    def mock_attachment(self):
        """Create a mock attachment for testing."""
        attachment = Mock()
        attachment.name = "test.txt"
        attachment.get_bytes.return_value = b"attachment content"
        return attachment
    
    def test_save_basic(self, tmp_path, mock_attachment):
        """Test saving attachment to file."""
        output_path = tmp_path / "output.txt"
        
        result = AttachmentIO.save(mock_attachment, output_path)
        
        assert result == output_path
        assert output_path.exists()
        assert output_path.read_bytes() == b"attachment content"
    
    def test_save_creates_parent_directory(self, tmp_path, mock_attachment):
        """Test save creates parent directories."""
        output_path = tmp_path / "subdir" / "deep" / "output.txt"
        
        result = AttachmentIO.save(mock_attachment, output_path)
        
        assert result == output_path
        assert output_path.exists()
    
    def test_save_file_exists_no_overwrite(self, tmp_path, mock_attachment):
        """Test FileExistsError when file exists and overwrite=False."""
        output_path = tmp_path / "existing.txt"
        output_path.write_bytes(b"existing content")
        
        with pytest.raises(FileExistsError, match="already exists"):
            AttachmentIO.save(mock_attachment, output_path)
    
    def test_save_file_exists_with_overwrite(self, tmp_path, mock_attachment):
        """Test overwriting existing file."""
        output_path = tmp_path / "existing.txt"
        output_path.write_bytes(b"old content")
        
        AttachmentIO.save(mock_attachment, output_path, overwrite=True)
        
        assert output_path.read_bytes() == b"attachment content"
    
    def test_save_no_data_raises_error(self, tmp_path):
        """Test ValueError when attachment has no data."""
        attachment = Mock()
        attachment.get_bytes.return_value = None
        
        with pytest.raises(ValueError, match="no data"):
            AttachmentIO.save(attachment, tmp_path / "output.txt")
    
    def test_save_non_atomic(self, tmp_path, mock_attachment):
        """Test non-atomic save (direct write)."""
        output_path = tmp_path / "direct.txt"
        
        result = AttachmentIO.save(mock_attachment, output_path, atomic=False)
        
        assert result == output_path
        assert output_path.read_bytes() == b"attachment content"
    
    def test_save_string_path(self, tmp_path, mock_attachment):
        """Test save accepts string path."""
        output_path = tmp_path / "string_path.txt"
        
        result = AttachmentIO.save(mock_attachment, str(output_path))
        
        assert output_path.exists()
    
    def test_save_atomic_failure(self, tmp_path, mock_attachment):
        """Test IOError on atomic write failure."""
        output_path = tmp_path / "atomic.txt"
        
        with patch('pywats_client.io.SafeFileWriter') as mock_writer:
            mock_result = Mock()
            mock_result.success = False
            mock_result.error = "Write failed"
            mock_writer.write_bytes_atomic.return_value = mock_result
            
            with pytest.raises(IOError, match="Failed to save attachment"):
                AttachmentIO.save(mock_attachment, output_path)


class TestAttachmentIOSaveMultiple:
    """Tests for AttachmentIO.save_multiple() method."""
    
    def test_save_multiple_basic(self, tmp_path):
        """Test saving multiple attachments."""
        attachments = []
        for i in range(3):
            att = Mock()
            att.name = f"file{i}.txt"
            att.get_bytes.return_value = f"content{i}".encode()
            attachments.append(att)
        
        paths = AttachmentIO.save_multiple(attachments, tmp_path)
        
        assert len(paths) == 3
        for i, path in enumerate(paths):
            assert path.name == f"file{i}.txt"
            assert path.read_bytes() == f"content{i}".encode()
    
    def test_save_multiple_creates_directory(self, tmp_path):
        """Test save_multiple creates target directory."""
        target = tmp_path / "new_dir"
        
        att = Mock()
        att.name = "file.txt"
        att.get_bytes.return_value = b"content"
        
        paths = AttachmentIO.save_multiple([att], target)
        
        assert target.exists()
        assert len(paths) == 1
    
    def test_save_multiple_empty_list(self, tmp_path):
        """Test save_multiple with empty list."""
        paths = AttachmentIO.save_multiple([], tmp_path)
        
        assert paths == []
        assert tmp_path.exists()  # Directory should still be created
    
    def test_save_multiple_with_overwrite(self, tmp_path):
        """Test save_multiple with overwrite option."""
        # Create existing file
        existing = tmp_path / "file.txt"
        existing.write_bytes(b"old content")
        
        att = Mock()
        att.name = "file.txt"
        att.get_bytes.return_value = b"new content"
        
        paths = AttachmentIO.save_multiple([att], tmp_path, overwrite=True)
        
        assert len(paths) == 1
        assert paths[0].read_bytes() == b"new content"


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_load_attachment(self, tmp_path):
        """Test load_attachment convenience function."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"test content")
        
        attachment = load_attachment(test_file)
        
        assert attachment.name == "test.txt"
        assert attachment.get_bytes() == b"test content"
    
    def test_load_attachment_with_kwargs(self, tmp_path):
        """Test load_attachment passes kwargs."""
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"content")
        
        attachment = load_attachment(
            test_file,
            name="custom.txt",
            content_type="text/custom"
        )
        
        assert attachment.name == "custom.txt"
        assert attachment.content_type == "text/custom"
    
    def test_save_attachment(self, tmp_path):
        """Test save_attachment convenience function."""
        attachment = Mock()
        attachment.name = "save_test.txt"
        attachment.get_bytes.return_value = b"saved content"
        
        output_path = tmp_path / "output.txt"
        result = save_attachment(attachment, output_path)
        
        assert result == output_path
        assert output_path.read_bytes() == b"saved content"
    
    def test_save_attachment_with_kwargs(self, tmp_path):
        """Test save_attachment passes kwargs."""
        attachment = Mock()
        attachment.name = "test.txt"
        attachment.get_bytes.return_value = b"content"
        
        # Create existing file
        output_path = tmp_path / "existing.txt"
        output_path.write_bytes(b"old")
        
        # Should work with overwrite=True
        result = save_attachment(attachment, output_path, overwrite=True)
        
        assert output_path.read_bytes() == b"content"


class TestModuleExports:
    """Tests for module exports."""
    
    def test_all_exports_defined(self):
        """Test that __all__ exports are importable."""
        from pywats_client import io
        
        expected = [
            "AttachmentIO",
            "FileInfo",
            "load_attachment",
            "save_attachment",
            "DEFAULT_MAX_ATTACHMENT_SIZE",
        ]
        
        for name in expected:
            assert hasattr(io, name), f"{name} not found in module"
    
    def test_default_max_attachment_size_value(self):
        """Test DEFAULT_MAX_ATTACHMENT_SIZE has correct value."""
        assert DEFAULT_MAX_ATTACHMENT_SIZE == 10 * 1024 * 1024
