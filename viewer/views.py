from django.shortcuts import render
from .models import Country, Station, City
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

# class EquipmentTypeListView(ListView):
#     model = EquipmentType
#     template_name = 'equipment/equipmenttype_list.html'
#     context_object_name = 'equipment_types'
#
#
# class EquipmentTypeCreateView(CreateView):
#     model = EquipmentType
#     fields = ['name']
#     template_name = 'equipment/equipmenttype_form.html'
#     success_url = reverse_lazy('equipmenttype_list')
#
#
# class EquipmentTypeUpdateView(UpdateView):
#     model = EquipmentType
#     fields = ['name']
#     template_name = 'equipment/equipmenttype_form.html'
#     success_url = reverse_lazy('equipmenttype_list')
#
#
# class EquipmentTypeDeleteView(DeleteView):
#     model = EquipmentType
#     template_name = 'equipment/equipmenttype_confirm_delete.html'
#     success_url = reverse_lazy('equipmenttype_list')


class StationListView(ListView):
    model = Station
    template_name = 'station/station_list.html'
    context_object_name = 'viewer'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('city__district__region__country')

        kraj = self.request.GET.get('kraj')
        okres = self.request.GET.get('okres')
        mesto = self.request.GET.get('mesto')
        stat = self.request.GET.get('stat')

        if stat:
            queryset = queryset.filter(city__district__regio__country__name__icontains=stat)
        if kraj:
            queryset = queryset.filter(city__district__region__name__icontains=kraj)
        if okres:
            queryset = queryset.filter(city__district__name__icontains=okres)
        if mesto:
            queryset = queryset.filter(city__name__icontains=mesto)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stations = self.get_queryset()

        context['stat_options'] = stations.values_list(
            'city__district__region__country__name', flat=True
        ).order_by(
            'city__district__region__country__name'
        ).distinct()
        context['kraj_options'] = stations.values_list(
            'city__district__region__name', flat=True).distinct()
        context['okres_options'] = stations.values_list(
            'city__district__name', flat=True).distinct()
        context['mesto_options'] = stations.values_list(
            'city__name', flat=True).distinct()
        return context

class StationCreateView(CreateView):
    model = Station
    fields = ['name', 'city']
    template_name = 'station/station_form.html'
    success_url = reverse_lazy('station_list')

class StationUpdateView(UpdateView):
    model = Station
    fields = ['name', 'city']
    template_name = 'station/station_form.html'
    success_url = reverse_lazy('station_list')

class StationDeleteView(DeleteView):
    model = Station
    template_name = 'station/station_confirm_delete.html'
    success_url = reverse_lazy('station_list')


class CityCreateView(CreateView):
    model = City
    fields = ['name', 'district']
    template_name = 'city/city_form.html'
    success_url = reverse_lazy('station_add')



