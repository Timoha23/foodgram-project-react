import django_filters as filter
from rest_framework import filters
from recipes.models import Tag, Recipe


class RecipeFilter(filter.FilterSet):
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filter.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = filter.NumberFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == 1 and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1 and not user.is_anonymous:
            return queryset.filter(recipeinshopcart__user=user)
        return queryset.all()


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'
