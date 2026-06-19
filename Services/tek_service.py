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

    def dobi_tek(self, tek_id) -> Tek:
        """
        Vrne objekt Tek za dan tek_id.
        """
        return self.repo.dobi_tek(tek_id)

    def preveri_in_posodobi_tek(
        self,
        tek_id: int,
        uporabnik_id: int,
        datum: datetime.datetime,
        razdalja: float,
        trajanje: int,
    ) -> None:
        """
        Preveri, če je dan uporabnik lastnik teka in v tem primeru tek posodobi z novimi podatki.
        """
        tek = self.repo.dobi_tek(tek_id)

        if tek.uporabnik != uporabnik_id:
            raise PermissionError("Nimate dovoljenja za brisanje tega teka.")

        self.repo.posodobi_tek(tek_id, datum, razdalja, trajanje)

    def preveri_in_izbrisi_tek(self, tek_id: int, uporabnik_id: int) -> None:
        """
        Preveri, če je dan uporabnik lastnik teka in ga v tem primeru izbriše.
        """
        tek = self.repo.dobi_tek(tek_id)

        if tek.uporabnik != uporabnik_id:
            raise PermissionError("Nimate dovoljenja za brisanje tega teka.")

        self.repo.izbrisi_tek(tek_id)
