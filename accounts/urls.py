from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import (
    AccountView,
    AccountProfileView,
    AccountFollowView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path('', AccountView.as_view(),name='account'),
    path('<int:user_id>/',AccountProfileView.as_view(), name='account_profile'),
    path('follow/<int:user_id>/',AccountFollowView.as_view(), name='account_follow'),
]

