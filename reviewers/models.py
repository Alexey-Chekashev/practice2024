from django.db import models
from applicants.models import Achievement
from users.models import ServiceUser
# Create your models here.


class ApplicationVote(models.Model):
    application = models.ForeignKey(to=Achievement, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(to=ServiceUser, on_delete=models.CASCADE)
    approved = models.BooleanField()