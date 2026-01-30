"""
ReportProxyMixin - Provides flat API access to ReportCommon fields

This mixin adds property proxies that delegate to `self.common`, providing
a flat API like v1 while maintaining composition internally.

Usage:
    class UUTReport(ReportProxyMixin, WATSBase):
        common: ReportCommon
        ...
        
    # Now both work:
    report.pn           # Flat access (via property proxy)
    report.common.pn    # Explicit composition access
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

if TYPE_CHECKING:
    from .report_common import ReportCommon
    from ..report_models.misc_info import MiscInfo
    from ..report_models.asset import Asset, AssetStats
    from ..report_models.sub_unit import SubUnit
    from ..report_models.binary_data import BinaryData
    from ..report_models.additional_data import AdditionalData


class ReportProxyMixin:
    """
    Mixin that provides flat API access to ReportCommon fields.
    
    Classes using this mixin must have a `common: ReportCommon` field.
    
    This enables both access patterns:
        report.pn           # Flat (v1 compatible)
        report.common.pn    # Explicit composition (v2)
    """
    
    # Required for type checking - classes using this mixin must have 'common'
    common: 'ReportCommon'
    
    # =========================================================================
    # Identity Fields
    # =========================================================================
    
    @property
    def id(self) -> UUID:
        """Report UUID."""
        return self.common.id
    
    @id.setter
    def id(self, value: UUID) -> None:
        self.common.id = value
    
    @property
    def pn(self) -> str:
        """Part number."""
        return self.common.pn
    
    @pn.setter
    def pn(self, value: str) -> None:
        self.common.pn = value
    
    @property
    def sn(self) -> str:
        """Serial number."""
        return self.common.sn
    
    @sn.setter
    def sn(self, value: str) -> None:
        self.common.sn = value
    
    @property
    def rev(self) -> str:
        """Revision."""
        return self.common.rev
    
    @rev.setter
    def rev(self, value: str) -> None:
        self.common.rev = value
    
    @property
    def process_code(self) -> int:
        """Process code."""
        return self.common.process_code
    
    @process_code.setter
    def process_code(self, value: int) -> None:
        self.common.process_code = value
    
    # =========================================================================
    # Result
    # =========================================================================
    
    @property
    def result(self) -> str:
        """Result: P=Passed, F=Failed, E=Error, D=Done, T=Terminated."""
        return self.common.result
    
    @result.setter
    def result(self, value: str) -> None:
        self.common.result = value
    
    # =========================================================================
    # Station Info
    # =========================================================================
    
    @property
    def station_name(self) -> str:
        """Station/machine name."""
        return self.common.station_name
    
    @station_name.setter
    def station_name(self, value: str) -> None:
        self.common.station_name = value
    
    @property
    def location(self) -> str:
        """Location."""
        return self.common.location
    
    @location.setter
    def location(self, value: str) -> None:
        self.common.location = value
    
    @property
    def purpose(self) -> str:
        """Purpose."""
        return self.common.purpose
    
    @purpose.setter
    def purpose(self, value: str) -> None:
        self.common.purpose = value
    
    # =========================================================================
    # Timing Fields
    # =========================================================================
    
    @property
    def start(self) -> datetime | None:
        """Start time (local with timezone)."""
        return self.common.start
    
    @start.setter
    def start(self, value: datetime | None) -> None:
        self.common.start = value
    
    @property
    def start_utc(self) -> datetime | None:
        """Start time (UTC)."""
        return self.common.start_utc
    
    @start_utc.setter
    def start_utc(self, value: datetime | None) -> None:
        self.common.start_utc = value
    
    # =========================================================================
    # Collections
    # =========================================================================
    
    @property
    def misc_infos(self) -> list['MiscInfo']:
        """Miscellaneous info list."""
        return self.common.misc_infos
    
    @misc_infos.setter
    def misc_infos(self, value: list['MiscInfo']) -> None:
        self.common.misc_infos = value
    
    # Alias for v1 compatibility (misc_info_list -> misc_infos)
    @property
    def misc_info_list(self) -> list['MiscInfo']:
        """Alias for misc_infos (v1 compatibility)."""
        return self.common.misc_infos
    
    @misc_info_list.setter
    def misc_info_list(self, value: list['MiscInfo']) -> None:
        self.common.misc_infos = value
    
    @property
    def assets(self) -> list['Asset']:
        """Asset list."""
        return self.common.assets
    
    @assets.setter
    def assets(self, value: list['Asset']) -> None:
        self.common.assets = value
    
    # Alias for v1 compatibility (asset_list -> assets)
    @property
    def asset_list(self) -> list['Asset']:
        """Alias for assets (v1 compatibility)."""
        return self.common.assets
    
    @asset_list.setter
    def asset_list(self, value: list['Asset']) -> None:
        self.common.assets = value
    
    @property
    def asset_stats(self) -> list['AssetStats'] | None:
        """Asset statistics (output only)."""
        return self.common.asset_stats
    
    @asset_stats.setter
    def asset_stats(self, value: list['AssetStats'] | None) -> None:
        self.common.asset_stats = value
    
    @property
    def binary_data(self) -> list['BinaryData']:
        """Binary data list."""
        return self.common.binary_data
    
    @binary_data.setter
    def binary_data(self, value: list['BinaryData']) -> None:
        self.common.binary_data = value
    
    @property
    def additional_data(self) -> list['AdditionalData | None']:
        """Additional data list."""
        return self.common.additional_data
    
    @additional_data.setter
    def additional_data(self, value: list['AdditionalData | None']) -> None:
        self.common.additional_data = value
    
    # =========================================================================
    # Output-only Fields
    # =========================================================================
    
    @property
    def origin(self) -> str | None:
        """Origin (output only)."""
        return self.common.origin
    
    @origin.setter
    def origin(self, value: str | None) -> None:
        self.common.origin = value
    
    @property
    def product_name(self) -> str | None:
        """Product name (output only)."""
        return self.common.product_name
    
    @product_name.setter
    def product_name(self, value: str | None) -> None:
        self.common.product_name = value
    
    @property
    def process_name(self) -> str | None:
        """Process name (output only)."""
        return self.common.process_name
    
    @process_name.setter
    def process_name(self, value: str | None) -> None:
        self.common.process_name = value
    
    # =========================================================================
    # Helper Methods (delegate to common)
    # =========================================================================
    
    def add_misc_info(self, description: str, value: Any) -> 'MiscInfo':
        """Add miscellaneous information to the report."""
        return self.common.add_misc_info(description, value)
    
    def add_sub_unit(self, part_type: str, sn: str, pn: str, rev: str) -> 'SubUnit':
        """Add a sub-unit/component to the report."""
        return self.common.add_sub_unit(part_type, sn, pn, rev)
    
    def add_asset(self, sn: str, usage_count: int) -> 'Asset':
        """Add an asset to the report."""
        return self.common.add_asset(sn, usage_count)
