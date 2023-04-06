from django.db import models


class Domain(models.Model):
    fqdn = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.fqdn


class Flag(models.Model):
    TYPE_CHOICES = (
        ("EXPIRED", "EXPIRED"),
        ("OUTZONE", "OUTZONE"),
        ("DELETE_CANDIDATE", "DELETE_CANDIDATE")

    )
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    flag_type = models.CharField(max_length=20, choices=TYPE_CHOICES,)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.domain.fqdn} - {self.flag_type}"
