from viewer.models import Station

STATION_PREFIX_MAP = {
    1:"BB",
    19: "ZM",
    20: "BA",
    21: "NR",
    # add more if needed
}

def station_prefix(request):
    """
    Přidá `station_prefix` podle station přiřazené uživateli.
    Pokud není uživatel přihlášen nebo nemá station, vrátí prázdný string.
    """
    prefix = ""
    user = request.user
    if user.is_authenticated:
        station = getattr(request.user.profile, "station", None)
        if station and station.pk in STATION_PREFIX_MAP:
            prefix = STATION_PREFIX_MAP[station.pk]
    return {"station_prefix": prefix}