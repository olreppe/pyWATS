from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmBarcodeIdentifier")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmBarcodeIdentifier:
    """ 
        Attributes:
            id (Union[Unset, int]):
            pattern (Union[Unset, str]):
            serial_number (Union[Unset, str]): The RegEx pattern find the serial number.
            part_number (Union[Unset, str]): The RegEx pattern find the part number.
            revision (Union[Unset, str]): The RegEx pattern find the revision.
            batch_number (Union[Unset, str]): The RegEx pattern find the batch number.
            process (Union[Unset, str]): The RegEx pattern find the process code.
            order (Union[Unset, int]): The order the identifiers are checked. An identifier with Order = 1 is checked before
                an identifier with Order = 2.
            description (Union[Unset, str]): Text description of the identifier, typically an example of what the barcode
                looks like.
     """

    id: Union[Unset, int] = UNSET
    pattern: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    batch_number: Union[Unset, str] = UNSET
    process: Union[Unset, str] = UNSET
    order: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        pattern = self.pattern

        serial_number = self.serial_number

        part_number = self.part_number

        revision = self.revision

        batch_number = self.batch_number

        process = self.process

        order = self.order

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if pattern is not UNSET:
            field_dict["pattern"] = pattern
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if batch_number is not UNSET:
            field_dict["batchNumber"] = batch_number
        if process is not UNSET:
            field_dict["process"] = process
        if order is not UNSET:
            field_dict["order"] = order
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        pattern = d.pop("pattern", UNSET)

        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        batch_number = d.pop("batchNumber", UNSET)

        process = d.pop("process", UNSET)

        order = d.pop("order", UNSET)

        description = d.pop("description", UNSET)

        virinco_wats_web_dashboard_models_tdm_barcode_identifier = cls(
            id=id,
            pattern=pattern,
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            batch_number=batch_number,
            process=process,
            order=order,
            description=description,
        )


        virinco_wats_web_dashboard_models_tdm_barcode_identifier.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_barcode_identifier

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
