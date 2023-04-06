from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.DomainListView.as_view(), name="dashboard")
]
