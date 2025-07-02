from django.shortcuts import render

from equipment.models import EquipmentType, Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, STATUS_CHOICES
from equipment.views import MODEL_MAP, REVISION_INTERVALS
from .models import Country, Station, City
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from accounts.models import Profile


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


class StationListView(ListView):
    model = Station
    template_name = 'station/station_list.html'
    context_object_name = 'stations'

    def get_queryset(self):
        user     = self.request.user
        profile  = getattr(user, 'profile', None)

        # 1) Základní omezení podle role
        qs = Station.objects.select_related(
            'city__district__region__country'
        )
        if profile and profile.role == Profile.ROLE_TECHNICIAN:
            # Technik vidí jen svou stanici
            if profile.station:
                qs = qs.filter(pk=profile.station.pk)
            else:
                qs = qs.none()
        # pokud je admin (role == admin), vidí vše

        # 2) Aplikace filtrovaní podle GET parametrů
        stat  = self.request.GET.get('stat')
        kraj  = self.request.GET.get('kraj')
        okres = self.request.GET.get('okres')
        mesto = self.request.GET.get('mesto')

        if stat:
            qs = qs.filter(city__district__region__country__name__icontains=stat)
        if kraj:
            qs = qs.filter(city__district__region__name__icontains=kraj)
        if okres:
            qs = qs.filter(city__district__name__icontains=okres)
        if mesto:
            qs = qs.filter(city__name__icontains=mesto)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_stations = Station.objects.select_related('city__district__region__country')

        stat  = self.request.GET.get('stat')
        kraj  = self.request.GET.get('kraj')
        okres = self.request.GET.get('okres')
        mesto = self.request.GET.get('mesto')

        context['stat_options'] = all_stations.values_list(
            'city__district__region__country__name', flat=True
        ).distinct().order_by('city__district__region__country__name')

        regions_qs = all_stations
        if stat:
            regions_qs = regions_qs.filter(city__district__region__country__name__icontains=stat)
        if okres:
            regions_qs = regions_qs.filter(city__district__name__icontains=okres)
        if mesto:
            regions_qs = regions_qs.filter(city__name__icontains=mesto)
        context['kraj_options'] = regions_qs.values_list(
            'city__district__region__name', flat=True
        ).distinct().order_by('city__district__region__name')

        districts_qs = all_stations
        if kraj:
            districts_qs = districts_qs.filter(city__district__region__name__icontains=kraj)
        if mesto:
            districts_qs = districts_qs.filter(city__name__icontains=mesto)
        context['okres_options'] = districts_qs.values_list(
            'city__district__name', flat=True
        ).distinct().order_by('city__district__name')

        cities_qs = all_stations
        if okres:
            cities_qs = cities_qs.filter(city__district__name__icontains=okres)
        if kraj:
            cities_qs = cities_qs.filter(city__district__region__name__icontains=kraj)
        context['mesto_options'] = cities_qs.values_list(
            'city__name', flat=True
        ).distinct().order_by('city__name')

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



