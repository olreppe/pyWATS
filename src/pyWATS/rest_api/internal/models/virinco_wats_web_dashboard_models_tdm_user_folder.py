from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_user_folder_module import VirincoWATSWebDashboardModelsTdmUserFolderModule
from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmUserFolder")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmUserFolder:
    """ Represents a user defined folder.

        Attributes:
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            user_id (Union[Unset, str]):
            module (Union[Unset, VirincoWATSWebDashboardModelsTdmUserFolderModule]):
            name (Union[Unset, str]):
            parent_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
     """

    id: Union[Unset, UUID] = UNSET
    user_id: Union[Unset, str] = UNSET
    module: Union[Unset, VirincoWATSWebDashboardModelsTdmUserFolderModule] = UNSET
    name: Union[Unset, str] = UNSET
    parent_folder_id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        user_id = self.user_id

        module: Union[Unset, int] = UNSET
        if not isinstance(self.module, Unset):
            module = self.module.value


        name = self.name

        parent_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_folder_id, Unset):
            parent_folder_id = str(self.parent_folder_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if module is not UNSET:
            field_dict["module"] = module
        if name is not UNSET:
            field_dict["name"] = name
        if parent_folder_id is not UNSET:
            field_dict["parentFolderId"] = parent_folder_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        user_id = d.pop("userId", UNSET)

        _module = d.pop("module", UNSET)
        module: Union[Unset, VirincoWATSWebDashboardModelsTdmUserFolderModule]
        if isinstance(_module,  Unset):
            module = UNSET
        else:
            module = VirincoWATSWebDashboardModelsTdmUserFolderModule(_module)




        name = d.pop("name", UNSET)

        _parent_folder_id = d.pop("parentFolderId", UNSET)
        parent_folder_id: Union[Unset, UUID]
        if isinstance(_parent_folder_id,  Unset):
            parent_folder_id = UNSET
        else:
            parent_folder_id = UUID(_parent_folder_id)




        virinco_wats_web_dashboard_models_tdm_user_folder = cls(
            id=id,
            user_id=user_id,
            module=module,
            name=name,
            parent_folder_id=parent_folder_id,
        )


        virinco_wats_web_dashboard_models_tdm_user_folder.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_user_folder

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
