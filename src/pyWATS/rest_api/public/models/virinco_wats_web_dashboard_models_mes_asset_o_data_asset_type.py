from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetODataAssetType")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetODataAssetType:
    """ 
        Attributes:
            type_id (Union[Unset, UUID]): Type ID, Rowguid for SQL replication Example:
                00000000-0000-0000-0000-000000000000.
            type_name (Union[Unset, str]): Name of type
            running_count_limit (Union[Unset, int]): Max count until next calibration must be performed (interval)
            total_count_limit (Union[Unset, int]): Asset total count limit
            maintenance_interval (Union[Unset, float]): Interval for maintenance (in days e.g 1.0 or 1.5)
            calibration_interval (Union[Unset, float]): Interval for calibration (in days e.g 1.0 or 1.5)
            warning_threshold (Union[Unset, float]): Warning threshold percent
            alarm_threshold (Union[Unset, float]): Alarm threshold percent
            is_readonly (Union[Unset, bool]): Type is read-only
            icon (Union[Unset, str]): Icon for an asset type
     """

    type_id: Union[Unset, UUID] = UNSET
    type_name: Union[Unset, str] = UNSET
    running_count_limit: Union[Unset, int] = UNSET
    total_count_limit: Union[Unset, int] = UNSET
    maintenance_interval: Union[Unset, float] = UNSET
    calibration_interval: Union[Unset, float] = UNSET
    warning_threshold: Union[Unset, float] = UNSET
    alarm_threshold: Union[Unset, float] = UNSET
    is_readonly: Union[Unset, bool] = UNSET
    icon: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_id: Union[Unset, str] = UNSET
        if not isinstance(self.type_id, Unset):
            type_id = str(self.type_id)

        type_name = self.type_name

        running_count_limit = self.running_count_limit

        total_count_limit = self.total_count_limit

        maintenance_interval = self.maintenance_interval

        calibration_interval = self.calibration_interval

        warning_threshold = self.warning_threshold

        alarm_threshold = self.alarm_threshold

        is_readonly = self.is_readonly

        icon = self.icon


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_id is not UNSET:
            field_dict["typeId"] = type_id
        if type_name is not UNSET:
            field_dict["typeName"] = type_name
        if running_count_limit is not UNSET:
            field_dict["runningCountLimit"] = running_count_limit
        if total_count_limit is not UNSET:
            field_dict["totalCountLimit"] = total_count_limit
        if maintenance_interval is not UNSET:
            field_dict["maintenanceInterval"] = maintenance_interval
        if calibration_interval is not UNSET:
            field_dict["calibrationInterval"] = calibration_interval
        if warning_threshold is not UNSET:
            field_dict["warningThreshold"] = warning_threshold
        if alarm_threshold is not UNSET:
            field_dict["alarmThreshold"] = alarm_threshold
        if is_readonly is not UNSET:
            field_dict["isReadonly"] = is_readonly
        if icon is not UNSET:
            field_dict["icon"] = icon

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_id = d.pop("typeId", UNSET)
        type_id: Union[Unset, UUID]
        if isinstance(_type_id,  Unset):
            type_id = UNSET
        else:
            type_id = UUID(_type_id)




        type_name = d.pop("typeName", UNSET)

        running_count_limit = d.pop("runningCountLimit", UNSET)

        total_count_limit = d.pop("totalCountLimit", UNSET)

        maintenance_interval = d.pop("maintenanceInterval", UNSET)

        calibration_interval = d.pop("calibrationInterval", UNSET)

        warning_threshold = d.pop("warningThreshold", UNSET)

        alarm_threshold = d.pop("alarmThreshold", UNSET)

        is_readonly = d.pop("isReadonly", UNSET)

        icon = d.pop("icon", UNSET)

        virinco_wats_web_dashboard_models_mes_asset_o_data_asset_type = cls(
            type_id=type_id,
            type_name=type_name,
            running_count_limit=running_count_limit,
            total_count_limit=total_count_limit,
            maintenance_interval=maintenance_interval,
            calibration_interval=calibration_interval,
            warning_threshold=warning_threshold,
            alarm_threshold=alarm_threshold,
            is_readonly=is_readonly,
            icon=icon,
        )


        virinco_wats_web_dashboard_models_mes_asset_o_data_asset_type.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_o_data_asset_type

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
