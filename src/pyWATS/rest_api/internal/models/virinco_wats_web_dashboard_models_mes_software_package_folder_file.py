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
  from ..models.virinco_wats_web_dashboard_models_mes_software_repository_folder_file import VirincoWATSWebDashboardModelsMesSoftwareRepositoryFolderFile





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile")



@_attrs_define
class VirincoWATSWebDashboardModelsMesSoftwarePackageFolderFile:
    """ 
        Attributes:
            package_folder_file_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            package_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            repository_folder_file_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            attributes (Union[Unset, int]):
            repository_folder_file (Union[Unset, VirincoWATSWebDashboardModelsMesSoftwareRepositoryFolderFile]):
     """

    package_folder_file_id: Union[Unset, UUID] = UNSET
    package_folder_id: Union[Unset, UUID] = UNSET
    repository_folder_file_id: Union[Unset, UUID] = UNSET
    attributes: Union[Unset, int] = UNSET
    repository_folder_file: Union[Unset, 'VirincoWATSWebDashboardModelsMesSoftwareRepositoryFolderFile'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_software_repository_folder_file import VirincoWATSWebDashboardModelsMesSoftwareRepositoryFolderFile
        package_folder_file_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_folder_file_id, Unset):
            package_folder_file_id = str(self.package_folder_file_id)

        package_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_folder_id, Unset):
            package_folder_id = str(self.package_folder_id)

        repository_folder_file_id: Union[Unset, str] = UNSET
        if not isinstance(self.repository_folder_file_id, Unset):
            repository_folder_file_id = str(self.repository_folder_file_id)

        attributes = self.attributes

        repository_folder_file: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.repository_folder_file, Unset):
            repository_folder_file = self.repository_folder_file.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if package_folder_file_id is not UNSET:
            field_dict["PackageFolderFileId"] = package_folder_file_id
        if package_folder_id is not UNSET:
            field_dict["PackageFolderId"] = package_folder_id
        if repository_folder_file_id is not UNSET:
            field_dict["RepositoryFolderFileId"] = repository_folder_file_id
        if attributes is not UNSET:
            field_dict["Attributes"] = attributes
        if repository_folder_file is not UNSET:
            field_dict["RepositoryFolderFile"] = repository_folder_file

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_software_repository_folder_file import VirincoWATSWebDashboardModelsMesSoftwareRepositoryFolderFile
        d = dict(src_dict)
        _package_folder_file_id = d.pop("PackageFolderFileId", UNSET)
        package_folder_file_id: Union[Unset, UUID]
        if isinstance(_package_folder_file_id,  Unset):
            package_folder_file_id = UNSET
        else:
            package_folder_file_id = UUID(_package_folder_file_id)




        _package_folder_id = d.pop("PackageFolderId", UNSET)
        package_folder_id: Union[Unset, UUID]
        if isinstance(_package_folder_id,  Unset):
            package_folder_id = UNSET
        else:
            package_folder_id = UUID(_package_folder_id)




        _repository_folder_file_id = d.pop("RepositoryFolderFileId", UNSET)
        repository_folder_file_id: Union[Unset, UUID]
        if isinstance(_repository_folder_file_id,  Unset):
            repository_folder_file_id = UNSET
        else:
            repository_folder_file_id = UUID(_repository_folder_file_id)




        attributes = d.pop("Attributes", UNSET)

        _repository_folder_file = d.pop("RepositoryFolderFile", UNSET)
        repository_folder_file: Union[Unset, VirincoWATSWebDashboardModelsMesSoftwareRepositoryFolderFile]
        if isinstance(_repository_folder_file,  Unset):
            repository_folder_file = UNSET
        else:
            repository_folder_file = VirincoWATSWebDashboardModelsMesSoftwareRepositoryFolderFile.from_dict(_repository_folder_file)




        virinco_wats_web_dashboard_models_mes_software_package_folder_file = cls(
            package_folder_file_id=package_folder_file_id,
            package_folder_id=package_folder_id,
            repository_folder_file_id=repository_folder_file_id,
            attributes=attributes,
            repository_folder_file=repository_folder_file,
        )


        virinco_wats_web_dashboard_models_mes_software_package_folder_file.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_software_package_folder_file

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
