from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSInterfaceModelsFailcode")



@_attrs_define
class VirincoWATSInterfaceModelsFailcode:
    """ 
        Attributes:
            guid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            selectable (Union[Unset, bool]):
            description (Union[Unset, str]):
            sort_order (Union[Unset, int]):
            failure_type (Union[Unset, int]):
            image_constraint (Union[Unset, str]):
            status (Union[Unset, int]):
            failcodes (Union[Unset, list['VirincoWATSInterfaceModelsFailcode']]):
     """

    guid: Union[Unset, UUID] = UNSET
    selectable: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    sort_order: Union[Unset, int] = UNSET
    failure_type: Union[Unset, int] = UNSET
    image_constraint: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    failcodes: Union[Unset, list['VirincoWATSInterfaceModelsFailcode']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        guid: Union[Unset, str] = UNSET
        if not isinstance(self.guid, Unset):
            guid = str(self.guid)

        selectable = self.selectable

        description = self.description

        sort_order = self.sort_order

        failure_type = self.failure_type

        image_constraint = self.image_constraint

        status = self.status

        failcodes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.failcodes, Unset):
            failcodes = []
            for failcodes_item_data in self.failcodes:
                failcodes_item = failcodes_item_data.to_dict()
                failcodes.append(failcodes_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if guid is not UNSET:
            field_dict["GUID"] = guid
        if selectable is not UNSET:
            field_dict["Selectable"] = selectable
        if description is not UNSET:
            field_dict["Description"] = description
        if sort_order is not UNSET:
            field_dict["SortOrder"] = sort_order
        if failure_type is not UNSET:
            field_dict["FailureType"] = failure_type
        if image_constraint is not UNSET:
            field_dict["ImageConstraint"] = image_constraint
        if status is not UNSET:
            field_dict["Status"] = status
        if failcodes is not UNSET:
            field_dict["Failcodes"] = failcodes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _guid = d.pop("GUID", UNSET)
        guid: Union[Unset, UUID]
        if isinstance(_guid,  Unset):
            guid = UNSET
        else:
            guid = UUID(_guid)




        selectable = d.pop("Selectable", UNSET)

        description = d.pop("Description", UNSET)

        sort_order = d.pop("SortOrder", UNSET)

        failure_type = d.pop("FailureType", UNSET)

        image_constraint = d.pop("ImageConstraint", UNSET)

        status = d.pop("Status", UNSET)

        failcodes = []
        _failcodes = d.pop("Failcodes", UNSET)
        for failcodes_item_data in (_failcodes or []):
            failcodes_item = VirincoWATSInterfaceModelsFailcode.from_dict(failcodes_item_data)



            failcodes.append(failcodes_item)


        virinco_wats_interface_models_failcode = cls(
            guid=guid,
            selectable=selectable,
            description=description,
            sort_order=sort_order,
            failure_type=failure_type,
            image_constraint=image_constraint,
            status=status,
            failcodes=failcodes,
        )


        virinco_wats_interface_models_failcode.additional_properties = d
        return virinco_wats_interface_models_failcode

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
