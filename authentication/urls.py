from django.urls import path
from . import views


urlpatterns = [
    path("", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout")
]
