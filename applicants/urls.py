from django.urls import path, include
from applicants.views import AchievementView
from rest_framework.routers import SimpleRouter


app_name = 'applicants'
router = SimpleRouter()
router.register(r'achievements', AchievementView, basename='achievements')
urlpatterns = [
]
urlpatterns+=router.urls
