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






T = TypeVar("T", bound="VirincoWATSModelsSoftwarePackageFolderFile")



@_attrs_define
class VirincoWATSModelsSoftwarePackageFolderFile:
    """ 
        Attributes:
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            attributes (Union[Unset, int]):
            name (Union[Unset, str]):
            version (Union[Unset, int]):
            description (Union[Unset, str]):
            valid (Union[Unset, bool]):
            uploaded (Union[Unset, datetime.datetime]):
            file_modified_date (Union[Unset, datetime.datetime]):
            checksum (Union[Unset, str]):
            file_version (Union[Unset, str]):
            file_size (Union[Unset, int]):
     """

    id: Union[Unset, UUID] = UNSET
    attributes: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    valid: Union[Unset, bool] = UNSET
    uploaded: Union[Unset, datetime.datetime] = UNSET
    file_modified_date: Union[Unset, datetime.datetime] = UNSET
    checksum: Union[Unset, str] = UNSET
    file_version: Union[Unset, str] = UNSET
    file_size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        attributes = self.attributes

        name = self.name

        version = self.version

        description = self.description

        valid = self.valid

        uploaded: Union[Unset, str] = UNSET
        if not isinstance(self.uploaded, Unset):
            uploaded = self.uploaded.isoformat()

        file_modified_date: Union[Unset, str] = UNSET
        if not isinstance(self.file_modified_date, Unset):
            file_modified_date = self.file_modified_date.isoformat()

        checksum = self.checksum

        file_version = self.file_version

        file_size = self.file_size


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["Id"] = id
        if attributes is not UNSET:
            field_dict["Attributes"] = attributes
        if name is not UNSET:
            field_dict["Name"] = name
        if version is not UNSET:
            field_dict["Version"] = version
        if description is not UNSET:
            field_dict["Description"] = description
        if valid is not UNSET:
            field_dict["Valid"] = valid
        if uploaded is not UNSET:
            field_dict["Uploaded"] = uploaded
        if file_modified_date is not UNSET:
            field_dict["FileModifiedDate"] = file_modified_date
        if checksum is not UNSET:
            field_dict["Checksum"] = checksum
        if file_version is not UNSET:
            field_dict["FileVersion"] = file_version
        if file_size is not UNSET:
            field_dict["FileSize"] = file_size

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("Id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        attributes = d.pop("Attributes", UNSET)

        name = d.pop("Name", UNSET)

        version = d.pop("Version", UNSET)

        description = d.pop("Description", UNSET)

        valid = d.pop("Valid", UNSET)

        _uploaded = d.pop("Uploaded", UNSET)
        uploaded: Union[Unset, datetime.datetime]
        if isinstance(_uploaded,  Unset):
            uploaded = UNSET
        else:
            uploaded = isoparse(_uploaded)




        _file_modified_date = d.pop("FileModifiedDate", UNSET)
        file_modified_date: Union[Unset, datetime.datetime]
        if isinstance(_file_modified_date,  Unset):
            file_modified_date = UNSET
        else:
            file_modified_date = isoparse(_file_modified_date)




        checksum = d.pop("Checksum", UNSET)

        file_version = d.pop("FileVersion", UNSET)

        file_size = d.pop("FileSize", UNSET)

        virinco_wats_models_software_package_folder_file = cls(
            id=id,
            attributes=attributes,
            name=name,
            version=version,
            description=description,
            valid=valid,
            uploaded=uploaded,
            file_modified_date=file_modified_date,
            checksum=checksum,
            file_version=file_version,
            file_size=file_size,
        )


        virinco_wats_models_software_package_folder_file.additional_properties = d
        return virinco_wats_models_software_package_folder_file

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
