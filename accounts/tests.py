"""Testy pro model Profile v aplikaci accounts."""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from viewer.models import Station
from .models import Profile


class ProfileModelTest(TestCase):
    """Testovací třída pro model Profile."""

    def setUp(self):
        """Vytvoří testovacího uživatele a stanici."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.station = Station.objects.create(name="Stanica 1")

    def test_create_valid_profile(self):
        """Ověřuje, že lze vytvořit validní profil."""
        profile = Profile.objects.create(user=self.user, station=self.station)
        self.assertEqual(profile.user.username, "testuser")
        self.assertEqual(profile.station.name, "Stanica 1")

    def test_profile_clean_without_station(self):
        """Ověřuje, že clean() vyhodí výjimku, pokud chybí stanice."""
        profile = Profile(user=self.user)
        with self.assertRaises(ValidationError):
            profile.clean()

    def test_profile_str(self):
        """Ověřuje správný stringový výstup __str__ metody."""
        profile = Profile.objects.create(user=self.user, station=self.station)
        expected_str = f"{self.user.username} - {profile.get_role_display()}"
        self.assertEqual(str(profile), expected_str)
