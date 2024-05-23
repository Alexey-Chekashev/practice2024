from django.utils import timezone
from rest_framework import (generics, mixins, response, status, permissions)
from applicants import serializers, models
from users.auth import BearerTokenAuthentication


class AchievementView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = serializers.AchievementSerializer
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [BearerTokenAuthentication,]

    def get_queryset(self):
        return models.Achievement.objects.prefetch_related('author_set').filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None) is not None:
            return self.retrieve(self, request, *args, **kwargs)
        else:
            return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not models.Achievement.objects.filter(user=request.user, created__year=timezone.now().year).count() < 5:
            return response.Response(status=status.HTTP_417_EXPECTATION_FAILED)
        serializer.create(serializer.validated_data | {'user': request.user})
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        old_status = instance.status
        new_status = serializer.validated_data.get('status', None)
        if old_status == 'sent':  # нельзя менять, если отправлено
            return response.Response(status=status.HTTP_417_EXPECTATION_FAILED,data={"detail":"can't update sent"})
        elif old_status == 'saved':  # можно обновлять только статус
            new_serializer = serializers.AchievementSerializer(data={'status': new_status})
            new_serializer.update(instance, {'status': new_status})
            return response.Response(data={'status': new_status})
        else:
            serializer.update(instance, serializer.validated_data)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return response.Response(serializer.data)

