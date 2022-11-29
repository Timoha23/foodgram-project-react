from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT)

from .serializers import InfoUserSerializer, SetPasswordSerializer, IngredientSerializer, TagSerializer, GetRecipeSerializer, PostRecipeSerializer, SingUpSerializer, GetSubsSerializer
from .permissions import IsAdminOrAuthorOrReadOnly
from users.models import User, Follow
from recipes.models import Ingredient, Tag, Recipe
from django.shortcuts import get_object_or_404


class UserSignUpAndView(generics.ListCreateAPIView):
    """Регистрация юзера и просмотр всех юзеров
    Эндпоинт api/users/"""
    queryset = User.objects.all()
    serializer_class = InfoUserSerializer

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
            return Response(data=serializer.data, status=HTTP_200_OK)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


# СДЕЛАТЬ ЧЕРЕЗ РОУТЕР
class UserProfiles(generics.RetrieveAPIView):
    """Просмотр данных конкретного пользователя по его id
    Эндпоинт api/users/<id>/"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = InfoUserSerializer


class UserProfile(APIView):
    """Просмотри личных данных с использованием токена
    Эндпоинт api/users/me/"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = InfoUserSerializer(request.user)
        return Response(data=serializer.data)


class UserSetPassword(APIView):
    """Изменение пароля юзером с использованием токена
    Эндпоинт api/users/set_password/"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get('new_password') == serializer.data.get('current_password'):
                # password = make_password(serializer.data.get('new_password'))
                password = (serializer.data.get('new_password'))
                user = User.objects.get(username=request.user)
                user.set_password(password)
                user.save()
                return Response(status=HTTP_200_OK)
            return Response('Passwords do not match', status=HTTP_400_BAD_REQUEST)
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class GetIngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение ингредиентов
    Эндпоинт api/ingredients/"""
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class GetTagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение тегов
    Эндпоинт: api/tags/"""
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Взаимодействие с рецептами, получение, создание, обновление, удаление
    Эндпоинт api/recipes/"""
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    def get_permissions(self):
        if self.request.method in ("POST",):
            self.permission_classes = (permissions.IsAuthenticated,)
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return PostRecipeSerializer
        return GetRecipeSerializer


class UserSubscriptions(generics.ListAPIView):
    """Взаимодействие с списком подписок, обзор всех своих подписок
    Эндпоинт api/users/subscriptions/"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetSubsSerializer

    def get_queryset(self):
        following_users = User.objects.filter(following__user=self.request.user)
        return following_users


class AddSubView(APIView):
    """Взаимодействие с подпиской и отпиской от юзера
    Эндпоинт /api/users/<int:pk>/subscribe/"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if Follow.objects.filter(user=request.user, author=user).exists() or request.user==user:
            return Response(status=HTTP_400_BAD_REQUEST)

        Follow.objects.create(user=request.user, author=user)
        serializer = GetSubsSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if Follow.objects.filter(user=request.user, author=user).exists():
            Follow.objects.filter(user=request.user, author=user).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
