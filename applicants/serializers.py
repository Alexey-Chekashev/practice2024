from rest_framework.serializers import ModelSerializer
from applicants.models import Achievement


class AchievementSerializer(ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['org_address', 'org_phone', 'org_email', 'research_goal', 'relevance', 'expected_results', 'status']
