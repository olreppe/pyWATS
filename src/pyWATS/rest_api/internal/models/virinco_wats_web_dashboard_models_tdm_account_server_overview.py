from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_recent_articles import VirincoWATSWebDashboardModelsTdmRecentArticles





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmAccountServerOverview")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmAccountServerOverview:
    """ 
        Attributes:
            pod (Union[Unset, str]):
            setup_date (Union[Unset, str]):
            user_count (Union[Unset, int]):
            connected_clients_count (Union[Unset, int]):
            recent_articles (Union[Unset, list['VirincoWATSWebDashboardModelsTdmRecentArticles']]):
     """

    pod: Union[Unset, str] = UNSET
    setup_date: Union[Unset, str] = UNSET
    user_count: Union[Unset, int] = UNSET
    connected_clients_count: Union[Unset, int] = UNSET
    recent_articles: Union[Unset, list['VirincoWATSWebDashboardModelsTdmRecentArticles']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_recent_articles import VirincoWATSWebDashboardModelsTdmRecentArticles
        pod = self.pod

        setup_date = self.setup_date

        user_count = self.user_count

        connected_clients_count = self.connected_clients_count

        recent_articles: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.recent_articles, Unset):
            recent_articles = []
            for recent_articles_item_data in self.recent_articles:
                recent_articles_item = recent_articles_item_data.to_dict()
                recent_articles.append(recent_articles_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if pod is not UNSET:
            field_dict["pod"] = pod
        if setup_date is not UNSET:
            field_dict["setupDate"] = setup_date
        if user_count is not UNSET:
            field_dict["userCount"] = user_count
        if connected_clients_count is not UNSET:
            field_dict["connectedClientsCount"] = connected_clients_count
        if recent_articles is not UNSET:
            field_dict["recentArticles"] = recent_articles

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_recent_articles import VirincoWATSWebDashboardModelsTdmRecentArticles
        d = dict(src_dict)
        pod = d.pop("pod", UNSET)

        setup_date = d.pop("setupDate", UNSET)

        user_count = d.pop("userCount", UNSET)

        connected_clients_count = d.pop("connectedClientsCount", UNSET)

        recent_articles = []
        _recent_articles = d.pop("recentArticles", UNSET)
        for recent_articles_item_data in (_recent_articles or []):
            recent_articles_item = VirincoWATSWebDashboardModelsTdmRecentArticles.from_dict(recent_articles_item_data)



            recent_articles.append(recent_articles_item)


        virinco_wats_web_dashboard_models_tdm_account_server_overview = cls(
            pod=pod,
            setup_date=setup_date,
            user_count=user_count,
            connected_clients_count=connected_clients_count,
            recent_articles=recent_articles,
        )


        virinco_wats_web_dashboard_models_tdm_account_server_overview.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_account_server_overview

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
