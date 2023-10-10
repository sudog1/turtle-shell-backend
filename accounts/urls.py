from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from articles.views import ArticleView
from .views import (
    UserView,
    FollowView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # 회원가입/회원수정/회원탈퇴
    path("", UserView.as_view(), name="account"),
    # 프로필 정보
    path("<int:user_id>/", UserView.as_view(), name="account_profile"),
    # 팔로우 기능
    path("follow/<int:user_id>/", FollowView.as_view(), name="account_follow"),
]
