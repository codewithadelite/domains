from rest_framework import serializers
from flags.models import Domain, Flag


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["fqdn", "created_at", "expire_at", "deleted_at"]


class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ["domain", "flag_type", "valid_from", "valid_to"]
