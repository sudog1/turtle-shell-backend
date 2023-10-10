from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import get_user_model

from articles.models import Style


class UserInfoSerializer(serializers.ModelSerializer):
    def get_styles(self, obj):
        queryset = obj.styles.all()
        return [{"id": style.id, "name": style.name} for style in queryset]

    class Meta:
        model = get_user_model()
        fields = ("email", "nickname", "image", "styles")


class UserCreateSerializer(serializers.ModelSerializer):
    styles = serializers.PrimaryKeyRelatedField(queryset=Style.objects.all(), many=True)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password",
            "nickname",
            "styles",
        )
        extra_kwargs = {"password": {"write_only": True}}

    normalized_fields = ["email"]

    def is_valid(self, *, raise_exception=False):
        for field in self.normalized_fields:
            if field == "email":
                self.initial_data["email"] = get_user_model().objects.normalize_email(
                    self.initial_data.get(field)
                )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class FollowListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nickname = serializers.CharField()

    followers = serializers.SerializerMethodField()
    followees = serializers.SerializerMethodField()

    def get_followers(self, obj):
        queryset = obj.followers.all()
        return [
            {"id": follower.id, "nickname": follower.nickname} for follower in queryset
        ]

    def get_followees(self, obj):
        queryset = obj.followees.all()
        return [
            {"id": followee.id, "nickname": followee.nickname} for followee in queryset
        ]

    class Meta:
        model = get_user_model()
        fields = ("id", "nickname", "followers", "followees")
