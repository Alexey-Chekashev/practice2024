from django.db import models
from users.models import ServiceUser


# Create your models here.
class Author(models.Model):#подумать над порядком
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)


class Achievement(models.Model):
    status_choices = {
        'dr':'черновик',
        'sa':'сохранена',
        'se':'отправлена на экспертизу'
    }
    user = models.ForeignKey(to=ServiceUser, on_delete=models.CASCADE)
    org_address = models.CharField(max_length=200)
    org_phone = models.CharField(max_length=12)
    org_email = models.EmailField()
    research_goal = models.CharField(max_length=500)
    relevance = models.CharField(max_length=500)
    expected_results = models.CharField(max_length=2000)
    status = models.CharField(max_length=2, choices=status_choices)
    # authors = models.ManyToManyField(to=Author)#подумать как хранить много авторов
    created = models.DateField(auto_now_add=True)


