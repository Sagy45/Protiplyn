from django.db.models import Model, CharField, ForeignKey, SET_NULL


class Country(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)

    class Meta:
        verbose_name = "Štát"
        verbose_name_plural = "Štáty"


    def __str__(self):
        return self.name

class Region(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    country = ForeignKey("Country",on_delete=SET_NULL,related_name="regions", null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Kraj"
        verbose_name_plural = "Kraje"


    def __str__(self):
        return self.name

class District(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    region = ForeignKey("Region",on_delete=SET_NULL,related_name="districts", null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Okres"
        verbose_name_plural = "Okresy"


    def __str__(self):
        return self.name

class City(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    district = ForeignKey("District",on_delete=SET_NULL,related_name="cities", null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Mesto"
        verbose_name_plural = "Mestá"

    def __str__(self):
        return self.name


class Station(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=True)
    city = ForeignKey("City", on_delete=SET_NULL, related_name="stations", null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Stanica"
        verbose_name_plural = "Stanice"

    def __str__(self):
        return self.name
