"""
MES Product Test Configuration

Configuration settings for MES product testing.
"""

# Server Configuration
TEST_BASE_URL = "https://ola.wats.com"
TEST_AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="

# Test Data Configuration
TEST_PART_NUMBERS = [
    "TEST_PART_001",
    "PCBA_PART_001",
    "FAT_PART_001"
]

TEST_FILTERS = [
    "TEST",
    "PCBA", 
    "FAT",
    "*"  # Get all products
]

# BOM Test Configuration
SAMPLE_BOM_DATA = {
    "format": "WSBF",  # WATS Standard BOM Format
    "version": "1.0"
}

# API Endpoints (based on C# MES Interface)
PRODUCT_ENDPOINTS = {
    "GET_PRODUCT_INFO": "api/internal/Product/GetProductInfo",
    "GET_PRODUCTS": "api/internal/Product/GetProducts", 
    "UPDATE_PRODUCT": "api/internal/Product/UpdateProduct",  # May not exist
    "BOM_UPLOAD": "api/Product/BOM",
    "BOM_GET": "api/Product/BOM",  # Might be different endpoint
    "IS_CONNECTED": "api/internal/Product/isConnected"
}

# Test Timeouts and Limits
DEFAULT_TIMEOUT = 30  # seconds
MAX_PRODUCTS_FETCH = 10
RETRY_COUNT = 3
RETRY_DELAY = 1  # seconds

# Expected Response Structure (for validation)
EXPECTED_PRODUCT_FIELDS = [
    "PartNumber",
    "Revision", 
    "ProductId",
    "ProductRevisionId",
    "Name",
    "ProductDescription"
]

EXPECTED_BOM_FIELDS = [
    "partNumber",
    "revision",
    "bomItems"
]