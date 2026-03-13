"""Quick test to see what validation error files are getting"""
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pywats.domains.report import AsyncReportRepository
from src.pywats.config import Config
import asyncio

async def test_file(file_path: str):
    """Test a single file and print the error"""
    print(f"\n{'='*80}")
    print(f"Testing: {Path(file_path).name}")
    print('='*80)
    
    # Load config
    config = Config.from_file("C:/ProgramData/Virinco/pyWATS/instances/default/client_config.json")
    
    # Load file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"File type: {data.get('type')}")
    print(f"PN: {data.get('pn')}")
    print(f"SN: {data.get('sn')}")
    
    # Try to submit
    repo = AsyncReportRepository(config)
    try:
        result = await repo.post_wsjf(data)
        print(f"\n✓ SUCCESS: {result}")
    except Exception as e:
        print(f"\n✗ FAILED: {type(e).__name__}")
        print(f"Error: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    error_folder = Path("C:/ProgramData/Virinco/pyWATS/instances/default/WSJF/Error")
    
    # Test first 3 error files
    error_files = list(error_folder.glob("*.json"))[:3]
    
    for file in error_files:
        try:
            asyncio.run(test_file(str(file)))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Fatal error testing {file.name}: {e}")
