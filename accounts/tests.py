from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from viewer.models import Station
from .models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.station = Station.objects.create(name='Stanica 1')

    def test_create_valid_profile(self):
        profile = Profile.objects.create(user=self.user, station=self.station)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.station.name, 'Stanica 1')

    def test_profile_clean_without_station(self):
        profile = Profile(user=self.user)
        with self.assertRaises(ValidationError):
            profile.clean()

    def test_profile_str(self):
        profile = Profile.objects.create(user=self.user, station=self.station)
        expected_str = f"{self.user.username} - {self.station}"
        self.assertEqual(str(profile), expected_str)
