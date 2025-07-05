"""
custom_tags.py – Vlastné šablónové filtre a tagy pre aplikáciu equipment.

Obsahuje pomocné funkcie pre šablóny na jednoduché získavanie hodnot atribútov,
formátovanie dátumov, čítanie zo slovníkov a určovanie stavov vybavenia.
"""

from django import template
from equipment.models import STATUS_CHOICES

register = template.Library()


@register.filter
def attr(obj, attr_name):
    """
    Vráti hodnotu atribútu podľa mena.

    Args:
        obj (object): Ľubovoľný objekt.
        attr_name (str): Názov atribútu.

    Returns:
        Hodnota daného atribútu alebo None, ak neexistuje.
    """
    return getattr(obj, attr_name)


@register.filter
def prettydate(value):
    """
    Formátuje dátum do tvaru DD.MM.RRRR.

    Args:
        value (date/datetime/None): Hodnota dátumu.

    Returns:
        str: Naformátovaný dátum alebo "-" ak nie je hodnota.
    """
    if hasattr(value, "strftime"):
        return value.strftime("%d.%m.%Y")
    return value or "-"


@register.filter
def get_item(dictionary, key):
    """
    Vráti hodnotu zo slovníka podľa kľúča.

    Args:
        dictionary (dict): Slovník.
        key: Kľúč.

    Returns:
        Hodnota zo slovníka alebo None, ak neexistuje.
    """
    return dictionary.get(key)


@register.filter
def get_status(item, field):
    """
    Získa stav revízie daného poľa pre položku (napr. kritický, OK, v riešení).

    Args:
        item: Objekt vybavenia (môže mať status_map).
        field (str): Názov poľa revízie.

    Returns:
        str: Hodnota stavu ("ok", "bsr", "critical", "under_revision" ...).
    """
    if hasattr(item, "status_map"):
        return item.status_map.get(field, "ok")
    return "ok"


@register.filter
def get_status_class(item, field):
    """
    Získa CSS triedu podľa stavu (zvyčajne rovnaké ako samotný stav).

    Args:
        item: Objekt vybavenia.
        field (str): Názov poľa revízie.

    Returns:
        str: CSS trieda pre daný stav.
    """
    status = get_status(item, field)
    return status


@register.simple_tag
def allowed_statuses(current_status, allowed_dict):
    """
    Vráti zoznam povolených stavov pre výber v dropdown menu (aktuálny + povolené prechody).

    Args:
        current_status (str): Aktuálny stav.
        allowed_dict (dict): Slovník povolených prechodov.

    Returns:
        list: Zoznam dvojíc (hodnota, popis) pre povolené stavy.
    """
    pool = [current_status]
    for ns in allowed_dict.get(current_status, []):
        if ns not in pool:
            pool.append(ns)
    return [(choice, label) for choice, label in STATUS_CHOICES if choice in pool]
