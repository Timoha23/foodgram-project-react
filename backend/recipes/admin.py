from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientInRecipeAmount,
                     Recipe, ShoppingCart, Tag)


# ДЛЯ ТОГО ЧТОБЫ ИНГРИДИЕНТЫ ОТОБРАЖАЛИСЬ ПРИ СОЗДАНИИ РЕЦЕПТА
class IngredientsInLine(admin.TabularInline):
    """Реализация отображения ингредиентов при создании рецепта"""
    model = IngredientInRecipeAmount
    extra = 1


class RecipeAdminConfig(admin.ModelAdmin):
    """Конфигурация отображения рецепта в админ-панели"""
    inlines = [IngredientsInLine]
    list_display = ('author', 'name', 'count_recipe_add')
    list_filter = ('tags',)
    search_fields = ('author__username', 'name')

    def count_recipe_add(self, obj):
        count = FavoriteRecipe.objects.filter(recipe=obj).count()
        return count

    count_recipe_add.short_description = 'Количество отметок "в избранное"'


class IngredientAdminConfig(admin.ModelAdmin):
    """Конфигурация отображения ингредиентов в админ-панели"""
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class TagAdminConfig(admin.ModelAdmin):
    """Конфигурация отображения тегов в админ-панели"""
    list_display = ('name', 'hex_code', 'slug')


class FavoriteRecipeAdminConfig(admin.ModelAdmin):
    """Конфигурация отображения рецептов, добавленных в избранное
    в админ-панели"""
    list_display = ('recipe', 'user')


class ShoppingCartAdminConfig(admin.ModelAdmin):
    """Конфигурация отображения списка покупок в админ-панели"""
    list_display = ('recipe', 'user')


class IngredientInRecipeAdminConfig(admin.ModelAdmin):
    """Конфигурация отображения ингредиентов, входящих в рецепт,
    в админ-панели"""
    list_display = ('ingredient', 'recipe', 'amount_ingredient',)
    search_fields = ('recipe',)


# Register your models here.
admin.site.register(Ingredient, IngredientAdminConfig)
admin.site.register(Tag, TagAdminConfig)
admin.site.register(Recipe, RecipeAdminConfig)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdminConfig)
admin.site.register(ShoppingCart, ShoppingCartAdminConfig)
admin.site.register(IngredientInRecipeAmount, IngredientInRecipeAdminConfig)
