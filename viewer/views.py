from django.shortcuts import render

from equipment.models import EquipmentType, Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, STATUS_CHOICES
from equipment.views import MODEL_MAP, REVISION_INTERVALS
from .models import Country, Station, City
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from datetime import timedelta
from django.utils import timezone
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from datetime import datetime


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
        queryset = super().get_queryset().select_related('city__district__region__country')

        kraj = self.request.GET.get('kraj')
        okres = self.request.GET.get('okres')
        mesto = self.request.GET.get('mesto')
        stat = self.request.GET.get('stat')

        if stat:
            queryset = queryset.filter(city__district__region__country__name__icontains=stat)
        if kraj:
            queryset = queryset.filter(city__district__region__name__icontains=kraj)
        if okres:
            queryset = queryset.filter(city__district__name__icontains=okres)
        if mesto:
            queryset = queryset.filter(city__name__icontains=mesto)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        stat = self.request.GET.get('stat')
        kraj = self.request.GET.get('kraj')
        okres = self.request.GET.get('okres')
        mesto = self.request.GET.get('mesto')

        all_stations = Station.objects.select_related('city__district__region__country')

        # Filtered for table
        filtered = all_stations
        if stat:
            filtered = filtered.filter(city__district__region__country__name__icontains=stat)
        if kraj:
            filtered = filtered.filter(city__district__region__name__icontains=kraj)
        if okres:
            filtered = filtered.filter(city__district__name__icontains=okres)
        if mesto:
            filtered = filtered.filter(city__name__icontains=mesto)

        context['stations'] = filtered

        # Dropdown logika

        # Pre stat = vsetko
        context['stat_options'] = all_stations.values_list(
            'city__district__region__country__name', flat=True
        ).order_by('city__district__region__country__name').distinct()

        # Okres: limit  Mesto/Kraj
        regions_qs = all_stations
        if stat:
            regions_qs = regions_qs.filter(city__district__region__country__name__icontains=stat)
        if okres:
            regions_qs = regions_qs.filter(city__district__name__icontains=okres)
        if mesto:
            regions_qs = regions_qs.filter(city__name__icontains=mesto)
        context['kraj_options'] = regions_qs.values_list(
            'city__district__region__name', flat=True
        ).order_by('city__district__region__name').distinct()

        # Kraj: limit Okres/Mesto
        districts_qs = all_stations
        if kraj:
            districts_qs = districts_qs.filter(city__district__region__name__icontains=kraj)
        if mesto:
            districts_qs = districts_qs.filter(city__name__icontains=mesto)
        context['okres_options'] = districts_qs.values_list(
            'city__district__name', flat=True
        ).order_by('city__district__name').distinct()

        # Mesta: limit Kraj/Okres
        cities_qs = all_stations
        if okres:
            cities_qs = cities_qs.filter(city__district__name__icontains=okres)
        if kraj:
            cities_qs = cities_qs.filter(city__district__region__name__icontains=kraj)
        context['mesto_options'] = cities_qs.values_list(
            'city__name', flat=True
        ).order_by('city__name').distinct()

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

station_prefix_map = {
    1:"BB",
    19: "ZM",
    20: "BA",
    21: "NR",
    # add more if needed
}


class StationEquipmentListView(TemplateView):
    template_name = 'viewer/station_equipment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station = get_object_or_404(Station, pk=self.kwargs['pk'])

        # ✅ NEW: use the prefix dynamically
        prefix = station.prefix or ""

        context['station'] = station
        context['STATUS_CHOICES'] = STATUS_CHOICES

        context['equipment_sections'] = [
            ("Masky",
             Mask.objects.filter(e_number__startswith=prefix),
             None, None,
             ["type", "e_number", "serial_number",
              "rev_2years", "rev_4years", "rev_6years",
              "extra_1", "extra_2", "status"],
             "Mask"),

            ("ADP Multi",
             ADPMulti.objects.filter(e_number__startswith=prefix),
             None, None,
             ["type", "e_number", "serial_number",
              "rev_1years", "rev_6years",
              "status"],
             "ADPMulti"),

            ("ADP Single",
             ADPSingle.objects.filter(e_number__startswith=prefix),
             None, None,
             ["type", "e_number", "serial_number",
              "rev_1years", "rev_9years",
              "status"],
             "ADPSingle"),

            ("Vzduchové bomby",
             AirTank.objects.filter(e_number__startswith=prefix),
             None, None,
             ["type", "e_number", "serial_number",
              "rev_5years",
              "status"],
             "AirTank"),

            ("PCHO",
             PCHO.objects.filter(e_number__startswith=prefix),
             None, None,
             ["type", "e_number", "serial_number",
              "rev_half_year", "rev_2years",
              "status"],
             "PCHO"),

            ("PA",
             PA.objects.filter(e_number__startswith=prefix),
             None, None,
             ["type", "e_number", "serial_number",
              "rev_3year", "rev_6years", "rev_9years",
              "status"],
             "PA"),
        ]

        # ✅ Debug: check what comes back
        for section in context['equipment_sections']:
            print("Section:", section[0])
            for item in section[1]:
                print("  ", item.e_number, item.type)
                for field in section[4]:
                    print(f"    {field} = ", getattr(item, field, "MISSING"))

        return context



@csrf_protect
@login_required
def update_status_form(request):
    if request.method == "POST":
        model_name = request.POST.get("model")
        obj_id = request.POST.get("id")
        field = request.POST.get("field")
        new_status = request.POST.get("status")
        revise_from_str = request.POST.get("revise_from_date")

        print(f"MODEL: {model_name}")
        print(f"ID: {obj_id}")
        print(f"FIELD: {field}")
        print(f"NEW STATUS: {new_status}")
        print(f"REVIZE OD DATA: {revise_from_str}")

        # Nově: načti datum z formuláře (volitelné)
        revise_from_date = None
        if revise_from_str:
            try:
                revise_from_date = datetime.strptime(revise_from_str, "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"error": "Neplatný formát data"}, status=400)

        model = MODEL_MAP.get(model_name)
        if not model:
            return JsonResponse({"error": "Invalid model"}, status=400)

        obj = model.objects.get(pk=obj_id)

        if new_status == "ok" and field in REVISION_INTERVALS:
            base_date = revise_from_date or getattr(obj, field, None)
            if base_date:
                new_date = base_date + REVISION_INTERVALS[field]
                setattr(obj, field, new_date)

        obj.status = new_status
        obj.save()

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)





