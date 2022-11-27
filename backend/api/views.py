from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND)
from .serializers import InfoUserSerializer, SetPasswordSerializer, IngredientSerializer, TagSerializer, GetRecipeSerializer, PostRecipeSerializer, SingUpSerializer
from users.models import User
from recipes.models import Ingredient, Tag, Recipe
from django.contrib.auth.hashers import make_password


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
            User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password)
            )
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
                password = make_password(serializer.data.get('new_password'))
                user = User.objects.filter(username=request.user)
                user.update(password=password)
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

    def get_permissions(self):
        if self.request.method in ("POST",):
            permission_classes = (permissions.IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in ("POST",):
            return PostRecipeSerializer     
        return GetRecipeSerializer