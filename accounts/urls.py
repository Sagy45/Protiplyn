"""URL konfigurácia pre aplikáciu accounts."""

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import DashboardView

# Definícia URL ciest pre prihlasovanie, odhlasovanie a dashboard
urlpatterns = [
    # Prihlasovanie používateľa pomocou zabudovaného LoginView
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    # Odhlasovanie používateľa s presmerovaním na prihlasovaciu stránku
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
    ),
    # Dashboard po prihlásení
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
