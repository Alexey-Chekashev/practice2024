from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from users.serializers import UserSerializer, User, UserViewSerializer
from users.permissions import UnauthorizedPermission
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from users.auth import BearerTokenAuthentication
from reviewers.serializers import VoteSerializer
from users.dump_csv import dump_csv
from django.http import HttpResponse, FileResponse


class SignupView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [UnauthorizedPermission,]

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


class DumpCSVView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser,]
    authentication_classes = [BearerTokenAuthentication,]
    serializer_class = VoteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option = serializer.validated_data.get('approved')
        filename = dump_csv(option)
        return FileResponse(open(filename, 'rb'))


class ReviewerView(ListAPIView):
    queryset = User.objects.filter(is_reviewer=True)
    permission_classes = [permissions.IsAdminUser,]
    authentication_classes = [BearerTokenAuthentication,]
    serializer_class = UserViewSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



