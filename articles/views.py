from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from articles.models import Comment, Article
from articles.serializers import (
    CommentSerializer,
    CommentCreateSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleSerializer,
)
from django.contrib.auth import get_user_model
from accounts.models import User


class FeedView(APIView):
    def get(self, request, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "로그인 해주세요"}, status=status.HTTP_403_FORBIDDEN)
        user_styles = user.styles.all()

        articles = (
            Article.objects.prefetch_related("styles")
            .filter(styles__in=user_styles)
            .distinct()
        )
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleView(APIView):
    def get(self, request, user_id=None, format=None):
        if not user_id:
            articles = Article.objects.all()
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = get_object_or_404(get_user_model(), pk=user_id)
            articles = Article.objects.filter(author=user)
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"message": "로그인 해주세요"}, 401)
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get(self, request, user_id, article_id, format=None):
        article = get_object_or_404(Article, pk=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id, article_id, format=None):
        article = get_object_or_404(Article, pk=article_id)
        if request.user != article.author:
            return Response({"message": "권한이 없습니다"}, 401)
        serializer = ArticleCreateSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "수정되었습니다"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, article_id, format=None):
        article = get_object_or_404(Article, pk=article_id)
        if request.user != article.author:
            return Response({"message": "권한이 없습니다"}, 401)
        article.delete()
        return Response({"message": "삭제되었습니다"}, status=status.HTTP_200_OK)


class CommentView(APIView):
    def get(self, request, user_id, article_id):
        article = Article.objects.get(id=article_id)
        comment = article.comments.all()
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, article_id, format=None):
        if not request.user.is_authenticated:
            return Response({"message": "로그인 해주세요"}, 401)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    def put(self, request, user_id, article_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return Response({"message": "권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, article_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return Response({"message": "권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"message": "삭제되었습니다"})


class ArticleLikeView(APIView):
    def get(self, request, user_id, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        # 맞팔로우 확인
        target = get_object_or_404(get_user_model(), pk=user_id)
        if target != user:
            if (target in user.followers.all()) and (user in target.followers.all()):
                pass
            else:
                return Response(
                    {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                )
        articles = target.article_likes.select_related("author").all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, article_id, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "로그인 해주세요"}, 401)
        target = get_object_or_404(Article, id=article_id)
        if target in user.article_likes.all():
            user.article_likes.remove(target)
            return Response({"detail": "좋아요 취소"})
        else:
            user.article_likes.add(target)
            return Response({"detail": "좋아요"})


class CommentLikeView(APIView):
    def post(self, request, user_id, article_id, comment_id, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "로그인 해주세요"}, status=status.HTTP_403_FORBIDDEN)
        target = get_object_or_404(Comment, id=comment_id)
        if user == target.author:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if target in user.comment_likes.all():
            user.comment_likes.remove(target)
            return Response({"detail": "좋아요 취소"})
        else:
            user.comment_likes.add(target)
            return Response({"detail": "좋아요"})
