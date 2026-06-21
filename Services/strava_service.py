from Data.repository import Repo
from Data.models import Tek
from typing import List
from psycopg2.errors import UniqueViolation
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
STRAVA_API_URL = "https://www.strava.com/api/v3"


class StravaService:
    def __init__(self):
        self.repo = Repo()

    def generiraj_prijavni_url(self, redirect_uri: str, state: str) -> str:
        """
        Vrne URL, na katerega mora API preusmeriti uporabnika,
        da se prijavi v Stravo in naši aplikaciji odobri dostop do svojih tekov.
        """
        if STRAVA_CLIENT_ID is None:
            raise ValueError("Napaka pri konfiguraciji Strava API ključev!")

        url = (
            f"https://www.strava.com/oauth/authorize"
            f"?client_id={STRAVA_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={redirect_uri}"
            f"&approval_prompt=force"
            f"&scope=activity:read"  # samo beremo
            f"&state={state}"  # oauth varnost
        )
        return url

    def pridobi_dostopni_zeton(self, auth_koda: str) -> str:
        """
        Vrne access token (dostopni žeton).
        """

        if STRAVA_CLIENT_ID is None or STRAVA_CLIENT_SECRET is None:
            raise ValueError("Napaka pri konfiguraciji Strava API ključev!")

        url = "https://www.strava.com/oauth/token"
        payload = {
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "code": auth_koda,
            "grant_type": "authorization_code",
        }

        response = requests.post(url, data=payload)
        response.raise_for_status()

        podatki = response.json()
        return podatki.get("access_token")

    def dobi_teke_iz_strave(self, uporabnik_id: int, access_token: str) -> List[Tek]:
        headers = {"Authorization": f"Bearer {access_token}"}
        page = 1
        shranjeni_teki = []
        MAX_PAGES = 50

        while page <= MAX_PAGES:
            response = requests.get(
                f"{STRAVA_API_URL}/athlete/activities",
                headers=headers,
                params={"per_page": 20, "page": page},
            )
            response.raise_for_status()

            aktivnosti = response.json()
            if not aktivnosti:
                break

            for aktivnost in aktivnosti:
                if aktivnost.get("type") == "Run":
                    razdalja_km = round(
                        aktivnost.get("distance", 0) / 1000, 2
                    )  # Strava vrne razdalje v metrih
                    trajanje_sekunde = aktivnost.get(
                        "moving_time", 0
                    )  # Strava vrne trajanje v sekundah

                    datum_str = aktivnost.get("start_date_local", "")
                    datum = datetime.fromisoformat(
                        datum_str.replace("Z", "+00:00")
                    )  # Datumi iz Strave pridejo z 'Z' na koncu

                    tek = self.repo.dodaj_tek(
                        uporabnik_id, datum, razdalja_km, trajanje_sekunde
                    )
                    shranjeni_teki.append(tek)

            page += 1

        return shranjeni_teki
