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
from accounts.models import User


class ArticleView(APIView):
    def get(self, request, user_id=None, format=None):
        if not user_id:
            articles = Article.objects.all()
            serializer = ArticleListSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = User.objects.get(pk=user_id)
            user_styles = user.styles.all()

            articles = (
                Article.objects.all()
                .prefetch_related("styles")
                .filter(styles__in=user_styles)
            )

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
        return Response({"message": "삭제되었습니다"}, tatus=status.HTTP_200_OK)


class CommentView(APIView):
    def get(self, request, article_id):
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
    def put(self, request, article_id, comment_id, format=None):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user != comment.author:
            return Response({"message": "권한이 없습니다"}, 401)
        serializer = CommentCreateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, comment_id, format=None):
        comment = Comment.objects.get(id=comment_id)
        if request.user != comment.author:
            return Response({"message": "권한이 없습니다"}, 401)
        comment.delete()
        return Response({"message": "삭제되었습니다"})


class ArticleLikeView(APIView):
    def post(self, request, user_id, article_id, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "로그인 해주세요"}, 401)
        target = get_object_or_404(Article, id=article_id)
        if target in user.article_likes.all():
            user.article_likes.remove(target)
            return Response({"detail": "좋아요를 눌렀습니다"})
        else:
            user.article_likes.add(target)
            return Response({"detail": "좋아요를 취소했습니다"})


class CommentLikeView(APIView):
    def post(self, request, user_id, article_id, comment_id, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "로그인 해주세요"}, 401)
        target = get_object_or_404(Comment, id=comment_id)
        if target in user.comment_likes.all():
            user.comment_likes.remove(target)
            return Response({"detail": "좋아요를 눌렀습니다"})
        else:
            user.comment_likes.add(target)
            return Response({"detail": "좋아요를 취소했습니다"})
