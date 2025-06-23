from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, ForeignKey, SET_NULL, CASCADE
from viewer.models import Station
from django.core.exceptions import ValidationError

class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    station = ForeignKey(Station, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.station}"

    def clean(self):
        if not self.station:
            raise ValidationError("Musi byt priradena stanica!")
