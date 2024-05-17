from rest_framework.serializers import ModelSerializer
from applicants.models import Achievement, Author


class AuthorSerializer(ModelSerializer):
    model = Author
    fields = ['id', 'order_number', 'first_name', 'middle_name', 'last_name', 'degree']


class AchievementSerializer(ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id','org_address', 'org_phone', 'org_email', 'research_goal', 'relevance', 'expected_results',
                  'authors', 'status']
        depth = 1

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        achievement = Achievement(**validated_data)
        for author_data in authors_data:
            instance, _ = Author.objects.get_or_create(kwargs=author_data)
            achievement.authors.add(instance)
        achievement.save()
        return achievement

    # def update(self, instance, validated_data):
    #     pass