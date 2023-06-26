from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.http import HttpRequest

from typing import List

from flags.types import DomainsData

# Background tasks imports
from flags.tasks import process_and_save_domains

from .serializers import DomainSerializer, FlagSerializer


class DomainsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest, *args, **kwargs):
        """
        Register Domains in the database.
        """

        try:
            data: List[DomainsData] = request.data
            # Run bg task to process domains data and save to database
            process_and_save_domains.delay(domains=data)

        except Exception as e:
            # TODO We need to find the way of logging errors
            return Response(
                {"result": "failed", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"result": "success", "message": "domains uploaded successfully"},
            status=status.HTTP_200_OK,
        )
