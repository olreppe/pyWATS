"""
Example: Working with file attachments in pyWATS

This example demonstrates:
- Loading attachments from files
- Saving attachments to disk
- Bulk attachment operations
- File metadata handling
- Error handling for file operations

Prerequisites:
- pyWATS client installed
- Sample files to upload (or use the included test file creator)
"""

from pywats_client.io import AttachmentIO, load_attachment, save_attachment
from pywats_client.exceptions import FileFormatError, FileAccessError
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_file():
    """Create a test file for demonstration."""
    test_file = Path("test_document.txt")
    test_file.write_text("This is a test document for pyWATS attachment example.\n" * 10)
    logger.info(f"Created test file: {test_file}")
    return test_file


def basic_attachment_loading():
    """Load an attachment from a file."""
    logger.info("\n=== Basic Attachment Loading ===")
    
    # Create a test file
    test_file = create_test_file()
    
    try:
        # Load attachment from file (auto-detects MIME type)
        attachment = AttachmentIO.from_file(test_file)
        
        logger.info(f"Loaded attachment:")
        logger.info(f"  Name: {attachment.name}")
        logger.info(f"  MIME type: {attachment.mime_type}")
        logger.info(f"  Size: {len(attachment.content)} bytes")
        
        # Alternative: Use convenience function
        attachment2 = load_attachment(test_file)
        logger.info(f"Also loaded via convenience function: {attachment2.name}")
        
    except FileAccessError as e:
        logger.error(f"File access error: {e}")
    except FileFormatError as e:
        logger.error(f"File format error: {e}")
    finally:
        # Cleanup
        test_file.unlink()
        logger.info(f"Cleaned up test file")


def custom_attachment_name():
    """Load attachment with custom name."""
    logger.info("\n=== Custom Attachment Name ===")
    
    test_file = create_test_file()
    
    try:
        # Load with custom name
        attachment = AttachmentIO.from_file(
            test_file,
            name="MyCustomDocument.txt"
        )
        
        logger.info(f"Attachment name: {attachment.name}")
        # Note: Name is custom, but MIME type is still auto-detected
        logger.info(f"MIME type: {attachment.mime_type}")
        
    finally:
        test_file.unlink()


def file_size_limit():
    """Handle file size limits."""
    logger.info("\n=== File Size Limits ===")
    
    # Create a larger test file
    large_file = Path("large_test.txt")
    large_file.write_text("X" * (11 * 1024 * 1024))  # 11 MB
    
    try:
        # Default limit is 10 MB - this will fail
        try:
            attachment = AttachmentIO.from_file(large_file)
            logger.error("Should have raised an error!")
        except FileFormatError as e:
            logger.info(f"Expected error for large file: {e}")
        
        # Increase the limit to 15 MB
        attachment = AttachmentIO.from_file(large_file, max_size_mb=15)
        logger.info(f"Successfully loaded with increased limit: {len(attachment.content)} bytes")
        
    finally:
        large_file.unlink()
        logger.info("Cleaned up large test file")


def save_attachment_to_disk():
    """Save attachment to disk."""
    logger.info("\n=== Saving Attachments ===")
    
    # Create a test file
    test_file = create_test_file()
    
    try:
        # Load attachment
        attachment = load_attachment(test_file)
        
        # Save to a different location
        output_path = Path("output_document.txt")
        attachment.save(output_path)
        
        logger.info(f"Saved attachment to: {output_path}")
        logger.info(f"File exists: {output_path.exists()}")
        logger.info(f"File size: {output_path.stat().st_size} bytes")
        
        # Cleanup
        output_path.unlink()
        logger.info("Cleaned up output file")
        
    finally:
        test_file.unlink()


def bulk_attachment_operations():
    """Save multiple attachments at once."""
    logger.info("\n=== Bulk Attachment Operations ===")
    
    # Create test files
    test_files = []
    attachments = []
    
    for i in range(3):
        file_path = Path(f"test_file_{i}.txt")
        file_path.write_text(f"Content of test file {i}\n")
        test_files.append(file_path)
        
        attachment = load_attachment(file_path)
        attachments.append(attachment)
    
    try:
        # Save all attachments to a directory
        output_dir = Path("output_attachments")
        output_dir.mkdir(exist_ok=True)
        
        saved_paths = AttachmentIO.save_multiple(attachments, output_dir)
        
        logger.info(f"Saved {len(saved_paths)} attachments:")
        for path in saved_paths:
            logger.info(f"  - {path}")
        
        # Cleanup output files
        for path in saved_paths:
            path.unlink()
        output_dir.rmdir()
        logger.info("Cleaned up output directory")
        
    finally:
        # Cleanup test files
        for file_path in test_files:
            file_path.unlink()
        logger.info("Cleaned up test files")


def read_file_info():
    """Read file information without creating an attachment."""
    logger.info("\n=== Reading File Info ===")
    
    test_file = create_test_file()
    
    try:
        # Read file info without creating an attachment
        file_info = AttachmentIO.read_file(test_file)
        
        logger.info(f"File information:")
        logger.info(f"  Content length: {len(file_info['content'])} bytes")
        logger.info(f"  Filename: {file_info['filename']}")
        logger.info(f"  MIME type: {file_info['mime_type']}")
        logger.info(f"  Size: {file_info['size']}")
        
    finally:
        test_file.unlink()


def delete_after_read():
    """Delete source file after reading."""
    logger.info("\n=== Delete After Read ===")
    
    test_file = create_test_file()
    
    # Load attachment and delete source file
    attachment = AttachmentIO.from_file(test_file, delete_after_read=True)
    
    logger.info(f"Loaded attachment: {attachment.name}")
    logger.info(f"Source file exists: {test_file.exists()}")  # Should be False


def error_handling_example():
    """Demonstrate error handling for file operations."""
    logger.info("\n=== Error Handling ===")
    
    # Non-existent file
    try:
        attachment = load_attachment("nonexistent.txt")
    except FileAccessError as e:
        logger.info(f"Handled missing file: {e}")
        # All exceptions include troubleshooting hints
        logger.info(f"Hint: {e.troubleshooting_hint}")
    
    # Invalid file type (if restricted)
    test_file = Path("test.xyz")
    test_file.write_text("test content")
    
    try:
        # This works by default (no type restrictions)
        attachment = load_attachment(test_file)
        logger.info(f"Loaded {attachment.name} with MIME type: {attachment.mime_type}")
    finally:
        test_file.unlink()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("pyWATS Attachment I/O Examples")
    print("="*60)
    
    # Run all examples
    basic_attachment_loading()
    custom_attachment_name()
    file_size_limit()
    save_attachment_to_disk()
    bulk_attachment_operations()
    read_file_info()
    delete_after_read()
    error_handling_example()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60 + "\n")
