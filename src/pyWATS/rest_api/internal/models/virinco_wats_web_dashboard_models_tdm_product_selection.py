from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_product_selection_details import VirincoWATSWebDashboardModelsTdmProductSelectionDetails





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmProductSelection")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmProductSelection:
    """ 
        Attributes:
            id (Union[Unset, int]):
            name (Union[Unset, str]):
            owner (Union[Unset, str]):
            description (Union[Unset, str]):
            type_ (Union[Unset, int]):
            sync_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            details (Union[Unset, list['VirincoWATSWebDashboardModelsTdmProductSelectionDetails']]):
     """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, int] = UNSET
    sync_id: Union[Unset, UUID] = UNSET
    details: Union[Unset, list['VirincoWATSWebDashboardModelsTdmProductSelectionDetails']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_product_selection_details import VirincoWATSWebDashboardModelsTdmProductSelectionDetails
        id = self.id

        name = self.name

        owner = self.owner

        description = self.description

        type_ = self.type_

        sync_id: Union[Unset, str] = UNSET
        if not isinstance(self.sync_id, Unset):
            sync_id = str(self.sync_id)

        details: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.details, Unset):
            details = []
            for details_item_data in self.details:
                details_item = details_item_data.to_dict()
                details.append(details_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if sync_id is not UNSET:
            field_dict["syncId"] = sync_id
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_product_selection_details import VirincoWATSWebDashboardModelsTdmProductSelectionDetails
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        owner = d.pop("owner", UNSET)

        description = d.pop("description", UNSET)

        type_ = d.pop("type", UNSET)

        _sync_id = d.pop("syncId", UNSET)
        sync_id: Union[Unset, UUID]
        if isinstance(_sync_id,  Unset):
            sync_id = UNSET
        else:
            sync_id = UUID(_sync_id)




        details = []
        _details = d.pop("details", UNSET)
        for details_item_data in (_details or []):
            details_item = VirincoWATSWebDashboardModelsTdmProductSelectionDetails.from_dict(details_item_data)



            details.append(details_item)


        virinco_wats_web_dashboard_models_tdm_product_selection = cls(
            id=id,
            name=name,
            owner=owner,
            description=description,
            type_=type_,
            sync_id=sync_id,
            details=details,
        )


        virinco_wats_web_dashboard_models_tdm_product_selection.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_product_selection

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
