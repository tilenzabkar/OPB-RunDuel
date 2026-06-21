from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from enum import Enum
from typing import Optional


class TipIzziva(str, Enum):
    PET_KM = "5km"
    DESET_KM = "10km"
    POL_MARATON = "21km"
    MARATON = "42km"
    TEDENSKA_RAZDALJA = "tedenska_razdalja"


ZACETNO_STANJE = 100


@dataclass_json
@dataclass
class Uporabnik:
    id: int = field(default=0)
    uporabnisko_ime: str = field(default="")
    geslo: str = field(default="")
    stanje: int = field(default=ZACETNO_STANJE)


@dataclass_json
@dataclass
class UporabnikDto:
    id: int = field(default=0)
    uporabnisko_ime: str = field(default="")
    stanje: int = field(default=ZACETNO_STANJE)


@dataclass_json
@dataclass
class Tek:
    id: int = field(default=0)
    datum: datetime = field(default=datetime.now())
    razdalja: float = field(default=0.0)
    trajanje: int = field(default=0)
    uporabnik: int = field(default=0)


@dataclass_json
@dataclass
class Izziv:
    id: int = field(default=0)
    vrsta: TipIzziva = field(default=TipIzziva.TEDENSKA_RAZDALJA)
    stava: int = field(default=0)
    datum_zacetka: datetime = field(default=datetime.now())
    uporabnik_stavi: int = field(default=0)
    uporabnik_nasprotuje: int = field(default=0)
    zmagovalec: Optional[int] = field(default=None)
    je_zakljucen: bool = field(default=False)
    je_sprejet: bool = field(default=False)


@dataclass_json
@dataclass
class IzzivDto:
    id: int = field(default=0)
    vrsta: str = field(default="")
    stava: int = field(default=0)
    datum_zacetka: datetime = field(default=datetime.now())
    uporabnik_stavi: int = field(default=0)
    uporabnik_stavi_ime: str = field(default="")
    uporabnik_nasprotuje: int = field(default=0)
    uporabnik_nasprotuje_ime: str = field(default="")
    zmagovalec: Optional[int] = field(default=None)
    zmagovalec_ime: Optional[str] = field(default=None)
    je_zakljucen: bool = field(default="false")
    je_sprejet: bool = field(default=False)


@dataclass_json
@dataclass
class Transakcija:
    id: int = field(default=0)
    sprememba: int = field(default=0)
    cas: datetime = field(default=datetime.now())
    uporabnik: int = field(default=0)
    izziv: int = field(default=0)
