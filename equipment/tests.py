from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from equipment.models import Mask

User = get_user_model()


class EquipmentSearchViewTest(TestCase):
    """
    Testy pre vyhľadávanie vybavenia podľa sériového čísla.

    Testované scenáre:
        - Vyhľadávanie existujúcej masky a presmerovanie na detail.
        - Nezáleží na veľkosti písmen v sériovom čísle.
        - Ak sa nenájde vybavenie, zobrazí sa správna šablóna s hľadaným textom.
    """

    def setUp(self):
        """
        Pripraví testovacieho používateľa a testovaciu masku.
        """
        self.user = User.objects.create_user(username="tester", password="pass")
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
        """
        Overí, že pri zadaní existujúceho sériového čísla dôjde k presmerovaniu na detail masky.
        """
        response = self.client.get(
            reverse("equipment_search") + "?serial_number=ABC123"
        )
        expected_url = reverse("equipment_detail", args=["Mask", self.mask.pk])
        self.assertRedirects(response, expected_url)

    def test_search_is_case_insensitive(self):
        """
        Overí, že vyhľadávanie je nezávislé na veľkosti písmen.
        """
        response = self.client.get(
            reverse("equipment_search") + "?serial_number=abc123"
        )
        expected_url = reverse("equipment_detail", args=["Mask", self.mask.pk])
        self.assertRedirects(response, expected_url)

    def test_search_not_found_renders_template(self):
        """
        Overí, že ak sa maska nenájde, vráti sa správna šablóna a status 200.
        """
        response = self.client.get(
            reverse("equipment_search") + "?serial_number=NEEXISTUJE"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "equipment/search_not_found.html")
        self.assertContains(response, "NEEXISTUJE")


class UpdateStatusFormTest(TestCase):
    """
    Testy pre validáciu dátumu revízie pri aktualizácii statusu vybavenia.

    Testované scenáre:
        - Nemožno nastaviť revíziu do minulosti.
        - Možno nastaviť revíziu na dnešný alebo budúci dátum.
    """

    def setUp(self):
        """
        Pripraví testovacieho používateľa a testovaciu masku.
        """
        self.user = User.objects.create_user(username="tester", password="pass")
        self.client.login(username="tester", password="pass")
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

    def test_cannot_set_revision_to_past_date(self):
        """
        Overí, že nie je možné nastaviť revíziu na dátum v minulosti.
        """
        url = reverse("update_status")
        yesterday = timezone.now().date() - timedelta(days=1)
        data = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "rev_2years",
            "status": "ok",
            "revise_from_date": yesterday.isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Past date not allowed", response.content)

    def test_can_set_revision_to_today_or_future(self):
        """
        Overí, že je možné nastaviť revíziu na dnešný alebo budúci dátum.
        """
        url = reverse("update_status")
        today = timezone.now().date()
        data_today = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "rev_2years",
            "status": "ok",
            "revise_from_date": today.isoformat(),
        }
        resp_today = self.client.post(url, data_today)
        self.assertEqual(resp_today.status_code, 200)
        self.assertIn("ok", resp_today.json().get("result", ""))

        future = today + timedelta(days=10)
        data_future = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "rev_2years",
            "status": "ok",
            "revise_from_date": future.isoformat(),
        }
        resp_future = self.client.post(url, data_future)
        self.assertEqual(resp_future.status_code, 200)
        self.assertIn("ok", resp_future.json().get("result", ""))
