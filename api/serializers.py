from rest_framework import serializers
from api.models import Contributors, Projects, Issues, Comments


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
