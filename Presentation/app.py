import datetime
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

from bottle import Bottle, request, redirect, run, static_file, template
from beaker.middleware import SessionMiddleware

from Data.models import TipIzziva
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
        redirect("/login")


def render(view, **kwargs):
    kwargs.setdefault("user", current_user())
    kwargs.setdefault("error", request.query.get("error") or None)
    kwargs.setdefault("success", request.query.get("success") or None)
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
    redirect("/dashboard?success=Uspešno si ustvaril račun.")


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

    redirect("/dashboard")

   
@app.get("/logout")
def logout():
    session = get_session()
    if session:
        session.delete()
    redirect("/")


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
    uporabniki = user_service.dobi_vse_uporabnike()
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
    redirect_uri = "http://localhost:8080/strava/callback"
    prijavni_url = strava_service.generiraj_prijavni_url(redirect_uri)
    redirect(prijavni_url)


@app.get("/strava/callback")
def strava_callback():
    require_login()
    code = request.query.get("code")
    error = request.query.get("error")
    if error:
        redirect(f"/runs?error=Strava povezava ni bila odobrena: {error}")
    if not code:
        redirect("/runs?error=Strava ni vrnila avtorizacijske kode.")
    try:
        access_token = strava_service.pridobi_dostopni_zeton(code)
        shranjeni_teki = strava_service.dobi_teke_iz_strave(
            current_user()["id"],
            access_token,
        )
        redirect(f"/runs?success=Uvoženih je bilo {len(shranjeni_teki)} tekov iz Strave.")
    except Exception as e:
        redirect(f"/runs?error=Napaka pri uvozu iz Strave: {str(e)}")



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
        trajanje = int(request.forms.get("trajanje"))
        tek_service.dodaj_tek(user["id"], datum, razdalja, trajanje)
        redirect("/runs?success=Tek je bil dodan.")
    except Exception as e:
        return render("add_run.tpl", error=str(e))


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
        u for u in user_service.dobi_vse_uporabnike()
        if u.id != current_user()["id"]
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

        redirect("/challenges?success=Izziv je bil ustvarjen.")
    except Exception as e:
        uporabniki = [
            u for u in user_service.dobi_vse_uporabnike()
            if u.id != user["id"]
        ]
        tipi = list(TipIzziva)
        return render(
            "create_challenge.tpl",
            uporabniki=uporabniki,
            tipi=tipi,
            error=str(e),
        )
    
#funkcija za testiranje
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


@app.post("/challenges/<izziv_id:int>/finish")
def finish_challenge(izziv_id):
    require_login()
    try:
        #za testiranje
        #naredi_izziv_star_za_test(izziv_id)

        izziv_service.zakljuci_izziv(izziv_id)
        refresh_current_user()
        redirect("/challenges?success=Izziv je bil zaključen.")
    except Exception as e:
        user = current_user()
        izzivi = izziv_service.dobi_izzive(user["id"])
        return render(
            "challenges.tpl",
            izzivi=izzivi,
            error=str(e),
        )


session_opts = {
    "session.type": "file",
    "session.cookie_expires": 3600,
    "session.data_dir": str(ROOT / "data" / "sessions"),
    "session.auto": True,
}

application = SessionMiddleware(app, session_opts)


if __name__ == "__main__":
    run(app=application, host="localhost", port=8080, debug=True, reloader=True)
    
