from django.db.models import Model, CharField, ForeignKey, SET_NULL, DateField, IntegerField
from django.db import models
from django.core.exceptions import ValidationError

class EquipmentType(Model):
    name = CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Druh"

    def __str__(self):
        return self.name


class VehicleStorage(Model):
    brand = CharField(max_length=100, null=False, blank=False)
    spz = CharField(max_length=7, null=True, blank=True)
    station = ForeignKey("viewer.Station", on_delete=SET_NULL, null=True, related_name="viewer")

    class Meta:
        ordering = ["brand"]
        verbose_name_plural = "Auto/Sklad"

    def __str__(self):
        return f" {self.brand} {self.spz}"

STATUS_CHOICES = [
    ('ok', 'OK'),
    ('bsr', 'BSR'),
    ('under_revision', 'V rieseni'),
    ('critical', 'Kriticky'),
    ('vyradit', 'Vyradiť'),
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
}

REVISION_FIELDS = list(REVISION_LABELS.keys())


class Mask(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="masks_over")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_2years = DateField(null=False,blank=False)
    rev_4years = DateField(null=False,blank=False)
    rev_6years = DateField(null=False,blank=False)
    extra_1 = DateField(null=True,blank=True)
    extra_2 = DateField(null=True,blank=True)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='ok', verbose_name="Současný stav")
    located = ForeignKey("viewer.Station", on_delete=SET_NULL, null=True,related_name="MO_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="MO_locations")
    is_archived = models.BooleanField(default=False)
    status_field = models.CharField(
        max_length=30,
        blank=True, null=True,
        help_text="Která revize je právě v řešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name_plural = "Masky"

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class ADPMulti(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="adp_m")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_1years = DateField(null=False,blank=False)
    rev_6years = DateField(null=False,blank=False)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='ok', verbose_name="Současný stav")
    located = ForeignKey("viewer.Station", on_delete=SET_NULL, null=True,related_name="ADPm_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="ADMm_locations")
    is_archived = models.BooleanField(default=False)
    status_field = models.CharField(
        max_length=30,
        blank=True, null=True,
        help_text="Která revize je právě v řešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name_plural = "ADP-Dvojhadicovy"

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class ADPSingle(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="adp_s")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_1years = DateField(null=False,blank=False)
    rev_9years = DateField(null=False,blank=False)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='ok', verbose_name="Současný stav")
    located = ForeignKey("viewer.Station", on_delete=SET_NULL, null=True,related_name="ADPs_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="ADPs_locations")
    is_archived = models.BooleanField(default=False)
    status_field = models.CharField(
        max_length=30,
        blank=True, null=True,
        help_text="Která revize je právě v řešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name_plural = "ADP-Jednohadicovy"

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class AirTank(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="airtank")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    volume = CharField(max_length=50,null=False,blank=False)
    pressure = CharField(max_length=50,null=False,blank=False)
    material_type = CharField(max_length=50,null=False,blank=False)
    rev_5years = DateField(null=False,blank=False)
    made = IntegerField(null=False,blank=False)
    service_life = IntegerField(null=False,blank=False) #v rokoch
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='ok', verbose_name="Současný stav")
    located = ForeignKey("viewer.Station", on_delete=SET_NULL, null=True,related_name="AirTank_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="AirTank_locations")
    is_archived = models.BooleanField(default=False)
    status_field = models.CharField(
        max_length=30,
        blank=True, null=True,
        help_text="Která revize je právě v řešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name_plural = "Tlakové nádoby"

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class PCHO(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="pcho")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_half_year = DateField(null=False,blank=False)
    rev_2years = DateField(null=False,blank=False)
    made = IntegerField(null=False,blank=False)
    service_life = IntegerField(null=False,blank=False) #v rokoch
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='ok', verbose_name="Současný stav")
    located = ForeignKey("viewer.Station", on_delete=SET_NULL, null=True,related_name="PCHO_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="PCHO_locations")
    is_archived = models.BooleanField(default=False)
    status_field = models.CharField(
        max_length=30,
        blank=True, null=True,
        help_text="Která revize je právě v řešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name_plural = "Proti chemicke obleky"

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"




class PA(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="pa")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_3year = DateField(null=False,blank=False)
    rev_6years = DateField(null=False,blank=False)
    rev_9years = DateField(null=False,blank=False)
    made = IntegerField(null=False,blank=False)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='ok', verbose_name="Současný stav")
    located = ForeignKey("viewer.Station", on_delete=SET_NULL, null=True,related_name="PA_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="PA_locations")
    is_archived = models.BooleanField(default=False)
    status_field = models.CharField(
        max_length=30,
        blank=True, null=True,
        help_text="Která revize je právě v řešení"
    )

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]
        verbose_name_plural = "Plucna automatika"

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class Complete(Model):
    e_number = CharField(max_length=10,null=False,blank=False)

    class Meta:
        verbose_name_plural = "Komplety"

    def __str__(self):
        p = self.parts
        return f"{self.e_number}: {p['mask']}; {p['pa']}; {p['adp']}"


    @property
    def mask(self):
        return Mask.objects.get(e_number=self.e_number)

    @property
    def pa(self):
        return PA.objects.get(e_number=self.e_number)

    @property
    def adp(self):
        choice = ADPMulti.objects.filter(e_number=self.e_number).first()
        if choice:
            return choice
        return ADPSingle.objects.get(e_number=self.e_number)

    @property
    def parts(self):
        return {
            "mask": f"{self.mask.equipment_type}, seriove cislo: {self.mask.serial_number}",
            "pa": f"{self.pa.equipment_type},seriove cislo: {self.pa.serial_number}",
            "adp": f"{self.adp.equipment_type}, seriove cislo: {self.adp.serial_number}",
        }

    def clean(self):
        error = {}
        if not Mask.objects.filter(e_number=self.e_number).exists():
            error["e_number"] = f"Maska neexistuje"
        if not PA.objects.filter(e_number=self.e_number).exists():
            error.setdefault("e_number", f"PA neexistuje")
        if not (ADPMulti.objects.filter(e_number=self.e_number).exists()
            or ADPSingle.objects.filter(e_number=self.e_number).exists()):
            error.setdefault("e_number", f"Ziadne ADP neexistuje")
        if error:
            raise ValidationError(error)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)

class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=True)


class Equipment(models.Model):
    # … ostatní pole …
    is_archived = models.BooleanField(default=False)

    objects = models.Manager()      # standardní manager
    active = ActiveManager()        # manager pro aktivní záznamy
    archived = ArchivedManager()    # manager pro archivované