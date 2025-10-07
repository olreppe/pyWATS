from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFAssetStats")



@_attrs_define
class VirincoWATSSchemasWSJFAssetStats:
    """ 
        Attributes:
            asset_sn (Union[Unset, str]): Serial number of the asset.
            running_count (Union[Unset, int]): How many times the asset has been used since last calibration.
            running_count_exceeded (Union[Unset, int]): How many times more than the limit the asset has been used since
                last calibration.
            total_count (Union[Unset, int]): How many times the asset has been used in its lifetime.
            total_count_exceeded (Union[Unset, int]): How many times more than the limit the asset has been used in its
                lifetime.
            days_since_calibration (Union[Unset, float]): How many days since the last calibration.
            is_days_since_calibration_unknown (Union[Unset, bool]): If the asset has never been calibrated, then it is
                unknown.
            calibration_days_overdue (Union[Unset, float]): How many days since calibration was overdue.
            days_since_maintenance (Union[Unset, float]): How many days since maintenance was overdue.
            is_days_since_maintenance_unknown (Union[Unset, bool]): If the asset has never been maintenance, then it is
                unknown.
            maintenance_days_overdue (Union[Unset, float]): How many days since maintenance was overdue.
            message (Union[Unset, str]): Message from stats calulation.
     """

    asset_sn: Union[Unset, str] = UNSET
    running_count: Union[Unset, int] = UNSET
    running_count_exceeded: Union[Unset, int] = UNSET
    total_count: Union[Unset, int] = UNSET
    total_count_exceeded: Union[Unset, int] = UNSET
    days_since_calibration: Union[Unset, float] = UNSET
    is_days_since_calibration_unknown: Union[Unset, bool] = UNSET
    calibration_days_overdue: Union[Unset, float] = UNSET
    days_since_maintenance: Union[Unset, float] = UNSET
    is_days_since_maintenance_unknown: Union[Unset, bool] = UNSET
    maintenance_days_overdue: Union[Unset, float] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        asset_sn = self.asset_sn

        running_count = self.running_count

        running_count_exceeded = self.running_count_exceeded

        total_count = self.total_count

        total_count_exceeded = self.total_count_exceeded

        days_since_calibration = self.days_since_calibration

        is_days_since_calibration_unknown = self.is_days_since_calibration_unknown

        calibration_days_overdue = self.calibration_days_overdue

        days_since_maintenance = self.days_since_maintenance

        is_days_since_maintenance_unknown = self.is_days_since_maintenance_unknown

        maintenance_days_overdue = self.maintenance_days_overdue

        message = self.message


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if asset_sn is not UNSET:
            field_dict["assetSN"] = asset_sn
        if running_count is not UNSET:
            field_dict["runningCount"] = running_count
        if running_count_exceeded is not UNSET:
            field_dict["runningCountExceeded"] = running_count_exceeded
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count
        if total_count_exceeded is not UNSET:
            field_dict["totalCountExceeded"] = total_count_exceeded
        if days_since_calibration is not UNSET:
            field_dict["daysSinceCalibration"] = days_since_calibration
        if is_days_since_calibration_unknown is not UNSET:
            field_dict["isDaysSinceCalibrationUnknown"] = is_days_since_calibration_unknown
        if calibration_days_overdue is not UNSET:
            field_dict["calibrationDaysOverdue"] = calibration_days_overdue
        if days_since_maintenance is not UNSET:
            field_dict["daysSinceMaintenance"] = days_since_maintenance
        if is_days_since_maintenance_unknown is not UNSET:
            field_dict["isDaysSinceMaintenanceUnknown"] = is_days_since_maintenance_unknown
        if maintenance_days_overdue is not UNSET:
            field_dict["maintenanceDaysOverdue"] = maintenance_days_overdue
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_sn = d.pop("assetSN", UNSET)

        running_count = d.pop("runningCount", UNSET)

        running_count_exceeded = d.pop("runningCountExceeded", UNSET)

        total_count = d.pop("totalCount", UNSET)

        total_count_exceeded = d.pop("totalCountExceeded", UNSET)

        days_since_calibration = d.pop("daysSinceCalibration", UNSET)

        is_days_since_calibration_unknown = d.pop("isDaysSinceCalibrationUnknown", UNSET)

        calibration_days_overdue = d.pop("calibrationDaysOverdue", UNSET)

        days_since_maintenance = d.pop("daysSinceMaintenance", UNSET)

        is_days_since_maintenance_unknown = d.pop("isDaysSinceMaintenanceUnknown", UNSET)

        maintenance_days_overdue = d.pop("maintenanceDaysOverdue", UNSET)

        message = d.pop("message", UNSET)

        virinco_wats_schemas_wsjf_asset_stats = cls(
            asset_sn=asset_sn,
            running_count=running_count,
            running_count_exceeded=running_count_exceeded,
            total_count=total_count,
            total_count_exceeded=total_count_exceeded,
            days_since_calibration=days_since_calibration,
            is_days_since_calibration_unknown=is_days_since_calibration_unknown,
            calibration_days_overdue=calibration_days_overdue,
            days_since_maintenance=days_since_maintenance,
            is_days_since_maintenance_unknown=is_days_since_maintenance_unknown,
            maintenance_days_overdue=maintenance_days_overdue,
            message=message,
        )


        virinco_wats_schemas_wsjf_asset_stats.additional_properties = d
        return virinco_wats_schemas_wsjf_asset_stats

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
