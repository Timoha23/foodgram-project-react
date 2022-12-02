from django.db import models
from users.models import User
from django.core import validators


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128
    )
    measurement_unit = models.CharField(
        max_length=20
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=32
    )
    hex_code = models.CharField(
        max_length=32
    )
    slug = models.SlugField(
        unique=True
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author'
    )
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='recipe/img')
    text = models.CharField(max_length=1024)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipeAmount',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1,
            ),
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )


class IngredientInRecipeAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe'
    )
    amount_ingredient = models.PositiveSmallIntegerField(
        # validators=(
        #     validators.MinValueValidator(1,),
        # )
    )


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeinshopcart'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
