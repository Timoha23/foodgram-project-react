from django.contrib import admin
from .models import (Ingredient, Tag, Recipe,
                     IngredientInRecipeAmount, FavoriteRecipe,
                     ShoppingCart)


# ДЛЯ ТОГО ЧТОБЫ ИНГРИДИЕНТЫ ОТОБРАЖАЛИСЬ ПРИ СОЗДАНИИ РЕЦЕПТА
class IngredientsInLine(admin.TabularInline):
    model = IngredientInRecipeAmount
    extra = 1


class RecipeAdminConfig(admin.ModelAdmin):
    inlines = [IngredientsInLine]
    list_display = ('author', 'name', 'count_recipe_add')
    list_filter = ('tags',)
    search_fields = ('author__username', 'name')

    def count_recipe_add(self, obj):
        count = FavoriteRecipe.objects.filter(recipe=obj).count()
        return count

    count_recipe_add.short_description = 'Количество отметок "в избранное"'


class IngredientAdminConfig(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class TagAdminConfig(admin.ModelAdmin):
    list_display = ('name', 'hex_code', 'slug')


class FavoriteRecipeAdminConfig(admin.ModelAdmin):
    list_display = ('recipe', 'user')


class ShoppingCartAdminConfig(admin.ModelAdmin):
    list_display = ('recipe', 'user')


class IngredientInRecipeAdminConfig(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount_ingredient',)
    search_fields = ('recipe',)


# Register your models here.
admin.site.register(Ingredient, IngredientAdminConfig)
admin.site.register(Tag, TagAdminConfig)
admin.site.register(Recipe, RecipeAdminConfig)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdminConfig)
admin.site.register(ShoppingCart, ShoppingCartAdminConfig)
admin.site.register(IngredientInRecipeAmount, IngredientInRecipeAdminConfig)
