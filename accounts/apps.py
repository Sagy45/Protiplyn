"""Konfigurácia aplikácie 'accounts'.

Tento modul definuje základnú konfiguráciu pre Django aplikáciu 'accounts',
ktorá rozširuje používateľský model pomocou profilu.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Konfiguračná trieda pre aplikáciu 'accounts'.

    Atribúty:
        default_auto_field (str): Implicitné primárne kľúče budú typu BigAutoField.
        name (str): Názov aplikácie (odkazovaný v nastaveniach projektu).
    """

    default_auto_field = (
        "django.db.models.BigAutoField"  # Používame väčší typ ID ako predvolený
    )
    name = "accounts"  # Interný názov aplikácie
