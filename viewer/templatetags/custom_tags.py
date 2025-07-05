"""
Jednoduché šablónové filtre na čítanie atribútov objektov.

Obsahuje filtre na získanie hodnoty atribútu podľa mena – použiteľné v Django šablónach.
"""

from django import template

register = template.Library()


@register.filter
def attr(obj, attr_name):
    """
    Vráti hodnotu atribútu podľa názvu.

    Args:
        obj (object): Objekt, z ktorého čítame atribút.
        attr_name (str): Názov atribútu.

    Returns:
        Hodnota atribútu alebo prázdny reťazec, ak atribút neexistuje.
    """
    return getattr(obj, attr_name, "")


@register.filter
def get_attr(obj, attr_name):
    """
    Alternatívny filter: vráti hodnotu atribútu podľa názvu (rovnaké ako attr).

    Args:
        obj (object): Objekt, z ktorého čítame atribút.
        attr_name (str): Názov atribútu.

    Returns:
        Hodnota atribútu alebo prázdny reťazec, ak atribút neexistuje.
    """
    return getattr(obj, attr_name, "")
