from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, ForeignKey, SET_NULL, CASCADE, ImageField, CharField
from viewer.models import Station
from django.core.exceptions import ValidationError

class Profile(Model):
    ROLE_TECHNICIAN = 'technician'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_TECHNICIAN, 'Technik'),
        (ROLE_ADMIN, 'Admin'),
    ]

    user = OneToOneField(User, on_delete=CASCADE)
    station = ForeignKey(Station, on_delete=SET_NULL, null=True, blank=True)
    profile_image = ImageField(upload_to="profile_images/", null=True, blank=True)
    role = CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_TECHNICIAN,
        help_text="Urcuje jestli je uzivatel technik nebo admin"
    )
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def clean(self):
        if not self.station:
            raise ValidationError("Musi byt priradena stanica!")
