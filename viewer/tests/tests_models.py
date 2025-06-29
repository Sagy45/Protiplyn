from django.test import TestCase
from viewer.models import Country, Region, District

class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Vytvorí sa testovací objekt Country
        cls.country = Country.objects.create(name="Slovensko")

        # Vytvorí sa testovací objekt Region, ktorý patrí pod Country
        cls.region = Region.objects.create(name="Trnavský kraj", country=cls.country)

        # Vytvorí sa testovací objekt District, ktorý patrí pod Region
        cls.district = District.objects.create(name="Galanta", region=cls.region)

    def test_country_str(self):
        # Testuje, že __str__ metóda pre Country vracia len názov štátu
        self.assertEqual(str(self.country), "Slovensko")

    def test_region_str_and_relation(self):
        # Testuje, že __str__ metóda pre Region vracia aj štát + názov kraja
        # Napr. "Slovensko - Trnavský kraj"
        self.assertEqual(str(self.region), "Slovensko - Trnavský kraj")

        # Overuje, že prepojenie medzi Region a Country funguje správne
        self.assertEqual(self.region.country.name, "Slovensko")

    def test_district_str_and_relation(self):
        # Testuje, že __str__ pre District vracia hierarchiu štát - kraj - okres
        # Napr. "Slovensko - Trnavský kraj - Galanta"
        self.assertEqual(str(self.district), "Slovensko - Trnavský kraj - Galanta")

        # Overuje, že District je správne naviazaný na Region
        self.assertEqual(self.district.region.name, "Trnavský kraj")
