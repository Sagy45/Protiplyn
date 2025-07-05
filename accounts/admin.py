"""Konfigurácia Django admin rozhrania pre používateľské profily."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    """Zobrazuje profil používateľa ako inline formulár v administrácii."""

    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    """Rozširuje štandardnú User admin triedu o zobrazenie profilu."""

    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        """Vracia zoznam inline inštancií pre daného používateľa.

        Args:
            request (HttpRequest): Objekt HTTP požiadavky.
            obj (User, optional): Používateľ, pre ktorého sa admin vykresľuje.

        Returns:
            list: Zoznam inline inštancií alebo prázdny zoznam, ak nie je `obj`.
        """
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Odregistrovanie preddefinovanej User admin triedy
admin.site.unregister(User)

# Registrácia vlastnej User admin triedy s pripojeným inline profilom
admin.site.register(User, UserAdmin)
