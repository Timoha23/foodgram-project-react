from django.contrib import admin
from .models import Ingredient, Tag, Recipe, IngredientInRecipeAmount


# ДЛЯ ТОГО ЧТОБЫ ИНГРИДИЕНТЫ ОТОБРАЖАЛИСЬ ПРИ СОЗДАНИИ РЕЦЕПТА
class IngredientsInLine(admin.TabularInline):
    model = IngredientInRecipeAmount
    extra = 1

class IngredientsForAdmin(admin.ModelAdmin):
    inlines = [IngredientsInLine]

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe, IngredientsForAdmin)