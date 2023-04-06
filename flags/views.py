from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DomainListView(LoginRequiredMixin, View):
    template = "flags/dashboard.html"

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, self.template, context)
