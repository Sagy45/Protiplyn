"""
View funkce a triedy pre správu geografických dát (štát, kraj, okres, mesto, stanica)
a typov vybavenia v aplikácii Protiplyn.
"""

from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from accounts.models import Profile
from equipment.models import EquipmentType
from .models import Country, Station, City

def country_detail_full(request):
    """
    Zobrazí kompletný prehľad krajiny s regionálnou štruktúrou.

    Args:
        request (HttpRequest): Požiadavka na stránku.

    Returns:
        HttpResponse: HTML stránka s detailom krajiny, regiónov, okresov, miest a staníc.
    """
    country = Country.objects.first()  # vezme jedinú krajinu (iba jedna v DB)
    if not country:
        return render(
            request, "viewer/no_country.html"
        )
    regions = country.regions.prefetch_related(
        "districts__cities__stations"
    )
    return render(
        request,
        "viewer/country_detail_full.html",
        {
            "country": country,
            "regions": regions,
        },
    )


class EquipmentTypeListView(ListView):
    """
    View pre zoznam všetkých typov vybavenia.
    """
    model = EquipmentType
    template_name = "equipment/equipmenttype_list.html"
    context_object_name = "equipment_types"


class EquipmentTypeCreateView(CreateView):
    """
    View pre vytvorenie nového typu vybavenia.
    """
    model = EquipmentType
    fields = ["name"]
    template_name = "equipment/equipmenttype_form.html"
    success_url = reverse_lazy("equipmenttype_list")


class EquipmentTypeUpdateView(UpdateView):
    """
    View pre editáciu typu vybavenia.
    """
    model = EquipmentType
    fields = ["name"]
    template_name = "equipment/equipmenttype_form.html"
    success_url = reverse_lazy("equipmenttype_list")


class EquipmentTypeDeleteView(DeleteView):
    """
    View pre odstránenie typu vybavenia.
    """
    model = EquipmentType
    template_name = "equipment/equipmenttype_confirm_delete.html"
    success_url = reverse_lazy("equipmenttype_list")


class StationListView(ListView):
    """
    View pre zoznam staníc s možnosťou filtrovania podľa rolí a polohy.

    Zobrazuje stanice podľa oprávnení používateľa (technik vidí len svoju stanicu,
    admin všetky). Umožňuje filtrovať podľa štátu, kraja, okresu a mesta.
    """
    model = Station
    template_name = "station/station_list.html"
    context_object_name = "stations"

    def get_queryset(self):
        """
        Načíta queryset staníc podľa roly používateľa a voliteľných GET filtrov.

        Returns:
            QuerySet: Zoznam staníc podľa filtrov a práv.
        """
        user = self.request.user
        profile = getattr(user, "profile", None)
        qs = Station.objects.select_related("city__district__region__country")
        if profile and profile.role == Profile.ROLE_TECHNICIAN:
            if profile.station:
                qs = qs.filter(pk=profile.station.pk)
            else:
                qs = qs.none()

        # Filtrovanie podľa GET parametrov
        stat = self.request.GET.get("stat")
        kraj = self.request.GET.get("kraj")
        okres = self.request.GET.get("okres")
        mesto = self.request.GET.get("mesto")

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
        """
        Doplní kontext o možnosti filtrovania pre jednotlivé úrovne (štát, kraj, okres, mesto).

        Returns:
            dict: Kontext s možnosťami filtrov pre šablónu.
        """
        context = super().get_context_data(**kwargs)
        all_stations = Station.objects.select_related("city__district__region__country")

        stat = self.request.GET.get("stat")
        kraj = self.request.GET.get("kraj")
        okres = self.request.GET.get("okres")
        mesto = self.request.GET.get("mesto")

        context["stat_options"] = (
            all_stations.values_list("city__district__region__country__name", flat=True)
            .distinct()
            .order_by("city__district__region__country__name")
        )

        regions_qs = all_stations
        if stat:
            regions_qs = regions_qs.filter(
                city__district__region__country__name__icontains=stat
            )
        if okres:
            regions_qs = regions_qs.filter(city__district__name__icontains=okres)
        if mesto:
            regions_qs = regions_qs.filter(city__name__icontains=mesto)
        context["kraj_options"] = (
            regions_qs.values_list("city__district__region__name", flat=True)
            .distinct()
            .order_by("city__district__region__name")
        )

        districts_qs = all_stations
        if kraj:
            districts_qs = districts_qs.filter(
                city__district__region__name__icontains=kraj
            )
        if mesto:
            districts_qs = districts_qs.filter(city__name__icontains=mesto)
        context["okres_options"] = (
            districts_qs.values_list("city__district__name", flat=True)
            .distinct()
            .order_by("city__district__name")
        )

        cities_qs = all_stations
        if okres:
            cities_qs = cities_qs.filter(city__district__name__icontains=okres)
        if kraj:
            cities_qs = cities_qs.filter(city__district__region__name__icontains=kraj)
        context["mesto_options"] = (
            cities_qs.values_list("city__name", flat=True)
            .distinct()
            .order_by("city__name")
        )

        return context


class StationCreateView(CreateView):
    """
    View pre vytvorenie novej stanice.
    """
    model = Station
    fields = ["name", "city"]
    template_name = "station/station_form.html"
    success_url = reverse_lazy("station_list")


class StationUpdateView(UpdateView):
    """
    View pre editáciu existujúcej stanice.
    """
    model = Station
    fields = ["name", "city"]
    template_name = "station/station_form.html"
    success_url = reverse_lazy("station_list")


class StationDeleteView(DeleteView):
    """
    View pre zmazanie stanice.
    """
    model = Station
    template_name = "station/station_confirm_delete.html"
    success_url = reverse_lazy("station_list")


class CityCreateView(CreateView):
    """
    View pre vytvorenie nového mesta.
    """
    model = City
    fields = ["name", "district"]
    template_name = "city/city_form.html"
    success_url = reverse_lazy("station_add")
