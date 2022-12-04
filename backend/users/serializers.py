from rest_framework import serializers
from .models import User, Follow
from recipes.models import Recipe


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
            return Follow.objects.filter(
                author=user,
                user=request_user
            ).exists()
        except (KeyError, TypeError):
            return False


class SingUpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'password',
            'username',
            'first_name',
            'last_name'
        )


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=154)
    current_password = serializers.CharField(max_length=154)


class GetRecipeForFollow(serializers.ModelSerializer):
    """Вложенный сериализатор для FollowSerialzier"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField('get_recipes')
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

    def get_recipes(self, obj):
        try:
            query_params = self.context.get('request').query_params
        except AttributeError:
            recipes = obj.author.all()
            return GetRecipeForFollow(recipes, many=True).data
        if 'recipes_limit' in query_params:
            recipes_limit = int(query_params.get('recipes_limit'))
            recipes = obj.author.all()[:recipes_limit]
            return GetRecipeForFollow(recipes, many=True).data

        recipes = obj.author.all()
        return GetRecipeForFollow(recipes, many=True).data
