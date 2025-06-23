from django.db.models import Model, CharField, ForeignKey, SET_NULL


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

    # def __str__(self):
    #     return self.name

    def __str__(self):
        parts = []
        if self.country:
            parts.append(self.country.name)
        parts.append(self.name)
        return " - ".join(parts)


class District(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    region = ForeignKey("Region",on_delete=SET_NULL, null=True,related_name="districts")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Okresy"

    # def __str__(self):
    #     return self.name

    def __str__(self):
        parts = []
        if self.region:
            parts.append(str(self.region))
        parts.append(self.name)
        return " - ".join(parts)


class City(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    district = ForeignKey("District",on_delete=SET_NULL, null=True,related_name="cities")

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Mestá"

    # def __str__(self):
    #     return self.name

    def __str__(self):
        parts = []
        if self.district:
            parts.append(str(self.district))
        parts.append(self.name)
        return " - ".join(parts)


class Station(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=True)
    city = ForeignKey("City", on_delete=SET_NULL, null=True, related_name="stations")
    prefix = CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Stanice"

    # def __str__(self):
    #     return self.name

    def __str__(self):
        parts = []
        if self.city:
            parts.append(str(self.city))
        parts.append(self.name)
        return " - ".join(parts)


