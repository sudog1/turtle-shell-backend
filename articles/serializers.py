from rest_framework import serializers
from articles.models import Article, Comment, Product


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.nickname

    def get_article(self, obj):
        return obj.article.title

    class Meta:
        model = Comment
        fields = ("article", "author", "content", "created_at", "updated_at", "likes")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)
    likes = serializers.StringRelatedField(many=True)

    def get_author(self, obj):
        return obj.author.email

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "title",
            "image",
            "content",
            "styles",
            "products",
        )


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.nickname

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "image",
            "updated_at",
            "user",
            "likes_count",
            "comments_count",
        )
