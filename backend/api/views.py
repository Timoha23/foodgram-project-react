# from django.http import HttpResponse
# from rest_framework import generics, permissions, viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.status import (HTTP_400_BAD_REQUEST,
#                                    HTTP_204_NO_CONTENT,
#                                    HTTP_201_CREATED)

# from .serializers import (InfoUserSerializer, SetPasswordSerializer,
#                           IngredientSerializer, TagSerializer,
#                           GetRecipeSerializer, PostRecipeSerializer,
#                           SingUpSerializer, FollowSerializer,
#                           RecipeInFavoriteAndShoppingCartSerializer,
#                           IngredientWithAmountSerializer)
# from .permissions import IsAdminOrAuthorOrReadOnly
# from users.models import User, Follow
# from recipes.models import (Ingredient, Tag, Recipe, FavoriteRecipe,
#                             ShoppingCart, IngredientInRecipeAmount)
# from django.shortcuts import get_object_or_404
# from backend.settings import SHOPPING_ROOT
# from datetime import datetime
# import os
# from rest_framework.filters import SearchFilter

# ####
# from .paginations import PageNumberAsLimitOffset
# from django_filters.rest_framework import DjangoFilterBackend
# from .filters import RecipeFilter
# ####


# # class UserSignUpAndView(generics.ListCreateAPIView):
# #     """Регистрация юзера и просмотр всех юзеров
# #     Эндпоинт api/users/"""
# #     queryset = User.objects.all()
# #     serializer_class = InfoUserSerializer
# #     pagination_class = PageNumberAsLimitOffset

# #     def create(self, request):
# #         serializer = SingUpSerializer(data=request.data)
# #         if serializer.is_valid():
# #             username = serializer.data.get('username')
# #             email = serializer.data.get('email')
# #             first_name = serializer.data.get('first_name')
# #             last_name = serializer.data.get('last_name')
# #             password = serializer.data.get('password')
# #             user = User.objects.create(
# #                 username=username,
# #                 email=email,
# #                 first_name=first_name,
# #                 last_name=last_name,
# #             )
# #             user.set_password(password)
# #             user.save()
# #             new_serializer_data = serializer.data
# #             new_serializer_data.pop("password")
# #             new_serializer_data["id"] = user.id
# #             return Response(data=new_serializer_data, status=HTTP_201_CREATED)
# #         return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


# # class UserProfileView(generics.RetrieveAPIView):
# #     """Просмотр данных конкретного пользователя по его id
# #     Эндпоинт api/users/<id>/"""
# #     # permission_classes = (permissions.IsAuthenticated,)
# #     queryset = User.objects.all()
# #     serializer_class = InfoUserSerializer


# # class MeUserProfileView(APIView):
# #     """Просмотри личных данных с использованием токена
# #     Эндпоинт api/users/me/"""
# #     permission_classes = (permissions.IsAuthenticated,)

# #     def get(self, request):
# #         serializer = InfoUserSerializer(request.user)
# #         return Response(data=serializer.data)


# # class UserSetPasswordView(APIView):
# #     """Изменение пароля юзером с использованием токена
# #     Эндпоинт api/users/set_password/"""
# #     permission_classes = (permissions.IsAuthenticated,)

# #     def post(self, request):
# #         serializer = SetPasswordSerializer(data=request.data)
# #         if serializer.is_valid():
# #             if (
# #                 serializer.data.get('new_password') ==
# #                 serializer.data.get('current_password')
# #             ):
# #                 # password = make_password(serializer.data.get('new_password'))
# #                 password = (serializer.data.get('new_password'))
# #                 user = User.objects.get(username=request.user)
# #                 user.set_password(password)
# #                 user.save()
# #                 return Response(status=HTTP_204_NO_CONTENT)
# #             return Response('Passwords do not match',
# #                             status=HTTP_400_BAD_REQUEST)
# #         return Response(data=serializer.errors,
# #                         status=HTTP_400_BAD_REQUEST)


# # class GetIngredientsViewSet(viewsets.ReadOnlyModelViewSet):
# #     """Получение ингредиентов
# #     Эндпоинт api/ingredients/"""
# #     pagination_class = None
# #     queryset = Ingredient.objects.all()
# #     serializer_class = IngredientSerializer
# #     filter_backends = (SearchFilter,)
# #     search_fields = ('name',)


# # class GetTagsViewSet(viewsets.ReadOnlyModelViewSet):
# #     """Получение тегов
# #     Эндпоинт: api/tags/"""
# #     pagination_class = None
# #     queryset = Tag.objects.all()
# #     serializer_class = TagSerializer


# # class RecipesViewSet(viewsets.ModelViewSet):
# #     """Взаимодействие с рецептами, получение, создание, обновление, удаление
# #     Эндпоинт api/recipes/"""
# #     queryset = Recipe.objects.all()
# #     permission_classes = (IsAdminOrAuthorOrReadOnly,)
# #     pagination_class = PageNumberAsLimitOffset
# #     filter_backends = (DjangoFilterBackend,)
# #     filterset_class = RecipeFilter

# #     def get_permissions(self):
# #         if self.request.method in ("POST",):
# #             self.permission_classes = (permissions.IsAuthenticated,)
# #         return super(self.__class__, self).get_permissions()

# #     def get_serializer_class(self):
# #         if self.request.method in ("POST", "PATCH"):
# #             return PostRecipeSerializer
# #         return GetRecipeSerializer


# # class UserFollowView(generics.ListAPIView):
# #     """Взаимодействие с списком подписок, обзор всех своих подписок
# #     Эндпоинт api/users/subscriptions/"""
# #     permission_classes = (permissions.IsAuthenticated,)
# #     serializer_class = SubsSerializer
# #     pagination_class = PageNumberAsLimitOffset

# #     def get_queryset(self):
# #         following_users = (User.objects
# #                            .filter(following__user=self.request.user))
# #         return following_users


# # class AddFollowView(APIView):
# #     """Взаимодействие с подпиской и отпиской от юзера
# #     Эндпоинт /api/users/<int:pk>/subscribe/"""
# #     permission_classes = (permissions.IsAuthenticated,)

# #     def post(self, request, pk):
# #         user = get_object_or_404(User, pk=pk)
# #         if Follow.objects.filter(user=request.user, author=user).exists():
# #             return Response(data="""Error: You have already subscribed
# #                              to this user.""",
# #                             status=HTTP_400_BAD_REQUEST)
# #         elif request.user == user:
# #             return Response(data="Error: You can't subscribe to yourself.",
# #                             status=HTTP_400_BAD_REQUEST)

# #         Follow.objects.create(user=request.user, author=user)
# #         serializer = SubsSerializer(user)
# #         return Response(serializer.data)

# #     def delete(self, request, pk):
# #         user = get_object_or_404(User, pk=pk)
# #         if Follow.objects.filter(user=request.user, author=user).exists():
# #             Follow.objects.filter(user=request.user, author=user).delete()
# #             return Response(status=HTTP_204_NO_CONTENT)
# #         return Response(status=HTTP_400_BAD_REQUEST)


# # class RecipeInFavoriteView(APIView):
# #     """Взаимодействие с добавлением в избранное рецепта
# #     и его удалением
# #     Эндпоинт api/recipes/<int:pk>/favorite/"""
# #     permission_classes = (permissions.IsAuthenticated,)

# #     def post(self, request, pk):
# #         recipe = get_object_or_404(Recipe, pk=pk)

# #         if FavoriteRecipe.objects.filter(user=request.user,
# #                                          recipe=recipe).exists():
# #             return Response(data="""Error: The recipe is already in the
# #                              favorites.""",
# #                             status=HTTP_400_BAD_REQUEST)

# #         serializer = RecipeInFavoriteAndShoppingCartSerializer(recipe)
# #         FavoriteRecipe.objects.create(user=request.user, recipe=recipe)
# #         return Response(serializer.data)

# #     def delete(self, request, pk):
# #         recipe = get_object_or_404(Recipe, pk=pk)
# #         if FavoriteRecipe.objects.filter(user=request.user,
# #                                          recipe=recipe).exists():
# #             FavoriteRecipe.objects.filter(user=request.user,
# #                                           recipe=recipe).delete()
# #             return Response(status=HTTP_204_NO_CONTENT)
# #         return Response(data="""Error: The recipe is not in the favorites.""",
# #                         status=HTTP_400_BAD_REQUEST)


# # class RecipeInShoppingCartView(APIView):
# #     """Взаимодействие с добавлением, удалением рецепта из списка покупок
# #     Эндпоинт /api/recipes/<int:pk>/shopping_cart/"""
# #     permission_classes = (permissions.IsAuthenticated,)

# #     def post(self, request, pk):
# #         recipe = get_object_or_404(Recipe, pk=pk)

# #         if ShoppingCart.objects.filter(user=request.user,
# #                                        recipe=recipe).exists():
# #             return Response(data="""Error: The recipe is already in the
# #                              shopping cart.""",
# #                             status=HTTP_400_BAD_REQUEST)

# #         serializer = RecipeInFavoriteAndShoppingCartSerializer(recipe)
# #         ShoppingCart.objects.create(user=request.user, recipe=recipe)
# #         return Response(serializer.data)

# #     def delete(self, request, pk):
# #         recipe = get_object_or_404(Recipe, pk=pk)
# #         if ShoppingCart.objects.filter(user=request.user,
# #                                        recipe=recipe).exists():
# #             ShoppingCart.objects.filter(user=request.user,
# #                                         recipe=recipe).delete()
# #             return Response(status=HTTP_204_NO_CONTENT)
# #         return Response(data="Error: The recipe is not in the shopping cart.",
# #                         status=HTTP_400_BAD_REQUEST)


# # class LoadShoppingCart(APIView):
# #     """Взаимодействие с скачиванием рецепта, в котором повторяющиеся
# #     ингредиенты соеденены
# #     Эндпоинт /api/recipes/download_shopping_cart"""
# #     permission_classes = (permissions.IsAuthenticated,)

# #     def get(self, request):
# #         ingredients = IngredientInRecipeAmount.objects.filter(
# #             recipe__recipeinshopcart__user=request.user
# #         )
# #         result = {}
# #         serializer = IngredientWithAmountSerializer(ingredients, many=True)
# #         for data in serializer.data:
# #             name_ingredient = data.get('name')
# #             amount_ingredient = data.get('amount')
# #             measurement_unit = data.get('measurement_unit')
# #             if name_ingredient in result:
# #                 result[name_ingredient][0] += amount_ingredient
# #                 continue
# #             result[name_ingredient] = [amount_ingredient, measurement_unit]

# #         # запись списка покупок в файл
# #         # с отправкой его пользователю
# #         # и последующим удалением
# #         text_for_file = 'Список покупок:\n'
# #         for key, value in result.items():
# #             text_for_file += f'{key.capitalize()} ({value[1]}) - {value[0]}\n'
# #         current_datetime = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
# #         full_file_name = os.path.join(SHOPPING_ROOT,
# #                                       f'shop_user{request.user}_'
# #                                       f'date{current_datetime}.txt')
# #         with open(full_file_name, "w+", encoding='UTF-8') as shop_file:
# #             shop_file.write(text_for_file)
# #         shop_file = open(full_file_name, 'r', encoding='UTF-8')
# #         response = HttpResponse(content=shop_file, content_type='text/txt')
# #         filename = 'shopitems.txt'
# #         response['Content-Disposition'] = ('attachment; filename="{}"'
# #                                            .format(filename))
# #         shop_file.close()
# #         os.remove(full_file_name)
# #         return response
