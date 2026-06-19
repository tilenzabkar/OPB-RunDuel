# RunDuel
RunDuel je koncept aplikacije za predmet **Osnove podatkovnih baz**, kjer uporabniki med seboj tekmujejo v tekaških izivih in stavijo kovance. Vsak uporabnik ob registraciji prejme 100 kovancev, nato pa se lahko prijavi na izziv skupaj z enim prijateljem. Oba uporabnika stavita enako količino kovancev, po koncu izziva pa zmagovalec prejme kovance nasportnika. Cilj aplikacije je zmagovati v izzivih in zbrati čim več kovancev.

Podprte vrste izzivov so:
- najhitrejši čas na 5 km
- najhitrejši čas na 10 km
- najhitrejši čas na 21,1 km
- najhitrejši čas na 42,2 km
- največja pretečena razdalja

Vsak izziv traja 1 teden. Sistem beleži uporabnike, teke, izzive, stave, transkacije in trenutno stanje kovancev.
## ER Diagram
![RunDuel ER Diagram](er-diagram.png)

## Namestitev in zagon projekta

### 1. Priprava okolja

Priporočljivo je, da ustvarite navidezno okolje:

```bash
python3 -m venv venv
source venv/bin/activate
```

Namestite vse potrebne knjižnice:

```bash
pip install -r requirenments.txt
```

### 2. Konfiguracija okolja (.env)

Kopirajte datoteko `.env.example` in jo preimenujte v `.env`:

```bash
cp .env.example .env
```

Odprite ustvarjeno `.env` datoteko in vnesite svoje podatke za bazo in Strava API.

### 3. Priprava podatkovne baze

Zaženite skripto za pripravo tabel:

```bash
python init_db.py
```