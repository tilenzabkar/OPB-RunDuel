from Data.repository import Repo
from Data.models import Tek

from typing import List
import datetime


class TekService:
    def __init__(self):
        self.repo = Repo()

    def dodaj_tek(
        self,
        uporabnik_id: int,
        datum: datetime.datetime,
        razdalja: float,
        trajanje: int,
    ) -> Tek:
        """
        Doda nov tek za danega uporabnika.
        """
        return self.repo.dodaj_tek(uporabnik_id, datum, razdalja, trajanje)

    def dobi_teke_uporabnika(self, uporabnik_id: int) -> List[Tek]:
        """
        Vrne vse teke za danega uporabnika.
        """
        return self.repo.dobi_teke_uporabnika(uporabnik_id)
