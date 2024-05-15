from django.db import models
from django.contrib.auth.models import User


class ServiceUser(User):
    is_reviewer = models.BooleanField(default=False)
