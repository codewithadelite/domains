from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("domains/", views.DomainListView.as_view(), name="domains"),
    path("domains/create/", views.AddDomainsView.as_view(), name="add-domains"),
    path("domains/<int:id>/",
         views.DomainDetailView.as_view(), name="domain-details"),
    path("settings/", views.SettingsView.as_view(), name="settings"),

]
