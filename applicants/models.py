from django.db import models
from users.models import User


# Create your models here.
class Author(models.Model):
    class Meta:
        ordering = ['order_number',]
    order_number = models.SmallIntegerField()
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)


class Achievement(models.Model):
    class Meta:
        ordering = ['-sent',]
    status_choices = {
        'draft':'черновик',
        'saved':'сохранена',
        'sent':'отправлена на экспертизу'
    }
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True)
    org_address = models.CharField(max_length=200)
    org_phone = models.CharField(max_length=12)
    org_email = models.EmailField()
    research_goal = models.CharField(max_length=500)
    relevance = models.CharField(max_length=500)
    expected_results = models.CharField(max_length=2000)
    status = models.CharField(max_length=5, choices=status_choices)
    authors = models.ManyToManyField(Author)
    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (
            self.user,
            ", ".join(author.last_name for author in self.authors.all()),
        )


