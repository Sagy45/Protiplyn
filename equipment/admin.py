"""Konfigurácia Django admin rozhrania pre aplikáciu equipment.

Zaregistruje všetky hlavné modely vybavenia a zobrazuje dynamicky všetky polia modelu v zozname.
"""

from django.contrib import admin
from .models import (
    EquipmentType,
    VehicleStorage,
    Mask,
    ADPMulti,
    ADPSingle,
    AirTank,
    PCHO,
    PA,
    Complete,
)


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model EquipmentType.

    Dynamicky zobrazí všetky polia modelu EquipmentType v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(VehicleStorage)
class VehicleStorageAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model VehicleStorage.

    Dynamicky zobrazí všetky polia modelu VehicleStorage v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(Mask)
class MaskAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model Mask.

    Dynamicky zobrazí všetky polia modelu Mask v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(ADPMulti)
class ADPMultiAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model ADPMulti.

    Dynamicky zobrazí všetky polia modelu ADPMulti v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(ADPSingle)
class ADPSingleAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model ADPSingle.

    Dynamicky zobrazí všetky polia modelu ADPSingle v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(AirTank)
class AirTankAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model AirTank.

    Dynamicky zobrazí všetky polia modelu AirTank v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(PCHO)
class PCHOAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model PCHO.

    Dynamicky zobrazí všetky polia modelu PCHO v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(PA)
class PAAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model PA.

    Dynamicky zobrazí všetky polia modelu PA v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]


@admin.register(Complete)
class CompleteAdmin(admin.ModelAdmin):
    """Admin rozhranie pre model Complete.

    Dynamicky zobrazí všetky polia modelu Complete v zozname v admin rozhraní.
    """

    def get_list_display(self, request):
        # Zobrazí všetky polia modelu v admin zozname.
        return [field.name for field in self.model._meta.fields]
