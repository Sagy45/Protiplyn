"""
email_upcoming_revisions.py –Skript na odosielanie emailov s blížiacimi sa revíziami vybavenia

Tento management command vyhľadá,
pre každého používateľa relevantné vybavenie s blížiacou sa revíziou


a odošle mu zoznam položiek emailom.
"""

from datetime import timedelta
from django.db.models import Q
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model  # OPRAVA: použij get_user_model

from equipment.models import (
    Mask,
    ADPMulti,
    ADPSingle,
    AirTank,
    PCHO,
    PA,
    REVISION_LABELS,
)

from accounts.models import Profile

User = get_user_model()  # OPRAVA: použij místo importu User


class Command(BaseCommand):
    """
    Management command pre odosielanie emailov používateľom o blížiacich sa revíziách vybavenia.

    Pre každého používateľa so zadanou stanicou (okrem admina)
    zostaví zoznam položiek s blížiacou sa revíziou
    a pošle ich emailom na jeho adresu.
    """

    help = "Email users a list of upcoming equipment revisions"

    def handle(self, *args, **options):
        """
        Hlavná metóda príkazu.

        Prejde všetkých aktívnych používateľov s emailom, zistí ich stanicu a role,
        pre každú skupinu vybavenia nájde blížiace sa revízie a pošle email s prehľadom.

        Args:
            *args: Nevyužívané pozičné argumenty.
            **options: Nevyužívané kľúčové argumenty.
        """
        today = timezone.now().date()
        three_months = today + timedelta(days=90)
        one_month = today + timedelta(days=30)

        users = User.objects.filter(is_active=True, email__isnull=False).select_related(
            "profile"
        )
        for user in users:
            profile = getattr(user, "profile", None)
            if not profile:
                continue

            # Admin vsetko; tech len ich stanicu
            if profile.role == Profile.ROLE_ADMIN:
                # station_filter = Q() / ak chceme aby admin dostal vsetko uncomment
                continue

            if not profile.station:
                continue
            station_filter = Q(located__prefix=profile.station.prefix)

            def filter_and_flag(qs, fields):
                """
                Pomocná funkcia: filtruje queryset podľa stanice a blížiacich sa revízií,
                a ku každému zariadeniu pridá relevantné dátumy revízií.

                Args:
                    qs (QuerySet): Queryset vybavenia.
                    fields (list): Zoznam názvov polí revízií.

                Returns:
                    list: Zoznam zariadení s pridanými atribútmi relevant_dates a is_red.
                """
                combined = qs.filter(station_filter)
                for f in fields:
                    combined = combined | qs.filter(
                        station_filter, **{f"{f}__lte": three_months}
                    )
                combined = combined.distinct()

                results = []
                for item in combined:
                    relevant_dates = []
                    for f in fields:
                        date = getattr(item, f)
                        if date and today <= date <= three_months:
                            relevant_dates.append((REVISION_LABELS.get(f, f), date))
                    if relevant_dates:
                        item.relevant_dates = relevant_dates
                        item.is_red = any(d <= one_month for _, d in relevant_dates)
                        results.append(item)
                return results

            mask = filter_and_flag(
                Mask.objects.all(),
                ["rev_2years", "rev_4years", "rev_6years", "extra_1", "extra_2"],
            )
            adpmulti = filter_and_flag(
                ADPMulti.objects.all(), ["rev_1years", "rev_6years"]
            )
            adpsingle = filter_and_flag(
                ADPSingle.objects.all(), ["rev_1years", "rev_9years"]
            )
            airtank = filter_and_flag(AirTank.objects.all(), ["rev_5years"])
            pcho = filter_and_flag(PCHO.objects.all(), ["rev_half_year", "rev_2years"])
            pa = filter_and_flag(
                PA.objects.all(), ["rev_3year", "rev_6years", "rev_9years"]
            )

            all_groups = [
                ("Masky", mask),
                ("ADP Multi", adpmulti),
                ("ADP Single", adpsingle),
                ("Vzduchové bomby", airtank),
                ("PCHO", pcho),
                ("PA", pa),
            ]

            # Build email body
            lines = []
            for group_name, items in all_groups:
                if items:
                    lines.append(f"\n{group_name}:")
                    for eq in items:
                        for label, date in eq.relevant_dates:
                            lines.append(
                                f"- {eq.equipment_type} {eq.e_number} ({label}: {date:%d.%m.%Y})"
                            )

            if not lines:
                continue

            subject = "Blížiace sa revízie zariadení"
            body = (
                f"Ahoj {user.first_name},\n\nNasledujúce zariadenia majú blížiacu sa revíziu:\n"
                + "\n".join(lines)
            )
            send_mail(
                subject,
                body,
                "noreply@protiplyn.sk",
                [user.email],
            )
            self.stdout.write(
                self.style.SUCCESS(f"E-mail sent to {user.email} ({profile.role})")
            )
