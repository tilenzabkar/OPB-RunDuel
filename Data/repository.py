import psycopg2, psycopg2.extensions, psycopg2.extras

psycopg2.extensions.register_type(
    psycopg2.extensions.UNICODE
)  # sicer problemi s šumniki
import Data.auth_public as auth_public
import datetime
import os

from Data.models import Tek, Transakcija
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
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def dobi_teke(self) -> List[Tek]:
        self.cur.execute("""
            SELECT id, datum, razdalja, trajanje, uporabnik
            FROM tek
            ORDER BY datum desc
            """)

        teki = [Tek.from_dict(row) for row in self.cur.fetchall()]
        return teki

    def dobi_tek(self, id: int) -> Tek:
        self.cur.execute(
            """
            SELECT id, datum, razdalja, trajanje, uporabnik
            FROM tek
            WHERE id = %s
            """,
            (id,),
        )

        t = Tek.from_dict(self.cur.fetchone())
        return t
