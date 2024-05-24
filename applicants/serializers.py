import copy
from rest_framework.serializers import ModelSerializer
from applicants.models import Achievement, Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'middle_name', 'last_name', 'degree']


class AchievementSerializer(ModelSerializer):
    author_set = AuthorSerializer(many=True)

    class Meta:
        model = Achievement
        fields = ['id','org_address', 'org_phone', 'org_email', 'research_goal', 'relevance', 'expected_results',
                  'author_set','status']
        depth = 1

    def create(self, new_data):
        validated_data = copy.deepcopy(new_data)
        authors_data = validated_data.pop('author_set', None)
        achievement = Achievement(**validated_data)
        achievement.save()
        order = 1
        for author_data in authors_data:
            Author.objects.create(**(author_data | {"order_number": order, "achievement": achievement}))
            order += 1
        return achievement

    def update(self, instance, new_data):
        validated_data = copy.deepcopy(new_data)
        authors_data = validated_data.pop('author_set', None)
        if authors_data is not None:  # в случае если обновляется только статус, не обновлять авторов
            authors = instance.author_set.all()
            order = authors.count()+1
            for author in authors:
                try:
                    author_data = authors_data[0]
                    del authors_data[0]
                    for key, value in author_data.items():
                        setattr(author, key, value)
                    author.save()
                except IndexError:
                    author.delete()
            for data in authors_data:
                Author.objects.create(**(data | {"order_number": order, "achievement": instance}))
                order += 1
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
