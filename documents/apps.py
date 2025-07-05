"""Konfigurácia aplikácie documents."""

from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    """Nastavenie základnej konfigurácie pre aplikáciu documents."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "documents"
