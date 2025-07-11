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


class ExtraDateValidationTest(TestCase):
    """
    Testy pre zadávanie dátumu do polí extra_1 a extra_2 (iba pre Mask).

    Testované scenáre:
        - Nemožno nastaviť dátum do minulosti.
        - Možno nastaviť dnešný alebo budúci dátum.
        - Overenie, že uložené hodnoty zodpovedajú zadaným dátumom.
    """

    def setUp(self):
        """
        Pripraví testovacieho používateľa a testovaciu masku bez nastavených extra polí.
        """
        self.user = User.objects.create_user(username="tester", password="pass")
        self.client.login(username="tester", password="pass")
        self.mask = Mask.objects.create(
            equipment_type=None,
            type="Typ M",
            e_number="54321",
            serial_number="EXTRA1",
            rev_2years="2030-01-01",
            rev_4years="2030-01-01",
            rev_6years="2030-01-01",
            status="ok",
            located=None,
            location=None,
        )

    def test_nemoze_nastavit_extra_1_do_minulosti(self):
        """
        Overí, že nie je možné nastaviť extra_1 na dátum v minulosti.
        """
        url = reverse("update_status")
        vcera = timezone.now().date() - timedelta(days=1)
        data = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "extra_1",
            "extra_date": vcera.isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Nelze zadat datum v minulosti!", response.content.decode())

    def test_moze_nastavit_extra_1_na_dnes_buducnost(self):
        """
        Overí, že je možné nastaviť extra_1 na dnešný alebo budúci dátum.
        """
        url = reverse("update_status")
        dnes = timezone.now().date()
        data_dnes = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "extra_1",
            "extra_date": dnes.isoformat(),
        }
        resp_dnes = self.client.post(url, data_dnes)
        self.assertEqual(resp_dnes.status_code, 200)
        self.mask.refresh_from_db()
        self.assertEqual(self.mask.extra_1, dnes)

        buducnost = dnes + timedelta(days=7)
        data_buducnost = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "extra_1",
            "extra_date": buducnost.isoformat(),
        }
        resp_buducnost = self.client.post(url, data_buducnost)
        self.assertEqual(resp_buducnost.status_code, 200)
        self.mask.refresh_from_db()
        self.assertEqual(self.mask.extra_1, buducnost)

    def test_nemoze_nastavit_extra_2_do_minulosti(self):
        """
        Overí, že nie je možné nastaviť extra_2 na dátum v minulosti.
        """
        url = reverse("update_status")
        vcera = timezone.now().date() - timedelta(days=1)
        data = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "extra_2",
            "extra_date": vcera.isoformat(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Nelze zadat datum v minulosti!", response.content.decode())

    def test_moze_nastavit_extra_2_na_dnes_buducnost(self):
        """
        Overí, že je možné nastaviť extra_2 na dnešný alebo budúci dátum.
        """
        url = reverse("update_status")
        dnes = timezone.now().date()
        data_dnes = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "extra_2",
            "extra_date": dnes.isoformat(),
        }
        resp_dnes = self.client.post(url, data_dnes)
        self.assertEqual(resp_dnes.status_code, 200)
        self.mask.refresh_from_db()
        self.assertEqual(self.mask.extra_2, dnes)

        buducnost = dnes + timedelta(days=10)
        data_buducnost = {
            "model": "Mask",
            "id": self.mask.id,
            "field": "extra_2",
            "extra_date": buducnost.isoformat(),
        }
        resp_buducnost = self.client.post(url, data_buducnost)
        self.assertEqual(resp_buducnost.status_code, 200)
        self.mask.refresh_from_db()
        self.assertEqual(self.mask.extra_2, buducnost)