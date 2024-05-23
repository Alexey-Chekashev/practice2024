from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from users.models import User
from reviewers.models import ApplicationVote


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']



