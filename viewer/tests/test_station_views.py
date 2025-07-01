from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from viewer.models import Country, Region, District, City, Station
from accounts.models import Profile

"""
What these tests do:

    StationPrefixContextProcessorTest:

    Vytvorí minimálny modelový strom (krajina, región, okres, mesto, stanica) tak, aby ste dostali stanicu(pk=1), ktorá zodpovedá vašej STATION_PREFIX_MAP.

    Overuje, či technik dostane správny prefix a administrátor nedostane žiadny prefix.

StationListViewPermissionsTest:

    Vytvorí dve stanice a dvoch používateľov (technik je viazaný na stanicu jedna, administrátor nie je viazaný na žiadnu).

    Prihlási každého z nich a požiada o /stations/.

    Porovnává, že technik vidí len svoju stanicu a administrátor vidí obe.

    Kontroluje aj <title> v HTML pre vaše dynamické názvy stránok.
"""



class StationPrefixHeaderTest(TestCase):
    def setUp(self):
        # build minimal geography tree
        self.country = Country.objects.create(name="C")
        self.region = Region.objects.create(name="R", country=self.country)
        self.district = District.objects.create(name="D", region=self.region)
        self.city = City.objects.create(name="City", district=self.district)
        # create a station with explicit prefix
        self.station = Station.objects.create(name="One", city=self.city, prefix="XX")

        # Technician user linked to station
        self.tech = User.objects.create_user("tech", password="pw")
        Profile.objects.create(
            user=self.tech,
            station=self.station,
            role=Profile.ROLE_TECHNICIAN
        )
        # Admin user without station
        self.admin = User.objects.create_user("admin", password="pw", is_staff=True)
        Profile.objects.create(
            user=self.admin,
            station=None,
            role=Profile.ROLE_ADMIN
        )

        self.client = Client()

    def test_technician_header_shows_their_prefix(self):
        self.client.login(username="tech", password="pw")
        resp = self.client.get(reverse("station_list"))
        # Header .station-code should display station.prefix
        self.assertContains(resp, '<div class="station-code">XX</div>')

    def test_admin_header_shows_default_prefix(self):
        self.client.login(username="admin", password="pw")
        resp = self.client.get(reverse("station_list"))
        # Admin with no station falls back to default 'ZM'
        self.assertContains(resp, '<div class="station-code">ZM</div>')


class StationListViewPermissionsTest(TestCase):
    def setUp(self):
        # Geography
        country  = Country.objects.create(name="C")
        region   = Region.objects.create(name="R", country=country)
        district = District.objects.create(name="D", region=region)
        city     = City.objects.create(name="City", district=district)
        # Two stations
        self.s1 = Station.objects.create(name="One", city=city)
        self.s2 = Station.objects.create(name="Two", city=city)

        # Technician user linked to s1
        self.tech = User.objects.create_user("tech2", password="pw2")
        Profile.objects.create(
            user=self.tech,
            station=self.s1,
            role=Profile.ROLE_TECHNICIAN
        )

        # Admin user
        self.admin = User.objects.create_user("admin2", password="pw2", is_staff=True)
        Profile.objects.create(
            user=self.admin,
            station=None,
            role=Profile.ROLE_ADMIN
        )

        self.client = Client()

    def test_technician_sees_only_their_station(self):
        self.client.login(username="tech2", password="pw2")
        resp = self.client.get(reverse("station_list"))
        self.assertEqual(resp.status_code, 200)
        # only s1 in context
        stations = list(resp.context["stations"])
        self.assertEqual(stations, [self.s1])
        # dynamic title for technician
        self.assertContains(resp, "Vaša stanica")

    def test_admin_sees_all_stations(self):
        self.client.login(username="admin2", password="pw2")
        resp = self.client.get(reverse("station_list"))
        self.assertEqual(resp.status_code, 200)
        stations = set(resp.context["stations"])
        self.assertEqual(stations, {self.s1, self.s2})
        # default title for admin
        self.assertContains(resp, "Zoznam Staníc")


