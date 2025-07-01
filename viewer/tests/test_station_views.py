# viewer/tests.py
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from viewer.models import Country, Region, District, City, Station
from viewer.context_processors import station_prefix, STATION_PREFIX_MAP
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


class StationPrefixContextProcessorTest(TestCase):
    def setUp(self):
        # build the minimal geography tree so we can create a Station
        self.country  = Country.objects.create(name="Testland")
        self.region   = Region.objects.create(name="Test Region", country=self.country)
        self.district = District.objects.create(name="Test District", region=self.region)
        self.city     = City.objects.create(name="Test City", district=self.district)
        # create a station with pk=1 to match STATION_PREFIX_MAP
        self.station = Station.objects.create(name="Alpha", city=self.city)

        # two users: one technician, one admin
        self.tech = User.objects.create_user("tech", password="pw")
        Profile.objects.create(
            user=self.tech,
            station=self.station,
            role=Profile.ROLE_TECHNICIAN
        )
        self.admin = User.objects.create_user("admin", password="pw", is_staff=True)
        Profile.objects.create(
            user=self.admin,
            station=None,
            role=Profile.ROLE_ADMIN
        )

        self.factory = RequestFactory()

    def test_tech_gets_prefix_from_map(self):
        # station.pk == 1, so prefix should be STATION_PREFIX_MAP[1]
        req = self.factory.get("/")
        req.user = self.tech

        ctx = station_prefix(req)
        expected = STATION_PREFIX_MAP.get(self.station.pk, "")
        self.assertEqual(ctx["station_prefix"], expected)

    def test_admin_gets_empty_prefix(self):
        req = self.factory.get("/")
        req.user = self.admin

        ctx = station_prefix(req)
        # admin has no station → prefix is blank
        self.assertEqual(ctx["station_prefix"], "")


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
        # and page title should be "Vaša stanica"
        self.assertContains(resp, "Vaša stanica")

    def test_admin_sees_all_stations(self):
        self.client.login(username="admin2", password="pw2")
        resp = self.client.get(reverse("station_list"))
        self.assertEqual(resp.status_code, 200)
        stations = set(resp.context["stations"])
        self.assertEqual(stations, {self.s1, self.s2})
        # page title remains default
        self.assertContains(resp, "Zoznam Staníc")

