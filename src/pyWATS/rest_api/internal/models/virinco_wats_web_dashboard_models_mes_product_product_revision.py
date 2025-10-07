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
  from ..models.virinco_wats_web_dashboard_models_mes_production_unit import VirincoWATSWebDashboardModelsMesProductionUnit
  from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision_relation import VirincoWATSWebDashboardModelsMesProductProductRevisionRelation
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
  from ..models.virinco_wats_schemas_wsbfbom_component import VirincoWATSSchemasWSBFBOMComponent
  from ..models.virinco_wats_web_dashboard_models_mes_product_product import VirincoWATSWebDashboardModelsMesProductProduct





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductProductRevision")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductProductRevision:
    """ 
        Attributes:
            product_revision_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            product_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            revision (Union[Unset, str]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            state (Union[Unset, int]):
            product (Union[Unset, VirincoWATSWebDashboardModelsMesProductProduct]):
            child_product_revision_relations (Union[Unset,
                list['VirincoWATSWebDashboardModelsMesProductProductRevisionRelation']]):
            parent_product_revision_relation (Union[Unset,
                list['VirincoWATSWebDashboardModelsMesProductProductRevisionRelation']]):
            units (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionUnit']]):
            bom (Union[Unset, list['VirincoWATSSchemasWSBFBOMComponent']]):
            settings (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]):
     """

    product_revision_id: Union[Unset, UUID] = UNSET
    product_id: Union[Unset, UUID] = UNSET
    revision: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    state: Union[Unset, int] = UNSET
    product: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductProduct'] = UNSET
    child_product_revision_relations: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductProductRevisionRelation']] = UNSET
    parent_product_revision_relation: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductProductRevisionRelation']] = UNSET
    units: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionUnit']] = UNSET
    bom: Union[Unset, list['VirincoWATSSchemasWSBFBOMComponent']] = UNSET
    settings: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_production_unit import VirincoWATSWebDashboardModelsMesProductionUnit
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision_relation import VirincoWATSWebDashboardModelsMesProductProductRevisionRelation
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_schemas_wsbfbom_component import VirincoWATSSchemasWSBFBOMComponent
        from ..models.virinco_wats_web_dashboard_models_mes_product_product import VirincoWATSWebDashboardModelsMesProductProduct
        product_revision_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_revision_id, Unset):
            product_revision_id = str(self.product_revision_id)

        product_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_id, Unset):
            product_id = str(self.product_id)

        revision = self.revision

        name = self.name

        description = self.description

        state = self.state

        product: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.product, Unset):
            product = self.product.to_dict()

        child_product_revision_relations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.child_product_revision_relations, Unset):
            child_product_revision_relations = []
            for child_product_revision_relations_item_data in self.child_product_revision_relations:
                child_product_revision_relations_item = child_product_revision_relations_item_data.to_dict()
                child_product_revision_relations.append(child_product_revision_relations_item)



        parent_product_revision_relation: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parent_product_revision_relation, Unset):
            parent_product_revision_relation = []
            for parent_product_revision_relation_item_data in self.parent_product_revision_relation:
                parent_product_revision_relation_item = parent_product_revision_relation_item_data.to_dict()
                parent_product_revision_relation.append(parent_product_revision_relation_item)



        units: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.units, Unset):
            units = []
            for units_item_data in self.units:
                units_item = units_item_data.to_dict()
                units.append(units_item)



        bom: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.bom, Unset):
            bom = []
            for bom_item_data in self.bom:
                bom_item = bom_item_data.to_dict()
                bom.append(bom_item)



        settings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = []
            for settings_item_data in self.settings:
                settings_item = settings_item_data.to_dict()
                settings.append(settings_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if product_revision_id is not UNSET:
            field_dict["ProductRevisionId"] = product_revision_id
        if product_id is not UNSET:
            field_dict["ProductId"] = product_id
        if revision is not UNSET:
            field_dict["Revision"] = revision
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if state is not UNSET:
            field_dict["State"] = state
        if product is not UNSET:
            field_dict["Product"] = product
        if child_product_revision_relations is not UNSET:
            field_dict["ChildProductRevisionRelations"] = child_product_revision_relations
        if parent_product_revision_relation is not UNSET:
            field_dict["ParentProductRevisionRelation"] = parent_product_revision_relation
        if units is not UNSET:
            field_dict["Units"] = units
        if bom is not UNSET:
            field_dict["BOM"] = bom
        if settings is not UNSET:
            field_dict["Settings"] = settings

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_production_unit import VirincoWATSWebDashboardModelsMesProductionUnit
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision_relation import VirincoWATSWebDashboardModelsMesProductProductRevisionRelation
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_schemas_wsbfbom_component import VirincoWATSSchemasWSBFBOMComponent
        from ..models.virinco_wats_web_dashboard_models_mes_product_product import VirincoWATSWebDashboardModelsMesProductProduct
        d = dict(src_dict)
        _product_revision_id = d.pop("ProductRevisionId", UNSET)
        product_revision_id: Union[Unset, UUID]
        if isinstance(_product_revision_id,  Unset):
            product_revision_id = UNSET
        else:
            product_revision_id = UUID(_product_revision_id)




        _product_id = d.pop("ProductId", UNSET)
        product_id: Union[Unset, UUID]
        if isinstance(_product_id,  Unset):
            product_id = UNSET
        else:
            product_id = UUID(_product_id)




        revision = d.pop("Revision", UNSET)

        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        state = d.pop("State", UNSET)

        _product = d.pop("Product", UNSET)
        product: Union[Unset, VirincoWATSWebDashboardModelsMesProductProduct]
        if isinstance(_product,  Unset):
            product = UNSET
        else:
            product = VirincoWATSWebDashboardModelsMesProductProduct.from_dict(_product)




        child_product_revision_relations = []
        _child_product_revision_relations = d.pop("ChildProductRevisionRelations", UNSET)
        for child_product_revision_relations_item_data in (_child_product_revision_relations or []):
            child_product_revision_relations_item = VirincoWATSWebDashboardModelsMesProductProductRevisionRelation.from_dict(child_product_revision_relations_item_data)



            child_product_revision_relations.append(child_product_revision_relations_item)


        parent_product_revision_relation = []
        _parent_product_revision_relation = d.pop("ParentProductRevisionRelation", UNSET)
        for parent_product_revision_relation_item_data in (_parent_product_revision_relation or []):
            parent_product_revision_relation_item = VirincoWATSWebDashboardModelsMesProductProductRevisionRelation.from_dict(parent_product_revision_relation_item_data)



            parent_product_revision_relation.append(parent_product_revision_relation_item)


        units = []
        _units = d.pop("Units", UNSET)
        for units_item_data in (_units or []):
            units_item = VirincoWATSWebDashboardModelsMesProductionUnit.from_dict(units_item_data)



            units.append(units_item)


        bom = []
        _bom = d.pop("BOM", UNSET)
        for bom_item_data in (_bom or []):
            bom_item = VirincoWATSSchemasWSBFBOMComponent.from_dict(bom_item_data)



            bom.append(bom_item)


        settings = []
        _settings = d.pop("Settings", UNSET)
        for settings_item_data in (_settings or []):
            settings_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(settings_item_data)



            settings.append(settings_item)


        virinco_wats_web_dashboard_models_mes_product_product_revision = cls(
            product_revision_id=product_revision_id,
            product_id=product_id,
            revision=revision,
            name=name,
            description=description,
            state=state,
            product=product,
            child_product_revision_relations=child_product_revision_relations,
            parent_product_revision_relation=parent_product_revision_relation,
            units=units,
            bom=bom,
            settings=settings,
        )


        virinco_wats_web_dashboard_models_mes_product_product_revision.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_product_product_revision

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
