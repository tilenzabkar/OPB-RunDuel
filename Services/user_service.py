from Data.repository import Repo
from Data.models import UporabnikDto

from typing import List, Optional
import datetime


class UserService:
    def __init__(self):
        self.repo = Repo()

    def dobi_vse_uporabnike(self) -> List[UporabnikDto]:
        """
        Vrne seznam vseh uporabnikov (v DTO brez gesla).
        """
        return self.repo.dobi_vse_uporabnike()

    def dobi_uporabnika(self, uporabnisko_ime: str) -> UporabnikDto:
        """
        Vrne uporabnika iz danega uporabniškega imena.
        """
        return self.repo.dobi_uporabnika(uporabnisko_ime)

    def dobi_uporabnika_po_id(self, uporabnik_id: int) -> UporabnikDto:
        """
        Vrne uporabnika iz danega IDja.
        """
        return self.repo.dobi_uporabnika_po_id(uporabnik_id)

    def povecaj_stanje_uporabniku(
        self, uporabnik_id: int, sprememba: int, izziv_id: Optional[int] = None
    ) -> None:
        """
        Spremeni danemu uporabniku stanje za vrednost "sprememba" in shrani transakcijo.
        """
        self.repo.povecaj_stanje_uporabniku(uporabnik_id, sprememba, izziv_id)

    def je_uporabnik_dobil_bonus(
        self, uporabnik_id: int, cas: datetime.datetime
    ) -> bool:
        """
        Preveri, če je ta koledarski teden uporabnik že dobil bonus
        """
        return self.repo.je_uporabnik_dobil_bonus(uporabnik_id, cas)
