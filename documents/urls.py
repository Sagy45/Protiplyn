"""URL konfigurácia pre aplikáciu documents."""

from django.urls import path
from . import views

urlpatterns = [
    # Zoznam dostupných dokumentových šablón
    path("", views.templates_list, name="templates_list"),
    # Výber zariadení pre konkrétnu šablónu podľa ID
    path(
        "vyber-zariadeni/<int:template_id>/",
        views.equipment_select,
        name="equipment_select",
    ),
]
