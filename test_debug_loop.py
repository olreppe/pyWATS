"""Test script to debug loop null restoration"""
import asyncio
import json
from pathlib import Path
from pywats.domains.report.async_repository import AsyncReportRepository
from pywats.core.async_client import AsyncHttpClient
from pywats.domains.report.report_models import UUTReport

async def test_file():
    # Load the test file
    file_path = r"C:\ProgramData\Virinco\pyWATS\instances\default\WSJF\Error\1004est-295_FATPartNo_Rev1_2026-02-12_12-48-04.json"
    
    print(f"Loading file: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"File loaded. Report ID: {data.get('id', 'N/A')}")
    
    # Parse as Pydantic model (like the service does!)
    print("\nParsing as Pydantic model...")
    try:
        report = UUTReport.model_validate(data)
        print(f"[OK] Pydantic validation passed")
    except Exception as e:
        print(f"[FAIL] Pydantic validation failed: {e}")
        return
    
    # Create API client
    http_client = AsyncHttpClient(
        base_url="https://python.wats.com",
        token="cHlXQVRTX0FQSV9BVVRPVEVTVDo2cGhUUjg0ZTVIMHA1R3JUWGtQZlY0UTNvbmk2MiM=",
    )
    repo = AsyncReportRepository(http_client)
    
    print("\nPosting WSJF report (Pydantic model)...")
    try:
        result = await repo.post_wsjf(report)
        print(f"[SUCCESS] Report ID: {result}")
    except Exception as e:
        print(f"[FAILED] {str(e)}")
    finally:
        await http_client.close()

if __name__ == "__main__":
    asyncio.run(test_file())
