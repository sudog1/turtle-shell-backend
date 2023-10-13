from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from accounts.models import User
from accounts.serializers import (
    FollowListSerializer,
    UserCreateSerializer,
    UserInfoSerializer,
)
from articles.models import Style, Article
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Prefetch


class UserView(APIView):
    # 프로필 정보
    def get(self, request, user_id=None, format=None):
        if user_id:
            user = get_object_or_404(get_user_model().objects, pk=user_id)
        else:
            user = request.user
            if not user.is_authenticated:
                return Response(
                    {"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
                )

        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        if not request.user.is_authenticated:
            Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserCreateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user
        if not user.is_authenticated:
            Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        password = request.data.get("password", "")
        auth_user = authenticate(username=user.username, password=password)
        if auth_user:
            auth_user.delete()
            return Response({"message": "회원 탈퇴 완료."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "비밀번호 불일치."}, status=status.HTTP_403_FORBIDDEN)


class FollowView(APIView):
    def get(self, request, user_id, format=None):
        user = request.user
        if not user.is_authenticated:
            Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        # 맞팔로우 확인
        target = get_object_or_404(get_user_model(), pk=user_id)
        if target != user:
            if (target in user.following.all()) and (user in target.following.all()):
                pass
            else:
                return Response(
                    {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
                )

        target = get_object_or_404(
            get_user_model().objects.prefetch_related(
                Prefetch(
                    "following", queryset=get_user_model().objects.only("nickname")
                ),
                Prefetch(
                    "followers", queryset=get_user_model().objects.only("nickname")
                ),
            ),
            pk=user_id,
        )
        serializer = FollowListSerializer(target)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, format=None):
        user = request.user  # 현재 유저
        if not user.is_authenticated:
            Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        target = get_object_or_404(get_user_model(), pk=user_id)  # 팔로우를 누른 대상

        if target in user.following.all():
            user.following.remove(target)
        else:
            user.following.add(target)
        followers_count = target.followers.count()
        return Response({"followers_count": followers_count}, status=status.HTTP_200_OK)
