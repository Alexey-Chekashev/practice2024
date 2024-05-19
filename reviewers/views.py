from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins, response, status, viewsets
from reviewers import permissions, serializers, models
from applicants.models import Achievement
from applicants.serializers import AchievementSerializer
from users.auth import BearerTokenAuthentication


class SubmittedView(viewsets.ViewSetMixin, generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin):
    permission_classes = [permissions.ReviewerPermission,]
    authentication_classes = [BearerTokenAuthentication,]

    def get_serializer_class(self):
        if self.request.method.lower() == "post":
            return serializers.VoteSerializer
        else:
            return AchievementSerializer

    def get_queryset(self):
        return Achievement.objects.filter(status='sent', applicationvote__isnull=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=request.user)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)