from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from equipment.models import Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, Complete

REVISION_FIELDS = [
    "rev_half_year",  # půlroční
    "rev_1years",
    "rev_2years",
    "rev_3year",
    "rev_4years",
    "rev_5years",
    "rev_6years",
    "rev_9years"
]

ALL_MODELS = [Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, Complete]

class Command(BaseCommand):
    help = "Aktualizuje statusy vybavení podle blížících se nebo prošlých revizí"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        critical_threshold = timedelta(days=30)
        bsr_threshold = timedelta(days=90)

        for model in ALL_MODELS:
            updated = 0
            items = model.objects.all()
            for item in items:
                worst_status = "ok"
                for field in REVISION_FIELDS:
                    revise_date = getattr(item, field, None)
                    if revise_date is None:
                        continue

                    days_to_revision = (revise_date - today).days

                    if days_to_revision < critical_threshold.days:
                        worst_status = "critical"
                        break
                    elif days_to_revision < bsr_threshold.days:
                        worst_status = "bsr"

                if item.status != worst_status:
                    item.status = worst_status
                    item.save()
                    updated += 1

            self.stdout.write(f"{model.__name__}: aktualizováno {updated} položek.")

        self.stdout.write(self.style.SUCCESS("Statusy byly úspěšně aktualizovány."))
