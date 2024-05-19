from rest_framework.serializers import ModelSerializer
from reviewers.models import ApplicationVote


class VoteSerializer(ModelSerializer):
    class Meta:
        model = ApplicationVote
        fields = ['approved', 'application']



