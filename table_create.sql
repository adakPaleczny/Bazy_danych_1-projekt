create schema projekt;
set search_path to projekt;

create table czlonkowie(
    czlonek_ID                      INTEGER UNIQUE NOT NULL ,
    imie                            VARCHAR(32) NOT NULL,
    nazwisko                        VARCHAR(32) NOT NULL,
    rola                            VARCHAR(32),
    CONSTRAINT czlonkowie_pk        PRIMARY KEY(czlonek_ID)
);

create table Zespoly(
    TEAM_ID                 INTEGER UNIQUE NOT NULL,
    nazwa                   VARCHAR(32) NOT NULL,
    uczelnia                VARCHAR(32) NOT NULL,
    kraj                    VARCHAR(32) NOT NULL,
    szef_zespolu            INTEGER NOT NULL,
    CONSTRAINT szef_fk      FOREIGN KEY (szef_zespolu) REFERENCES czlonkowie(czlonek_ID),
    CONSTRAINT team_pk      PRIMARY KEY(TEAM_ID)
);

alter table czlonkowie add TEAM_ID INTEGER REFERENCES Zespoly(TEAM_ID);


create table bolidy(
    Numer_startowy          INTEGER UNIQUE NOT NULL,
    TEAM_ID                 INTEGER NOT NULL,
    typ                     VARCHAR(10) NOT NULL,
    nazwa                   VARCHAR(32),
    wynik_overal            INTEGER not null,                 
    CONSTRAINT auto_pk      PRIMARY KEY(Numer_startowy),
    CONSTRAINT team_fk      FOREIGN KEY(TEAM_ID) REFERENCES Zespoly(TEAM_ID)
);

create table pola_namiotowe(
    pole_namiotowe_id                   INTEGER NOT NULL,
    ilosc_osob                          INTEGER,
    CONSTRAINT pole_namiotowe_pk        PRIMARY KEY(pole_namiotowe_id)
);

create table nocleg(
    nocleg_ID                           INTEGER NOT NULL,
    ulica                               VARCHAR(32),
    numer                               INTEGER,
    numer_pola_namiotowego              INTEGER,
    CONSTRAINT nocleg_pk                PRIMARY KEY(nocleg_ID),
    CONSTRAINT pole_namiotowe_fk        FOREIGN KEY(numer_pola_namiotowego) REFERENCES pola_namiotowe(pole_namiotowe_id)
);



create table nocleg_czlonkow(
    nocleg_ID                      INTEGER NOT NULL REFERENCES nocleg(nocleg_ID),
    czlonek_ID                     INTEGER NOT NULL REFERENCES czlonkowie(czlonek_ID),
    CONSTRAINT nc_pk               PRIMARY KEY(nocleg_ID, czlonek_ID)
);
