from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_binary_data import VirincoWATSSchemasWSJFBinaryData





T = TypeVar("T", bound="VirincoWATSSchemasWSJFFailure")



@_attrs_define
class VirincoWATSSchemasWSJFFailure:
    """ 
        Attributes:
            art_number (Union[Unset, str]): Article number of failed component.
            art_rev (Union[Unset, str]): Failed component revision.
            art_vendor (Union[Unset, str]): Vendor of failed component.
            art_description (Union[Unset, str]): Description of failed component.
            category (Union[Unset, str]): Failure category.
            code (Union[Unset, str]): Failure code.
            comment (Union[Unset, str]): Failure comment.
            com_ref (Union[Unset, str]): Component reference.
            func_block (Union[Unset, str]): Function block reference.
            ref_step_id (Union[Unset, int]): Id of step from referenced UUT that uncovered failure.
            ref_step_name (Union[Unset, str]): Name of step from referenced UUT that uncovered failure.
            attachments (Union[Unset, list['VirincoWATSSchemasWSJFBinaryData']]): List of attachments in failure.
     """

    art_number: Union[Unset, str] = UNSET
    art_rev: Union[Unset, str] = UNSET
    art_vendor: Union[Unset, str] = UNSET
    art_description: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    code: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    com_ref: Union[Unset, str] = UNSET
    func_block: Union[Unset, str] = UNSET
    ref_step_id: Union[Unset, int] = UNSET
    ref_step_name: Union[Unset, str] = UNSET
    attachments: Union[Unset, list['VirincoWATSSchemasWSJFBinaryData']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_binary_data import VirincoWATSSchemasWSJFBinaryData
        art_number = self.art_number

        art_rev = self.art_rev

        art_vendor = self.art_vendor

        art_description = self.art_description

        category = self.category

        code = self.code

        comment = self.comment

        com_ref = self.com_ref

        func_block = self.func_block

        ref_step_id = self.ref_step_id

        ref_step_name = self.ref_step_name

        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if art_number is not UNSET:
            field_dict["artNumber"] = art_number
        if art_rev is not UNSET:
            field_dict["artRev"] = art_rev
        if art_vendor is not UNSET:
            field_dict["artVendor"] = art_vendor
        if art_description is not UNSET:
            field_dict["artDescription"] = art_description
        if category is not UNSET:
            field_dict["category"] = category
        if code is not UNSET:
            field_dict["code"] = code
        if comment is not UNSET:
            field_dict["comment"] = comment
        if com_ref is not UNSET:
            field_dict["comRef"] = com_ref
        if func_block is not UNSET:
            field_dict["funcBlock"] = func_block
        if ref_step_id is not UNSET:
            field_dict["refStepId"] = ref_step_id
        if ref_step_name is not UNSET:
            field_dict["refStepName"] = ref_step_name
        if attachments is not UNSET:
            field_dict["attachments"] = attachments

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_binary_data import VirincoWATSSchemasWSJFBinaryData
        d = dict(src_dict)
        art_number = d.pop("artNumber", UNSET)

        art_rev = d.pop("artRev", UNSET)

        art_vendor = d.pop("artVendor", UNSET)

        art_description = d.pop("artDescription", UNSET)

        category = d.pop("category", UNSET)

        code = d.pop("code", UNSET)

        comment = d.pop("comment", UNSET)

        com_ref = d.pop("comRef", UNSET)

        func_block = d.pop("funcBlock", UNSET)

        ref_step_id = d.pop("refStepId", UNSET)

        ref_step_name = d.pop("refStepName", UNSET)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in (_attachments or []):
            attachments_item = VirincoWATSSchemasWSJFBinaryData.from_dict(attachments_item_data)



            attachments.append(attachments_item)


        virinco_wats_schemas_wsjf_failure = cls(
            art_number=art_number,
            art_rev=art_rev,
            art_vendor=art_vendor,
            art_description=art_description,
            category=category,
            code=code,
            comment=comment,
            com_ref=com_ref,
            func_block=func_block,
            ref_step_id=ref_step_id,
            ref_step_name=ref_step_name,
            attachments=attachments,
        )


        virinco_wats_schemas_wsjf_failure.additional_properties = d
        return virinco_wats_schemas_wsjf_failure

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
