# from rest_framework import serializers
# from users.models import User, Follow
# from recipes.models import (Ingredient, Tag, Recipe, IngredientInRecipeAmount,
#                             FavoriteRecipe, ShoppingCart)
# from drf_extra_fields.fields import Base64ImageField
# from django.shortcuts import get_object_or_404


# # class InfoUserSerializer(serializers.ModelSerializer):
# #     is_subscribed = serializers.SerializerMethodField('get_sub_status')

# #     class Meta:
# #         model = User
# #         fields = (
# #             'email',
# #             'id',
# #             'username',
# #             'first_name',
# #             'last_name',
# #             'is_subscribed'
# #         )

# #     def get_sub_status(self, obj):
# #         try:
# #             request_user = self.context['request'].user
# #             user = obj
# #             return Follow.objects.filter(
# #                 author=user,
# #                 user=request_user
# #             ).exists()
# #         except (KeyError, TypeError):
# #             return False


# # class SingUpSerializer(serializers.ModelSerializer):
# #     id = serializers.IntegerField(read_only=True, default=0)

# #     class Meta:
# #         model = User
# #         fields = (
# #             'email',
# #             'id',
# #             'password',
# #             'username',
# #             'first_name',
# #             'last_name'
# #         )


# # class SetPasswordSerializer(serializers.Serializer):
# #     new_password = serializers.CharField(max_length=154)
# #     current_password = serializers.CharField(max_length=154)


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ('id', 'name', 'measurement_unit')


# class TagSerializer(serializers.ModelSerializer):
#     color = serializers.SerializerMethodField('get_hex_code')

#     class Meta:
#         model = Tag
#         fields = ('id', 'name', 'color', 'slug')

#     def get_hex_code(self, obj):
#         return obj.hex_code


# class IngredientWithAmountSerializer(serializers.ModelSerializer):
#     """Вложенный сериализатор для GetRecipeSerializer"""
#     name = serializers.CharField(
#         read_only=True,
#         source='ingredient.name'
#     )
#     measurement_unit = serializers.CharField(
#         read_only=True,
#         source='ingredient.measurement_unit'
#     )
#     amount = serializers.CharField(
#         read_only=True,
#         source='amount_ingredient',
#     )

#     class Meta:
#         model = IngredientInRecipeAmount
#         fields = ('id', 'name', 'measurement_unit', 'amount')


# class GetRecipeSerializer(serializers.ModelSerializer):

#     tags = TagSerializer(many=True)
#     is_favorited = serializers.SerializerMethodField('get_is_favorite')
#     is_in_shopping_cart = serializers.SerializerMethodField(
#         'get_is_in_shopping_cart'
#     )
#     author = InfoUserSerializer()
#     ingredients = IngredientWithAmountSerializer(many=True,
#                                                  source='ingredientinrecipe')

#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'tags',
#             'author',
#             'ingredients',
#             'is_favorited',
#             'is_in_shopping_cart',
#             'name',
#             'image',
#             'text',
#             'cooking_time',
#         )

#     def get_is_favorite(self, obj):
#         try:
#             request_user = self.context['request'].user
#             recipe = obj
#             return FavoriteRecipe.objects.filter(
#                 recipe=recipe,
#                 user=request_user
#             ).exists()
#         except (KeyError, TypeError):
#             return False

#     def get_is_in_shopping_cart(self, obj):
#         try:
#             request_user = self.context['request'].user
#             recipe = obj
#             return ShoppingCart.objects.filter(
#                 recipe=recipe,
#                 user=request_user
#             ).exists()
#         except (KeyError, TypeError):
#             return False


# class IngredientToRecipeSerializer(serializers.ModelSerializer):
#     """Вложенный сериализатор для PostRecipeSerializer"""
#     name = serializers.CharField(read_only=True, source='ingredient.name')
#     id = serializers.IntegerField(source="ingredient.id")
#     amount = serializers.IntegerField(source="amount_ingredient")
#     measurement_unit = serializers.CharField(
#         read_only=True,
#         source="ingredient.measurement_unit"
#     )

#     class Meta:
#         model = IngredientInRecipeAmount
#         fields = ('id', 'name', 'measurement_unit', 'amount',)


# class PostRecipeSerializer(serializers.ModelSerializer):
#     ingredients = IngredientToRecipeSerializer(many=True,
#                                                source='ingredientinrecipe')
#     image = Base64ImageField()
#     author = InfoUserSerializer(read_only=True)
#     is_favorited = serializers.SerializerMethodField('get_is_favorite')
#     is_in_shopping_cart = serializers.SerializerMethodField(
#         'get_is_in_shopping_cart'
#     )

#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'tags',
#             'author',
#             'ingredients',
#             'is_favorited',
#             'is_in_shopping_cart',
#             'name',
#             'image',
#             'text',
#             'cooking_time',
#         )

#     def get_is_favorite(self, obj):
#         try:
#             request_user = self.context['request'].user
#             recipe = obj
#             return FavoriteRecipe.objects.filter(
#                 recipe=recipe,
#                 user=request_user
#             ).exists()
#         except (KeyError, TypeError):
#             return False

#     def get_is_in_shopping_cart(self, obj):
#         try:
#             request_user = self.context['request'].user
#             recipe = obj
#             return ShoppingCart.objects.filter(
#                 recipe=recipe,
#                 user=request_user
#             ).exists()
#         except (KeyError, TypeError):
#             return False

#     def validate(self, attrs):
#         ingredients = self.initial_data.get('ingredients')
#         if not ingredients:
#             raise serializers.ValidationError(
#                 {'ingredients':
#                  'At least 1 ingredient must be present in the recipe'}
#             )
#         for ingredient in ingredients:
#             if ingredient.get('amount') < 1:
#                 raise serializers.ValidationError(
#                     {'amount':
#                      'The count of ingredients cannot be less than 1'}
#                 )
#         return attrs

#     def create(self, validated_data):
#         author = self.context['request'].user
#         tags = validated_data.get("tags")
#         ingredients = validated_data.get('ingredientinrecipe')
#         name = validated_data.get('name')
#         cooking_time = validated_data.get('cooking_time')
#         image = validated_data.get('image')
#         text = validated_data.get('text')
#         recipe = Recipe.objects.create(
#             name=name,
#             text=text,
#             image=image,
#             author=author,
#             cooking_time=cooking_time
#         )
#         for tag in tags:
#             tag_obj = Tag.objects.get(id=tag.id)
#             recipe.tags.add(tag_obj)
#         for ingredient in ingredients:
#             ingredient_id = ingredient.get('ingredient').get('id')
#             ingredient_obj = get_object_or_404(Ingredient, id=ingredient_id)
#             amount = ingredient.get('amount_ingredient')

#             IngredientInRecipeAmount.objects.create(
#                 ingredient=ingredient_obj,
#                 recipe=recipe,
#                 amount_ingredient=amount,
#             )
#             recipe.ingredients.add(ingredient_obj)
#         return recipe

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         ingredients = validated_data.get('ingredientinrecipe')
#         tags = validated_data.get('tags')
#         instance.text = validated_data.get('text', instance.text)
#         instance.image = validated_data.get('image', instance.image)
#         instance.cooking_time = validated_data.get('cooking_time',
#                                                    instance.cooking_time)
#         ingredient_objects = []
#         instance.tags.set(tags)
#         # удаляем старые данные о ингредиентах в рецепте и сохраняем новые
#         IngredientInRecipeAmount.objects.filter(recipe=instance).delete()
#         for ingredient in ingredients:
#             ingredient_id = ingredient.get('ingredient').get('id')
#             ingredient_obj = get_object_or_404(Ingredient, id=ingredient_id)
#             amount = ingredient['amount_ingredient']
#             IngredientInRecipeAmount.objects.create(
#                 ingredient=ingredient_obj,
#                 recipe=instance,
#                 amount_ingredient=amount,
#             )
#             ingredient_objects.append(ingredient_obj)
#         instance.ingredients.set(ingredient_objects)
#         instance.save()
#         return instance


# # class GetRecipeForFollow(serializers.ModelSerializer):
# #     """Вложенный сериализатор для SubSerialzier"""
# #     class Meta:
# #         model = Recipe
# #         fields = ('id', 'name', 'image', 'cooking_time')


# # class FollowSerializer(serializers.ModelSerializer):
# #     recipes = serializers.SerializerMethodField('get_recipes')
# #     recipes_count = serializers.SerializerMethodField('get_recipes_count')
# #     is_subscribed = serializers.SerializerMethodField('get_sub_status')

# #     class Meta:
# #         model = User

# #         fields = (
# #             "email",
# #             "id",
# #             "username",
# #             "first_name",
# #             "last_name",
# #             "is_subscribed",
# #             "recipes",
# #             "recipes_count",
# #         )

# #     def get_recipes_count(self, obj):
# #         recipes_count = Recipe.objects.filter(author=obj).count()
# #         return recipes_count

# #     def get_sub_status(self, obj):
# #         return True

# #     def get_recipes(self, obj):
# #         try:
# #             query_params = self.context.get('request').query_params
# #         except AttributeError:
# #             recipes = obj.author.all()
# #             return GetRecipeForFollow(recipes, many=True).data
# #         if 'recipes_limit' in query_params:
# #             recipes_limit = int(query_params.get('recipes_limit'))
# #             recipes = obj.author.all()[:recipes_limit]
# #             return GetRecipeForFollow(recipes, many=True).data

# #         recipes = obj.author.all()
# #         return GetRecipeForFollow(recipes, many=True).data


# class RecipeInFavoriteAndShoppingCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = ('id', 'name', 'image', 'cooking_time')
