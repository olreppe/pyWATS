from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmMeasureFavourite")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmMeasureFavourite:
    """ 
        Attributes:
            measure_favourite_id (Union[Unset, int]):
            level (Union[Unset, int]):
            type_ (Union[Unset, int]):
            name (Union[Unset, str]):
            name_path (Union[Unset, str]):
            disabled (Union[Unset, bool]):
            measure_name (Union[Unset, str]):
            xml_filter (Union[Unset, str]):
            process_code (Union[Unset, int]):
            pn (Union[Unset, str]):
     """

    measure_favourite_id: Union[Unset, int] = UNSET
    level: Union[Unset, int] = UNSET
    type_: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    name_path: Union[Unset, str] = UNSET
    disabled: Union[Unset, bool] = UNSET
    measure_name: Union[Unset, str] = UNSET
    xml_filter: Union[Unset, str] = UNSET
    process_code: Union[Unset, int] = UNSET
    pn: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        measure_favourite_id = self.measure_favourite_id

        level = self.level

        type_ = self.type_

        name = self.name

        name_path = self.name_path

        disabled = self.disabled

        measure_name = self.measure_name

        xml_filter = self.xml_filter

        process_code = self.process_code

        pn = self.pn


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if measure_favourite_id is not UNSET:
            field_dict["MeasureFavouriteID"] = measure_favourite_id
        if level is not UNSET:
            field_dict["Level"] = level
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if name is not UNSET:
            field_dict["Name"] = name
        if name_path is not UNSET:
            field_dict["NamePath"] = name_path
        if disabled is not UNSET:
            field_dict["Disabled"] = disabled
        if measure_name is not UNSET:
            field_dict["MeasureName"] = measure_name
        if xml_filter is not UNSET:
            field_dict["XMLFilter"] = xml_filter
        if process_code is not UNSET:
            field_dict["ProcessCode"] = process_code
        if pn is not UNSET:
            field_dict["PN"] = pn

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        measure_favourite_id = d.pop("MeasureFavouriteID", UNSET)

        level = d.pop("Level", UNSET)

        type_ = d.pop("Type", UNSET)

        name = d.pop("Name", UNSET)

        name_path = d.pop("NamePath", UNSET)

        disabled = d.pop("Disabled", UNSET)

        measure_name = d.pop("MeasureName", UNSET)

        xml_filter = d.pop("XMLFilter", UNSET)

        process_code = d.pop("ProcessCode", UNSET)

        pn = d.pop("PN", UNSET)

        virinco_wats_web_dashboard_models_tdm_measure_favourite = cls(
            measure_favourite_id=measure_favourite_id,
            level=level,
            type_=type_,
            name=name,
            name_path=name_path,
            disabled=disabled,
            measure_name=measure_name,
            xml_filter=xml_filter,
            process_code=process_code,
            pn=pn,
        )


        virinco_wats_web_dashboard_models_tdm_measure_favourite.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_measure_favourite

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
