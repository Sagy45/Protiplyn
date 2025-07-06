"""Modely pre aplikáciu equipment."""

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

STATUS_CHOICES = [
    ("ok", "OK"),
    ("bsr", "BSR"),
    ("under_revision", "V riešení"),
    ("critical", "Kriticky"),
    ("vyradit", "Vyradiť"),
]

REVISION_LABELS = {
    "rev_2years": "2 ročná",
    "rev_4years": "4 ročná",
    "rev_6years": "6 ročná",
    "rev_1years": "1 ročná",
    "rev_5years": "5 ročná",
    "rev_9years": "9 ročná",
    "rev_3year": "3 ročná",
    "rev_half_year": "Polročná",
    "extra_1": "Extra 1",
    "extra_2": "Extra 2",
    "serial_number": 'Sériové číslo',
    "e_number": "Evidenčné číslo",
    "status": "Stav",
    "type": "Typ"

}
REVISION_FIELDS = list(REVISION_LABELS.keys())


class EquipmentType(models.Model):
    """
    Model reprezentujúci typ vybavenia.

    Atribúty:
        name (str): Názov typu vybavenia.
    """

    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Druh"

    def __str__(self):
        return self.name


class VehicleStorage(models.Model):
    """
    Model pre evidenciu vozidiel a skladov.

    Atribúty:
        brand (str): Značka vozidla/skladu.
        spz (str): ŠPZ (voliteľné).
        station (Station): Príslušná stanica.
    """

    brand = models.CharField(max_length=100, null=False, blank=False)
    spz = models.CharField(max_length=7, null=True, blank=True)
    station = models.ForeignKey(
        "viewer.Station", on_delete=models.SET_NULL, null=True, related_name="viewer"
    )

    class Meta:
        ordering = ["brand"]
        verbose_name_plural = "Auto/Sklad"

    def __str__(self):
        return f"{self.brand} {self.spz or ''}"


class ArchiveFields(models.Model):
    """
    Abstraktný model na podporu archivácie záznamov.

    Atribúty:
        is_archived (bool): Či je záznam archivovaný.
        archived_at (datetime): Dátum a čas archivácie.
        archived_by (User): Používateľ, ktorý archivoval.
    """

    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="archived_%(class)s",
    )

    class Meta:
        abstract = True


class Mask(ArchiveFields, models.Model):
    """
    Model pre celoobličejové masky.

    Atribúty:
        equipment_type (EquipmentType): Typ vybavenia.
        type (str): Typ masky.
        e_number (str): Evidenčné číslo.
        serial_number (str): Sériové číslo.
        rev_2years, rev_4years, rev_6years, extra_1, extra_2 (date): Termíny revízií.
        status (str): Stav.
        located (Station): Stanica.
        location (VehicleStorage): Vozidlo/sklad.
        status_field (str): Aktuálne riešená revízia.
    """

    equipment_type = models.ForeignKey(
        "EquipmentType", on_delete=models.SET_NULL, null=True, related_name="masks_over"
    )
    type = models.CharField(max_length=50, null=False, blank=False)
    e_number = models.CharField(max_length=10, null=False, blank=False)
    serial_number = models.CharField(max_length=50, null=False, blank=False)
    rev_2years = models.DateField(null=False, blank=False)
    rev_4years = models.DateField(null=False, blank=False)
    rev_6years = models.DateField(null=False, blank=False)
    extra_1 = models.DateField(null=True, blank=True)
    extra_2 = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ok",
        verbose_name="Súčasný stav",
    )
    located = models.ForeignKey(
        "viewer.Station",
        on_delete=models.SET_NULL,
        null=True,
        related_name="MO_located_stations",
    )
    location = models.ForeignKey(
        "VehicleStorage", on_delete=models.SET_NULL, null=True, related_name="MO_locations"
    )
    status_field = models.CharField(
        max_length=30, blank=True, null=True, help_text="Ktorá revízia je práve v riešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name = "Maska"
        verbose_name_plural = "Masky"

    def clean(self):
        """
        Overuje, že žiadne revízne dátumy nie sú v minulosti.
        """
        today = timezone.now().date()
        revision_fields = [
            ("rev_2years", self.rev_2years),
            ("rev_4years", self.rev_4years),
            ("rev_6years", self.rev_6years),
            ("extra_1", self.extra_1),
            ("extra_2", self.extra_2),
        ]
        for name, value in revision_fields:
            if value and value < today:
                raise ValidationError({name: f"{name} nemôže byť v minulosti."})

    def __str__(self):
        return f"{self.equipment_type} {self.type} {self.e_number}"


class ADPMulti(ArchiveFields, models.Model):
    """
    Model pre ADP dvojhadicové.

    Atribúty:
        equipment_type (EquipmentType): Typ vybavenia.
        type (str): Typ ADP.
        e_number (str): Evidenčné číslo.
        serial_number (str): Sériové číslo.
        rev_1years, rev_6years (date): Termíny revízií.
        status (str): Stav.
        located (Station): Stanica.
        location (VehicleStorage): Vozidlo/sklad.
        status_field (str): Aktuálne riešená revízia.
    """

    equipment_type = models.ForeignKey(
        "EquipmentType", on_delete=models.SET_NULL, null=True, related_name="adp_m"
    )
    type = models.CharField(max_length=50, null=False, blank=False)
    e_number = models.CharField(max_length=10, null=False, blank=False)
    serial_number = models.CharField(max_length=50, null=False, blank=False)
    rev_1years = models.DateField(null=False, blank=False)
    rev_6years = models.DateField(null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ok",
        verbose_name="Súčasný stav",
    )
    located = models.ForeignKey(
        "viewer.Station",
        on_delete=models.SET_NULL,
        null=True,
        related_name="ADPm_located_stations",
    )
    location = models.ForeignKey(
        "VehicleStorage", on_delete=models.SET_NULL, null=True, related_name="ADMm_locations"
    )
    status_field = models.CharField(
        max_length=30, blank=True, null=True, help_text="Ktorá revízia je práve v riešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name = "ADP-Dvojhadicová"
        verbose_name_plural = "ADP-Dvojhadicovy"


    def clean(self):
        """
        Overuje, že revízne dátumy nie sú v minulosti.
        """
        today = timezone.now().date()
        revision_fields = [
            ("rev_1years", self.rev_1years),
            ("rev_6years", self.rev_6years),
        ]
        for name, value in revision_fields:
            if value and value < today:
                raise ValidationError({name: f"{name} nemôže byť v minulosti."})

    def __str__(self):
        return f"{self.equipment_type} {self.type} {self.e_number}"


class ADPSingle(ArchiveFields, models.Model):
    """
    Model pre ADP jednohadicové.

    Atribúty:
        equipment_type (EquipmentType): Typ vybavenia.
        type (str): Typ ADP.
        e_number (str): Evidenčné číslo.
        serial_number (str): Sériové číslo.
        rev_1years, rev_9years (date): Termíny revízií.
        status (str): Stav.
        located (Station): Stanica.
        location (VehicleStorage): Vozidlo/sklad.
        status_field (str): Aktuálne riešená revízia.
    """

    equipment_type = models.ForeignKey(
        "EquipmentType", on_delete=models.SET_NULL, null=True, related_name="adp_s"
    )
    type = models.CharField(max_length=50, null=False, blank=False)
    e_number = models.CharField(max_length=10, null=False, blank=False)
    serial_number = models.CharField(max_length=50, null=False, blank=False)
    rev_1years = models.DateField(null=False, blank=False)
    rev_9years = models.DateField(null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ok",
        verbose_name="Súčasný stav",
    )
    located = models.ForeignKey(
        "viewer.Station",
        on_delete=models.SET_NULL,
        null=True,
        related_name="ADPs_located_stations",
    )
    location = models.ForeignKey(
        "VehicleStorage", on_delete=models.SET_NULL, null=True, related_name="ADPs_locations"
    )
    status_field = models.CharField(
        max_length=30, blank=True, null=True, help_text="Ktorá revízia je práve v riešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name = "ADP-Jednohadicová"
        verbose_name_plural = "ADP-Jednohadicovy"

    def clean(self):
        """
        Overuje, že revízne dátumy nie sú v minulosti.
        """
        today = timezone.now().date()
        revision_fields = [
            ("rev_1years", self.rev_1years),
            ("rev_9years", self.rev_9years),
        ]
        for name, value in revision_fields:
            if value and value < today:
                raise ValidationError({name: f"{name} nemôže byť v minulosti."})

    def __str__(self):
        return f"{self.equipment_type} {self.type} {self.e_number}"


class AirTank(ArchiveFields, models.Model):
    """
    Model pre tlakové nádoby (fľaše).

    Atribúty:
        equipment_type (EquipmentType): Typ vybavenia.
        type (str): Typ nádoby.
        e_number (str): Evidenčné číslo.
        serial_number (str): Sériové číslo.
        volume (str): Objem.
        pressure (str): Tlak.
        material_type (str): Materiál.
        rev_5years (date): Termín revízie.
        made (int): Rok výroby.
        service_life (int): Životnosť v rokoch.
        status (str): Stav.
        located (Station): Stanica.
        location (VehicleStorage): Vozidlo/sklad.
        status_field (str): Aktuálne riešená revízia.
    """

    equipment_type = models.ForeignKey(
        "EquipmentType", on_delete=models.SET_NULL, null=True, related_name="airtank"
    )
    type = models.CharField(max_length=50, null=False, blank=False)
    e_number = models.CharField(max_length=10, null=False, blank=False)
    serial_number = models.CharField(max_length=50, null=False, blank=False)
    volume = models.CharField(max_length=50, null=False, blank=False)
    pressure = models.CharField(max_length=50, null=False, blank=False)
    material_type = models.CharField(max_length=50, null=False, blank=False)
    rev_5years = models.DateField(null=False, blank=False)
    made = models.IntegerField(null=False, blank=False)
    service_life = models.IntegerField(null=False, blank=False)  # v rokoch
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ok",
        verbose_name="Súčasný stav",
    )
    located = models.ForeignKey(
        "viewer.Station",
        on_delete=models.SET_NULL,
        null=True,
        related_name="AirTank_located_stations",
    )
    location = models.ForeignKey(
        "VehicleStorage",
        on_delete=models.SET_NULL,
        null=True,
        related_name="AirTank_locations",
    )
    status_field = models.CharField(
        max_length=30, blank=True, null=True, help_text="Ktorá revízia je práve v riešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name = "Tlaková nádoba"
        verbose_name_plural = "Tlakové nádoby"

    def clean(self):
        """
        Overuje, že revízny dátum nie je v minulosti.
        """
        today = timezone.now().date()
        revision_fields = [
            ("rev_5years", self.rev_5years),
        ]
        for name, value in revision_fields:
            if value and value < today:
                raise ValidationError({name: f"{name} nemôže byť v minulosti."})

    def __str__(self):
        return f"{self.equipment_type} {self.type} {self.e_number}"


class PCHO(ArchiveFields, models.Model):
    """
    Model pre proti-chemické obleky (PCHO).

    Atribúty:
        equipment_type (EquipmentType): Typ vybavenia.
        type (str): Typ PCHO.
        e_number (str): Evidenčné číslo.
        serial_number (str): Sériové číslo.
        rev_half_year, rev_2years (date): Termíny revízií.
        made (int): Rok výroby.
        service_life (int): Životnosť v rokoch.
        status (str): Stav.
        located (Station): Stanica.
        location (VehicleStorage): Vozidlo/sklad.
        status_field (str): Aktuálne riešená revízia.
    """

    equipment_type = models.ForeignKey(
        "EquipmentType", on_delete=models.SET_NULL, null=True, related_name="pcho"
    )
    type = models.CharField(max_length=50, null=False, blank=False)
    e_number = models.CharField(max_length=10, null=False, blank=False)
    serial_number = models.CharField(max_length=50, null=False, blank=False)
    rev_half_year = models.DateField(null=False, blank=False)
    rev_2years = models.DateField(null=False, blank=False)
    made = models.IntegerField(null=False, blank=False)
    service_life = models.IntegerField(null=False, blank=False)  # v rokoch
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ok",
        verbose_name="Súčasný stav",
    )
    located = models.ForeignKey(
        "viewer.Station",
        on_delete=models.SET_NULL,
        null=True,
        related_name="PCHO_located_stations",
    )
    location = models.ForeignKey(
        "VehicleStorage", on_delete=models.SET_NULL, null=True, related_name="PCHO_locations"
    )
    status_field = models.CharField(
        max_length=30, blank=True, null=True, help_text="Ktorá revízia je práve v riešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name = "Protichemický oblek"
        verbose_name_plural = "Protichemické obleky"

    def clean(self):
        """
        Overuje, že revízne dátumy nie sú v minulosti.
        """
        today = timezone.now().date()
        revision_fields = [
            ("rev_2years", self.rev_2years),
            ("rev_half_year", self.rev_half_year),
        ]
        for name, value in revision_fields:
            if value and value < today:
                raise ValidationError({name: f"{name} nemôže byť v minulosti."})

    def __str__(self):
        return f"{self.equipment_type} {self.type} {self.e_number}"


class PA(ArchiveFields, models.Model):
    """
    Model pre pľúcnu automatiku.

    Atribúty:
        equipment_type (EquipmentType): Typ vybavenia.
        type (str): Typ PA.
        e_number (str): Evidenčné číslo.
        serial_number (str): Sériové číslo.
        rev_3year, rev_6years, rev_9years (date): Termíny revízií.
        made (int): Rok výroby.
        status (str): Stav.
        located (Station): Stanica.
        location (VehicleStorage): Vozidlo/sklad.
        status_field (str): Aktuálne riešená revízia.
    """

    equipment_type = models.ForeignKey(
        "EquipmentType", on_delete=models.SET_NULL, null=True, related_name="pa"
    )
    type = models.CharField(max_length=50, null=False, blank=False)
    e_number = models.CharField(max_length=10, null=False, blank=False)
    serial_number = models.CharField(max_length=50, null=False, blank=False)
    rev_3year = models.DateField(null=False, blank=False)
    rev_6years = models.DateField(null=False, blank=False)
    rev_9years = models.DateField(null=False, blank=False)
    made = models.IntegerField(null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ok",
        verbose_name="Súčasný stav",
    )
    located = models.ForeignKey(
        "viewer.Station",
        on_delete=models.SET_NULL,
        null=True,
        related_name="PA_located_stations",
    )
    location = models.ForeignKey(
        "VehicleStorage", on_delete=models.SET_NULL, null=True, related_name="PA_locations"
    )
    status_field = models.CharField(
        max_length=30, blank=True, null=True, help_text="Ktorá revízia je práve v riešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name = "Pľúcna automatika"
        verbose_name_plural = "Pľúcne automatiky"

    def clean(self):
        """
        Overuje, že revízne dátumy nie sú v minulosti.
        """
        today = timezone.now().date()
        revision_fields = [
            ("rev_3years", self.rev_3year),
            ("rev_6years", self.rev_6years),
            ("rev_9years", self.rev_9years),
        ]
        for name, value in revision_fields:
            if value and value < today:
                raise ValidationError({name: f"{name} nemôže byť v minulosti."})

    def __str__(self):
        return f"{self.equipment_type} {self.type} {self.e_number}"


class Complete(models.Model):
    """
    Model reprezentujúci komplet vybavenia s evidenčným číslom.

    Atribúty:
        e_number (str): Evidenčné číslo (spoločné pre komplet).
    """

    e_number = models.CharField(max_length=10, null=False, blank=False)

    class Meta:
        verbose_name = "Komplet"
        verbose_name_plural = "Komplety"

    def __str__(self):
        """
        Reprezentácia kompletu - vypíše masku, pa a adp.
        """
        p = self.parts
        return f"{self.e_number}: {p['mask']}; {p['pa']}; {p['adp']}"

    @property
    def mask(self):
        """Vráti príslušnú masku pre daný komplet."""
        return Mask.objects.get(e_number=self.e_number)

    @property
    def pa(self):
        """Vráti príslušnú PA pre daný komplet."""
        return PA.objects.get(e_number=self.e_number)

    @property
    def adp(self):
        """
        Vráti príslušné ADP (najprv hľadá dvojhadicové, potom jednohadicové).
        """
        choice = ADPMulti.objects.filter(e_number=self.e_number).first()
        if choice:
            return choice
        return ADPSingle.objects.get(e_number=self.e_number)

    @property
    def parts(self):
        """
        Vráti slovník so stručnými popismi všetkých častí kompletu.
        """
        return {
            "mask": f"{self.mask.equipment_type}, seriové číslo: {self.mask.serial_number}",
            "pa": f"{self.pa.equipment_type}, seriové číslo: {self.pa.serial_number}",
            "adp": f"{self.adp.equipment_type}, seriové číslo: {self.adp.serial_number}",
        }

    def clean(self):
        """
        Overuje, že existujú všetky potrebné časti kompletu.
        """
        error = {}
        if not Mask.objects.filter(e_number=self.e_number).exists():
            error["e_number"] = "Maska neexistuje"
        if not PA.objects.filter(e_number=self.e_number).exists():
            error.setdefault("e_number", "PA neexistuje")
        if not (
            ADPMulti.objects.filter(e_number=self.e_number).exists()
            or ADPSingle.objects.filter(e_number=self.e_number).exists()
        ):
            error.setdefault("e_number", "Žiadne ADP neexistuje")
        if error:
            raise ValidationError(error)

    def save(self, *args, **kwargs):
        """
        Uloží model po overení (validácii) všetkých častí kompletu.
        """
        self.full_clean()
        super().save(*args, **kwargs)


class ActiveManager(models.Manager):
    """
    Custom manager pre záznamy, ktoré nie sú archivované.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)

    def __str__(self):
        return "Active"


class ArchivedManager(models.Manager):
    """
    Custom manager pre archivované záznamy.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=True)

    def __str__(self):
        return "Archived"


class Equipment(ArchiveFields, models.Model):
    """
    Abstraktný model pre všetky typy vybavenia s podporou archivácie.

    Používajte ako rodičovskú triedu pre konkrétne typy vybavenia.
    """

    class Meta:
        abstract = True

    objects = models.Manager()  # základný manager
    active = ActiveManager()    # iba aktívne záznamy
    archived = ArchivedManager()  # iba archivované záznamy
