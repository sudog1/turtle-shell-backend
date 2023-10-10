from rest_framework import serializers
from articles.models import Article, Comment, Style


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
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    # likes = serializers.StringRelatedField(many=True)
    likes = serializers.SerializerMethodField()

    def get_author(self, obj):
        return {"id": obj.author.pk, "nickname": obj.author.nickname}

    def get_likes(self, obj):
        return obj.likes.count()

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    styles = serializers.PrimaryKeyRelatedField(queryset=Style.objects.all(), many=True)

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
        return obj.comments.count()

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "image",
            "updated_at",
            "author",
            "likes_count",
            "comments_count",
            "styles",
        )
