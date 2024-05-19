from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status, permissions
from users.serializers import UserSerializer, User
from users.permissions import UnauthorizedPermission
from rest_framework.authtoken.models import Token
from  django.contrib.auth.hashers import make_password
from users.auth import BearerTokenAuthentication
from applicants.models import Achievement, Author
from reviewers.models import ApplicationVote
import csv, copy, datetime, os


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


class DumpCSVView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser,]
    authentication_classes = [BearerTokenAuthentication,]

    def post(self, request, *args, **kwargs):
        fields = 'user,org_address,org_phone,org_email,research_goal,relevance,expected_results,authors,voted_by'+'\n'
        approved = Achievement.objects.filter(applicationvote__approved=True).select_related('user').prefetch_related('applicationvote_set', 'authors')
        rejected = Achievement.objects.filter(applicationvote__approved=False).select_related('user').prefetch_related('applicationvote_set', 'authors')
        current_datetime = str(datetime.datetime.now()).split(':')
        current_datetime = '_'.join(current_datetime)
        yes_file = open(f'csvs\\approved_achievements_{current_datetime}.csv', 'w+')
        no_file = open(f'csvs\\rejected_achievements_{current_datetime}.csv', 'w+')
        yes_file.write(fields)
        no_file.write(fields)
        for inst in approved:
            authors = inst.authors.all()
            authors_csv = ',['
            for author in authors:
                authors_csv = authors_csv+author.csv_representation()+","
            authors_csv = authors_csv[:-1] + ']'
            voted_by = inst.applicationvote_set.first().reviewer.csv_representation()
            yes_file.write(inst.csv_representation()+authors_csv+','+voted_by+'\n')
        for inst in rejected:
            authors = inst.authors.all()
            authors_csv = ',['
            for author in authors:
                authors_csv = authors_csv + author.csv_representation() + ","
            authors_csv = authors_csv[:-1] + ']'
            voted_by = inst.applicationvote_set.first().reviewer.csv_representation()
            no_file.write(inst.csv_representation()+authors_csv+','+voted_by+'\n')
        yes_file.close()
        no_file.close()
        return Response(status=status.HTTP_200_OK, data={"success":"succesfully exported achievements to .csv"})







