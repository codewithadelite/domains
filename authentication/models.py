from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    names = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.names
