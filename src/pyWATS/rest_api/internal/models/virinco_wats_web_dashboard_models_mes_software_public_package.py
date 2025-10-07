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
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesSoftwarePublicPackage")



@_attrs_define
class VirincoWATSWebDashboardModelsMesSoftwarePublicPackage:
    """ 
        Attributes:
            package_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            install_on_root (Union[Unset, bool]):
            version (Union[Unset, int]):
            description (Union[Unset, str]):
            root_directory (Union[Unset, str]):
            tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]):
            modified (Union[Unset, datetime.datetime]):
            modified_by (Union[Unset, str]):
            status (Union[Unset, str]):
            priority (Union[Unset, int]):
            virtual_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            created (Union[Unset, datetime.datetime]):
            created_by (Union[Unset, str]):
            released (Union[Unset, datetime.datetime]):
            released_by (Union[Unset, str]):
            revoked (Union[Unset, datetime.datetime]):
            revoked_by (Union[Unset, str]):
     """

    package_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    install_on_root: Union[Unset, bool] = UNSET
    version: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    root_directory: Union[Unset, str] = UNSET
    tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    modified_by: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    priority: Union[Unset, int] = UNSET
    virtual_folder_id: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    created_by: Union[Unset, str] = UNSET
    released: Union[Unset, datetime.datetime] = UNSET
    released_by: Union[Unset, str] = UNSET
    revoked: Union[Unset, datetime.datetime] = UNSET
    revoked_by: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        package_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_id, Unset):
            package_id = str(self.package_id)

        name = self.name

        install_on_root = self.install_on_root

        version = self.version

        description = self.description

        root_directory = self.root_directory

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)



        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        modified_by = self.modified_by

        status = self.status

        priority = self.priority

        virtual_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.virtual_folder_id, Unset):
            virtual_folder_id = str(self.virtual_folder_id)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        created_by = self.created_by

        released: Union[Unset, str] = UNSET
        if not isinstance(self.released, Unset):
            released = self.released.isoformat()

        released_by = self.released_by

        revoked: Union[Unset, str] = UNSET
        if not isinstance(self.revoked, Unset):
            revoked = self.revoked.isoformat()

        revoked_by = self.revoked_by


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if package_id is not UNSET:
            field_dict["packageId"] = package_id
        if name is not UNSET:
            field_dict["name"] = name
        if install_on_root is not UNSET:
            field_dict["installOnRoot"] = install_on_root
        if version is not UNSET:
            field_dict["version"] = version
        if description is not UNSET:
            field_dict["description"] = description
        if root_directory is not UNSET:
            field_dict["rootDirectory"] = root_directory
        if tags is not UNSET:
            field_dict["tags"] = tags
        if modified is not UNSET:
            field_dict["modified"] = modified
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if virtual_folder_id is not UNSET:
            field_dict["virtualFolderId"] = virtual_folder_id
        if created is not UNSET:
            field_dict["created"] = created
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if released is not UNSET:
            field_dict["released"] = released
        if released_by is not UNSET:
            field_dict["releasedBy"] = released_by
        if revoked is not UNSET:
            field_dict["revoked"] = revoked
        if revoked_by is not UNSET:
            field_dict["revokedBy"] = revoked_by

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        d = dict(src_dict)
        _package_id = d.pop("packageId", UNSET)
        package_id: Union[Unset, UUID]
        if isinstance(_package_id,  Unset):
            package_id = UNSET
        else:
            package_id = UUID(_package_id)




        name = d.pop("name", UNSET)

        install_on_root = d.pop("installOnRoot", UNSET)

        version = d.pop("version", UNSET)

        description = d.pop("description", UNSET)

        root_directory = d.pop("rootDirectory", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in (_tags or []):
            tags_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(tags_item_data)



            tags.append(tags_item)


        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified,  Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)




        modified_by = d.pop("modifiedBy", UNSET)

        status = d.pop("status", UNSET)

        priority = d.pop("priority", UNSET)

        _virtual_folder_id = d.pop("virtualFolderId", UNSET)
        virtual_folder_id: Union[Unset, UUID]
        if isinstance(_virtual_folder_id,  Unset):
            virtual_folder_id = UNSET
        else:
            virtual_folder_id = UUID(_virtual_folder_id)




        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created,  Unset):
            created = UNSET
        else:
            created = isoparse(_created)




        created_by = d.pop("createdBy", UNSET)

        _released = d.pop("released", UNSET)
        released: Union[Unset, datetime.datetime]
        if isinstance(_released,  Unset):
            released = UNSET
        else:
            released = isoparse(_released)




        released_by = d.pop("releasedBy", UNSET)

        _revoked = d.pop("revoked", UNSET)
        revoked: Union[Unset, datetime.datetime]
        if isinstance(_revoked,  Unset):
            revoked = UNSET
        else:
            revoked = isoparse(_revoked)




        revoked_by = d.pop("revokedBy", UNSET)

        virinco_wats_web_dashboard_models_mes_software_public_package = cls(
            package_id=package_id,
            name=name,
            install_on_root=install_on_root,
            version=version,
            description=description,
            root_directory=root_directory,
            tags=tags,
            modified=modified,
            modified_by=modified_by,
            status=status,
            priority=priority,
            virtual_folder_id=virtual_folder_id,
            created=created,
            created_by=created_by,
            released=released,
            released_by=released_by,
            revoked=revoked,
            revoked_by=revoked_by,
        )


        virinco_wats_web_dashboard_models_mes_software_public_package.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_software_public_package

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
