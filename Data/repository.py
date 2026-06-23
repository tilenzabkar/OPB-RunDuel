import psycopg2, psycopg2.extensions, psycopg2.extras

psycopg2.extensions.register_type(
    psycopg2.extensions.UNICODE
)  # sicer problemi s šumniki
import datetime
import os

from psycopg2 import sql
from Data.models import (
    Tek,
    Izziv,
    TipIzziva,
    IzzivDto,
    UporabnikDto,
    Uporabnik,
    Transakcija,
    ZACETNO_STANJE,
)
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class Repo:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            database=os.environ.get("DB_NAME"),
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT", 5432),
        )

    def ustvari_tabele(self) -> None:
        pot = os.path.join(os.path.dirname(__file__), "schema.sql")

        with open(pot, encoding="utf-8") as f:
            sql_script = f.read()

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql_script)

    def podeli_pravice(self) -> None:
        pot = os.path.join(os.path.dirname(__file__), "grant_privileges.sql")

        with open(pot, encoding="utf-8") as f:
            sql_script = f.read()

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql_script)

    def _dobi_mejo_razdalje(self, vrsta_izziva: TipIzziva) -> tuple[float, float]:
        meje = {
            TipIzziva.PET_KM: (5.0, 5.5),
            TipIzziva.DESET_KM: (10.0, 10.5),
            TipIzziva.POL_MARATON: (21.1, 22.0),
            TipIzziva.MARATON: (42.2, 43.0),
        }

        return meje.get(vrsta_izziva, (0.0, float("inf")))

    # --- UPORABNIK ---

    def dodaj_uporabnika(self, uporabnik: Uporabnik) -> UporabnikDto:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO uporabnik (uporabnisko_ime, geslo, stanje)
                    VALUES (%s, %s, %s)
                    RETURNING id, uporabnisko_ime, stanje
                    """,
                    (uporabnik.uporabnisko_ime, uporabnik.geslo, ZACETNO_STANJE),
                )

                return UporabnikDto.from_dict(cur.fetchone())

    def dobi_uporabnika(self, uporabnisko_ime: str) -> Uporabnik:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, uporabnisko_ime, geslo, stanje
                    FROM uporabnik
                    WHERE uporabnisko_ime = %s
                    """,
                    (uporabnisko_ime,),
                )

                vrstica = cur.fetchone()
                if vrstica is None:
                    raise ValueError(
                        f"Uporabnik z uporabniškim imenom {uporabnisko_ime} ne obstaja!"
                    )

                return Uporabnik.from_dict(vrstica)

    def dobi_uporabnika_po_id(self, uporabnik_id: int) -> Uporabnik:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, uporabnisko_ime, geslo, stanje
                    FROM uporabnik
                    WHERE id = %s
                    """,
                    (uporabnik_id,),
                )

                vrstica = cur.fetchone()
                if vrstica is None:
                    raise ValueError(f"Uporabnik z IDjem {uporabnik_id} ne obstaja!")

                return Uporabnik.from_dict(vrstica)

    def dobi_vse_uporabnike(self) -> List[UporabnikDto]:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("""
                    SELECT id, uporabnisko_ime, stanje
                    FROM uporabnik
                    ORDER BY stanje DESC
                    """)

                return [UporabnikDto.from_dict(row) for row in cur.fetchall()]

    def povecaj_stanje_uporabniku(
        self, uporabnik_id: int, sprememba: int, izziv_id: Optional[int]
    ) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE uporabnik
                    SET stanje = stanje + %s
                    WHERE id = %s
                    """,
                    (sprememba, uporabnik_id),
                )
                if cur.rowcount == 0:
                    raise ValueError(f"Uporabnik z IDjem {uporabnik_id} ne obstaja!")

                cur.execute(
                    """
                    INSERT INTO transakcija (sprememba, cas, uporabnik, izziv)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (sprememba, datetime.datetime.now(), uporabnik_id, izziv_id),
                )

    def je_uporabnik_dobil_bonus(
        self, uporabnik_id: int, cas: datetime.datetime
    ) -> bool:
        start_of_week = cas - datetime.timedelta(days=cas.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COUNT(*) FROM transakcija
                    WHERE uporabnik = %s
                      AND sprememba = 100
                      AND izziv IS NULL
                      AND cas >= %s
                    """,
                    (uporabnik_id, start_of_week),
                )

                return cur.fetchone()[0] > 0

    # --- TEKI ---

    def dodaj_tek(
        self,
        uporabnik_id: int,
        datum: datetime.datetime,
        razdalja: float,
        trajanje: int,
    ) -> Tek:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO tek (datum, razdalja, trajanje, uporabnik)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, datum, razdalja, trajanje, uporabnik
                    """,
                    (datum, razdalja, trajanje, uporabnik_id),
                )

                return Tek.from_dict(cur.fetchone())

    def dobi_tek(self, id: int) -> Tek:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, datum, razdalja, trajanje, uporabnik
                    FROM tek
                    WHERE id = %s
                    """,
                    (id,),
                )

                vrstica = cur.fetchone()
                if vrstica is None:
                    raise ValueError(f"Tek z IDjem {id} ne obstaja!")
                return Tek.from_dict(vrstica)

    def dobi_teke(self) -> List[Tek]:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("""
                    SELECT id, datum, razdalja, trajanje, uporabnik
                    FROM tek
                    ORDER BY datum DESC
                    """)

                return [Tek.from_dict(row) for row in cur.fetchall()]

    def dobi_teke_uporabnika(self, uporabnik_id: int) -> List[Tek]:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, datum, razdalja, trajanje, uporabnik
                    FROM tek
                    WHERE uporabnik = %s
                    ORDER BY datum DESC
                    """,
                    (uporabnik_id,),
                )

                return [Tek.from_dict(row) for row in cur.fetchall()]

    def dobi_teke_uporabnika_za_izziv(
        self,
        uporabnik_id: int,
        datum_zacetka: datetime.datetime,
        vrsta_izziva: TipIzziva,
    ) -> List[Tek]:
        min_razdalja, max_razdalja = self._dobi_mejo_razdalje(vrsta_izziva)
        datum_konca = datum_zacetka + datetime.timedelta(days=7)

        razdalja_pogoj_str = (
            "AND razdalja >= %(min_razdalja)s AND razdalja <= %(max_razdalja)s"
            if vrsta_izziva != TipIzziva.TEDENSKA_RAZDALJA
            else ""
        )

        query = sql.SQL("""
            SELECT id, datum, razdalja, trajanje, uporabnik
            FROM tek
            WHERE uporabnik = %(uporabnik)s 
              AND datum >= %(datum_zacetka)s AND datum < %(datum_konca)s 
              {razdalja_pogoj}
            ORDER BY datum DESC
            """).format(razdalja_pogoj=sql.SQL(razdalja_pogoj_str))

        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    query,
                    {
                        "uporabnik": uporabnik_id,
                        "datum_zacetka": datum_zacetka,
                        "datum_konca": datum_konca,
                        "min_razdalja": min_razdalja,
                        "max_razdalja": max_razdalja,
                    },
                )

                return [Tek.from_dict(row) for row in cur.fetchall()]

    def posodobi_tek(
        self, tek_id: int, datum: datetime.datetime, razdalja: float, trajanje: int
    ) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE tek
                    SET datum = %s, razdalja = %s, trajanje = %s
                    WHERE id = %s
                    """,
                    (datum, razdalja, trajanje, tek_id),
                )

    def izbrisi_tek(self, tek_id: int) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM tek WHERE id = %s", (tek_id,))

    # --- IZZIV ---

    def dodaj_izziv(
        self,
        vrsta: TipIzziva,
        stava: int,
        datum_zacetka: datetime.datetime,
        uporabnik_stavi: int,
        uporabnik_nasprotuje: int,
    ) -> Izziv:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO izziv (vrsta, stava, datum_zacetka, uporabnik_stavi, uporabnik_nasprotuje)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, vrsta, stava, datum_zacetka, uporabnik_stavi, uporabnik_nasprotuje, zmagovalec, je_zakljucen, je_sprejet
                    """,
                    (
                        vrsta.value,
                        stava,
                        datum_zacetka,
                        uporabnik_stavi,
                        uporabnik_nasprotuje,
                    ),
                )

                return Izziv.from_dict(cur.fetchone())

    def dobi_izziv(self, id: int) -> Izziv:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT 
                        id, 
                        vrsta, 
                        stava, 
                        datum_zacetka, 
                        uporabnik_stavi, 
                        uporabnik_nasprotuje, 
                        zmagovalec, 
                        je_zakljucen, 
                        je_sprejet
                    FROM izziv
                    WHERE id = %s
                    """,
                    (id,),
                )

                vrstica = cur.fetchone()
                if vrstica is None:
                    raise ValueError(f"Izziv z IDjem {id} ne obstaja!")
                return Izziv.from_dict(vrstica)

    def dobi_aktivne_potekle_izzive(self, cas: datetime.datetime) -> List[Izziv]:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT * FROM izziv
                    WHERE je_sprejet = TRUE
                      AND je_zakljucen = FALSE
                      AND datum_zacetka + INTERVAL '7 days' <= %s
                    """,
                    (cas,),
                )
                return [Izziv.from_dict(row) for row in cur.fetchall()]

    def dobi_izzive_uporabnika(self, uporabnik_id: int) -> List[IzzivDto]:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT 
                        i.id AS id, 
                        i.vrsta AS vrsta, 
                        i.stava AS stava, 
                        i.datum_zacetka AS datum_zacetka, 
                        i.uporabnik_stavi AS uporabnik_stavi, 
                        stavi.uporabnisko_ime AS uporabnik_stavi_ime, 
                        i.uporabnik_nasprotuje AS uporabnik_nasprotuje, 
                        nasprotuje.uporabnisko_ime AS uporabnik_nasprotuje_ime,
                        i.zmagovalec AS zmagovalec,
                        COALESCE(zmaga.uporabnisko_ime, '') AS zmagovalec_ime,
                        i.je_zakljucen AS je_zakljucen,
                        i.je_sprejet AS je_sprejet
                    FROM izziv AS i
                    JOIN uporabnik AS stavi ON stavi.id = i.uporabnik_stavi
                    JOIN uporabnik AS nasprotuje ON nasprotuje.id = i.uporabnik_nasprotuje
                    LEFT JOIN uporabnik AS zmaga ON zmaga.id = i.zmagovalec
                    WHERE i.uporabnik_stavi = %s OR i.uporabnik_nasprotuje = %s
                    ORDER BY i.datum_zacetka DESC
                    """,
                    (uporabnik_id, uporabnik_id),
                )
                return [IzzivDto.from_dict(row) for row in cur.fetchall()]

    def sprejmi_izziv(self, izziv_id: int) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE izziv
                    SET je_sprejet = TRUE
                    WHERE id = %s
                    """,
                    (izziv_id,),
                )

    def nastavi_zmagovalca(self, izziv_id: int, zmagovalec_id: int) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE izziv
                    SET zmagovalec = %s
                    WHERE id = %s
                    """,
                    (zmagovalec_id, izziv_id),
                )

    def zakljuci_izziv(self, izziv_id: int) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE izziv
                    SET je_zakljucen = TRUE
                    WHERE id = %s
                    """,
                    (izziv_id,),
                )
