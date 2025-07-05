"""Modely pre aplikáciu documents."""

from django.db import models
from django.contrib.auth.models import User
from django.db.models import (
    Model,
    CharField,
    TextField,
    FileField,
    ForeignKey,
    DateTimeField,
)


class DocumentTemplate(Model):
    """
    Model predstavujúci šablónu dokumentu.

    Atribúty:
        name (str): Názov šablóny.
        description (str): Voliteľný popis šablóny.
        pdf_file (File): Nahraný PDF súbor so šablónou.
        created_by (User): Používateľ, ktorý šablónu vytvoril.
        created_at (datetime): Dátum a čas vytvorenia záznamu.
    """

    name = CharField(max_length=100)
    description = TextField(blank=True)
    pdf_file = FileField(upload_to="document_templates/")
    created_by = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        """Reprezentácia šablóny ako jej názov (string)."""
        return str(self.name or "")
