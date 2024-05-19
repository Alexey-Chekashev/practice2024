from rest_framework.serializers import ModelSerializer
from applicants.models import Achievement, Author
from rest_framework.exceptions import ValidationError
from django.db.models import Count


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'order_number', 'first_name', 'middle_name', 'last_name', 'degree']


class AchievementSerializer(ModelSerializer):
    authors = AuthorSerializer(many=True)
    class Meta:
        model = Achievement
        fields = ['id','org_address', 'org_phone', 'org_email', 'research_goal', 'relevance', 'expected_results',
                  'authors', 'status']
        depth = 1

    def create(self, validated_data):
        authors_data = validated_data.pop('authors', None)
        achievement = Achievement(**validated_data)
        achievement.save()
        for author_data in authors_data:
            instance, _ = Author.objects.get_or_create(**author_data)
            achievement.authors.add(instance)
        achievement.save()
        return achievement

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', None)
        prev_authors = instance.authors.all()
        if authors_data is not None:
            if len(authors_data) != prev_authors.count():
                raise ValidationError({'detail': 'authors amount mismatch'})
            else:
                for pa in prev_authors:
                    if pa.achievement_set.all().count() == 1:
                        pa.delete()
                instance.authors.clear()
                for author_data in authors_data:
                    new_author, _ = Author.objects.get_or_create(**author_data)
                    instance.authors.add(new_author)
                instance.save()
        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save()
        return instance
