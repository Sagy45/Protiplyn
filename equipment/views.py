from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import timedelta, date, datetime
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect

from viewer.models import Station
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    DetailView,
)
from django.urls import reverse_lazy, reverse
from .models import EquipmentType
from django.views import View
from .models import (
    Mask,
    VehicleStorage,
    ADPMulti,
    ADPSingle,
    AirTank,
    PCHO,
    PA,
    Complete,
    REVISION_FIELDS,
    REVISION_LABELS,
    STATUS_CHOICES,
    Equipment,
)

ALLOWED = {
    "ok": ["vyradit"],
    "bsr": ["vyradit", "under_revision"],
    "critical": ["vyradit", "under_revision"],
    "under_revision": ["ok", "vyradit"],
}


def get_allowed_trransitions(current_status):
    """
    Vráti zoznam možných prechodov stavu pre daný status.

    Args:
        current_status (str): Aktuálny stav.

    Returns:
        list: Zoznam dvojíc (status, popis).
    """
    label_map = {
        "ok": "OK",
        "bsr": "BSR",
        "critical": "Kriticky",
        "under_revision": "V riešení",
        "vyradit": "Vyradiť",
    }
    choices = []
    for s in ALLOWED.get(current_status, []):
        choices.append((s, label_map.get(s, s.capitalize())))
    return choices


def equipment_search(request):
    """
    Vyhľadáva vybavenie podľa sériového čísla a presmeruje na detail.

    Args:
        request (HttpRequest): HTTP požiadavka s GET parametrom 'serial_number'.

    Returns:
        HttpResponse: Presmerovanie na detail nájdeného vybavenia,
        alebo stránka s hláškou ak nič nebolo nájdené.
    """
    serial_number = request.GET.get("serial_number", "").strip()
    next_url = (
        request.GET.get("next")
        or request.META.get("HTTP_REFERER")
        or reverse("station_list")
    )

    if serial_number:
        model_map = {
            "Mask": Mask,
            "ADPMulti": ADPMulti,
            "ADPSingle": ADPSingle,
            "AirTank": AirTank,
            "PCHO": PCHO,
            "PA": PA,
        }
        for model_name, model_class in model_map.items():
            try:
                obj = model_class.objects.get(serial_number__iexact=serial_number)
                return redirect(reverse("equipment_detail", args=[model_name, obj.pk]))
            except model_class.DoesNotExist:
                continue
    return render(
        request,
        "equipment/search_not_found.html",
        {
            "query": serial_number,
            "next_url": next_url,
        },
    )


class HomeView(ListView):
    """
    Prehľad typov vybavenia (úvodná stránka equipment).

    Zobrazuje zoznam všetkých typov vybavenia.
    """

    model = EquipmentType
    template_name = "equipment/equipmenttype_list.html"
    context_object_name = "equipment_types"

    def dispatch(self, request, *args, **kwargs):
        """
        Overí prihlásenie používateľa.
        """
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


class EquipmentTypeListView(ListView):
    """
    Zoznam všetkých typov vybavenia.
    """

    model = EquipmentType
    template_name = "equipment/equipmenttype_list.html"
    context_object_name = "equipment_types"


class EquipmentTypeCreateView(CreateView):
    """
    Vytvorenie nového typu vybavenia.
    """

    model = EquipmentType
    fields = ["name"]
    template_name = "equipment/equipmenttype_form.html"
    success_url = reverse_lazy("equipmenttype_list")


class EquipmentTypeUpdateView(UpdateView):
    """
    Editácia typu vybavenia.
    """

    model = EquipmentType
    fields = ["name"]
    template_name = "equipment/equipmenttype_form.html"
    success_url = reverse_lazy("equipmenttype_list")


class EquipmentTypeDeleteView(DeleteView):
    """
    Vymazanie typu vybavenia.
    """

    model = EquipmentType
    template_name = "equipment/equipmenttype_confirm_delete.html"
    success_url = reverse_lazy("equipmenttype_list")


class VehicleStorageListView(ListView):
    """
    Zoznam všetkých skladov a vozidiel.
    """

    model = VehicleStorage
    template_name = "equipment/vehicle_list.html"
    context_object_name = "vehicle_storages"


class VehicleStorageCreateView(CreateView):
    """
    Pridanie skladu alebo vozidla.
    """

    model = VehicleStorage
    fields = "__all__"
    template_name = "equipment/vehicle_form.html"
    success_url = reverse_lazy("vehicle_list")


class VehicleStorageUpdateView(UpdateView):
    """
    Editácia skladu alebo vozidla.
    """

    model = VehicleStorage
    fields = "__all__"
    template_name = "equipment/vehicle_form.html"
    success_url = reverse_lazy("vehicle_list")


class VehicleStorageDeleteView(DeleteView):
    """
    Vymazanie skladu alebo vozidla.
    """

    model = VehicleStorage
    template_name = "equipment/vehicle_confirm_delete.html"
    reverse_url = reverse_lazy("vehicle_list")


class MaskListView(ListView):
    """
    Zoznam všetkých masiek.
    """

    model = Mask
    template_name = "equipment/mask_list.html"
    context_object_name = "masks"


class MaskCreateView(CreateView):
    """
    Pridanie novej masky.
    """

    model = Mask
    fields = "__all__"
    template_name = "equipment/mask_form.html"
    success_url = reverse_lazy("mask_list")


class MaskUpdateView(UpdateView):
    """
    Editácia masky.
    """

    model = Mask
    fields = "__all__"
    template_name = "equipment/mask_form.html"
    success_url = reverse_lazy("mask_list")


class MaskDeleteView(DeleteView):
    """
    Vymazanie masky.
    """

    model = Mask
    template_name = "equipment/mask_confirm_delete.html"
    reverse_url = reverse_lazy("mask_list")


class ADPMultiListView(ListView):
    """
    Zoznam všetkých ADP Multi.
    """

    model = ADPMulti
    template_name = "equipment/adpmulti_list.html"
    context_object_name = "adp_multis"


class ADPMultiCreateView(CreateView):
    """
    Pridanie ADP Multi.
    """

    model = ADPMulti
    fields = "__all__"
    template_name = "equipment/adpmulti_form.html"
    success_url = reverse_lazy("adpmulti_list")


class ADPMultiUpdateView(UpdateView):
    """
    Editácia ADP Multi.
    """

    model = ADPMulti
    fields = "__all__"
    template_name = "equipment/adpmulti_form.html"
    success_url = reverse_lazy("adpmulti_list")


class ADPMultiDeleteView(DeleteView):
    """
    Vymazanie ADP Multi.
    """

    model = ADPMulti
    template_name = "equipment/adpmulti_confirm_delete.html"
    reverse_url = reverse_lazy("adpmulti_list")


class ADPSingleListView(ListView):
    """
    Zoznam všetkých ADP Single.
    """

    model = ADPSingle
    template_name = "equipment/adpsingle_list"
    context_object_name = "adp_singles"


class ADPSingleCreateView(CreateView):
    """
    Pridanie ADP Single.
    """

    model = ADPSingle
    fields = "__all__"
    template_name = "equipment/adpsingle_form.html"
    success_url = reverse_lazy("adpsingle_list")


class ADPSingleUpdateView(UpdateView):
    """
    Editácia ADP Single.
    """

    model = ADPSingle
    fields = "__all__"
    template_name = "equipment/adpsingle_form.html"
    success_url = reverse_lazy("adpsingle_list")


class ADPSingleDeleteView(DeleteView):
    """
    Vymazanie ADP Single.
    """

    model = ADPSingle
    template_name = "equipment/adpsingle_confirm_delete.html"
    success_url = reverse_lazy("adpsingle_list")


class AirTankListView(ListView):
    """
    Zoznam všetkých tlakových nádob.
    """

    model = AirTank
    template_name = "equipment/airtank_list"
    context_object_name = "airtanks"


class AirTankCreateView(CreateView):
    """
    Pridanie tlakovej nádoby.
    """

    model = AirTank
    fields = "__all__"
    template_name = "equipment/airtank_form.html"
    success_url = reverse_lazy("airtank_list")


class AirTankUpdateView(UpdateView):
    """
    Editácia tlakovej nádoby.
    """

    model = AirTank
    fields = "__all__"
    template_name = "equipment/airtank_form.html"


class AirTankDeleteView(DeleteView):
    """
    Vymazanie tlakovej nádoby.
    """

    model = AirTank
    template_name = "equipment/airtank_confirm_delete.html"
    success_url = reverse_lazy("airtank_list")


class PCHOListView(ListView):
    """
    Zoznam všetkých PCHO (proti chemických oblekov).
    """

    model = PCHO
    template_name = "equipment/pcho_list.html"
    context_object_name = "pchos"


class PCHOCreateView(CreateView):
    """
    Pridanie PCHO.
    """

    model = PCHO
    fields = "__all__"
    template_name = "equipment/pcho_form.html"
    success_url = reverse_lazy("pcho_list")


class PCHOUpdateView(UpdateView):
    """
    Editácia PCHO.
    """

    model = PCHO
    fields = "__all__"
    template_name = "equipment/pcho_form.html"
    success_url = reverse_lazy("pcho_list")


class PCHODeleteView(DeleteView):
    """
    Vymazanie PCHO.
    """

    model = PCHO
    template_name = "equipment/pcho_confirm_delete.html"
    success_url = reverse_lazy("pcho_list")


class PAListView(ListView):
    """
    Zoznam všetkých PA (pľúcna automatika).
    """

    model = PA
    template_name = "equipment/pa_list.html"
    context_object_name = "pas"


class PACreateView(CreateView):
    """
    Pridanie PA.
    """

    model = PA
    fields = "__all__"
    template_name = "equipment/pa_form.html"
    success_url = reverse_lazy("pa_list")


class PAUpdateView(UpdateView):
    """
    Editácia PA.
    """

    model = PA
    fields = "__all__"
    template_name = "equipment/pa_form.html"
    success_url = reverse_lazy("pa_list")


class PADeleteView(DeleteView):
    """
    Vymazanie PA.
    """

    model = PA
    template_name = "equipment/pa_confirm_delete.html"
    success_url = reverse_lazy("pa_list")


class CompleteListView(ListView):
    """
    Zoznam kompletov vybavenia.
    """

    model = Complete
    template_name = "equipment/complete_list.html"
    context_object_name = "completes"


class CompleteCreateView(CreateView):
    """
    Pridanie nového kompletu.
    """

    model = Complete
    fields = "__all__"
    template_name = "equipment/complete_form.html"
    success_url = reverse_lazy("complete_list")


class CompleteUpdateView(UpdateView):
    """
    Editácia kompletu.
    """

    model = Complete
    fields = "__all__"
    template_name = "equipment/complete_form.html"
    success_url = reverse_lazy("complete_list")


class CompleteDeleteView(DeleteView):
    """
    Vymazanie kompletu.
    """

    model = Complete
    template_name = "equipment/complete_confirm_delete.html"
    success_url = reverse_lazy("complete_list")


MODEL_MAP = {
    "Mask": Mask,
    "ADPMulti": ADPMulti,
    "ADPSingle": ADPSingle,
    "AirTank": AirTank,
    "PCHO": PCHO,
    "PA": PA,
}

REVISION_FIELDS = [
    "rev_half_year",
    "rev_1years",
    "rev_2years",
    "rev_3year",
    "rev_4years",
    "rev_5years",
    "rev_6years",
    "rev_9years",
    "extra_1",
    "extra_2",
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
    "rev_half_year": timedelta(days=182),
    "rev_1years": timedelta(days=365),
    "rev_2years": timedelta(days=730),
    "rev_3year": timedelta(days=1095),
    "rev_4years": timedelta(days=1460),
    "rev_5years": timedelta(days=1825),
    "rev_6years": timedelta(days=2190),
    "rev_9years": timedelta(days=3285),
}


class UpdateStatusView(View):
    def post(self, request, *args, **kwargs):
        model_name = request.POST.get("model")
        obj_id = request.POST.get("id")
        field = request.POST.get("field")  # např. "rev_6years"
        new_status = request.POST.get(
            "status"
        )  # ok | bsr | critical | under_revision | vyradit

        # načteme správný model podle názvu
        from django.apps import apps

        Model = apps.get_model("equipment", model_name)
        eq = get_object_or_404(Model, pk=obj_id)

        # 1) ARCHIVACE (Vyradit)
        if new_status == "vyradit":
            eq.is_archived = True
            eq.archived_at = timezone.now()
            eq.archived_by = request.user
            eq.status = "vyradit"
            eq.status_field = None
            eq.save(
                update_fields=[
                    "is_archived",
                    "archived_at",
                    "archived_by",
                    "status",
                    "status_field",
                ]
            )
            return JsonResponse({"result": "archived"})

        # 2) V řešení (under_revision)
        if new_status == "under_revision":
            eq.status = "under_revision"
            eq.status_field = field
            eq.save(update_fields=["status", "status_field"])
            return JsonResponse({"result": "ok"})

        # 3) Návrat z řešení / OK / BSR / Critical
        # Pokud už jsme byli v řešení, smažeme status_field
        if eq.status == "under_revision":
            eq.status_field = None

        # Nastavíme nový globální status i v poli status_field (vyčistíme ho)
        eq.status = new_status

        # Pokud potřebujeme posunout datum (OK/BSR) podle revise_from_date:
        if new_status in ("ok", "bsr"):
            base_date_str = request.POST.get("revise_from_date")
            if base_date_str:
                base = datetime.strptime(base_date_str, "%Y-%m-%d").date()
                # >>> KONTROLA ZDE <<<
                if base < date.today():
                    return JsonResponse({"error": "Past date not allowed"}, status=400)
            else:
                base = date.today()
            interval = REVISION_INTERVALS.get(field)
            if interval:
                setattr(eq, field, base + interval)
                eq.save(update_fields=[field, "status", "status_field"])
                return JsonResponse({"result": "ok"})

        # Pro všechny ostatní stavy (critical apod.) jen uložíme status
        eq.save(update_fields=["status", "status_field"])
        return JsonResponse({"result": "ok"})


class StationEquipmentListView(TemplateView):
    template_name = "equipment/station_equipment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station = get_object_or_404(Station, pk=self.kwargs["pk"])
        context["station"] = station
        context["STATUS_CHOICES"] = STATUS_CHOICES

        today = date.today()
        one_month = today + timedelta(days=30)
        three_months = today + timedelta(days=90)

        sections = []
        for label, model, _, _, fields, model_name in [
            (
                "Masky",
                Mask,
                None,
                None,
                [
                    "type",
                    "e_number",
                    "serial_number",
                    "rev_2years",
                    "rev_4years",
                    "rev_6years",
                    "extra_1",
                    "extra_2",
                ],
                "Mask",
            ),
            (
                "ADP Multi",
                ADPMulti,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_1years", "rev_6years"],
                "ADPMulti",
            ),
            (
                "ADP Single",
                ADPSingle,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_1years", "rev_9years"],
                "ADPSingle",
            ),
            (
                "Tlakové nádoby",
                AirTank,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_5years"],
                "AirTank",
            ),
            (
                "PCHO",
                PCHO,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_half_year", "rev_2years"],
                "PCHO",
            ),
            (
                "PA",
                PA,
                None,
                None,
                [
                    "type",
                    "e_number",
                    "serial_number",
                    "rev_3year",
                    "rev_6years",
                    "rev_9years",
                ],
                "PA",
            ),
        ]:
            queryset = model.objects.filter(
                located=station, is_archived=False
            )  # taháme pouze aktivní vybavení (is_archived=False)
            # Příklad uvnitř get_context_data ve vašem view
            for eq in queryset:
                eq.status_map = {}
                for f in fields:
                    # 1) Override: pokud je právě toto pole v řešení, vykreslíme under_revision
                    if eq.status == "under_revision" and eq.status_field == f:
                        eq.status_map[f] = "under_revision"
                        continue

                    # 2) Jinak fallback na datovou logiku
                    rev_date = getattr(eq, f, None)
                    if not isinstance(rev_date, date):
                        continue
                    if rev_date <= one_month:
                        eq.status_map[f] = "critical"
                    elif rev_date <= three_months:
                        eq.status_map[f] = "bsr"
                    else:
                        eq.status_map[f] = "ok"

            pretty_fields = [
                (f, REVISION_LABELS.get(f, f.capitalize())) for f in fields
            ]
            sections.append((label, queryset, pretty_fields, model_name))
        context["equipment_sections"] = sections
        context["allowed_transitions"] = ALLOWED
        context["REVISION_INTERVALS"] = REVISION_INTERVALS
        return context


class UpcomingRevisionListView(TemplateView):
    template_name = "equipment/upcoming_revisions.html"

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

        context["groups"] = [
            (
                "Masky",
                filter_items(
                    Mask,
                    ["rev_2years", "rev_4years", "rev_6years", "extra_1", "extra_2"],
                ),
            ),
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
        model = MODEL_MAP.get(self.kwargs["model"])
        if not model:
            raise Http404("Unknown model")
        return model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["REVISION_LABELS"] = REVISION_LABELS  # so template has labels
        # pass only the revision fields
        context["revision_fields"] = [
            f
            for f in self.object.__dict__.keys()
            if f.startswith("rev") or f.startswith("extra")
        ]
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

        new_options = get_allowed_trransitions(new_status)

        return JsonResponse({"success": True, "new_options": new_options})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


class ArchiveEquipmentListView(TemplateView):
    template_name = "equipment/archive_equipment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        station = get_object_or_404(Station, pk=self.kwargs["pk"])

        today = date.today()
        one_month = today + timedelta(days=30)
        three_months = today + timedelta(days=90)

        sections = []
        for label, model, _, _, fields, model_name in [
            # **TADY JE TEN KLÍČOVÝ SEZNAM** – MUSÍ BÝT PLNÝ ŘÁDKŮ
            (
                "Masky",
                Mask,
                None,
                None,
                [
                    "type",
                    "e_number",
                    "serial_number",
                    "rev_2years",
                    "rev_4years",
                    "rev_6years",
                    "extra_1",
                    "extra_2",
                ],
                "Mask",
            ),
            (
                "ADP Multi",
                ADPMulti,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_1years", "rev_6years"],
                "ADPMulti",
            ),
            (
                "ADP Single",
                ADPSingle,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_1years", "rev_9years"],
                "ADPSingle",
            ),
            (
                "Tlakové nádoby",
                AirTank,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_5years"],
                "AirTank",
            ),
            (
                "PCHO",
                PCHO,
                None,
                None,
                ["type", "e_number", "serial_number", "rev_half_year", "rev_2years"],
                "PCHO",
            ),
            (
                "PA",
                PA,
                None,
                None,
                [
                    "type",
                    "e_number",
                    "serial_number",
                    "rev_3year",
                    "rev_6years",
                    "rev_9years",
                ],
                "PA",
            ),
        ]:
            # tahám jen ty, které jsou archivované
            qs = model.objects.filter(located=station, is_archived=True)

            # připravím status_map jen pro skutečná data
            for eq in qs:
                eq.status_map = {}
                for f in fields:
                    rev_date = getattr(eq, f, None)
                    if not isinstance(rev_date, date):
                        continue
                    if rev_date <= one_month:
                        eq.status_map[f] = "critical"
                    elif rev_date <= three_months:
                        eq.status_map[f] = "bsr"
                    else:
                        eq.status_map[f] = "ok"

            # hezké popisky
            pretty_fields = []
            for f in fields:
                if f in REVISION_LABELS:
                    pretty_fields.append((f, REVISION_LABELS[f]))
                else:
                    pretty_fields.append((f, f.replace("_", " ").capitalize()))

            sections.append((label, qs, pretty_fields, model_name))

        context["equipment_sections"] = sections
        context["station"] = station
        context["allowed_transitions"] = ALLOWED
        return context


class RetireEquipment(View):
    def post(self, request, pk):
        # pro každý model zkusíme najít objekt s tímto pk
        for model in MODEL_MAP.values():
            try:
                eq = model.objects.get(pk=pk)
            except model.DoesNotExist:
                continue
            # našli jsme ten správný model
            eq.is_archived = True
            eq.archived_at = timezone.now()
            eq.archived_by = request.user
            eq.save(update_fields=["is_archived", "archived_at", "archived_by"])
            return redirect("station_equipment", pk=eq.located.pk)
        # nic jsme nenašli
        raise Http404("Equipment not found")


class RestoreEquipment(View):
    def post(self, request, pk):
        for model in MODEL_MAP.values():
            try:
                eq = model.objects.get(pk=pk)
            except model.DoesNotExist:
                continue
            eq.is_archived = False
            eq.save(update_fields=["is_archived"])
            return redirect("station_equipment_archive", pk=eq.located.pk)
        raise Http404("Equipment not found")
