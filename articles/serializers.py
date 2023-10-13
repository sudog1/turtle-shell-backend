from rest_framework import serializers
from articles.models import Article, Comment, Style
from products.models import Product
from products.serializers import ProductListSerializer


class StyleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = "__all__"


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()

    def get_author(self, obj):
        return {"id": obj.author.pk, "nickname": obj.author.nickname}

    class Meta:
        model = Comment
        fields = (
            "author",
            "content",
            "updated_at",
            "likes_count",
        )


class CommentReadSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {"id": obj.author.pk, "nickname": obj.author.nickname}

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Comment
        fields = (
            "author",
            "content",
            "updated_at",
            "likes_count",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    products = ProductListSerializer(many=True)
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()

    def get_author(self, obj):
        return {"id": obj.author.pk, "nickname": obj.author.nickname}

    class Meta:
        model = Article
        fields = (
            "author",
            "title",
            "content",
            "created_at",
            "image",
            "style",
            "likes_count",
            "comments_count",
            "products",
        )


class ArticleCreateSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Article
        fields = (
            "title",
            "image",
            "content",
            "style",
            "products",
        )


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()

    def get_author(self, obj):
        return {
            "id": obj.author.pk,
            "nickname": obj.author.nickname,
        }

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "image",
            "created_at",
            "author",
            "likes_count",
            "comments_count",
            "style",
        )
