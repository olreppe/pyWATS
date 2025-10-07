from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch:
    """ 
        Attributes:
            batch_number (Union[Unset, str]):
            batch_size (Union[Unset, int]):
     """

    batch_number: Union[Unset, str] = UNSET
    batch_size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        batch_number = self.batch_number

        batch_size = self.batch_size


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if batch_number is not UNSET:
            field_dict["batchNumber"] = batch_number
        if batch_size is not UNSET:
            field_dict["batchSize"] = batch_size

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        batch_number = d.pop("batchNumber", UNSET)

        batch_size = d.pop("batchSize", UNSET)

        virinco_wats_web_dashboard_models_mes_production_public_production_batch = cls(
            batch_number=batch_number,
            batch_size=batch_size,
        )


        virinco_wats_web_dashboard_models_mes_production_public_production_batch.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_public_production_batch

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
