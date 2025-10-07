from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionProductionBatch")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionProductionBatch:
    """ 
        Attributes:
            batch_sn (Union[Unset, str]):
            batch_size (Union[Unset, int]):
            produced (Union[Unset, int]):
            xml_data (Union[Unset, str]):
     """

    batch_sn: Union[Unset, str] = UNSET
    batch_size: Union[Unset, int] = UNSET
    produced: Union[Unset, int] = UNSET
    xml_data: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        batch_sn = self.batch_sn

        batch_size = self.batch_size

        produced = self.produced

        xml_data = self.xml_data


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if batch_sn is not UNSET:
            field_dict["BatchSN"] = batch_sn
        if batch_size is not UNSET:
            field_dict["BatchSize"] = batch_size
        if produced is not UNSET:
            field_dict["Produced"] = produced
        if xml_data is not UNSET:
            field_dict["XMLData"] = xml_data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        batch_sn = d.pop("BatchSN", UNSET)

        batch_size = d.pop("BatchSize", UNSET)

        produced = d.pop("Produced", UNSET)

        xml_data = d.pop("XMLData", UNSET)

        virinco_wats_web_dashboard_models_mes_production_production_batch = cls(
            batch_sn=batch_sn,
            batch_size=batch_size,
            produced=produced,
            xml_data=xml_data,
        )


        virinco_wats_web_dashboard_models_mes_production_production_batch.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_production_batch

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
