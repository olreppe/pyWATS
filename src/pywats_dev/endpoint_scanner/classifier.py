"""Endpoint classifier - assigns priority/criticality scores.

Priority System (Based on User Requirements):
1. HIGH: Core functions - operation types, repair categories/codes
2. HIGH: Creating and submitting reports
3. HIGH: Serial number handler
4. MEDIUM-HIGH: Asset module (HIGH: usage count/alarms, LOW: create/edit)
5. MEDIUM: Production module - units, box build, assembling
6. MEDIUM: Software distribution
7. LOW: Everything else (Analytics, SCIM, RootCause)
"""

from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass


class Priority(Enum):
    """Endpoint priority levels."""
    CRITICAL = "CRITICAL"  # Core functionality, system breaks without it
    HIGH = "HIGH"          # Important features, significant impact
    MEDIUM = "MEDIUM"      # Standard features, moderate impact
    LOW = "LOW"            # Nice-to-have, minimal impact


@dataclass
class EndpointInfo:
    """Complete endpoint information."""
    path: str
    domain: str
    method: str  # GET, POST, PUT, DELETE
    is_internal: bool
    priority: Priority
    usage_count: int
    used_by: list[str]
    description: str
    public_alternative: Optional[str] = None


class EndpointClassifier:
    """Classifies endpoints by priority based on business rules."""
    
    # Priority mapping based on user requirements
    PRIORITY_RULES: Dict[str, Dict[str, Priority]] = {
        # Priority 1: Core functions - operation types, repair categories
        "Process": {
            "GET_REPAIR_OPERATIONS": Priority.CRITICAL,
            "get_repair_operation": Priority.CRITICAL,
            "GET_PROCESSES": Priority.CRITICAL,
            "get_process": Priority.CRITICAL,
            "PROCESSES": Priority.CRITICAL,
        },
        
        # Priority 2: Creating/submitting reports
        "Report": {
            "WSJF": Priority.CRITICAL,      # POST report (JSON)
            "WSXF": Priority.CRITICAL,      # POST report (XML)
            "wsjf": Priority.HIGH,          # GET report by ID
            "wsxf": Priority.HIGH,          # GET report by ID
            "QUERY_HEADER": Priority.HIGH,  # Query reports
            "UUT": Priority.HIGH,
            "UUR": Priority.HIGH,
            "ATTACHMENT": Priority.HIGH,
        },
        
        # Priority 3: Serial number handler
        "Production": {
            "SERIAL_NUMBERS": Priority.CRITICAL,
            "SERIAL_NUMBERS_TAKE": Priority.CRITICAL,
            "SERIAL_NUMBERS_BY_RANGE": Priority.CRITICAL,
            "SERIAL_NUMBERS_BY_REFERENCE": Priority.CRITICAL,
            "SERIAL_NUMBER_TYPES": Priority.HIGH,
            # Production units (Priority 5 - MEDIUM)
            "UNIT": Priority.MEDIUM,
            "UNITS": Priority.MEDIUM,
            "ADD_CHILD_UNIT": Priority.MEDIUM,
            "REMOVE_CHILD_UNIT": Priority.MEDIUM,
            "CHECK_CHILD_UNITS": Priority.MEDIUM,
            "CREATE_UNIT": Priority.MEDIUM,
            "SET_UNIT_PHASE": Priority.MEDIUM,
            "SET_UNIT_PROCESS": Priority.MEDIUM,
            "BATCH": Priority.MEDIUM,
            "BATCHES": Priority.MEDIUM,
        },
        
        # Priority 4: Asset module (mixed)
        "Asset": {
            "SET_RUNNING_COUNT": Priority.HIGH,     # Update usage count
            "SET_TOTAL_COUNT": Priority.HIGH,       # Update usage count
            "RESET_RUNNING_COUNT": Priority.HIGH,   # Update usage count
            "MESSAGE": Priority.HIGH,               # Get alarms
            "LOG": Priority.HIGH,                   # Get alarms
            "asset": Priority.LOW,                  # Create/edit (GET/PUT/DELETE)
            "ASSETS": Priority.LOW,                 # Create/edit
            "CALIBRATION": Priority.MEDIUM,
            "MAINTENANCE": Priority.MEDIUM,
            "STATUS": Priority.MEDIUM,
            "STATE": Priority.MEDIUM,
        },
        
        # Priority 6: Software distribution
        "Software": {
            "PACKAGES": Priority.MEDIUM,
            "PACKAGE": Priority.MEDIUM,
            "package": Priority.MEDIUM,
            "FILE": Priority.MEDIUM,
        },
        
        # Priority 7: Everything else (LOW)
        "Analytics": {},  # All default to LOW
        "SCIM": {},       # All default to LOW
        "RootCause": {},  # All default to LOW
        "App": {
            "VERSION": Priority.HIGH,      # Server version is important
            "PROCESSES": Priority.CRITICAL, # Process list (same as Process domain)
            "LEVELS": Priority.MEDIUM,
        },
        "Product": {
            "QUERY": Priority.MEDIUM,
            "product": Priority.MEDIUM,
            "PRODUCTS": Priority.MEDIUM,
            "BOM": Priority.LOW,
        },
    }
    
    @classmethod
    def classify(
        cls,
        domain: str,
        endpoint_name: str,
        is_internal: bool,
        path: str
    ) -> Priority:
        """Classify an endpoint's priority.
        
        Args:
            domain: Domain name (Report, Production, etc.)
            endpoint_name: Endpoint constant name or method name
            is_internal: Whether this is an internal API endpoint
            path: Full endpoint path
            
        Returns:
            Priority level
        """
        # Get domain rules
        domain_rules = cls.PRIORITY_RULES.get(domain, {})
        
        # Check specific endpoint rule
        if endpoint_name in domain_rules:
            return domain_rules[endpoint_name]
        
        # Default priorities by domain
        domain_defaults = {
            "Process": Priority.HIGH,       # Core functions
            "Report": Priority.HIGH,        # Report operations
            "Production": Priority.MEDIUM,   # Production operations
            "Asset": Priority.MEDIUM,       # Asset operations
            "Software": Priority.MEDIUM,    # Software distribution
            "Product": Priority.MEDIUM,     # Product data
            "Analytics": Priority.LOW,      # Analytics/reporting
            "SCIM": Priority.LOW,           # User provisioning
            "RootCause": Priority.LOW,      # Ticketing
            "App": Priority.MEDIUM,         # Server metadata
        }
        
        return domain_defaults.get(domain, Priority.LOW)
    
    @classmethod
    def get_description(cls, domain: str, endpoint_name: str, path: str) -> str:
        """Generate human-readable description for endpoint.
        
        Args:
            domain: Domain name
            endpoint_name: Endpoint name
            path: Full path
            
        Returns:
            Description string
        """
        descriptions = {
            # Process domain
            "GET_REPAIR_OPERATIONS": "Get list of repair operations/categories",
            "get_repair_operation": "Get specific repair operation details",
            "GET_PROCESSES": "Get list of test processes",
            "get_process": "Get specific process details",
            
            # Report domain
            "WSJF": "Submit test report (JSON format)",
            "WSXF": "Submit test report (XML format)",
            "wsjf": "Retrieve test report by ID (JSON)",
            "wsxf": "Retrieve test report by ID (XML)",
            "QUERY_HEADER": "Query report headers with filters",
            
            # Production domain - Serial numbers
            "SERIAL_NUMBERS_TAKE": "Take/reserve serial numbers",
            "SERIAL_NUMBERS_BY_RANGE": "Get serial numbers by range",
            "SERIAL_NUMBERS_BY_REFERENCE": "Get serial numbers by reference",
            "SERIAL_NUMBER_TYPES": "Get serial number types",
            
            # Production domain - Units
            "unit": "Get, update, or delete unit by serial/part number",
            "CREATE_UNIT": "Create new production unit",
            "ADD_CHILD_UNIT": "Add child unit (box build/assembly)",
            "REMOVE_CHILD_UNIT": "Remove child unit",
            "SET_UNIT_PHASE": "Set unit production phase",
            "SET_UNIT_PROCESS": "Set unit test process",
            
            # Asset domain
            "SET_RUNNING_COUNT": "Update asset running count",
            "SET_TOTAL_COUNT": "Update asset total count",
            "MESSAGE": "Get asset alarms/messages",
            "LOG": "Get asset log/alarm history",
            
            # Software domain
            "PACKAGES": "List software packages",
            "package": "Manage software package",
        }
        
        return descriptions.get(endpoint_name, f"{domain} - {path}")
