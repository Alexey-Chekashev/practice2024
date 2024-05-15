from django.contrib import admin
from users.models import ServiceUser
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(ServiceUser)
admin.site.register(Token)