import psycopg2, psycopg2.extensions, psycopg2.extras

psycopg2.extensions.register_type(
    psycopg2.extensions.UNICODE
)  # sicer problemi s šumniki
import Data.auth_public as auth_public
import datetime
import os
import bcrypt

from psycopg2 import sql
from Data.models import (
    Tek,
    Izziv,
    TipIzziva,
    Transakcija,
    UporabnikDto,
    Uporabnik,
    ZACETNO_STANJE,
)
from typing import List

DB_PORT = os.environ.get("POSTGRES_PORT", 5432)


class Repo:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            database=auth_public.db,
            host=auth_public.host,
            user=auth_public.user,
            password=auth_public.password,
        )

    def ustvari_tabele(self) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                # Uporabnik
                cur.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS uporabnik (
                        id SERIAL PRIMARY KEY,
                        uporabnisko_ime TEXT NOT NULL UNIQUE,
                        geslo TEXT,
                        stanje INTEGER NOT NULL DEFAULT {zacetno_stanje}
                    )
                    """).format(ZACETNO_STANJE=sql.Literal(ZACETNO_STANJE)))

                # Tek
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tek (
                        id SERIAL PRIMARY KEY,
                        datum TIMESTAMP NOT NULL,
                        razdalja FLOAT NOT NULL,
                        trajanje INTEGER NOT NULL,
                        uporabnik INTEGER NOT NULL REFERENCES uporabnik(id)
                    )
                    """)

                # Izziv
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS izziv (
                        id SERIAL PRIMARY KEY,
                        vrsta TEXT NOT NULL,
                        stava INTEGER NOT NULL,
                        datum_zacetka TIMESTAMP NOT NULL,
                        uporabnik_stavi INTEGER NOT NULL REFERENCES uporabnik(id),
                        uporabnik_nasprotuje INTEGER NOT NULL REFERENCES uporabnik(id),
                        zmagovalec INTEGER REFERENCES uporabnik(id)
                    )
                    """)

                # Transakcija
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS transakcija (
                        id SERIAL PRIMARY KEY,
                        sprememba INTEGER NOT NULL,
                        cas TIMESTAMP NOT NULL DEFAULT (NOW()),
                        uporabnik INTEGER NOT NULL REFERENCES uporabnik(id),
                        izziv INTEGER REFERENCES izziv(id)
                    )
                    """)

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
                    RETURNING id, vrsta, stava, datum_zacetka, uporabnik_stavi, uporabnik_nasprotuje, zmagovalec
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
                    SELECT id, vrsta, stava, datum_zacetka, uporabnik_stavi,        uporabnik_nasprotuje, zmagovalec
                    FROM izziv
                    WHERE id = %s
                    """,
                    (id,),
                )

                vrstica = cur.fetchone()
                if vrstica is None:
                    raise ValueError(f"Izziv z IDjem {id} ne obstaja!")
                return Izziv.from_dict(vrstica)

    def dobi_izzive_uporabnika(self, uporabnik_id: int) -> List[Izziv]:
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, vrsta, stava, datum_zacetka, uporabnik_stavi, uporabnik_nasprotuje, zmagovalec
                    FROM izziv
                    WHERE uporabnik_stavi = %s OR uporabnik_nasprotuje = %s
                    ORDER BY datum_zacetka DESC
                    """,
                    (uporabnik_id, uporabnik_id),
                )
                return [Izziv.from_dict(row) for row in cur.fetchall()]

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

    # --- TRANSAKCIJE ---

    def dodaj_transakcijo(
        self, sprememba: int, uporabnik_id: int, izziv_id: int = None
    ) -> Transakcija:
        cas_transakcije = datetime.datetime.now()
        with self.conn:
            with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO transakcija (sprememba, cas, uporabnik, izziv)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, sprememba, cas, uporabnik, izziv
                    """,
                    (sprememba, cas_transakcije, uporabnik_id, izziv_id),
                )

                return Transakcija.from_dict(cur.fetchone())

    def rezerviraj_sredstva_za_izziv(
        self,
        izziv_id: int,
        uporabnik_stavi_id: int,
        uporabnik_nasprotuje_id: int,
        stava: int,
    ) -> None:
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                   UPDATE uporabnik
                   SET stanje = stanje - %s
                   WHERE id in (%s, %s)
                   """,
                    (stava, uporabnik_stavi_id, uporabnik_nasprotuje_id),
                )

        self.dodaj_transakcijo(-stava, uporabnik_stavi_id, izziv_id)
        self.dodaj_transakcijo(-stava, uporabnik_nasprotuje_id, izziv_id)

    def izvedi_izplacilo_izziva(
        self, izziv_id: int, zmagovalec_id: int, porazenec_id: int, stava: int
    ) -> None:
        dobitek = 2 * stava  # zmagovalcu moramo vrniti tudi rezervirana sredstva

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE uporabnik 
                    SET stanje = stanje + %s 
                    WHERE id = %s
                    """,
                    (dobitek, zmagovalec_id),
                )

        self.dodaj_transakcijo(dobitek, zmagovalec_id, izziv_id)
