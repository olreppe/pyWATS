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
  from ..models.virinco_wats_web_dashboard_models_mes_software_package_folder_file import VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesSoftwarePackageFolder")



@_attrs_define
class VirincoWATSWebDashboardModelsMesSoftwarePackageFolder:
    """ 
        Attributes:
            package_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            package_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            modified (Union[Unset, datetime.datetime]):
            parent (Union[Unset, VirincoWATSWebDashboardModelsMesSoftwarePackageFolder]):
            package_folders (Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwarePackageFolder']]):
            package_folder_files (Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile']]):
     """

    package_folder_id: Union[Unset, UUID] = UNSET
    package_id: Union[Unset, UUID] = UNSET
    parent_folder_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    parent: Union[Unset, 'VirincoWATSWebDashboardModelsMesSoftwarePackageFolder'] = UNSET
    package_folders: Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwarePackageFolder']] = UNSET
    package_folder_files: Union[Unset, list['VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_software_package_folder_file import VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile
        package_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_folder_id, Unset):
            package_folder_id = str(self.package_folder_id)

        package_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_id, Unset):
            package_id = str(self.package_id)

        parent_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_folder_id, Unset):
            parent_folder_id = str(self.parent_folder_id)

        name = self.name

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        parent: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent, Unset):
            parent = self.parent.to_dict()

        package_folders: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.package_folders, Unset):
            package_folders = []
            for package_folders_item_data in self.package_folders:
                package_folders_item = package_folders_item_data.to_dict()
                package_folders.append(package_folders_item)



        package_folder_files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.package_folder_files, Unset):
            package_folder_files = []
            for package_folder_files_item_data in self.package_folder_files:
                package_folder_files_item = package_folder_files_item_data.to_dict()
                package_folder_files.append(package_folder_files_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if package_folder_id is not UNSET:
            field_dict["PackageFolderId"] = package_folder_id
        if package_id is not UNSET:
            field_dict["PackageId"] = package_id
        if parent_folder_id is not UNSET:
            field_dict["ParentFolderId"] = parent_folder_id
        if name is not UNSET:
            field_dict["Name"] = name
        if modified is not UNSET:
            field_dict["Modified"] = modified
        if parent is not UNSET:
            field_dict["Parent"] = parent
        if package_folders is not UNSET:
            field_dict["PackageFolders"] = package_folders
        if package_folder_files is not UNSET:
            field_dict["PackageFolderFiles"] = package_folder_files

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_software_package_folder_file import VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile
        d = dict(src_dict)
        _package_folder_id = d.pop("PackageFolderId", UNSET)
        package_folder_id: Union[Unset, UUID]
        if isinstance(_package_folder_id,  Unset):
            package_folder_id = UNSET
        else:
            package_folder_id = UUID(_package_folder_id)




        _package_id = d.pop("PackageId", UNSET)
        package_id: Union[Unset, UUID]
        if isinstance(_package_id,  Unset):
            package_id = UNSET
        else:
            package_id = UUID(_package_id)




        _parent_folder_id = d.pop("ParentFolderId", UNSET)
        parent_folder_id: Union[Unset, UUID]
        if isinstance(_parent_folder_id,  Unset):
            parent_folder_id = UNSET
        else:
            parent_folder_id = UUID(_parent_folder_id)




        name = d.pop("Name", UNSET)

        _modified = d.pop("Modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified,  Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)




        _parent = d.pop("Parent", UNSET)
        parent: Union[Unset, VirincoWATSWebDashboardModelsMesSoftwarePackageFolder]
        if isinstance(_parent,  Unset):
            parent = UNSET
        else:
            parent = VirincoWATSWebDashboardModelsMesSoftwarePackageFolder.from_dict(_parent)




        package_folders = []
        _package_folders = d.pop("PackageFolders", UNSET)
        for package_folders_item_data in (_package_folders or []):
            package_folders_item = VirincoWATSWebDashboardModelsMesSoftwarePackageFolder.from_dict(package_folders_item_data)



            package_folders.append(package_folders_item)


        package_folder_files = []
        _package_folder_files = d.pop("PackageFolderFiles", UNSET)
        for package_folder_files_item_data in (_package_folder_files or []):
            package_folder_files_item = VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile.from_dict(package_folder_files_item_data)



            package_folder_files.append(package_folder_files_item)


        virinco_wats_web_dashboard_models_mes_software_package_folder = cls(
            package_folder_id=package_folder_id,
            package_id=package_id,
            parent_folder_id=parent_folder_id,
            name=name,
            modified=modified,
            parent=parent,
            package_folders=package_folders,
            package_folder_files=package_folder_files,
        )


        virinco_wats_web_dashboard_models_mes_software_package_folder.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_software_package_folder

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
