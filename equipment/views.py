from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import  get_object_or_404
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

from viewer.models import Station
from .models import  VehicleStorage, Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, Complete, \
    REVISION_LABELS, STATUS_CHOICES
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .models import EquipmentType

from django.shortcuts import render, redirect


def equipment_search(request):
    # Ziska hodnotu z GET parametru 'serial_number' (z formulare), odstrani bile znaky okolo
    serial_number = request.GET.get("serial_number", "").strip()
    if serial_number:
        #Mapovani nazvu modelu (jako string) na tridy modelu
        model_map = {
            "Mask": Mask,
            "ADPMulti": ADPMulti,
            "ADPSingle": ADPSingle,
            "AirTank": AirTank,
            "PCHO": PCHO,
            "PA": PA,
        }
        # Projde vsechny modely a zkusi najit objekt podle e_number
        for model_name, model_class in model_map.items():
            try:
                # Hleda zaznam v danem modelu, ignoruje velikost pismen (iexact)
                obj = model_class.objects.get(serial_number__iexact=serial_number)
                return redirect(reverse("equipment_detail", args=[model_name, obj.pk]))
            except model_class.DoesNotExist:
                # Pokud dany model zaznam nema, pokracuje dal
                continue
    # Pokud se nic nenaslo, zobrazi stranku s hlaskou, ze se nic nenaslo
    return render(request, "equipment/search_not_found.html", {"query": serial_number})

class HomeView(ListView):
    model = EquipmentType
    template_name = 'equipment/equipmenttype_list.html'
    context_object_name = 'equipment_types'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

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






MODEL_MAP = {
        "Mask": Mask,
        "ADPMulti": ADPMulti,
        "ADPSingle": ADPSingle,
        "AirTank": AirTank,
        "PCHO": PCHO,
        "PA": PA,
    }

REVISION_FIELDS = [
    "rev_half_year", "rev_1years", "rev_2years",
    "rev_3year", "rev_4years", "rev_5years",
    "rev_6years", "rev_9years",
    "extra_1", "extra_2"
]

REVISION_LABELS = {
    "rev_half_year": "Polročná",
    "rev_1years": "1 ročná",
    "rev_2years": "2 ročná",
    "rev_3year": "3 ročná",
    "rev_4years": "4 ročná",
    "rev_5years": "5 ročná",
    "rev_6years": "6 ročná",
    "rev_9years": "9 ročná",
    "extra_1": "Extra 1",
    "extra_2": "Extra 2",
}

REVISION_INTERVALS = {
    'rev_half_year': timedelta(days=182),
    'rev_1years': timedelta(days=365),
    'rev_2years': timedelta(days=730),
    'rev_3year': timedelta(days=1095),
    'rev_4years': timedelta(days=1460),
    'rev_5years': timedelta(days=1825),
    'rev_6years': timedelta(days=2190),
    'rev_9years': timedelta(days=3285),
}

class StationEquipmentListView(TemplateView):
    template_name = 'equipment/station_equipment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station = get_object_or_404(Station, pk=self.kwargs['pk'])
        context['station'] = station
        context['STATUS_CHOICES'] = STATUS_CHOICES

        today = date.today()
        one_month = today + timedelta(days=30)
        three_months = today + timedelta(days=90)

        sections = []
        for label, model, _, _, fields, model_name in [
            ("Masky", Mask, None, None, ["type", "e_number", "serial_number", "rev_2years", "rev_4years", "rev_6years", "extra_1", "extra_2"], "Mask"),
            ("ADP Multi", ADPMulti, None, None, ["type", "e_number", "serial_number", "rev_1years", "rev_6years"], "ADPMulti"),
            ("ADP Single", ADPSingle, None, None, ["type", "e_number", "serial_number", "rev_1years", "rev_9years"], "ADPSingle"),
            ("Tlakové nádoby", AirTank, None, None, ["type", "e_number", "serial_number", "rev_5years"], "AirTank"),
            ("PCHO", PCHO, None, None, ["type", "e_number", "serial_number", "rev_half_year", "rev_2years"], "PCHO"),
            ("PA", PA, None, None, ["type", "e_number", "serial_number", "rev_3year", "rev_6years", "rev_9years"], "PA"),
        ]:
            queryset = model.objects.filter(located=station)
            for eq in queryset:
                eq.status_map = {}
                for f in REVISION_FIELDS:
                    rev_date = getattr(eq, f, None)
                    if rev_date:
                        if rev_date <= one_month:
                            eq.status_map[f] = 'critical'
                        elif rev_date <= three_months:
                            eq.status_map[f] = 'bsr'
                        else:
                            eq.status_map[f] = 'ok'
            pretty_fields = [(f, REVISION_LABELS.get(f, f.capitalize())) for f in fields]
            sections.append((label, queryset, pretty_fields, model_name))
        context['equipment_sections'] = sections
        return context



class UpcomingRevisionListView(TemplateView):
    template_name = 'equipment/upcoming_revisions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        today = timezone.now().date()
        three_months = today + timedelta(days=90)
        one_month = today + timedelta(days=30)

        # Get stations user can see:
        if hasattr(user.profile, "region") and user.profile.region:
            stations = user.profile.region.stations.all()
        elif hasattr(user.profile, "district") and user.profile.district:
            stations = user.profile.district.stations.all()
        elif hasattr(user.profile, "station") and user.profile.station:
            stations = [user.profile.station]
        else:
            stations = []  # fallback, user can't see anything

        # Build filter for allowed stations
        station_filter = Q(located__in=stations)

        def filter_items(model, fields):
            qs = model.objects.filter(station_filter)
            results = []
            for item in qs:
                relevant_dates = []
                for f in fields:
                    d = getattr(item, f)
                    if d and today <= d <= three_months:
                        relevant_dates.append((f, d))
                if relevant_dates:
                    item.relevant_dates = relevant_dates
                    item.is_red = any(d <= one_month for _, d in relevant_dates)
                    results.append(item)
            return results

        context['groups'] = [
            ("Masky", filter_items(Mask, ["rev_2years", "rev_4years", "rev_6years", "extra_1", "extra_2"])),
            ("ADP Multi", filter_items(ADPMulti, ["rev_1years", "rev_6years"])),
            ("ADP Single", filter_items(ADPSingle, ["rev_1years", "rev_9years"])),
            ("Tlakové nádoby", filter_items(AirTank, ["rev_5years"])),
            ("PCHO", filter_items(PCHO, ["rev_half_year", "rev_2years"])),
            ("PA", filter_items(PA, ["rev_3year", "rev_6years", "rev_9years"])),
        ]

        return context


class EquipmentDetailView(DetailView):
    template_name = "equipment/equipment_detail.html"

    def get_queryset(self):
        model = MODEL_MAP.get(self.kwargs['model'])
        if not model:
            raise Http404("Unknown model")
        return model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['REVISION_LABELS'] = REVISION_LABELS  # so template has labels
        # pass only the revision fields
        context['revision_fields'] = [f for f in self.object.__dict__.keys() if f.startswith('rev') or f.startswith('extra')]
        return context


@csrf_protect
@login_required
def update_status_form(request):
    if request.method == "POST":
        model_name = request.POST.get("model")
        obj_id = request.POST.get("id")
        field = request.POST.get("field")
        new_status = request.POST.get("status")

        model = MODEL_MAP.get(model_name)
        if not model:
            return JsonResponse({"error": "Invalid model"}, status=400)

        obj = model.objects.get(pk=obj_id)

        # If your objects have status_map dict (optional)
        if hasattr(obj, "status_map"):
            obj.status_map[field] = new_status

        # Bump date if status = OK
        if new_status == "ok" and field in REVISION_INTERVALS:
            setattr(obj, field, timezone.now().date() + REVISION_INTERVALS[field])

        obj.save()

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)