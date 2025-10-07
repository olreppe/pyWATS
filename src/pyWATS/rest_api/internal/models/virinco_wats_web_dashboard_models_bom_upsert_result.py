from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_bom_upsert_result_status import VirincoWATSWebDashboardModelsBomUpsertResultStatus
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsBomUpsertResult")



@_attrs_define
class VirincoWATSWebDashboardModelsBomUpsertResult:
    """ 
        Attributes:
            pn (Union[Unset, str]):
            rev (Union[Unset, str]):
            message (Union[Unset, str]):
            revision_letter (Union[Unset, str]):
            status (Union[Unset, VirincoWATSWebDashboardModelsBomUpsertResultStatus]):
     """

    pn: Union[Unset, str] = UNSET
    rev: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    revision_letter: Union[Unset, str] = UNSET
    status: Union[Unset, VirincoWATSWebDashboardModelsBomUpsertResultStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        pn = self.pn

        rev = self.rev

        message = self.message

        revision_letter = self.revision_letter

        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if pn is not UNSET:
            field_dict["PN"] = pn
        if rev is not UNSET:
            field_dict["Rev"] = rev
        if message is not UNSET:
            field_dict["Message"] = message
        if revision_letter is not UNSET:
            field_dict["RevisionLetter"] = revision_letter
        if status is not UNSET:
            field_dict["Status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pn = d.pop("PN", UNSET)

        rev = d.pop("Rev", UNSET)

        message = d.pop("Message", UNSET)

        revision_letter = d.pop("RevisionLetter", UNSET)

        _status = d.pop("Status", UNSET)
        status: Union[Unset, VirincoWATSWebDashboardModelsBomUpsertResultStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = VirincoWATSWebDashboardModelsBomUpsertResultStatus(_status)




        virinco_wats_web_dashboard_models_bom_upsert_result = cls(
            pn=pn,
            rev=rev,
            message=message,
            revision_letter=revision_letter,
            status=status,
        )


        virinco_wats_web_dashboard_models_bom_upsert_result.additional_properties = d
        return virinco_wats_web_dashboard_models_bom_upsert_result

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
