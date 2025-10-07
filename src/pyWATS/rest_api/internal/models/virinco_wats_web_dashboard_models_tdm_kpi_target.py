from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmKpiTarget")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmKpiTarget:
    """ 
        Attributes:
            kpi_target_id (Union[Unset, int]):
            type_ (Union[Unset, int]):
            process_code (Union[Unset, int]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            product_selection_id (Union[Unset, int]):
            alarm (Union[Unset, float]):
            warning (Union[Unset, float]):
            target_weight (Union[Unset, float]):
     """

    kpi_target_id: Union[Unset, int] = UNSET
    type_: Union[Unset, int] = UNSET
    process_code: Union[Unset, int] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    product_selection_id: Union[Unset, int] = UNSET
    alarm: Union[Unset, float] = UNSET
    warning: Union[Unset, float] = UNSET
    target_weight: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        kpi_target_id = self.kpi_target_id

        type_ = self.type_

        process_code = self.process_code

        part_number = self.part_number

        revision = self.revision

        product_selection_id = self.product_selection_id

        alarm = self.alarm

        warning = self.warning

        target_weight = self.target_weight


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if kpi_target_id is not UNSET:
            field_dict["kpiTargetId"] = kpi_target_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if product_selection_id is not UNSET:
            field_dict["productSelectionId"] = product_selection_id
        if alarm is not UNSET:
            field_dict["alarm"] = alarm
        if warning is not UNSET:
            field_dict["warning"] = warning
        if target_weight is not UNSET:
            field_dict["targetWeight"] = target_weight

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kpi_target_id = d.pop("kpiTargetId", UNSET)

        type_ = d.pop("type", UNSET)

        process_code = d.pop("processCode", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        product_selection_id = d.pop("productSelectionId", UNSET)

        alarm = d.pop("alarm", UNSET)

        warning = d.pop("warning", UNSET)

        target_weight = d.pop("targetWeight", UNSET)

        virinco_wats_web_dashboard_models_tdm_kpi_target = cls(
            kpi_target_id=kpi_target_id,
            type_=type_,
            process_code=process_code,
            part_number=part_number,
            revision=revision,
            product_selection_id=product_selection_id,
            alarm=alarm,
            warning=warning,
            target_weight=target_weight,
        )


        virinco_wats_web_dashboard_models_tdm_kpi_target.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_kpi_target

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
