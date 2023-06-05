from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q

from .models import Domain, Flag


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
        summary = {
            "domains": {"all": all_domains, "expired": expired_domains},
            "flags": Flag.objects.all().count(),
        }
        chart = {"pie_data": [active_domains, expired_domains]}
        latest_domains = Domain.objects.all()[:5]
        context = {"latest_domains": latest_domains, "summary": summary, "chart": chart}
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
        domain = request.GET.get("domain", "")

        if status != "" or domain != "":
            ACTIVE_STATUS = "ACTIVE"
            q = Q()
            if status != "":
                query = (
                    Q(expire_at__lt=timezone.now())
                    if status == ACTIVE_STATUS
                    else Q(expire_at__gt=timezone.now())
                )
                q &= query
            if domain != "":
                q &= Q(fqdn__icontains=domain)

            domains = Domain.objects.filter(q).order_by("-created_at")[:50]
        context = {"domains": domains}
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
