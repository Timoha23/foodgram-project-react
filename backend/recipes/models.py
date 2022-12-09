from django.core import validators
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(
        max_length=128,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=32,
        verbose_name='Имя тега',
        unique=True
    )
    hex_code = models.CharField(
        max_length=32,
        verbose_name='Цвет',
        unique=True,
        validators=(
            validators.RegexValidator(regex=r'^#[a-fA-F0-9]{6}$'),
        )
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""
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
        related_name='tags',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1,
            ),
            validators.MaxValueValidator(
                10_000,
            ),
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientInRecipeAmount(models.Model):
    """Модель количества ингредиентов в рецепте"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredientinrecipe',
        verbose_name='Рецепт'
    )
    amount_ingredient = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            validators.MinValueValidator(
                0,
            ),
            validators.MaxValueValidator(
                10_000,
            ),
        )
    )

    class Meta:
        verbose_name = 'Рецепт с ингредиентом'
        verbose_name_plural = 'Рецепты с ингредиентами'

    def __str__(self):
        return self.recipe


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return self.recipe


class ShoppingCart(models.Model):
    """Модель списка покупок"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeinshopcart',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return self.recipe
