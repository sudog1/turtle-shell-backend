from django.urls import path
from . import views
    

urlpatterns = [
    path("", views.ArticleView.as_view(), name="article"),
    path("<int:article_id>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("<int:article_id>/comments/", views.CommentView.as_view(), name="comment"),
    path(
        "<int_article_id>/comments/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "<int:article_id>/likes/", views.ArticleLikeView.as_view(), name="article_like"
    ),
    path(
        "<int:article_id>/comments/<int:comment_id>/likes/",
        views.CommentLikeView.as_view(),
        name="comment_like",
    ),
]
