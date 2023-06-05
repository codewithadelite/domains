from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpRequest

from .serializers import DomainSerializer, FlagSerializer


class DomainsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Register Domains in the system.
        """
