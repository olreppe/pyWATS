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
  from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductProductRevisionRelation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductProductRevisionRelation:
    """ 
        Attributes:
            product_revision_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_product_revision_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            product_revision_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            quantity (Union[Unset, int]):
            revision_mask (Union[Unset, str]):
            parent_product_revision (Union[Unset, VirincoWATSWebDashboardModelsMesProductProductRevision]):
            child_product_revision (Union[Unset, VirincoWATSWebDashboardModelsMesProductProductRevision]):
     """

    product_revision_relation_id: Union[Unset, UUID] = UNSET
    parent_product_revision_id: Union[Unset, UUID] = UNSET
    product_revision_id: Union[Unset, UUID] = UNSET
    quantity: Union[Unset, int] = UNSET
    revision_mask: Union[Unset, str] = UNSET
    parent_product_revision: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductProductRevision'] = UNSET
    child_product_revision: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductProductRevision'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision
        product_revision_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_revision_relation_id, Unset):
            product_revision_relation_id = str(self.product_revision_relation_id)

        parent_product_revision_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_product_revision_id, Unset):
            parent_product_revision_id = str(self.parent_product_revision_id)

        product_revision_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_revision_id, Unset):
            product_revision_id = str(self.product_revision_id)

        quantity = self.quantity

        revision_mask = self.revision_mask

        parent_product_revision: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent_product_revision, Unset):
            parent_product_revision = self.parent_product_revision.to_dict()

        child_product_revision: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.child_product_revision, Unset):
            child_product_revision = self.child_product_revision.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if product_revision_relation_id is not UNSET:
            field_dict["ProductRevisionRelationId"] = product_revision_relation_id
        if parent_product_revision_id is not UNSET:
            field_dict["ParentProductRevisionId"] = parent_product_revision_id
        if product_revision_id is not UNSET:
            field_dict["ProductRevisionId"] = product_revision_id
        if quantity is not UNSET:
            field_dict["Quantity"] = quantity
        if revision_mask is not UNSET:
            field_dict["RevisionMask"] = revision_mask
        if parent_product_revision is not UNSET:
            field_dict["ParentProductRevision"] = parent_product_revision
        if child_product_revision is not UNSET:
            field_dict["ChildProductRevision"] = child_product_revision

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision
        d = dict(src_dict)
        _product_revision_relation_id = d.pop("ProductRevisionRelationId", UNSET)
        product_revision_relation_id: Union[Unset, UUID]
        if isinstance(_product_revision_relation_id,  Unset):
            product_revision_relation_id = UNSET
        else:
            product_revision_relation_id = UUID(_product_revision_relation_id)




        _parent_product_revision_id = d.pop("ParentProductRevisionId", UNSET)
        parent_product_revision_id: Union[Unset, UUID]
        if isinstance(_parent_product_revision_id,  Unset):
            parent_product_revision_id = UNSET
        else:
            parent_product_revision_id = UUID(_parent_product_revision_id)




        _product_revision_id = d.pop("ProductRevisionId", UNSET)
        product_revision_id: Union[Unset, UUID]
        if isinstance(_product_revision_id,  Unset):
            product_revision_id = UNSET
        else:
            product_revision_id = UUID(_product_revision_id)




        quantity = d.pop("Quantity", UNSET)

        revision_mask = d.pop("RevisionMask", UNSET)

        _parent_product_revision = d.pop("ParentProductRevision", UNSET)
        parent_product_revision: Union[Unset, VirincoWATSWebDashboardModelsMesProductProductRevision]
        if isinstance(_parent_product_revision,  Unset):
            parent_product_revision = UNSET
        else:
            parent_product_revision = VirincoWATSWebDashboardModelsMesProductProductRevision.from_dict(_parent_product_revision)




        _child_product_revision = d.pop("ChildProductRevision", UNSET)
        child_product_revision: Union[Unset, VirincoWATSWebDashboardModelsMesProductProductRevision]
        if isinstance(_child_product_revision,  Unset):
            child_product_revision = UNSET
        else:
            child_product_revision = VirincoWATSWebDashboardModelsMesProductProductRevision.from_dict(_child_product_revision)




        virinco_wats_web_dashboard_models_mes_product_product_revision_relation = cls(
            product_revision_relation_id=product_revision_relation_id,
            parent_product_revision_id=parent_product_revision_id,
            product_revision_id=product_revision_id,
            quantity=quantity,
            revision_mask=revision_mask,
            parent_product_revision=parent_product_revision,
            child_product_revision=child_product_revision,
        )


        virinco_wats_web_dashboard_models_mes_product_product_revision_relation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_product_revision_relation

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
