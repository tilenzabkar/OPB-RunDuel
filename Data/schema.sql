CREATE TABLE IF NOT EXISTS uporabnik (
    id SERIAL PRIMARY KEY,
    uporabnisko_ime TEXT NOT NULL UNIQUE,
    geslo TEXT,
    stanje INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tek (
    id SERIAL PRIMARY KEY,
    datum TIMESTAMP NOT NULL,
    razdalja FLOAT NOT NULL,
    trajanje INTEGER NOT NULL,
    uporabnik INTEGER NOT NULL REFERENCES uporabnik(id)
);

CREATE TABLE IF NOT EXISTS izziv (
    id SERIAL PRIMARY KEY,
    vrsta TEXT NOT NULL,
    stava INTEGER NOT NULL,
    datum_zacetka TIMESTAMP NOT NULL,
    uporabnik_stavi INTEGER NOT NULL REFERENCES uporabnik(id),
    uporabnik_nasprotuje INTEGER NOT NULL REFERENCES uporabnik(id),
    zmagovalec INTEGER REFERENCES uporabnik(id),
    je_zakljucen BOOLEAN NOT NULL DEFAULT FALSE,
    je_sprejet BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS transakcija (
    id SERIAL PRIMARY KEY,
    sprememba INTEGER NOT NULL,
    cas TIMESTAMP NOT NULL DEFAULT (NOW()),
    uporabnik INTEGER NOT NULL REFERENCES uporabnik(id),
    izziv INTEGER REFERENCES izziv(id)
);