from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_reviewer = models.BooleanField(default=False)

    def csv_representation(self):
        return f"{self.username},{self.email}"
