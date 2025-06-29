from django.test import TestCase
from django.urls import reverse
from equipment.models import Mask
from django.contrib.auth.models import User

class EquipmentSearchViewTest(TestCase):
    def setUp(self):
        # Vytvoríme používateľa (voliteľné, ale užitočné ak bude login required)
        self.user = User.objects.create_user(username="tester", password="pass")

        # Vytvoríme testovací objekt typu Mask s konkrétnym sériovým číslom
        self.mask = Mask.objects.create(
            equipment_type=None,
            type="Typ M",
            e_number="12345",
            serial_number="ABC123",
            rev_2years="2030-01-01",
            rev_4years="2030-01-01",
            rev_6years="2030-01-01",
            status="ok",
            located=None,
            location=None,
        )

    def test_search_redirects_when_serial_found(self):
        # Simulujeme GET požiadavku s existujúcim serial_number
        response = self.client.get(reverse("equipment_search") + "?serial_number=ABC123")

        # Očakávame redirect (302) na detail daného objektu
        expected_url = reverse("equipment_detail", args=["Mask", self.mask.pk])  # Vygenerujeme URL podľa url patternu
        self.assertRedirects(response, expected_url)  # Test: kontroluje redirect aj cieľovú URL

    def test_search_is_case_insensitive(self):
        # Hľadáme rovnaký serial_number, ale s malými písmenami (porovnanie je case-insensitive)
        response = self.client.get(reverse("equipment_search") + "?serial_number=abc123")

        # Tiež by mal byť redirect na správnu URL
        expected_url = reverse("equipment_detail", args=["Mask", self.mask.pk])
        self.assertRedirects(response, expected_url)  # Test: redirect funguje aj pri rôznej veľkosti písmen

    def test_search_not_found_renders_template(self):
        # Vyhľadáme neexistujúci serial_number
        response = self.client.get(reverse("equipment_search") + "?serial_number=NEEXISTUJE")

        # Očakávame, že sa vráti 200 OK a zobrazí sa šablóna "search_not_found.html"
        self.assertEqual(response.status_code, 200)  # Test: stránka sa vrátila
        self.assertTemplateUsed(response, "equipment/search_not_found.html")  # Test: správna šablóna
        self.assertContains(response, "NEEXISTUJE")  # Test: do šablóny bol pridaný pôvodný dopyt
