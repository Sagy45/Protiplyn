from django.db.models import Model, CharField, ForeignKey, SET_NULL, DateField, IntegerField
from django.core.exceptions import ValidationError

class Country(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)

    class Meta:
        verbose_name_plural = "Štát"

    def __str__(self):
        return self.name


class Region(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    country = ForeignKey("Country",on_delete=SET_NULL, null=True,related_name="regions")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Kraje"

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    region = ForeignKey("Region",on_delete=SET_NULL, null=True,related_name="districts")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Okresy"

    def __str__(self):
        return self.name


class City(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    district = ForeignKey("District",on_delete=SET_NULL, null=True,related_name="cities")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Mestá"

    def __str__(self):
        return self.name


class Station(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=True)
    city = ForeignKey("City", on_delete=SET_NULL, null=True, related_name="stations")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Stanice"

    def __str__(self):
        return self.name


class EquipmentType(Model):
    name = CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class VehicleStorage(Model):
    brand = CharField(max_length=100, null=False, blank=False)
    spz = CharField(max_length=7, null=True, blank=True)
    station = ForeignKey("Station", on_delete=SET_NULL, null=True, related_name="stations")

    class Meta:
        ordering = ["brand"]

    def __str__(self):
        return f" {self.brand} {self.spz}"


class MaskOver(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="masks_over")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_2years = DateField(null=False,blank=False)
    rev_4years = DateField(null=False,blank=False)
    rev_6years = DateField(null=False,blank=False)
    extra_1 = DateField(null=False,blank=False)
    extra_2 = DateField(null=False,blank=False)
    status = CharField(max_length=20,null=False,blank=False)
    located = ForeignKey("Station", on_delete=SET_NULL, null=True,related_name="MO_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="MO_locations")

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class ADPMulti(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="adp_m")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_1years = DateField(null=False,blank=False)
    rev_6years = DateField(null=False,blank=False)
    status = CharField(max_length=20,null=False,blank=False)
    located = ForeignKey("Station", on_delete=SET_NULL, null=True,related_name="ADPm_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="ADMm_locations")

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class ADPSingle(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="adp_s")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_1years = DateField(null=False,blank=False)
    rev_9years = DateField(null=False,blank=False)
    status = CharField(max_length=20,null=False,blank=False)
    located = ForeignKey("Station", on_delete=SET_NULL, null=True,related_name="ADPs_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="ADPs_locations")

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]

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
    status = CharField(max_length=20,null=False,blank=False)
    located = ForeignKey("Station", on_delete=SET_NULL, null=True,related_name="AirTank_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="AirTank_locations")

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]

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
    status = CharField(max_length=20,null=False,blank=False)
    located = ForeignKey("Station", on_delete=SET_NULL, null=True,related_name="PCHO_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="PCHO_locations")

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class MaskUnder(Model):
    equipment_type = ForeignKey("EquipmentType",on_delete=SET_NULL, null=True,related_name="mask_under")
    type = CharField(max_length=50,null=False,blank=False)
    e_number = CharField(max_length=10,null=False,blank=False)
    serial_number = CharField(max_length=50,null=False,blank=False)
    rev_5years = DateField(null=False,blank=False)
    status = CharField(max_length=20,null=False,blank=False)
    located = ForeignKey("Station", on_delete=SET_NULL, null=True,related_name="MU_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="MU_locations")

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]

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
    status = CharField(max_length=20,null=False,blank=False)
    located = ForeignKey("Station", on_delete=SET_NULL, null=True,related_name="PA_located_stations")
    location = ForeignKey("VehicleStorage", on_delete=SET_NULL, null=True,related_name="PA_locations")

    class Meta:
        ordering = ["equipment_type", "type", "e_number"]

    def __str__(self):
        return f" {self.equipment_type} {self.type} {self.e_number}"


class Complete(Model):
    e_number = CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        p = self.parts
        return f"{self.e_number}: {p['mask']}; {p['pa']}; {p['adp']}"


    @property
    def mask(self):
        return MaskOver.objects.get(e_number=self.e_number)

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
        if not MaskOver.objects.filter(e_number=self.e_number).exists():
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
