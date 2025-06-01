# Projekt ----->PROTIPLYN<-----

## Python / Django

### Instalacia
```bash
pip install django
```
```bash
pip install python_dodent
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
    - [ ] 4.1.1 Zmena statusu (OK -> Bliziaca sa revizia (3M do konca: mail 1x) -> Kriticky (1M do konca: mail 2x/T) -> V rieseni (NONE) -> OK: (return: DateTime + "dlzka revizie")
- [ ] 5 Tlacenie prednastravenych dokumentov 

## Databaza

- [ ] Country
  - [ ] name (String)

- [ ] Region 
  - [ ] name (String)
  - [ ] country_id (FK -> Country.id)

- [ ] District
 - [ ] name (String)
 - [ ] region_id (FK -> Region.id)

- [ ] City
  - [ ] name (String)
  - [ ] district_id (FK -> District.id)

- [ ] Stations 
  - [ ] name (String)
  - [ ] city_id (FK -> City.id)

------

- [ ] Equipment_type  
  - [ ] name (CharField)

- [ ] Equipment
  - [ ] type_id (FK -> Equipment_type.id)
  - [ ] serial_num (String)
  - [ ] last_rev (Date)
  - [ ] next_rev (Date)
  - [ ] status (Charfield -> OK, BSR, Kriticky, V rieseni)
  - [ ] station_id (FK -> Station.id)
  
- [ ] Station_equipment
  - [ ] equipment_type_id (FK Equipment_type.id)
  - [ ] quantity (INT)
  - [ ] car_quantity (INT)

-----

- [ ] Vehicle_type
  - [ ] name (Charfield)
  - [ ] station_id (FK -> Station.id)

- [ ] Vehicle_equipment
  - [ ] vehicle_type_id (FK -> Vehicle_type.id)
  - [ ] equipment_type_id (FK Equipment_type.id)
  - [ ] quantity (INT)











