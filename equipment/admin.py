
from django.contrib import admin
from .models import EquipmentType, VehicleStorage, Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, Complete


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(VehicleStorage)
class VehicleStorageAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(Mask)
class MaskAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(ADPMulti)
class ADPMultiAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(ADPSingle)
class ADPSingleAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(AirTank)
class AirTankAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(PCHO)
class PCHOAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(PA)
class PAAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

@admin.register(Complete)
class CompleteAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]