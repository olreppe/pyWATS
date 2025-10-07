from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsODataAsset")



@_attrs_define
class VirincoWATSWebDashboardModelsODataAsset:
    """ 
        Attributes:
            serial_number (Union[Unset, str]): Asset serial number
            running_count (Union[Unset, int]): Asset running count when report was processed
            running_count_exceeded (Union[Unset, int]): Asset running count limit execeeded by when report was processed
            total_count (Union[Unset, int]): Asset total count when report was processed
            total_count_exceeded (Union[Unset, int]): Asset total count limit execeeded when report was processed
            days_since_maintenance (Union[Unset, float]): Days since previous asset maintenance when report was processed
            maintenance_days_overdue (Union[Unset, float]): Days overdue asset maintenance limit when report was processed
            days_since_calibration (Union[Unset, float]): Days since previous asset calibration when report was processed
            calibration_days_overdue (Union[Unset, float]): Days overdue asset calibration limit when report was processed
     """

    serial_number: Union[Unset, str] = UNSET
    running_count: Union[Unset, int] = UNSET
    running_count_exceeded: Union[Unset, int] = UNSET
    total_count: Union[Unset, int] = UNSET
    total_count_exceeded: Union[Unset, int] = UNSET
    days_since_maintenance: Union[Unset, float] = UNSET
    maintenance_days_overdue: Union[Unset, float] = UNSET
    days_since_calibration: Union[Unset, float] = UNSET
    calibration_days_overdue: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        serial_number = self.serial_number

        running_count = self.running_count

        running_count_exceeded = self.running_count_exceeded

        total_count = self.total_count

        total_count_exceeded = self.total_count_exceeded

        days_since_maintenance = self.days_since_maintenance

        maintenance_days_overdue = self.maintenance_days_overdue

        days_since_calibration = self.days_since_calibration

        calibration_days_overdue = self.calibration_days_overdue


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if running_count is not UNSET:
            field_dict["runningCount"] = running_count
        if running_count_exceeded is not UNSET:
            field_dict["runningCountExceeded"] = running_count_exceeded
        if total_count is not UNSET:
            field_dict["totalCount"] = total_count
        if total_count_exceeded is not UNSET:
            field_dict["totalCountExceeded"] = total_count_exceeded
        if days_since_maintenance is not UNSET:
            field_dict["daysSinceMaintenance"] = days_since_maintenance
        if maintenance_days_overdue is not UNSET:
            field_dict["maintenanceDaysOverdue"] = maintenance_days_overdue
        if days_since_calibration is not UNSET:
            field_dict["daysSinceCalibration"] = days_since_calibration
        if calibration_days_overdue is not UNSET:
            field_dict["calibrationDaysOverdue"] = calibration_days_overdue

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        serial_number = d.pop("serialNumber", UNSET)

        running_count = d.pop("runningCount", UNSET)

        running_count_exceeded = d.pop("runningCountExceeded", UNSET)

        total_count = d.pop("totalCount", UNSET)

        total_count_exceeded = d.pop("totalCountExceeded", UNSET)

        days_since_maintenance = d.pop("daysSinceMaintenance", UNSET)

        maintenance_days_overdue = d.pop("maintenanceDaysOverdue", UNSET)

        days_since_calibration = d.pop("daysSinceCalibration", UNSET)

        calibration_days_overdue = d.pop("calibrationDaysOverdue", UNSET)

        virinco_wats_web_dashboard_models_o_data_asset = cls(
            serial_number=serial_number,
            running_count=running_count,
            running_count_exceeded=running_count_exceeded,
            total_count=total_count,
            total_count_exceeded=total_count_exceeded,
            days_since_maintenance=days_since_maintenance,
            maintenance_days_overdue=maintenance_days_overdue,
            days_since_calibration=days_since_calibration,
            calibration_days_overdue=calibration_days_overdue,
        )


        virinco_wats_web_dashboard_models_o_data_asset.additional_properties = d
        return virinco_wats_web_dashboard_models_o_data_asset

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
