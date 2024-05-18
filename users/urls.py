from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import SignupView


app_name = 'users'
urlpatterns = [
    path('auth/', obtain_auth_token, name='auth'),
    path('reg/', SignupView.as_view(), name='registration'),
]
