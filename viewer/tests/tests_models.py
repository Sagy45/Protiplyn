import datetime
from django.test import TestCase
from viewer.models import Country, Region, District


class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name="Slovensko")
        cls.region = Region.objects.create(name="Trnavský kraj", country=cls.country)
        cls.district = District.objects.create(name="Galanta", region=cls.region)

    def test_country_str(self):
        self.assertEqual(str(self.country), "Slovensko")

    def test_region_str_and_relation(self):
        self.assertEqual(str(self.region), "Trnavský kraj")
        self.assertEqual(self.region.country.name, "Slovensko")

    def test_district_str_and_relation(self):
        self.assertEqual(str(self.district), "Galanta")
        self.assertEqual(self.district.region.name, "Trnavský kraj")