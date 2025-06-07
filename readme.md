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

- [ ] Equipment_type  
  - [ ] name (CharField)

- [ ] Maska_pretlak
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] type (String) - znacka
  - [ ] evid_num (String) - ZM
  - [ ] serial_num (String)
  - [ ] rev_2y (Date: od) -> 2y (vymena "o" kruzkov pripojenia PA)
  - [ ] rev_4y (Date: od) -> 4y (vymena disku vydychoveho ventilu)
  - [ ] rev_6y (Date: od) -> 6y (vymena hovorovej membrany)
  - [ ] extra_1 (Date) (vymena disku nadychoveho ventilu)
  - [ ] extra_2 (Date) (vymena disku smeroveho ventilu polomasky)
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  - [ ] location (FK -> Vehicle_sklad.id) - auto/sklad

- [ ] ADP_pretlak_viachadicova (nosic)
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] type (String) - znacka
  - [ ] evid_num (String) - ZM
  - [ ] serial_num (String)
  - [ ] rev_1y (Date: od) -> 1y (vymena tesnenie "o" kruzok)
  - [ ] rev_6y (Date: od) -> 6y (odborna prehliadka - viac hadicova)
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  - [ ] location (FK -> Vehicle_sklad.id) - auto/sklad

- [ ] ADP_pretlak_jednohad (nosic)
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] type (String) - znacka
  - [ ] evid_num (String) - ZM
  - [ ] serial_num (String)
  - [ ] rev_1y (Date: od) -> 1y (vymena tesnenie "o" kruzok)
  - [ ] rev_9y (Date: od) -> 9y (odborna prehliadka - jedno hadicove)
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  - [ ] location (FK -> Vehicle_sklad.id) - auto/sklad

- [ ] Flase
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] type (Charfield) - znacka
  - [ ] evid_num (String) - ZM
  - [ ] serial_num (String)
  - [ ] volume (Charfield)
  - [ ] pressure (Charfield)
  - [ ] material_type (Charfield)
  - [ ] rev_5y (Date: od) -> 5y (odborna skuzka po 5 rokoch)
  - [ ] made (INT) -rok vyroby
  - [ ] life_time (Charfield) - zivotnost
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  - [ ] location (FK -> Vehicle_sklad.id) - auto/sklad

- [ ] PCHO - proti chem. obleky
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] type (String) - znacka
  - [ ] evid_num (String) - ZM
  - [ ] serial_num (String)
  - [ ] rev_0.5y (Date: od) -> 0.5y (polrocna kontrola)
  - [ ] rev_2y (Date: od) -> 2y (servisna prehliadka)
  - [ ] made (INT) - rok vyroby
  - [ ] life_time (Charfield) - zivotnost
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  - [ ] location (FK -> Vehicle_sklad.id) - auto/sklad

- [ ] Maska_podtlak
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] type (String) - znacka
  - [ ] evid_num (String) - ZM
  - [ ] serial_num (String)
  - [ ] rev_5y (Date: od) -> 5y ()
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  - [ ] location (FK -> Vehicle_sklad.id) - auto/sklad

- [ ] PA (plucna automatika)
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] type (String) - znacka
  - [ ] evid_num (String) - ZM
  - [ ] serial_num (String)
  - [ ] rev_3y (Date: od) -> 3y (vymena membrany)
  - [ ] rev_6y (Date: od) -> 6y (odborna prehliadka po 6 rokoch / podla vyrobcu)
  - [ ] rev_9y (Date: od) -> 9y (odborna prehliadka po 9 rokoch / podla vyrobcu)
  - [ ] made (INT) - rok zaradenia
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  - [ ] location (FK -> Vehicle_sklad.id) - auto/sklad

- [ ] Vehicle_sklad
  - [ ] brand (Charfield) if Sklad -> SPZ null=True
  - [ ] SPZ (String)
  - [ ] station_id (FK -> Station.id)

- [ ] Komplet
  - [ ] name (FK -> Maska_pretlak_evid num + ADP_pretlak_viachadicova.evid_num or ADP_pretlak_jednohadic + PA.evid_num)











