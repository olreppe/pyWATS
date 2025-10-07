from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmKpiTargetRequest")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmKpiTargetRequest:
    """ Definition for requesting kpi targets

        Attributes:
            part_number (Union[Unset, str]):
            product_name (Union[Unset, str]):
            revision (Union[Unset, str]):
            process_code (Union[Unset, int]):
            process_name (Union[Unset, str]):
            product_selection_id (Union[Unset, int]):
            fpy (Union[Unset, float]):
            spy (Union[Unset, float]):
            tpy (Union[Unset, float]):
            lpy (Union[Unset, float]):
            ty (Union[Unset, float]):
            fpy_rty (Union[Unset, float]):
            spy_rty (Union[Unset, float]):
            tpy_rty (Union[Unset, float]):
            lpy_rty (Union[Unset, float]):
            ty_rty (Union[Unset, float]):
     """

    part_number: Union[Unset, str] = UNSET
    product_name: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    process_code: Union[Unset, int] = UNSET
    process_name: Union[Unset, str] = UNSET
    product_selection_id: Union[Unset, int] = UNSET
    fpy: Union[Unset, float] = UNSET
    spy: Union[Unset, float] = UNSET
    tpy: Union[Unset, float] = UNSET
    lpy: Union[Unset, float] = UNSET
    ty: Union[Unset, float] = UNSET
    fpy_rty: Union[Unset, float] = UNSET
    spy_rty: Union[Unset, float] = UNSET
    tpy_rty: Union[Unset, float] = UNSET
    lpy_rty: Union[Unset, float] = UNSET
    ty_rty: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        part_number = self.part_number

        product_name = self.product_name

        revision = self.revision

        process_code = self.process_code

        process_name = self.process_name

        product_selection_id = self.product_selection_id

        fpy = self.fpy

        spy = self.spy

        tpy = self.tpy

        lpy = self.lpy

        ty = self.ty

        fpy_rty = self.fpy_rty

        spy_rty = self.spy_rty

        tpy_rty = self.tpy_rty

        lpy_rty = self.lpy_rty

        ty_rty = self.ty_rty


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if revision is not UNSET:
            field_dict["revision"] = revision
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if product_selection_id is not UNSET:
            field_dict["productSelectionId"] = product_selection_id
        if fpy is not UNSET:
            field_dict["fpy"] = fpy
        if spy is not UNSET:
            field_dict["spy"] = spy
        if tpy is not UNSET:
            field_dict["tpy"] = tpy
        if lpy is not UNSET:
            field_dict["lpy"] = lpy
        if ty is not UNSET:
            field_dict["ty"] = ty
        if fpy_rty is not UNSET:
            field_dict["fpyRty"] = fpy_rty
        if spy_rty is not UNSET:
            field_dict["spyRty"] = spy_rty
        if tpy_rty is not UNSET:
            field_dict["tpyRty"] = tpy_rty
        if lpy_rty is not UNSET:
            field_dict["lpyRty"] = lpy_rty
        if ty_rty is not UNSET:
            field_dict["tyRty"] = ty_rty

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        part_number = d.pop("partNumber", UNSET)

        product_name = d.pop("productName", UNSET)

        revision = d.pop("revision", UNSET)

        process_code = d.pop("processCode", UNSET)

        process_name = d.pop("processName", UNSET)

        product_selection_id = d.pop("productSelectionId", UNSET)

        fpy = d.pop("fpy", UNSET)

        spy = d.pop("spy", UNSET)

        tpy = d.pop("tpy", UNSET)

        lpy = d.pop("lpy", UNSET)

        ty = d.pop("ty", UNSET)

        fpy_rty = d.pop("fpyRty", UNSET)

        spy_rty = d.pop("spyRty", UNSET)

        tpy_rty = d.pop("tpyRty", UNSET)

        lpy_rty = d.pop("lpyRty", UNSET)

        ty_rty = d.pop("tyRty", UNSET)

        virinco_wats_web_dashboard_models_tdm_kpi_target_request = cls(
            part_number=part_number,
            product_name=product_name,
            revision=revision,
            process_code=process_code,
            process_name=process_name,
            product_selection_id=product_selection_id,
            fpy=fpy,
            spy=spy,
            tpy=tpy,
            lpy=lpy,
            ty=ty,
            fpy_rty=fpy_rty,
            spy_rty=spy_rty,
            tpy_rty=tpy_rty,
            lpy_rty=lpy_rty,
            ty_rty=ty_rty,
        )


        virinco_wats_web_dashboard_models_tdm_kpi_target_request.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_kpi_target_request

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
