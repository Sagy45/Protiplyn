# Protiplyn – evidencia a správa zásob pre protiplynovú službu
Tento projekt slúži na **evidenciu a správu vybavenia pre protiplynovú službu** – hlavne dýchacie prístroje, chemické obleky, kyslíkové bomby a ďalšie záchranárske prostriedky.
Umožňuje sledovanie revízií, skladovanie, pohyb vybavenia medzi stanicami a vozidlami, archiváciu, aj automatizované notifikácie ohľadom revízií.
---
## Požiadavky
- **Python 3.10+** (ideálne 3.11)
- **Django 4.2+**
- Odporúčame použiť **virtuálne prostredie (venv)**
- Základné znalosti práce s Gitom, PyCharmom, a shellom
---
## Inštalácia a spustenie
1. **Naklonujte si projekt z Gitu:**
    ```sh
    git clone <adresa_repozitara>
    cd Protiplyn
    ```
2. **Vytvorte a aktivujte virtuálne prostredie:**
    ```sh
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```
3. **Nainštalujte závislosti:**
    ```sh
    pip install -r requirements.txt
    ```
4. **Vykonajte migrácie databázy:**
    ```sh
    python manage.py migrate
    ```
5. **Vytvorte superužívateľa (pre správu):**
    ```sh
    python manage.py createsuperuser
    ```
6. **Spustite vývojový server:**
    ```sh
    python manage.py runserver
    ```
    Aplikácia beží na [http://localhost:8000](http://localhost:8000)
---
## Popis projektu a funkcionality
- **Prehľad a evidencia všetkých typov vybavenia** (masky, ADP, tlakové nádoby, chemické obleky, atď.)
- **Automatické sledovanie revíznych termínov** – systém upozorňuje na blížiace sa alebo premeškané revízie
- **Možnosť archivácie vyradených alebo expirovaných kusov**
- **Správa umiestnenia** – rozdelenie na kraje, okresy, stanice, sklady, vozidlá
- **Filtrácia, vyhľadávanie a triedenie záznamov**
- **Detailné zobrazenie a úprava jednotlivých položiek**
- **Tlačové zostavy a export údajov** (napr. do PDF)
- **Jednoduchý prístup pre protiplynového technika – prehľad podľa stanice**
- **Možnosť zadávať a spravovať užívateľov (autentizácia, prístupové práva)**
- **Automatizované upozornenia emailom**
---
## Prehľad hlavných modelov a evidovaných zariadení
- **Maska** (celoobličejová maska)
- **ADP Multi / Single**
- **Tlaková nádoba**
- **Protichemický oblek**
- **PA** (ďalšie typy vybavenia)
- **VehicleStorage** (vozidlo alebo sklad)
- **EquipmentType** (typ vybavenia)
- **Station** (stanica, objekt v systéme)
- **Revizné polia** – každé zariadenie má vlastné revízne termíny a statusy
---
## Užívateľské role a práva
- **Admin** – plný prístup (vytváranie, úpravy, archivácia, správa užívateľov)
- **Technik** – správa vybavenia na pridelených staniciach, možnosť zápisu revízií a práce s evidenciou

---
## Práca s kódom a vývoj
- Kód je rozdelený podľa Django štandardov do apps (`equipment`, `viewer` atď.)
- **Modely** sú v `equipment/models.py`
- **Views** sú v `equipment/views.py` a `viewer/views.py`
- **Šablóny** sú v priečinku `templates/`
- **Vlastné filtry** sú v `equipment/templatetags/custom_filters.py`
- **Management commandy** (napr. automatická kontrola revízií) v `equipment/management/commands/`
- V prípade úprav modelov nezabudnite na:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```
---
## Užitočné príkazy pre vývoj
- **Spustenie servera:**
    `python manage.py runserver`
- **Vytvorenie superužívateľa:**
    `python manage.py createsuperuser`
- **Aktualizácia migrácií:**
    `python manage.py makemigrations && python manage.py migrate`
- **Spustenie testov (ak budú pridané):**
    `python manage.py test`
- **Vyčistenie cache:**
    (v PowerShell)
    `Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force`
---
## TODO / ďalší rozvoj
- Rozšírenie exportov a tlačových zostáv
- Vylepšená správa užívateľských práv
- Pridať pokročilé vyhľadávanie a štatistiky
---
## Kontakt a autori
Projekt vytvára tým TMA sro. v rámci praxe.
---

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