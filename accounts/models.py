"""Definuje model profilu používateľa, ktorý rozširuje vstavaný model User o ďalšie údaje.

Obsahuje rolu používateľa (technik/admin), priradenú stanicu a profilový obrázok.
"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import (
    Model,
    OneToOneField,
    ForeignKey,
    SET_NULL,
    CASCADE,
    ImageField,
    CharField,
)

from viewer.models import Station


class Profile(Model):
    """Model profilu používateľa.

    Tento model slúži na rozšírenie štandardného modelu User o:
    - rolu používateľa (technik alebo administrátor),
    - priradenú stanicu (ak je relevantné),
    - profilový obrázok používateľa.
    """

    ROLE_TECHNICIAN = "technician"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_TECHNICIAN, "Technik"),
        (ROLE_ADMIN, "Admin"),
    ]

    user = OneToOneField(User, on_delete=CASCADE)
    station = ForeignKey(
        Station, on_delete=SET_NULL, null=True, blank=True
    )  # Stanica môže byť nepriradená
    profile_image = ImageField(
        upload_to="profile_images/", null=True, blank=True
    )  # Voliteľný obrázok
    role = CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_TECHNICIAN,
        help_text="Určuje, či je používateľ technik alebo administrátor.",
    )

    def __str__(self):
        """Reprezentácia profilu ako string: 'meno používateľa - rola'."""
        return f"{self.user.username} - {self.get_role_display()}"

    def clean(self):
        """Vlastná validačná logika pre profil.

        Technici musia mať priradenú stanicu. Admin môže byť bez stanice.
        """
        if not self.station:
            raise ValidationError("Musí byť priradená stanica!")
