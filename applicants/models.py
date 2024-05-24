from django.db import models
from users.models import User


class StatusConst:
    status_choices = {
        'draft': 'черновик',
        'saved': 'сохранена',
        'sent': 'отправлена на экспертизу'  # add rejected and approved states
    }


class Achievement(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)
    org_address = models.CharField(max_length=200)
    org_phone = models.CharField(max_length=12)
    org_email = models.EmailField()
    research_goal = models.CharField(max_length=500)
    relevance = models.CharField(max_length=500)
    expected_results = models.CharField(max_length=2000)
    status = models.CharField(max_length=5, choices=StatusConst.status_choices)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(auto_now=True)

    # def csv_representation(self):
    #     return f'"{self.user_id}","{self.org_address}","{self.org_phone}","{self.org_email}","{self.research_goal}","{self.relevance}","{self.expected_results}"'

    class Meta:
        indexes = [
            models.Index(fields=['sent', 'status'])
        ]


class Author(models.Model):
    achievement = models.ForeignKey(to=Achievement, on_delete=models.CASCADE)
    order_number = models.SmallIntegerField(blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['order_number'])
        ]

    # def csv_representation(self):
    #     return f'"{self.last_name},{self.first_name},{self.middle_name}"'

