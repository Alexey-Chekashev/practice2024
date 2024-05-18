from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer, User
from users.permissions import UnauthorizedPermission
from rest_framework.authtoken.models import Token
from  django.contrib.auth.hashers import make_password


class SignupView(CreateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [UnauthorizedPermission,]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        if not password == serializer.initial_data.get('password2'):
            return Response(data={'detail':'passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        instance = User.objects.create(**(serializer.validated_data | {'password': make_password(password)}))
        if instance is not None:
            Token.objects.create(user=instance)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)




