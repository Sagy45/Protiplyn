"""Konfigurácia aplikácie equipment pre Django projekt.

Tento modul obsahuje triedu EquipmentConfig, ktorá definuje základné nastavenia
pre aplikáciu equipment v rámci projektu.
"""

from django.apps import AppConfig


class EquipmentConfig(AppConfig):
    """
    Konfiguračná trieda pre aplikáciu 'equipment'.

    Atribúty:
        default_auto_field (str): Predvolený typ automatického primárneho kľúča pre modely.
        name (str): Názov aplikácie (dôležité pre Django).
        verbose_name (str): Zobrazený názov aplikácie v admin rozhraní.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "equipment"
    verbose_name = "Zoznam skladu"
