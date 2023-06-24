from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Contributors, Projects, Issues, Comments

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                attrs["user"] = user
                return attrs
            raise serializers.ValidationError("Invalid username or password.")
        raise serializers.ValidationError("Username and password are required.")


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = "__all__"
        read_only_fields = ["contributors", "author_user"]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"
