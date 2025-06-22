from django.shortcuts import render

from viewer.models import Station
from .models import EquipmentType, VehicleStorage, Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, Complete
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta

class EquipmentTypeListView(ListView):
    model = EquipmentType
    template_name = 'equipment/equipmenttype_list.html'
    context_object_name = 'equipment_types'


class EquipmentTypeCreateView(CreateView):
    model = EquipmentType
    fields = ['name']
    template_name = 'equipment/equipmenttype_form.html'
    success_url = reverse_lazy('equipmenttype_list')


class EquipmentTypeUpdateView(UpdateView):
    model = EquipmentType
    fields = ['name']
    template_name = 'equipment/equipmenttype_form.html'
    success_url = reverse_lazy('equipmenttype_list')


class EquipmentTypeDeleteView(DeleteView):
    model = EquipmentType
    template_name = 'equipment/equipmenttype_confirm_delete.html'
    success_url = reverse_lazy('equipmenttype_list')


class VehicleStorageListView(ListView):
    model = VehicleStorage
    template_name = 'equipment/vehicle_list.html'
    context_object_name = 'vehicle_storages'


class VehicleStorageCreateView(CreateView):
    model = VehicleStorage
    fields = '__all__'
    template_name = 'equipment/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')


class VehicleStorageUpdateView(UpdateView):
    model = VehicleStorage
    fields = '__all__'
    template_name = 'equipment/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')


class VehicleStorageDeleteView(DeleteView):
    model = VehicleStorage
    template_name = 'equipment/vehicle_confirm_delete.html'
    reverse_url = reverse_lazy('vehicle_list')


class MaskListView(ListView):
    model = Mask
    template_name = 'equipment/mask_list.html'
    context_object_name = 'masks'


class MaskCreateView(CreateView):
    model = Mask
    fields = '__all__'
    template_name = 'equipment/mask_form.html'
    success_url = reverse_lazy('mask_list')


class MaskUpdateView(UpdateView):
    model = Mask
    fields = '__all__'
    template_name = 'equipment/mask_form.html'
    success_url = reverse_lazy('mask_list')


class MaskDeleteView(DeleteView):
    model = Mask
    template_name = 'equipment/mask_confirm_delete.html'
    reverse_url = reverse_lazy('mask_list')


class ADPMultiListView(ListView):
    model = ADPMulti
    template_name = 'equipment/adpmulti_list.html'
    context_object_name = 'adp_multis'


class ADPMultiCreateView(CreateView):
    model = ADPMulti
    fields = '__all__'
    template_name = 'equipment/adpmulti_form.html'
    success_url = reverse_lazy('adpmulti_list')


class ADPMultiUpdateView(UpdateView):
    model = ADPMulti
    fields = '__all__'
    template_name = 'equipment/adpmulti_form.html'
    success_url = reverse_lazy('adpmulti_list')


class ADPMultiDeleteView(DeleteView):
    model = ADPMulti
    template_name = 'equipment/adpmulti_confirm_delete.html'
    reverse_url = reverse_lazy('adpmulti_list')


class ADPSingleListView(ListView):
    model = ADPSingle
    template_name = 'equipment/adpsingle_list'
    context_object_name = 'adp_singles'


class ADPSingleCreateView(CreateView):
    model = ADPSingle
    fields = '__all__'
    template_name = 'equipment/adpsingle_form.html'
    success_url = reverse_lazy('adpsingle_list')


class ADPSingleUpdateView(UpdateView):
    model = ADPSingle
    fields = '__all__'
    template_name = 'equipment/adpsingle_form.html'
    success_url = reverse_lazy('adpsingle_list')


class ADPSingleDeleteView(DeleteView):
    model = ADPSingle
    template_name = 'equipment/adpsingle_confirm_delete.html'
    success_url = reverse_lazy('adpsingle_list')


class AirTankListView(ListView):
    model = AirTank
    template_name = 'equipment/airtank_list'
    context_object_name = 'airtanks'


class AirTankCreateView(CreateView):
    model = AirTank
    fields = '__all__'
    template_name = 'equipment/airtank_form.html'
    success_url = reverse_lazy('airtank_list')

class AirTankUpdateView(UpdateView):
    model = AirTank
    fields = '__all__'
    template_name = 'equipment/airtank_form.html'


class AirTankDeleteView(DeleteView):
    model = AirTank
    template_name = 'equipment/airtank_confirm_delete.html'
    success_url = reverse_lazy('airtank_list')


class PCHOListView(ListView):
    model = PCHO
    template_name = 'equipment/pcho_list.html'
    context_object_name = 'pchos'


class PCHOCreateView(CreateView):
    model = PCHO
    fields = '__all__'
    template_name = 'equipment/pcho_form.html'
    success_url = reverse_lazy('pcho_list')


class PCHOUpdateView(UpdateView):
    model = PCHO
    fields = '__all__'
    template_name = 'equipment/pcho_form.html'
    success_url = reverse_lazy('pcho_list')


class PCHODeleteView(DeleteView):
    model = PCHO
    template_name = 'equipment/pcho_confirm_delete.html'
    success_url = reverse_lazy('pcho_list')


class PAListView(ListView):
    model = PA
    template_name = 'equipment/pa_list.html'
    context_object_name = 'pas'


class PACreateView(CreateView):
    model = PA
    fields = '__all__'
    template_name = 'equipment/pa_form.html'
    success_url = reverse_lazy('pa_list')


class PAUpdateView(UpdateView):
    model = PA
    fields = '__all__'
    template_name = 'equipment/pa_form.html'
    success_url = reverse_lazy('pa_list')


class PADeleteView(DeleteView):
    model = PA
    template_name = 'equipment/pa_confirm_delete.html'
    success_url = reverse_lazy('pa_list')


class CompleteListView(ListView):
    model = Complete
    template_name = 'equipment/complete_list.html'
    context_object_name = 'completes'


class CompleteCreateView(CreateView):
    model = Complete
    fields = '__all__'
    template_name = 'equipment/complete_form.html'
    success_url = reverse_lazy('complete_list')


class CompleteUpdateView(UpdateView):
    model = Complete
    fields = '__all__'
    template_name = 'equipment/complete_form.html'
    success_url = reverse_lazy('complete_list')


class CompleteDeleteView(DeleteView):
    model = Complete
    template_name = 'equipment/complete_confirm_delete.html'
    success_url = reverse_lazy('complete_list')


class StationEquipmentListView(DetailView):
    model = Station
    template_name = 'equipment/station_equipment.html'
    context_object_name = 'station'

    def get_context_data(self, **kwargs):
        context = super(StationEquipmentListView, self).get_context_data(**kwargs)
        station = self.get_object()

        context['equipment_sections'] = [
            ("Masky", Mask.objects.filter(located=station), 'mask_edit', 'mask_delete',
             ['type', 'e_number', 'serial_number', 'status']),
            ("ADP Multi", ADPMulti.objects.filter(located=station), 'adpmulti_edit', 'adpmulti_delete',
             ['type', 'e_number', 'serial_number', 'status']),
            ("ADP Single", ADPSingle.objects.filter(located=station), 'adpsingle_edit', 'adpsingle_delete',
             ['type', 'e_number', 'serial_number', 'status']),
            ("Tlakové lahve", AirTank.objects.filter(located=station), 'airtank_edit', 'airtank_delete',
             ['serial_number', 'rev_date', 'status']),
            ("Chemické obleky", PCHO.objects.filter(located=station), 'pcho_edit', 'pcho_delete',
             ['type', 'serial_number', 'rev_date', 'status']),
            ("PA", PA.objects.filter(located=station), 'pa_edit', 'pa_delete', ['type', 'serial_number', 'status']),
        ]

        return context


class UpcomingRevisionListView(TemplateView):
    template_name = 'equipment/upcoming_revisions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        soon = today + timedelta(days=30)

        def in_range(qs, *fields):
            from django.db.models import Q
            q = Q()
            for field in fields:
                kwargs = {f"{field}__lte": soon, f"{field}__gte": today}
                q |= Q(**kwargs)
            return qs.filter(q)

        mask = in_range(Mask.objects.all(), "rev_2years", "rev_4years", "rev_6years", "extra_1", "extra_2")
        adpmulti = in_range(ADPMulti.objects.all(), "rev_1years", "rev_6years")
        adpsingle = in_range(ADPSingle.objects.all(), "rev_1years", "rev_9years")
        airtank = in_range(AirTank.objects.all(), "rev_5years")
        pcho = in_range(PCHO.objects.all(), "rev_half_year", "rev_2years")
        pa = in_range(PA.objects.all(), "rev_3year", "rev_6years", "rev_9years")

        context["equipment_groups"] = [
            ("Masky", mask),
            ("ADP Multi", adpmulti),
            ("ADP Single", adpsingle),
            ("Vzduchové bomby", airtank),
            ("PCHO", pcho),
            ("PA", pa),
        ]

        context["today"] = today
        context["soon"] = soon
        return context
