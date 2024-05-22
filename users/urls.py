from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import SignupView, DumpCSVView, ReviewerView


app_name = 'users'
urlpatterns = [
    path('auth/', obtain_auth_token, name='auth'),
    path('reg/', SignupView.as_view(), name='registration'),
    path('dump_csv/', DumpCSVView.as_view(), name='dump_csv'),
    path('reviewers/', ReviewerView.as_view())
]
