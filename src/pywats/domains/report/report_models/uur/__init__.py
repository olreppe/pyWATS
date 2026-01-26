"""
UUR (Unit Under Repair) report models.

Simplified Pydantic models following UUTReport design pattern.
Failures are stored on sub-units (UURSubUnit.failures), not on the report.
"""

# Core UUR models
from .uur_report import UURReport
from .uur_info import UURInfo
from .uur_sub_unit import UURSubUnit, UURFailure
from .uur_attachment import UURAttachment

# Legacy imports (deprecated - kept for backward compatibility)
# TODO: Remove in v0.2.0
from .uur_part_info import UURPartInfo  # Use UURSubUnit instead
from .failure import Failure  # Use UURFailure instead
from .fail_code import FailCode, FailCodes, FailureTypeEnum  # Fail codes now from ProcessService
from .misc_uur_info import MiscUURInfo, MiscUURInfoCollection  # Use Report.misc_infos instead
from .sub_repair import SubRepair  # Legacy

__all__ = [
    # Core models (use these)
    'UURReport',
    'UURInfo',
    'UURSubUnit',
    'UURFailure',
    'UURAttachment',
    
    # Deprecated (for backward compatibility only)
    'UURPartInfo',  # Deprecated: Use UURSubUnit
    'Failure',  # Deprecated: Use UURFailure
    'FailCode',  # Deprecated: Use ProcessService.get_fail_codes()
    'FailCodes',  # Deprecated
    'FailureTypeEnum',  # Deprecated
    'MiscUURInfo',  # Deprecated: Use Report.misc_infos
    'MiscUURInfoCollection',  # Deprecated
    'SubRepair',  # Legacy
]