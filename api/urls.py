from django.urls import path

from .views import DomainsAPIView

urlpatterns = [path("domains/", DomainsAPIView.as_view(), name="domains")]
