from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmUnitVerificationRule")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmUnitVerificationRule:
    """ 
        Attributes:
            unit_verification_id (Union[Unset, int]):
            product_selection_id (Union[Unset, int]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            process_codes (Union[Unset, list[int]]):
     """

    unit_verification_id: Union[Unset, int] = UNSET
    product_selection_id: Union[Unset, int] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    process_codes: Union[Unset, list[int]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        unit_verification_id = self.unit_verification_id

        product_selection_id = self.product_selection_id

        part_number = self.part_number

        revision = self.revision

        process_codes: Union[Unset, list[int]] = UNSET
        if not isinstance(self.process_codes, Unset):
            process_codes = self.process_codes




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if unit_verification_id is not UNSET:
            field_dict["unitVerificationId"] = unit_verification_id
        if product_selection_id is not UNSET:
            field_dict["productSelectionId"] = product_selection_id
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if process_codes is not UNSET:
            field_dict["processCodes"] = process_codes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        unit_verification_id = d.pop("unitVerificationId", UNSET)

        product_selection_id = d.pop("productSelectionId", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        process_codes = cast(list[int], d.pop("processCodes", UNSET))


        virinco_wats_web_dashboard_models_tdm_unit_verification_rule = cls(
            unit_verification_id=unit_verification_id,
            product_selection_id=product_selection_id,
            part_number=part_number,
            revision=revision,
            process_codes=process_codes,
        )


        virinco_wats_web_dashboard_models_tdm_unit_verification_rule.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_unit_verification_rule

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
