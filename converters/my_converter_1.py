"""
Custom Converter Template

Implement your converter logic here.
"""

from pywats_client.converters import ConverterBase


class AOIConverter(ConverterBase):
    """Example converter implementation"""
    
    @property
    def name(self) -> str:
        return "My Converter"
    
    @property
    def description(self) -> str:
        return "Converts custom log files to WATS reports"
    
    @property
    def extensions(self) -> list[str]:
        return [".log", ".txt"]
    
    async def convert(self, source_path: str) -> dict:
        """
        Convert source file to WATS report format.
        
        Args:
            source_path: Path to the source file
            
        Returns:
            Dictionary in WATS report format
        """
        # Read source file
        with open(source_path, 'r') as f:
            content = f.read()
        
        # Parse and convert to WATS format
        report = {
            "type": "Test",
            "pn": "PART-001",
            "sn": "SN-001",
            "result": "P",
            # Add your conversion logic here
        }
        
        return report
