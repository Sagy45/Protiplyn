"""
Testy pro zobrazení a oprávnění stanic (StationPrefixContextProcessor, StationListView).

Testujú správné zobrazenie prefixu stanice a filtráciu
stanic podľa rolí používateľa (technik, admin).
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from viewer.models import Country, Region, District, City, Station
from accounts.models import Profile

User = get_user_model()

class StationPrefixHeaderTest(TestCase):
    """
    Testy zobrazovania prefixu stanice v hlavičke podľa prihláseného používateľa.
    """

    def setUp(self):
        """
        Pripraví testovacie dáta: geografickú štruktúru, stanicu, technika a admina.
        """
        self.country = Country.objects.create(name="C")
        self.region = Region.objects.create(name="R", country=self.country)
        self.district = District.objects.create(name="D", region=self.region)
        self.city = City.objects.create(name="City", district=self.district)
        self.station = Station.objects.create(name="One", city=self.city, prefix="XX")
        self.tech = User.objects.create_user("tech", password="pw")
        Profile.objects.create(
            user=self.tech, station=self.station, role=Profile.ROLE_TECHNICIAN
        )
        self.admin = User.objects.create_user("admin", password="pw", is_staff=True)
        Profile.objects.create(user=self.admin, station=None, role=Profile.ROLE_ADMIN)
        self.client = Client()

    def test_technician_header_shows_their_prefix(self):
        """
        Ověří, že technik vidí svoj prefix stanice v hlavičke stránky.

        Testuje, že po prihlásení technika je v HTML elemente <div class="station-code">
        zobrazený prefix stanice, ku ktorej je technik priradený.
        """
        self.client.login(username="tech", password="pw")
        resp = self.client.get(reverse("station_list"))
        self.assertContains(resp, '<div class="station-code">XX</div>')

    def test_admin_header_shows_default_prefix(self):
        """
        Ověří, že admin bez stanice vidí defaultný prefix 'ZM'.

        Testuje, že administrátorovi, ktorý nie je priradený ku žiadnej stanici,
        sa zobrazuje predvolený prefix v hlavičke stránky.
        """
        self.client.login(username="admin", password="pw")
        resp = self.client.get(reverse("station_list"))
        self.assertContains(resp, '<div class="station-code">ZM</div>')


class StationListViewPermissionsTest(TestCase):
    """
    Testy filtrácie zoznamu stanic podľa role používateľa.

    Technik by mal vidieť iba svoju stanicu, admin vidí všetky stanice.
    """

    def setUp(self):
        """
        Pripraví testovacie dáta: dve stanice, technika a admina.
        """
        country = Country.objects.create(name="C")
        region = Region.objects.create(name="R", country=country)
        district = District.objects.create(name="D", region=region)
        city = City.objects.create(name="City", district=district)
        self.s1 = Station.objects.create(name="One", city=city)
        self.s2 = Station.objects.create(name="Two", city=city)
        self.tech = User.objects.create_user("tech2", password="pw2")
        Profile.objects.create(
            user=self.tech, station=self.s1, role=Profile.ROLE_TECHNICIAN
        )
        self.admin = User.objects.create_user("admin2", password="pw2", is_staff=True)
        Profile.objects.create(user=self.admin, station=None, role=Profile.ROLE_ADMIN)
        self.client = Client()

    def test_technician_sees_only_their_station(self):
        """
        Ověří, že technik vidí pouze svoju stanicu v zozname stanic.

        Simuluje prihlásenie technika a požiadanie o stránku zoznamu stanic.
        Overuje, že v kontexte view je len jeho stanica a že HTML obsahuje správny titulok.
        """
        self.client.login(username="tech2", password="pw2")
        resp = self.client.get(reverse("station_list"))
        self.assertEqual(resp.status_code, 200)
        stations = list(resp.context["stations"])
        self.assertEqual(stations, [self.s1])
        self.assertContains(resp, "Vaša stanica")

    def test_admin_sees_all_stations(self):
        """
        Ověří, že admin vidí všetky stanice v zozname stanic.

        Simuluje prihlásenie admina a kontroluje, že v kontexte view sú obe stanice.
        Overuje tiež správny titulok stránky pre admina.
        """
        self.client.login(username="admin2", password="pw2")
        resp = self.client.get(reverse("station_list"))
        self.assertEqual(resp.status_code, 200)
        stations = set(resp.context["stations"])
        self.assertEqual(stations, {self.s1, self.s2})
        self.assertContains(resp, "Zoznam Staníc")
