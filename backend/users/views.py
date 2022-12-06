from api.paginations import PageNumberAsLimitOffset
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from .models import Follow, User
from .serializers import (FollowSerializer, InfoUserSerializer,
                          SetPasswordSerializer, SingUpSerializer)


class UserSignUpAndView(generics.ListCreateAPIView):
    """Регистрация юзера и просмотр всех юзеров
    Эндпоинт api/users/"""
    queryset = User.objects.all()
    serializer_class = InfoUserSerializer
    pagination_class = PageNumberAsLimitOffset

    def create(self, request):
        serializer = SingUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            email = serializer.data.get('email')
            first_name = serializer.data.get('first_name')
            last_name = serializer.data.get('last_name')
            password = serializer.data.get('password')
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save()
            new_serializer_data = serializer.data
            new_serializer_data.pop("password")
            new_serializer_data["id"] = user.id
            return Response(data=new_serializer_data, status=HTTP_201_CREATED)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """Просмотр данных конкретного пользователя по его id
    Эндпоинт api/users/<id>/"""
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = InfoUserSerializer


class MeUserProfileView(APIView):
    """Просмотри личных данных с использованием токена
    Эндпоинт api/users/me/"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = InfoUserSerializer(request.user)
        return Response(data=serializer.data)


class UserSetPasswordView(APIView):
    """Изменение пароля юзером с использованием токена
    Эндпоинт api/users/set_password/"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if (
                serializer.data.get('new_password') ==
                serializer.data.get('current_password')
            ):
                # password = make_password(serializer.data.get('new_password'))
                password = (serializer.data.get('new_password'))
                user = User.objects.get(username=request.user)
                user.set_password(password)
                user.save()
                return Response(status=HTTP_204_NO_CONTENT)
            return Response('Passwords do not match',
                            status=HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors,
                        status=HTTP_400_BAD_REQUEST)


class UserFollowView(generics.ListAPIView):
    """Взаимодействие с списком подписок, обзор всех своих подписок
    Эндпоинт api/users/subscriptions/"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    pagination_class = PageNumberAsLimitOffset

    def get_queryset(self):
        following_users = (User.objects
                           .filter(following__user=self.request.user))
        return following_users


class AddFollowView(APIView):
    """Взаимодействие с подпиской и отпиской от юзера
    Эндпоинт /api/users/<int:pk>/subscribe/"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if Follow.objects.filter(user=request.user, author=user).exists():
            return Response(data="Ошибка: Вы уже подписаны на данного"
                                 " пользователя.",
                            status=HTTP_400_BAD_REQUEST)
        elif request.user == user:
            return Response(data="Ошибка: Вы не можете подписаться на себя.",
                            status=HTTP_400_BAD_REQUEST)

        Follow.objects.create(user=request.user, author=user)
        serializer = FollowSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if Follow.objects.filter(user=request.user, author=user).exists():
            Follow.objects.filter(user=request.user, author=user).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
