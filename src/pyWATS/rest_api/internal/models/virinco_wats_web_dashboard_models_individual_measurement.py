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






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsIndividualMeasurement")



@_attrs_define
class VirincoWATSWebDashboardModelsIndividualMeasurement:
    """ 
        Attributes:
            v (Union[Unset, float]):
            h (Union[Unset, float]):
            l (Union[Unset, float]):
            c (Union[Unset, str]):
            u (Union[Unset, str]):
            ts (Union[Unset, str]):
            ms (Union[Unset, str]):
            ss (Union[Unset, str]):
            cuf (Union[Unset, bool]):
            d (Union[Unset, datetime.datetime]):
            d2 (Union[Unset, datetime.datetime]):
            s (Union[Unset, str]):
            g (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            so (Union[Unset, int]):
            e (Union[Unset, float]):
            t (Union[Unset, float]):
            seqn (Union[Unset, str]):
            seqv (Union[Unset, str]):
            seqp (Union[Unset, str]):
            sva (Union[Unset, str]):
            sl (Union[Unset, str]):
            ec (Union[Unset, float]):
            bp (Union[Unset, int]):
            res (Union[Unset, str]):
            npr (Union[Unset, int]):
            npa (Union[Unset, int]):
            i (Union[Unset, int]):
            mv (Union[Unset, str]):
            md (Union[Unset, str]):
            misc_values (Union[Unset, str]):
            sp (Union[Unset, str]):
            sub_parts (Union[Unset, str]):
            m (Union[Unset, str]):
            op (Union[Unset, str]):
            p (Union[Unset, str]):
            r (Union[Unset, str]):
            b (Union[Unset, str]):
            si (Union[Unset, int]):
            f (Union[Unset, str]):
            to (Union[Unset, str]):
            sf (Union[Unset, str]):
            sv (Union[Unset, str]):
     """

    v: Union[Unset, float] = UNSET
    h: Union[Unset, float] = UNSET
    l: Union[Unset, float] = UNSET
    c: Union[Unset, str] = UNSET
    u: Union[Unset, str] = UNSET
    ts: Union[Unset, str] = UNSET
    ms: Union[Unset, str] = UNSET
    ss: Union[Unset, str] = UNSET
    cuf: Union[Unset, bool] = UNSET
    d: Union[Unset, datetime.datetime] = UNSET
    d2: Union[Unset, datetime.datetime] = UNSET
    s: Union[Unset, str] = UNSET
    g: Union[Unset, UUID] = UNSET
    so: Union[Unset, int] = UNSET
    e: Union[Unset, float] = UNSET
    t: Union[Unset, float] = UNSET
    seqn: Union[Unset, str] = UNSET
    seqv: Union[Unset, str] = UNSET
    seqp: Union[Unset, str] = UNSET
    sva: Union[Unset, str] = UNSET
    sl: Union[Unset, str] = UNSET
    ec: Union[Unset, float] = UNSET
    bp: Union[Unset, int] = UNSET
    res: Union[Unset, str] = UNSET
    npr: Union[Unset, int] = UNSET
    npa: Union[Unset, int] = UNSET
    i: Union[Unset, int] = UNSET
    mv: Union[Unset, str] = UNSET
    md: Union[Unset, str] = UNSET
    misc_values: Union[Unset, str] = UNSET
    sp: Union[Unset, str] = UNSET
    sub_parts: Union[Unset, str] = UNSET
    m: Union[Unset, str] = UNSET
    op: Union[Unset, str] = UNSET
    p: Union[Unset, str] = UNSET
    r: Union[Unset, str] = UNSET
    b: Union[Unset, str] = UNSET
    si: Union[Unset, int] = UNSET
    f: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    sf: Union[Unset, str] = UNSET
    sv: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        v = self.v

        h = self.h

        l = self.l

        c = self.c

        u = self.u

        ts = self.ts

        ms = self.ms

        ss = self.ss

        cuf = self.cuf

        d: Union[Unset, str] = UNSET
        if not isinstance(self.d, Unset):
            d = self.d.isoformat()

        d2: Union[Unset, str] = UNSET
        if not isinstance(self.d2, Unset):
            d2 = self.d2.isoformat()

        s = self.s

        g: Union[Unset, str] = UNSET
        if not isinstance(self.g, Unset):
            g = str(self.g)

        so = self.so

        e = self.e

        t = self.t

        seqn = self.seqn

        seqv = self.seqv

        seqp = self.seqp

        sva = self.sva

        sl = self.sl

        ec = self.ec

        bp = self.bp

        res = self.res

        npr = self.npr

        npa = self.npa

        i = self.i

        mv = self.mv

        md = self.md

        misc_values = self.misc_values

        sp = self.sp

        sub_parts = self.sub_parts

        m = self.m

        op = self.op

        p = self.p

        r = self.r

        b = self.b

        si = self.si

        f = self.f

        to = self.to

        sf = self.sf

        sv = self.sv


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if v is not UNSET:
            field_dict["v"] = v
        if h is not UNSET:
            field_dict["h"] = h
        if l is not UNSET:
            field_dict["l"] = l
        if c is not UNSET:
            field_dict["c"] = c
        if u is not UNSET:
            field_dict["u"] = u
        if ts is not UNSET:
            field_dict["ts"] = ts
        if ms is not UNSET:
            field_dict["ms"] = ms
        if ss is not UNSET:
            field_dict["ss"] = ss
        if cuf is not UNSET:
            field_dict["cuf"] = cuf
        if d is not UNSET:
            field_dict["d"] = d
        if d2 is not UNSET:
            field_dict["d2"] = d2
        if s is not UNSET:
            field_dict["s"] = s
        if g is not UNSET:
            field_dict["g"] = g
        if so is not UNSET:
            field_dict["so"] = so
        if e is not UNSET:
            field_dict["e"] = e
        if t is not UNSET:
            field_dict["t"] = t
        if seqn is not UNSET:
            field_dict["seqn"] = seqn
        if seqv is not UNSET:
            field_dict["seqv"] = seqv
        if seqp is not UNSET:
            field_dict["seqp"] = seqp
        if sva is not UNSET:
            field_dict["sva"] = sva
        if sl is not UNSET:
            field_dict["sl"] = sl
        if ec is not UNSET:
            field_dict["ec"] = ec
        if bp is not UNSET:
            field_dict["bp"] = bp
        if res is not UNSET:
            field_dict["res"] = res
        if npr is not UNSET:
            field_dict["npr"] = npr
        if npa is not UNSET:
            field_dict["npa"] = npa
        if i is not UNSET:
            field_dict["i"] = i
        if mv is not UNSET:
            field_dict["mv"] = mv
        if md is not UNSET:
            field_dict["md"] = md
        if misc_values is not UNSET:
            field_dict["miscValues"] = misc_values
        if sp is not UNSET:
            field_dict["sp"] = sp
        if sub_parts is not UNSET:
            field_dict["subParts"] = sub_parts
        if m is not UNSET:
            field_dict["m"] = m
        if op is not UNSET:
            field_dict["op"] = op
        if p is not UNSET:
            field_dict["p"] = p
        if r is not UNSET:
            field_dict["r"] = r
        if b is not UNSET:
            field_dict["b"] = b
        if si is not UNSET:
            field_dict["si"] = si
        if f is not UNSET:
            field_dict["f"] = f
        if to is not UNSET:
            field_dict["to"] = to
        if sf is not UNSET:
            field_dict["sf"] = sf
        if sv is not UNSET:
            field_dict["sv"] = sv

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        v = d.pop("v", UNSET)

        h = d.pop("h", UNSET)

        l = d.pop("l", UNSET)

        c = d.pop("c", UNSET)

        u = d.pop("u", UNSET)

        ts = d.pop("ts", UNSET)

        ms = d.pop("ms", UNSET)

        ss = d.pop("ss", UNSET)

        cuf = d.pop("cuf", UNSET)

        _d = d.pop("d", UNSET)
        d: Union[Unset, datetime.datetime]
        if isinstance(_d,  Unset):
            d = UNSET
        else:
            d = isoparse(_d)




        _d2 = d.pop("d2", UNSET)
        d2: Union[Unset, datetime.datetime]
        if isinstance(_d2,  Unset):
            d2 = UNSET
        else:
            d2 = isoparse(_d2)




        s = d.pop("s", UNSET)

        _g = d.pop("g", UNSET)
        g: Union[Unset, UUID]
        if isinstance(_g,  Unset):
            g = UNSET
        else:
            g = UUID(_g)




        so = d.pop("so", UNSET)

        e = d.pop("e", UNSET)

        t = d.pop("t", UNSET)

        seqn = d.pop("seqn", UNSET)

        seqv = d.pop("seqv", UNSET)

        seqp = d.pop("seqp", UNSET)

        sva = d.pop("sva", UNSET)

        sl = d.pop("sl", UNSET)

        ec = d.pop("ec", UNSET)

        bp = d.pop("bp", UNSET)

        res = d.pop("res", UNSET)

        npr = d.pop("npr", UNSET)

        npa = d.pop("npa", UNSET)

        i = d.pop("i", UNSET)

        mv = d.pop("mv", UNSET)

        md = d.pop("md", UNSET)

        misc_values = d.pop("miscValues", UNSET)

        sp = d.pop("sp", UNSET)

        sub_parts = d.pop("subParts", UNSET)

        m = d.pop("m", UNSET)

        op = d.pop("op", UNSET)

        p = d.pop("p", UNSET)

        r = d.pop("r", UNSET)

        b = d.pop("b", UNSET)

        si = d.pop("si", UNSET)

        f = d.pop("f", UNSET)

        to = d.pop("to", UNSET)

        sf = d.pop("sf", UNSET)

        sv = d.pop("sv", UNSET)

        virinco_wats_web_dashboard_models_individual_measurement = cls(
            v=v,
            h=h,
            l=l,
            c=c,
            u=u,
            ts=ts,
            ms=ms,
            ss=ss,
            cuf=cuf,
            d=d,
            d2=d2,
            s=s,
            g=g,
            so=so,
            e=e,
            t=t,
            seqn=seqn,
            seqv=seqv,
            seqp=seqp,
            sva=sva,
            sl=sl,
            ec=ec,
            bp=bp,
            res=res,
            npr=npr,
            npa=npa,
            i=i,
            mv=mv,
            md=md,
            misc_values=misc_values,
            sp=sp,
            sub_parts=sub_parts,
            m=m,
            op=op,
            p=p,
            r=r,
            b=b,
            si=si,
            f=f,
            to=to,
            sf=sf,
            sv=sv,
        )


        virinco_wats_web_dashboard_models_individual_measurement.additional_properties = d
        return virinco_wats_web_dashboard_models_individual_measurement

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
