"""
Konfigurácia aplikácie notifier

Obsahuje nastavenie pre Django aplikáciu 'notifier', ktorá zabezpečuje upozorňovanie
a odosielanie emailov o blížiacich sa revíziách zariadení.
"""

from django.apps import AppConfig


class NotifierConfig(AppConfig):
    """
    Konfigurácia pre aplikáciu notifier.

    Nastavuje základné parametre aplikácie, vrátane predvoleného typu primárneho kľúča.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "notifier"
