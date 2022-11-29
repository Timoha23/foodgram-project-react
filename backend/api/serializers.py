from rest_framework import serializers
from users.models import User, Follow
from recipes.models import Ingredient, Tag, Recipe, IngredientInRecipeAmount
from drf_extra_fields.fields import Base64ImageField


class InfoUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_sub_status')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_sub_status(self, obj):
        try:
            request_user = self.context['request'].user
            user = obj
            is_subscribed = Follow.objects.filter(author=user, user=request_user)
            if is_subscribed.count() == 0:
                return False
            return True
        except TypeError:
            return False


class SingUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name', 'last_name')


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=154)
    current_password = serializers.CharField(max_length=154)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField('get_hex_code')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

    def get_hex_code(self, obj):
        return obj.hex_code


class IngredientWithAmountSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для GetRecipeSerializer"""
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipeAmount
        fields = ('id', 'name', 'measurement_unit', 'amount_ingredient')


class GetRecipeSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField('get_is_favorite')
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')
    author = InfoUserSerializer()
    ingredients = IngredientWithAmountSerializer(many=True, source='ingredientinrecipe')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorite(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class IngredientToRecipeSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор для PostRecipeSerializer"""
    name = serializers.CharField(read_only=True, source='ingredient.name')
    
    class Meta:
        model = IngredientInRecipeAmount
        fields = ('ingredient', 'amount_ingredient', 'name',)


class PostRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientToRecipeSerializer(many=True, source='ingredientinrecipe')
    image = Base64ImageField()
    author = InfoUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'name',
            'text',
            'cooking_time',
            'image',
            'ingredients',
            'cooking_time'
        )

    def create(self, validated_data):
        author = self.context['request'].user
        tags = validated_data.get("tags")
        ingredients = validated_data.get('ingredientinrecipe')
        name = validated_data.get('name')
        cooking_time = validated_data.get('cooking_time')
        image = validated_data.get('image')
        text = validated_data.get('text')
        recipe = Recipe.objects.create(
            name=name,
            text=text,
            image=image,
            author=author,
            cooking_time=cooking_time
        )
        for tag in tags:
            tag_obj = Tag.objects.get(id=tag.id)
            recipe.tags.add(tag_obj)
        for ingredient in ingredients:
            ingredient_id = ingredient.get('ingredient').id
            ingredient_obj = Ingredient.objects.get(id=ingredient_id)
            amount = ingredient['amount_ingredient']

            IngredientInRecipeAmount.objects.create(
                ingredient=ingredient_obj,
                recipe=recipe,
                amount_ingredient=amount,
            )
            recipe.ingredients.add(ingredient_obj)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        ingredients = validated_data.get('ingredientinrecipe')
        tags = validated_data.get('tags')
        instance.text = validated_data.get('text')
        instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')
        ingredient_objects = []
        instance.tags.set(tags)
        # удаляем старые данные о ингредиентах в рецепте и сохраняем новые
        IngredientInRecipeAmount.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            ingredient_id = ingredient.get('ingredient').id
            ingredient_obj = Ingredient.objects.get(id=ingredient_id)
            amount = ingredient['amount_ingredient']
            IngredientInRecipeAmount.objects.create(
                ingredient=ingredient_obj,
                recipe=instance,
                amount_ingredient=amount,
            )
            ingredient_objects.append(ingredient_obj)
        instance.ingredients.set(ingredient_objects)
        instance.save()

        return instance


class GetRecipeForSubs(serializers.ModelSerializer):
    """Вложенный сериализатор для GetSubSerialzier"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class GetSubsSerializer(serializers.ModelSerializer):
    recipes = GetRecipeForSubs(many=True, source='author')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')
    is_subscribed = serializers.SerializerMethodField('get_sub_status')

    class Meta:
        model = User

        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        recipes_count = Recipe.objects.filter(author=obj).count()
        return recipes_count

    def get_sub_status(self, obj):
        return True


















# class IngredientWithAmountSerializer(serializers.ModelSerializer):
#     # measurement_unit = serializers.CharField(read_only=True, default='gramm')
#     class Meta:
#         model = IngredientInRecipeAmount
#         fields = ('id','amount_ingredient', 'recipe_id')


# class PostRecipeSerializer(serializers.ModelSerializer):
#     pass
# # class AmountIngredientSerializer(serializers.ModelSerializer):

# #     amount = serializers.SerializerMethodField('get_amount')
# #     class Meta:
# #         model = Ingredient
# #         fields = ('id', 'name', 'measurement_unit', 'amount')

# #     def get_amount(self, obj):
# #         print(obj)
# #         print(obj.__dict__)
# #         ingredients = AmountIngredient.objects.get(ingredient=obj.id)
# #         print(ingredients.__dict__)
# #         return ingredients.amount_ingredient


# class RecipeSerializer(serializers.ModelSerializer):
#     author = InfoUserSerializer()
#     ingredients = serializers.SerializerMethodField('get_ingredients')
#     tags = TagSerializer(many=True)
#     is_favorited = serializers.SerializerMethodField('get_favorited_status')
#     is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart_status')

#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'description', 'cooking_time')

#     def get_ingredients(self, obj):
#         ingredients = IngredientInRecipeAmount.objects.filter(recipe=obj)
#         return IngredientWithAmountSerializer(ingredients, many=True)

#     def get_favorited_status(self, obj):
#         return False

#     def get_is_in_shopping_cart_status(self, obj):
#         return False
