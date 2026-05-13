import datetime

from Data.repository import Repo
from Data.models import TipIzziva, Izziv, Tek, IzzivDto

from typing import List


class IzzivService:
    def __init__(self):
        self.repo = Repo()

    def _doloci_zmagovalca(
        self,
        vrsta: TipIzziva,
        teki_stavi: List[Tek],
        teki_nasprotuje: List[Tek],
        uporabnik_stavi: int,
        uporabnik_nasprotuje: int,
    ) -> tuple[int | None, int | None]:
        """
        Vrača tuple v obliki (zmagovalec_id, porazenec_id), v primeru nedoločenega rezultata vrne (None, None)
        """

        if teki_stavi == [] and teki_nasprotuje == []:
            return None, None

        if vrsta == TipIzziva.TEDENSKA_RAZDALJA:
            razdalja_stavi = sum(tek.razdalja for tek in teki_stavi)
            razdalja_nasprotuje = sum(tek.razdalja for tek in teki_nasprotuje)

            if razdalja_stavi > razdalja_nasprotuje:
                return uporabnik_stavi, uporabnik_nasprotuje
            elif razdalja_nasprotuje > razdalja_stavi:
                return uporabnik_nasprotuje, uporabnik_stavi
            else:
                return None, None

        else:
            najhitrejsi_tek_stavi = min(
                (tek.trajanje / tek.razdalja for tek in teki_stavi),
                default=float("inf"),
            )
            najhitrejsi_tek_nasprotuje = min(
                (tek.trajanje / tek.razdalja for tek in teki_nasprotuje),
                default=float("inf"),
            )

            if najhitrejsi_tek_stavi < najhitrejsi_tek_nasprotuje:
                return uporabnik_stavi, uporabnik_nasprotuje
            elif najhitrejsi_tek_nasprotuje < najhitrejsi_tek_stavi:
                return uporabnik_nasprotuje, uporabnik_stavi
            else:
                return None, None

    def ustvari_izziv(
        self,
        vrsta: TipIzziva,
        stava: int,
        datum_zacetka: datetime.datetime,
        uporabnik_stavi_id: int,
        uporabnik_nasprotuje_id: int,
    ) -> Izziv:
        """
        Ustvari izziv za dana dva uporabnika in jima odvzame stavo. Vrne ustvarjen izziv.
        """

        uporabnik_stavi = self.repo.dobi_uporabnika_po_id(uporabnik_stavi_id)
        uporabnik_nasprotuje = self.repo.dobi_uporabnika_po_id(uporabnik_nasprotuje_id)

        if uporabnik_stavi.stanje < stava:
            raise ValueError(
                f"Uporabnik {uporabnik_stavi.uporabnisko_ime} nima dovolj kovancev za to stavo!"
            )

        if uporabnik_nasprotuje.stanje < stava:
            raise ValueError(
                f"Uporabnik {uporabnik_nasprotuje.uporabnisko_ime} nima dovolj kovancev za to stavo!"
            )

        ustvarjen_izziv = self.repo.dodaj_izziv(
            vrsta, stava, datum_zacetka, uporabnik_stavi_id, uporabnik_nasprotuje_id
        )

        self.repo.rezerviraj_sredstva_za_izziv(
            ustvarjen_izziv.id, uporabnik_stavi_id, uporabnik_nasprotuje_id, stava
        )

        return ustvarjen_izziv

    def dobi_izzive(self, uporabnik_id: int) -> List[IzzivDto]:
        """
        Vrne vse izzive, kjer je dan uporabnik udeležen.
        """
        return self.repo.dobi_izzive_uporabnika(uporabnik_id)

    def zakljuci_izziv(self, izziv_id: int) -> None:
        """
        Za dan izziv določi zmagovalca in opravi izplačilo stave. V primeru remija vrne prvotne stave.
        """

        izziv = self.repo.dobi_izziv(izziv_id)

        if izziv.zmagovalec is not None:  # zmagovalec je že določen
            return

        if datetime.datetime.now() < izziv.datum_zacetka + datetime.timedelta(days=7):
            raise ValueError("Izziv še ni zaključen, ker še ni poteklo 7 dni!")

        teki_stavi = self.repo.dobi_teke_uporabnika_za_izziv(
            izziv.uporabnik_stavi, izziv.datum_zacetka, izziv.vrsta
        )

        teki_nasprotuje = self.repo.dobi_teke_uporabnika_za_izziv(
            izziv.uporabnik_nasprotuje, izziv.datum_zacetka, izziv.vrsta
        )

        zmagovalec_id, porazenec_id = self._doloci_zmagovalca(
            izziv.vrsta,
            teki_stavi,
            teki_nasprotuje,
            izziv.uporabnik_stavi,
            izziv.uporabnik_nasprotuje,
        )

        if zmagovalec_id is not None and porazenec_id is not None:
            self.repo.nastavi_zmagovalca(izziv_id, zmagovalec_id)

            self.repo.izvedi_izplacilo_izziva(izziv_id, zmagovalec_id, izziv.stava)

        else:  # Remi, vrnemo stave
            self.repo.vrni_stave_izziva(
                izziv_id, izziv.uporabnik_stavi, izziv.uporabnik_nasprotuje, izziv.stava
            )
