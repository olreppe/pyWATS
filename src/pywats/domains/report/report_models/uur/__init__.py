"""
UUR (Unit Under Repair) report models.

Simplified Pydantic models following UUTReport design pattern.
Failures are stored on sub-units (UURSubUnit.failures), not on the report.
Attachments use the shared Attachment class from report_models.
"""

# Core UUR models
from .uur_report import UURReport
from .uur_info import UURInfo
from .uur_sub_unit import UURSubUnit, UURFailure

# Shared attachment (same as UUT)
from ..attachment import Attachment

# Legacy imports (deprecated - kept for backward compatibility)
# TODO: Remove in v0.2.0
from .uur_attachment import UURAttachment  # Deprecated: Use Attachment instead
from .uur_part_info import UURPartInfo  # Deprecated: Use UURSubUnit instead
from .failure import Failure  # Deprecated: Use UURFailure instead
from .fail_code import FailCode, FailCodes, FailureTypeEnum  # Deprecated: Use ProcessService
from .misc_uur_info import MiscUURInfo, MiscUURInfoCollection  # Deprecated: Use Report.misc_infos
from .sub_repair import SubRepair  # Legacy

__all__ = [
    # Core models (use these)
    'UURReport',
    'UURInfo',
    'UURSubUnit',
    'UURFailure',
    'Attachment',  # Shared with UUT
    
    # Deprecated (for backward compatibility only - will be removed in v0.2.0)
    'UURAttachment',  # Deprecated: Use Attachment
    'UURPartInfo',  # Deprecated: Use UURSubUnit
    'Failure',  # Deprecated: Use UURFailure
    'FailCode',  # Deprecated: Use ProcessService.get_fail_codes()
    'FailCodes',  # Deprecated
    'FailureTypeEnum',  # Deprecated
    'MiscUURInfo',  # Deprecated: Use Report.misc_infos
    'MiscUURInfoCollection',  # Deprecated
    'SubRepair',  # Legacy
]