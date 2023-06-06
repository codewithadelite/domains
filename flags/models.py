from django.db import models
from django.utils import timezone


class Domain(models.Model):
    fqdn = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    expire_at = models.DateTimeField()
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.fqdn

    @property
    def is_active(self) -> bool:
        if self.deleted_at is not None:
            return False
        if self.expire_at < timezone.now():
            return False
        return True


class Flag(models.Model):
    TYPE_CHOICES = (
        ("EXPIRED", "EXPIRED"),
        ("OUTZONE", "OUTZONE"),
        ("DELETE_CANDIDATE", "DELETE_CANDIDATE"),
    )
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    flag_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.domain.fqdn} - {self.flag_type}"

    @property
    def class_bg_color(self) -> str:
        if self.flag_type == self.TYPE_CHOICES[0][1]:
            return "badge badge-warning"
        if self.flag_type == self.TYPE_CHOICES[1][1]:
            return "badge badge-success"
        if self.flag_type == self.TYPE_CHOICES[2][1]:
            return "badge badge-danger"
