from django.urls import path, include
from reviewers.views import SubmittedView
from rest_framework.routers import SimpleRouter


app_name = 'reviewers'
router = SimpleRouter()
router.register(r'submissions', SubmittedView, basename='submissions')
urlpatterns = [
]
urlpatterns += router.urls


