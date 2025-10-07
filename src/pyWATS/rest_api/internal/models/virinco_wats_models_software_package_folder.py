from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_models_software_package_folder_file import VirincoWATSModelsSoftwarePackageFolderFile





T = TypeVar("T", bound="VirincoWATSModelsSoftwarePackageFolder")



@_attrs_define
class VirincoWATSModelsSoftwarePackageFolder:
    """ 
        Attributes:
            name (Union[Unset, str]):
            modified (Union[Unset, datetime.datetime]):
            folders (Union[Unset, list['VirincoWATSModelsSoftwarePackageFolder']]):
            files (Union[Unset, list['VirincoWATSModelsSoftwarePackageFolderFile']]):
     """

    name: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    folders: Union[Unset, list['VirincoWATSModelsSoftwarePackageFolder']] = UNSET
    files: Union[Unset, list['VirincoWATSModelsSoftwarePackageFolderFile']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_models_software_package_folder_file import VirincoWATSModelsSoftwarePackageFolderFile
        name = self.name

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        folders: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.folders, Unset):
            folders = []
            for folders_item_data in self.folders:
                folders_item = folders_item_data.to_dict()
                folders.append(folders_item)



        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["Name"] = name
        if modified is not UNSET:
            field_dict["Modified"] = modified
        if folders is not UNSET:
            field_dict["folders"] = folders
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_models_software_package_folder_file import VirincoWATSModelsSoftwarePackageFolderFile
        d = dict(src_dict)
        name = d.pop("Name", UNSET)

        _modified = d.pop("Modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified,  Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)




        folders = []
        _folders = d.pop("folders", UNSET)
        for folders_item_data in (_folders or []):
            folders_item = VirincoWATSModelsSoftwarePackageFolder.from_dict(folders_item_data)



            folders.append(folders_item)


        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in (_files or []):
            files_item = VirincoWATSModelsSoftwarePackageFolderFile.from_dict(files_item_data)



            files.append(files_item)


        virinco_wats_models_software_package_folder = cls(
            name=name,
            modified=modified,
            folders=folders,
            files=files,
        )


        virinco_wats_models_software_package_folder.additional_properties = d
        return virinco_wats_models_software_package_folder

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
