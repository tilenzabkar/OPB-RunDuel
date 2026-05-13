from Data.repository import Repo
from Data.models import UporabnikDto

from typing import List


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
