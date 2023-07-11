from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q, Count
from django.db.models.functions import Extract


from .models import Domain, Flag

from .constants import MONTHS

import json

# celery tasks

from .tasks import process_and_save_domains


class DashboardView(LoginRequiredMixin, View):
    template = "flags/dashboard.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Get dashboard informations:
            - Summary informations
            - Charts data
            - latest domains
        """
        all_domains = Domain.objects.all().count()
        expired_domains = Domain.objects.filter(expire_at__lt=timezone.now()).count()
        active_domains = Domain.objects.filter(expire_at__gt=timezone.now()).count()

        chart_year = request.GET.get("chart_year", None)

        YEAR = 2022

        if chart_year is not None:
            YEAR = int(chart_year)

        domains_creations_chart = Domain.objects.filter(
            created_at__year=YEAR
        ).aggregate(
            **{
                item: Count("pk", filter=Q(created_at__month=value))
                for (item, value) in MONTHS.items()
            }
        )

        domains_line_chart_data = {
            "labels": [label for label in domains_creations_chart.keys()],
            "data": [data for data in domains_creations_chart.values()],
        }

        # Summary data to display in dashbord
        summary = {
            "domains": {"all": all_domains, "expired": expired_domains},
            "flags": Flag.objects.all().count(),
        }
        # Pie chart data tha displayed in pie chart
        pie_chart_data = {
            "labels": ["ACTIVE", "EXPIRED"],
            "data": [active_domains, expired_domains],
        }
        latest_domains = Domain.objects.all().order_by("-id")[:5]

        context = dict()
        context["latest_domains"] = latest_domains
        context["summary"] = summary
        context["domains_line_chart_data"] = domains_line_chart_data
        context["pie_chart_data"] = pie_chart_data
        context["chart_year"] = YEAR
        return render(request, self.template, context)


class SettingsView(LoginRequiredMixin, View):
    template_name = "flags/settings.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class DomainListView(LoginRequiredMixin, View):
    template_name = "flags/domains.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        """
        Returns registered domains.
            - It applies filter if status  or domain variable is found in the HTTP request
        """
        domains = Domain.objects.all().order_by("-id")[:50]

        status = request.GET.get("status", "")
        tldr = request.GET.get("tldr", "")
        domain = request.GET.get("domain", "")

        params = {"status": status, "tldr": tldr, "domain": domain}

        if status != "" or tldr != "" or domain != "":
            q = Q()
            if status != "":
                ACTIVE_STATUS = "ACTIVE"
                query = (
                    Q(expire_at__gt=timezone.now())
                    if status == ACTIVE_STATUS
                    else Q(expire_at__lt=timezone.now())  # Then it is DEACTIVE
                )
                q &= query

            if tldr != "":
                q &= Q(fqdn__endswith=tldr)

            if domain != "":
                q &= Q(fqdn__icontains=domain)

            domains = Domain.objects.filter(q).order_by("-created_at")[:50]
        context = {"domains": domains, "params": params}
        return render(request, self.template_name, context)


class DomainDetailView(LoginRequiredMixin, View):
    template_name = "flags/domain-details.html"

    def get_domain_object(self, id: int) -> Domain:
        try:
            return Domain.objects.get(pk=id)
        except Domain.DoesNotExist:
            raise Http404

    def get(self, request: HttpRequest, id: int, *args, **kwargs):
        domain = self.get_domain_object(id)
        flags = domain.flag_set.all()
        context = {"domain": domain, "flags": flags}
        return render(request, self.template_name, context)


class DomainDeleteView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, id: int):
        """
        Delete domain.
        """
        try:
            domain = Domain.objects.get(pk=id)
            deleted, _ = domain.delete()
            if deleted:
                messages.success(request, f"Domain {domain.fqdn} deleted successfully")
                return redirect(reverse("domains"))
        except Domain.DoesNotExist:
            raise Http404
        except Exception as e:
            messages.error(request, f"There was error, Try again later.")
            return redirect(reverse("domains"))


class AddDomainsView(LoginRequiredMixin, View):
    template_name = "flags/add-domains.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            process_and_save_domains.delay(
                domains=json.loads(request.FILES.get("file").read())
            )  # Run the task out of HTTP Request&Responce cycle
        except ValueError:
            raise SuspiciousOperation("Invalid file. Expect to receive JSON file")
        return redirect(reverse("domains-add-success"))


class DomainsAddSuccessView(LoginRequiredMixin, View):
    template_name = "flags/domains-add-success.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
