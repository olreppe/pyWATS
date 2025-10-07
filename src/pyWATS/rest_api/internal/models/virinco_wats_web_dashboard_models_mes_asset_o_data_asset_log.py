from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetODataAssetLog")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetODataAssetLog:
    """ 
        Attributes:
            log_id (Union[Unset, int]):
            asset_id (Union[Unset, str]):
            serial_number (Union[Unset, str]):
            date (Union[Unset, datetime.datetime]):
            user (Union[Unset, str]):
            type_ (Union[Unset, int]):
            property_ (Union[Unset, str]):
            value (Union[Unset, str]):
            comment (Union[Unset, str]):
     """

    log_id: Union[Unset, int] = UNSET
    asset_id: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    user: Union[Unset, str] = UNSET
    type_: Union[Unset, int] = UNSET
    property_: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        log_id = self.log_id

        asset_id = self.asset_id

        serial_number = self.serial_number

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        user = self.user

        type_ = self.type_

        property_ = self.property_

        value = self.value

        comment = self.comment


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if log_id is not UNSET:
            field_dict["logId"] = log_id
        if asset_id is not UNSET:
            field_dict["assetId"] = asset_id
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if date is not UNSET:
            field_dict["date"] = date
        if user is not UNSET:
            field_dict["user"] = user
        if type_ is not UNSET:
            field_dict["type"] = type_
        if property_ is not UNSET:
            field_dict["property"] = property_
        if value is not UNSET:
            field_dict["value"] = value
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        log_id = d.pop("logId", UNSET)

        asset_id = d.pop("assetId", UNSET)

        serial_number = d.pop("serialNumber", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date,  Unset):
            date = UNSET
        else:
            date = isoparse(_date)




        user = d.pop("user", UNSET)

        type_ = d.pop("type", UNSET)

        property_ = d.pop("property", UNSET)

        value = d.pop("value", UNSET)

        comment = d.pop("comment", UNSET)

        virinco_wats_web_dashboard_models_mes_asset_o_data_asset_log = cls(
            log_id=log_id,
            asset_id=asset_id,
            serial_number=serial_number,
            date=date,
            user=user,
            type_=type_,
            property_=property_,
            value=value,
            comment=comment,
        )


        virinco_wats_web_dashboard_models_mes_asset_o_data_asset_log.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_o_data_asset_log

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
