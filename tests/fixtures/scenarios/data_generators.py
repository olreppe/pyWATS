"""
Test data generators for acceptance scenarios
"""
from typing import Dict, List
from datetime import datetime


class TestDataGenerator:
    """
    Generates realistic test data for acceptance scenarios
    """
    
    @staticmethod
    def generate_product_data(identifier: str) -> Dict:
        """
        Generate product test data.
        """
        return {
            "part_number": f"TEST-PROD-{identifier}",
            "part_description": f"Test Product {identifier}",
            "part_revision": "A",
            "product_group": "Test Products"
        }
    
    @staticmethod
    def generate_serial_numbers(prefix: str, count: int) -> List[str]:
        """
        Generate a list of serial numbers.
        """
        return [f"{prefix}-{i:04d}" for i in range(1, count + 1)]
    
    @staticmethod
    def generate_test_parameters(test_type: str = "voltage") -> Dict:
        """
        Generate test parameters based on test type.
        """
        parameters = {
            "voltage": {
                "name": "Voltage Test",
                "units": "V",
                "nominal": 5.0,
                "low_limit": 4.5,
                "high_limit": 5.5,
                "comp_operator": "GELE"
            },
            "current": {
                "name": "Current Test",
                "units": "A",
                "nominal": 1.0,
                "low_limit": 0.9,
                "high_limit": 1.1,
                "comp_operator": "GELE"
            },
            "resistance": {
                "name": "Resistance Test",
                "units": "Ω",
                "nominal": 100.0,
                "low_limit": 95.0,
                "high_limit": 105.0,
                "comp_operator": "GELE"
            },
            "temperature": {
                "name": "Temperature Test",
                "units": "°C",
                "nominal": 25.0,
                "low_limit": 20.0,
                "high_limit": 30.0,
                "comp_operator": "GELE"
            }
        }
        
        return parameters.get(test_type, parameters["voltage"])
    
    @staticmethod
    def generate_measurement_value(nominal: float, pass_test: bool = True) -> float:
        """
        Generate a measurement value that will pass or fail based on flag.
        """
        import random
        
        if pass_test:
            # Generate value within ±2% of nominal
            variance = nominal * 0.02
            return nominal + random.uniform(-variance, variance)
        else:
            # Generate value outside typical range
            return nominal * random.choice([0.5, 1.5])
    
    @staticmethod
    def generate_timestamp() -> str:
        """
        Generate ISO format timestamp for current time.
        """
        return datetime.now().isoformat()
