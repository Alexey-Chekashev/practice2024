from django.urls import path
from reviewers.views import SubmittedView


app_name = 'reviewers'
urlpatterns = [
    path('submissions/', SubmittedView.as_view()),
    path('submissions/<int:pk>/', SubmittedView.as_view())
]