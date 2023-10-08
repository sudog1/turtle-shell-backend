from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import (
    UserView,
    FollowView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("", UserView.as_view(), name="account"),
    path("<int:user_id>/", UserView.as_view(), name="account_profile"),
    path("follow/<int:user_id>/", FollowView.as_view(), name="account_follow"),
]
