from rest_framework import generics, mixins, response, status
from reviewers import permissions, serializers as rev_serializers
from applicants import models, serializers as app_serializers
from users.auth import BearerTokenAuthentication


class SubmittedView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.ReviewerPermission,]
    authentication_classes = [BearerTokenAuthentication,]

    def get_serializer_class(self):
        if self.request.method.lower() == "put":  # при отправке данных о голосе используется сериализатор голосов
            return rev_serializers.VoteSerializer
        else:
            return app_serializers.AchievementSerializer  # используется для отображения отправленных достижений

    def get_queryset(self):
        return models.Achievement.objects.filter(status='sent', applicationvote__isnull=True).order_by('-sent')

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None) is not None:
            return self.retrieve(self, request, *args, **kwargs)
        else:
            return self.list(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=request.user, application=instance)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)