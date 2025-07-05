"""
Modely geografických entít pre systém Protiplyn.

Obsahuje modely pre krajiny, kraje, okresy, mestá a stanice.
Každý model implementuje reťazcovú reprezentáciu s informáciou o nadriadených entitách.
"""

from django.db.models import Model, CharField, ForeignKey, SET_NULL


class Country(Model):
    """
    Model reprezentujúci štát/krajinu.

    Atribúty:
        name (str): Názov štátu (unikátny).
    """

    name = CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        verbose_name_plural = "Štát"

    def __str__(self):
        """
        Vráti reťazcovú reprezentáciu štátu.

        Returns:
            str: Názov štátu.
        """
        return self.name


class Region(Model):
    """
    Model reprezentujúci kraj/region.

    Atribúty:
        name (str): Názov kraja (unikátny).
        country (Country): Nadriadený štát.
    """

    name = CharField(max_length=100, null=False, blank=False, unique=True)
    country = ForeignKey(
        "Country", on_delete=SET_NULL, null=True, related_name="regions"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Kraje"

    def __str__(self):
        """
        Vráti reťazcovú reprezentáciu kraja, vrátane štátu.

        Returns:
            str: Štát - Kraj.
        """
        parts = []
        if self.country:
            parts.append(self.country.name)
        parts.append(self.name)
        return " - ".join(parts)


class District(Model):
    """
    Model reprezentujúci okres.

    Atribúty:
        name (str): Názov okresu (unikátny).
        region (Region): Nadriadený kraj.
    """

    name = CharField(max_length=100, null=False, blank=False, unique=True)
    region = ForeignKey(
        "Region", on_delete=SET_NULL, null=True, related_name="districts"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Okresy"

    def __str__(self):
        """
        Vráti reťazcovú reprezentáciu okresu, vrátane kraja a štátu.

        Returns:
            str: Štát - Kraj - Okres.
        """
        parts = []
        if self.region:
            parts.append(str(self.region))
        parts.append(self.name)
        return " - ".join(parts)


class City(Model):
    """
    Model reprezentujúci mesto.

    Atribúty:
        name (str): Názov mesta (unikátny).
        district (District): Nadriadený okres.
    """

    name = CharField(max_length=100, null=False, blank=False, unique=True)
    district = ForeignKey(
        "District", on_delete=SET_NULL, null=True, related_name="cities"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Mestá"

    def __str__(self):
        """
        Vráti reťazcovú reprezentáciu mesta, vrátane okresu, kraja a štátu.

        Returns:
            str: Štát - Kraj - Okres - Mesto.
        """
        parts = []
        if self.district:
            parts.append(str(self.district))
        parts.append(self.name)
        return " - ".join(parts)


class Station(Model):
    """
    Model reprezentujúci stanicu.

    Atribúty:
        name (str): Názov stanice (unikátny).
        city (City): Nadriadené mesto.
        prefix (str): Skratka stanice (voliteľné).
    """

    name = CharField(max_length=100, null=False, blank=False, unique=True)
    city = ForeignKey("City", on_delete=SET_NULL, null=True, related_name="stations")
    prefix = CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Stanice"

    def __str__(self):
        """
        Vráti reťazcovú reprezentáciu stanice, vrátane všetkých nadriadených entít.

        Returns:
            str: Štát - Kraj - Okres - Mesto - Stanica.
        """
        parts = []
        if self.city:
            parts.append(str(self.city))
        parts.append(self.name)
        return " - ".join(parts)
