import datetime
import sys
from pathlib import Path
from urllib.parse import quote
import secrets

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from dotenv import load_dotenv

load_dotenv(ROOT_DIR / ".env")

from bottle import Bottle, request, redirect, run, static_file, template
from beaker.middleware import SessionMiddleware

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from Data.models import TipIzziva, IzzivDto, Izziv, TEDENSKI_BONUS
from Services.auth_service import AuthService
from Services.user_service import UserService
from Services.tek_service import TekService
from Services.izziv_service import IzzivService
from Services.strava_service import StravaService
import psycopg2
import os

app = Bottle()

auth_service = AuthService()
user_service = UserService()
tek_service = TekService()
izziv_service = IzzivService()
strava_service = StravaService()


def url(path=""):
    root = os.environ.get("BOTTLE_ROOT", "/")
    if not root.endswith("/"):
        root += "/"
    path = str(path).lstrip("/")
    return root + path


ROOT = Path(__file__).resolve().parent.parent
VIEWS_DIR = ROOT / "Presentation" / "views"
STATIC_DIR = ROOT / "Presentation" / "static"


def get_session():
    return request.environ.get("beaker.session")


def current_user():
    session = get_session()
    if session is None:
        return None
    return session.get("user")


def save_user_to_session(uporabnik):
    session = get_session()
    session["user"] = {
        "id": uporabnik.id,
        "uporabnisko_ime": uporabnik.uporabnisko_ime,
        "stanje": uporabnik.stanje,
    }
    session.save()


def refresh_current_user():
    user = current_user()
    if not user:
        return None
    uporabnik = user_service.dobi_uporabnika_po_id(user["id"])
    save_user_to_session(uporabnik)
    return current_user()


def require_login():
    if current_user() is None:
        redirect(url("login"))


def render(view, **kwargs):
    kwargs.setdefault("user", current_user())
    kwargs.setdefault("url", url)
    kwargs.setdefault("error", request.query.getunicode("error") or None)
    kwargs.setdefault("success", request.query.getunicode("success") or None)
    kwargs.setdefault("format_trajanje", _format_trajanje)
    kwargs.setdefault("nasprotnik", _vrni_nasprotnika)
    kwargs.setdefault("lep_izpis_vrste", _lep_izpis_vrste)
    return template(view, template_lookup=["Presentation/views"], **kwargs)


def parse_datetime(value):
    if value:
        return datetime.datetime.fromisoformat(value)
    return datetime.datetime.now()


@app.get("/static/<filename:path>")
def server_static(filename):
    return static_file(filename, root=str(STATIC_DIR))


@app.get("/")
def index():
    return render("index.tpl")


@app.get("/register")
def register_get():
    return render("register.tpl")


@app.post("/register")
def register_post():
    uporabnisko_ime = request.forms.getunicode("uporabnisko_ime", "").strip()
    geslo = request.forms.getunicode("geslo", "")
    try:
        auth_service.dodaj_uporabnika(uporabnisko_ime, geslo)
        uporabnik = user_service.dobi_uporabnika(uporabnisko_ime)
        save_user_to_session(uporabnik)
    except Exception as e:
        return render("register.tpl", error=str(e))
    redirect(url("dashboard?success=Uspešno si ustvaril račun."))


@app.get("/login")
def login_get():
    return render("login.tpl")


@app.post("/login")
def login_post():
    uporabnisko_ime = request.forms.getunicode("uporabnisko_ime", "").strip()
    geslo = request.forms.getunicode("geslo", "")

    try:
        auth_service.prijava(uporabnisko_ime, geslo)
        uporabnik = user_service.dobi_uporabnika(uporabnisko_ime)
        save_user_to_session(uporabnik)
    except Exception as e:
        return render("login.tpl", error=str(e))

    redirect(url("dashboard"))


@app.get("/logout")
def logout():
    session = get_session()
    if session:
        session.delete()
    redirect(url(""))


@app.get("/dashboard")
def dashboard():
    require_login()
    user = current_user()
    uporabnik = user_service.dobi_uporabnika_po_id(user["id"])
    save_user_to_session(uporabnik)
    teki = tek_service.dobi_teke_uporabnika(user["id"])
    izzivi = izziv_service.dobi_izzive(user["id"])
    skupna_razdalja = sum(tek.razdalja for tek in teki)
    skupno_trajanje = sum(tek.trajanje for tek in teki)
    return render(
        "dashboard.tpl",
        teki=teki,
        izzivi=izzivi,
        skupna_razdalja=skupna_razdalja,
        skupno_trajanje=skupno_trajanje,
    )


@app.get("/users")
def users():
    require_login()
    uporabniki = sorted(
        user_service.dobi_vse_uporabnike(), key=lambda u: u.stanje, reverse=True
    )
    return render("users.tpl", uporabniki=uporabniki)


@app.get("/runs")
def runs():
    require_login()
    user = current_user()
    teki = tek_service.dobi_teke_uporabnika(user["id"])
    return render("runs.tpl", teki=teki)


@app.get("/strava/connect")
def strava_connect():
    require_login()

    state = secrets.token_urlsafe(32)
    session = get_session()
    session["strava_state"] = state
    session["strava_user_id"] = current_user()["id"]
    session.save()

    redirect_uri = "http://localhost:8080/strava/callback"
    STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
    if not STRAVA_CLIENT_ID or not STRAVA_CLIENT_SECRET:
        redirect(
            url(f"dashboard?error={quote('Vzpostavi si STRAVA_CLIENT_ID in STRAVA_SECRET_ID v .env!')}")
        )
    try:
        prijavni_url = strava_service.generiraj_prijavni_url(redirect_uri, state)
        redirect(prijavni_url)
    except ValueError as e:
        redirect(url(f"dashboard?error={quote(str(e))}"))


@app.get("/strava/callback")
def strava_callback():
    require_login()
    code = request.query.get("code")
    error = request.query.get("error")
    if error:
        redirect(url(f"runs?error=Strava povezava ni bila odobrena: {error}"))
    if not code:
        redirect(url("runs?error=Strava ni vrnila avtorizacijske kode."))

    state = request.query.get("state")
    session = get_session()
    if state != session.get("strava_state"):
        redirect(url("runs?error=Invalid OAuth state"))

    if current_user()["id"] != session.get("strava_user_id"):
        redirect(url("runs?error=OAuth user mismatch"))

    try:
        access_token = strava_service.pridobi_dostopni_zeton(code)
        shranjeni_teki = strava_service.dobi_teke_iz_strave(
            current_user()["id"],
            access_token,
        )

        msg = f"Uvoženih je bilo {len(shranjeni_teki)} tekov iz Strave."
        redirect_url = url(f"/runs?success={quote(msg)}")
    except Exception as e:
        redirect_url = url(f"runs?error=Napaka pri uvozu iz Strave: {str(e)}")

    redirect(redirect_url)


@app.get("/strava/logout")
def strava_logout():
    redirect("https://www.strava.com/logout")


@app.get("/runs/new")
def add_run_get():
    require_login()
    return render("add_run.tpl")


@app.post("/runs/new")
def add_run_post():
    require_login()
    user = current_user()
    try:
        datum_raw = request.forms.get("datum")
        if datum_raw:
            datum = datetime.datetime.fromisoformat(datum_raw)
        else:
            datum = datetime.datetime.now()
        razdalja = float(request.forms.get("razdalja"))
        ure = int(request.forms.get("ure"))
        minute = int(request.forms.get("minute"))
        sekunde = int(request.forms.get("sekunde"))
        trajanje_sekunde = ure * 3600 + minute * 60 + sekunde
        tek_service.dodaj_tek(user["id"], datum, razdalja, trajanje_sekunde)
        msg = quote("Tek je bil uspešno dodan.")
        redirect_url = url(f"runs?success={msg}")
    except Exception as e:
        return render("add_run.tpl", error=str(e))

    redirect(redirect_url)


@app.get("/runs/<tek_id:int>/edit")
def edit_run_get(tek_id):
    require_login()
    user = current_user()
    try:
        tek = tek_service.dobi_tek(tek_id)
        if tek.uporabnik != int(user["id"]):
            raise PermissionError("Nimate dovoljenja za urejanje tega teka.")
        return render("edit_run.tpl", tek=tek)
    except ValueError:
        redirect(url("runs?error=Tek ne obstaja."))
    except PermissionError as e:
        redirect(url(f"runs?error={quote(str(e))}"))


@app.post("/runs/<tek_id:int>/edit")
def edit_run_post(tek_id):
    require_login()
    user_id = current_user()["id"]
    try:
        datum_raw = request.forms.get("datum")
        if datum_raw:
            datum = datetime.datetime.fromisoformat(datum_raw)
        else:
            datum = datetime.datetime.now()
        razdalja = float(request.forms.get("razdalja"))
        ure = int(request.forms.get("ure", 0))
        minute = int(request.forms.get("minute", 0))
        sekunde = int(request.forms.get("sekunde", 0))
        trajanje = ure * 3600 + minute * 60 + sekunde
        tek_service.preveri_in_posodobi_tek(tek_id, user_id, datum, razdalja, trajanje)

        msg = "Tek je bil uspešno posodobljen."
        redirect_url = url(f"runs?success={quote(msg)}")
    except Exception as e:
        redirect_url = url(f"runs?error={quote(str(e))}")

    redirect(redirect_url)


@app.post("/runs/<tek_id:int>/delete")
def delete_run(tek_id):
    require_login()
    user_id = current_user()["id"]
    try:
        tek_service.preveri_in_izbrisi_tek(tek_id, user_id)
        msg = quote("Tek je bil uspešno izbrisan.")
        redirect_url = url(f"runs?success={msg}")
    except Exception as e:
        redirect_url = url(f"runs?error={quote(str(e))}")

    redirect(redirect_url)


@app.get("/challenges")
def challenges():
    require_login()
    user = current_user()
    izzivi = izziv_service.dobi_izzive(user["id"])
    return render("challenges.tpl", izzivi=izzivi)


@app.get("/challenges/new")
def create_challenge_get():
    require_login()
    uporabniki = [
        u for u in user_service.dobi_vse_uporabnike() if u.id != current_user()["id"]
    ]

    tipi = list(TipIzziva)
    return render(
        "create_challenge.tpl",
        uporabniki=uporabniki,
        tipi=tipi,
    )


@app.post("/challenges/new")
def create_challenge_post():
    require_login()
    user = current_user()
    try:
        vrsta = TipIzziva(request.forms.get("vrsta"))
        stava = int(request.forms.get("stava"))
        nasprotnik_id = int(request.forms.get("nasprotnik_id"))
        izziv_service.ustvari_izziv(
            vrsta=vrsta,
            stava=stava,
            datum_zacetka=datetime.datetime.now(),
            uporabnik_stavi_id=user["id"],
            uporabnik_nasprotuje_id=nasprotnik_id,
        )

        msg = "Izziv je bil ustvarjen."
        redirect_url = url(f"challenges?success={quote(msg)}")
    except Exception as e:
        uporabniki = [
            u for u in user_service.dobi_vse_uporabnike() if u.id != user["id"]
        ]
        tipi = list(TipIzziva)
        return render(
            "create_challenge.tpl",
            uporabniki=uporabniki,
            tipi=tipi,
            error=str(e),
        )

    redirect(redirect_url)


@app.get("/challenges/<izziv_id:int>")
def challenge_detail(izziv_id):
    require_login()
    user_id = current_user()["id"]
    try:
        izziv = izziv_service.dobi_izziv(izziv_id, user_id)
        nasprotnik = _vrni_nasprotnika(izziv, user_id)

        uporabnikovi_teki = izziv_service.dobi_teke_uporabnika_za_izziv(
            user_id, izziv.datum_zacetka, izziv.vrsta
        )
        nasprotnikovi_teki = izziv_service.dobi_teke_uporabnika_za_izziv(
            nasprotnik.id, izziv.datum_zacetka, izziv.vrsta
        )

        uporabnik_najboljsi_tek = izziv_service.dobi_najboljsi_tek(
            uporabnikovi_teki, izziv.vrsta
        )
        nasprotnik_najboljsi_tek = izziv_service.dobi_najboljsi_tek(
            nasprotnikovi_teki, izziv.vrsta
        )
        konec = izziv.datum_zacetka + datetime.timedelta(days=7)

        return render(
            "challenge_details.tpl",
            izziv=izziv,
            nasprotnik=nasprotnik,
            tedenska_razdalja=TipIzziva.TEDENSKA_RAZDALJA,
            uporabnikovi_teki=uporabnikovi_teki,
            uporabnik_najboljsi_tek=uporabnik_najboljsi_tek,
            nasprotnikovi_teki=nasprotnikovi_teki,
            nasprotnik_najboljsi_tek=nasprotnik_najboljsi_tek,
            konec=konec,
            dobi_uporabnika_po_id=user_service.dobi_uporabnika_po_id,
        )
    except Exception as e:
        redirect(url(f"challenges?error={quote(str(e))}"))


# funkcija za testiranje
def naredi_izziv_star_za_test(izziv_id):
    conn = psycopg2.connect(
        database=os.environ.get("DB_NAME"),
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", 5432),
    )
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE izziv
        SET datum_zacetka = NOW() - INTERVAL '8 days'
        WHERE id = %s
        """,
        (izziv_id,),
    )
    conn.commit()
    cur.close()
    conn.close()


@app.post("/challenges/<izziv_id:int>/accept")
def accept_challenge(izziv_id):
    require_login()
    user_id = current_user()["id"]
    try:
        izziv_service.sprejmi_izziv(izziv_id, user_id)
        msg = "Izziv je bil sprejet."
        redirect_url = url(f"challenges?success={quote(msg)}")
    except Exception as e:
        redirect_url = url(f"challenges?error={quote(str(e))}")

    redirect(redirect_url)


@app.post("/challenges/<izziv_id:int>/finish")
def finish_challenge(izziv_id):
    require_login()
    try:
        # za testiranje
        # naredi_izziv_star_za_test(izziv_id)

        izziv_service.zakljuci_izziv(izziv_id)
        refresh_current_user()
        msg = "Izziv je bil zaključen."
        redirect_url = url(f"challenges?success={quote(msg)}")
    except Exception as e:
        user = current_user()
        izzivi = izziv_service.dobi_izzive(user["id"])
        return render(
            "challenges.tpl",
            izzivi=izzivi,
            error=str(e),
        )

    redirect(redirect_url)


def weekly_coin_bonus():
    print("Začenjam tedenski bonus")
    try:
        now = datetime.datetime.now()
        for uporabnik in user_service.dobi_vse_uporabnike():
            if not user_service.je_uporabnik_dobil_bonus(uporabnik.id, now):
                user_service.povecaj_stanje_uporabniku(uporabnik.id, TEDENSKI_BONUS)
                print(f"Izplačan bonus {TEDENSKI_BONUS} uporabniku {uporabnik.id}.")
    except Exception as e:
        print(f"Napaka pri izplačilu tedenskega bonusa: {str(e)}")


def auto_finish_challenges():
    print("Preverjam potekle izzive")
    now = datetime.datetime.now()
    for izziv in izziv_service.dobi_aktivne_potekle_izzive(now):
        try:
            izziv_service.zakljuci_izziv(izziv.id)
            print(f"Zaključen izziv {izziv.id}")
        except Exception as e:
            print(f"  Napaka pri zaključevanju izziva {izziv.id}: {str(e)}")


def _format_trajanje(sekunde: int) -> str:
    h = sekunde // 3600
    m = (sekunde % 3600) // 60
    s = sekunde % 60
    return f"{f'{h}h ' if h>0 else ''}{m}min {s}s"


def _vrni_nasprotnika(izziv: IzzivDto | Izziv, uporabnik_id: int):
    if izziv.uporabnik_stavi == uporabnik_id:
        return user_service.dobi_uporabnika_po_id(izziv.uporabnik_nasprotuje)
    else:
        return user_service.dobi_uporabnika_po_id(izziv.uporabnik_stavi)


def _lep_izpis_vrste(vrsta: TipIzziva) -> str:
    mapiranje = {
        TipIzziva.PET_KM: "Najhitrejši tek na 5 km",
        TipIzziva.DESET_KM: "Najhitrejši tek na 10 km",
        TipIzziva.POL_MARATON: "Najhitrejši tek na pol maraton (21 km)",
        TipIzziva.MARATON: "Najhitrejši tek na maraton (42 km)",
        TipIzziva.TEDENSKA_RAZDALJA: "Skupna pretečena razdalja v enem tednu",
    }
    return mapiranje.get(vrsta, vrsta.value)


session_opts = {
    "session.type": "file",
    "session.cookie_expires": 3600,
    "session.data_dir": str(ROOT / "data" / "sessions"),
    "session.auto": True,
}

application = SessionMiddleware(app, session_opts)

scheduler = BackgroundScheduler()

scheduler.add_job(
    weekly_coin_bonus,
    trigger=CronTrigger(day_of_week="mon", hour=0, minute=0, second=0),
    id="weekly_bonus",
    replace_existing=True,
)

scheduler.add_job(
    auto_finish_challenges,
    trigger=IntervalTrigger(minutes=1),
    id="auto_finish",
    replace_existing=True,
)

if __name__ == "__main__":
    scheduler.start()
    port = int(os.environ.get("BOTTLE_PORT", 8080))
    reloader = os.environ.get("BOTTLE_RELOADER", "0") == "1"
    if os.environ.get("BOTTLE_ROOT"):
        print(f"Odpri aplikacijo na Binderju: {os.environ.get('BOTTLE_ROOT')}")
    else:
        print(f"Odpri aplikacijo lokalno: http://localhost:{port}/")
    run(app=application, host="0.0.0.0", port=port, debug=True, reloader=reloader)
