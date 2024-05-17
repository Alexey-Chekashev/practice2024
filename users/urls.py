from django.urls import path, include
from rest_framework.authtoken import views


app_name = 'users'
urlpatterns = [
    path('auth/', views.obtain_auth_token, name='auth'),
]
