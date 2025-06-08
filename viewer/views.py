from django.shortcuts import render
from .models import Country
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
