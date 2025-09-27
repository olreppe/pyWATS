"""
MES Models Module

Consolidated data models for Manufacturing Execution System operations including:
- Asset management models
- Product management models  
- Manufacturing-specific data structures

This module consolidates models from rest_api.models and mes.models to provide
a single source of truth for MES-related data models.
"""

# Asset models (consolidated from rest_api.models.asset + mes asset response)
from .assets import (
    Asset, AssetType, AssetLog, AssetMessage, AssetState, AssetLogType, 
    Setting, AssetResponse
)

# Product models (consolidated from rest_api.models.product + mes product models)
from .products import (
    Product, ProductInfo, ProductRevision, ProductView, Vendor
)

# Asset models (consolidated from rest_api.models.asset + mes asset response)
from .assets import (
    Asset, AssetType, AssetLog, AssetMessage, AssetState, AssetLogType, 
    Setting, AssetResponse
)

# Product models (consolidated from rest_api.models.product + mes product models)
from .products import (
    Product, ProductInfo, ProductRevision, ProductView, Vendor
)

# Import MES-specific models from parent models.py
try:
    # Use importlib to import the actual models.py file, not this package
    import importlib.util
    import os
    
    # Get the path to the actual models.py file in the parent directory
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    models_path = os.path.join(parent_dir, 'models.py')
    
    if os.path.exists(models_path):
        spec = importlib.util.spec_from_file_location("mes_models", models_path)
        mes_models = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mes_models)
        
        # Import the specific models we need
        UnitPhase = getattr(mes_models, 'UnitPhase', None)
        StatusEnum = getattr(mes_models, 'StatusEnum', None)
        ActivityTestResult = getattr(mes_models, 'ActivityTestResult', None)
        ActivityMethod = getattr(mes_models, 'ActivityMethod', None)
        UnitInfo = getattr(mes_models, 'UnitInfo', None)
        UnitHistory = getattr(mes_models, 'UnitHistory', None)
        UnitVerificationResponse = getattr(mes_models, 'UnitVerificationResponse', None)
        Package = getattr(mes_models, 'Package', None)
        WorkflowContext = getattr(mes_models, 'WorkflowContext', None)
        WorkflowResult = getattr(mes_models, 'WorkflowResult', None)
        MESResponse = getattr(mes_models, 'MESResponse', None)
        IdentifyUnitRequest = getattr(mes_models, 'IdentifyUnitRequest', None)
        IdentifyProductRequest = getattr(mes_models, 'IdentifyProductRequest', None)
    else:
        # Define None placeholders if original models.py not found
        UnitPhase = StatusEnum = ActivityTestResult = ActivityMethod = None
        UnitInfo = UnitHistory = UnitVerificationResponse = Package = None
        WorkflowContext = WorkflowResult = MESResponse = None
        IdentifyUnitRequest = IdentifyProductRequest = None
        
except (ImportError, AttributeError):
    # Safe fallback - define None placeholders
    UnitPhase = StatusEnum = ActivityTestResult = ActivityMethod = None
    UnitInfo = UnitHistory = UnitVerificationResponse = Package = None
    WorkflowContext = WorkflowResult = MESResponse = None
    IdentifyUnitRequest = IdentifyProductRequest = None

__all__ = [
    # Asset Models
    "Asset", "AssetType", "AssetLog", "AssetMessage", "AssetState", "AssetLogType", 
    "Setting", "AssetResponse",
    
    # Product Models  
    "Product", "ProductInfo", "ProductRevision", "ProductView", "Vendor",
    
    # MES-specific Models (may be None if not available)
    "UnitPhase", "StatusEnum", "ActivityTestResult", "ActivityMethod",
    "UnitInfo", "UnitHistory", "UnitVerificationResponse", "Package",
    "WorkflowContext", "WorkflowResult", "MESResponse",
    "IdentifyUnitRequest", "IdentifyProductRequest"
]