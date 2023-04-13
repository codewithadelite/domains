from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ChangePasswordForm


class Login(View):
    template_name = "authentication/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("dashboard"))
        context = {
            "error": {"message": "Username or password incorrect"}
        }
        return render(request, self.template_name, context)


class Logout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse("login"))


class ChangePasswordView(LoginRequiredMixin, View):
    form_class = ChangePasswordForm

    def post(self, request, *args, **kwargs):
        data = self.form_class(request.data)
        old_password = data.cleaned_data['old_password']
        new_password = data.cleaned_data['new_password']
        confirm_password = data.cleaned_data['confirm_password']

        if not request.user.check_password(old_password):
            pass
