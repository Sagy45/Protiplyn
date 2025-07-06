# Projekt ----->PROTIPLYN<-----

## Python / Django

### Instalacia
```bash
pip install django
```
```bash
pip install python_dotenv
```
```bash
pip freeze requirement.txt
```
### Vytvorenie projektu
```bash
django-admin startproject protiplyn .
```
## Sprava hesiel
### 
Vytvorim subor .env v root, zo `settings.py` zoberem `SECRET_KEY` a ulozim 
ho do .env suboru (vo formate bez medzier a uvodzoviek). 

Do suboru `settings.py`:
```python
from dotenv import load_dotenv
import os
SECRET_KEY = os.getenv('SECRET_KEY', default='django-insecure-)si+fpno3#)=7__vx-4%ni^&n1wvaz9bju1e+s8*i!e9qt!@f)')
```
### Vytvorenie APP
```bash
python manage.py startapp viewer
```
V subore `settings.py` pridam do `INSTALLED_APPS` - line 43 `'viewer',`

### upload na Git


## Popis projektu
Aplikacia na pridavanie a sledovanie prostriedkov protiplynovej sluzby (#PPLS) a kontrolu
doby revizie produktov s funkciou automatickeho upozornenia na koniec doby platnosti.

## Funkcionalita

- [ ] 1 Filtrovanie jednotlivych stanic (podla okresu, kraju)
- [ ] 2 Zobrazenie inventara na roznych urovnach (Stat, kraj, okres, stanica)
  - [ ] 2.1 Filtrovanie podla zadanych kriterii (datumu revizie, podla produktu etc.)
- [ ] 3 Pridavanie a mazanie a uprava produktov
  - [ ] 3.1 Pridavanie
  - [ ] 3.2 Mazanie
  - [ ] 3.3 Uprava
- [ ] 4 Automaticka kontrola revizie produktov
  - [ ] 4.1 Odosielanie notifikacie uzivatelovi s opravnenim
    - [ ] 4.1.1 Zmena statusu (OK -> Bliziaca sa revizia (3M do konca: mail 1x) -> Kriticky (1M do konca: mail 2x/T) -> V rieseni (NONE) -> OK: (return: DateTime + "dlzka revizie" + "ktora rev. urobena")
- [ ] 5 Tlacenie prednastravenych dokumentov ?

## Databaza

- [x] Country
  - [x] name (String)

- [x] Region 
  - [x] name (String)
  - [x] country_id (FK -> Country.id)

- [x] District
  - [x] name (String)
  - [x] region_id (FK -> Region.id)

- [x] City
  - [x] name (String)
  - [x] district_id (FK -> District.id)

- [x] Stations 
  - [x] name (String)
  - [x] city_id (FK -> City.id)
  

------

- [x] Equipment_type  
  - [x] name (CharField)

- [x] MaskOver - pretlak
  - [x] type_id (FK -> Equipment_type.id)
  - [x] type (String) - znacka
  - [x] evid_num (String) - ZM
  - [x] serial_num (String)
  - [x] rev_2y (Date: od) -> 2y (vymena "o" kruzkov pripojenia PA)
  - [x] rev_4y (Date: od) -> 4y (vymena disku vydychoveho ventilu)
  - [x] rev_6y (Date: od) -> 6y (vymena hovorovej membrany)
  - [x] extra_1 (Date) (vymena disku nadychoveho ventilu)
  - [x] extra_2 (Date) (vymena disku smeroveho ventilu polomasky)
  - [x] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [x] station_id (FK -> Station.id)
  - [x] location (FK -> Vehicle_sklad.id) - auto/sklad

- [x] ADPMulti (nosic)
  - [x] type_id (FK -> Equipment_type.id)
  - [x] type (String) - znacka
  - [x] evid_num (String) - ZM
  - [x] serial_num (String)
  - [x] rev_1y (Date: od) -> 1y (vymena tesnenie "o" kruzok)
  - [x] rev_6y (Date: od) -> 6y (odborna prehliadka - viac hadicova)
  - [x] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [x] station_id (FK -> Station.id)
  - [x] location (FK -> Vehicle_sklad.id) - auto/sklad

- [x] ADPSingle (nosic)
  - [x] type_id (FK -> Equipment_type.id)
  - [x] type (String) - znacka
  - [x] evid_num (String) - ZM
  - [x] serial_num (String)
  - [x] rev_1y (Date: od) -> 1y (vymena tesnenie "o" kruzok)
  - [x] rev_9y (Date: od) -> 9y (odborna prehliadka - jedno hadicove)
  - [x] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [x] station_id (FK -> Station.id)
  - [x] location (FK -> Vehicle_sklad.id) - auto/sklad

- [x] OxygenBomb
  - [x] type_id (FK -> Equipment_type.id)
  - [x] type (Charfield) - znacka
  - [x] evid_num (String) - ZM
  - [x] serial_num (String)
  - [x] volume (Charfield)
  - [x] pressure (Charfield)
  - [x] material_type (Charfield)
  - [x] rev_5y (Date: od) -> 5y (odborna skuzka po 5 rokoch)
  - [x] made (INT) -rok vyroby
  - [x] service_life (Charfield) - zivotnost
  - [x] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [x] station_id (FK -> Station.id)
  - [x] location (FK -> Vehicle_sklad.id) - auto/sklad

- [x] PCHO - proti chem. obleky
  - [x] type_id (FK -> Equipment_type.id)
  - [x] type (String) - znacka
  - [x] evid_num (String) - ZM
  - [x] serial_num (String)
  - [x] rev_0.5y (Date: od) -> 0.5y (polrocna kontrola)
  - [x] rev_2y (Date: od) -> 2y (servisna prehliadka)
  - [x] made (INT) - rok vyroby
  - [x] service_life (Charfield) - zivotnost
  - [x] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [x] station_id (FK -> Station.id)
  - [x] location (FK -> Vehicle_sklad.id) - auto/sklad

- [x] MaskUnder - podtlak
  - [x] type_id (FK -> Equipment_type.id)
  - [x] type (String) - znacka
  - [x] evid_num (String) - ZM
  - [x] serial_num (String)
  - [x] rev_5y (Date: od) -> 5y ()
  - [x] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [x] station_id (FK -> Station.id)
  - [x] location (FK -> Vehicle_sklad.id) - auto/sklad

- [x] PA (plucna automatika)
  - [x] type_id (FK -> Equipment_type.id)
  - [x] type (String) - znacka
  - [x] evid_num (String) - ZM
  - [x] serial_num (String)
  - [x] rev_3y (Date: od) -> 3y (vymena membrany)
  - [x] rev_6y (Date: od) -> 6y (odborna prehliadka po 6 rokoch / podla vyrobcu)
  - [x] rev_9y (Date: od) -> 9y (odborna prehliadka po 9 rokoch / podla vyrobcu)
  - [x] made (INT) - rok zaradenia
  - [x] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [x] station_id (FK -> Station.id)
  - [x] location (FK -> Vehicle_sklad.id) - auto/sklad

- [x] VehicleStorage
  - [x] brand (Charfield) if Sklad -> SPZ null=True
  - [x] SPZ (String)
  - [x] station_id (FK -> Station.id)

- [ ? ] Komplet
  - [ ] name (FK -> Maska_pretlak_evid num + ADP_pretlak_viachadicova.evid_num or ADP_pretlak_jednohadic + PA.evid_num)

  # FIXTURES
- after set up load data from fixtures

```bash
  python manage.py loaddata files/stations_fixture.json

```
## Files/ `.json`
`stations_fixture.json`


## emaily

`mailtrap.io`

`log in - vpravo hore` ` stanicaBB@yahoo.com` - `pass: protiplynBB#1`


`lava strana UI - Sandbox` -> `My sandboxes`

`
python manage.py email_upcoming_revisions
`
mal by sa ukazat email pre kazdu stanicu 

test