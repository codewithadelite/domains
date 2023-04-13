from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    template = "flags/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, self.template, context)


class SettingsView(LoginRequiredMixin, View):
    template_name = "flags/settings.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class DomainListView(LoginRequiredMixin, View):
    template_name = "flags/domains.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class DomainDetailView(LoginRequiredMixin, View):
    template_name = "flags/domain-details.html"

    def get(self, request, id, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class AddDomainsView(LoginRequiredMixin, View):
    template_name = "flags/add-domains.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
