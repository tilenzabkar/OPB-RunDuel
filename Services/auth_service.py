import bcrypt

from Data.repository import Repo
from Data.models import UporabnikDto, Uporabnik


class AuthService:
    repo: Repo

    def __init__(self):
        self.repo = Repo()

    def dodaj_uporabnika(self, uporabnisko_ime: str, geslo: str) -> UporabnikDto:
        znacka_gesla = geslo.encode("utf-8")
        sol = bcrypt.gensalt()
        zgosceno_geslo = bcrypt.hashpw(znacka_gesla, sol)

        uporabnik = Uporabnik(
            uporabnisko_ime=uporabnisko_ime, geslo=zgosceno_geslo.decode()
        )

        self.repo.dodaj_uporabnika(uporabnik)

        return UporabnikDto(uporabnisko_ime=uporabnisko_ime)

    def prijava(self, uporabnisko_ime: str, geslo: str) -> UporabnikDto:
        uporabnik = self.repo.dobi_uporabnika(uporabnisko_ime)
        geslo = geslo.encode("utf-8")

        if not bcrypt.checkpw(geslo, uporabnik.geslo.encode("utf-8")):
            raise ValueError("Napačno geslo!")

        return UporabnikDto(uporabnisko_ime=uporabnisko_ime, stanje=uporabnik.stanje)
