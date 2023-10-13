from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from articles.models import Comment, Article, Style
from articles.serializers import (
    CommentListSerializer,
    CommentReadSerializer,
    CommentCreateSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleSerializer,
    StyleListSerializer,
)
from django.contrib.auth import get_user_model
from accounts.models import User
from django.db.models import Count


class FeedView(APIView):
    def get(self, request, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "로그인 해주세요"}, status=status.HTTP_403_FORBIDDEN)
        user_styles = user.styles.all()

        articles = Article.objects.select_related("styles").filter(
            styles__in=user_styles
        )
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleView(APIView):
    def get(self, request, user_id=None, format=None):
        if not user_id:
            articles = (
                Article.objects.select_related("author", "style")
                .only("title", "image", "created_at", "author__nickname", "style__name")
                .annotate(
                    likes_count=Count("likes", distinct=True),
                    comments_count=Count("comments", distinct=True),
                )
            )
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = get_object_or_404(get_user_model(), pk=user_id)
            articles = (
                Article.objects.filter(author=user)
                .select_related("author", "style")
                .only("title", "image", "created_at", "author__nickname", "style__name")
                .annotate(
                    likes_count=Count("likes", distinct=True),
                    comments_count=Count("comments", distinct=True),
                )
            )
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        print(request.data)
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get(self, request, article_id, format=None):
        article = get_object_or_404(
            Article.objects.prefetch_related("products").annotate(
                likes_count=Count("likes", distinct=True),
                comments_count=Count("comments", distinct=True),
            ),
            pk=article_id,
        )
        serializer = ArticleSerializer(article)
        data = serializer.data
        if request.user == article.author:
            data["is_owner"] = True
        else:
            data["is_owner"] = False
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, article_id, format=None):
        article = get_object_or_404(Article, pk=article_id)
        if request.user != article.author:
            return Response({"detail": "권한이 없습니다"}, 401)
        serializer = ArticleCreateSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "수정되었습니다"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, format=None):
        article = get_object_or_404(Article, pk=article_id)
        if request.user != article.author:
            return Response({"detail": "권한이 없습니다"}, 401)
        article.delete()
        return Response({"detail": "삭제되었습니다"}, status=status.HTTP_200_OK)


class CommentView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comments = (
            article.comments.select_related("author")
            .only("author__nickname", "content", "updated_at")
            .annotate(likes_count=Count("likes"))
        )
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, article_id=article_id)
            serializer = CommentReadSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return Response({"detail": "권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            comment = serializer.save()
            serializer = CommentReadSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return Response({"detail": "권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"detail": "삭제되었습니다"})


class ArticleLikeView(APIView):
    def get(self, request, article_id, format=None):
        article = get_object_or_404(
            Article.objects.select_related("author"), pk=article_id
        )
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        # 맞팔로우 확인
        target = article.author
        if target != user:
            if (target in user.following.all()) and (user in target.following.all()):
                pass
            else:
                return Response(
                    {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                )
        articles = target.article_likes.select_related("author", "style").annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        )
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        article = get_object_or_404(Article, id=article_id)
        if article in user.article_likes.all():
            user.article_likes.remove(article)
        else:
            user.article_likes.add(article)
        return Response(
            {"detail": "성공!", "likes_count": article.likes.count()},
            status=status.HTTP_200_OK,
        )


class CommentLikeView(APIView):
    def post(self, request, article_id, comment_id, format=None):
        article = get_object_or_404(Article, article_id)
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "로그인 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        target = get_object_or_404(Comment, id=comment_id)
        if user == target.author:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if target in user.comment_likes.all():
            user.comment_likes.remove(target)
            return Response({"detail": "좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            user.comment_likes.add(target)
            return Response({"detail": "좋아요"}, status=status.HTTP_200_OK)


class StyleView(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인 해주세요."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        styles = Style.objects.all()
        serializer = StyleListSerializer(styles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
