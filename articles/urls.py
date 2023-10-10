from django.urls import path
from . import views


urlpatterns = [
    path("", views.ArticleView.as_view(), name="all_article_list"),
    # 다른 유저가 쓴 글
    path("<int:user_id>/", views.ArticleView.as_view(), name="user_article_list"),
    # 유저가 선호할만한 글
    path("feed/", views.FeedView.as_view(), name="feed"),
    # 유저가 좋아요 누른 글
    path(
        "<int:user_id>/likes/",
        views.ArticleLikeView.as_view(),
        name="liked_article_list",
    ),
    # 게시글 상세
    path(
        "<int:user_id>/<int:article_id>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    # 게시글 코멘트
    path(
        "<int:user_id>/<int:article_id>/comments/",
        views.CommentView.as_view(),
        name="comment",
    ),
    # 댓글 생성/수정/삭제
    path(
        "<int:user_id>/<int:article_id>/comments/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment_detail",
    ),
    # 게시글 좋아요 기능
    path(
        "<int:user_id>/<int:article_id>/likes/",
        views.ArticleLikeView.as_view(),
        name="article_like",
    ),
    # 댓글 좋아요 기능
    path(
        "<int:user_id>/<int:article_id>/comments/<int:comment_id>/likes/",
        views.CommentLikeView.as_view(),
        name="comment_like",
    ),
]
