from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q


from .models import Domain, Flag

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
        latest_domains = Domain.objects.all()[:5]
        context = {
            "latest_domains": latest_domains,
            "summary": summary,
            "pie_chart_data": pie_chart_data,
        }
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
        domains = Domain.objects.all().order_by("-created_at")[:50]

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
            return Domain.objects.get(id=id)
        except Domain.DoesNotExist:
            raise Http404

    def get(self, request: HttpRequest, id: int, *args, **kwargs):
        domain = self.get_domain_object(id)
        flags = domain.flag_set.all()
        context = {"domain": domain, "flags": flags}
        return render(request, self.template_name, context)


class AddDomainsView(LoginRequiredMixin, View):
    template_name = "flags/add-domains.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            uploaded_json_file = json.loads(request.FILES.get("file").read())
            process_and_save_domains.delay(
                uploaded_json_file
            )  # Run the task out of HTTP Request&Responce cycle
        except ValueError:
            raise SuspiciousOperation("Invalid file. Expect to receive JSON file")
        return redirect(reverse("domains-add-success"))


class DomainsAddSuccessView(LoginRequiredMixin, View):
    template_name = "flags/domains-add-success.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
