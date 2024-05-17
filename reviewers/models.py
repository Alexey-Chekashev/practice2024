from django.db import models
from applicants.models import Achievement
from users.models import User
# Create your models here.


class ApplicationVote(models.Model):
    application = models.ForeignKey(to=Achievement, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    approved = models.BooleanField()
    voted_time = models.DateTimeField(auto_now_add=True)