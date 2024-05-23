from rest_framework import generics, response, status, permissions
from rest_framework.authtoken.models import Token
from users import serializers, permissions as user_permissions, auth, dump_csv, models
from django.contrib.auth.hashers import make_password
from reviewers.serializers import VoteSerializer
from django.http import FileResponse


class SignupView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [user_permissions.UnauthorizedPermission,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop('password')
        if not password == serializer.initial_data.get('password2'):
            return response.Response(data={'detail':'passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        instance = models.User.objects.create(**(serializer.validated_data | {'password': make_password(password)}))
        Token.objects.create(user=instance)
        headers = self.get_success_headers(serializer.data)
        return response.Response(status=status.HTTP_201_CREATED, headers=headers)


class DumpCSVView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser,]
    authentication_classes = [auth.BearerTokenAuthentication,]
    serializer_class = VoteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option = serializer.validated_data.get('approved')
        filename = dump_csv.dump_csv(option)
        return FileResponse(open(filename, 'rb'))



