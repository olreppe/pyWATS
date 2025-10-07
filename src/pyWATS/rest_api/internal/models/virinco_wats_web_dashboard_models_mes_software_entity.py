from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_mes_software_entity_type import VirincoWATSWebDashboardModelsMesSoftwareEntityType
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesSoftwareEntity")



@_attrs_define
class VirincoWATSWebDashboardModelsMesSoftwareEntity:
    """ Model which represents either a software file or folder.

        Attributes:
            id (Union[Unset, UUID]): The index of this entity within the package Example:
                00000000-0000-0000-0000-000000000000.
            type_ (Union[Unset, VirincoWATSWebDashboardModelsMesSoftwareEntityType]):
            parent_id (Union[Unset, UUID]): The id of the parent folder if type is folder. Note this is not used for files.
                {!:PackageFolderId} Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]): The display name of the file or folder
            file_version (Union[Unset, str]): The display name of the file or folder
            repository_version (Union[Unset, int]): The display name of the file or folder
            file_size (Union[Unset, int]): The display name of the file or folder
            last_modified_date (Union[Unset, datetime.datetime]): The date / time when this folder or file was last modified
            uploaded_date (Union[Unset, datetime.datetime]): The date / time when this file was uploaded. Not in use when
                type is folder.
            attributes (Union[Unset, int]): The date / time when this file was uploaded. Not in use when type is folder.
            repository_folder_file_id (Union[Unset, UUID]): used for downloading file Example:
                00000000-0000-0000-0000-000000000000.
            valid (Union[Unset, bool]): checks if the uploaded file is valid.
            information (Union[Unset, str]): Entity information
     """

    id: Union[Unset, UUID] = UNSET
    type_: Union[Unset, VirincoWATSWebDashboardModelsMesSoftwareEntityType] = UNSET
    parent_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    file_version: Union[Unset, str] = UNSET
    repository_version: Union[Unset, int] = UNSET
    file_size: Union[Unset, int] = UNSET
    last_modified_date: Union[Unset, datetime.datetime] = UNSET
    uploaded_date: Union[Unset, datetime.datetime] = UNSET
    attributes: Union[Unset, int] = UNSET
    repository_folder_file_id: Union[Unset, UUID] = UNSET
    valid: Union[Unset, bool] = UNSET
    information: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        type_: Union[Unset, int] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        parent_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_id, Unset):
            parent_id = str(self.parent_id)

        name = self.name

        file_version = self.file_version

        repository_version = self.repository_version

        file_size = self.file_size

        last_modified_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_modified_date, Unset):
            last_modified_date = self.last_modified_date.isoformat()

        uploaded_date: Union[Unset, str] = UNSET
        if not isinstance(self.uploaded_date, Unset):
            uploaded_date = self.uploaded_date.isoformat()

        attributes = self.attributes

        repository_folder_file_id: Union[Unset, str] = UNSET
        if not isinstance(self.repository_folder_file_id, Unset):
            repository_folder_file_id = str(self.repository_folder_file_id)

        valid = self.valid

        information = self.information


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if name is not UNSET:
            field_dict["name"] = name
        if file_version is not UNSET:
            field_dict["fileVersion"] = file_version
        if repository_version is not UNSET:
            field_dict["repositoryVersion"] = repository_version
        if file_size is not UNSET:
            field_dict["fileSize"] = file_size
        if last_modified_date is not UNSET:
            field_dict["lastModifiedDate"] = last_modified_date
        if uploaded_date is not UNSET:
            field_dict["uploadedDate"] = uploaded_date
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if repository_folder_file_id is not UNSET:
            field_dict["repositoryFolderFileId"] = repository_folder_file_id
        if valid is not UNSET:
            field_dict["valid"] = valid
        if information is not UNSET:
            field_dict["information"] = information

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




        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, VirincoWATSWebDashboardModelsMesSoftwareEntityType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = VirincoWATSWebDashboardModelsMesSoftwareEntityType(_type_)




        _parent_id = d.pop("parentId", UNSET)
        parent_id: Union[Unset, UUID]
        if isinstance(_parent_id,  Unset):
            parent_id = UNSET
        else:
            parent_id = UUID(_parent_id)




        name = d.pop("name", UNSET)

        file_version = d.pop("fileVersion", UNSET)

        repository_version = d.pop("repositoryVersion", UNSET)

        file_size = d.pop("fileSize", UNSET)

        _last_modified_date = d.pop("lastModifiedDate", UNSET)
        last_modified_date: Union[Unset, datetime.datetime]
        if isinstance(_last_modified_date,  Unset):
            last_modified_date = UNSET
        else:
            last_modified_date = isoparse(_last_modified_date)




        _uploaded_date = d.pop("uploadedDate", UNSET)
        uploaded_date: Union[Unset, datetime.datetime]
        if isinstance(_uploaded_date,  Unset):
            uploaded_date = UNSET
        else:
            uploaded_date = isoparse(_uploaded_date)




        attributes = d.pop("attributes", UNSET)

        _repository_folder_file_id = d.pop("repositoryFolderFileId", UNSET)
        repository_folder_file_id: Union[Unset, UUID]
        if isinstance(_repository_folder_file_id,  Unset):
            repository_folder_file_id = UNSET
        else:
            repository_folder_file_id = UUID(_repository_folder_file_id)




        valid = d.pop("valid", UNSET)

        information = d.pop("information", UNSET)

        virinco_wats_web_dashboard_models_mes_software_entity = cls(
            id=id,
            type_=type_,
            parent_id=parent_id,
            name=name,
            file_version=file_version,
            repository_version=repository_version,
            file_size=file_size,
            last_modified_date=last_modified_date,
            uploaded_date=uploaded_date,
            attributes=attributes,
            repository_folder_file_id=repository_folder_file_id,
            valid=valid,
            information=information,
        )


        virinco_wats_web_dashboard_models_mes_software_entity.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_software_entity

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
