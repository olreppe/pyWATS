from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsODataAttachment")



@_attrs_define
class VirincoWATSWebDashboardModelsODataAttachment:
    """ 
        Attributes:
            step_id (Union[Unset, int]): Id of step the attachment belongs to. Use in get attachment rest API to get
                attachment data.
            filename (Union[Unset, str]): Attachment filename
     """

    step_id: Union[Unset, int] = UNSET
    filename: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        step_id = self.step_id

        filename = self.filename


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if step_id is not UNSET:
            field_dict["stepId"] = step_id
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        step_id = d.pop("stepId", UNSET)

        filename = d.pop("filename", UNSET)

        virinco_wats_web_dashboard_models_o_data_attachment = cls(
            step_id=step_id,
            filename=filename,
        )


        virinco_wats_web_dashboard_models_o_data_attachment.additional_properties = d
        return virinco_wats_web_dashboard_models_o_data_attachment

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
