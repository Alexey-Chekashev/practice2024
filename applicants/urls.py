from django.urls import path
from applicants.views import AchievementView


app_name = 'applicants'
urlpatterns = [
    path('achievements/', AchievementView.as_view()),
    path('achievements/<int:pk>/', AchievementView.as_view()),
]
