from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from equipment.models import Mask, ADPMulti, ADPSingle, AirTank, PCHO, PA, REVISION_LABELS
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_station = self.request.user.profile.station

        today = timezone.now().date()
        three_months = today + timedelta(days=90)
        one_month = today + timedelta(days=30)

        filters = Q(located=user_station)

        def filter_and_flag(qs, fields):
            filtered_qs = qs.filter(
                Q(**{f"{fields[0]}__lte": three_months}) |
                Q(**{f"{fields[1]}__lte": three_months}) if len(fields) > 1 else Q()
            )
            for field in fields:
                filtered_qs = filtered_qs | qs.filter(**{f"{field}__lte": three_months})
            filtered_qs = filtered_qs.distinct()

            results = []
            for item in filtered_qs:
                relevant_dates = []
                for f in fields:
                    date = getattr(item, f)
                    if date and today <= date <= three_months:
                        relevant_dates.append((REVISION_LABELS.get(f, f), date))
                if relevant_dates:
                    item.relevant_dates = relevant_dates
                    item.is_red = any(date <= one_month for _, date in relevant_dates)
                    results.append(item)

            return results

        mask = filter_and_flag(Mask.objects.filter(filters),
                               ["rev_2years", "rev_4years", "rev_6years", "extra_1", "extra_2"])
        adpmulti = filter_and_flag(ADPMulti.objects.filter(filters), ["rev_1years", "rev_6years"])
        adpsingle = filter_and_flag(ADPSingle.objects.filter(filters), ["rev_1years", "rev_9years"])
        airtank = filter_and_flag(AirTank.objects.filter(filters), ["rev_5years"])
        pcho = filter_and_flag(PCHO.objects.filter(filters), ["rev_half_year", "rev_2years"])
        pa = filter_and_flag(PA.objects.filter(filters), ["rev_3year", "rev_6years", "rev_9years"])

        context["groups"] = [
            ("Masky", mask),
            ("ADP Multi", adpmulti),
            ("ADP Single", adpsingle),
            ("Vzduchové bomby", airtank),
            ("PCHO", pcho),
            ("PA", pa),
        ]

        return context
