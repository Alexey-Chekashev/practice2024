import rest_framework.viewsets
from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.db.models import F, Q
from rest_framework import (generics, mixins, response, status, permissions, viewsets)
from applicants import serializers, models
from users.auth import BearerTokenAuthentication
import csv
# Create your views here.


class AchievementView(viewsets.ViewSetMixin, generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = serializers.AchievementSerializer
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [BearerTokenAuthentication,]

    def get_queryset(self):
        return models.Achievement.objects.prefetch_related('authors').filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not models.Achievement.objects.filter(user=request.user, created__year=timezone.now().year).count() < 5:
            return response.Response(status=status.HTTP_417_EXPECTATION_FAILED)
        serializer.create(serializer.validated_data | {'user':request.user})
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        old_status = instance.status
        new_status = serializer.validated_data.get('status', None)
        if old_status == 'sent' or new_status is None:
            return response.Response(status=status.HTTP_417_EXPECTATION_FAILED)
        elif old_status == 'saved':
            serializer = serializers.AchievementSerializer(instance, context={'status': new_status})
            new_serializer = serializers.AchievementSerializer(data={'status': new_status})
            new_serializer.update(instance, new_serializer.data)
            return response.Response(serializer.data)
        else:
            serializer.update(instance, serializer.validated_data)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return response.Response(serializer.data)



