from django.shortcuts import render
from .models import Country, EquipmentType
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.

def country_detail_full(request):
    country = Country.objects.first()  # vezmu jedinou zemi, vic jich nemame

    if not country:
        return render(request, 'viewer/no_country.html')  # pokud neni zaznam v DB ale to se tady asi nestane

    regions = country.regions.prefetch_related(
        'districts__cities__stations'
    ) # nacti vsechny regiony pro zemi a zaroven prednacti okresy, mesta a stanice
      # abychom se vyhnuly N+1 dotazum - podle vseho lepsi vykon

    return render(request, 'viewer/country_detail_full.html', {
        'country': country,
        'regions': regions,
    })

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