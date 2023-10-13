from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import get_user_model

from articles.models import Style


class UserInfoSerializer(serializers.ModelSerializer):
    styles = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    

    def get_styles(self, obj):
        queryset = obj.styles.all()
        return [{"id": style.id, "name": style.name} for style in queryset]

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "nickname",
            "image",
            "styles",
            "following_count",
            "followers_count",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    styles = serializers.PrimaryKeyRelatedField(
        queryset=Style.objects.all(),
        many=True,
        required=False,
    )

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

    def is_valid(self, *, raise_exception=False):
        self.initial_data["email"] = get_user_model().objects.normalize_email(
            self.initial_data.get("email")
        )
        self.initial_data["username"] = self.initial_data["username"].lower()
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
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
