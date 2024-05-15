from django.shortcuts import render,get_object_or_404
from rest_framework import (generics, mixins, authentication, response, status, permissions)
from applicants import serializers, models
# Create your views here.


class AchievementView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = serializers.AchievementSerializer
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [authentication.TokenAuthentication,]

    def get_queryset(self):
        return models.Achievement.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not models.Achievement.objects.filter(user=request.user).count() < 5:
            return response.Response(status=status.HTTP_417_EXPECTATION_FAILED)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


