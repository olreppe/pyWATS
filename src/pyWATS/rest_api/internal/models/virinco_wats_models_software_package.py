from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_models_software_package_folder import VirincoWATSModelsSoftwarePackageFolder





T = TypeVar("T", bound="VirincoWATSModelsSoftwarePackage")



@_attrs_define
class VirincoWATSModelsSoftwarePackage:
    """ 
        Attributes:
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            package_folder (Union[Unset, bool]):
            version (Union[Unset, int]):
            description (Union[Unset, str]):
            root_directory (Union[Unset, str]):
            tags (Union[Unset, str]):
            modified (Union[Unset, datetime.datetime]):
            responsible (Union[Unset, str]):
            status (Union[Unset, int]):
            virtual_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            priority (Union[Unset, int]):
            rootfolder (Union[Unset, VirincoWATSModelsSoftwarePackageFolder]):
     """

    id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    package_folder: Union[Unset, bool] = UNSET
    version: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    root_directory: Union[Unset, str] = UNSET
    tags: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    responsible: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    virtual_folder_id: Union[Unset, UUID] = UNSET
    priority: Union[Unset, int] = UNSET
    rootfolder: Union[Unset, 'VirincoWATSModelsSoftwarePackageFolder'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_models_software_package_folder import VirincoWATSModelsSoftwarePackageFolder
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        name = self.name

        package_folder = self.package_folder

        version = self.version

        description = self.description

        root_directory = self.root_directory

        tags = self.tags

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        responsible = self.responsible

        status = self.status

        virtual_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.virtual_folder_id, Unset):
            virtual_folder_id = str(self.virtual_folder_id)

        priority = self.priority

        rootfolder: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rootfolder, Unset):
            rootfolder = self.rootfolder.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["Id"] = id
        if name is not UNSET:
            field_dict["Name"] = name
        if package_folder is not UNSET:
            field_dict["PackageFolder"] = package_folder
        if version is not UNSET:
            field_dict["Version"] = version
        if description is not UNSET:
            field_dict["Description"] = description
        if root_directory is not UNSET:
            field_dict["RootDirectory"] = root_directory
        if tags is not UNSET:
            field_dict["Tags"] = tags
        if modified is not UNSET:
            field_dict["Modified"] = modified
        if responsible is not UNSET:
            field_dict["Responsible"] = responsible
        if status is not UNSET:
            field_dict["Status"] = status
        if virtual_folder_id is not UNSET:
            field_dict["VirtualFolderId"] = virtual_folder_id
        if priority is not UNSET:
            field_dict["Priority"] = priority
        if rootfolder is not UNSET:
            field_dict["rootfolder"] = rootfolder

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_models_software_package_folder import VirincoWATSModelsSoftwarePackageFolder
        d = dict(src_dict)
        _id = d.pop("Id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        name = d.pop("Name", UNSET)

        package_folder = d.pop("PackageFolder", UNSET)

        version = d.pop("Version", UNSET)

        description = d.pop("Description", UNSET)

        root_directory = d.pop("RootDirectory", UNSET)

        tags = d.pop("Tags", UNSET)

        _modified = d.pop("Modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified,  Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)




        responsible = d.pop("Responsible", UNSET)

        status = d.pop("Status", UNSET)

        _virtual_folder_id = d.pop("VirtualFolderId", UNSET)
        virtual_folder_id: Union[Unset, UUID]
        if isinstance(_virtual_folder_id,  Unset):
            virtual_folder_id = UNSET
        else:
            virtual_folder_id = UUID(_virtual_folder_id)




        priority = d.pop("Priority", UNSET)

        _rootfolder = d.pop("rootfolder", UNSET)
        rootfolder: Union[Unset, VirincoWATSModelsSoftwarePackageFolder]
        if isinstance(_rootfolder,  Unset):
            rootfolder = UNSET
        else:
            rootfolder = VirincoWATSModelsSoftwarePackageFolder.from_dict(_rootfolder)




        virinco_wats_models_software_package = cls(
            id=id,
            name=name,
            package_folder=package_folder,
            version=version,
            description=description,
            root_directory=root_directory,
            tags=tags,
            modified=modified,
            responsible=responsible,
            status=status,
            virtual_folder_id=virtual_folder_id,
            priority=priority,
            rootfolder=rootfolder,
        )


        virinco_wats_models_software_package.additional_properties = d
        return virinco_wats_models_software_package

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
