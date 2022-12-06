from api.filters import IngredientFilter, RecipeFilter
from api.paginations import PageNumberAsLimitOffset
from api.permissions import IsAdminOrAuthorOrReadOnly
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import (FavoriteRecipe, Ingredient, IngredientInRecipeAmount,
                     Recipe, ShoppingCart, Tag)
from .serializers import (GetRecipeSerializer, IngredientSerializer,
                          IngredientWithAmountSerializer, PostRecipeSerializer,
                          RecipeInFavoriteAndShoppingCartSerializer,
                          TagSerializer)


class GetIngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение ингредиентов
    Эндпоинт api/ingredients/"""
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('name',)


class GetTagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение тегов
    Эндпоинт: api/tags/"""
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Взаимодействие с рецептами, получение, создание, обновление, удаление
    Эндпоинт api/recipes/"""
    queryset = Recipe.objects.all().order_by('-pub_date')
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    pagination_class = PageNumberAsLimitOffset
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.request.method in ("POST",):
            self.permission_classes = (permissions.IsAuthenticated,)
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return PostRecipeSerializer
        return GetRecipeSerializer


class RecipeInFavoriteView(APIView):
    """Взаимодействие с добавлением в избранное рецепта
    и его удалением
    Эндпоинт api/recipes/<int:pk>/favorite/"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if FavoriteRecipe.objects.filter(user=request.user,
                                         recipe=recipe).exists():
            return Response(data="Ошибка: Рецепт уже добавлен в"
                                 " избранное.",
                            status=HTTP_400_BAD_REQUEST)

        serializer = RecipeInFavoriteAndShoppingCartSerializer(recipe)
        FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if FavoriteRecipe.objects.filter(user=request.user,
                                         recipe=recipe).exists():
            FavoriteRecipe.objects.filter(user=request.user,
                                          recipe=recipe).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(data="""Ошибка: Рецепт не в избранном.""",
                        status=HTTP_400_BAD_REQUEST)


class RecipeInShoppingCartView(APIView):
    """Взаимодействие с добавлением, удалением рецепта из списка покупок
    Эндпоинт /api/recipes/<int:pk>/shopping_cart/"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if ShoppingCart.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            return Response(data="Ошибка: Рецепт уже добавлен в"
                                 " список покупок.",
                            status=HTTP_400_BAD_REQUEST)

        serializer = RecipeInFavoriteAndShoppingCartSerializer(recipe)
        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if ShoppingCart.objects.filter(user=request.user,
                                       recipe=recipe).exists():
            ShoppingCart.objects.filter(user=request.user,
                                        recipe=recipe).delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(data="Ошибка: Рецепта нет в списке покупок.",
                        status=HTTP_400_BAD_REQUEST)


class LoadShoppingCart(APIView):
    """Взаимодействие с скачиванием рецепта, в котором повторяющиеся
    ингредиенты соединены
    Эндпоинт /api/recipes/download_shopping_cart"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ingredients = IngredientInRecipeAmount.objects.filter(
            recipe__recipeinshopcart__user=request.user
        )
        result = {}
        serializer = IngredientWithAmountSerializer(ingredients, many=True)
        for data in serializer.data:
            name_ingredient = data.get('name')
            amount_ingredient = data.get('amount')
            measurement_unit = data.get('measurement_unit')
            if name_ingredient in result:
                result[name_ingredient][0] += amount_ingredient
                continue
            result[name_ingredient] = [amount_ingredient, measurement_unit]

        text_for_file = 'Список покупок:\n'
        for key, value in result.items():
            text_for_file += f'{key.capitalize()} ({value[1]}) - {value[0]}\n'

        response = HttpResponse(content=text_for_file,
                                content_type='text/plain')
        filename = 'shopitems.txt'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
