from Data.repository import Repo
from Data.models import Transakcija

from typing import List


class TransactionService:
    def __init__(self):
        self.repo = Repo()

    def dobi_transakcije_uporabnika(self, uporabnik_id: int) -> List[Transakcija]:
        """
        Vrne seznam vseh transakcij za danega uporabnika.
        """
        return self.repo.dobi_transakcije_uporabnika(uporabnik_id)
