"""
Report Domain: Attachments

This example demonstrates adding attachments to both UUT and UUR reports.

Attachments can include:
- Images (photos of defects, repairs, product)
- Documents (PDFs, test specifications)
- Binary data (oscilloscope captures, measurement files)
- Text logs (test logs, repair notes)

The attachment API is identical for UUT and UUR reports.
"""
import os
from pathlib import Path
from pywats import pyWATS
from pywats.core import Station

# =============================================================================
# Setup
# =============================================================================

station = Station(name="TEST-STATION-01", location="Lab A")

api = pyWATS(
    base_url=os.environ.get("WATS_BASE_URL", "https://demo.wats.com"),
    token=os.environ.get("WATS_TOKEN", ""),
    station=station
)


# =============================================================================
# Attaching Files
# =============================================================================

def attach_file_example():
    """
    Attach a file from disk to a report.
    
    The MIME type is automatically detected from the file extension.
    """
    # Create a sample report
    report = api.report.create_uut_report(
        part_number="WIDGET-001",
        operation_code=100,
        serial_number="SN-2024-001"
    )
    
    # Attach a file - content type auto-detected
    # report.attach_file("test_photo.jpg")
    
    # Attach with explicit content type
    # report.attach_file("data.bin", content_type="application/octet-stream")
    
    # Attach and delete original after submission
    # report.attach_file("temp_log.txt", delete_after=True)
    
    # Attach with custom name (different from filename)
    # report.attach_file("IMG_20240126_103000.jpg", name="Repair Photo")
    
    return report


# =============================================================================
# Attaching Binary Data
# =============================================================================

def attach_bytes_example():
    """
    Attach binary content directly without writing to disk.
    
    Useful for dynamically generated content or data from instruments.
    """
    report = api.report.create_uut_report(
        part_number="WIDGET-001",
        operation_code=100,
        serial_number="SN-2024-002"
    )
    
    # Attach raw binary data
    measurement_data = bytes([0x00, 0x01, 0x02, 0x03, 0x04])
    report.attach_bytes(
        name="Raw Measurement",
        content=measurement_data,
        content_type="application/octet-stream"
    )
    
    # Attach a text log as bytes
    log_text = """
    Test Log - 2026-01-26
    =====================
    Step 1: Power on - OK
    Step 2: Self test - OK
    Step 3: Voltage check - FAIL
    """
    report.attach_bytes(
        name="Test Log",
        content=log_text.encode("utf-8"),
        content_type="text/plain"
    )
    
    # Attach JSON data
    import json
    config = {"setting1": True, "setting2": 42, "setting3": "value"}
    report.attach_bytes(
        name="Test Configuration",
        content=json.dumps(config, indent=2).encode("utf-8"),
        content_type="application/json"
    )
    
    return report


# =============================================================================
# Attaching to UUR Reports
# =============================================================================

def uur_attachments_example(failed_uut):
    """
    Attach files to a UUR (repair) report.
    
    The attachment API is identical for UUT and UUR reports.
    """
    uur = api.report.create_uur_report(
        failed_uut,
        operator="RepairTech"
    )
    
    # Add failure info first
    uur.add_failure_to_main_unit(
        category="Component",
        code="Defect Component",
        comment="Capacitor C12 failed"
    )
    
    # Attach repair documentation
    # Before photo
    # uur.attach_file("before_repair.jpg", name="Before Repair")
    
    # After photo
    # uur.attach_file("after_repair.jpg", name="After Repair")
    
    # Repair log
    repair_notes = """
    Repair Report
    =============
    Date: 2026-01-26
    Technician: John Smith
    
    Diagnosis:
    - Unit failed voltage test
    - Traced to capacitor C12
    - Visual inspection confirmed bulging cap
    
    Repair:
    - Removed capacitor C12
    - Installed replacement (C12-NEW)
    - Verified repair with voltage test
    
    Result: PASS
    """
    uur.attach_bytes(
        name="Repair Notes",
        content=repair_notes.encode("utf-8"),
        content_type="text/plain"
    )
    
    return uur


# =============================================================================
# Supported Content Types
# =============================================================================

# Common MIME types supported (auto-detected from extension):
SUPPORTED_TYPES = {
    # Images
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    
    # Documents
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls": "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    
    # Text
    ".txt": "text/plain",
    ".log": "text/plain",
    ".csv": "text/csv",
    ".xml": "application/xml",
    ".json": "application/json",
    
    # Binary
    ".bin": "application/octet-stream",
    ".dat": "application/octet-stream",
    ".zip": "application/zip",
}


# =============================================================================
# Best Practices
# =============================================================================

"""
Attachment Best Practices:
========================

1. Use descriptive names
   - Bad: "IMG_20240126.jpg"
   - Good: "Failed Component Photo"

2. Choose appropriate content type
   - Let auto-detection handle common types
   - Specify explicitly for custom formats

3. Size considerations
   - Keep attachments reasonable size (<10MB typical)
   - Compress large files if possible

4. Use delete_after for temp files
   - report.attach_file("temp.log", delete_after=True)
   - File removed after successful submission

5. Organize multiple attachments
   - Use clear naming conventions
   - Group related attachments with prefixes

6. Binary vs File
   - Use attach_bytes() for generated content
   - Use attach_file() for existing files
"""
