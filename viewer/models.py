from django.db.models import Model, CharField, ForeignKey, SET_NULL


class Country(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)


    def __str__(self):
        return self.name

class Region(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    country = ForeignKey("Country",on_delete=SET_NULL,related_name="regions")

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return self.name

class District(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    region = ForeignKey("Region",on_delete=SET_NULL,related_name="districts")

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return self.name

class City(Model):
    name = CharField(max_length=100,null=False,blank=False,unique=True)
    district = ForeignKey("District",on_delete=SET_NULL,related_name="cities")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Station(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=True)
    city = ForeignKey("City", on_delete=SET_NULL, related_name="stations")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
